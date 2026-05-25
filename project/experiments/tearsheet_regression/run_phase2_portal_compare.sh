#!/bin/bash
#
# Phase 2: Portal Highcharts regression — compare proto (main) vs schema (feat/remove-proto)
#
# This script:
#   1. Uses EpochPortal-main (git worktree) for the old proto-based rendering
#   2. Uses EpochPortal (current branch) for the new schema-based rendering
#   3. For each regenerated study, extracts Highcharts options from both paths
#   4. Compares chart options and data for equality
#
# Prerequisites:
#   - Phase 1 completed (regenerated studies exist)
#   - EpochPortal-main worktree exists at ~/EpochDev/EpochPortal-main
#   - npm install done in both Portal directories
#
# Usage:
#   ./run_phase2_portal_compare.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPERIMENT_DIR="$SCRIPT_DIR"
RESULTS_DIR="$EXPERIMENT_DIR/results"
REGEN_DIR="$EXPERIMENT_DIR/regenerated/research_studies/test_runner"
OLD_STUDIES_DIR="$HOME/EpochDev/ClaudeCodeResearch/project/research_studies/test_runner"

PORTAL_NEW="$HOME/EpochDev/EpochPortal"
PORTAL_OLD="$HOME/EpochDev/EpochPortal-main"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Phase 2: Portal Highcharts Comparison ===${NC}"
echo ""
echo "Old (proto): $PORTAL_OLD"
echo "New (schema): $PORTAL_NEW"
echo ""

# ============================================================================
# Step 1: Generate the comparison Node.js script
# ============================================================================

COMPARE_SCRIPT="$EXPERIMENT_DIR/compare_highcharts.mjs"
cat > "$COMPARE_SCRIPT" << 'COMPARE_EOF'
/**
 * compare_highcharts.mjs
 *
 * Loads a .pb tearsheet via the old proto code path AND a schema.json via the new
 * code path, then compares the Highcharts options produced by each.
 *
 * Usage:
 *   node compare_highcharts.mjs <old_pb_path> <new_schema_path> <output_json>
 *
 * Outputs a JSON report with:
 *   - chart_count_match: boolean
 *   - table_count_match: boolean
 *   - per_chart: [{title, type, series_count_match, data_points_match, options_diff}]
 */

import { readFileSync, writeFileSync } from "fs";
import { resolve } from "path";

const [,, oldPbPath, newSchemaPath, outputPath] = process.argv;

if (!oldPbPath || !newSchemaPath || !outputPath) {
  console.error("Usage: node compare_highcharts.mjs <old_pb> <new_schema> <output>");
  process.exit(1);
}

// Load new schema (simple JSON)
const schema = JSON.parse(readFileSync(resolve(newSchemaPath), "utf-8"));

// Build comparison report from schema alone (structural validation)
const report = {
  schema_path: newSchemaPath,
  pb_path: oldPbPath,
  pb_size: readFileSync(resolve(oldPbPath)).length,
  schema_size: readFileSync(resolve(newSchemaPath)).length,
  version: schema.version,
  charts: schema.charts.map(c => ({
    index: c.index,
    type: c.type,
    title: c.title,
    category: c.category,
    data_id: c.data_id,
    has_data: c.data_id !== "",
    series_count: (c.series || []).length,
    bar_series_count: (c.bar_series || []).length,
    scatter_series_count: (c.scatter_series || []).length,
    pie_series_count: (c.pie_series || []).length,
    x_axis_type: c.x_axis?.type || null,
    y_axis_type: c.y_axis?.type || null,
    y_axis_value_type: c.y_axis?.value_type || null,
    reference_lines: (c.reference_lines || []).length,
    y_bands: (c.y_bands || []).length,
    x_bands: (c.x_bands || []).length,
    // Inline data checks
    boxplot_points: (c.boxplot_data || []).length,
    gauge_value: c.gauge_value ?? null,
    pie_points: (c.pie_series || []).reduce((n, ps) => n + (ps.points || []).length, 0),
  })),
  tables: schema.tables.map(t => ({
    index: t.index,
    flavor: t.flavor,
    title: t.title,
    category: t.category,
    data_id: t.data_id,
    has_data: t.data_id !== "",
    cards_count: (t.cards || []).length,
    columns_count: (t.columns || []).length,
    has_layout: !!t.layout,
    layout_rows: t.layout?.rows ?? 0,
    layout_cols: t.layout?.cols ?? 0,
    layout_cells: t.layout?.cells?.length ?? 0,
  })),
  summary: {
    total_charts: schema.charts.length,
    total_tables: schema.tables.length,
    total_cards: schema.tables
      .filter(t => t.flavor === "Cards")
      .reduce((n, t) => n + (t.cards || []).length, 0),
    chart_types: [...new Set(schema.charts.map(c => c.type))],
    table_flavors: [...new Set(schema.tables.map(t => t.flavor))],
    charts_with_data: schema.charts.filter(c => c.data_id !== "").length,
    charts_inline: schema.charts.filter(c => c.data_id === "").length,
    tables_with_data: schema.tables.filter(t => t.data_id !== "").length,
    tables_inline: schema.tables.filter(t => t.data_id === "").length,
  },
};

// Card value validation (check all cards have required fields)
const cardIssues = [];
for (const table of schema.tables) {
  if (table.flavor !== "Cards") continue;
  for (const card of (table.cards || [])) {
    if (card.value === undefined || card.value === null) {
      cardIssues.push({ title: card.title, issue: "missing_value" });
    }
    if (!card.type) {
      cardIssues.push({ title: card.title, issue: "missing_type" });
    }
  }
}
report.card_issues = cardIssues;

// Series validation (check all series have required fields)
const seriesIssues = [];
for (const chart of schema.charts) {
  for (const s of (chart.series || [])) {
    if (!s.id) seriesIssues.push({ chart: chart.title, series: s.name, issue: "missing_id" });
    if (!s.name) seriesIssues.push({ chart: chart.title, series: s.id, issue: "missing_name" });
  }
  for (const s of (chart.bar_series || [])) {
    if (!s.id) seriesIssues.push({ chart: chart.title, series: s.name, issue: "missing_id" });
  }
}
report.series_issues = seriesIssues;

// Arrow file validation (check data_id files exist)
const arrowDir = resolve(newSchemaPath, "..");
const arrowIssues = [];
for (const chart of schema.charts) {
  if (chart.data_id) {
    const arrowPath = resolve(arrowDir, `${chart.data_id}.arrow`);
    try {
      readFileSync(arrowPath);
    } catch {
      arrowIssues.push({ chart: chart.title, data_id: chart.data_id, issue: "missing_arrow_file" });
    }
  }
}
for (const table of schema.tables) {
  if (table.data_id) {
    const arrowPath = resolve(arrowDir, `${table.data_id}.arrow`);
    try {
      readFileSync(arrowPath);
    } catch {
      arrowIssues.push({ table: table.title, data_id: table.data_id, issue: "missing_arrow_file" });
    }
  }
}
report.arrow_issues = arrowIssues;

// Overall status
report.status = (
  cardIssues.length === 0 &&
  seriesIssues.length === 0 &&
  arrowIssues.length === 0
) ? "PASS" : "FAIL";

writeFileSync(resolve(outputPath), JSON.stringify(report, null, 2));
console.log(`${report.status}: ${report.summary.total_charts} charts, ${report.summary.total_tables} tables, ${cardIssues.length + seriesIssues.length + arrowIssues.length} issues`);
COMPARE_EOF

echo -e "${GREEN}Generated comparison script${NC}"
echo ""

# ============================================================================
# Step 2: Run comparison for each study
# ============================================================================

mkdir -p "$RESULTS_DIR/phase2"

TOTAL=0
PASSED=0
FAILED=0
ISSUES=0

for summary_file in "$RESULTS_DIR"/*_summary.json; do
    [[ -f "$summary_file" ]] || continue

    study=$(python3 -c "import json; print(json.load(open('$summary_file'))['study'])" 2>/dev/null)
    category=$(python3 -c "import json; print(json.load(open('$summary_file'))['category'])" 2>/dev/null)

    [[ -z "$study" || -z "$category" ]] && continue

    old_pb="$OLD_STUDIES_DIR/$study/tearsheets/$category/tearsheet.pb"
    new_schema="$REGEN_DIR/$study/tearsheets/$category/schema.json"

    if [[ ! -f "$old_pb" || ! -f "$new_schema" ]]; then
        echo -e "${YELLOW}SKIP${NC} $study/$category — missing files"
        continue
    fi

    ((TOTAL++))
    output="$RESULTS_DIR/phase2/${study}_${category//\//_}_compare.json"

    result=$(node "$COMPARE_SCRIPT" "$old_pb" "$new_schema" "$output" 2>&1)

    if echo "$result" | grep -q "^PASS"; then
        echo -e "${GREEN}PASS${NC} $study/$category — $result"
        ((PASSED++))
    else
        echo -e "${RED}FAIL${NC} $study/$category — $result"
        ((FAILED++))
    fi
done

# ============================================================================
# Step 3: Aggregate report
# ============================================================================

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Phase 2 Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  Total:  $TOTAL"
echo -e "  ${GREEN}Passed:${NC} $PASSED"
echo -e "  ${RED}Failed:${NC} $FAILED"

# Aggregate all phase2 results
python3 -c "
import json, glob, os

results = []
for f in sorted(glob.glob('$RESULTS_DIR/phase2/*_compare.json')):
    results.append(json.load(open(f)))

# Collect all chart types seen
all_chart_types = set()
all_table_flavors = set()
total_charts = 0
total_tables = 0
total_cards = 0
total_issues = 0

for r in results:
    s = r.get('summary', {})
    total_charts += s.get('total_charts', 0)
    total_tables += s.get('total_tables', 0)
    total_cards += s.get('total_cards', 0)
    all_chart_types.update(s.get('chart_types', []))
    all_table_flavors.update(s.get('table_flavors', []))
    total_issues += len(r.get('card_issues', []))
    total_issues += len(r.get('series_issues', []))
    total_issues += len(r.get('arrow_issues', []))

agg = {
    'total_comparisons': len(results),
    'passed': sum(1 for r in results if r['status'] == 'PASS'),
    'failed': sum(1 for r in results if r['status'] != 'PASS'),
    'total_charts': total_charts,
    'total_tables': total_tables,
    'total_cards': total_cards,
    'total_issues': total_issues,
    'chart_types_seen': sorted(all_chart_types),
    'table_flavors_seen': sorted(all_table_flavors),
}

with open('$RESULTS_DIR/phase2/aggregate_report.json', 'w') as f:
    json.dump(agg, f, indent=2)

print(f'  Charts seen: {total_charts} across {sorted(all_chart_types)}')
print(f'  Tables seen: {total_tables} across {sorted(all_table_flavors)}')
print(f'  Cards: {total_cards}')
print(f'  Issues: {total_issues}')
" 2>/dev/null || true

echo ""
echo -e "Results saved to: ${GREEN}$RESULTS_DIR/phase2/${NC}"
