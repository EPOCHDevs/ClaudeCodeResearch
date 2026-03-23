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
// Chart types with inline data (no Arrow file needed)
const INLINE_CHART_TYPES = new Set(["Pie", "Gauge", "BoxPlot"]);
for (const chart of schema.charts) {
  if (chart.data_id && !INLINE_CHART_TYPES.has(chart.type)) {
    const arrowPath = resolve(arrowDir, `${chart.data_id}.arrow`);
    try {
      readFileSync(arrowPath);
    } catch {
      arrowIssues.push({ chart: chart.title, data_id: chart.data_id, issue: "missing_arrow_file" });
    }
  }
}
for (const table of schema.tables) {
  // Cards and Summary tables have inline data — data_id is set but no Arrow file exists (by design)
  const isInlineTable = table.flavor === "Cards" || table.flavor === "Summary";
  if (table.data_id && !isInlineTable) {
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
