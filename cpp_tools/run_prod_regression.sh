#!/bin/bash
#
# Run tearsheet regression studies on the prod server via HTTP API.
#
# Flow:
#   1. Create study definitions on prod server
#   2. Execute each definition (server runs the study)
#   3. Poll for completion
#   4. Resync EFS data from S3
#   5. Run local generate_job_data with same definitions to produce schema.json + Arrow
#   6. Compare prod .pb tearsheets with local schema.json output
#
# Usage:
#   ./run_prod_regression.sh                    # Run all test definitions
#   ./run_prod_regression.sh --token <TOKEN>    # Provide auth token explicitly
#   ./run_prod_regression.sh --resync-only      # Skip execution, just resync + compare
#   ./run_prod_regression.sh --list             # List existing executions on prod
#
# Prerequisites:
#   - AWS CLI configured (for S3 sync)
#   - Cognito auth token (obtained via Portal login or CLI)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPERIMENT_DIR="$HOME/EpochDev/ClaudeCodeResearch/project/experiments/tearsheet_regression"
PROD_DATA="$EXPERIMENT_DIR/prod_data/epoch-prod"
REGEN_DIR="$EXPERIMENT_DIR/regenerated"
RESULTS_DIR="$EXPERIMENT_DIR/results"
GENERATOR="$HOME/EpochDev/EpochBackend/build/bin/generate_job_data"
MARKET_DATA="$HOME/EpochDev/ClaudeCodeResearch/project/market_data"

PROD_URL="https://prod-server.epoch.trade"
DEV_URL="https://dev-server.epoch.trade"
BASE_URL="${EPOCH_SERVER_URL:-$PROD_URL}"

S3_BUCKET="epoch-db"
S3_PREFIX="efs-sync-prod/epoch-prod"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_section() { echo -e "\n${BLUE}=== $1 ===${NC}"; }

# ============================================================================
# Auth token
# ============================================================================

TOKEN=""
RESYNC_ONLY=false
LIST_ONLY=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --token)
            TOKEN="$2"; shift 2 ;;
        --resync-only)
            RESYNC_ONLY=true; shift ;;
        --list)
            LIST_ONLY=true; shift ;;
        --dev)
            BASE_URL="$DEV_URL"; shift ;;
        --url)
            BASE_URL="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: $0 [--token TOKEN] [--resync-only] [--list] [--dev] [--url URL]"
            exit 0 ;;
        *)
            log_error "Unknown option: $1"; exit 1 ;;
    esac
done

COGNITO_AUTH="$HOME/EpochDev/EpochAI/tools/cognito_auth.py"

if [[ -z "$TOKEN" && "$RESYNC_ONLY" == false ]]; then
    # Try environment variable first
    TOKEN="${EPOCH_AUTH_TOKEN:-}"

    # Try cognito_auth.py auto-refresh
    if [[ -z "$TOKEN" && -f "$COGNITO_AUTH" ]]; then
        log_info "Getting token via cognito_auth.py..."
        TOKEN=$(python3 "$COGNITO_AUTH" token 2>/dev/null) || true
    fi

    if [[ -z "$TOKEN" ]]; then
        log_error "Auth token required. Options:"
        echo "  1. Login first:   python3 $COGNITO_AUTH login"
        echo "  2. Pass directly: $0 --token <TOKEN>"
        echo "  3. Environment:   EPOCH_AUTH_TOKEN=<token> $0"
        exit 1
    fi
    log_info "Token obtained (${#TOKEN} chars)"
fi

api_call() {
    local method="$1" path="$2" data="${3:-}"
    local url="${BASE_URL}${path}"
    local args=(-s -w "\n%{http_code}" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json")

    if [[ -n "$data" ]]; then
        args+=(-X "$method" -d "$data")
    else
        args+=(-X "$method")
    fi

    local response
    response=$(curl "${args[@]}" "$url")
    local http_code=$(echo "$response" | tail -1)
    local body=$(echo "$response" | head -n -1)

    if [[ "$http_code" -ge 400 ]]; then
        echo "ERROR:$http_code:$body"
        return 1
    fi
    echo "$body"
}

# ============================================================================
# List existing executions
# ============================================================================

if $LIST_ONLY; then
    log_section "Existing Executions on $(basename $BASE_URL)"
    result=$(api_call GET "/api/v1/studies/executions")
    echo "$result" | python3 -c "
import sys, json
data = json.load(sys.stdin)
execs = data if isinstance(data, list) else data.get('executions', data.get('data', []))
for e in execs[:20]:
    eid = e.get('execution_id', e.get('id', '?'))
    status = e.get('status', '?')
    name = e.get('name', e.get('definition_name', '?'))
    print(f'  {eid[:20]:22s} {status:12s} {name}')
" 2>/dev/null || echo "$result"
    exit 0
fi

# ============================================================================
# Test definitions covering all chart types
# ============================================================================

# These are minimal EpochScript scripts designed to exercise specific chart/table types.
# Each produces at least one tearsheet with the target chart type.

DEFINITIONS_DIR="$EXPERIMENT_DIR/regression_definitions"
mkdir -p "$DEFINITIONS_DIR"

# Helper to create a definition JSON
create_def() {
    local filename="$1" name="$2" assets="$3" source="$4" timeframe="${5:-1D}"
    cat > "$DEFINITIONS_DIR/$filename" << DEFEOF
{
    "name": "$name",
    "description": "Regression test: $name",
    "data": {
        "assets": [$assets],
        "source": "polygon",
        "cache_dir": "$MARKET_DATA"
    },
    "source": $(python3 -c "import json; print(json.dumps('''$source'''))"),
    "global_timeframe": "$timeframe"
}
DEFEOF
}

# ============================================================================
# Step 1: Execute definitions on server
# ============================================================================

# Pick 5 diverse definitions that already exist on prod:
# - 2 research studies (SPY, multi-asset)
# - 2 campaigns (pairs trade, portfolio)
# - 1 research (BTC)
# These cover: Lines, Bar, Scatter, HeatMap, Histogram, NumericLines, Cards, Summary, Detailed

# Override: pass specific IDs via REGRESSION_DEF_IDS env var (comma-separated)
if [[ -n "${REGRESSION_DEF_IDS:-}" ]]; then
    IFS=',' read -ra DEF_IDS <<< "$REGRESSION_DEF_IDS"
else
    # Auto-discover: find 5 most recent definitions that have successful executions
    log_info "Discovering recent definitions with executions..."
    DEF_IDS=()

    all_defs=$(api_call GET "/api/v1/studies/definitions" 2>&1)
    discovered=$(echo "$all_defs" | python3 -c "
import sys, json
data = json.load(sys.stdin)
defs = data if isinstance(data, list) else data.get('definitions', data.get('data', []))
# Take 5 most recent
for d in defs[:5]:
    did = d.get('definition_id', d.get('id', ''))
    name = d.get('name', '?')
    if did:
        print(f'{did}|{name}')
" 2>/dev/null)

    while IFS='|' read -r did dname; do
        [[ -n "$did" ]] && DEF_IDS+=("$did") && log_info "  $dname ($did)"
    done <<< "$discovered"
fi

log_info "Will execute ${#DEF_IDS[@]} definitions"

if ! $RESYNC_ONLY; then
    log_section "Executing ${#DEF_IDS[@]} Studies on Server"

    EXECUTION_IDS=()

    for def_id in "${DEF_IDS[@]}"; do
        echo -n "  Executing $def_id... "

        exec_body="{\"id\": \"$def_id\", \"period\": {\"start\": \"2020-01-01\", \"end\": \"2025-12-31\"}}"
        exec_result=$(api_call POST "/api/v1/studies/executions" "$exec_body" 2>&1) || true

        if echo "$exec_result" | grep -q "ERROR:"; then
            echo -e "${YELLOW}failed${NC}"
        else
            exec_id=$(echo "$exec_result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('execution_id', d.get('id', '')))" 2>/dev/null || echo "")
            if [[ -n "$exec_id" ]]; then
                echo -e "${GREEN}OK${NC} ($exec_id)"
                EXECUTION_IDS+=("$exec_id")
            else
                echo -e "${YELLOW}no id${NC}"
            fi
        fi
    done

    log_info "${#EXECUTION_IDS[@]} executions started"

    # ========================================================================
    # Step 2: Poll for completion
    # ========================================================================

    if [[ ${#EXECUTION_IDS[@]} -gt 0 ]]; then
        log_section "Waiting for Executions (${#EXECUTION_IDS[@]} jobs)"

        MAX_WAIT=600  # 10 minutes
        POLL_INTERVAL=15
        elapsed=0

        while [[ $elapsed -lt $MAX_WAIT ]]; do
            completed=0; failed=0; pending=0
            for exec_id in "${EXECUTION_IDS[@]}"; do
                status=$(api_call GET "/api/v1/studies/executions/$exec_id" 2>&1 | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null || echo "unknown")
                case "$status" in
                    completed|Completed|COMPLETED) completed=$((completed+1)) ;;
                    failed|Failed|FAILED) failed=$((failed+1)) ;;
                    *) pending=$((pending+1)) ;;
                esac
            done

            echo "  completed=$completed failed=$failed pending=$pending (${elapsed}s/${MAX_WAIT}s)"

            if [[ $pending -eq 0 ]]; then
                log_info "All executions done! ($completed completed, $failed failed)"
                break
            fi

            sleep "$POLL_INTERVAL"
            elapsed=$((elapsed + POLL_INTERVAL))
        done

        if [[ $elapsed -ge $MAX_WAIT ]]; then
            log_warn "Timeout. Proceeding with resync anyway."
        fi
    fi
fi

# ============================================================================
# Step 4: Resync EFS data from S3
# ============================================================================

log_section "Syncing Prod EFS from S3"

log_info "Syncing s3://$S3_BUCKET/$S3_PREFIX/ → $PROD_DATA/"
aws s3 sync "s3://$S3_BUCKET/$S3_PREFIX/" "$PROD_DATA/" --quiet

TOTAL_PBS=$(find "$PROD_DATA" -name "tearsheet.pb" | wc -l)
TOTAL_CONFIGS=$(find "$PROD_DATA" -name "config.json" | wc -l)
log_info "Synced: $TOTAL_PBS tearsheets, $TOTAL_CONFIGS configs"

# ============================================================================
# Step 5: Re-run locally with generate_job_data for schema.json + Arrow
# ============================================================================

log_section "Regenerating Locally (schema.json + Arrow)"

rm -rf "$REGEN_DIR" "$RESULTS_DIR"
mkdir -p "$REGEN_DIR/definitions/test_runner" "$RESULTS_DIR"

PASSED=0; FAILED=0; SKIPPED=0; TOTAL=0

# Find all studies/campaigns with tearsheets and config.json
find "$PROD_DATA" -name "config.json" | while read config; do
    dir=$(dirname "$config")
    ts_count=$(find "$dir/tearsheets" -name "tearsheet.pb" 2>/dev/null | wc -l)
    [[ "$ts_count" -gt 0 ]] || continue
    echo "$config"
done | sort -t/ -k10 | tail -20 | while IFS= read -r config; do
    dir=$(dirname "$config")
    job_id=$(basename "$dir")
    parent_type=$(echo "$dir" | grep -oP '(research_studies|campaigns)')

    # Clean definition
    def_file="$REGEN_DIR/definitions/test_runner/${job_id}.json"
    python3 -c "
import json
d = json.load(open('$config'))
clean = {'name': d.get('name','$job_id'), 'description': d.get('description',''), 'data': d['data'], 'source': d['source'], 'global_timeframe': d.get('global_timeframe','1D')}
clean['data']['cache_dir'] = '$MARKET_DATA'
with open('$def_file', 'w') as f:
    json.dump(clean, f, indent=2)
" 2>/dev/null || continue

    start=$(python3 -c "import json; d=json.load(open('$config')); print(d.get('period',{}).get('start','2020-01-01'))" 2>/dev/null || echo "2020-01-01")
    end=$(python3 -c "import json; d=json.load(open('$config')); print(d.get('period',{}).get('end','2025-12-31'))" 2>/dev/null || echo "2025-12-31")
    cash=$(python3 -c "import json; d=json.load(open('$config')); c=d.get('cash'); print(c if c else '')" 2>/dev/null)
    name=$(python3 -c "import json; print(json.load(open('$def_file'))['name'][:40])" 2>/dev/null)

    TOTAL=$((TOTAL + 1))
    echo -n "  [$TOTAL] $job_id ($name)... "

    export EPOCH_PROJECT_DIR="$REGEN_DIR"
    extra_args=""
    [[ -n "$cash" ]] && extra_args="--cash $cash"

    if "$GENERATOR" "$def_file" --start "$start" --end "$end" $extra_args --name "$job_id" > "$RESULTS_DIR/${job_id}.log" 2>&1; then
        out_base="$REGEN_DIR/${parent_type:-research_studies}/test_runner/$job_id"
        schemas=$(find "$out_base/tearsheets" -name "schema.json" 2>/dev/null | wc -l)
        arrows=$(find "$out_base/tearsheets" -name "*.arrow" 2>/dev/null | wc -l)
        echo -e "${GREEN}PASS${NC} ($schemas schemas, $arrows arrows)"
        PASSED=$((PASSED + 1))
    else
        error=$(grep -m1 "what():" "$RESULTS_DIR/${job_id}.log" 2>/dev/null | sed 's/.*what(): //')
        echo -e "${RED}FAIL${NC}: ${error:-(check log)}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
log_section "Summary"
echo "  Total:   $TOTAL"
echo -e "  ${GREEN}Passed:${NC}  $PASSED"
echo -e "  ${RED}Failed:${NC}  $FAILED"
echo ""
log_info "Results in: $RESULTS_DIR"
log_info "Regenerated data in: $REGEN_DIR"

# ============================================================================
# Step 6: Structural validation on all new schema.json files
# ============================================================================

log_section "Validating Generated Schemas"

COMPARE_SCRIPT="$EXPERIMENT_DIR/compare_highcharts.mjs"
if [[ -f "$COMPARE_SCRIPT" ]]; then
    mkdir -p "$RESULTS_DIR/phase2"
    VALID=0; INVALID=0

    find "$REGEN_DIR" -name "schema.json" -path "*/tearsheets/*" | while read schema; do
        # Find matching .pb in prod data
        rel_path=$(echo "$schema" | sed "s|$REGEN_DIR/||" | sed 's|/test_runner/|/|' | sed 's|schema.json|tearsheet.pb|')
        old_pb=$(find "$PROD_DATA" -path "*${rel_path##*/tearsheets/}" -name "tearsheet.pb" 2>/dev/null | head -1)

        if [[ -n "$old_pb" ]]; then
            out_file="$RESULTS_DIR/phase2/$(basename $(dirname $(dirname "$schema")))_compare.json"
            result=$(node "$COMPARE_SCRIPT" "$old_pb" "$schema" "$out_file" 2>&1)

            if echo "$result" | grep -q "^PASS"; then
                echo -e "  ${GREEN}PASS${NC} $result"
                VALID=$((VALID + 1))
            else
                echo -e "  ${RED}FAIL${NC} $result"
                INVALID=$((INVALID + 1))
            fi
        fi
    done

    echo ""
    echo "  Valid: $VALID  Invalid: $INVALID"
fi
