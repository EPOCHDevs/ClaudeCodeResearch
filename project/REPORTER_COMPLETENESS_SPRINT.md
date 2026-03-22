# Reporter Completeness Sprint

Systematic review of all EpochScript reporter transforms to ensure complete coverage, compile-time validation, and exhaustive test definitions.

---

## Goal

Make Epoch the center of financial research by ensuring every reporter transform:
1. Has every valid layout combination **documented** in the handbook
2. Catches errors at **compile time**, not runtime
3. Has a **runnable test definition** for every layout form
4. **Renders correctly** on the dashboard (visually verified)

---

## Procedure (Per Family)

### Step 1: Gap Analysis + Feature Proposals

```
READ:
  - Metadata (.h inline ReportMetadata)
  - Implementation (.h + .cpp)
  - Builder (epoch-dashboard/include/epoch_dashboard/tearsheet/)
  - Frontend component (EpochPortal/src/components/dashboard/charts/)

ENUMERATE:
  - Every option and its valid values
  - Every input pattern (positional, named, tuple)
  - Every visually distinct layout combination

IDENTIFY GAPS:
  - Layouts you'd want but can't express today
  - Options declared but not wired
  - Frontend fields ignored
  - Missing options that would unlock common financial chart patterns
  - Cross-stack disconnections (builder has it, frontend doesn't, etc.)

PROPOSE:
  - Numbered list of feature additions with rationale
  - User accepts/rejects each proposal
```

**Output:** Gap analysis report with accepted feature list

### Step 2: Feature Development + Unit Tests

```
FOR EACH accepted feature:
  1. Write/update unit test first (test should fail or be missing)
  2. Implement the feature (metadata + impl + builder + frontend as needed)
  3. Build + run tests: ./cpp_tools/run_tests.sh --release -j16 <target>
  4. Verify all tests pass

ITERATE:
  - One feature at a time
  - No bundling multiple features in one edit
```

**Output:** Working features with passing tests

### Step 3: Handbook Update

```
UPDATE:
  - Handbook section with ALL layouts (old + new from Step 2)
  - ASCII art for each layout
  - Numbered Layout Catalog
  - Decision tree updated if new capabilities change routing
```

**Output:** Updated handbook section reflecting final state

### Step 4: Compile-Time Validations

```
AUDIT:
  - What errors currently wait until runtime?
  - What option combos are invalid but not checked?
  - What input patterns fail silently?

REGISTER:
  - New validation rules in the compiler
  - Clear error messages for each invalid combo
  - Build + test to confirm validations fire
```

**Output:** New/updated validator code, passing tests

### Step 5: Exhaustive Test Definitions

```
CREATE:
  - One .json definition per valid layout from Step 3
  - Naming: {family}_layout_{NN}_{description}.json
  - Use simple, reliable data sources (SPY 1D, multi-asset for CS)

RUN:
  - /run-job-data each definition
  - Confirm no runtime errors

VERIFY:
  - User visually inspects dashboard
  - Mark pass/fail in checklist below
```

**Output:** Complete set of test definitions, verification checklist

---

## Key Paths

```
BACKEND=/home/adesola/EpochDev/EpochBackend
PORTAL=/home/adesola/EpochDev/EpochPortal

# Reporter source
$BACKEND/packages/epoch-script/src/transforms/components/reports/

# Metadata (inline in .h files)
# Same directory as source

# Compiler validators
$BACKEND/packages/epoch-script/src/compiler/validators/

# Builders
$BACKEND/packages/epoch-dashboard/include/epoch_dashboard/tearsheet/
$BACKEND/packages/epoch-dashboard/src/tearsheet/

# Frontend components
$PORTAL/src/components/dashboard/charts/

# Proto definitions
$BACKEND/packages/epoch-protos/proto/

# Handbook (design reference)
/home/adesola/EpochDev/AgentSwarm/reference/epochscript_handbook_layout copy.md

# Test definitions (output)
/home/adesola/EpochDev/ClaudeCodeResearch/project/definitions/test_runner/

# Verification tracking
/home/adesola/EpochDev/ClaudeCodeResearch/project/verification/
```

---

## Family Tracker

| # | Family | Variants | Step 1 (Gaps) | Step 2 (Features) | Step 3 (Handbook) | Step 4 (Validations) | Step 5 (Tests) | Status |
|---|--------|----------|---------------|-------------------|-------------------|---------------------|----------------|--------|
| 1 | **Lines** | xy_lines, cs_lines, timeseries_lines, labeled_lines, cs_labeled_lines | DONE | DONE | DONE | - | DONE | Complete (28 layouts, band legend, plot bands, overlays) |
| 2 | **Bars** | xy_bars, cs_bars, (timeseries_bars disabled) | DONE | DONE | DONE | DONE | DONE | Complete (21 layouts: 13 xy_bars + 8 cs_bars, BarSeriesSchemaValidator, bars_handbook.json verified) |
| 3 | **Table** | cards, summary_table, cs_cards, cs_summary_table | DONE | N/A (agent-facing only) | DONE | DONE (TableSchemaValidator) | DONE | Complete (12 layouts: 7 summary_table + 5 cs_summary_table, tables_handbook.json verified. ENG-687: schema=TableReportSchema crashes at runtime) |
| 4 | **Heatmap** | heatmap, cs_heatmap | DONE | DONE | DONE | DONE | DONE | Complete (19 layouts: 11 heatmap + 8 cs_heatmap, ColorStopSchema, HeatmapSchemaValidator, heatmap_handbook.json verified) |
| 5 | **Scatter** | xy_scatter, cs_scatter, labeled_scatter, cs_labeled_scatter | - | - | - | - | - | NOT STARTED |
| 6 | **Boxplot** | boxplot, cs_boxplot | DONE | DONE (none needed) | DONE | - | DONE | Complete (10 layouts: 6 boxplot + 4 cs_boxplot, boxplot_handbook.json verified) |
| 7 | **Bubble** | bubble, cs_bubble | DONE | DONE (F1: size_by wired, F2: reference_lines wired, F3: removed misleading z input from cs_bubble, F4: removed misleading agg from cs_bubble) | DONE | DONE (bubble_validator.cpp) | DONE | Complete (13 layouts: 7 bubble + 6 cs_bubble, 26 unit tests / 462 assertions, bubble_handbook.json verified) |
| 8 | **Pie** | pie, cs_pie | - | - | - | - | - | NOT STARTED |
| 9 | **Gauge** | gauge, cs_gauge | DONE | N/A | DONE | N/A | DONE | Complete (12 layouts, gauge_handbook.json verified) |
| 10 | **Histogram** | histogram, cs_histogram | DONE | DONE (pre-aggregation, cs_histogram, plot bands) | DONE | DONE (HistogramSchemaValidator) | DONE | Complete (11 layouts: 8 histogram + 3 cs_histogram, pre-aggregated bins in proto, server-side analytics, histogram_handbook.json verified) |

**Legend:** `-` = not done, `DONE` = complete, `IN PROGRESS` = working on it

---

## Reporter Registry (28 Active)

### Per-Asset (14)
| ID | Family | Template | File |
|----|--------|----------|------|
| xy_lines | Lines | `Lines<false, false>` | lines.h |
| timeseries_lines | Lines | `Lines<true, false>` | lines.h |
| labeled_lines | Lines | `LabeledLines<false>` | labeled_lines.h |
| xy_bars | Bars | `Bars<false, false>` | bars.h |
| xy_scatter | Scatter | `Scatter<false>` | scatter.h |
| labeled_scatter | Scatter | `LabeledScatter<false>` | labeled_scatter.h |
| bubble | Bubble | `Bubble<false>` | bubble.h |
| boxplot | Boxplot | `Boxplot<false>` | boxplot.h |
| heatmap | Heatmap | `Heatmap<false>` | heatmap.h |
| histogram | Histogram | `Histogram<false>` | histogram.h |
| pie | Pie | `Pie<false>` | pie.h |
| gauge | Gauge | `Gauge<false>` | gauge.h |
| cards | Table | `Table<Cards, false>` | table.h |
| summary_table | Table | `Table<Summary, false>` | table.h |

### Cross-Sectional (14)
| ID | Family | Template | File |
|----|--------|----------|------|
| cs_lines | Lines | `Lines<false, true>` | lines.h |
| cs_labeled_lines | Lines | `LabeledLines<true>` | labeled_lines.h |
| cs_bars | Bars | `Bars<false, true>` | bars.h |
| cs_scatter | Scatter | `Scatter<true>` | scatter.h |
| cs_labeled_scatter | Scatter | `LabeledScatter<true>` | labeled_scatter.h |
| cs_bubble | Bubble | `Bubble<true>` | bubble.h |
| cs_boxplot | Boxplot | `Boxplot<true>` | boxplot.h |
| cs_heatmap | Heatmap | `Heatmap<true>` | heatmap.h |
| cs_histogram | Histogram | `Histogram<true>` | histogram.h |
| cs_pie | Pie | `Pie<true>` | pie.h |
| cs_gauge | Gauge | `Gauge<true>` | gauge.h |
| cs_cards | Table | `Table<Cards, true>` | table.h |
| cs_summary_table | Table | `Table<Summary, true>` | table.h |

### Disabled (1)
| ID | Family | Template | File | Reason |
|----|--------|----------|------|--------|
| timeseries_bars | Bars | `Bars<true, false>` | bars.h | Commented out in register.h |

### Deleted (no impl)
bellcurve, treemap, treegraph, sankey, waterfall, xrange, gap_report, arearange (unregistered)

---

## Verification Checklist Template

Each family gets a verification file at `project/verification/{family}_verification.md`:

```markdown
# {Family} Layout Verification

| # | Definition | Layout Description | Compiles | Runs | Renders | Notes |
|---|------------|-------------------|----------|------|---------|-------|
| 1 | lines_layout_01_basic.json | Single series time plot | - | - | - | |
| 2 | lines_layout_02_multi.json | Two series overlay | - | - | - | |
```

User marks each cell after visual inspection.
