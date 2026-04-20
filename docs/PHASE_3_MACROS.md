# Phase 3 — Variadic Macros

**Status:** Not started
**Depends on:** Phase 0 (COMPILER_MACROS + grammar + `BuiltinRegistry` from 0e), Phase 1 (variadic expansion infrastructure proven by resample)
**Goal:** Six macros that each collapse multiple registered transforms into one intent-focused construct.
**Touches:** `grammar_generator.cpp` (EBNF output), new files: `marker_expander.h`, `volatility_expander.h`, `select_expander.h`, `pair_stat_expander.h`, registration calls in `InitializeTransforms()`

### Architecture note

All macro expansion uses Phase 0e strategy interfaces. No code in `constructor_parser.cpp`.

- **`marker`** — custom `MarkerExpander` (event-to-defaults mapping, schema construction)
- **`candlestick_pattern`** — `VariadicInputExpander` strategy (N patterns → N impl nodes)
- **`macro_data`** — `VariadicInputExpander` strategy (N indicators → N common_indicators nodes)
- **`pair_stat`** — custom `PairStatExpander` (N metrics → N impl nodes sharing same inputs)
- **`volatility`** — custom `VolatilityExpander` (method enum routes to different impl nodes)
- **`select`** — custom `SelectExpander` (maps direction enum to cs_select options)

---

## 3a — `marker`

**Priority: highest.** `event_marker` is the #3 most misused construct in the library (skills audit). 4-level nesting, plural/singular confusion (`schema` vs `schemas`), wrong input order — all documented failures. `marker` collapses this to a single call.

### Current `event_marker` (what agents get wrong)

```python
# Current — 4 levels deep, agents consistently mis-specify:
event_marker(schema=EventMarkerSchema(
    title="Long Entry",
    icon=Icon.TrendingUpIcon,
    schemas=[
        EventMarkerColumnSchema(title="Price", value=close)
    ]
))(long_entry_signal)
```

### `marker` macro (what it becomes)

```python
# New — inputs first, event type last
marker(long_entry_signal, close, Event.LongEntry)
marker(long_entry_signal, open, Event.LongEntry, price_source=Price.Open, label="Entry")
```

### EBNF

```ebnf
marker_expr ::=
    "marker" "("
        series_expr ("," series_expr)?
        "," marker_event
        ("," "price_source" "=" price_source_ref)?
        ("," "label"        "=" string_literal)?
    ")"

marker_event ::= "Event" "." event_value
event_value  ::= "RoundTrip" | "Signal" | "Entry" | "Exit"
               | "LongEntry" | "LongExit" | "ShortEntry" | "ShortExit"
               | "StopLoss" | "TakeProfit" | "Rebalance"

price_source_ref ::= "Price" "." ("Open" | "High" | "Low" | "Close" | "Typical" | "Weighted")
```

### Expansion

```
marker(signal, close, Event.RoundTrip)
→ event_marker(schema=EventMarkerSchema(
      title="Round Trip",
      icon=<default for RoundTrip>,
      schemas=[EventMarkerColumnSchema(title="Price", value=close)]
  ))(signal)

marker(signal, open, Event.LongEntry, price_source=Price.Open, label="Entry")
→ event_marker(schema=EventMarkerSchema(
      title="Entry",
      icon=<default for LongEntry>,
      schemas=[EventMarkerColumnSchema(title="Price", value=open)]
  ))(signal)
```

The constructor_parser maps `Event.X` → default title + default icon + price column wiring. `label` overrides the title. `price_source` determines which price series is used in the column schema.

### Event → defaults map (hardcoded in constructor_parser.cpp)

| Event | Default title | Default icon |
|---|---|---|
| `RoundTrip` | "Round Trip" | `Icon.RepeatIcon` |
| `LongEntry` | "Long Entry" | `Icon.TrendingUpIcon` |
| `LongExit` | "Long Exit" | `Icon.TrendingDownIcon` |
| `ShortEntry` | "Short Entry" | `Icon.TrendingDownIcon` |
| `ShortExit` | "Short Exit" | `Icon.TrendingUpIcon` |
| `StopLoss` | "Stop Loss" | `Icon.ShieldIcon` |
| `TakeProfit` | "Take Profit" | `Icon.TargetIcon` |
| `Signal` | "Signal" | `Icon.BellIcon` |
| `Rebalance` | "Rebalance" | `Icon.RefreshIcon` |

### New enums to register

```cpp
RegisterEnumType("EventType", {"RoundTrip","Signal","Entry","Exit","LongEntry","LongExit","ShortEntry","ShortExit","StopLoss","TakeProfit","Rebalance"});
RegisterEnumType("PriceSource", {"Open","High","Low","Close","Typical","Weighted"});
```

Both small (≤12 values) → inline in EBNF quick reference, bundled on `marker` fetch.

### Grammar addition (`GenerateEBNF()` COMPILER MACROS section)

```
# ── marker ──────────────────────────────────────────────────────────────────
# marker(signal, event)
# marker(signal, price, event, price_source=Price.Close, label=String?)
#
#   marker(long_signal, Event.LongEntry)
#   marker(long_signal, close, Event.LongEntry, label="Entry")
#
# @EventType: RoundTrip Signal Entry Exit LongEntry LongExit
#             ShortEntry ShortExit StopLoss TakeProfit Rebalance
# @PriceSource: Open High Low Close Typical Weighted
#
# Deprecates: event_marker()
```

### Acceptance criteria

- [ ] `"marker"` in `COMPILER_MACROS`
- [ ] `marker(signal, close, Event.RoundTrip)` expands to valid `event_marker` node
- [ ] `label=` override works
- [ ] `price_source=` override works
- [ ] `EventType` and `PriceSource` enums registered and appear in Lezer grammar
- [ ] Grammar COMPILER MACROS section includes `marker` production rule with enum values
- [ ] `S_marker_event_types.md` skill complete

---

## 3b — `candlestick_pattern`

### What it replaces

26 individual transforms (`doji`, `hammer`, `engulfing_bull`, etc.) each with identical `(o, h, l, c) → Integer` signature. Using multiple patterns requires 26 separate lines. All 26 → `internalUse=true`.

### API

```python
# Request N patterns in one call → N named outputs
doji_s, hammer_s, engulf_s = candlestick_pattern(
    o, h, l, c,
    patterns=[Pattern.doji, Pattern.hammer, Pattern.engulfing_bull]
)
```

Output: Integer per pattern (-100 = bearish, 0 = none, +100 = bullish).

### EBNF

```ebnf
candlestick_expr ::=
    "candlestick_pattern" "("
        series_expr "," series_expr "," series_expr "," series_expr
        "," "patterns" "=" "[" pattern_ref ("," pattern_ref)* "]"
    ")"

pattern_ref    ::= "Pattern" "." pattern_name
pattern_name   ::=
    "doji" | "dragonfly_doji" | "gravestone_doji" | "four_price_doji" | "long_legged_doji"
  | "hammer" | "inverted_hammer" | "hanging_man" | "shooting_star"
  | "morning_star" | "evening_star" | "morning_doji_star" | "evening_doji_star"
  | "engulfing_bull" | "engulfing_bear"
  | "three_white_soldiers" | "three_black_crows"
  | "abandoned_baby_bull" | "abandoned_baby_bear"
  | "marubozu_bull" | "marubozu_bear"
  | "spinning_top" | "star" | "big_candle_bull" | "big_candle_bear"
```

### Expansion (input-driven variadic)

N patterns → N impl nodes, all sharing the same `(o, h, l, c)` inputs.

```
candlestick_pattern(o, h, l, c, patterns=[Pattern.doji, Pattern.hammer])
→ doji()(o, h, l, c)        → .result: Integer
  hammer()(o, h, l, c)      → .result: Integer
```

Empty `patterns=[]` → COMPILE ERROR.

### New enum to register

```cpp
RegisterEnumType("CandlestickPattern", {
    "doji", "dragonfly_doji", "gravestone_doji", "four_price_doji", "long_legged_doji",
    "hammer", "inverted_hammer", "hanging_man", "shooting_star",
    "morning_star", "evening_star", "morning_doji_star", "evening_doji_star",
    "engulfing_bull", "engulfing_bear",
    "three_white_soldiers", "three_black_crows",
    "abandoned_baby_bull", "abandoned_baby_bear",
    "marubozu_bull", "marubozu_bear",
    "spinning_top", "star", "big_candle_bull", "big_candle_bear"
});
```

26 values — inline in enum reference (this IS the pattern catalog, not a discovery space).

### Grammar addition (`GenerateEBNF()` COMPILER MACROS section)

```
# ── candlestick_pattern ──────────────────────────────────────────────────────
# candlestick_pattern(o, h, l, c, patterns=[Pattern.X, ...]) → Integer per pattern
#
#   doji_s = candlestick_pattern(o, h, l, c, patterns=[Pattern.doji])
#   doji_s, hammer_s = candlestick_pattern(o, h, l, c,
#                        patterns=[Pattern.doji, Pattern.hammer])
#
# Output: +100 bullish, 0 none, -100 bearish per pattern
#
# @CandlestickPattern: doji dragonfly_doji gravestone_doji four_price_doji
#   long_legged_doji hammer inverted_hammer hanging_man shooting_star
#   morning_star evening_star morning_doji_star evening_doji_star
#   engulfing_bull engulfing_bear three_white_soldiers three_black_crows
#   abandoned_baby_bull abandoned_baby_bear marubozu_bull marubozu_bear
#   spinning_top star big_candle_bull big_candle_bear
```

### Acceptance criteria

- [ ] `"candlestick_pattern"` in `COMPILER_MACROS`
- [ ] Single pattern → 1 impl node
- [ ] Multiple patterns → N impl nodes sharing same OHLC inputs
- [ ] Empty patterns list → COMPILE ERROR
- [ ] All 26 individual candlestick transforms marked `internalUse=true`
- [ ] `CandlestickPattern` enum registered and appears in grammar

---

## 3c — `macro_data`

### What it replaces

`common_indicators` with a single `MacroEconomicsIndicator` option — one call per indicator. Variadic form allows N indicators in one line → N output series.

### API

```python
cpi, pce, unemp = macro_data(Macro.CPI, Macro.PCE, Macro.Unemployment)
fed_funds        = macro_data(Macro.FedFunds)
```

### EBNF

```ebnf
macro_data_expr ::=
    "macro_data" "(" macro_indicator ("," macro_indicator)* ")"

macro_indicator ::= "Macro" "." macro_name
```

### Expansion (option-driven variadic — each positional arg is an indicator)

```
macro_data(Macro.CPI, Macro.PCE)
→ common_indicators(category=CPI)()    → Decimal
  common_indicators(category=PCE)()    → Decimal
```

### Note on `MacroEconomicsIndicator` enum

150+ values — discovery/catalog enum, NOT inlined in grammar. Users browse with `find_enum()` tool separately. Grammar just names the enum; inlining is skipped (same exclusion rule as Color, Icon).

### Grammar addition (`GenerateEBNF()` COMPILER MACROS section)

```
# ── macro_data ───────────────────────────────────────────────────────────────
# macro_data(Macro.X, Macro.Y, ...) → Decimal per indicator
#
#   fed_funds      = macro_data(Macro.FedFunds)
#   cpi, pce       = macro_data(Macro.CPI, Macro.PCE)
#
# @MacroEconomicsIndicator: 150+ values — use find_enum() to browse
# Deprecates: common_indicators()
```

### Acceptance criteria

- [ ] `"macro_data"` in `COMPILER_MACROS`
- [ ] Single indicator → 1 `common_indicators` node
- [ ] N indicators → N nodes, all with correct `category` option
- [ ] `common_indicators` marked `internalUse=true`
- [ ] No empty call `macro_data()` — COMPILE ERROR
- [ ] Grammar notes `MacroEconomicsIndicator` as catalog enum (not inlined)

---

## 3d — `pair_stat`

### What it replaces

`rolling_corr`, `rolling_cov`, `beta`, `ewm_corr` — 4 transforms with nearly identical signatures `(x, y) → Decimal`. Using multiple metrics requires 4 separate calls.

### API

```python
corr, cov = pair_stat(a, b, metrics=[Metric.correlation, Metric.covariance], window=60)
beta_v    = pair_stat(portfolio, benchmark, metrics=[Metric.beta], window=252)
```

### EBNF

```ebnf
pair_stat_expr ::=
    "pair_stat" "("
        series_expr "," series_expr
        "," "metrics" "=" "[" pair_metric ("," pair_metric)* "]"
        ("," "window"             "=" integer)?
        ("," "window_type"        "=" ("\"rolling\"" | "\"expanding\""))?
        ("," "correlation_method" "=" corr_method)?
    ")"

pair_metric ::= "Metric" "." ("correlation" | "covariance" | "beta" | "ewm_correlation")
corr_method ::= "\"pearson\"" | "\"spearman\"" | "\"kendall\""
```

### Expansion

N metrics → N impl nodes sharing same `(x, y)` inputs.

```
pair_stat(a, b, metrics=[Metric.correlation, Metric.covariance], window=60)
→ rolling_corr(window=60)(a, b)   → Decimal
  rolling_cov(window=60)(a, b)    → Decimal
```

`correlation_method` only forwarded to `rolling_corr` nodes (ignored for others).
Empty `metrics=[]` → COMPILE ERROR.

### New enum

```cpp
RegisterEnumType("PairMetric", {"correlation", "covariance", "beta", "ewm_correlation"});
```

### Grammar addition (`GenerateEBNF()` COMPILER MACROS section)

```
# ── pair_stat ────────────────────────────────────────────────────────────────
# pair_stat(x, y, metrics=[Metric.X, ...], window=N, window_type="rolling",
#           correlation_method="pearson") → Decimal per metric
#
#   corr, cov = pair_stat(a, b, metrics=[Metric.correlation, Metric.covariance], window=60)
#   beta_v    = pair_stat(portfolio, benchmark, metrics=[Metric.beta], window=252)
#
# @PairMetric: correlation covariance beta ewm_correlation
# Deprecates: rolling_corr() rolling_cov() beta() ewm_corr()
```

### Acceptance criteria

- [ ] `"pair_stat"` in `COMPILER_MACROS`
- [ ] Each metric maps to correct impl node
- [ ] `correlation_method` only forwarded where relevant
- [ ] Empty metrics → COMPILE ERROR
- [ ] All 4 individual transforms marked `internalUse=true`
- [ ] Grammar COMPILER MACROS section includes `pair_stat` production rule

---

## 3e — `volatility`

### What it replaces

`volatility` (annualized) + `basic_volatility` (returns/price_diff variants). `basic_volatility` → `internalUse=true`.

### API

```python
vol_ann    = volatility(close, method=VolMethod.annualized, period=14)
vol_ret    = volatility(close, method=VolMethod.returns, period=14)
vol_price  = volatility(close, method=VolMethod.price_diff, period=14)
```

`volatility_estimator` is NOT affected — different input arity (OHLC vs C).

### EBNF

```ebnf
volatility_macro_expr ::=
    "volatility" "("
        series_expr
        "," "method"          "=" vol_method
        ("," "period"         "=" integer)?
        ("," "trading_periods" "=" integer)?
    ")"

vol_method ::= "VolMethod" "." ("annualized" | "returns" | "price_diff")
```

### Expansion

```
volatility(c, method=VolMethod.annualized, period=14) → volatility(period=14)(c)
volatility(c, method=VolMethod.returns, period=14)    → basic_volatility(type=return_type, period=14)(c)
volatility(c, method=VolMethod.price_diff, period=14) → basic_volatility(type=price_diff, period=14)(c)
```

### New enum

```cpp
RegisterEnumType("VolMethod", {"annualized", "returns", "price_diff"});
```

### Grammar addition (`GenerateEBNF()` COMPILER MACROS section)

```
# ── volatility ───────────────────────────────────────────────────────────────
# volatility(source, method=VolMethod.X, period=N, trading_periods=N)
#
#   vol_ann   = volatility(close, method=VolMethod.annualized, period=14)
#   vol_ret   = volatility(close, method=VolMethod.returns, period=14)
#   vol_price = volatility(close, method=VolMethod.price_diff, period=14)
#
# @VolMethod: annualized returns price_diff
# NOTE: volatility_estimator (OHLC input) is a separate registered transform — not affected.
# Deprecates: basic_volatility()
```

### Acceptance criteria

- [ ] `"volatility"` in `COMPILER_MACROS`
- [ ] Each method routes to correct impl node
- [ ] `basic_volatility` marked `internalUse=true`
- [ ] `volatility_estimator` unchanged
- [ ] Grammar COMPILER MACROS section includes `volatility` production rule

---

## 3f — `select`

### What it replaces

`cs_select` with confusing `direction` enum and easy-to-forget `group_by`.

### API

```python
top5    = select(momentum, n=5, direction=Direction.Top)
bottom5 = select(momentum, n=5, direction=Direction.Bottom, group_by=GroupBy.sector)
```

### EBNF

```ebnf
select_expr ::=
    "select" "("
        series_expr
        "," "n"         "=" integer
        "," "direction" "=" select_direction
        ("," "group_by" "=" grouping_mode)?
    ")"

select_direction ::= "Direction" "." ("Top" | "Bottom")
```

### Expansion

```
select(momentum, n=5, direction=Direction.Top)
→ cs_select(n=5, direction=SelectDirection.Top)(momentum)
```

### New enum

```cpp
RegisterEnumType("SelectDirection", {"Top", "Bottom"});
```

### Grammar addition (`GenerateEBNF()` COMPILER MACROS section)

```
# ── select ───────────────────────────────────────────────────────────────────
# select(source, n=N, direction=Direction.X, group_by=GroupBy.Y?)
#
#   top5    = select(momentum, n=5, direction=Direction.Top)
#   bottom5 = select(momentum, n=5, direction=Direction.Bottom, group_by=GroupBy.sector)
#
# @SelectDirection: Top Bottom
# Deprecates: cs_select()
```

### Acceptance criteria

- [ ] `"select"` in `COMPILER_MACROS`
- [ ] Top and Bottom both route correctly
- [ ] `group_by` forwarded when present
- [ ] `cs_select` marked `internalUse=true`
- [ ] Grammar COMPILER MACROS section includes `select` production rule

---

## Phase 3 shared acceptance criteria

- [ ] All 6 macro names in `COMPILER_MACROS`
- [ ] Grammar COMPILER MACROS section has a production rule block for each macro
- [ ] All deprecated transforms marked `internalUse=true`
- [ ] Skill files complete for all macros
- [ ] No regressions in existing two-stage tests
