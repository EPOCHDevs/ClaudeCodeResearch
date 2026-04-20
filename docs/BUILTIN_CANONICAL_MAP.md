# Builtin Canonical Map

Takes the raw inventory and organizes into:
- Enum-gated builtins (multiple related operations under one name)
- Standalone builtins (single formula, no enum needed)

Every entry must point to an existing impl node OR be a one-liner arithmetic composite.

---

## Enum-gated builtins

### `returns(src, N=1, type=ReturnType.X)` — financial return family

All "how did src change proportionally relative to N bars ago" questions live here.

| `ReturnType` | Formula | Lowers to |
|---|---|---|
| `Simple` *(default)* | `(src - src[N]) / src[N]` | arithmetic — `(src - lag(src,N)) / lag(src,N)` |
| `Log` | `ln(src / src[N])` | arithmetic — `ln(src / lag(src,N))` using `ln` builtin |

```python
daily_ret    = returns(close)                          # simple 1-bar return
weekly_ret   = returns(close, 5)                       # simple 5-bar return
log_ret      = returns(close, type=ReturnType.Log)     # log return
weekly_log   = returns(close, 5, type=ReturnType.Log)
```

Natural names covered: `pct_change`, `simple_return`, `ret`, `returns`, `log_return`, `log_ret`

NOTE: `roc` (registered transform) = `(src - src[N]) / src[N] * 100` — the × 100 form.
`returns(Simple)` = unpacked form without × 100. `roc` stays as registered transform.

---

### `cum(src, Agg.X)` — expanding/cumulative series

All "expanding window from data start" operations under one name.
Reuses the existing `AggregationType` enum — no new enum needed.

| `Agg.X` | Formula | Lowers to |
|---|---|---|
| `Agg.Sum` *(default)* | running total from bar 0 | expanding sum impl ⚠ verify |
| `Agg.Product` | running product from bar 0 | expanding product impl ⚠ verify |
| `Agg.Max` | running maximum from bar 0 | expanding max impl ⚠ verify |
| `Agg.Min` | running minimum from bar 0 | expanding min impl ⚠ verify |

```python
equity_curve  = cum(1 + returns(close), Agg.Product)   # cumulative growth
total_volume  = cum(volume)                             # Agg.Sum (default)
all_time_high = cum(close, Agg.Max)
all_time_low  = cum(close, Agg.Min)
```

Natural names covered: `cumsum`, `cumprod`, `cummax`, `cummin`, `running_max`, `running_min`

No new enum registration — `AggregationType` is already registered alongside `agg`.

⚠ All 4 need expanding window impl nodes verified. If only some exist, support those first
and COMPILE ERROR the rest with "not yet supported".

---

### `linreg(src, N, type=LinRegType.X)` — linear regression outputs

All outputs of a linear regression over N bars under one name.

| `LinRegType` | Meaning | Lowers to |
|---|---|---|
| `Value` *(default)* | regression line value at current bar | `linearreg(period=N)` impl ⚠ verify |
| `Slope` | slope of regression line | `linearreg_slope(period=N)` impl ⚠ verify |
| `Intercept` | y-intercept of regression line | `linearreg_intercept(period=N)` impl ⚠ verify |
| `Forecast` | 1-bar-ahead projection | `tsf(period=N)` impl ⚠ verify |

```python
trend_value  = linreg(close, 20)
slope        = linreg(close, 20, type=LinRegType.Slope)
forecast     = linreg(close, 20, type=LinRegType.Forecast)
```

Natural names covered: `linreg`, `tsf`, `linear_regression`, `trendline`

⚠ All 4 need impl node ids verified in transform_metadata.json before implementing.

---

## Standalone builtins (one name, one formula)

### `diff(src, N=1)` — absolute difference

```
diff(src)     → mom(period=1)(src)    ← lowers to existing mom impl
diff(src, N)  → mom(period=N)(src)
```

Natural names covered: `diff`, `change`, `mom` (as builtin name), `delta`

`mom` registered transform → `internalUse=true` after this ships (becomes the impl node).

---

### `lag(src, N=1)` — lag / shift

```
lag(src, 1)   → LagOp(src, 1)    ← compiler emits lag AST node directly
lag(src, N)   → LagOp(src, N)
```

Natural names covered: `lag`, `shift`, `delay`

---

### `prev(src)` — previous bar value (readability alias for lag(src, 1))

```
prev(src)     → lag(src, 1)    ← grammar rewrite, no new node
```

Natural names covered: `prev`, `prior`, `last_value`
Useful in context: `entry_price = valuewhen(signal, prev(close))`

---

### `ratio(src, N=1)` — price ratio to N bars ago

```
ratio(src)    → src / lag(src, 1)    ← arithmetic
ratio(src, N) → src / lag(src, N)
```

Natural names covered: `ratio`, `rocr`, `rel`, `relative`

---

### `normalize(src, N)` — min-max scale to [0, 1]

```
normalize(src, N)
→ (src - agg(src, N, Agg.Min)) / (agg(src, N, Agg.Max) - agg(src, N, Agg.Min))
```

Arithmetic composite using `agg`. No impl node needed.

Natural names covered: `normalize`, `minmax`, `minmax_scale`, `scale`

⚠ Division by zero when max == min (flat series). Compiler should emit:
`nz((src - min) / (max - min), 0)` — wrapping in `nz` guards the flat case.

---

### `drawdown(src, N)` — current drawdown from rolling high

```
drawdown(src, N)
→ (src - agg(src, N, Agg.Max)) / agg(src, N, Agg.Max)
```

Arithmetic composite using `agg`. Result is negative or zero (0 = at the high).

Natural names covered: `drawdown`, `underwater`, `dd`

---

### `to_int(cond)` — Boolean → 0/1 integer

```
to_int(cond)  → where(cond, 1, 0)    ← uses existing `where` builtin
```

Natural names covered: `to_int`, `indicator`, `bool_to_int`, `as_int`

---

### `relu(src)` — zero-floor (ReLU activation)

```
relu(src)     → where(src > 0, src, 0)    ← arithmetic
```

Natural names covered: `relu`, `positive`, `clip_zero`, `hinge`

---

### `between(src, lo, hi)` — range membership

```
between(src, lo, hi)  → (src >= lo) and (src <= hi)    ← arithmetic/logical
```

Returns Boolean. Matches pandas `.between(lo, hi)`.

Natural names covered: `between`, `in_range`, `within`

---

### `isna(src)` — null check (alias for `is_null`)

```
isna(src)   → is_null(src)    ← grammar alias, `is_null` already exists in BUILTIN_FUNCTIONS
```

Natural names covered: `isna`, `isnull`, `na`, `is_null`

---

### `notna(src)` — non-null check (alias for `is_valid`)

```
notna(src)  → is_valid(src)   ← grammar alias, `is_valid` already exists in BUILTIN_FUNCTIONS
```

Natural names covered: `notna`, `notnull`, `is_valid`

---

## What stays as registered transforms (NOT promoted)

These are NOT builtins — they are registered two-stage transforms and stay that way.

| Transform | Reason not promoted |
|---|---|
| `roc` | Percentage × 100 form — confusing as builtin; agents can use `returns(Simple) * 100` |
| `zscore` | Options-heavy (window_type, method) — stays as two-stage registered transform |
| `winsorize` | Options-heavy — stays as two-stage |
| `ma` (ema, hma, etc.) | Options-heavy — stays as two-stage |
| `volatility` / `basic_volatility` | Absorbed by `volatility` macro (Phase 3) |
| `rolling_corr`, `rolling_cov`, `beta`, `ewm_corr` | Absorbed by `pair_stat` macro (Phase 3) |

---

## Complete Phase 2 builtin list (updated)

### Added to `BUILTIN_FUNCTIONS`

```cpp
// Existing (already in BUILTIN_FUNCTIONS — no change):
// abs, ceil, floor, round, sqrt, exp, ln, log10, sin, cos, tan, ...
// coalesce, where, is_null, is_valid, crossover, crossunder, crossany, ffill, ffill_day

// Phase 2 additions:
"agg",          // enum-gated rolling + cs aggregation
"returns",      // ReturnType.Simple | Log
"cum",          // Agg.Sum | Product | Max | Min  (reuses AggregationType — no new enum)
"linreg",       // LinRegType.Value | Slope | Intercept | Forecast  ⚠ impl verification required
"diff",         // absolute difference → mom impl
"lag",          // lag operator → LagOp
"prev",         // alias → lag(src, 1)
"ratio",        // src / src[N] → arithmetic
"normalize",    // min-max → arithmetic (agg composite)
"drawdown",     // drawdown → arithmetic (agg composite)
"to_int",       // Boolean → 0/1 → where arithmetic
"relu",         // zero-floor → where arithmetic
"between",      // range check → logical arithmetic
"isna",         // → is_null alias
"notna",        // → is_valid alias
"valuewhen",    // existing impl, single-stage promotion
"barssince",    // existing impl, single-stage promotion
"nz",           // → coalesce grammar rewrite
"clamp",        // → arithmetic
"sign",         // → arithmetic
```

### New enums to register

```cpp
RegisterEnumType("ReturnType", {"Simple", "Log"});
RegisterEnumType("LinRegType", {"Value", "Slope", "Intercept", "Forecast"});
// CumType NOT needed — cum reuses existing AggregationType (Agg.Sum/Product/Max/Min)
```

Both small (≤ 4 values) → auto-inline in grammar.

---

## Transforms → internalUse=true after Phase 2

| Transform | Replaced by |
|---|---|
| `mom` | `diff(src, N)` builtin |
| `max` (rolling) | `agg(src, N, Agg.Max)` |
| `min` (rolling) | `agg(src, N, Agg.Min)` |
| `sum` (rolling) | `agg(src, N, Agg.Sum)` |
| `stddev` | `agg(src, N, Agg.Std)` |
| `var` | `agg(src, N, Agg.Var)` |
| `cs_agg` | `agg(src, Agg.X, cross_sectional=True)` |
| `valuewhen` (two-stage) | `valuewhen(cond, src, N)` builtin |
| `barssince` (two-stage) | `barssince(cond)` builtin |
