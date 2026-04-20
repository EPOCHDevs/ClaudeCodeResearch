# Transform Expansion Map

Pre-implementation reference. Every new construct mapped to every impl node it can lower to,
plus the complete list of transforms changing from `internalUse=false` → `internalUse=true`.

---

## Legend

```
[builtin]  — single-stage, added to BUILTIN_FUNCTIONS, Phase 2
[macro]    — single-stage, added to COMPILER_MACROS
[meta]     — two-stage registered transform gaining a new routing option (Phase 4)
→          — lowers to this impl node at compile time
⚠           — impl node may not exist yet; needs verification before implementing
```

---

## Phase 1 — resample `[macro]`

Direction inferred at compile time from source node's timeframe vs target timeframe.

### Downsample cases (source_tf < target_tf)

```
resample(src.c, target_timeframe="1D")
→  downsample(target_timeframe="1D", agg=[Last])(src.c)
   NOTE: default agg per input when agg= not specified — TBD (Last? must decide before implementing)

resample(src.c, target_timeframe="1D", agg=[Agg.Last])
→  downsample(target_timeframe="1D", agg=[Last])(src.c)

resample(src.c, src.h, target_timeframe="1D", agg=[Agg.Last, Agg.Max])   ← input-driven
→  downsample(target_timeframe="1D", agg=[Last])(src.c)
   downsample(target_timeframe="1D", agg=[Max])(src.h)

resample(src.c, target_timeframe=["1D","1W"])                             ← option-driven
→  downsample(target_timeframe="1D", agg=[Last])(src.c)
   downsample(target_timeframe="1W", agg=[Last])(src.c)

resample(src.c, target_timeframe=["1D","1W"], agg=[Agg.Last])
→  downsample(target_timeframe="1D", agg=[Last])(src.c)
   downsample(target_timeframe="1W", agg=[Last])(src.c)
```

### Upsample cases (source_tf > target_tf)

```
resample(daily_close, target_timeframe="1H")
→  upsample(target_timeframe="1H", how=ffill)(daily_close)
   NOTE: default how=FillMethod.ffill when how= not specified

resample(daily_close, target_timeframe="1H", how=FillMethod.ffill)
→  upsample(target_timeframe="1H", how=ffill)(daily_close)

resample(daily_close, target_timeframe="1H", how=FillMethod.bfill)
→  upsample(target_timeframe="1H", how=bfill)(daily_close)

resample(daily_close, target_timeframe="1H", how=FillMethod.nearest)
→  upsample(target_timeframe="1H", how=nearest)(daily_close)

resample(daily_close, target_timeframe="1H", how=FillMethod.asfreq)
→  upsample(target_timeframe="1H", how=asfreq)(daily_close)
```

### Combined / mixed-direction case (option-driven list, directions inferred per element)

Source timeframe sits between the targets — some larger (downsample), some smaller (upsample).
Direction is resolved independently per element in the list.

```
resample(daily_close, target_timeframe=["1W", "1H"])
→  downsample(target_timeframe="1W", agg=[Last])(daily_close)   ← 1W > 1D → downsample
   upsample(target_timeframe="1H", how=ffill)(daily_close)      ← 1H < 1D → upsample

resample(daily_close, target_timeframe=["1W", "1D", "1H"])
→  downsample(target_timeframe="1W", agg=[Last])(daily_close)
   COMPILE ERROR: resample to same timeframe has no effect ("1D")
   upsample(target_timeframe="1H", how=ffill)(daily_close)
   NOTE: same-TF element still errors even in a list — entire call fails

resample(daily_close, target_timeframe=["1W", "1H", "30m"])
→  downsample(target_timeframe="1W", agg=[Last])(daily_close)
   upsample(target_timeframe="1H", how=ffill)(daily_close)
   upsample(target_timeframe="30m", how=ffill)(daily_close)
```

Mixed direction + `agg=` or `how=` → compile error on conflicting elements:

```
resample(daily_close, target_timeframe=["1W", "1H"], agg=[Agg.Last])
→  COMPILE ERROR: agg implies downsample but "1H" is smaller than source timeframe

resample(daily_close, target_timeframe=["1W", "1H"], how=FillMethod.ffill)
→  COMPILE ERROR: how implies upsample but "1W" is larger than source timeframe
```

### Compile errors

```
resample(src.c, src.h, target_timeframe=["1D","1W"])
→  COMPILE ERROR: ambiguous expansion — both inputs (2) and target_timeframe list (2) are plural

resample(src.c, target_timeframe="1D", agg=[Agg.Last], how=FillMethod.ffill)
→  COMPILE ERROR: cannot specify both agg and how

resample(src.c, target_timeframe="1D")   where src.c is already "1D"
→  COMPILE ERROR: resample to same timeframe has no effect

resample(src.c, target_timeframe="1D")   where src.c timeframe is unknown
→  COMPILE ERROR: cannot infer resample direction — source timeframe unknown; use downsample() or upsample() directly

resample(src.c, target_timeframe="1D", agg=[Agg.Last, Agg.Max])   ← agg count > input count
→  COMPILE ERROR: agg list length (2) does not match input count (1)
```

### Impl nodes hidden after resample ships

| Impl node | Current options |
|---|---|
| `downsample` | target_timeframe (required), agg (List AggType, required) |
| `upsample` | target_timeframe (required), how (FillMethod, default ffill), limit (Int, default -1) |

---

## Phase 2 — agg `[builtin]`

### Rolling axis (3 positional args: src, N, Agg.X)

Second arg is integer → rolling window over N bars.

| Call | Lowers to impl node | Impl exists? |
|---|---|---|
| `agg(src, N, Agg.Max)` | `max(period=N)(src)` | ✓ |
| `agg(src, N, Agg.Min)` | `min(period=N)(src)` | ✓ |
| `agg(src, N, Agg.Sum)` | `sum(period=N)(src)` | ✓ |
| `agg(src, N, Agg.Std)` | `stddev(period=N)(src)` | ✓ |
| `agg(src, N, Agg.Var)` | `var(period=N)(src)` | ✓ |
| `agg(src, N, Agg.Mean)` | `ma(type=sma, period=N)(src)` | ✓ (ma exists, type=sma) |
| `agg(src, N, Agg.Median)` | `rolling_median(period=N)(src)` | ⚠ verify |
| `agg(src, N, Agg.Count)` | `rolling_count(period=N)(src)` | ⚠ verify |
| `agg(src, N, Agg.First)` | `rolling_first(period=N)(src)` | ⚠ verify |
| `agg(src, N, Agg.Last)` | `rolling_last(period=N)(src)` | ⚠ verify |
| `agg(src, N, Agg.Skew)` | `rolling_skew(period=N)(src)` | ⚠ verify |
| `agg(src, N, Agg.Kurtosis)` | `rolling_kurtosis(period=N)(src)` | ⚠ verify |
| `agg(src, N, Agg.Product)` | `rolling_product(period=N)(src)` | ⚠ verify |
| `agg(src, N, Agg.Mode)` | `rolling_mode(period=N)(src)` | ⚠ verify |
| `agg(src, N, Agg.Any)` | `rolling_any(period=N)(src)` | ⚠ verify |
| `agg(src, N, Agg.All)` | `rolling_all(period=N)(src)` | ⚠ verify |

**Phase 2 priority subset:** Max, Min, Sum, Std, Var, Mean — these 6 have confirmed impl nodes.
Remaining enum values → COMPILE ERROR "not yet supported" until their impl nodes are confirmed.

### Cross-sectional axis (cross_sectional=True required)

`agg(src, Agg.X)` with no kwarg → **COMPILE ERROR** — does not default to cs. Intent must be explicit.

```
agg(src, Agg.Mean, cross_sectional=True)
→  cs_agg(type=Mean)(src)

agg(src, Agg.Max, cross_sectional=True)
→  cs_agg(type=Max)(src)

agg(src, Agg.Min, cross_sectional=True)
→  cs_agg(type=Min)(src)

agg(src, Agg.Sum, cross_sectional=True)
→  cs_agg(type=Sum)(src)

agg(src, Agg.Std, cross_sectional=True)
→  cs_agg(type=Std)(src)

agg(src, Agg.Var, cross_sectional=True)
→  cs_agg(type=Var)(src)

agg(src, Agg.Median, cross_sectional=True)
→  cs_agg(type=Median)(src)

agg(src, Agg.Count, cross_sectional=True)
→  cs_agg(type=Count)(src)

agg(src, Agg.CountDistinct, cross_sectional=True)
→  cs_agg(type=CountDistinct)(src)   ← cs-only, no rolling equivalent

agg(src, Agg.Quantile, cross_sectional=True)
→  cs_agg(type=Quantile)(src)        ← cs-only, no rolling equivalent
```

### Cross-sectional grouped (group_by= kwarg — implies cs, no need for cross_sectional=True)

```
agg(src, Agg.Mean, group_by=GroupBy.sector)
→  cs_agg(type=Mean, group_by=sector)(src)

agg(src, Agg.Std, group_by=GroupBy.industry)
→  cs_agg(type=Std, group_by=industry)(src)

agg(src, Agg.Max, group_by=GroupBy.asset_class)
→  cs_agg(type=Max, group_by=asset_class)(src)
```

Any Agg value + any GroupBy value is valid (cs_agg supports all combinations).

### Compile errors

```
agg(src, Agg.Mean)
→  COMPILE ERROR: missing period for rolling form, or specify cross_sectional=True
   hint: did you mean agg(src, 20, Agg.Mean) or agg(src, Agg.Mean, cross_sectional=True)?

agg(src)
→  COMPILE ERROR: agg() requires at least 2 arguments

agg(src, 20, Agg.Max, group_by=GroupBy.sector)
→  COMPILE ERROR: rolling + group_by is ambiguous

agg(src, 20, Agg.Median)    (if rolling_median not yet implemented)
→  COMPILE ERROR: Agg.Median not yet supported in rolling form

agg(src, Agg.RollingMax, cross_sectional=True)
→  COMPILE ERROR: unknown AggregationType value "RollingMax"
```

---

## Phase 2 — valuewhen `[builtin]`

```
valuewhen(cond, src)
→  valuewhen(occurrence=0)(cond, src)

valuewhen(cond, src, 1)
→  valuewhen(occurrence=1)(cond, src)

valuewhen(cond, src, N)
→  valuewhen(occurrence=N)(cond, src)
```

Two-stage form `valuewhen(occurrence=0)(cond, src)` → COMPILE ERROR after promotion.

---

## Phase 2 — barssince `[builtin]`

```
barssince(cond)
→  barssince()(cond)
```

Two-stage form `barssince()(cond)` → COMPILE ERROR after promotion.

---

## Phase 2 — diff `[builtin]`

`diff` is the canonical public name (numpy/pandas convention). Lowers to existing `mom` impl node.
`change` dropped — identical formula. `mom` registered transform → `internalUse=true`.

```
diff(src)
→  mom(period=1)(src)     ← 1-bar absolute difference

diff(src, N)
→  mom(period=N)(src)     ← N-bar absolute difference
```

NOTE: `roc` (percentage ×100 form) stays as registered transform.

---

## Phase 2 — returns `[builtin]`

Arithmetic composite — no new impl node.

```
returns(src)
→  (src - lag(src,1)) / lag(src,1)

returns(src, N)
→  (src - lag(src,N)) / lag(src,N)

returns(src, type=ReturnType.Log)
→  ln(src / lag(src,1))

returns(src, N, type=ReturnType.Log)
→  ln(src / lag(src,N))
```

New enum: `ReturnType` (Simple, Log).

---

## Phase 2 — cum `[builtin]`

Expanding (cumulative from bar 0). Reuses `AggregationType` — no new enum.

```
cum(src)
→  expanding_sum()(src)       ⚠ verify impl node id

cum(src, Agg.Sum)
→  expanding_sum()(src)       ⚠ verify

cum(src, Agg.Product)
→  expanding_product()(src)   ⚠ verify

cum(src, Agg.Max)
→  expanding_max()(src)       ⚠ verify

cum(src, Agg.Min)
→  expanding_min()(src)       ⚠ verify
```

---

## Phase 2 — linreg `[builtin]`

All linear regression outputs under one name. New enum: `LinRegType` (Value, Slope, Intercept, Forecast).

```
linreg(src, N)
→  linearreg(period=N)(src)             ⚠ verify

linreg(src, N, type=LinRegType.Slope)
→  linearreg_slope(period=N)(src)       ⚠ verify

linreg(src, N, type=LinRegType.Intercept)
→  linearreg_intercept(period=N)(src)   ⚠ verify

linreg(src, N, type=LinRegType.Forecast)
→  tsf(period=N)(src)                   ⚠ verify
```

---

## Phase 2 — lag `[builtin]`

Compiler emits lag AST node directly — no impl node lookup.

```
lag(src, 1) → LagOp(src, 1)
lag(src, N) → LagOp(src, N)
```

---

## Phase 2 — prev `[builtin]`

Grammar-level rewrite — disappears from compiled graph.

```
prev(src) → lag(src, 1)
```

---

## Phase 2 — ratio `[builtin]`

Arithmetic composite — no impl node.

```
ratio(src)    → src / lag(src, 1)
ratio(src, N) → src / lag(src, N)
```

---

## Phase 2 — normalize `[builtin]`

Arithmetic composite using `agg`. `nz` guard prevents division by zero on flat windows.

```
normalize(src, N)
→  nz((src - agg(src, N, Agg.Min)) / (agg(src, N, Agg.Max) - agg(src, N, Agg.Min)), 0)
```

---

## Phase 2 — drawdown `[builtin]`

Arithmetic composite using `agg`. Result is ≤ 0.

```
drawdown(src, N)
→  (src - agg(src, N, Agg.Max)) / agg(src, N, Agg.Max)
```

---

## Phase 2 — to_int `[builtin]`

```
to_int(cond) → where(cond, 1, 0)
```

---

## Phase 2 — relu `[builtin]`

```
relu(src) → where(src > 0, src, 0)
```

---

## Phase 2 — between `[builtin]`

```
between(src, lo, hi) → (src >= lo) and (src <= hi)
```

---

## Phase 2 — isna `[builtin]`

Grammar alias — identical compiled node as `is_null`.

```
isna(src) → is_null(src)
```

---

## Phase 2 — notna `[builtin]`

Grammar alias — identical compiled node as `is_valid`.

```
notna(src) → is_valid(src)
```

---

## Phase 2 — nz `[builtin]`

Grammar-level rewrite — lowers to `coalesce` at compile time, no new impl node.

```
nz(src)
→  coalesce(src, 0.0)          ← default replacement=0

nz(src, fallback)
→  coalesce(src, fallback)
```

`coalesce` is already a builtin (variadic, no default). `nz` is the 2-arg null-guard shorthand
with `replacement=0` as default — `nz(eps)` vs `coalesce(eps, 0)` is the difference.
`nz` does not appear in the compiled node graph.

---

## Phase 2 — clamp `[builtin]` (arithmetic — no impl node)

```
clamp(src, lo, hi)
→  min(max(src, lo), hi)    (arithmetic using existing min/max builtins)
```

NOTE: These are the scalar arithmetic `min`/`max` builtins, not the rolling transform `min`/`max`.

---

## Phase 2 — sign `[builtin]` (arithmetic — no impl node)

```
sign(src)
→  where(src > 0, 1, where(src < 0, -1, 0))
```

---

## Phase 3 — marker `[macro]`

### Without price series (signal only)

```
marker(signal, Event.LongEntry)
→  event_marker(schema=EventMarkerSchema(
       title="Long Entry",
       icon=Icon.TrendingUpIcon,
       schemas=[]
   ))(signal)

marker(signal, Event.LongExit)
→  event_marker(schema=EventMarkerSchema(
       title="Long Exit",
       icon=Icon.TrendingDownIcon,
       schemas=[]
   ))(signal)

marker(signal, Event.RoundTrip)
→  event_marker(schema=EventMarkerSchema(
       title="Round Trip",
       icon=Icon.RepeatIcon,
       schemas=[]
   ))(signal)
```

### With price series

```
marker(signal, close, Event.LongEntry)
→  event_marker(schema=EventMarkerSchema(
       title="Long Entry",
       icon=Icon.TrendingUpIcon,
       schemas=[EventMarkerColumnSchema(title="Price", value=close)]
   ))(signal)
```

### With label override

```
marker(signal, close, Event.LongEntry, label="Entry")
→  event_marker(schema=EventMarkerSchema(
       title="Entry",                             ← label overrides default title
       icon=Icon.TrendingUpIcon,
       schemas=[EventMarkerColumnSchema(title="Price", value=close)]
   ))(signal)
```

### With price_source override

```
marker(signal, open, Event.LongEntry, price_source=Price.Open)
→  event_marker(schema=EventMarkerSchema(
       title="Long Entry",
       icon=Icon.TrendingUpIcon,
       schemas=[EventMarkerColumnSchema(title="Price", value=open)]
   ))(signal)
```

NOTE: `price_source=Price.Open` controls the column label only — the actual series passed
is whatever series_expr the user provides as the second positional argument.

### Event → default title + icon map

| Event value | Default title | Default icon |
|---|---|---|
| `RoundTrip` | "Round Trip" | `Icon.RepeatIcon` |
| `LongEntry` | "Long Entry" | `Icon.TrendingUpIcon` |
| `LongExit` | "Long Exit" | `Icon.TrendingDownIcon` |
| `ShortEntry` | "Short Entry" | `Icon.TrendingDownIcon` |
| `ShortExit` | "Short Exit" | `Icon.TrendingUpIcon` |
| `StopLoss` | "Stop Loss" | `Icon.ShieldIcon` |
| `TakeProfit` | "Take Profit" | `Icon.TargetIcon` |
| `Signal` | "Signal" | `Icon.BellIcon` |
| `Entry` | "Entry" | `Icon.TrendingUpIcon` |
| `Exit` | "Exit" | `Icon.TrendingDownIcon` |
| `Rebalance` | "Rebalance" | `Icon.RefreshIcon` |

⚠ Icon names (`Icon.RepeatIcon`, etc.) need verification against registered Icon enum values.

---

## Phase 3 — candlestick_pattern `[macro]`

N patterns in list → N impl nodes, all sharing the same (o, h, l, c) inputs.
Each impl node is called with no options (default thresholds).

```
candlestick_pattern(o, h, l, c, patterns=[Pattern.doji])
→  doji()(o, h, l, c)

candlestick_pattern(o, h, l, c, patterns=[Pattern.hammer])
→  hammer()(o, h, l, c)

candlestick_pattern(o, h, l, c, patterns=[Pattern.doji, Pattern.hammer, Pattern.engulfing_bull])
→  doji()(o, h, l, c)
   hammer()(o, h, l, c)
   engulfing_bull()(o, h, l, c)
```

### Full pattern → impl node map

| Pattern enum value | Impl node id |
|---|---|
| `Pattern.doji` | `doji` |
| `Pattern.dragonfly_doji` | `dragonfly_doji` |
| `Pattern.gravestone_doji` | `gravestone_doji` |
| `Pattern.four_price_doji` | `four_price_doji` |
| `Pattern.long_legged_doji` | `long_legged_doji` |
| `Pattern.hammer` | `hammer` |
| `Pattern.inverted_hammer` | `inverted_hammer` |
| `Pattern.hanging_man` | `hanging_man` |
| `Pattern.shooting_star` | `shooting_star` |
| `Pattern.morning_star` | `morning_star` |
| `Pattern.evening_star` | `evening_star` |
| `Pattern.morning_doji_star` | `morning_doji_star` |
| `Pattern.evening_doji_star` | `evening_doji_star` |
| `Pattern.engulfing_bull` | `engulfing_bull` |
| `Pattern.engulfing_bear` | `engulfing_bear` |
| `Pattern.three_white_soldiers` | `three_white_soldiers` |
| `Pattern.three_black_crows` | `three_black_crows` |
| `Pattern.abandoned_baby_bull` | `abandoned_baby_bull` |
| `Pattern.abandoned_baby_bear` | `abandoned_baby_bear` |
| `Pattern.marubozu_bull` | `marubozu_bull` ⚠ verify exact id |
| `Pattern.marubozu_bear` | `marubozu_bear` ⚠ verify exact id |
| `Pattern.spinning_top` | `spinning_top` |
| `Pattern.star` | `star` ⚠ verify id exists |
| `Pattern.big_candle_bull` | `big_candle_bull` ⚠ verify id exists |
| `Pattern.big_candle_bear` | `big_candle_bear` ⚠ verify id exists |

⚠ Output type discrepancy: individual pattern transforms currently output `Boolean` per metadata.
Phase 3 spec says Integer (-100/0/+100). Resolve before implementing — either the spec needs
updating or the impl nodes need an output type change.

### Compile error

```
candlestick_pattern(o, h, l, c, patterns=[])
→  COMPILE ERROR: patterns list cannot be empty
```

---

## Phase 3 — macro_data `[macro]`

Each positional argument is a `Macro.X` enum value → one `common_indicators` node per indicator.

```
macro_data(Macro.FedFunds)
→  common_indicators(category=FedFunds)()

macro_data(Macro.CPI)
→  common_indicators(category=CPI)()

macro_data(Macro.CPI, Macro.PCE)
→  common_indicators(category=CPI)()
   common_indicators(category=PCE)()

macro_data(Macro.CPI, Macro.PCE, Macro.Unemployment)
→  common_indicators(category=CPI)()
   common_indicators(category=PCE)()
   common_indicators(category=Unemployment)()
```

`MacroEconomicsIndicator` enum values are the option values of `common_indicators`'s `category` option.
The macro enum value names must match exactly.

### Compile error

```
macro_data()
→  COMPILE ERROR: macro_data requires at least one indicator argument
```

---

## Phase 3 — pair_stat `[macro]`

N metrics in list → N impl nodes, all sharing the same (x, y) inputs.

### Single metric cases

```
pair_stat(a, b, metrics=[Metric.correlation], window=60)
→  rolling_corr(window=60, method=pearson)(a, b)

pair_stat(a, b, metrics=[Metric.correlation], window=60, window_type="expanding")
→  rolling_corr(window=60, window_type=expanding, method=pearson)(a, b)

pair_stat(a, b, metrics=[Metric.correlation], window=60, correlation_method="spearman")
→  rolling_corr(window=60, method=spearman)(a, b)

pair_stat(a, b, metrics=[Metric.covariance], window=60)
→  rolling_cov(window=60)(a, b)

pair_stat(a, b, metrics=[Metric.covariance], window=60, window_type="expanding")
→  rolling_cov(window=60, window_type=expanding)(a, b)

pair_stat(a, b, metrics=[Metric.beta], window=252)
→  beta(window=252)(a, b)

pair_stat(a, b, metrics=[Metric.ewm_correlation], window=20)
→  ewm_corr(span=20)(a, b)
   NOTE: pair_stat `window` maps to ewm_corr's `span` option
```

### Multi-metric cases (variadic output)

```
pair_stat(a, b, metrics=[Metric.correlation, Metric.covariance], window=60)
→  rolling_corr(window=60, method=pearson)(a, b)
   rolling_cov(window=60)(a, b)

pair_stat(a, b, metrics=[Metric.correlation, Metric.covariance, Metric.beta], window=60)
→  rolling_corr(window=60, method=pearson)(a, b)
   rolling_cov(window=60)(a, b)
   beta(window=60)(a, b)

pair_stat(a, b, metrics=[Metric.correlation, Metric.ewm_correlation], window=30)
→  rolling_corr(window=30, method=pearson)(a, b)
   ewm_corr(span=30)(a, b)
```

### correlation_method forwarding rule

`correlation_method` only forwards to `rolling_corr` nodes. Ignored for covariance, beta, ewm_corr:

```
pair_stat(a, b, metrics=[Metric.correlation, Metric.covariance], window=60, correlation_method="kendall")
→  rolling_corr(window=60, method=kendall)(a, b)   ← method forwarded
   rolling_cov(window=60)(a, b)                    ← correlation_method ignored
```

### Compile error

```
pair_stat(a, b, metrics=[])
→  COMPILE ERROR: metrics list cannot be empty
```

---

## Phase 3 — volatility `[macro]`

```
volatility(close, method=VolMethod.annualized)
→  volatility(period=14)(close)                     ← default period

volatility(close, method=VolMethod.annualized, period=20)
→  volatility(period=20)(close)

volatility(close, method=VolMethod.annualized, period=20, trading_periods=252)
→  volatility(period=20, trading_periods=252)(close)

volatility(close, method=VolMethod.returns)
→  basic_volatility(type=return_type, period=20)(close)   ← default period

volatility(close, method=VolMethod.returns, period=14)
→  basic_volatility(type=return_type, period=14)(close)

volatility(close, method=VolMethod.price_diff)
→  basic_volatility(type=price_diff, period=20)(close)

volatility(close, method=VolMethod.price_diff, period=14)
→  basic_volatility(type=price_diff, period=14)(close)
```

`volatility_estimator` is NOT affected (OHLC input, different transform entirely).

⚠ Name collision note: the macro is called `volatility` and the annualized impl node is also
called `volatility`. The two-stage form `volatility(period=14)(close)` becomes internalUse=true
(hidden from users). The macro `volatility(close, method=VolMethod.annualized, period=14)` is the
user-facing form.

---

## Phase 3 — select `[macro]`

```
select(momentum, n=5, direction=Direction.Top)
→  cs_select(n=5, direction=Top)(momentum)

select(momentum, n=5, direction=Direction.Bottom)
→  cs_select(n=5, direction=Bottom)(momentum)

select(momentum, n=5, direction=Direction.Top, group_by=GroupBy.sector)
→  cs_select(n=5, direction=Top, group_by=sector)(momentum)

select(momentum, n=5, direction=Direction.Bottom, group_by=GroupBy.industry)
→  cs_select(n=5, direction=Bottom, group_by=industry)(momentum)
```

⚠ Verify cs_select option names: `n`, `direction` (SelectDirection enum), `group_by` — confirm exact
ids and enum values in transform_metadata.json before implementing.

---

## Phase 4 — Cross-sectional scope flag `[meta]` (two-stage routing, not macros)

These remain two-stage registered transforms. The `cross_sectional` flag routes to the cs_* impl node.

### zscore

```
zscore(period=60)(signal)
→  zscore impl node (unchanged)

zscore(cross_sectional=True)(signal)
→  cs_zscore impl node (no group_by)

zscore(cross_sectional=True, group_by=GroupBy.sector)(signal)
→  cs_zscore(group_by=sector) impl node
```

### winsorize

```
winsorize(lower=0.05, upper=0.95, period=60)(signal)
→  winsorize impl node (unchanged)

winsorize(lower=0.05, upper=0.95, cross_sectional=True)(signal)
→  cs_winsorize(lower=0.05, upper=0.95) impl node

winsorize(lower=0.05, upper=0.95, cross_sectional=True, group_by=GroupBy.sector)(signal)
→  cs_winsorize(lower=0.05, upper=0.95, group_by=sector) impl node
```

### rank (new canonical name — cs_rank only, cross_sectional defaults True)

```
rank(cross_sectional=True)(signal)
→  cs_rank() impl node

rank(cross_sectional=True, group_by=GroupBy.sector)(signal)
→  cs_rank(group_by=sector) impl node
```

⚠ Does `rank` exist as a registered transform today, or is this a new registration?
If new, the metadata struct needs to be created (not just modified).

### quantile (new canonical name — from cs_quantile)

```
quantile(q=0.5, cross_sectional=True)(signal)
→  cs_quantile(q=0.5) impl node

quantile(q=0.5, cross_sectional=True, group_by=GroupBy.sector)(signal)
→  cs_quantile(q=0.5, group_by=sector) impl node
```

⚠ Same question — new registration or existing transform rename?

### weighted_mean (new canonical name — from cs_weighted_mean)

```
weighted_mean(cross_sectional=True)(signal, weights)
→  cs_weighted_mean() impl node (signal + weights inputs)

weighted_mean(cross_sectional=True, group_by=GroupBy.sector)(signal, weights)
→  cs_weighted_mean(group_by=sector) impl node
```

⚠ Same question — new registration or existing transform rename?

---

## Complete internalUse=false → true Changeset

Transforms being hidden. They remain as compiler-internal impl nodes; the two-stage
user-facing form produces a COMPILE ERROR pointing to the replacement.

### Phase 1 (2 transforms)

| Transform | Replacement |
|---|---|
| `downsample` | `resample(..., agg=[...])` |
| `upsample` | `resample(..., how=...)` |

### Phase 2 (9 transforms)

| Transform | Replacement |
|---|---|
| `max` | `agg(src, N, Agg.Max)` |
| `min` | `agg(src, N, Agg.Min)` |
| `sum` | `agg(src, N, Agg.Sum)` |
| `stddev` | `agg(src, N, Agg.Std)` |
| `var` | `agg(src, N, Agg.Var)` |
| `cs_agg` | `agg(src, Agg.X, cross_sectional=True)` or `agg(src, Agg.X, group_by=GroupBy.Y)` |
| `valuewhen` (two-stage) | `valuewhen(cond, src, occurrence)` [builtin] |
| `barssince` (two-stage) | `barssince(cond)` [builtin] |
| `mom` | `diff(src, N)` [builtin] |

NOTE: `ma` stays public — it is NOT replaced. `agg(src, N, Agg.Mean)` = SMA only.
Non-SMA types (`ema`, `hma`, `kama`, etc.) require `ma(type=...)(src)` directly.

### Phase 3 (34 transforms)

| Transform | Replacement |
|---|---|
| `event_marker` | `marker(signal, [price,] Event.X)` |
| `doji` | `candlestick_pattern(..., patterns=[Pattern.doji])` |
| `dragonfly_doji` | `candlestick_pattern(..., patterns=[Pattern.dragonfly_doji])` |
| `gravestone_doji` | `candlestick_pattern(..., patterns=[Pattern.gravestone_doji])` |
| `four_price_doji` | `candlestick_pattern(..., patterns=[Pattern.four_price_doji])` |
| `long_legged_doji` | `candlestick_pattern(..., patterns=[Pattern.long_legged_doji])` |
| `hammer` | `candlestick_pattern(..., patterns=[Pattern.hammer])` |
| `inverted_hammer` | `candlestick_pattern(..., patterns=[Pattern.inverted_hammer])` |
| `hanging_man` | `candlestick_pattern(..., patterns=[Pattern.hanging_man])` |
| `shooting_star` | `candlestick_pattern(..., patterns=[Pattern.shooting_star])` |
| `morning_star` | `candlestick_pattern(..., patterns=[Pattern.morning_star])` |
| `evening_star` | `candlestick_pattern(..., patterns=[Pattern.evening_star])` |
| `morning_doji_star` | `candlestick_pattern(..., patterns=[Pattern.morning_doji_star])` |
| `evening_doji_star` | `candlestick_pattern(..., patterns=[Pattern.evening_doji_star])` |
| `engulfing_bull` | `candlestick_pattern(..., patterns=[Pattern.engulfing_bull])` |
| `engulfing_bear` | `candlestick_pattern(..., patterns=[Pattern.engulfing_bear])` |
| `three_white_soldiers` | `candlestick_pattern(..., patterns=[Pattern.three_white_soldiers])` |
| `three_black_crows` | `candlestick_pattern(..., patterns=[Pattern.three_black_crows])` |
| `abandoned_baby_bull` | `candlestick_pattern(..., patterns=[Pattern.abandoned_baby_bull])` |
| `abandoned_baby_bear` | `candlestick_pattern(..., patterns=[Pattern.abandoned_baby_bear])` |
| `marubozu_bull` ⚠ | `candlestick_pattern(..., patterns=[Pattern.marubozu_bull])` |
| `marubozu_bear` ⚠ | `candlestick_pattern(..., patterns=[Pattern.marubozu_bear])` |
| `spinning_top` | `candlestick_pattern(..., patterns=[Pattern.spinning_top])` |
| `star` ⚠ | `candlestick_pattern(..., patterns=[Pattern.star])` |
| `big_candle_bull` ⚠ | `candlestick_pattern(..., patterns=[Pattern.big_candle_bull])` |
| `big_candle_bear` ⚠ | `candlestick_pattern(..., patterns=[Pattern.big_candle_bear])` |
| `common_indicators` | `macro_data(Macro.X, ...)` |
| `rolling_corr` | `pair_stat(..., metrics=[Metric.correlation])` |
| `rolling_cov` | `pair_stat(..., metrics=[Metric.covariance])` |
| `beta` | `pair_stat(..., metrics=[Metric.beta])` |
| `ewm_corr` | `pair_stat(..., metrics=[Metric.ewm_correlation])` |
| `basic_volatility` | `volatility(..., method=VolMethod.returns/price_diff)` |
| `volatility` (two-stage) | `volatility(..., method=VolMethod.annualized)` [macro] |
| `cs_select` | `select(src, n=N, direction=Direction.X)` |

### Phase 4 (5 transforms)

| Transform | Replacement |
|---|---|
| `cs_zscore` | `zscore(cross_sectional=True)` |
| `cs_winsorize` | `winsorize(cross_sectional=True)` |
| `cs_rank` | `rank(cross_sectional=True)` |
| `cs_quantile` | `quantile(q=..., cross_sectional=True)` |
| `cs_weighted_mean` | `weighted_mean(cross_sectional=True)` |

---

## Total changeset summary

| Phase | New constructs | Transforms → internalUse=true |
|---|---|---|
| 1 | `resample` | 2 |
| 2 | `agg`, `diff`, `returns`, `cum`, `linreg`, `lag`, `prev`, `ratio`, `normalize`, `drawdown`, `to_int`, `relu`, `between`, `isna`, `notna`, `valuewhen`, `barssince`, `nz`, `clamp`, `sign` | 9 |
| 3 | `marker`, `candlestick_pattern`, `macro_data`, `pair_stat`, `volatility`, `select` | 34 |
| 4 | *(metadata only — no new constructs)* | 5 |
| **Total** | **27 new constructs** | **50 transforms hidden** |

---

## Open questions to resolve before implementation

1. **resample default agg** — what agg type is used when `agg=` is not specified in a downsample case?
2. **resample default agg for mixed-direction** — what agg type is used for the downsample elements when `agg=` is not specified in a mixed-direction option-driven call?
3. **candlestick output type** — individual patterns currently output `Boolean` per metadata; Phase 3 spec says Integer (-100/0/+100). Which is correct?
4. **marubozu/star/big_candle ids** — verify exact transform ids for `marubozu_bull`, `marubozu_bear`, `star`, `big_candle_bull`, `big_candle_bear`.
5. **cs_select option names** — verify exact option ids and Direction enum values in cs_select metadata.
6. **rank/quantile/weighted_mean** — are these new metadata registrations or renames of existing transforms?
7. **ewm_corr window→span mapping** — confirm `pair_stat(window=N)` maps to `ewm_corr(span=N)` correctly.
8. **Icon enum values** — verify `Icon.RepeatIcon`, `Icon.ShieldIcon`, `Icon.TargetIcon`, `Icon.BellIcon`, `Icon.RefreshIcon` exist in registered Icon enum.
