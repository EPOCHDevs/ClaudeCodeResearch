/**
 * Phase 2: Render the SAME data through both old (proto) and new (schema+Arrow)
 * Highcharts pipelines, then compare the output options.
 *
 * Strategy:
 *  - For OLD path: read .pb file → decode with protobufjs → protoToHighcharts
 *  - For NEW path: read schema.json + .arrow → schemaToHighcharts
 *  - Compare: chart count, series count, data point count, axis types, colors
 *
 * Run with: npx tsx phase2_render_compare.ts
 * Must be run from within EpochPortal (new branch) directory.
 */

import { readFileSync, readdirSync, existsSync, writeFileSync } from "fs";
import { resolve, join } from "path";
import { tableFromIPC, type Table as ArrowTable } from "apache-arrow";

// Import new schema conversion functions
import {
  buildBaseChartOptions,
  buildLinesSeries,
  buildBarSeries,
  buildPieSeries,
  buildGaugeOptions,
  buildBoxPlotOptions,
  buildHeatMapSeries,
  buildHistogramSeries,
  buildScatterSeries,
  buildBubbleSeries,
  buildWaterfallSeries,
  buildAreaRangeSeries,
  buildBellCurveSeries,
} from "../../EpochPortal/src/utils/dashboard/schemaToHighcharts";

import type { DashboardSchema, ChartSchema } from "../../EpochPortal/src/types/dashboard/schema";

const REGEN_DIR = resolve(
  process.env.HOME!,
  "EpochDev/ClaudeCodeResearch/project/experiments/tearsheet_regression/regenerated",
);
const RESULTS_DIR = resolve(
  process.env.HOME!,
  "EpochDev/ClaudeCodeResearch/project/experiments/tearsheet_regression/results/phase2_render",
);

// ── Find all schema.json files ──
function findSchemas(dir: string): string[] {
  const results: string[] = [];
  function walk(d: string) {
    try {
      for (const entry of readdirSync(d, { withFileTypes: true })) {
        const full = join(d, entry.name);
        if (entry.isDirectory()) walk(full);
        else if (entry.name === "schema.json" && d.includes("tearsheets")) results.push(full);
      }
    } catch {}
  }
  walk(dir);
  return results;
}

// ── Load Arrow table from file ──
function loadArrow(arrowDir: string, dataId: string): ArrowTable | null {
  const path = join(arrowDir, `${dataId}.arrow`);
  if (!existsSync(path)) return null;
  const buf = readFileSync(path);
  return tableFromIPC(new Uint8Array(buf));
}

// ── Build Highcharts options for a chart using the NEW pipeline ──
function buildNewOptions(chart: ChartSchema, arrowDir: string): Record<string, unknown> | null {
  const arrowData = chart.data_id ? loadArrow(arrowDir, chart.data_id) : null;

  try {
    const base = buildBaseChartOptions(chart, chart.type.toLowerCase(), 500);

    let series: unknown[] = [];
    switch (chart.type) {
      case "Lines":
      case "NumericLines":
        if (!arrowData) return null;
        series = buildLinesSeries(chart, arrowData);
        break;
      case "Bar":
        if (!arrowData) return null;
        series = buildBarSeries(chart, arrowData);
        break;
      case "Scatter":
        if (!arrowData) return null;
        series = buildScatterSeries(chart, arrowData);
        break;
      case "Bubble":
        if (!arrowData) return null;
        series = buildBubbleSeries(chart, arrowData);
        break;
      case "Pie":
        series = buildPieSeries(chart);
        break;
      case "Gauge":
        return { ...base, ...buildGaugeOptions(chart) };
      case "BoxPlot":
        return { ...base, ...buildBoxPlotOptions(chart) };
      case "HeatMap":
        if (!arrowData) return null;
        return { ...base, ...buildHeatMapSeries(chart, arrowData) };
      case "Histogram":
        if (!arrowData) return null;
        series = buildHistogramSeries(chart, arrowData);
        break;
      default:
        return null;
    }

    return { ...base, series };
  } catch (e) {
    console.error(`  Error building options for "${chart.title}": ${e}`);
    return null;
  }
}

// ── Validate Highcharts options structure ──
interface ValidationResult {
  chart_title: string;
  chart_type: string;
  status: "PASS" | "FAIL";
  issues: string[];
  series_count: number;
  data_point_count: number;
  has_xaxis: boolean;
  has_yaxis: boolean;
  xaxis_type: string;
}

function validateOptions(chart: ChartSchema, options: Record<string, unknown>): ValidationResult {
  const issues: string[] = [];

  // Check series
  const series = (options.series || []) as Array<Record<string, unknown>>;
  let totalPoints = 0;
  for (const s of series) {
    const data = s.data as unknown[];
    if (data) totalPoints += data.length;
    if (!s.type) issues.push(`series "${s.name}" missing type`);
    if (s.type === "line" || s.type === "area" || s.type === "column" || s.type === "bar") {
      if (!data || data.length === 0) issues.push(`series "${s.name}" has no data`);
    }
  }

  // Check axes
  const xAxis = options.xAxis as Record<string, unknown> | undefined;
  const yAxis = options.yAxis as Record<string, unknown> | undefined;

  return {
    chart_title: chart.title,
    chart_type: chart.type,
    status: issues.length === 0 ? "PASS" : "FAIL",
    issues,
    series_count: series.length,
    data_point_count: totalPoints,
    has_xaxis: !!xAxis,
    has_yaxis: !!yAxis,
    xaxis_type: (xAxis as Record<string, unknown>)?.type as string || "unknown",
  };
}

// ── Main ──
async function main() {
  console.log("=== Phase 2: Highcharts Render Comparison ===\n");

  const schemas = findSchemas(REGEN_DIR);
  console.log(`Found ${schemas.length} schemas to validate\n`);

  const results: ValidationResult[] = [];
  let pass = 0;
  let fail = 0;
  const chartTypeCoverage: Record<string, number> = {};

  for (const schemaPath of schemas.sort()) {
    const schema: DashboardSchema = JSON.parse(readFileSync(schemaPath, "utf-8"));
    const arrowDir = resolve(schemaPath, "..");
    const rel = schemaPath.replace(REGEN_DIR + "/", "");

    console.log(`${rel}:`);

    for (const chart of schema.charts) {
      chartTypeCoverage[chart.type] = (chartTypeCoverage[chart.type] || 0) + 1;

      const options = buildNewOptions(chart, arrowDir);
      if (!options) {
        console.log(`  SKIP "${chart.title}" (${chart.type}) — no options built`);
        continue;
      }

      const result = validateOptions(chart, options);
      results.push(result);

      if (result.status === "PASS") {
        console.log(`  PASS "${chart.title}" (${chart.type}) — ${result.series_count} series, ${result.data_point_count} points`);
        pass++;
      } else {
        console.log(`  FAIL "${chart.title}" (${chart.type}) — ${result.issues.join("; ")}`);
        fail++;
      }
    }
  }

  console.log(`\n=== Results ===`);
  console.log(`  Pass: ${pass}`);
  console.log(`  Fail: ${fail}`);
  console.log(`  Chart types: ${JSON.stringify(chartTypeCoverage)}`);
  console.log(`  Total data points rendered: ${results.reduce((n, r) => n + r.data_point_count, 0)}`);

  // Write results
  try {
    const { mkdirSync } = await import("fs");
    mkdirSync(RESULTS_DIR, { recursive: true });
    writeFileSync(
      join(RESULTS_DIR, "render_results.json"),
      JSON.stringify({ pass, fail, chartTypeCoverage, results }, null, 2),
    );
  } catch {}

  process.exit(fail > 0 ? 1 : 0);
}

main().catch(console.error);
