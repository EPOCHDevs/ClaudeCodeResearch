# EpochScript Transform Refactor Design

> ⚠ **SUPERSEDED** — This document is the original conceptual design.
> The live implementation plan is **[COMPILER_MACRO_PLAN.md](COMPILER_MACRO_PLAN.md)** and the phase files.
> Key differences from this doc: `rolling_stat` was replaced by `agg` builtin; `resample` is single-stage macro (not two-stage); `mom` is now `diff`.
> Keep this file for historical context only.

**Status:** Superseded by COMPILER_MACRO_PLAN.md
**Date:** 2026-03-28
**Scope:** All 299 transforms — intent-focused API, variadic Sequence outputs, scope unification

---

## Motivation

The library's current surface area has two failure modes:

1. **Implementation-detail naming** — users choose between `upsample`/`downsample`, `volatility`/`basic_volatility`, or five different "reference OHLCV" calls by reasoning about *how* something works, not *what* they want.
2. **Forced duplication** — fetching 4 macro indicators requires 4 identical calls; detecting 3 candlestick patterns requires 3 identical transforms; getting both correlation and covariance requires duplicated window params.

The refactor applies three axes of unification:

- **Scope axis** — `cs_*` transforms become the base transform with `cross_sectional=True`
- **Aggregation axis** — `min`, `max`, `sum`, `stddev`, `var` become `rolling_stat(agg=...)`
- **Sequence axis** — N-element Sequence option → N independent variadic outputs (compile-time macro; all outputs must be the same type)

---

## Design Constraints

- **Variadic output constraint:** All variadic outputs from a Sequence must be the same type (e.g., all `Decimal`, all `Integer`). This is a compile-time expansion — each element maps to a separate existing runtime node.
- **Backward compat:** Old transform IDs become aliases during a migration window; no scripts break on upgrade.
- **Scope flag semantics:** `cross_sectional=True` changes the aggregation *axis* — time-series operates along rows (per-asset over time); cross-sectional operates along columns (across assets at each timestamp). Period param only applies to time-series axis.

---

## Axis 1: Scope Unification — `cs_*` → base + `cross_sectional` flag

Every `cs_*` statistical transform is the same algorithm on a different axis. Instead of a parallel namespace, a single flag switches the axis.

### Statistical Transforms (direct pairs)

| Before (2 transforms) | After (1 transform) | Key param difference |
|---|---|---|
| `winsorize` + `cs_winsorize` | `winsorize(cross_sectional=False)` | `period` (ts) vs `group_by` (cs) |
| `zscore` + `cs_zscore` | `zscore(cross_sectional=False)` | `period` (ts) vs `group_by` (cs) |
| `cs_rank` *(no ts counterpart)* | `rank(cross_sectional=True)` | new ts rank via `nlargest`/`nsmallest` semantics |
| `cs_quantile` *(no ts counterpart)* | `quantile(cross_sectional=True, q=0.5)` | new ts rolling quantile |
| `cs_weighted_mean` *(no ts counterpart)* | `weighted_mean(cross_sectional=True)` | new ts weighted rolling mean |
| `cs_first_last` *(no ts counterpart)* | `first_last(cross_sectional=True)` | new ts boundary values |
| `cs_rank_quantile` | `rank_quantile(cross_sectional=True)` | cross-sectional only for now |
| `cs_select` | `select(cross_sectional=True)` | top/bottom N assets |
| `cs_momentum` | `momentum(cross_sectional=True)` | relative momentum across assets |

**API pattern:**
```python
# Time-series (default) — operates per-asset over N periods
score = zscore(period=60)(signal)

# Cross-sectional — operates across assets at each timestamp
score = zscore(cross_sectional=True, group_by=GroupBy.sector)(signal)
```

**Params that only apply per axis:**

| Param | Time-series | Cross-sectional |
|---|---|---|
| `period` / `window` | ✓ | ✗ (ignored) |
| `window_type` | ✓ | ✗ |
| `group_by` | ✗ | ✓ |

### Reporter `cs_*` — keep separate

Reporter transforms (`cs_bars`, `cs_lines`, `cs_scatter`, `cs_histogram`, `cs_boxplot`, `cs_bubble`, `cs_pie`, `cs_gauge`, `cs_heatmap`, `cs_summary_table`, `cs_labeled_*`, `cs_news`) are **not** scope variants of their non-cs counterparts — they are genuinely different chart types optimized for cross-sectional visualization. Keep them as-is.

---

## Axis 2: Aggregation Unification — rolling math primitives → `rolling_stat`

### Current: 5 separate rolling transforms

```python
peak = max(period=52)(price)
trough = min(period=52)(price)
total = sum(period=20)(returns)
vol = stddev(period=20)(returns)
dispersion = var(period=20)(returns)
```

### After: `rolling_stat(agg=AggregationType, period=N)`

```python
peak = rolling_stat(agg=Agg.Max, period=52)(price)
trough = rolling_stat(agg=Agg.Min, period=52)(price)
total = rolling_stat(agg=Agg.Sum, period=20)(returns)
vol = rolling_stat(agg=Agg.Std, period=20)(returns)
dispersion = rolling_stat(agg=Agg.Var, period=20)(returns)
```

**Key insight:** `cs_agg` already exists with the full `AggregationType` enum (Mean, Sum, Min, Max, Median, Std, Var, Skew, Kurtosis, Count, CountDistinct, Product, Quantile, First, Last, Mode, Any, All). The time-series counterpart `rolling_stat` mirrors it with a `period` param instead of `group_by`.

### Combining both axes

With `cross_sectional` flag, `rolling_stat` and `cs_agg` unify completely:

```python
# Time-series rolling (was: min/max/sum/stddev/var)
result = rolling_stat(agg=Agg.Max, period=52)(price)

# Cross-sectional (was: cs_agg)
result = rolling_stat(agg=Agg.Mean, cross_sectional=True, group_by=GroupBy.sector)(signal)
```

### Transform map

| Old | New |
|---|---|
| `min(period=N)` | `rolling_stat(agg=Agg.Min, period=N)` |
| `max(period=N)` | `rolling_stat(agg=Agg.Max, period=N)` |
| `sum(period=N)` | `rolling_stat(agg=Agg.Sum, period=N)` |
| `stddev(period=N)` | `rolling_stat(agg=Agg.Std, period=N)` |
| `var(period=N)` | `rolling_stat(agg=Agg.Var, period=N)` |
| `cs_agg(type=T, group_by=G)` | `rolling_stat(agg=T, cross_sectional=True, group_by=G)` |

**Saves 6 transforms.** `AggregationType` already has 17 values — `rolling_stat` unlocks rolling mean, median, skew, kurtosis, etc. for free.

---

## Axis 3: Sequence / Variadic Outputs

A Sequence of N elements produces N independent outputs. Each element maps to an existing runtime node. All outputs must be the same type.

### 3a. Reference Data Sources → `reference_assets` *(in progress)*

```python
# Before: 5 separate transforms
spy_data = reference_stocks(ticker=ReferenceStock.SPY)()          # → o,h,l,c,v
eur_data = fx_pairs(ticker=ReferenceFXPair.EURUSD)()              # → o,h,l,c,v
es_data  = reference_futures(ticker="ES")()                        # → o,h,l,c,v,oi
spx_data = common_indices(ticker=ReferenceIndex.SPX)()             # → o,h,l,c,v
btc_data = common_crypto_pairs(ticker=ReferenceCryptoPair.BTCUSD)() # → o,h,l,c,v

# After: unified, variadic
spy, eur   = reference_assets(stock("SPY"), fx("EURUSD"))()
spy, eur, es = reference_assets(stock("SPY"), fx("EURUSD"), futures("ES"))()
spy, eur   = reference_assets(stock("SPY"), fx("EURUSD"))()       # mixed asset classes
```

Also: `market_data_source` → `study_assets` (the strategy's own configurable feed).

```python
# Variadic timeframes on study feed
daily, hourly = study_assets(target_timeframe=["1D", "1H"])()
```

### 3b. `common_indicators` → `macro_data` (variadic)

**Problem:** Fetching multiple macro series requires N identical calls. The name `common_indicators` is vague — `MacroEconomicsIndicator` enum has 150+ values.

```python
# Before: one call per indicator
cpi      = common_indicators(category=MacroEconomicsIndicator.CPI)()
pce      = common_indicators(category=MacroEconomicsIndicator.PCE)()
unemp    = common_indicators(category=MacroEconomicsIndicator.Unemployment)()
fedfunds = common_indicators(category=MacroEconomicsIndicator.FedFunds)()

# After: variadic — all outputs are Decimal (same type ✓)
cpi, pce, unemp, fedfunds = macro_data(
    MacroIndicator.CPI,
    MacroIndicator.PCE,
    MacroIndicator.Unemployment,
    MacroIndicator.FedFunds
)()
```

**Saves:** N-1 lines per research script using multiple macro series.

### 3c. 26 Candlestick Patterns → `candlestick_pattern` (variadic)

All 26 candlestick transforms share identical `(o, h, l, c) → Integer` signature. Integer output is -100 (bearish), 0 (none), +100 (bullish).

```python
# Before: 26 separate transforms with identical signatures
d = doji()(o, h, l, c)
h = hammer()(o, h, l, c)
es = evening_star()(o, h, l, c)
ms = morning_star()(o, h, l, c)

# After: single enum, optional variadic
signal = candlestick_pattern(pattern=Pattern.doji)(o, h, l, c)

# Variadic: detect multiple, all Integer outputs (same type ✓)
doji_sig, hammer_sig, evening_star_sig = candlestick_pattern(
    patterns=[Pattern.doji, Pattern.hammer, Pattern.evening_star]
)(o, h, l, c)
```

**Full pattern enum:**
```
doji, dragonfly_doji, gravestone_doji, four_price_doji, long_legged_doji,
hammer, inverted_hammer, hanging_man, shooting_star,
morning_star, evening_star, morning_doji_star, evening_doji_star,
engulfing_bull, engulfing_bear,
three_white_soldiers, three_black_crows,
abandoned_baby_bull, abandoned_baby_bear,
marubozu_bull, marubozu_bear, spinning_top, star, big_candle_bull, big_candle_bear
```

**Saves: 25 transforms (26 → 1).**

### 3d. `rolling_corr` + `rolling_cov` → `pair_stat` (variadic metrics)

Both transforms: `(x: Decimal, y: Decimal) → Decimal`, identical window params, differ only in metric computed.

```python
# Before: duplicated window params
corr = rolling_corr(window=60, window_type="rolling", method="pearson")(ret_a, ret_b)
cov  = rolling_cov(window=60, window_type="rolling")(ret_a, ret_b)

# After: single transform, variadic metrics, all Decimal (same type ✓)
corr, cov = pair_stat(
    metrics=[PairMetric.correlation, PairMetric.covariance],
    window=60,
    window_type="rolling",
    correlation_method="pearson"
)(ret_a, ret_b)

# Single metric still works
corr = pair_stat(metrics=[PairMetric.correlation], window=60)(ret_a, ret_b)
```

**Extension:** `beta` and `ewm_corr` also have `(x, y) → Decimal` pairwise signature — they join this family:

```python
corr, cov, beta = pair_stat(
    metrics=[PairMetric.correlation, PairMetric.covariance, PairMetric.beta],
    window=60
)(ret_a, ret_b)
```

**Saves:** `rolling_corr`, `rolling_cov`, `beta`, `ewm_corr` → 1 transform.

---

## Other Targeted Cleanups

### `upsample` + `downsample` → `resample`

**Problem:** Users must know whether target timeframe is higher or lower frequency — an implementation detail. Intent is "change timeframe."

Direction is deterministic from timeframes (inferred at compile time). Secondary params differ: `agg` (list per column) for downsample; `how` (fill method) for upsample — these are self-documenting.

```python
# Before: pick the right one
o, h, l, c = downsample(target_timeframe="1D", agg=[first, max, min, last])(o15m, h15m, l15m, c15m)
c_1min = upsample(target_timeframe="1min", how=FillMethod.ffill)(c_daily)

# After: unified — direction inferred from source vs target
o, h, l, c = resample(target_timeframe="1D", agg=[first, max, min, last])(o15m, h15m, l15m, c15m)
c_1min = resample(target_timeframe="1min", how=FillMethod.ffill)(c_daily)
```

### `volatility` + `basic_volatility` → `volatility(method=...)`

**Problem:** Two close-only volatility transforms with overlapping purpose and confusing names.

| | `volatility` | `basic_volatility` |
|---|---|---|
| Input | close | close |
| Method | annualized log-return stddev | `return_type` or `price_diff` (enum) |
| Annualized | yes | no |

```python
# Before
vol1 = volatility(period=14)(c)                                      # annualized
vol2 = basic_volatility(type=BasicVolatilityType.return_type, period=20)(c)
vol3 = basic_volatility(type=BasicVolatilityType.price_diff, period=20)(c)

# After: unified VolatilityMethod enum
vol = volatility(method=VolatilityMethod.annualized, period=14)(c)    # was volatility()
vol = volatility(method=VolatilityMethod.returns, period=20)(c)        # was basic_volatility(return_type)
vol = volatility(method=VolatilityMethod.price_diff, period=20)(c)     # was basic_volatility(price_diff)
```

`volatility_estimator` stays **separate** — it requires OHLC inputs (4 args vs 1). `VolatilityEstimatorType` (garman_klass, parkinson, yang_zhang, hodges_tompkins) already documents it well.

---

## Full Transform Count Summary

| Change | Before | After | Saves |
|---|---|---|---|
| Reference OHLCV (5 sources → `reference_assets`) | 5 | 2 | 3 |
| `common_indicators` → `macro_data` variadic | 1 | 1 | 0 transforms, but N-1 lines per use |
| Candlestick patterns → `candlestick_pattern` | 26 | 1 | 25 |
| `pair_stat` (corr + cov + beta + ewm_corr) | 4 | 1 | 3 |
| `rolling_stat` (min + max + sum + stddev + var + cs_agg) | 6 | 1 | 5 |
| `resample` (upsample + downsample) | 2 | 1 | 1 |
| `volatility` absorbs `basic_volatility` | 2 | 1 | 1 |
| `cs_*` statistical scope flag (9 pairs) | 18 | 9 | 9 |
| **Total** | **64** | **17** | **47 transforms** |

---

## What NOT to Merge

| Transforms | Reason |
|---|---|
| `rolling_adf`, `rolling_arima`, `rolling_garch`, `rolling_hurst_exponent` | Different algorithms, heterogeneous multi-output types (p-value, test-stat, critical values, forecasts) |
| `engle_granger` + `johansen` | Different cointegration tests, different output count per test |
| `volatility_estimator` | OHLC inputs (4 args) vs `volatility` close input (1 arg) — different type signature |
| Reporter `cs_*` (bars, lines, scatter, histogram, etc.) | Genuinely different visualization semantics, not scope variants |
| ML transforms (LightGBM, Logistic, SVR, KMeans, etc.) | Unique hyperparameter surfaces per algorithm |
| `earnings`, `analyst_ratings`, `dividends`, `news` | Genuinely different output schemas, already intent-named |
| `string_contains`, `string_trim`, `string_case`, `string_check` | Mixed output types (Boolean vs String) — already reasonably focused |

---

## Implementation Order (suggested)

1. **`rolling_stat`** — pure enum consolidation, no new concepts, immediate simplification
2. **`cs_*` scope flag** — add `cross_sectional` param to statistical transforms, alias old names
3. **`candlestick_pattern`** — largest transform count reduction (25 saves), pure enum + variadic
4. **`resample`** — intent rename, direction inference, simple merge
5. **`volatility`** — absorb `basic_volatility` with method enum
6. **`pair_stat`** — variadic pairwise metrics
7. **`macro_data`** — variadic macro series (requires Sequence runtime support)
8. **`reference_assets` / `study_assets`** — in progress separately

---

## New Enums Required

```
VolatilityMethod:
  annualized, returns, price_diff

PairMetric:
  correlation, covariance, beta, ewm_correlation

CandlestickPattern:
  doji, dragonfly_doji, gravestone_doji, four_price_doji, long_legged_doji,
  hammer, inverted_hammer, hanging_man, shooting_star,
  morning_star, evening_star, morning_doji_star, evening_doji_star,
  engulfing_bull, engulfing_bear,
  three_white_soldiers, three_black_crows,
  abandoned_baby_bull, abandoned_baby_bear,
  marubozu_bull, marubozu_bear, spinning_top, star,
  big_candle_bull, big_candle_bear

MacroIndicator:
  (rename/alias of MacroEconomicsIndicator — same 150+ values)
```

`AggregationType` already exists with all needed values.
`Scope` / `cross_sectional: Boolean` — simple flag, no new enum needed.
