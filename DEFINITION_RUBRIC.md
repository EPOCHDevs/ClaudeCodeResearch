# Definition Evaluation Rubric

Checklist for evaluating all 74 EpochScript definitions against their ScriptTemplate manifests.

---

## How to Use

For each definition (`project/definitions/test_runner/*.json`):

1. Load the definition's `source` field (the EpochScript code)
2. Load the matching ScriptTemplate manifest entry (`ScriptTemplates/{research|strategy}/manifest.json`)
3. Optionally load the `.epochscript` file for the canonical script
4. Score each rubric category below (PASS / NEEDS_FIX / N/A)
5. Record findings in a results CSV or table

---

## A. Report Component Usage

### A1. Cards — Use Sparingly (1-3 Overarching Metrics Only)

| Check | Pass | Fail |
|-------|------|------|
| Card count | 1-3 hero/summary metrics | 4+ cards acting as a data dump |
| Card purpose | High-level KPIs only (e.g., total return, win rate, sample count) | Granular per-window or per-regime stats crammed into cards |
| Aggregation diversity | Uses appropriate agg (Last, Sum, Count) for the metric type | Every card is `AggregationType.Mean` on returns |
| Hero slot | Exactly 1 card uses `card_slot=CardSlot.Hero` | Multiple heroes or no hero designated |

**Preferred alternative:** If you need 4+ summary metrics, use `summary_table()` instead.

### A2. Summary Tables — The Default for Structured Summaries

| Check | Pass | Fail |
|-------|------|------|
| Multi-metric summaries | Uses `summary_table()` for 4+ row structured data | Uses 8+ cards instead |
| Row/col structure | Named rows with meaningful column headers (e.g., "Last Session" vs "20-Day Avg") | Flat list that should be cards |
| Aggregation columns | At least 2 columns showing different aggregations (Last vs Mean, or Current vs Historical) | Single column (should be cards) |

### A3. Event Markers — Purpose Check

| Check | Pass | Fail |
|-------|------|------|
| Marks meaningful events | Trade entries/exits, signal triggers, regime changes | Marks every bar or trivial conditions |
| Schema completeness | Has title, icon, Hero + Details slots with relevant fields | Missing icon or empty schema |
| Boolean filter | First schema column is `BooleanFormat` with `table_is_filter=True` | No filter column |

---

## B. Timeframe Usage

### B1. Only Add Timeframe to Nodes for Multi-Timeframe Charts

| Check | Pass | Fail |
|-------|------|------|
| Base timeframe | Uses `global_timeframe` or single `market_data_source(timeframe=X)` | Multiple timeframe specifications without multi-TF purpose |
| Transform nodes | No `timeframe=` on individual transforms (sma, stddev, roc, etc.) | Transforms carry redundant `timeframe=` that matches global |
| Multi-TF justified | If multiple timeframes exist, they serve a clear analytical purpose (e.g., 1Min data + 1D aggregation) | Extra timeframes "just in case" |

### B2. Reasonable Approximation on Base Timeframe

| Check | Pass | Fail |
|-------|------|------|
| Period estimation | Uses bar-count approximation for daily stats on intraday data (e.g., `period=78` for ~1 day of 5Min bars) | Creates a separate 1D data source just to get a daily SMA |
| Session windows | Uses `session_window()` for intraday aggregation to daily-equivalent | Adds 1D timeframe node solely for session-level values |

---

## C. Chart Quality

### C1. Chart Type Selection

| Check | Pass | Fail |
|-------|------|------|
| Time series data | Uses `xy_lines` for continuous series | Uses `xy_scatter` for time series |
| Distributions | Uses `histogram` for single-variable distributions | Uses `boxplot` for single series (boxplot needs 2+ series comparison) |
| Category comparisons | Uses `xy_bars` with `label=` for categorical breakdowns | Uses `xy_lines` for bar-chart-like data |
| Multi-series comparison | Uses `boxplot` to compare distributions across 2+ groups | Uses overlaid histograms (hard to read) |
| Scatter relationships | Uses `xy_scatter` for X-Y relationship analysis | Uses `xy_lines` connecting unordered points |

### C2. Visual Styling

| Check | Pass | Fail |
|-------|------|------|
| Series colors | Every `LineSeriesSpec` / `BarSeriesSpec` has explicit `color=Color.X` | Missing colors (relies on defaults) |
| Reference lines | Uses `DashStyle.Dash` for reference/threshold lines | Reference lines use solid style (indistinguishable from data) |
| Reference line color | Uses `Color.Gray` or muted color for reference lines | Reference lines use bright data colors |
| Reference line title | Every `ReferenceLine` has a `title=` | Unlabeled reference lines |
| Color semantics | Green/Success for positive, Red/Error for negative, Blue for neutral data | Random color assignments |
| Axis labels | `y_axis_label` and `x_axis_label` specified on all charts | Missing axis labels |
| Axis format | `y_axis_format` / `x_axis_format` matches data type (PercentFormat for returns, MonetaryFormat for prices) | Wrong format or missing |

### C3. Bar Chart Specifics

| Check | Pass | Fail |
|-------|------|------|
| `color_by_value` | Set to `True` when bars can be positive/negative | Missing on signed-value bars |
| `data_labels` | Set to `True` for readability | Missing on summary bars |

---

## D. Statistical Rigor

### D1. Metric Diversity (Avoid "Average Returns Everywhere")

| Check | Pass | Fail |
|-------|------|------|
| Central tendency | Reports both mean AND median where distribution may be skewed | Only reports mean |
| Dispersion | Includes stddev, IQR, or min/max range | No dispersion metrics |
| Distribution shape | Histogram or boxplot showing actual distribution | Only scalar summary stats |
| Robustness | Uses median for skewed data (returns, ratios) | Uses mean for heavily skewed metrics |

### D2. Aggregation in Cards/Tables

| Check | Pass | Fail |
|-------|------|------|
| Agg type variety | Uses Sum (counts), Mean (averages), Last (current), Max/Min (extremes) as appropriate | Everything is `AggregationType.Mean` |
| Count context | Win/loss/trigger counts shown alongside rates | Only shows rates without sample size |

---

## E. Manifest Alignment

### E1. Definition vs Manifest Description

| Check | Pass | Fail |
|-------|------|------|
| Data sources match | Definition loads the assets/indicators described in manifest | Missing data sources or extra unexplained sources |
| Methodology match | Computation approach matches manifest description | Manifest says "rolling correlation" but definition uses simple diff |
| Dashboard match | Report components cover what manifest DASHBOARD line describes | Manifest promises charts that don't exist in definition |
| Tag consistency | Definition behavior matches manifest tags (intraday, methodology, asset_class) | Tags say `intraday: true` but no session windows or intraday data |

### E2. Definition vs .epochscript File

| Check | Pass | Fail |
|-------|------|------|
| Source match | Definition `source` field matches `.epochscript` content | Diverged — one was updated without the other |
| Config match | Definition `data.assets`, `global_timeframe` consistent with script | Script references assets not in definition config |

---

## Scoring Summary Template

```
| Definition | A1 Cards | A2 Tables | A3 Events | B1 TF | B2 Approx | C1 Type | C2 Style | C3 Bars | D1 Stats | D2 Agg | E1 Manifest | E2 Script | Notes |
|------------|----------|-----------|-----------|-------|-----------|---------|----------|---------|----------|--------|-------------|-----------|-------|
| spy_morning_dip_research | FAIL(8) | N/A | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | FAIL | PASS | ? | Cards overloaded, only mean returns |
```

Status key: PASS / FAIL(reason) / N/A (not applicable for this definition type)

---

## Common Anti-Patterns to Flag

1. **Card overload** — 5+ cards when a summary_table would be cleaner
2. **Average-only stats** — Cards showing only `AggregationType.Mean` on returns with no stddev/median/distribution
3. **Missing colors** — Charts without explicit color specs on series
4. **Solid reference lines** — Reference lines without `DashStyle.Dash`
5. **Unnecessary timeframes** — `timeframe=` on transforms that inherit from global
6. **Histogram for comparison** — Using histogram when boxplot would compare groups better
7. **Scatter for time series** — Using xy_scatter for ordered temporal data
8. **Manifest drift** — Definition promises things the manifest doesn't describe, or vice versa
9. **Missing axis labels/formats** — Charts without proper axis annotation
10. **No sample size context** — Showing win rates or averages without counts
