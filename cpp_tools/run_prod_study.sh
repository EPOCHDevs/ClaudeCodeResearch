#!/bin/bash
#
# Run a single study definition on the prod server and sync results locally.
#
# Flow:
#   1. Read definition JSON
#   2. Create study definition on prod via API
#   3. Execute it (start + poll for completion)
#   4. Sync job data from S3/EFS
#   5. Copy results to script_templates/research_studies/test_runner/<id>/
#
# Usage:
#   ./run_prod_study.sh <definition.json>                    # Auto-detect dates
#   ./run_prod_study.sh <definition.json> --start 2003-09-10 --end 2026-04-15
#   ./run_prod_study.sh <definition.json> --token <TOKEN>    # Provide token
#   ./run_prod_study.sh <definition.json> --dev               # Use dev server
#   ./run_prod_study.sh <definition.json> --skip-sync         # Don't sync S3
#
# Prerequisites:
#   - AWS CLI configured (for S3 sync)
#   - Cognito auth token (via cognito_auth.py or --token)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$WORKSPACE_ROOT/script_templates/research_studies/test_runner"

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
# Parse args
# ============================================================================

DEF_FILE=""
TOKEN=""
START_DATE=""
END_DATE=""
SKIP_SYNC=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --token)   TOKEN="$2"; shift 2 ;;
        --start)   START_DATE="$2"; shift 2 ;;
        --end)     END_DATE="$2"; shift 2 ;;
        --dev)     BASE_URL="$DEV_URL"; shift ;;
        --url)     BASE_URL="$2"; shift 2 ;;
        --skip-sync) SKIP_SYNC=true; shift ;;
        -h|--help)
            echo "Usage: $0 <definition.json> [--start DATE] [--end DATE] [--token TOKEN] [--dev] [--skip-sync]"
            exit 0 ;;
        *)
            if [[ -z "$DEF_FILE" ]]; then
                DEF_FILE="$1"
            else
                log_error "Unknown option: $1"
                exit 1
            fi
            shift ;;
    esac
done

if [[ -z "$DEF_FILE" || ! -f "$DEF_FILE" ]]; then
    log_error "Definition file required. Usage: $0 <definition.json>"
    exit 1
fi

DEF_ID=$(python3 -c "from pathlib import Path; print(Path('$DEF_FILE').stem)")
DEF_NAME=$(python3 -c "import json; print(json.load(open('$DEF_FILE'))['name'])")

# Default dates
[[ -z "$START_DATE" ]] && START_DATE="2003-09-10"
[[ -z "$END_DATE" ]]   && END_DATE="2026-04-15"

log_info "Definition: $DEF_ID"
log_info "Name: $DEF_NAME"
log_info "Period: $START_DATE → $END_DATE"
log_info "Server: $BASE_URL"

# ============================================================================
# Auth
# ============================================================================

COGNITO_AUTH="$HOME/EpochDev/AgentSwarm/tools/cognito_auth.py"

if [[ -z "$TOKEN" ]]; then
    TOKEN="${EPOCH_AUTH_TOKEN:-}"

    if [[ -z "$TOKEN" && -f "$COGNITO_AUTH" ]]; then
        log_info "Getting token via cognito_auth.py..."
        TOKEN=$(python3 "$COGNITO_AUTH" token 2>/dev/null) || true
    fi

    # Also try EpochAI location
    if [[ -z "$TOKEN" && -f "$HOME/EpochDev/EpochAI/tools/cognito_auth.py" ]]; then
        TOKEN=$(python3 "$HOME/EpochDev/EpochAI/tools/cognito_auth.py" token 2>/dev/null) || true
    fi

    if [[ -z "$TOKEN" ]]; then
        log_error "Auth token required. Options:"
        echo "  1. Login first:   python3 $COGNITO_AUTH login"
        echo "  2. Pass directly: $0 $DEF_FILE --token <TOKEN>"
        echo "  3. Environment:   EPOCH_AUTH_TOKEN=<token> $0 $DEF_FILE"
        exit 1
    fi
fi
log_info "Token: ${#TOKEN} chars"

# ============================================================================
# API helper
# ============================================================================

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
        log_error "HTTP $http_code: $body"
        return 1
    fi
    echo "$body"
}

# ============================================================================
# Step 1: Create study definition
# ============================================================================

log_section "Creating Study Definition"

# Build the create payload from the definition JSON
CREATE_PAYLOAD=$(python3 -c "
import json
d = json.load(open('$DEF_FILE'))
payload = {
    'name': d['name'],
    'description': d.get('description', ''),
    'data': {'assets': d['data']['assets'], 'source': d['data'].get('source', 'polygon')},
    'source': d['source'],
    'data_foundation': d.get('global_timeframe', '1D').lower().replace('1d', 'daily')
}
print(json.dumps(payload))
")

result=$(api_call POST "/api/v1/studies/definitions" "$CREATE_PAYLOAD")
STUDY_ID=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('definition_id', d.get('id', '')))" 2>/dev/null)

if [[ -z "$STUDY_ID" ]]; then
    log_error "Failed to create definition. Response: $result"
    exit 1
fi

log_info "Study ID: $STUDY_ID"

# ============================================================================
# Step 2: Execute
# ============================================================================

log_section "Starting Execution"

EXEC_PAYLOAD="{\"id\": \"$STUDY_ID\", \"period\": {\"start\": \"$START_DATE\", \"end\": \"$END_DATE\"}}"
exec_result=$(api_call POST "/api/v1/studies/executions" "$EXEC_PAYLOAD")
EXEC_ID=$(echo "$exec_result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('execution_id', d.get('id', '')))" 2>/dev/null)

if [[ -z "$EXEC_ID" ]]; then
    log_error "Failed to start execution. Response: $exec_result"
    exit 1
fi

log_info "Execution ID: $EXEC_ID"

# ============================================================================
# Step 3: Poll for completion
# ============================================================================

log_section "Polling for Completion"

MAX_WAIT=300  # 5 minutes
POLL_INTERVAL=10
elapsed=0

while [[ $elapsed -lt $MAX_WAIT ]]; do
    status_result=$(api_call GET "/api/v1/studies/executions/$EXEC_ID" 2>&1)
    status=$(echo "$status_result" | python3 -c "
import sys, json
d = json.load(sys.stdin)
s = d.get('status', 'unknown')
# Handle both string and int status
if isinstance(s, int):
    s = {0:'pending',1:'started',2:'in_progress',3:'completed',4:'failed',5:'cancelled'}.get(s,'unknown')
print(str(s).lower())
" 2>/dev/null || echo "unknown")

    echo "  Status: $status (${elapsed}s / ${MAX_WAIT}s)"

    case "$status" in
        completed)
            log_info "Execution completed!"
            break ;;
        failed)
            log_error "Execution failed!"
            echo "$status_result" | python3 -m json.tool 2>/dev/null || echo "$status_result"
            exit 1 ;;
        cancelled)
            log_error "Execution cancelled!"
            exit 1 ;;
    esac

    sleep "$POLL_INTERVAL"
    elapsed=$((elapsed + POLL_INTERVAL))
done

if [[ $elapsed -ge $MAX_WAIT ]]; then
    log_warn "Timeout after ${MAX_WAIT}s. Proceeding with sync anyway."
fi

# ============================================================================
# Step 4: Sync from S3
# ============================================================================

if ! $SKIP_SYNC; then
    log_section "Syncing Job Data from S3"

    # Sync the specific study's data
    LOCAL_SYNC_DIR="$OUTPUT_DIR/$DEF_ID"
    mkdir -p "$LOCAL_SYNC_DIR"

    # Sync the full EFS tree for this study
    log_info "Syncing s3://$S3_BUCKET/$S3_PREFIX/research_studies/ → local"
    aws s3 sync "s3://$S3_BUCKET/$S3_PREFIX/" "$LOCAL_SYNC_DIR/" \
        --exclude "*" \
        --include "*${STUDY_ID}*" \
        --include "*${EXEC_ID}*" \
        --quiet 2>/dev/null || {
        log_warn "Targeted sync failed, trying broad sync..."
        aws s3 sync "s3://$S3_BUCKET/$S3_PREFIX/" "/tmp/epoch-prod-sync/" --quiet
        # Find and copy matching data
        find /tmp/epoch-prod-sync -path "*${STUDY_ID}*" -exec cp -r {} "$LOCAL_SYNC_DIR/" \; 2>/dev/null
    }

    # Count what we got
    TEARSHEETS=$(find "$LOCAL_SYNC_DIR" -name "tearsheet.pb" 2>/dev/null | wc -l)
    ARROWS=$(find "$LOCAL_SYNC_DIR" -name "*.arrow" 2>/dev/null | wc -l)
    CONFIGS=$(find "$LOCAL_SYNC_DIR" -name "config.json" 2>/dev/null | wc -l)

    log_info "Synced: $TEARSHEETS tearsheets, $ARROWS arrow files, $CONFIGS configs"
fi

# ============================================================================
# Summary
# ============================================================================

log_section "Done"
echo "  Definition ID:  $STUDY_ID"
echo "  Execution ID:   $EXEC_ID"
echo "  Definition:     $DEF_ID"
echo "  Output:         $OUTPUT_DIR/$DEF_ID/"
echo ""
echo "  To analyze results:"
echo "    python3 analyze_job/get_study_reports.py $OUTPUT_DIR/$DEF_ID/"
echo "    python3 analyze_job/query_study_dataframes.py $OUTPUT_DIR/$DEF_ID/"
