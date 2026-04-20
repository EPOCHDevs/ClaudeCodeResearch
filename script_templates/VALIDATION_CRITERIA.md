# Script Template Validation Criteria

## Status Definitions

| Status | Meaning | Criteria |
|--------|---------|----------|
| **OPEN** | Not yet processed | No grammar refactoring or execution attempted |
| **REFACTORED** | Grammar updated | Layer 1/2/3 syntax applied, not yet executed |
| **EXECUTED** | Ran without crash | `generate_job_data` completed, output directory exists |
| **VALIDATED** | Research objective met | All structural + semantic + quality checks pass |
| **DEGRADED** | Runs but incomplete | Executes but has quality issues (empty charts, no signals, etc.) |
| **PARSE_ERROR** | Won't compile | EpochScript compiler rejects the source |
| **RUNTIME_ERROR** | Crashes during run | Execution fails (data issues, transform errors) |
| **INFRA_ERROR** | Infrastructure issue | Permissions, missing cache paths, network |

## Validation Checks

### 1. Structural Checks (must pass)

- [ ] `manifest.json` exists in study output
- [ ] `tearsheets/metadata.json` exists with at least 1 category
- [ ] Each chart in schema has a corresponding `.arrow` data file
- [ ] Market data table exists with > 0 rows
- [ ] Date range covers the requested study period

### 2. Semantic Checks (must pass for VALIDATED)

- [ ] **Charts have data**: Every chart's arrow file has rows. Series columns are not all-null.
- [ ] **Tables have values**: Summary tables render with populated cells, not all zeros or NaN.
- [ ] **Signals fire**: For event-driven studies, event markers have > 0 events. Where-filtered columns have some non-null values (signals are triggering).
- [ ] **Computed columns work**: Key computed transforms (SMA, RSI, returns, etc.) produce non-null output after warmup period.

### 3. Quality Checks (warnings, don't block VALIDATED)

- [ ] **Sample size**: Signal/event count > 3 for statistical relevance
- [ ] **No degenerate results**: Charts don't show flat lines or identical values across all series
- [ ] **Return calculations**: Forward/backward returns are within reasonable bounds (not > 1000%)
- [ ] **Date continuity**: No unexpected large gaps in market data index

## Grammar Refactoring Rules

When refactoring definitions from old to new grammar:

### Layer 1 (Builtins) — single-stage: `fn(inputs, options)`

```python
# OLD (Layer 3 style)              → NEW (Layer 1 style)
market_data_source(timeframe=1D)()  → study_assets()
economic_indicators(series_id='X')()→ economic_indicators(series_id="X")
earnings()()                        → earnings()
analyst_ratings()()                 → analyst_ratings()
short_volume()()                    → short_volume()
short_interest()()                  → short_interest()
income_statement(period=X)()        → income_statement(period=X)
balance_sheet(period=X)()           → balance_sheet(period=X)
dividends(dividend_type=X)()        → dividends(dividend_type=X)
economic_calendar(source=X, ...)()  → economic_calendar(source=X, ...)

sma(period=20)(close)               → sma(close, 20)
ema(period=10)(close)               → ema(close, 10)
rsi(period=14)(close)               → rsi(close, 14)
roc(period=12)(close)               → roc(close, 12)
atr(period=14)(h, l, c)             → atr(h, l, c, 14)

corr(window=60)(a, b)               → corr(a, b, window=60)
beta(window=252)(a, b)              → beta(a, b, window=252)
```

### Layer 2 (Macros) — single-stage: `fn(inputs, options)`

```python
# OLD                               → NEW
volatility(method=X, period=N)(src) → volatility(src, method=X, period=N)
donchian_channel(window=N)(h, l)    → donchian_channel(h, l, window=N)
# bbands, macd, stoch, aroon, supertrend, ichimoku, keltner_channels follow same pattern
```

### Layer 3 (Registered Transforms) — two-stage: `fn(options)(inputs)`

These keep the existing `fn(options)(inputs)` syntax:
- All Reporter transforms: `xy_bars(...)()`, `xy_lines(...)()`, `summary_table(...)()`, etc.
- All Compute transforms: `kalman_filter(...)()`, `zscore(...)()`, etc.
- All ML, Portfolio, Execution transforms

### JSON Schema

Remove `"global_timeframe"` field — not in `StudyDefinition` struct.

## Tracking

Results tracked in `definition_status.csv`:

| Column | Description |
|--------|-------------|
| `file` | Definition filename |
| `name` | Study display name |
| `type` | `research` or `strategy` |
| `status` | See status definitions above |
| `assets` | Asset list (semicolon-separated) |
| `needs_refactor` | `yes` if old grammar patterns detected |
| `error` | Error message or validation notes |
