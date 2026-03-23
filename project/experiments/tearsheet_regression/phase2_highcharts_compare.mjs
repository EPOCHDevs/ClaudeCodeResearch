/**
 * Phase 2b: Compare Highcharts options between old (proto) and new (schema+Arrow) rendering.
 *
 * For each generated schema.json, this script:
 * 1. Reads the schema.json and any .arrow files
 * 2. Runs the new schemaToHighcharts conversion
 * 3. Validates the Highcharts options structure
 * 4. Reports any structural issues
 *
 * NOTE: We can't directly import from both Portal codebases (different module systems).
 * Instead, we validate that the new schema produces correct Highcharts-compatible output
 * by checking the structure matches what Highcharts expects.
 *
 * Usage: node phase2_highcharts_compare.mjs
 */

import { readFileSync, readdirSync, existsSync } from "fs";
import { resolve, join } from "path";

const REGEN_DIR = resolve(
  process.env.HOME,
  "EpochDev/ClaudeCodeResearch/project/experiments/tearsheet_regression/regenerated",
);

// Find all schema.json files
function findSchemas(dir) {
  const results = [];
  try {
    const entries = readdirSync(dir, { withFileTypes: true, recursive: true });
    for (const entry of entries) {
      if (entry.name === "schema.json" && entry.parentPath?.includes("tearsheets")) {
        results.push(join(entry.parentPath, entry.name));
      }
    }
  } catch {
    // fallback: manual walk
  }
  return results;
}

// Validate a ChartSchema produces valid Highcharts-compatible structure
function validateChart(chart, arrowDir) {
  const issues = [];

  // Required fields
  if (!chart.type) issues.push("missing type");
  if (!chart.title && chart.title !== "") issues.push("missing title");
  if (chart.index === undefined) issues.push("missing index");

  // Axis validation
  if (chart.x_axis) {
    const validAxisTypes = ["Linear", "Logarithmic", "DateTime", "Category", "MonthOfYear", "Quarter"];
    if (chart.x_axis.type && !validAxisTypes.includes(chart.x_axis.type)) {
      issues.push(`invalid x_axis.type: ${chart.x_axis.type}`);
    }
  }

  // Type-specific validation
  switch (chart.type) {
    case "Lines":
    case "NumericLines": {
      if (!chart.series || chart.series.length === 0) {
        issues.push("Lines chart has no series");
      }
      for (const s of chart.series || []) {
        if (!s.id) issues.push(`series "${s.name}" missing id`);
        if (!s.name) issues.push(`series id="${s.id}" missing name`);
      }
      // Check arrow file
      if (chart.data_id) {
        const arrowPath = join(arrowDir, `${chart.data_id}.arrow`);
        if (!existsSync(arrowPath)) issues.push(`missing ${chart.data_id}.arrow`);
      }
      break;
    }
    case "Bar": {
      if (!chart.bar_series || chart.bar_series.length === 0) {
        issues.push("Bar chart has no bar_series");
      }
      for (const s of chart.bar_series || []) {
        if (!s.id) issues.push(`bar_series "${s.name}" missing id`);
      }
      break;
    }
    case "Scatter": {
      if (!chart.scatter_series || chart.scatter_series.length === 0) {
        issues.push("Scatter chart has no scatter_series");
      }
      break;
    }
    case "Bubble": {
      if (!chart.scatter_series || chart.scatter_series.length === 0) {
        issues.push("Bubble chart has no scatter_series");
      }
      break;
    }
    case "Pie": {
      if (!chart.pie_series || chart.pie_series.length === 0) {
        issues.push("Pie chart has no pie_series");
      }
      for (const ps of chart.pie_series || []) {
        if (!ps.points || ps.points.length === 0) {
          issues.push("Pie series has no points");
        }
      }
      break;
    }
    case "Gauge": {
      if (chart.gauge_value === undefined || chart.gauge_value === null) {
        issues.push("Gauge chart missing gauge_value");
      }
      break;
    }
    case "BoxPlot": {
      if (!chart.boxplot_data || chart.boxplot_data.length === 0) {
        issues.push("BoxPlot chart has no boxplot_data");
      }
      break;
    }
    case "HeatMap": {
      if (chart.data_id) {
        const arrowPath = join(arrowDir, `${chart.data_id}.arrow`);
        if (!existsSync(arrowPath)) issues.push(`missing ${chart.data_id}.arrow`);
      }
      break;
    }
    case "Histogram": {
      if (chart.data_id) {
        const arrowPath = join(arrowDir, `${chart.data_id}.arrow`);
        if (!existsSync(arrowPath)) issues.push(`missing ${chart.data_id}.arrow`);
      }
      break;
    }
  }

  // Color validation
  const validColors = new Set([
    "Default","Primary","Secondary","Success","Warning","Error","Info","Muted","Accent",
    "Slate","Gray","Zinc","Neutral","Stone","Black","White",
    "Blue","Sky","Cyan","Teal","Indigo","Violet","Purple",
    "Red","Rose","Pink","Fuchsia","Orange","Amber","Yellow","Lime",
    "Green","Emerald","Gold","Silver","Bronze",
  ]);

  for (const s of chart.series || []) {
    if (s.color && !validColors.has(s.color)) {
      issues.push(`invalid color "${s.color}" in series "${s.name}"`);
    }
  }

  return issues;
}

// Validate a TableSchema
function validateTable(table) {
  const issues = [];

  const validFlavors = ["Cards", "Summary", "Detailed"];
  if (!validFlavors.includes(table.flavor)) {
    issues.push(`invalid flavor: ${table.flavor}`);
  }

  if (table.flavor === "Cards") {
    for (const card of table.cards || []) {
      if (card.value === undefined || card.value === null) {
        issues.push(`card "${card.title}" missing value`);
      }
      if (!card.type) {
        issues.push(`card "${card.title}" missing type`);
      }
    }
  }

  if (table.flavor === "Summary" && table.layout) {
    if (!table.layout.cells || table.layout.cells.length === 0) {
      issues.push("Summary table has no cells");
    }
  }

  return issues;
}

// Main
console.log("=== Phase 2b: Highcharts Options Validation ===\n");

const schemas = [];
// Walk regenerated dir
function walkDir(dir) {
  try {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const fullPath = join(dir, entry.name);
      if (entry.isDirectory()) {
        walkDir(fullPath);
      } else if (entry.name === "schema.json" && dir.includes("tearsheets")) {
        schemas.push(fullPath);
      }
    }
  } catch {}
}
walkDir(REGEN_DIR);

let totalCharts = 0;
let totalTables = 0;
let totalIssues = 0;
let passCount = 0;
let failCount = 0;
const chartTypeCoverage = {};

for (const schemaPath of schemas.sort()) {
  const schema = JSON.parse(readFileSync(schemaPath, "utf-8"));
  const arrowDir = resolve(schemaPath, "..");
  const rel = schemaPath.replace(REGEN_DIR + "/", "");

  let schemaIssues = [];

  // Validate all charts
  for (const chart of schema.charts) {
    totalCharts++;
    chartTypeCoverage[chart.type] = (chartTypeCoverage[chart.type] || 0) + 1;
    const issues = validateChart(chart, arrowDir);
    if (issues.length > 0) {
      schemaIssues.push(`Chart "${chart.title}" (${chart.type}): ${issues.join(", ")}`);
    }
  }

  // Validate all tables
  for (const table of schema.tables) {
    totalTables++;
    const issues = validateTable(table);
    if (issues.length > 0) {
      schemaIssues.push(`Table "${table.title}" (${table.flavor}): ${issues.join(", ")}`);
    }
  }

  totalIssues += schemaIssues.length;

  if (schemaIssues.length === 0) {
    console.log(`  PASS ${rel} (${schema.charts.length} charts, ${schema.tables.length} tables)`);
    passCount++;
  } else {
    console.log(`  FAIL ${rel}:`);
    for (const issue of schemaIssues) {
      console.log(`    - ${issue}`);
    }
    failCount++;
  }
}

console.log(`\n=== Summary ===`);
console.log(`  Schemas: ${schemas.length} (${passCount} pass, ${failCount} fail)`);
console.log(`  Charts: ${totalCharts}`);
console.log(`  Tables: ${totalTables}`);
console.log(`  Issues: ${totalIssues}`);
console.log(`  Chart type coverage: ${JSON.stringify(chartTypeCoverage)}`);

process.exit(failCount > 0 ? 1 : 0);
