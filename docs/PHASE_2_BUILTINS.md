# Phase 2 — Builtins Expansion

**Status:** Not started
**Depends on:** Phase 0 complete (including `BuiltinRegistry` + strategy interfaces from 0e)
**Goal:** `agg` unified builtin + time-series primitives. All single-output, single-stage, inputs-first.
**Touches:** `grammar_generator.cpp` (EBNF output), new file: `agg_lowering.h`, registration calls in `InitializeTransforms()`

### Architecture note

All lowering in this phase uses the strategy interfaces from Phase 0e. No code goes in `constructor_parser.cpp`. Each builtin is registered declaratively via `BuiltinRegistry::RegisterBuiltin()`.

- **`agg`** — custom `AggLowering` class (shape-based disambiguation)
- **`valuewhen`, `barssince`, `diff`** — `AliasLowering` strategy
- **`nz`, `clamp`, `sign`, `to_int`, `relu`, `between`** — `ArithmeticLowering` strategy
- **`returns`, `ratio`, `normalize`, `drawdown`** — `ArithmeticLowering` strategy
- **`lag`** — custom lowering (emits LagOp AST node directly)
- **`prev`** — `AliasLowering("lag", "period", 1)`
- **`cum`, `linreg`** — `EnumGatedLowering` (enum selects impl node)
- **`isna`, `notna`** — `AliasLowering("is_null")`, `AliasLowering("is_valid")`

---

## 2a — `agg` unified aggregation builtin

### Why `agg` over named variants

Separate named builtins (`highest`, `lowest`, `sum`, `stdev`, `mean`) invite hallucination:
agents invent `rolling_max`, `windowed_std`, `rolling_average`. A single name with an enum
gate means the compiler validates the aggregation type — the agent only has to know `Agg`.

Same pattern as the existing `cs_agg` transform which agents already understand. `agg`
unifies rolling and cross-sectional under one name — argument shape determines which.

### Three forms, one name

| Form | Axis | Lowers to |
|---|---|---|
| `agg(src, N, Agg.X)` | Rolling over N bars | `max`/`min`/`sum`/`stddev`/`var` impl node with `period=N` |
| `agg(src, Agg.X, cross_sectional=True)` | Cross-sectional (all assets at t) | `cs_agg(type=X)` impl node |
| `agg(src, Agg.X, group_by=GroupBy.Y)` | Cross-sectional grouped (`group_by` implies cs) | `cs_agg(type=X, group_by=Y)` impl node |

**Compile-time disambiguation:**
- Second arg is `Int`, third is `AggType` → rolling
- Second arg is `AggType` + `cross_sectional=True` kwarg → cross-sectional
- Second arg is `AggType` + `group_by=GroupBy.X` kwarg → cross-sectional grouped (`group_by` implies cs; no need to also write `cross_sectional=True`)
- Second arg is `AggType` with **no explicit kwarg** → COMPILE ERROR: "missing period for rolling form, or specify cross_sectional=True"

**Why the explicit kwarg is required:** `agg(src, Agg.Mean)` with a forgotten period must not
silently become cross-sectional. Rolling and cross-sectional produce completely different results.
Making `agg(src, Agg.X)` a COMPILE ERROR means the agent gets a clear diagnostic instead of a
wrong answer that passes silently.

### `AggregationType` enum → impl node map (rolling axis)

| Agg.X | Lowers to impl node | Notes |
|---|---|---|
| `Agg.Max` | `max(period=N)` | |
| `Agg.Min` | `min(period=N)` | |
| `Agg.Sum` | `sum(period=N)` | |
| `Agg.Std` | `stddev(period=N)` | |
| `Agg.Var` | `var(period=N)` | |
| `Agg.Mean` | `ma(type=sma, period=N)` | SMA = rolling mean |
| `Agg.Median` | `rolling_median(period=N)` | must exist or add thin impl |
| `Agg.Count` | `rolling_count(period=N)` | count non-null |
| `Agg.First` | `rolling_first(period=N)` | |
| `Agg.Last` | `rolling_last(period=N)` | |
| `Agg.Skew` | `rolling_skew(period=N)` | |
| `Agg.Kurtosis` | `rolling_kurtosis(period=N)` | |
| `Agg.Product` | `rolling_product(period=N)` | |
| `Agg.Quantile` | requires `q=` param → **not valid in rolling form without q** | COMPILE ERROR if used without q |
| `Agg.Mode` | `rolling_mode(period=N)` | |
| `Agg.Any` | `rolling_any(period=N)` | Boolean input expected |
| `Agg.All` | `rolling_all(period=N)` | Boolean input expected |

**Open question:** Some of these impl nodes may not exist yet (rolling_median, rolling_skew, etc.). For Phase 2, implement the common set and emit COMPILE ERROR with "not yet supported" for the rest. Expand later.

**Priority subset for Phase 2:** `Max`, `Min`, `Sum`, `Std`, `Var`, `Mean` — these are the 5 old transforms being retired.

### EBNF

```ebnf
agg_builtin ::=
    "agg" "(" series_expr "," integer "," agg_type ")"                                        (* rolling *)
  | "agg" "(" series_expr "," agg_type "," "cross_sectional" "=" "True" ")"                  (* cs plain *)
  | "agg" "(" series_expr "," agg_type "," "group_by" "=" grouping_mode ")"                  (* cs grouped *)
  | "agg" "(" series_expr "," agg_type "," "cross_sectional" "=" "True"
                                          "," "group_by" "=" grouping_mode ")"               (* cs grouped explicit *)

(* agg(src, Agg.X) with no kwarg → COMPILE ERROR *)

agg_type     ::= "Agg" "." agg_value
agg_value    ::= "Mean" | "Sum" | "Min" | "Max" | "Median" | "Std" | "Var"
               | "Skew" | "Kurtosis" | "Count" | "First" | "Last"
               | "Product" | "Quantile" | "Mode" | "Any" | "All"

grouping_mode ::= "GroupBy" "." grouping_value
grouping_value ::= "none" | "sector" | "industry" | "category"
                 | "asset_class" | "exchange" | "auto_detect"
                 | "base_currency" | "quote_currency"
```

### `constructor_parser.cpp` lowering

```cpp
if (name == "agg" && IsMember(BUILTIN_FUNCTIONS, name)) {
    auto args    = parse_positional_args(call);
    auto kwargs  = parse_kwargs(call);

    auto src = expect_series(args[0]);

    if (args.size() == 3 && is_integer(args[1])) {
        // Rolling: agg(src, N, Agg.X)
        auto n    = expect_integer(args[1]);
        auto agg  = expect_enum(args[2], "AggregationType");
        auto impl = AggTypeToRollingImpl(agg);   // "Agg.Max" → "max"
        emit_node(impl, {{"period", n}}, {src});

    } else if (args.size() == 2 && is_enum(args[1], "AggregationType")) {
        // Second arg is AggType — must have explicit cs kwarg or error
        auto agg         = expect_enum(args[1], "AggregationType");
        bool has_cs      = has_kwarg(kwargs, "cross_sectional");
        bool has_groupby = has_kwarg(kwargs, "group_by");

        if (!has_cs && !has_groupby) {
            compile_error(
                "agg(" + agg + ") — missing period for rolling form, "
                "or specify cross_sectional=True for cross-sectional. "
                "Did you forget the period? e.g. agg(src, 20, " + agg + ")"
            );
        }

        auto groupby = has_groupby
            ? get_optional_kwarg(kwargs, "group_by")
            : std::nullopt;

        if (groupby) {
            emit_node("cs_agg", {{"type", agg}, {"group_by", *groupby}}, {src});
        } else {
            emit_node("cs_agg", {{"type", agg}}, {src});
        }

    } else {
        compile_error("agg() requires agg(src, N, Agg.X) or agg(src, Agg.X, cross_sectional=True)");
    }
}
```

### grammar_generator.cpp change

```cpp
// Add to BUILTIN_FUNCTIONS:
"agg",
```

### Deprecations

Mark `internalUse=true` in metadata after migration window:
- `max`, `min`, `sum`, `stddev`, `var` (old rolling two-stage forms)
- `cs_agg` (old cross-sectional two-stage form)

These continue to work during migration but are hidden from docs and search results.

### Grammar addition (`GenerateEBNF()` BUILTIN FUNCTIONS section)

This block is added to the Tier B (Aggregation) section of the generated grammar:

```
# ── agg — unified aggregation ───────────────────────────────────────────────
# agg(source, N, Agg.X)                          — rolling over N bars (N required)
# agg(source, Agg.X, cross_sectional=True)        — cross-sectional across all assets
# agg(source, Agg.X, group_by=GroupBy.Y)          — cross-sectional grouped
#
#   agg(close, 52, Agg.Max)                              — rolling max, 52 bars
#   agg(returns, 20, Agg.Std)                            — rolling std dev
#   agg(close, 20, Agg.Mean)                             — 20-bar SMA
#   agg(momentum, Agg.Mean, cross_sectional=True)        — cross-sectional mean
#   agg(momentum, Agg.Mean, group_by=GroupBy.sector)     — sector-grouped mean
#
# agg(src, Agg.X) with no kwarg → COMPILE ERROR (forgot period, or missing cross_sectional=True)
#
# @AggregationType: Mean Sum Min Max Median Std Var
#                   Skew Kurtosis Count First Last Product Mode Any All
# @GroupBy: none sector industry category asset_class exchange auto_detect
#           base_currency quote_currency
#
# Deprecates: max() min() sum() stddev() var() cs_agg()
```

### Skill: `S_agg_enum_gate.md`

```markdown
# S_agg_enum_gate — agg() shape disambiguation

RULE: Rolling requires an explicit period (N). Cross-sectional requires cross_sectional=True or group_by=.
      agg(src, Agg.X) with NO kwarg is a COMPILE ERROR — it does NOT default to either form.

ROLLING (period N required, always 3 positional args):
  agg(close, 52, Agg.Max)      — rolling max over 52 bars
  agg(returns, 20, Agg.Std)    — rolling standard deviation
  agg(close, 20, Agg.Mean)     — simple moving average (same as ma(type=sma, period=20))
  agg(returns, 20, Agg.Sum)    — rolling sum

CROSS-SECTIONAL (cross_sectional=True or group_by= required):
  agg(momentum, Agg.Mean, cross_sectional=True)           — mean across all assets at each bar
  agg(momentum, Agg.Mean, group_by=GroupBy.sector)        — mean within each sector group
  agg(momentum, Agg.Std, cross_sectional=True)            — std dev across all assets

COMPILE ERRORS:
  agg(close, Agg.Max)                         — COMPILE ERROR: forgot period? use agg(close, N, Agg.Max)
  agg(returns, Agg.Std)                       — COMPILE ERROR: forgot period? use agg(returns, N, Agg.Std)
  agg(close, 52, Agg.Max, group_by=...)       — COMPILE ERROR: rolling + group_by is ambiguous

DO NOT:
  rolling_max(close, 52)                      — doesn't exist
  max(period=52)(close)                       — old form, internalUse only
  cs_agg(type=Agg.Mean)(momentum)             — old form, internalUse only
```

### Test cases

```cpp
TEST_CASE("agg rolling max") { /* agg(close, 52, Agg.Max) → max(period=52)(close) */ }
TEST_CASE("agg rolling std") { /* agg(returns, 20, Agg.Std) → stddev(period=20)(returns) */ }
TEST_CASE("agg rolling mean") { /* agg(close, 20, Agg.Mean) → ma(type=sma, period=20)(close) */ }
TEST_CASE("agg cross-sectional no group") { /* agg(sig, Agg.Mean, cross_sectional=True) → cs_agg(type=Mean)(sig) */ }
TEST_CASE("agg cross-sectional grouped via group_by") { /* agg(sig, Agg.Mean, group_by=GroupBy.sector) → cs_agg(type=Mean, group_by=sector)(sig) */ }
TEST_CASE("agg compile error no kwarg") { /* agg(sig, Agg.Mean) → COMPILE ERROR: missing period or cross_sectional=True */ }
TEST_CASE("agg compile error rolling+groupby") { /* agg(src, 20, Agg.Max, group_by=GroupBy.sector) → COMPILE ERROR */ }
TEST_CASE("agg compile error wrong arg count") { /* agg(src) → COMPILE ERROR */ }
TEST_CASE("agg compile error unknown enum value") { /* agg(src, 20, Agg.RollingMax) → COMPILE ERROR */ }
```

### Acceptance criteria

- [ ] `"agg"` in `BUILTIN_FUNCTIONS`
- [ ] All 8 test cases pass
- [ ] `agg(close, 52, Agg.Max)` produces identical output to `max(period=52)(close)`
- [ ] `agg(sig, Agg.Mean, GroupBy.sector)` produces identical output to `cs_agg(type=Mean, group_by=sector)(sig)`
- [ ] `max`, `min`, `sum`, `stddev`, `var`, `cs_agg` marked `internalUse=true`
- [ ] Grammar Tier B section updated with `agg` production rule, enum values, and examples
- [ ] `S_agg_enum_gate.md` skill complete

---

## 2b — Time-series and utility primitives

### `valuewhen`

Already has an impl node (`ControlFlow` category, `occurrence` option). Builtin form is single-stage inputs-first.

**Lowering:**
```
valuewhen(cond, src)       → valuewhen(occurrence=0)(cond, src)
valuewhen(cond, src, N)    → valuewhen(occurrence=N)(cond, src)
```

**Pitfall prevented:** Agents currently call `valuewhen(occurrence=0)(signal, close)` but get the input order wrong or forget to specify `occurrence`. Single-stage form makes order unambiguous.

**Grammar line (Tier C — Time-series primitives):**
```
# valuewhen(condition: Boolean, source: Decimal, occurrence: Int = 0) → Decimal
#   entry_price = valuewhen(long_signal, close)       — close at most recent signal bar
#   prev_price  = valuewhen(long_signal, close, 1)    — close at second most recent
```

---

### `barssince`

Already has an impl node (`ControlFlow` category, no options). Trivial single-stage promotion.

**Lowering:**
```
barssince(cond)   → barssince()(cond)
```

**Grammar line (Tier C — Time-series primitives):**
```
# barssince(condition: Boolean) → Int
#   freshness  = barssince(long_signal)          — bars since signal fired
#   is_fresh   = barssince(long_signal) < 5      — still within 5-bar window
#   NOTE: returns null if condition has never been True; guard with nz() if needed
```

---

### `diff`

`diff` is the canonical builtin name (numpy/pandas `diff`, most universal). Lowers to the
existing `mom` impl node — no new impl node needed. `mom` registered transform → `internalUse=true`.

`diff(src, N)` = `src - src[N]` (absolute difference). Distinct from `roc` which is
`(src - src[N]) / src[N] * 100` — `roc` stays as registered transform (the ×100 form).

**Lowering:**
```
diff(src)      → mom(period=1)(src)    ← default period=1 for "1-bar absolute change"
diff(src, N)   → mom(period=N)(src)
```

**Grammar line (Tier C — Time-series primitives):**
```
# diff(source: Decimal, N: Int = 1) → Decimal    — absolute difference vs N bars ago
#   daily_chg  = diff(close)     — close - close[1]
#   weekly_chg = diff(close, 5)  — close - close[5]
#   NOTE: for percentage change use roc(period=N)(src) or returns(close, N) builtin
# Natural names: diff, change, mom, delta
```

---

### `nz`

Grammar-level rewrite. At compile time `nz(src, fallback)` emits a `coalesce(src, fallback)`
call — no new impl node. `coalesce` is already a builtin (variadic, returns first non-null from
N args, no default). `nz` adds the `replacement=0` default and gives the null-guard pattern a
canonical name that the S02 skill and grammar doc reference directly.

**Lowering:**
```
nz(src)           → coalesce(src, 0.0)    ← default replacement=0
nz(src, fallback) → coalesce(src, fallback)
```

Both lower to the same `coalesce` impl. `nz` does not appear in the compiled node graph.

**Relationship to coalesce:**
- `coalesce(a, b, c)` — variadic; general "first non-null" pattern; no default
- `nz(src)` — 2-arg shorthand; null-guard idiom; default 0; always emits `coalesce(src, 0)`

**Pitfall prevented (S02):** Agents currently write `where(is_null(x), 0, x)` by hand or omit NaN guards entirely. `nz` is the canonical form.

**Grammar line (Tier A — Math & Logic):**
```
# nz(source: Decimal, replacement: Decimal = 0) → Decimal
#   clean_eps = nz(eps_surprise, 0)   — replace null earnings with 0
#   safe_div  = nz(a / b, 1)          — guard division result
```

---

### `clamp`

**Lowering** (arithmetic or thin impl):
```
clamp(src, lo, hi)  → min(max(src, lo), hi)
```
Can be emitted as nested `coalesce`-style arithmetic or as a thin impl node if it doesn't exist.

**Grammar line (Tier A — Math & Logic):**
```
# clamp(source: Decimal, lo: Decimal, hi: Decimal) → Decimal
#   bounded = clamp(zscore, -3, 3)   — clip z-scores to ±3σ
```

---

### `sign`

**Lowering:**
```
sign(src)  → where(src > 0, 1, where(src < 0, -1, 0))
```
Or thin impl node if `sign` already exists.

**Grammar line (Tier A — Math & Logic):**
```
# sign(source: Decimal) → Int       — 1 if positive, -1 if negative, 0 if zero
#   direction = sign(momentum)
```

---

## 2c — Financial / quantitative builtins

### `returns`

**Lowering (arithmetic):**
```
returns(src)                           → (src - lag(src,1)) / lag(src,1)
returns(src, N)                        → (src - lag(src,N)) / lag(src,N)
returns(src, type=ReturnType.Log)      → ln(src / lag(src,1))
returns(src, N, type=ReturnType.Log)   → ln(src / lag(src,N))
```

New enum: `ReturnType` (Simple, Log). `ReturnType.Simple` is the default.

NOTE: `roc` = `returns(Simple) * 100` (×100 form). `roc` stays as registered transform.

**Grammar line (Tier C — Time-series primitives):**
```
# returns(source: Decimal, N: Int = 1, type: ReturnType = ReturnType.Simple) → Decimal
#   daily_ret  = returns(close)                       — simple 1-bar return
#   weekly_ret = returns(close, 5)                    — simple 5-bar return
#   log_ret    = returns(close, type=ReturnType.Log)  — log return
# @ReturnType: Simple Log
# Natural names: pct_change, simple_return, ret, log_return, log_ret
```

---

### `cum`

Expanding (cumulative from bar 0) operations. Reuses `AggregationType` — no new enum.

**Lowering:**
```
cum(src)               → expanding_sum()(src)       ← Agg.Sum default ⚠ verify impl node id
cum(src, Agg.Sum)      → expanding_sum()(src)       ⚠ verify
cum(src, Agg.Product)  → expanding_product()(src)   ⚠ verify
cum(src, Agg.Max)      → expanding_max()(src)       ⚠ verify
cum(src, Agg.Min)      → expanding_min()(src)       ⚠ verify
```

⚠ All 4 impl node ids need verification before implementing. COMPILE ERROR "not yet supported" for any missing impl.

**Grammar line (Tier C — Time-series primitives):**
```
# cum(source: Decimal, agg: AggregationType = Agg.Sum) → Decimal
#   equity_curve  = cum(1 + returns(close), Agg.Product)  — cumulative growth
#   total_volume  = cum(volume)                            — running total (Agg.Sum default)
#   all_time_high = cum(close, Agg.Max)
# Natural names: cumsum, cumprod, cummax, cummin, running_max, running_min
```

---

### `linreg`

All outputs of a linear regression over N bars under one name.

**Lowering:**
```
linreg(src, N)                              → linearreg(period=N)(src)           ⚠ verify
linreg(src, N, type=LinRegType.Slope)       → linearreg_slope(period=N)(src)     ⚠ verify
linreg(src, N, type=LinRegType.Intercept)   → linearreg_intercept(period=N)(src) ⚠ verify
linreg(src, N, type=LinRegType.Forecast)    → tsf(period=N)(src)                 ⚠ verify
```

New enum: `LinRegType` (Value, Slope, Intercept, Forecast). `LinRegType.Value` is the default.

⚠ All 4 impl node ids need verification in transform_metadata.json before implementing.

**Grammar line (Tier C — Time-series primitives):**
```
# linreg(source: Decimal, length: Int, type: LinRegType = LinRegType.Value) → Decimal
#   trend_line = linreg(close, 20)
#   slope      = linreg(close, 20, type=LinRegType.Slope)
#   forecast   = linreg(close, 20, type=LinRegType.Forecast)  — 1-bar ahead (TSF)
# @LinRegType: Value Slope Intercept Forecast
# Natural names: linreg, tsf, linear_regression, trendline
```

---

### `lag`

Compiler emits a lag AST node directly — no impl node lookup needed.

**Lowering:**
```
lag(src, 1) → LagOp(src, 1)
lag(src, N) → LagOp(src, N)
```

**Grammar line (Tier C — Time-series primitives):**
```
# lag(source: Decimal, N: Int = 1) → Decimal    — value from N bars ago
#   prev_close = lag(close)    — same as close[1]
#   lag_5      = lag(close, 5)
# Natural names: lag, shift, delay
```

---

### `prev`

Grammar-level rewrite to `lag(src, 1)`. Readability alias for signal contexts.

**Lowering:**
```
prev(src) → lag(src, 1)
```

**Grammar line (Tier C — Time-series primitives):**
```
# prev(source: Decimal) → Decimal    — previous bar value; alias for lag(src, 1)
#   prev_close = prev(close)
#   entry_px   = valuewhen(signal, prev(close))   — close at bar before signal
# Natural names: prev, prior, last_value
```

---

### `ratio`

**Lowering (arithmetic):**
```
ratio(src)    → src / lag(src, 1)
ratio(src, N) → src / lag(src, N)
```

**Grammar line (Tier C — Time-series primitives):**
```
# ratio(source: Decimal, N: Int = 1) → Decimal    — src / src[N], price ratio to N bars ago
#   price_ratio = ratio(close)     — close / close[1]   (= 1 + returns(close, Simple))
# Natural names: ratio, rocr, rel, relative
```

---

## 2d — Arithmetic composite builtins

### `normalize`

**Lowering (arithmetic composite using `agg`):**
```
normalize(src, N)
→ nz((src - agg(src, N, Agg.Min)) / (agg(src, N, Agg.Max) - agg(src, N, Agg.Min)), 0)
```

Wrapped in `nz(..., 0)` to guard division-by-zero when max == min (flat series).

**Grammar line (Tier C — Time-series primitives):**
```
# normalize(source: Decimal, length: Int) → Decimal    — min-max scale to [0, 1]
#   score = normalize(rsi_val, 252)      — 1-year normalized RSI
#   NOTE: returns 0 when max == min (flat window) — guarded with nz internally
# Natural names: normalize, minmax, minmax_scale, scale
```

---

### `drawdown`

**Lowering (arithmetic composite using `agg`):**
```
drawdown(src, N)
→ (src - agg(src, N, Agg.Max)) / agg(src, N, Agg.Max)
```

Result is ≤ 0 (zero = at the rolling high).

**Grammar line (Tier C — Time-series primitives):**
```
# drawdown(source: Decimal, length: Int) → Decimal    — current drawdown from rolling N-bar high
#   dd = drawdown(close, 252)   — drawdown from 52-week high; result is 0 or negative
# Natural names: drawdown, underwater, dd
```

---

## 2e — Type / logic builtins

### `to_int`

**Lowering:**
```
to_int(cond) → where(cond, 1, 0)
```

**Grammar line (Tier A — Math & Logic):**
```
# to_int(condition: Boolean) → Int    — Boolean to 0/1 integer
#   signal_int = to_int(long_signal)
# Natural names: to_int, indicator, bool_to_int, as_int
```

---

### `relu`

**Lowering:**
```
relu(src) → where(src > 0, src, 0)
```

**Grammar line (Tier A — Math & Logic):**
```
# relu(source: Decimal) → Decimal    — zero-floor (positive-only clip)
#   upside = relu(returns(close))    — keep only positive returns
# Natural names: relu, positive, clip_zero, hinge
```

---

### `between`

**Lowering (logical arithmetic):**
```
between(src, lo, hi) → (src >= lo) and (src <= hi)
```

Returns Boolean. Mirrors pandas `.between(lo, hi)`.

**Grammar line (Tier A — Math & Logic):**
```
# between(source: Decimal, lo: Decimal, hi: Decimal) → Boolean
#   in_zone = between(rsi, 40, 60)   — RSI in neutral zone
# Natural names: between, in_range, within
```

---

### `isna`

Grammar alias for `is_null` — compiles to identical node, zero runtime overhead.

**Lowering:**
```
isna(src) → is_null(src)
```

**Grammar line (Tier A — Math & Logic):**
```
# isna(source: Decimal) → Boolean    — alias for is_null(src); is the value null?
# Natural names: isna, isnull, na, is_null
```

---

### `notna`

Grammar alias for `is_valid` — compiles to identical node.

**Lowering:**
```
notna(src) → is_valid(src)
```

**Grammar line (Tier A — Math & Logic):**
```
# notna(source: Decimal) → Boolean    — alias for is_valid(src); is the value non-null?
# Natural names: notna, notnull, is_valid
```

---

### Skill: `S_valuewhen_barssince.md`

```markdown
# S_valuewhen_barssince — Signal timing primitives

valuewhen(condition, source, occurrence=0):
  Returns value of source at the bar where condition was most recently True.
  occurrence=0: most recent True bar
  occurrence=1: second most recent True bar

  CORRECT: entry_price = valuewhen(long_signal, close)
           — captures close at the bar the signal fired

  WRONG:   entry_price = close  (current close, not entry bar close)
           entry_price = valuewhen(long_signal, close, occurrence=-1)  (invalid)

barssince(condition):
  Returns integer count of bars since condition was last True.
  Returns null if condition has never been True (guard with nz if needed).

  CORRECT: freshness = barssince(long_signal)
           is_fresh  = barssince(long_signal) < 5

  PATTERN: Signal age filter
    recent_signal = long_signal and barssince(long_signal) < 3
```

### Skill: `S_nz_nan_guard.md`

```markdown
# S_nz_nan_guard — NaN/null value guarding

nz(source, replacement=0):
  Replace null values with replacement. Default replacement is 0.
  Equivalent to coalesce(source, replacement).

  CORRECT: clean_eps = nz(eps_surprise, 0)
           ratio = nz(volume / avg_volume, 1)

  WRONG:   clean_eps = where(is_null(eps_surprise), 0, eps_surprise)  — verbose
           clean_eps = eps_surprise  — null propagates through arithmetic

NULL PROPAGATION RULE:
  Any arithmetic with null produces null.
  Any comparison with null produces null (not False).
  Guard before use if the source can be null.

WHEN TO GUARD:
  - Fundamental data (earnings, P/E, etc.) — sparse, always guard
  - Computed transforms with warmup periods — guard first N bars
  - Reference asset data — may have gaps, guard at merge point
```

### grammar_generator.cpp change

```cpp
// Add to BUILTIN_FUNCTIONS (2b — time-series and utility):
"valuewhen", "barssince", "diff", "nz", "clamp", "sign",

// Add to BUILTIN_FUNCTIONS (2c — financial / quantitative):
"returns",      // ReturnType.Simple | Log  (new enum: ReturnType)
"cum",          // Agg.Sum | Product | Max | Min  (reuses AggregationType)
"linreg",       // LinRegType.Value | Slope | Intercept | Forecast  (new enum: LinRegType)
"lag",          // LagOp — compiler emits AST node directly
"prev",         // grammar rewrite → lag(src, 1)
"ratio",        // arithmetic: src / lag(src, N)

// Add to BUILTIN_FUNCTIONS (2d — arithmetic composites):
"normalize",    // min-max → arithmetic (agg composite + nz guard)
"drawdown",     // drawdown from rolling high → arithmetic (agg composite)

// Add to BUILTIN_FUNCTIONS (2e — type / logic):
"to_int",       // Boolean → 0/1 → where arithmetic
"relu",         // zero-floor → where arithmetic
"between",      // range check → logical arithmetic
"isna",         // → is_null grammar alias
"notna",        // → is_valid grammar alias

// New enums to register:
// RegisterEnumType("ReturnType", {"Simple", "Log"});
// RegisterEnumType("LinRegType", {"Value", "Slope", "Intercept", "Forecast"});
// NOTE: cum reuses existing AggregationType — no new enum needed
```

### Test cases

```cpp
// 2b
TEST_CASE("valuewhen default occurrence") { /* valuewhen(cond, src) → valuewhen(occurrence=0)(cond, src) */ }
TEST_CASE("valuewhen explicit occurrence") { /* valuewhen(cond, src, 2) → valuewhen(occurrence=2)(cond, src) */ }
TEST_CASE("barssince lowering") { /* barssince(cond) → barssince()(cond) */ }
TEST_CASE("diff default period") { /* diff(src) → mom(period=1)(src) */ }
TEST_CASE("diff explicit period") { /* diff(src, 5) → mom(period=5)(src) */ }
TEST_CASE("nz default replacement") { /* nz(src) → coalesce(src, 0.0) */ }
TEST_CASE("nz explicit replacement") { /* nz(src, 1.0) → coalesce(src, 1.0) */ }
TEST_CASE("clamp range clip") { /* clamp(src, 0, 1) → correct range clamping */ }
TEST_CASE("sign positive") { /* sign(1.5) → 1 */ }
TEST_CASE("sign negative") { /* sign(-0.3) → -1 */ }
TEST_CASE("sign zero") { /* sign(0) → 0 */ }
// 2c
TEST_CASE("returns simple 1-bar") { /* returns(close) → (close - lag(close,1)) / lag(close,1) */ }
TEST_CASE("returns simple N-bar") { /* returns(close, 5) → correct */ }
TEST_CASE("returns log") { /* returns(close, type=ReturnType.Log) → ln(close / lag(close,1)) */ }
TEST_CASE("lag default N") { /* lag(close) → LagOp(close, 1) */ }
TEST_CASE("lag explicit N") { /* lag(close, 5) → LagOp(close, 5) */ }
TEST_CASE("prev rewrite") { /* prev(close) → lag(close, 1) */ }
TEST_CASE("ratio default N") { /* ratio(close) → close / lag(close, 1) */ }
TEST_CASE("ratio explicit N") { /* ratio(close, 5) → close / lag(close, 5) */ }
// 2d
TEST_CASE("normalize flat window") { /* normalize(flat_series, 20) → 0 (nz guard) */ }
TEST_CASE("normalize normal window") { /* normalize(close, 20) → [0,1] range */ }
TEST_CASE("drawdown at high") { /* drawdown at rolling max → 0 */ }
TEST_CASE("drawdown below high") { /* drawdown below max → negative */ }
// 2e
TEST_CASE("to_int true") { /* to_int(True) → 1 */ }
TEST_CASE("to_int false") { /* to_int(False) → 0 */ }
TEST_CASE("relu positive") { /* relu(0.5) → 0.5 */ }
TEST_CASE("relu negative") { /* relu(-0.5) → 0 */ }
TEST_CASE("between in range") { /* between(50, 40, 60) → True */ }
TEST_CASE("between out of range") { /* between(70, 40, 60) → False */ }
TEST_CASE("isna rewrite") { /* isna(x) → is_null(x) — identical output */ }
TEST_CASE("notna rewrite") { /* notna(x) → is_valid(x) — identical output */ }
```

### Acceptance criteria

- [ ] All 20 names added to `BUILTIN_FUNCTIONS` (`valuewhen`, `barssince`, `diff`, `nz`, `clamp`, `sign`, `returns`, `cum`, `linreg`, `lag`, `prev`, `ratio`, `normalize`, `drawdown`, `to_int`, `relu`, `between`, `isna`, `notna`)
- [ ] `ReturnType` and `LinRegType` enums registered (auto-inline in grammar)
- [ ] All 29 test cases pass
- [ ] `valuewhen` and `barssince` produce identical output to two-stage registered forms
- [ ] `diff(src, 5)` produces identical output to `mom(period=5)(src)`
- [ ] `nz(src)` produces identical output to `coalesce(src, 0.0)`
- [ ] `mom` registered transform marked `internalUse=true`
- [ ] Grammar Tier A/C sections updated with all 20 builtin signatures and examples
- [ ] `S_valuewhen_barssince.md` and `S_nz_nan_guard.md` skill files complete
