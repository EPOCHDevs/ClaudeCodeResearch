#!/bin/bash
#
# Phase 1: Regenerate all studies and compare old .pb tearsheets with new schema.json + Arrow
#
# This script:
#   1. Finds all studies that have existing .pb tearsheets
#   2. Re-runs each study with generate_job_data (which now produces schema.json + Arrow)
#   3. Compares the old .pb output with the new schema.json output
#
# Usage:
#   ./run_phase1_regenerate.sh              # Run all studies
#   ./run_phase1_regenerate.sh --dry-run    # List studies without running
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$HOME/EpochDev/ClaudeCodeResearch/project"
BACKEND_DIR="$HOME/EpochDev/EpochBackend"
STUDIES_DIR="$PROJECT_DIR/research_studies/test_runner"
EXPERIMENT_DIR="$SCRIPT_DIR"
RESULTS_DIR="$EXPERIMENT_DIR/results"
REGEN_DIR="$EXPERIMENT_DIR/regenerated"
GENERATOR="$BACKEND_DIR/build/bin/generate_job_data"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

mkdir -p "$RESULTS_DIR" "$REGEN_DIR"

# ============================================================================
# Step 1: Inventory all studies with .pb tearsheets
# ============================================================================

echo -e "${BLUE}=== Phase 1: Tearsheet Regression Test ===${NC}"
echo ""

# Build inventory: study_name -> list of tearsheet categories
declare -A STUDY_CATEGORIES
TOTAL_TEARSHEETS=0

while IFS= read -r pb_path; do
    # Extract: studies_dir/STUDY_NAME/tearsheets/CATEGORY/tearsheet.pb
    rel="${pb_path#$STUDIES_DIR/}"
    study_name="${rel%%/*}"
    category_path="${rel#*/tearsheets/}"
    category="${category_path%/tearsheet.pb}"

    if [[ -z "${STUDY_CATEGORIES[$study_name]+x}" ]]; then
        STUDY_CATEGORIES[$study_name]="$category"
    else
        STUDY_CATEGORIES[$study_name]="${STUDY_CATEGORIES[$study_name]}|$category"
    fi
    TOTAL_TEARSHEETS=$((TOTAL_TEARSHEETS + 1))
done < <(find "$STUDIES_DIR" -name "tearsheet.pb" -type f 2>/dev/null)

STUDY_COUNT=${#STUDY_CATEGORIES[@]}
echo -e "${GREEN}Found $STUDY_COUNT studies with $TOTAL_TEARSHEETS tearsheets${NC}"
echo ""

# List studies
for study in $(echo "${!STUDY_CATEGORIES[@]}" | tr ' ' '\n' | sort); do
    cats="${STUDY_CATEGORIES[$study]}"
    cat_count=$(echo "$cats" | tr '|' '\n' | wc -l)
    echo -e "  ${BLUE}$study${NC} ($cat_count categories: ${cats//|/, })"
done
echo ""

if $DRY_RUN; then
    echo -e "${YELLOW}Dry run — exiting without regeneration${NC}"
    exit 0
fi

# ============================================================================
# Step 2: Verify generator binary
# ============================================================================

if [[ ! -x "$GENERATOR" ]]; then
    echo -e "${RED}ERROR: generate_job_data not found at $GENERATOR${NC}"
    echo "Run: ninja -C $BACKEND_DIR/build generate_job_data -j8"
    exit 1
fi

# ============================================================================
# Step 3: Create definitions/ folder (generate_job_data requires path to contain "definitions")
# ============================================================================

DEFS_DIR="$REGEN_DIR/definitions/test_runner"
mkdir -p "$DEFS_DIR"

# Transform each study config.json into a clean definition for generate_job_data
# (strip unknown keys like definition_id, period, thread_id; add name if missing;
#  fix cache_dir to local path)
MARKET_DATA_DIR="$PROJECT_DIR/market_data"
for study in $(echo "${!STUDY_CATEGORIES[@]}" | tr ' ' '\n' | sort); do
    src_config="$STUDIES_DIR/$study/config.json"
    if [[ -f "$src_config" ]]; then
        python3 -c "
import json
d = json.load(open('$src_config'))
clean = {}
clean['name'] = d.get('name', '$study')
clean['description'] = d.get('description', '')
clean['data'] = d.get('data', {})
clean['source'] = d.get('source', '')
clean['global_timeframe'] = d.get('global_timeframe', '1D')
# Fix cache_dir to local market_data path
clean['data']['cache_dir'] = '$MARKET_DATA_DIR'
with open('$DEFS_DIR/${study}.json', 'w') as f:
    json.dump(clean, f, indent=2)
" 2>/dev/null
    fi
done

echo -e "${GREEN}Prepared ${#STUDY_CATEGORIES[@]} definitions in $DEFS_DIR${NC}"
echo ""

# ============================================================================
# Step 4: Re-run each study
# ============================================================================

PASSED=0
FAILED=0
SKIPPED=0
FAILED_STUDIES=()

# Set project dir so output goes to experiment folder
export EPOCH_PROJECT_DIR="$REGEN_DIR"

for study in $(echo "${!STUDY_CATEGORIES[@]}" | tr ' ' '\n' | sort); do
    def_file="$DEFS_DIR/${study}.json"

    if [[ ! -f "$def_file" ]]; then
        echo -e "${YELLOW}SKIP${NC} $study — no definition"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Running: $study${NC}"

    # Extract start/end from config
    start_date=$(python3 -c "import json; d=json.load(open('$def_file')); print(d.get('period',{}).get('start','2015-01-01'))" 2>/dev/null || echo "2015-01-01")
    end_date=$(python3 -c "import json; d=json.load(open('$def_file')); print(d.get('period',{}).get('end','2025-12-31'))" 2>/dev/null || echo "2025-12-31")

    regen_output="$REGEN_DIR/research_studies/test_runner/$study"
    mkdir -p "$regen_output"

    # Run generator
    echo "  Definition: $def_file"
    echo "  Period: $start_date → $end_date"
    echo "  Output: $regen_output"

    if "$GENERATOR" "$def_file" \
        --start "$start_date" \
        --end "$end_date" \
        --name "$study" \
        > "$RESULTS_DIR/${study}_generate.log" 2>&1; then
        echo -e "  ${GREEN}✓ Generated${NC}"
    else
        echo -e "  ${RED}✗ Generation failed${NC}"
        echo "  See: $RESULTS_DIR/${study}_generate.log"
        FAILED_STUDIES+=("$study")
        FAILED=$((FAILED + 1))
        continue
    fi

    # ========================================================================
    # Step 5: Compare old .pb vs new schema.json for each category
    # ========================================================================

    IFS='|' read -ra cats <<< "${STUDY_CATEGORIES[$study]}"
    study_pass=true

    for category in "${cats[@]}"; do
        old_pb="$STUDIES_DIR/$study/tearsheets/$category/tearsheet.pb"
        new_schema="$regen_output/tearsheets/$category/schema.json"

        if [[ ! -f "$new_schema" ]]; then
            echo -e "  ${RED}✗ Missing: $category/schema.json${NC}"
            study_pass=false
            continue
        fi

        # Count charts and tables in new schema
        new_charts=$(python3 -c "import json; d=json.load(open('$new_schema')); print(len(d.get('charts',[])))" 2>/dev/null || echo "?")
        new_tables=$(python3 -c "import json; d=json.load(open('$new_schema')); print(len(d.get('tables',[])))" 2>/dev/null || echo "?")

        # Count Arrow files
        arrow_count=$(find "$regen_output/tearsheets/$category" -name "*.arrow" 2>/dev/null | wc -l)

        echo -e "  ${GREEN}✓${NC} $category: $new_charts charts, $new_tables tables, $arrow_count arrow files"

        # Save comparison summary
        python3 -c "
import json, os

schema = json.load(open('$new_schema'))
summary = {
    'study': '$study',
    'category': '$category',
    'old_pb_size': os.path.getsize('$old_pb'),
    'new_schema_size': os.path.getsize('$new_schema'),
    'charts_count': len(schema.get('charts', [])),
    'tables_count': len(schema.get('tables', [])),
    'chart_types': [c['type'] for c in schema.get('charts', [])],
    'chart_titles': [c['title'] for c in schema.get('charts', [])],
    'table_flavors': [t['flavor'] for t in schema.get('tables', [])],
    'table_titles': [t['title'] for t in schema.get('tables', [])],
    'arrow_files': $arrow_count,
    'cards': sum(len(t.get('cards',[])) for t in schema.get('tables',[]) if t.get('flavor')=='Cards'),
}
with open('$RESULTS_DIR/${study}_${category}_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
" 2>/dev/null || true
    done

    if $study_pass; then
        PASSED=$((PASSED + 1))
    else
        FAILED_STUDIES+=("$study")
        FAILED=$((FAILED + 1))
    fi
    echo ""
done

# ============================================================================
# Step 5: Summary
# ============================================================================

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Phase 1 Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${GREEN}Passed:${NC}  $PASSED"
echo -e "  ${RED}Failed:${NC}  $FAILED"
echo -e "  ${YELLOW}Skipped:${NC} $SKIPPED"

if [[ ${#FAILED_STUDIES[@]} -gt 0 ]]; then
    echo ""
    echo -e "${RED}Failed studies:${NC}"
    for s in "${FAILED_STUDIES[@]}"; do
        echo -e "  ${RED}✗${NC} $s"
    done
fi

# Generate aggregate report
python3 -c "
import json, glob, os

results_dir = '$RESULTS_DIR'
summaries = []
for f in sorted(glob.glob(os.path.join(results_dir, '*_summary.json'))):
    summaries.append(json.load(open(f)))

report = {
    'total_studies': $STUDY_COUNT,
    'passed': $PASSED,
    'failed': $FAILED,
    'skipped': $SKIPPED,
    'total_tearsheets': len(summaries),
    'chart_type_distribution': {},
    'table_flavor_distribution': {},
    'total_charts': 0,
    'total_tables': 0,
    'total_cards': 0,
    'total_arrow_files': 0,
}

for s in summaries:
    report['total_charts'] += s['charts_count']
    report['total_tables'] += s['tables_count']
    report['total_cards'] += s['cards']
    report['total_arrow_files'] += s['arrow_files']
    for ct in s['chart_types']:
        report['chart_type_distribution'][ct] = report['chart_type_distribution'].get(ct, 0) + 1
    for tf in s['table_flavors']:
        report['table_flavor_distribution'][tf] = report['table_flavor_distribution'].get(tf, 0) + 1

with open(os.path.join(results_dir, 'aggregate_report.json'), 'w') as f:
    json.dump(report, f, indent=2)

print()
print(f'Aggregate: {report[\"total_charts\"]} charts, {report[\"total_tables\"]} tables, {report[\"total_cards\"]} cards, {report[\"total_arrow_files\"]} Arrow files')
print(f'Chart types: {json.dumps(report[\"chart_type_distribution\"])}')
print(f'Table flavors: {json.dumps(report[\"table_flavor_distribution\"])}')
" 2>/dev/null || true

echo ""
echo -e "Results saved to: ${GREEN}$RESULTS_DIR${NC}"
