# Phase 5 — Classic Indicators & TA Builtins

**Status:** Not started
**Depends on:** Phase 0 complete (including `BuiltinRegistry` + strategy interfaces from 0e)
**Goal:** ~99 new builtin aliases + ~36 new macros covering classic TA indicators, MA aliases, statistical pair functions, multi-output constructs, period boundary decompositions, and calendar utilities.
**Touches:** `grammar_generator.cpp` (EBNF output), registration calls in `InitializeTransforms()`

### Architecture note

Phase 5 is primarily **declarative registration** — the reusable strategy classes from Phase 0e cover ~90% of builtins. No custom lowering classes needed (all custom strategies were built in Phases 0–3). No code in `constructor_parser.cpp`.

**Strategy usage:**
- **5a (10 MA aliases):** `MaAliasLowering` — loop registration
- **5b (27 single-series):** `SameNamePeriodLowering` (most), `MultiPeriodLowering` (apo/ppo)
- **5c (22 multi-series):** `SameNamePeriodLowering` with input_count override, `MultiPeriodLowering` (ultosc/psar/adosc/kvo/vosc)
- **5d (4 pair stats):** `SameNamePeriodLowering` with option_name="window"
- **5e (22 no-param):** `SameNameNoParamLowering` — declarative input counts
- **5f (14 calendar):** `EnumGatedLowering` (4 filters), `PeriodBoundaryLowering` (9 decompositions), `SameNamePeriodLowering` (calendar_shift)
- **5g–5l (36 macros):** `SingleImplMultiOutputExpander` — declarative output slot lists

---

## Overview

| Section | Type | Count | Contents |
|---|---|---|---|
| 5a | builtins | 10 | MA type aliases (ema, sma, wma, ...) |
| 5b | builtins | 27 | Single-series period indicators (+apo, ppo, forward_returns, arg_max, arg_min) |
| 5c | builtins | 22 | Multi-series period indicators (+ultosc, psar, adosc, kvo, vosc) |
| 5d | builtins | 4 | Pair statistics (corr, cov, beta, ewm_cov) |
| 5e | builtins | 22 | No-parameter indicators (+hold_until, trade_count, switch, is_study_asset) |
| 5f | builtins | 14 | Calendar / temporal builtins (+9 period boundary decompositions, +calendar_shift) |
| 5g | macros | 7 | Trend multi-output (aroon, di, dm, vortex, alligator, supertrend, ichimoku) |
| 5h | macros | 5 | Momentum multi-output (macd, stoch, fisher, msw, qqe) |
| 5i | macros | 7 | Volatility multi-output (bbands, donchian_channel, ...) |
| 5j | macros | 4 | Statistical/math (cs_first_last, linear_fit, half_life_ar1, arg_minmax) |
| 5k | macros | 7 | PriceAction (bos_choch, fair_value_gap, order_blocks, ...) |
| 5l | macros | 6 | ControlFlow (turn_of_month, cusum, bar_gap, session_gap, session_window, pivot_point_sr) |
| 5m | internal | ~50 | All internalUse designations for this phase |

**After Phase 5:** ~160 total public Layer 1/2 constructs replacing ~220+ fragmented impl nodes.

---

## 5a — MA Type Aliases (10 builtins)

**Design rationale:** When the type is baked into the name, there is no need for an enum gate.
`ema(close, 14)` is unambiguous. `ma(type=ema, period=14)(close)` is the registered power-user form.
`vidya` stays `[registered]` because `alpha` is required with no universal default.

### API

```python
ema(close, 14)      # exponential MA
sma(close, 20)      # simple MA (= agg(close, 20, Agg.Mean) — both valid)
wma(close, 14)      # weighted MA
hma(close, 14)      # Hull MA
dema(close, 14)     # double EMA
tema(close, 14)     # triple EMA
kama(close, 14)     # Kaufman adaptive MA
trima(close, 14)    # triangular MA
wilders(close, 14)  # Wilder's smoothing
zlema(close, 14)    # zero-lag EMA
```

### Lowering

All: `fn(src, N)` → `ma(type=<fn_name>, period=N)(src)`

| Builtin | `ma(type=X, ...)` |
|---|---|
| `ema` | `type=ema` |
| `sma` | `type=sma` |
| `wma` | `type=wma` |
| `hma` | `type=hma` |
| `dema` | `type=dema` |
| `tema` | `type=tema` |
| `kama` | `type=kama` |
| `trima` | `type=trima` |
| `wilders` | `type=wilders` |
| `zlema` | `type=zlema` |

### grammar_generator.cpp additions

```cpp
// 5a — MA type aliases
"ema", "sma", "wma", "hma", "dema", "tema", "kama", "trima", "wilders", "zlema",
```

### Grammar block (Tier D — MA aliases)

```
# ── Moving Average aliases ────────────────────────────────────────────────────
# All single-stage: fn(source, period) → Decimal
# All lower to ma(type=X, period=N)(source). ma() registered form still available.
#
#   ema(close, 14)      — exponential MA
#   sma(close, 20)      — simple MA (= agg(close, 20, Agg.Mean))
#   wma(close, 14)      — weighted MA
#   hma(close, 14)      — Hull MA
#   dema(close, 14)     — double EMA
#   tema(close, 14)     — triple EMA
#   kama(close, 14)     — Kaufman adaptive MA
#   trima(close, 14)    — triangular MA
#   wilders(close, 14)  — Wilder's smoothing
#   zlema(close, 14)    — zero-lag EMA
#
# NOTE: vwma(src, volume, period) requires 2 series — see Section 5c
# NOTE: vidya stays as registered transform (alpha parameter is required, no default)
# DO NOT: ma(type=ema, period=14)(close) — use ema(close, 14) instead (internalUse after migration)
```

### Test cases

```cpp
TEST_CASE("ema 14") { /* ema(close, 14) → ma(type=ema, period=14)(close), identical output */ }
TEST_CASE("sma 20 equals agg mean") { /* sma(close, 20) === agg(close, 20, Agg.Mean) */ }
TEST_CASE("hma lowering") { /* hma(close, 20) → ma(type=hma, period=20)(close) */ }
TEST_CASE("zlema lowering") { /* zlema(close, 14) → ma(type=zlema, period=14)(close) */ }
TEST_CASE("ema missing period error") { /* ema(close) → COMPILE ERROR: period required */ }
```

### Acceptance criteria

- [ ] All 10 names in `BUILTIN_FUNCTIONS`
- [ ] `ema(close, 14)` produces identical output to `ma(type=ema, period=14)(close)`
- [ ] `sma(close, 20)` produces identical output to `agg(close, 20, Agg.Mean)`
- [ ] Missing period → COMPILE ERROR
- [ ] Grammar Tier D section added with all 10 names, notes on vidya/vwma

---

## 5b — Single-Series Period Builtins (27)

Pattern: `fn(src, period)` → `fn(period=N)(src)` — same name as the existing impl node.

| Builtin | Category | Notes |
|---|---|---|
| `rsi` | Momentum | RSI [0, 100] |
| `trix` | Momentum | Triple EMA oscillator |
| `cmo` | Momentum | Chande Momentum Oscillator |
| `fosc` | Momentum | Forecast Oscillator (deviation from TSF) |
| `roc` | Momentum | Rate of change ×100; distinct from `returns` |
| `rocr` | Momentum | Ratio form; alias for `ratio(src, N)` but keep canonical |
| `stochrsi` | Momentum | Stochastic RSI [0, 1] |
| `apo` | Momentum | Absolute Price Oscillator (short/long EMA diff) |
| `ppo` | Momentum | Percentage Price Oscillator (short/long EMA %diff) |
| `dpo` | Trend | Detrended Price Oscillator |
| `vhf` | Trend | Vertical Horizontal Filter |
| `md` | Trend | Mean Deviation (rolling) |
| `ulcer_index` | Volatility | Drawdown-based volatility; `use_sum=False` default ⚠ verify |
| `percentrank` | Statistical | Percentile rank within window |
| `streak_length` | Statistical | Signed: +N = up streak of N, −N = down streak. No period needed. |
| `nlargest` | Statistical | `nlargest(src, N)` — N-th largest rolling value. N = size not period. |
| `nsmallest` | Statistical | `nsmallest(src, N)` |
| `hurst_exponent` | Statistical | `hurst_exponent(src)` or `hurst_exponent(src, min_period=20)` |
| `rolling_hurst_exponent` | Statistical | `rolling_hurst_exponent(src, window)` |
| `decay` | Math | Linear decay weighting |
| `edecay` | Math | Exponential decay weighting |
| `stderr` | Math | Rolling standard error |
| `forward_returns` | Math | `forward_returns(src, N)` — N-bar ahead return (lookahead) |
| `arg_max` | Math | `arg_max(src)` `→ Timestamp` — timestamp of running maximum |
| `arg_min` | Math | `arg_min(src)` `→ Timestamp` — timestamp of running minimum |
| `highestbars` | Indicator | `→ Int` — bars since rolling highest |
| `lowestbars` | Indicator | `→ Int` — bars since rolling lowest |

**Note on `streak_length`:** Returns signed integer. No direction param needed — sign carries the direction. `+3` = currently in a 3-bar up streak, `−2` = currently in a 2-bar down streak.

**Note on `nlargest`/`nsmallest`:** The second argument is the rank N (e.g., 3rd largest), not a rolling window. These require a separate window param or use expanding context. ⚠ Verify impl node signature before implementing.

**Note on `apo`/`ppo`:** Two period params: `apo(src, short_period, long_period)`. Impl defaults are both 14 — standard usage is 12/26. Grammar documents standard call pattern.

**Note on `arg_max`/`arg_min`:** Return type is **Timestamp**, not Decimal. Optional `expanding` param (default true). `expanding=false` returns global argmax/argmin timestamp for all rows.

**Note on `forward_returns`:** Uses lookahead — label-only, not for live signals. Optional `return_type` param (default "simple", also "log").

### grammar_generator.cpp additions

```cpp
// 5b — single-series period builtins
"rsi", "trix", "cmo", "fosc", "roc", "rocr", "stochrsi",
"apo", "ppo",
"dpo", "vhf", "md",
"ulcer_index",
"percentrank", "streak_length", "nlargest", "nsmallest",
"hurst_exponent", "rolling_hurst_exponent",
"decay", "edecay", "stderr",
"forward_returns", "arg_max", "arg_min",
"highestbars", "lowestbars",
```

### Grammar block (Tier D — single-series period)

```
# ── Single-series period builtins ────────────────────────────────────────────
# Momentum — fn(source, period) → Decimal:
#   rsi(src, 14)          — Relative Strength Index [0, 100]
#   trix(src, 14)         — Triple-smoothed EMA rate of change
#   cmo(src, 14)          — Chande Momentum Oscillator
#   fosc(src, 14)         — Forecast Oscillator (pct deviation from TSF)
#   roc(src, 14)          — Rate of change ×100; for [−1,1] form use returns()
#   rocr(src, 14)         — Rate of change ratio; for ratio form use ratio()
#   stochrsi(src, 14)     — Stochastic RSI [0, 1]
#   apo(src, 12, 26)      — Absolute Price Oscillator (short/long EMA diff)
#   ppo(src, 12, 26)      — Percentage Price Oscillator (short/long EMA %diff)
#
# Trend — fn(source, period) → Decimal:
#   dpo(src, 14)          — Detrended Price Oscillator
#   vhf(src, 14)          — Vertical Horizontal Filter
#   md(src, 14)           — Mean Deviation (rolling)
#
# Volatility:
#   ulcer_index(src, 14)  — Ulcer Index (drawdown-based vol measure)
#
# Statistical:
#   percentrank(src, 14)                      — percentile rank in window, [0, 1]
#   streak_length(src)                         → Int — +N up, −N down streak
#   nlargest(src, N)                           — N-th largest value in rolling context
#   nsmallest(src, N)                          — N-th smallest value
#   hurst_exponent(src, min_period=20)         — Hurst exponent (full-series)
#   rolling_hurst_exponent(src, window)        — rolling Hurst exponent
#
# Math:
#   decay(src, period)                         — linear decay-weighted value
#   edecay(src, period)                        — exponential decay-weighted value
#   stderr(src, period)                        — rolling standard error
#   forward_returns(src, 5)                    — N-bar ahead return (lookahead, label-only)
#   arg_max(src)                → Timestamp    — timestamp of running maximum
#   arg_min(src)                → Timestamp    — timestamp of running minimum
#   arg_max(src, expanding=False) → Timestamp  — global max timestamp (broadcast)
#
# Indicator — returns Int:
#   highestbars(src, period) → Int  — bars since highest value in window
#   lowestbars(src, period)  → Int  — bars since lowest value in window
```

### Test cases

```cpp
TEST_CASE("rsi 14 single-stage") { /* rsi(close, 14) → rsi(period=14)(close), identical output */ }
TEST_CASE("roc vs returns distinction") { /* roc(close, 5) = returns(close, 5) * 100 */ }
TEST_CASE("streak_length signed up") { /* on 5-bar up streak → +5 */ }
TEST_CASE("streak_length signed down") { /* on 3-bar down streak → -3 */ }
TEST_CASE("highestbars returns int") { /* highestbars(close, 14) → Int series */ }
TEST_CASE("stochrsi bounds") { /* stochrsi(close, 14) ∈ [0, 1] */ }
TEST_CASE("apo two periods") { /* apo(close, 12, 26) → apo(short_period=12, long_period=26)(close) */ }
TEST_CASE("ppo two periods") { /* ppo(close, 12, 26) → ppo(short_period=12, long_period=26)(close) */ }
TEST_CASE("arg_max returns timestamp") { /* arg_max(close) → Timestamp series */ }
TEST_CASE("arg_min expanding false") { /* arg_min(close, expanding=False) → same timestamp every row */ }
TEST_CASE("forward_returns lookahead") { /* forward_returns(close, 5) → return 5 bars ahead */ }
```

### Acceptance criteria

- [ ] All 27 names in `BUILTIN_FUNCTIONS`
- [ ] Each `fn(src, N)` produces identical output to `fn(period=N)(src)` registered form
- [ ] `streak_length` returns signed integer (no direction param needed)
- [ ] `roc(close, N)` verified to differ from `returns(close, N)` by factor of 100
- [ ] `arg_max`/`arg_min` verified to return Timestamp type
- [ ] `forward_returns` verified to use lookahead (not for live signals)
- [ ] `apo`/`ppo` two-period lowering verified (short_period, long_period)

---

## 5c — Multi-Series Period Builtins (22)

These take 2–4 data series plus a period parameter.

| Builtin | Signature | Lowers to | Notes |
|---|---|---|---|
| `cci` | `cci(high, low, close, 14)` | `cci(period=14)(high, low, close)` | |
| `mfi` | `mfi(high, low, close, volume, 14)` | `mfi(period=14)(high, low, close, volume)` | |
| `willr` | `willr(high, low, close, 14)` | `willr(period=14)(high, low, close)` | |
| `atr` | `atr(high, low, close, 14)` | `atr(period=14)(high, low, close)` | |
| `natr` | `natr(high, low, close, 14)` | `natr(period=14)(high, low, close)` | Normalized ATR |
| `cvi` | `cvi(high, low, 14)` | `cvi(period=14)(high, low)` | Chaikin Volatility |
| `mass` | `mass(high, low, 14)` | `mass(period=14)(high, low)` | Mass Index |
| `adx` | `adx(high, low, 14)` | `adx(period=14)(high, low)` | ⚠ verify — ADX may need close internally |
| `adxr` | `adxr(high, low, 14)` | `adxr(period=14)(high, low)` | ⚠ verify input arity |
| `dx` | `dx(high, low, 14)` | `dx(period=14)(high, low)` | ⚠ verify input arity |
| `aroonosc` | `aroonosc(high, low, 14)` | `aroonosc(period=14)(high, low)` | |
| `vwma` | `vwma(src, volume, 14)` | `vwma(period=14)(src, volume)` | Volume-weighted MA |
| `qstick` | `qstick(open, close, 14)` | `qstick(period=14)(open, close)` | |
| `psl` | `psl(high, low, 12)` | `psl(period=12)(high, low)` | Psychological Strength Line |
| `ultosc` | `ultosc(h, l, c, 7, 14, 28)` | `ultosc(short=7, medium=14, long=28)(h, l, c)` | ⚠ impl defaults all 14, standard is 7/14/28 |
| `psar` | `psar(h, l, 0.02, 0.2)` | `psar(step=0.02, max=0.2)(h, l)` | Parabolic SAR |
| `adosc` | `adosc(h, l, c, vol, 3, 10)` | `adosc(short=3, long=10)(h, l, c, vol)` | A/D Oscillator |
| `kvo` | `kvo(h, l, c, vol, 34, 55)` | `kvo(short=34, long=55)(h, l, c, vol)` | Klinger Volume Oscillator |
| `vosc` | `vosc(volume, 12, 26)` | `vosc(short=12, long=26)(vol)` | Volume Oscillator |
| `intraday_returns` | `intraday_returns(close, open)` | `intraday_returns()(close, open)` | No period ⚠ verify return_type param |
| `rising` | `rising(src, 1)` | `rising(length=1)(src)` | Boolean: is src rising? |
| `falling` | `falling(src, 1)` | `falling(length=1)(src)` | Boolean: is src falling? |

**Note on `rising`/`falling`:** Categorized under ControlFlow but placed here since they take `(src, length)`. `length=1` default is appropriate: "is the value higher than 1 bar ago?"

**Note on `ultosc`:** Standard Williams defaults are 7/14/28. Impl node defaults are all 14 — grammar documents standard defaults, compiler passes through user values.

**Note on `psar`:** Impl param names are verbose (`acceleration_factor_step`/`acceleration_factor_maximum`). Builtin uses `step`/`max` — compiler maps to impl names.

### grammar_generator.cpp additions

```cpp
// 5c — multi-series period builtins
"cci", "mfi", "willr",
"atr", "natr", "cvi", "mass",
"adx", "adxr", "dx", "aroonosc",
"vwma", "qstick", "psl",
"ultosc", "psar",
"adosc", "kvo", "vosc",
"intraday_returns",
"rising", "falling",
```

### Grammar block

```
# ── Multi-series period builtins ─────────────────────────────────────────────
# Momentum:
#   cci(high, low, close, 14)          — Commodity Channel Index
#   mfi(high, low, close, volume, 14)  — Money Flow Index [0, 100]
#   willr(high, low, close, 14)        — Williams %R [−100, 0]
#   ultosc(h, l, c, 7, 14, 28)        — Ultimate Oscillator (3 periods)
#
# Volatility:
#   atr(high, low, close, 14)          — Average True Range
#   natr(high, low, close, 14)         — Normalized ATR (ATR / close × 100)
#   cvi(high, low, 14)                 — Chaikin Volatility Index
#   mass(high, low, 14)                — Mass Index (volatility reversal indicator)
#   psar(high, low, 0.02, 0.2)        — Parabolic SAR (step, max acceleration)
#
# Trend:
#   adx(high, low, 14)                 — Average Directional Index [0, 100]
#   adxr(high, low, 14)                — ADX Rating (smoothed ADX)
#   dx(high, low, 14)                  — Directional Movement Index
#   aroonosc(high, low, 14)            — Aroon Oscillator (−100 to +100)
#   vwma(source, volume, 14)           — Volume Weighted Moving Average
#
# Volume:
#   adosc(h, l, c, volume, 3, 10)     — Accumulation/Distribution Oscillator
#   kvo(h, l, c, volume, 34, 55)      — Klinger Volume Oscillator
#   vosc(volume, 12, 26)              — Volume Oscillator (short/long MA diff)
#
# Other:
#   qstick(open, close, 14)            — Qstick (body size MA)
#   psl(high, low, 12)                 — Psychological Strength Line
#   intraday_returns(close, open)      — intraday return (close vs open)
#
# Control:
#   rising(source, length=1)  → Boolean  — is source rising over length bars?
#   falling(source, length=1) → Boolean  — is source falling over length bars?
```

### Test cases

```cpp
TEST_CASE("atr 3-series") { /* atr(high, low, close, 14) → atr(period=14)(high, low, close) */ }
TEST_CASE("cci 3-series") { /* cci(high, low, close, 20) → cci(period=20)(high, low, close) */ }
TEST_CASE("vwma 2-series") { /* vwma(close, volume, 14) → vwma(period=14)(close, volume) */ }
TEST_CASE("rising default length") { /* rising(close) → rising(length=1)(close) */ }
TEST_CASE("falling explicit length") { /* falling(close, 3) → falling(length=3)(close) */ }
```

### Acceptance criteria

- [ ] All 22 names in `BUILTIN_FUNCTIONS`
- [ ] ADX/ADXR/DX input arity verified against actual impl nodes before shipping
- [ ] `intraday_returns` default return_type verified
- [ ] `rising`/`falling` return Boolean series
- [ ] `ultosc` standard defaults (7/14/28) documented; impl defaults verified
- [ ] `psar` param name mapping (step→acceleration_factor_step, max→acceleration_factor_maximum)
- [ ] `adosc`/`kvo`/`vosc` two-period lowering verified

---

## 5d — Pair Statistics Builtins (4)

**Design rationale:** `corr(a, b, 60)` and `cov(a, b, 60)` are universally known one-liners. No enum gate needed — grammar IS the contract. `pair_stat` macro (Phase 3) coexists for multi-metric batching.

| Builtin | Signature | Lowers to | Notes |
|---|---|---|---|
| `corr` | `corr(a, b, window)` | `rolling_corr(window=N)(a, b)` | Grammar documents, no enum |
| `cov` | `cov(a, b, window)` | `rolling_cov(window=N)(a, b)` | Grammar documents, no enum |
| `beta` | `beta(a, b, window)` | `beta(window=N)(a, b)` | Grammar documents, no enum |
| `ewm_cov` | `ewm_cov(a, b, span)` | `ewm_cov(span=N)(a, b)` | Not in pair_stat; standalone builtin |

**On `ewm_corr`:** Stays `[internal]` — accessible only via `pair_stat(metrics=[Metric.ewm_correlation])`. No standalone builtin (less commonly used as a direct one-liner).

### grammar_generator.cpp additions

```cpp
// 5d — pair statistics (no enum, grammar-documented)
"corr", "cov", "beta", "ewm_cov",
```

### Grammar block

```
# ── Pair statistics ───────────────────────────────────────────────────────────
# All: fn(series_a, series_b, window) → Decimal
# No enum gate — grammar is the contract. Use pair_stat() for multi-metric batching.
#
#   corr(returns_a, returns_b, 60)         — rolling Pearson correlation [−1, 1]
#   cov(returns_a, returns_b, 60)          — rolling covariance
#   beta(portfolio_returns, spy_returns, 252) — rolling beta
#   ewm_cov(returns_a, returns_b, span=20) — EWM covariance
#
# For multiple metrics in one call: pair_stat(a, b, metrics=[Metric.X, ...], window=N)
# Deprecates: rolling_corr() rolling_cov() beta() (impl nodes → internalUse)
```

### Test cases

```cpp
TEST_CASE("corr no enum") { /* corr(a, b, 60) → rolling_corr(window=60)(a, b), identical output */ }
TEST_CASE("cov no enum") { /* cov(a, b, 60) → rolling_cov(window=60)(a, b) */ }
TEST_CASE("beta window") { /* beta(portfolio, spy, 252) → beta(window=252)(portfolio, spy) */ }
TEST_CASE("ewm_cov span") { /* ewm_cov(a, b, 20) → ewm_cov(span=20)(a, b) */ }
TEST_CASE("corr result in minus1 plus1") { /* corr result ∈ [−1, 1] */ }
```

### Acceptance criteria

- [ ] `corr`, `cov`, `beta`, `ewm_cov` in `BUILTIN_FUNCTIONS`
- [ ] `corr(a, b, 60)` produces identical output to `rolling_corr(window=60)(a, b)`
- [ ] No enum referenced in the call site — positional args only
- [ ] `rolling_corr`, `rolling_cov`, `beta` (impl), `ewm_cov` (old registered) → `internalUse=true`

---

## 5e — No-Parameter Builtins (22)

All lower to `fn()(inputs...)` — registered impl with no options.

| Builtin | Signature | Category | Notes |
|---|---|---|---|
| `tr` | `tr(high, low, close)` | Volatility | True Range |
| `price_distance` | `price_distance(o, h, l, c)` | Volatility | Bar range metric |
| `bband_percent` | `bband_percent(upper, mid, lower)` | Volatility | %B — position within Bollinger Bands |
| `bband_width` | `bband_width(upper, mid, lower)` | Volatility | Bandwidth relative to middle band |
| `ao` | `ao(high, low)` | Momentum | Awesome Oscillator (5/34 MA of midpoints) |
| `bop` | `bop(open, high, low, close)` | Momentum | Balance of Power |
| `avgprice` | `avgprice(open, high, low, close)` | Trend | OHLC average |
| `medprice` | `medprice(high, low)` | Trend | (H+L)/2 |
| `typprice` | `typprice(high, low, close)` | Trend | (H+L+C)/3 |
| `wcprice` | `wcprice(high, low, close)` | Trend | Weighted Close (H+L+2C)/4 |
| `obv` | `obv(close, volume)` | Volume | On Balance Volume (cumulative) |
| `ad` | `ad(high, low, close, volume)` | Volume | Chaikin A/D Line |
| `emv` | `emv(high, low, volume)` | Volume | Ease of Movement |
| `nvi` | `nvi(close, volume)` | Volume | Negative Volume Index |
| `pvi` | `pvi(close, volume)` | Volume | Positive Volume Index |
| `marketfi` | `marketfi(high, low, volume)` | Volume | Market Facilitation Index |
| `wad` | `wad(high, low, close)` | Volume | Williams Accumulation/Distribution |
| `vwap` | `vwap()` | Volume | Session VWAP ⚠ datasource-aware, verify anchoring |
| `hold_until` | `hold_until(enter, exit)` | ControlFlow | `→ Boolean` — True from enter until exit signal |
| `trade_count` | `trade_count()` | ControlFlow | `→ Int` — datasource-aware, cumulative trade count |
| `switch` | `switch(index, a, b, c)` | ControlFlow | `→ Any` — variadic multiplexer by integer index |
| `is_study_asset` | `is_study_asset(ticker="SPY")` | ControlFlow | `→ Boolean` — check study asset metadata filters |

**Note on `bband_percent`/`bband_width`:** These consume the OUTPUT of `bbands`, not raw price:
```python
upper, middle, lower = bbands(close, 20, 2.0)
pct_b = bband_percent(upper, middle, lower)   # %B
width = bband_width(upper, middle, lower)      # bandwidth
```

**Note on `vwap`:** Zero explicit inputs — uses study market data context. ⚠ Verify whether anchoring is session (intraday reset) or day (daily data VWAP). Daily-data VWAP = typical price × volume / cumulative volume.

### grammar_generator.cpp additions

```cpp
// 5e — no-param builtins
"tr", "price_distance", "bband_percent", "bband_width",
"ao", "bop",
"avgprice", "medprice", "typprice", "wcprice",
"obv", "ad", "emv", "nvi", "pvi", "marketfi", "wad",
"vwap",
"hold_until", "trade_count",
"switch", "is_study_asset",
```

### Grammar block

```
# ── No-parameter indicator builtins ──────────────────────────────────────────
# Volatility:
#   tr(high, low, close)             — True Range
#   price_distance(o, h, l, c)       — full bar range metric
#   bband_percent(upper, mid, lower) — %B: (close − lower) / (upper − lower)
#   bband_width(upper, mid, lower)   — (upper − lower) / middle
#
# Momentum (no period):
#   ao(high, low)                    — Awesome Oscillator
#   bop(open, high, low, close)      — Balance of Power
#
# Price composites:
#   avgprice(open, high, low, close) — (O+H+L+C)/4
#   medprice(high, low)              — (H+L)/2
#   typprice(high, low, close)       — (H+L+C)/3
#   wcprice(high, low, close)        — (H+L+2C)/4
#
# Volume (no period):
#   obv(close, volume)               — cumulative On Balance Volume
#   ad(high, low, close, volume)     — Chaikin A/D Line
#   emv(high, low, volume)           — Ease of Movement
#   nvi(close, volume)               — Negative Volume Index
#   pvi(close, volume)               — Positive Volume Index
#   marketfi(high, low, volume)      — Market Facilitation Index
#   wad(high, low, close)            — Williams Accumulation/Distribution
#   vwap()                           — VWAP (datasource-aware)
#
# Control flow:
#   hold_until(enter, exit)    → Boolean  — True from enter signal until exit signal
#   trade_count()              → Int      — cumulative trade count (datasource-aware)
#   switch(index, a, b, c)    → Any      — returns slot matching integer index (variadic)
#
# Asset metadata filter (renamed from is_asset_ref):
#   is_study_asset(ticker="SPY")             → Boolean  — is this asset SPY?
#   is_study_asset(sector="Technology")      → Boolean  — is this a tech stock?
#   is_study_asset(asset_class="Stocks", exchange="NYSE") → Boolean
```

### Acceptance criteria

- [ ] All 22 names in `BUILTIN_FUNCTIONS`
- [ ] `bband_percent`/`bband_width` correctly documented as taking band values, not raw price
- [ ] `vwap()` impl semantics verified (session vs. day anchoring)

---

## 5f — Calendar / Temporal Builtins (14)

Three sub-groups: enum-gated calendar filters (4), period boundary decompositions (9), and calendar shift (1).

### 5f-i: Calendar filter builtins (4)

| Builtin | Signature | Enum | Notes |
|---|---|---|---|
| `day_of_week` | `day_of_week(DayOfWeek.Monday)` | `DayOfWeek` | True on matching weekday |
| `month_of_year` | `month_of_year(Month.January)` | `Month` | True in matching month |
| `quarter` | `quarter(Quarter.Q1)` | `Quarter` | True in matching quarter |
| `week_of_month` | `week_of_month(WeekOfMonth.First)` | `WeekOfMonth` | True in matching week |

**New enums to register:**

```cpp
RegisterEnumType("DayOfWeek",   {"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"});
RegisterEnumType("Month",       {"January","February","March","April","May","June",
                                  "July","August","September","October","November","December"});
RegisterEnumType("Quarter",     {"Q1","Q2","Q3","Q4"});
RegisterEnumType("WeekOfMonth", {"First","Second","Third","Fourth","Last"});
```

### 5f-ii: Period Boundary Decompositions (9)

**Design rationale:** `is_period_boundary` is a powerful registered transform with 8 options (period, boundary, ordinal, day_anchor, day_of_month, month_anchor, offset, timezone). Common use cases are simple one-liners that don't need this complexity. Decompose into named builtins for the 4×2 (period × boundary) matrix plus OPEX.

The full `is_period_boundary` registered transform stays available for advanced patterns (e.g., "second Tuesday of the month with offset -1").

| Builtin | Lowers to | Notes |
|---|---|---|
| `is_month_start` | `is_period_boundary(period=month, boundary=start)` | First bar of new month |
| `is_month_end` | `is_period_boundary(period=month, boundary=end)` | Last bar of month |
| `is_quarter_start` | `is_period_boundary(period=quarter, boundary=start)` | First bar of new quarter |
| `is_quarter_end` | `is_period_boundary(period=quarter, boundary=end)` | Last bar of quarter |
| `is_year_start` | `is_period_boundary(period=year, boundary=start)` | First bar of new year |
| `is_year_end` | `is_period_boundary(period=year, boundary=end)` | Last bar of year |
| `is_week_start` | `is_period_boundary(period=week, boundary=start)` | First bar of new week |
| `is_week_end` | `is_period_boundary(period=week, boundary=end)` | Last bar of week |
| `is_opex` | `is_period_boundary(period=quarter, month_anchor=3, ordinal=third, day_anchor=friday)` | Quarterly options expiration |

All return `Boolean`. All accept optional `offset` param for T-1/T+1 pre/post-positioning:
```python
rebal = is_month_start(offset=-1)   # T-1: signal one bar before month start
```

Input is implicitly the bar's timestamp (no explicit input needed — compiler injects study timestamp).

### 5f-iii: Calendar Shift (1)

**Design rationale:** `calendar_shift` has a single Duration option and single Decimal input/output. Perfect one-liner builtin. Very commonly used for cross-asset calendar-aligned lookbacks.

| Builtin | Signature | Notes |
|---|---|---|
| `calendar_shift` | `calendar_shift(src, "1M")` | Shift series by calendar duration |

Lowering: `calendar_shift(src, dur)` → `calendar_shift(period=dur)(src)`

Duration strings: `"1M"` (1 month), `"1W"` (1 week), `"63D"` (63 days), `"-7D"` (forward 7 days, negative = lead).

### grammar_generator.cpp additions

```cpp
// 5f — calendar builtins (enum-gated — names could be ambiguous without enum)
"day_of_week", "month_of_year", "quarter", "week_of_month",
// 5f — period boundary decompositions
"is_month_start", "is_month_end", "is_quarter_start", "is_quarter_end",
"is_year_start", "is_year_end", "is_week_start", "is_week_end", "is_opex",
// 5f — calendar shift
"calendar_shift",
```

### Grammar block

```
# ── Calendar / temporal builtins ─────────────────────────────────────────────
# Calendar filters → Boolean (True on matching bars):
#   day_of_week(DayOfWeek.Monday)       — True on Mondays
#   month_of_year(Month.January)        — True in January
#   quarter(Quarter.Q1)                 — True in Q1 (Jan–Mar)
#   week_of_month(WeekOfMonth.First)    — True in first calendar week of month
#
# @DayOfWeek: Monday Tuesday Wednesday Thursday Friday Saturday Sunday
# @Month: January February March April May June July August September October November December
# @Quarter: Q1 Q2 Q3 Q4
# @WeekOfMonth: First Second Third Fourth Last
#
# Period boundary decompositions → Boolean (all accept optional offset param):
#   is_month_start()        — first bar of new month
#   is_month_end()          — last bar of month
#   is_quarter_start()      — first bar of new quarter
#   is_quarter_end()        — last bar of quarter
#   is_year_start()         — first bar of new year
#   is_year_end()           — last bar of year
#   is_week_start()         — first bar of new week (ISO Monday)
#   is_week_end()           — last bar of week
#   is_opex()               — quarterly options expiration (3rd Friday of exp month)
#   is_month_start(offset=-1) — T-1 pre-positioning (one bar before boundary)
#
#   For advanced patterns (nth weekday, day_of_month, etc.):
#   use is_period_boundary(period=X, boundary=Y, ordinal=Z, day_anchor=W, ...)(timestamp)
#
# Calendar shift:
#   calendar_shift(src, "1M")  — shift by 1 month (calendar-aligned lookback)
#   calendar_shift(src, "1W")  — shift by 1 week
#   calendar_shift(src, "63D") — shift by 63 calendar days
#   calendar_shift(src, "-7D") — forward 7 days (negative = lead)
#
# Pattern: combine for seasonal filters
#   turn_of_year = month_of_year(Month.January) and week_of_month(WeekOfMonth.First)
#   rebalance    = is_month_start(offset=-1)
#   mom_12m      = close / calendar_shift(close, "12M")
```

### Test cases

```cpp
TEST_CASE("day_of_week monday") { /* day_of_week(DayOfWeek.Monday) → True on Mondays only */ }
TEST_CASE("quarter Q1") { /* quarter(Quarter.Q1) → True for Jan/Feb/Mar */ }
TEST_CASE("month_of_year december") { /* month_of_year(Month.December) → True in Dec */ }
TEST_CASE("is_month_start basic") { /* is_month_start() → True on first bar of each month */ }
TEST_CASE("is_month_end basic") { /* is_month_end() → True on last bar of each month */ }
TEST_CASE("is_opex quarterly") { /* is_opex() → True on third Friday of Mar/Jun/Sep/Dec */ }
TEST_CASE("is_month_start offset") { /* is_month_start(offset=-1) → True one bar before month start */ }
TEST_CASE("calendar_shift 1M") { /* calendar_shift(close, "1M") → value from ~21 trading days ago */ }
TEST_CASE("calendar_shift negative") { /* calendar_shift(close, "-1W") → forward shift (lead) */ }
```

### Acceptance criteria

- [ ] `day_of_week`, `month_of_year`, `quarter`, `week_of_month` in `BUILTIN_FUNCTIONS`
- [ ] All 4 calendar enums registered and appear in Lezer grammar
- [ ] Each calendar filter lowers to the correct impl node with the enum value forwarded
- [ ] All 9 period boundary builtins in `BUILTIN_FUNCTIONS`
- [ ] Each period boundary builtin lowers to `is_period_boundary` with correct option binding
- [ ] `offset` param correctly forwarded to impl node
- [ ] `is_opex` verified: month_anchor=3, ordinal=third, day_anchor=friday
- [ ] `calendar_shift` in `BUILTIN_FUNCTIONS`
- [ ] `calendar_shift(src, "1M")` → `calendar_shift(period="1M")(src)` produces identical output
- [ ] `is_period_boundary` remains as registered transform for advanced patterns (NOT internalUse)

---

## 5g — Trend Multi-Output Macros (7)

### `aroon`

Expansion: → `aroon(period=14)(h, l)` (single impl node, 2 outputs).

```
# aroon(high, low, period) → (aroon_up, aroon_down)
#   aroon_up, aroon_down = aroon(high, low, 14)
```

---

### `di`

⚠ Verify impl node ids for `plus_di` / `minus_di`.

```
# di(high, low, close, period) → (plus_di, minus_di)
#   plus_di, minus_di = di(high, low, close, 14)
```

---

### `dm`

⚠ Verify impl node ids for `plus_dm` / `minus_dm`.

```
# dm(high, low, period) → (plus_dm, minus_dm)
#   plus_dm, minus_dm = dm(high, low, 14)
```

---

### `vortex`

⚠ Verify impl node ids for `vortex_pos` / `vortex_neg`.

```
# vortex(high, low, close, period) → (vi_plus, vi_minus)
#   vi_plus, vi_minus = vortex(high, low, close, 14)
```

---

### `alligator`

⚠ Verify MA type used in alligator impl (SMMA/Wilder's). Expansion: 3 `ma` nodes at jaw/teeth/lips periods.

```
# alligator(source, jaw_period=13, teeth_period=8, lips_period=5) → (jaw, teeth, lips)
#   jaw, teeth, lips = alligator(close)
```

---

### `supertrend`

`direction` = +1 (uptrend) or −1 (downtrend).

```
# supertrend(high, low, close, atr_period=10, multiplier=3.0) → (line, direction)
#   line, direction = supertrend(high, low, close)
```

---

### `ichimoku`

```
# ichimoku(high, low, close, tenkan=9, kijun=26, senkou_b=52)
#          → (tenkan, kijun, span_a, span_b, chikou)
#   tenkan, kijun, span_a, span_b, chikou = ichimoku(high, low, close)
```

---

### Section 5g acceptance criteria

- [ ] All 7 names in `COMPILER_MACROS`
- [ ] All output names documented in grammar + match impl node output slot names
- [ ] `aroon`, `alligator`, `supertrend`, `ichimoku` impl node output arity verified
- [ ] `di`, `dm`, `vortex` impl node ids verified before implementing
- [ ] Grammar COMPILER MACROS section has production rule for each

---

## 5h — Momentum Multi-Output Macros (5)

### `macd`

```
# macd(source, fast=12, slow=26, signal=9) → (macd_line, signal_line, histogram)
#   macd_line, signal_line, hist = macd(close)
#   macd_line, signal_line, hist = macd(close, 5, 35, 5)
```

---

### `stoch`

```
# stoch(high, low, close, k=5, d=3) → (k, d)
#   k, d = stoch(high, low, close)
```

---

### `fisher`

⚠ Verify impl node id and output names.

```
# fisher(high, low, period) → (fisher_val, trigger)
#   fisher_val, trigger = fisher(high, low, 14)
```

---

### `msw`

⚠ Verify impl node id. (Market Sine Wave)

```
# msw(source, period) → (sine, lead)
#   sine, lead = msw(close, 14)
```

---

### `qqe`

⚠ Verify param names. (Quantitative Qualitative Estimation, 4 outputs)

```
# qqe(source, avg_period=14, smooth_period=5, width_factor=4.238)
#     → (qqe_line, histogram, upper_band, lower_band)
#   qqe_line, hist, upper, lower = qqe(close)
```

---

### Section 5h acceptance criteria

- [ ] `macd`, `stoch`, `fisher`, `msw`, `qqe` in `COMPILER_MACROS`
- [ ] `macd(close)` with defaults produces identical output to `macd(close, 12, 26, 9)`
- [ ] All output slot names verified against existing impl nodes

---

## 5i — Volatility Multi-Output Macros (7)

```
# bbands(source, period=20, stddev=2.0) → (upper, middle, lower)
#   upper, middle, lower = bbands(close)
#   width = bband_width(upper, middle, lower)

# donchian_channel(high, low, window=20) → (upper, middle, lower)
# keltner_channels(high, low, close, period=20, multiplier=2.0) → (upper, lower)
# acceleration_bands(high, low, close, period=20, multiplier=4.0) → (upper, middle, lower)
# chande_kroll_stop(high, low, close, p_period=10, q_period=9, multiplier=1.5) → (stop_short, stop_long)
# chandelier_exit(high, low, close, length=22, atr_length=22, multiplier=3.0) → (long_stop, short_stop, direction)
# elders_thermometer(high, low, period=20, buy_factor=0.5, sell_factor=2.0) → (therm, ema_therm, buy_signal, sell_signal)
```

### Section 5i acceptance criteria

- [ ] All 7 names in `COMPILER_MACROS`
- [ ] `bbands(close)` with defaults produces same output as `bbands(close, 20, 2.0)`
- [ ] `bband_percent`/`bband_width` work correctly with `bbands` outputs
- [ ] All output slot names verified against impl nodes before shipping

---

## 5j — Statistical / Math Macros (4)

```
# cs_first_last(source, cross_sectional=True | group_by=GroupBy.X) → (first, last)

# linear_fit(source, window=20) → (fit, upper_band, lower_band)   ⚠ verify impl id
#   fit, upper, lower = linear_fit(close, 20)

# half_life_ar1(source, window=60) → (half_life, zeta, std_err)   [Ornstein-Uhlenbeck]
#   hl, zeta, err = half_life_ar1(spread, 60)

# arg_minmax(source, expanding=False) → (max_idx, min_idx)         [expands to arg_max + arg_min]
#   max_i, min_i = arg_minmax(close)
```

---

## 5k — PriceAction Macros (7)

All implemented as single impl nodes. ⚠ Verify all output slot names before shipping.

```
# bos_choch(high, low, close, open, prev_high, prev_low, close_break=True)
#           → (bos_bull, bos_bear, choch_bull, choch_bear)

# fair_value_gap(open, high, low, close, join_consecutive=True)
#               → (fvg_bull, fvg_bear, fvg_top, fvg_bottom)

# order_blocks(open, high, low, close, volume, prev_close, close_mitigation=True)
#             → (ob_bull, ob_bear, ob_top, ob_bottom, ob_vol, ob_strength)

# liquidity(open, high, low, close, range_percent=0.1)
#           → (liq_high, liq_low, swept_high, swept_low)

# swing_highs_lows(high, low, swing_length=5) → (swing_high, swing_low)

# retracements(open, high, low, close) → (ret_50, ret_382, ret_618)

# previous_high_low(high, low, interval="1D", look_back=1)
#                  → (prev_high, prev_low, prev_open, prev_close)
```

### Section 5k acceptance criteria

- [ ] All 7 names in `COMPILER_MACROS`
- [ ] Output names match impl node slot names (verify before shipping)

---

## 5l — ControlFlow Macros (6)

```
# turn_of_month(days_before=2, days_after=2) → (start_signal, end_signal)
#   start, end = turn_of_month()

# cusum(source, threshold=1.0, drift=0.0, std_multiplier=1.0)
#       → (cusum_pos, cusum_neg, change_up, change_down, in_change)

# bar_gap(open, high, low, close, fill_percent=0.5, min_gap_size=0.002)
#         → (gap_up, gap_down, gap_size, gap_filled, gap_direction)

# session_gap(open, high, low, close, fill_percent=0.5)
#             → (gap_up, gap_down, gap_size, gap_filled, gap_direction)

# session_window(open, high, low, close, volume, timestamp, agg="1D")
#               → (open_s, high_s, low_s, close_s, volume_s, vwap_s, range_s, bar_count, session_id)
#               ⚠ verify impl node arity and param names

# pivot_point_sr(high, low, close) → (pp, r1, r2, r3, s1, s2, s3)   ⚠ verify impl node id
#   pp, r1, r2, r3, s1, s2, s3 = pivot_point_sr(high, low, close)
```

### Section 5l acceptance criteria

- [ ] All 6 names in `COMPILER_MACROS`
- [ ] `session_window` and `pivot_point_sr` impl arities verified before shipping
- [ ] `turn_of_month` expansion impl node id verified

---

## 5m — internalUse Designations

All transforms below gain `internalUse=true` in this phase. Existing scripts continue to function; these names are hidden from search and docs.

### MA impl nodes (stay for registered `ma` to reference)
None marked internalUse here — the underlying `ma` impl stays public (registered form still usable).

### Trend
| Transform id | Reason |
|---|---|
| `tsf` | Replaced by `linreg(src, N, LinRegType.Forecast)` — Phase 2 |
| `max` | Replaced by `agg(src, N, Agg.Max)` — Phase 2 |
| `min` | Replaced by `agg(src, N, Agg.Min)` — Phase 2 |

*(Already covered in earlier phases — listed for completeness.)*

### Statistical
| Transform id | Reason |
|---|---|
| `rolling_corr` | Replaced by `corr` builtin + `pair_stat` macro |
| `rolling_cov` | Replaced by `cov` builtin + `pair_stat` macro |
| `beta` (impl) | Replaced by `beta` builtin + `pair_stat` macro |
| `ewm_corr` | Replaced by `pair_stat(metrics=[Metric.ewm_correlation])` |
| `linreg` (impl) | Replaced by `linreg` builtin (Phase 2) |
| `linregslope` | Replaced by `linreg(src, N, LinRegType.Slope)` |
| `linregintercept` | Replaced by `linreg(src, N, LinRegType.Intercept)` |
| `cs_agg` | Replaced by `agg` builtin (Phase 2) |
| `cs_zscore` | Phase 4 — replaced by `zscore(cross_sectional=True)` |
| `cs_winsorize` | Phase 4 |
| `cs_rank` | Phase 4 |
| `cs_quantile` | Phase 4 |
| `cs_weighted_mean` | Phase 4 |
| `cs_rank_quantile` | Covered by Phase 4 rank |
| `cs_momentum` | Replaced by `select` + `agg` patterns |
| `cs_select` | Replaced by `select` macro (Phase 3) |

### Math
| Transform id | Reason |
|---|---|
| `returns` (Math impl) | Replaced by `returns` builtin (Phase 2) |
| `cumulative` (Math impl) | Replaced by `cum` builtin (Phase 2) |
| `stddev` | Replaced by `agg(src, N, Agg.Std)` |
| `var` | Replaced by `agg(src, N, Agg.Var)` |
| `sum` | Replaced by `agg(src, N, Agg.Sum)` |
| `mom` | Replaced by `diff` builtin (Phase 2) |

### DataSource
| Transform id | Reason |
|---|---|
| `common_reference_stocks` | Replaced by `reference_assets(stock(...))` (Phase 1) |
| `common_fx_pairs` | Replaced by `reference_assets(fx(...))` |
| `common_indices` | Replaced by `reference_assets(index(...))` |
| `common_reference_futures` | Replaced by `reference_assets(futures(...))` |
| `common_crypto_pairs` | Replaced by `reference_assets(crypto(...))` |
| `common_indicators` | Replaced by `macro_data` macro (Phase 3) |
| `market_data_source` | Replaced by `study_assets()` (Phase 1) |
| `extended_market_data_source` | Replaced by `study_assets(trading_hours=...)` |

### PriceAction
All 26 individual candlestick pattern transforms → `internalUse=true` (Phase 3, `candlestick_pattern` macro).

### ControlFlow
| Transform id | Reason |
|---|---|
| `crossunder` | Already a builtin — registered form redundant |
| `switch` | Replaced by `switch` builtin (Phase 5) |
| `is_asset_ref` | Replaced by `is_study_asset` builtin (Phase 5, renamed) |

### EventMarker
| Transform id | Reason |
|---|---|
| `event_marker` | Replaced by `marker` macro (Phase 3) |

### Statistical (Phase 4 promotions)
| Transform id | Reason |
|---|---|
| `zscore` | Replaced by `zscore` builtin with optional `cross_sectional` flag (Phase 4) |
| `winsorize` | Replaced by `winsorize` builtin with optional `cross_sectional` flag (Phase 4) |

---

## Phase 5 Complete `grammar_generator.cpp` additions

```cpp
// ── Phase 5 BUILTIN_FUNCTIONS additions ───────────────────────────────────
// 5a — MA type aliases (10)
"ema", "sma", "wma", "hma", "dema", "tema", "kama", "trima", "wilders", "zlema",

// 5b — single-series period (27)
"rsi", "trix", "cmo", "fosc", "roc", "rocr", "stochrsi",
"apo", "ppo",
"dpo", "vhf", "md",
"ulcer_index",
"percentrank", "streak_length", "nlargest", "nsmallest",
"hurst_exponent", "rolling_hurst_exponent",
"decay", "edecay", "stderr",
"forward_returns", "arg_max", "arg_min",
"highestbars", "lowestbars",

// 5c — multi-series period (22)
"cci", "mfi", "willr",
"atr", "natr", "cvi", "mass",
"adx", "adxr", "dx", "aroonosc",
"vwma", "qstick", "psl",
"ultosc", "psar",
"adosc", "kvo", "vosc",
"intraday_returns",
"rising", "falling",

// 5d — pair statistics (4, no enum)
"corr", "cov", "beta", "ewm_cov",

// 5e — no-param (20)
"tr", "price_distance", "bband_percent", "bband_width",
"ao", "bop",
"avgprice", "medprice", "typprice", "wcprice",
"obv", "ad", "emv", "nvi", "pvi", "marketfi", "wad",
"vwap",
"hold_until", "trade_count",
"switch", "is_study_asset",

// 5f — calendar filters (4, enum-gated)
"day_of_week", "month_of_year", "quarter", "week_of_month",
// 5f — period boundary decompositions (9)
"is_month_start", "is_month_end", "is_quarter_start", "is_quarter_end",
"is_year_start", "is_year_end", "is_week_start", "is_week_end", "is_opex",
// 5f — calendar shift (1)
"calendar_shift",

// ── Phase 5 COMPILER_MACROS additions ─────────────────────────────────────
// 5g — trend macros (7)
// "aroon", "di", "dm", "vortex", "alligator", "supertrend", "ichimoku",

// 5h — momentum macros (5)
// "macd", "stoch", "fisher", "msw", "qqe",

// 5i — volatility macros (7)
// "bbands", "donchian_channel", "keltner_channels", "acceleration_bands",
// "chande_kroll_stop", "chandelier_exit", "elders_thermometer",

// 5j — statistical/math macros (4)
// "cs_first_last", "linear_fit", "half_life_ar1", "arg_minmax",

// 5k — price action macros (7)
// "bos_choch", "fair_value_gap", "order_blocks", "liquidity",
// "swing_highs_lows", "retracements", "previous_high_low",

// 5l — control flow macros (6)
// "turn_of_month", "cusum", "bar_gap", "session_gap", "session_window",
// "pivot_point_sr",

// ── Phase 5 new enum registrations ────────────────────────────────────────
// RegisterEnumType("DayOfWeek",   {"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"});
// RegisterEnumType("Month",       {"January","February","March","April","May","June",
//                                   "July","August","September","October","November","December"});
// RegisterEnumType("Quarter",     {"Q1","Q2","Q3","Q4"});
// RegisterEnumType("WeekOfMonth", {"First","Second","Third","Fourth","Last"});
```

---

## Implementation order within Phase 5

Recommended: implement in sub-phases to allow progressive testing.

| Sub-phase | Contents | Risk |
|---|---|---|
| 5.1 | MA aliases (5a) | Low — trivial lowering |
| 5.2 | Single-series period builtins (5b) incl. arg_max/arg_min, forward_returns, apo/ppo | Low — same-name lowering, verify Timestamp return for arg_* |
| 5.3 | Multi-series period builtins (5c) + pair stats (5d) incl. ultosc, psar, adosc, kvo, vosc | Medium — verify input arity + param name mapping |
| 5.4 | No-param builtins (5e) incl. hold_until, trade_count | Low |
| 5.5 | Calendar filters (5f-i) + period boundary decompositions (5f-ii) + calendar_shift (5f-iii) | Medium — 9 builtins lower to is_period_boundary with different option combos |
| 5.6 | Trend macros (5g): aroon, alligator, supertrend, ichimoku first | Medium |
| 5.7 | Momentum macros (5h): macd, stoch | Low — well-known impl nodes |
| 5.8 | Volatility macros (5i): bbands first, then channel variants | Medium |
| 5.9 | Statistical/math macros (5j) + remaining macros (5k, 5l) | High — verify impl arities |
| 5.10 | All internalUse designations (5m) | Requires migration window |

---

## Phase 5 Acceptance Criteria

- [ ] All 99 builtin names added to `BUILTIN_FUNCTIONS` (10+27+22+4+22+14 = 99)
- [ ] All 36 macro names added to `COMPILER_MACROS`
- [ ] All 4 calendar enums registered (DayOfWeek, Month, Quarter, WeekOfMonth)
- [ ] All builtins produce identical output to their registered impl node forms
- [ ] All macros expand to correct impl nodes with correct output slot names verified
- [ ] All ~50 transforms in section 5m marked `internalUse=true`
- [ ] `is_period_boundary` remains public (NOT internalUse) for advanced patterns
- [ ] Type annotations verified: `arg_max`/`arg_min` → Timestamp, `highestbars`/`lowestbars` → Int, `hold_until` → Boolean, `trade_count` → Int
- [ ] Grammar file regenerates cleanly via `/dump-metadata`
- [ ] All existing Layer 3 tests still pass (no regressions)
- [ ] Representative test cases for each section pass
- [ ] ⚠ items (adx arity, di/dm impl ids, vwap anchoring, session_window arity, ultosc defaults, psar param mapping) resolved before shipping their respective sub-phases
