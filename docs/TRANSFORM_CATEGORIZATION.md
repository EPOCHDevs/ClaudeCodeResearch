# Transform Categorization — Full Audit

Complete classification of all 299 transforms.
Basis for Phase 5 planning and the permanent BE mapping reference.

**Design principle:** Enums gate things agents could hallucinate names for.
Well-known indicators with documented params in the grammar need no enum — agents already know
`macd(close, short=12, long=26, signal=9)`. Grammar IS the contract.

---

## Categories

| Tag | Meaning |
|---|---|
| `[builtin]` | Single-stage, inputs-first, grammar-documented. Lowers to impl node. |
| `[macro]` | Single-stage, multi-output or variadic expansion. |
| `[registered]` | Two-stage `fn(opts)(inputs)`. Options-heavy or algorithm-selection. Stays as-is. |
| `[internal]` | Planned `internalUse=true` — impl node only, no user-facing form. |
| `[leave]` | Reporter, ML, Portfolio, Executor — no change needed. |

---

## Trend (26)

| id | in→out | Params | Decision | Notes |
|---|---|---|---|---|
| `ma` | 1→1 | period, type (10 values) | `[registered]` | Meta-form stays; individual type aliases become `[builtin]` below |
| `ema` | via ma | period only | `[builtin]` | `ema(src, 14)` → `ma(type=ema, period=14)(src)` |
| `sma` | via ma | period only | `[builtin]` | `sma(src, 20)` → `ma(type=sma, period=20)(src)` — alias alongside `agg(src,N,Agg.Mean)` |
| `wma` | via ma | period only | `[builtin]` | `wma(src, 14)` → `ma(type=wma, period=14)(src)` |
| `hma` | via ma | period only | `[builtin]` | `hma(src, 14)` → `ma(type=hma, period=14)(src)` |
| `dema` | via ma | period only | `[builtin]` | `dema(src, 14)` → `ma(type=dema, period=14)(src)` |
| `tema` | via ma | period only | `[builtin]` | `tema(src, 14)` → `ma(type=tema, period=14)(src)` |
| `kama` | via ma | period only | `[builtin]` | `kama(src, 14)` → `ma(type=kama, period=14)(src)` |
| `trima` | via ma | period only | `[builtin]` | `trima(src, 14)` → `ma(type=trima, period=14)(src)` |
| `wilders` | via ma | period only | `[builtin]` | `wilders(src, 14)` → `ma(type=wilders, period=14)(src)` |
| `zlema` | via ma | period only | `[builtin]` | `zlema(src, 14)` → `ma(type=zlema, period=14)(src)` |
| `vwma` | 2→1 | period only | `[builtin]` | `vwma(src, volume, 14)` → `vwma(period=14)(src, volume)` |
| `vidya` | 1→1 | short_period, long_period, **alpha=req** | `[registered]` | alpha is required — no universal default; stays two-stage |
| `adx` | 2→1 | period only | `[builtin]` | `adx(high, low, 14)` |
| `adxr` | 2→1 | period only | `[builtin]` | `adxr(high, low, 14)` |
| `dx` | 2→1 | period only | `[builtin]` | `dx(high, low, 14)` |
| `aroonosc` | 2→1 | period only | `[builtin]` | `aroonosc(high, low, 14)` |
| `dpo` | 1→1 | period only | `[builtin]` | `dpo(src, 14)` — Detrended Price Oscillator |
| `vhf` | 1→1 | period only | `[builtin]` | `vhf(src, 14)` — Vertical Horizontal Filter |
| `md` | 1→1 | period only | `[builtin]` | `md(src, 14)` — Mean Deviation |
| `avgprice` | 4→1 | none | `[builtin]` | `avgprice(o, h, l, c)` — no params at all |
| `medprice` | 2→1 | none | `[builtin]` | `medprice(high, low)` |
| `typprice` | 3→1 | none | `[builtin]` | `typprice(high, low, close)` |
| `wcprice` | 3→1 | none | `[builtin]` | `wcprice(high, low, close)` — Weighted Close |
| `aroon` | 2→2 | period only | `[macro]` | 2 outputs: aroon_up, aroon_down |
| `di` | 3→2 | period only | `[macro]` | 2 outputs: +DI, -DI |
| `dm` | 2→2 | period only | `[macro]` | 2 outputs: +DM, -DM |
| `vortex` | 3→2 | period only | `[macro]` | 2 outputs: VI+, VI- |
| `alligator` | 1→3 | jaw/teeth/lips periods | `[macro]` | 3 outputs. Params well-known, no enum needed — grammar docs it |
| `supertrend` | 3→2 | atr_period, multiplier | `[macro]` | 2 outputs. Grammar documents `supertrend(h,l,c, atr_period=10, multiplier=3)` |
| `ichimoku` | 3→5 | tenkan/kijun/senkou_b | `[macro]` | 5 outputs. Well-known params, no enum needed |
| `tsf` | 1→1 | period | `[internal]` | Replaced by `linreg(src, N, LinRegType.Forecast)` |
| `max` | 1→1 | period | `[internal]` | Replaced by `agg(src, N, Agg.Max)` |
| `min` | 1→1 | period | `[internal]` | Replaced by `agg(src, N, Agg.Min)` |
| `calendar_shift` | 1→1 | period (bar/day/week/month) | `[registered]` | Non-standard period type |
| `forward_returns` | 1→1 | period, return_type | `[registered]` | Forward-looking — special semantics, keep explicit |

MA enum values: `dema | ema | hma | kama | sma | tema | trima | wilders | wma | zlema` (10 types)
All 10 get builtin aliases. `ma` stays as registered for power users / explicit type selection.

---

## Momentum (25)

| id | in→out | Params | Decision | Notes |
|---|---|---|---|---|
| `rsi` | 1→1 | period only | `[builtin]` | `rsi(close, 14)` |
| `cci` | 3→1 | period only | `[builtin]` | `cci(high, low, close, 14)` |
| `mfi` | 4→1 | period only | `[builtin]` | `mfi(high, low, close, volume, 14)` |
| `willr` | 3→1 | period only | `[builtin]` | `willr(high, low, close, 14)` |
| `stochrsi` | 1→1 | period only | `[builtin]` | `stochrsi(close, 14)` |
| `trix` | 1→1 | period only | `[builtin]` | `trix(close, 14)` |
| `cmo` | 1→1 | period only | `[builtin]` | `cmo(close, 14)` — Chande Momentum Oscillator |
| `fosc` | 1→1 | period only | `[builtin]` | `fosc(close, 14)` — Forecast Oscillator |
| `roc` | 1→1 | period only | `[builtin]` | `roc(close, 14)` — the ×100 form; well-known name, keep as builtin |
| `rocr` | 1→1 | period only | `[builtin]` | `rocr(close, 14)` — ratio form (= `ratio` builtin, but keep alias) |
| `ao` | 2→1 | none | `[builtin]` | `ao(high, low)` — Awesome Oscillator, no params |
| `bop` | 4→1 | none | `[builtin]` | `bop(open, high, low, close)` — Balance of Power, no params |
| `psl` | 2→1 | period only | `[builtin]` | `psl(high, low, 12)` |
| `mom` | 1→1 | period | `[internal]` | Replaced by `diff(src, N)` |
| `macd` | 1→3 | short/long/signal periods | `[macro]` | `macd(close, 12, 26, 9)` — grammar documents positional defaults. 3 outputs. |
| `stoch` | 3→2 | k/d periods | `[macro]` | `stoch(high, low, close, k=5, d=3)` — 2 outputs |
| `fisher` | 2→2 | period only | `[macro]` | `fisher(high, low, 14)` — 2 outputs |
| `msw` | 1→2 | period only | `[macro]` | `msw(src, 14)` — Market Sine Wave, 2 outputs |
| `aroon` | 2→2 | period | `[macro]` | Listed under Trend above |
| `apo` | 1→1 | short_period, long_period | `[registered]` | Two independent periods — not a one-liner |
| `ppo` | 1→1 | short_period, long_period | `[registered]` | Two independent periods |
| `ultosc` | 3→1 | three periods | `[registered]` | Three independent periods |
| `qqe` | 1→4 | avg_period, smooth_period, width_factor | `[macro]` | 4 outputs, non-trivial params |
| `psar` | 2→1 | accel_step, accel_max | `[registered]` | Non-period acceleration params |
| `cs_momentum` | 1→1 | group_by | `[internal]` | Replaced by `select` + `agg` patterns |
| `cs_select` | 1→1 | direction, mode, k, group_by | `[internal]` | Replaced by `select` macro |

---

## Volatility (20)

| id | in→out | Params | Decision | Notes |
|---|---|---|---|---|
| `atr` | 3→1 | period only | `[builtin]` | `atr(high, low, close, 14)` |
| `natr` | 3→1 | period only | `[builtin]` | `natr(high, low, close, 14)` — Normalized ATR |
| `tr` | 3→1 | none | `[builtin]` | `tr(high, low, close)` — True Range, no params |
| `cvi` | 2→1 | period only | `[builtin]` | `cvi(high, low, 14)` — Chaikin Volatility |
| `mass` | 2→1 | period only | `[builtin]` | `mass(high, low, 14)` — Mass Index |
| `ulcer_index` | 1→1 | period (+ minor use_sum) | `[builtin]` | `ulcer_index(close, 14)` — use_sum default False is fine |
| `price_distance` | 4→1 | none | `[builtin]` | `price_distance(o, h, l, c)` — no params |
| `bband_percent` | 3→1 | none | `[builtin]` | `bband_percent(upper, mid, lower)` — takes bands as inputs |
| `bband_width` | 3→1 | none | `[builtin]` | `bband_width(upper, mid, lower)` — takes bands as inputs |
| `bbands` | 1→3 | period, stddev | `[macro]` | `bbands(close, 20, 2.0)` — 3 outputs: upper, mid, lower |
| `donchian_channel` | 2→3 | window only | `[macro]` | `donchian_channel(high, low, 20)` — 3 outputs |
| `keltner_channels` | 3→2 | roll_period, band_multiplier | `[macro]` | `keltner_channels(h, l, c, 20, 2.0)` — 2 outputs |
| `acceleration_bands` | 3→3 | period, multiplier | `[macro]` | 3 outputs |
| `chande_kroll_stop` | 3→2 | p_period, q_period, multiplier | `[macro]` | 2 outputs |
| `chandelier_exit` | 3→3 | length, atr_length, multiplier | `[macro]` | 3 outputs |
| `elders_thermometer` | 2→4 | period, buy_factor, sell_factor | `[macro]` | 4 outputs |
| `volatility` | 1→1 | period | `[internal]` | Replaced by `volatility(src, method=VolMethod.annualized)` macro |
| `basic_volatility` | 1→1 | type, period | `[internal]` | Replaced by `volatility` macro |
| `volatility_estimator` | 4→1 | type (garman_klass/etc), period | `[registered]` | OHLC input + method selection; stays |
| `rolling_garch` | 1→7 | p, q, distribution, window | `[registered]` | Hyperparameter-heavy, 7 outputs |

---

## Statistical (35)

| id | in→out | Params | Decision | Notes |
|---|---|---|---|---|
| `rolling_corr` | 2→1 | window, method | `[internal]` | Replaced by `pair_stat` macro AND `corr` builtin |
| `rolling_cov` | 2→1 | window | `[internal]` | Replaced by `pair_stat` macro AND `cov` builtin |
| `beta` | 2→1 | window | `[internal]` | Replaced by `pair_stat` macro AND `beta` builtin |
| `ewm_corr` | 2→1 | span | `[internal]` | Replaced by `pair_stat` macro |
| `ewm_cov` | 2→1 | span | `[builtin]` | `ewm_cov(a, b, 20)` — not in pair_stat yet; add as builtin or add `Metric.ewm_covariance` to pair_stat |
| `corr` | via rolling_corr | window | `[builtin]` | NEW — `corr(a, b, 60)` → `rolling_corr(window=60)(a, b)`. No enum needed. |
| `cov` | via rolling_cov | window | `[builtin]` | NEW — `cov(a, b, 60)` → `rolling_cov(window=60)(a, b)`. No enum needed. |
| `percentrank` | 1→1 | period only | `[builtin]` | `percentrank(src, 14)` |
| `hurst_exponent` | 1→1 | min_period only | `[builtin]` | `hurst_exponent(src)` or `hurst_exponent(src, 20)` |
| `rolling_hurst_exponent` | 1→1 | window only | `[builtin]` | `rolling_hurst_exponent(src, 100)` |
| `streak_length` | 1→1 | direction (up/down) | `[builtin]` | `streak_length(src)` or `streak_length(src, direction=up)` — direction has clear default |
| `nlargest` | 1→1 | n | `[builtin]` | `nlargest(src, 10)` — top N rolling values |
| `nsmallest` | 1→1 | n | `[builtin]` | `nsmallest(src, 10)` |
| `zscore` | 1→1 | window | `[registered]` | Phase 4 — gains `cross_sectional` flag |
| `winsorize` | 1→1 | lower/upper limits | `[registered]` | Phase 4 |
| `cs_zscore` | 1→1 | group_by | `[internal]` | Phase 4 — replaced by `zscore(cross_sectional=True)` |
| `cs_winsorize` | 1→1 | lower/upper | `[internal]` | Phase 4 |
| `cs_rank` | 1→1 | ascending | `[internal]` | Phase 4 — `rank(cross_sectional=True)` |
| `cs_quantile` | 1→1 | q, group_by | `[internal]` | Phase 4 — `quantile(cross_sectional=True)` |
| `cs_weighted_mean` | 2→1 | group_by | `[internal]` | Phase 4 — `weighted_mean(cross_sectional=True)` |
| `cs_rank_quantile` | 1→1 | ascending | `[internal]` | Covered by Phase 4 rank |
| `cs_first_last` | 1→2 | group_by | `[macro]` | 2 outputs (first, last) — `first_last(cross_sectional=True)` |
| `cs_agg` | 1→1 | type, group_by | `[internal]` | Phase 2 — replaced by `agg` builtin |
| `linreg` | 1→1 | period | `[internal]` | Replaced by `linreg(src, N)` builtin |
| `linregslope` | 1→1 | period | `[internal]` | Replaced by `linreg(src, N, LinRegType.Slope)` |
| `linregintercept` | 1→1 | period | `[internal]` | Replaced by `linreg(src, N, LinRegType.Intercept)` |
| `linear_fit` | 2→3 | window | `[macro]` | 3 outputs (fit, upper, lower band) |
| `half_life_ar1` | 1→3 | window | `[macro]` | 3 outputs — Ornstein-Uhlenbeck half-life |
| `engle_granger` | 2→9 | window, lag, significance | `[registered]` | 9 outputs, complex cointegration test |
| `johansen` | 1→6 | num_vars, window, lag, det_order | `[registered]` | 6 outputs, complex |
| `rolling_adf` | 1→6 | window, lag, significance, deterministic | `[registered]` | 6 outputs |
| `rolling_arima` | 1→7 | p,d,q, window, step | `[registered]` | Hyperparameter-heavy |
| `kalman_filter` | 1→9 | model_type, noise params | `[registered]` | Algorithm selection + noise tuning |
| `multi_linear_fit` | 2→4 | num_vars, window | `[registered]` | Multiple regression |
| `finance_ratio` | 18→1 | ratio_type (req), period | `[registered]` | 18 inputs, complex |
| `frac_diff` | 1→1 | d (req), threshold | `[registered]` | d is required, fractional differentiation |
| `cs_factor_analysis` | 2→4 | method, min_obs, ir_window | `[registered]` | Complex |

**Key decision — `corr` and `cov` as builtins (no enum gate):**
`corr(a, b, 60)` and `cov(a, b, 60)` are universally known one-liners.
`pair_stat` macro is still useful for multi-metric extraction in one call.
They coexist: builtin for single metric, macro for batched multi-metric.

---

## Momentum — Math (11, Math category)

| id | in→out | Params | Decision | Notes |
|---|---|---|---|---|
| `returns` (Math) | 1→1 | period, type | `[internal]` | Impl node for `returns` builtin. Types: simple, log, cumulative, directional, monetary |
| `cumulative` | 2→1 | agg (AggType), q, ddof, bias | `[internal]` | Impl node for `cum` builtin |
| `stddev` | 1→1 | period | `[internal]` | Replaced by `agg(src, N, Agg.Std)` |
| `var` | 1→1 | period | `[internal]` | Replaced by `agg(src, N, Agg.Var)` |
| `sum` | 1→1 | period | `[internal]` | Replaced by `agg(src, N, Agg.Sum)` |
| `decay` | 1→1 | period | `[builtin]` | `decay(src, 14)` — linear decay weighting |
| `edecay` | 1→1 | period | `[builtin]` | `edecay(src, 14)` — exponential decay weighting |
| `stderr` | 1→1 | period | `[builtin]` | `stderr(src, 14)` — rolling standard error |
| `arg_max` | 1→1 | expanding bool | `[registered]` | expanding=True/False changes semantics meaningfully |
| `arg_min` | 1→1 | expanding bool | `[registered]` | Same |
| `arg_minmax` | 1→2 | expanding bool | `[macro]` | 2 outputs |

---

## Volume (12)

| id | in→out | Params | Decision | Notes |
|---|---|---|---|---|
| `obv` | 2→1 | none | `[builtin]` | `obv(close, volume)` — On Balance Volume |
| `ad` | 4→1 | none | `[builtin]` | `ad(high, low, close, volume)` — A/D Line |
| `emv` | 3→1 | none | `[builtin]` | `emv(high, low, volume)` — Ease of Movement |
| `nvi` | 2→1 | none | `[builtin]` | `nvi(close, volume)` — Negative Volume Index |
| `pvi` | 2→1 | none | `[builtin]` | `pvi(close, volume)` — Positive Volume Index |
| `marketfi` | 3→1 | none | `[builtin]` | `marketfi(high, low, volume)` — Market Facilitation Index |
| `wad` | 3→1 | none | `[builtin]` | `wad(high, low, close)` — Williams A/D |
| `vwap` | 0→1 | none | `[builtin]` | `vwap()` — datasource-like, no inputs or params |
| `trade_count` | 0→1 | none | `[leave]` | Datasource — stays |
| `adosc` | 4→1 | short_period, long_period | `[registered]` | Two independent periods |
| `kvo` | 4→1 | short_period, long_period | `[registered]` | Two independent periods — Klinger Volume Oscillator |
| `vosc` | 1→1 | short_period, long_period | `[registered]` | Two independent periods |

---

## PriceAction (34)

| id | in→out | Params | Decision | Notes |
|---|---|---|---|---|
| All 26 candlestick patterns | 4→1 each | body/wick thresholds (req) | `[internal]` | Phase 3 — replaced by `candlestick_pattern` macro |
| `qstick` | 2→1 | period only | `[builtin]` | `qstick(open, close, 14)` |
| `bos_choch` | 6→4 | close_break bool | `[macro]` | Break of Structure / Change of Character — 4 outputs |
| `fair_value_gap` | 4→4 | join_consecutive bool | `[macro]` | 4 outputs |
| `order_blocks` | 6→6 | close_mitigation bool | `[macro]` | 6 outputs |
| `liquidity` | 4→4 | range_percent | `[macro]` | 4 outputs |
| `swing_highs_lows` | 2→2 | swing_length | `[macro]` | 2 outputs |
| `retracements` | 4→3 | none | `[macro]` | 3 outputs — Fibonacci-style |
| `previous_high_low` | 2→4 | interval, type | `[macro]` | 4 outputs |

**Candlestick patterns — note on options:**
All 26 have body/wick threshold options marked `required`. In practice agents never set these —
they use the defaults. The `candlestick_pattern` macro should call each impl node with no options
(compiler uses defaults). This is already the plan.

---

## ControlFlow (23)

| id | in→out | Params | Decision | Notes |
|---|---|---|---|---|
| `barssince` | 1→1 | none | `[internal]` | Phase 2 — becomes builtin (same name) |
| `valuewhen` | 2→1 | occurrence | `[internal]` | Phase 2 — becomes builtin (same name) |
| `crossunder` | 2→1 | none | `[leave]` | Already in BUILTIN_FUNCTIONS |
| `rising` | 1→1 | length only | `[builtin]` | `rising(src, 1)` — Boolean: is src rising? |
| `falling` | 1→1 | length only | `[builtin]` | `falling(src, 1)` — Boolean: is src falling? |
| `day_of_week` | 0→1 | weekday enum | `[builtin]` | `day_of_week(Monday)` — calendar filter |
| `month_of_year` | 0→1 | month enum | `[builtin]` | `month_of_year(January)` |
| `quarter` | 0→1 | quarter enum | `[builtin]` | `quarter(Q1)` |
| `week_of_month` | 0→1 | week enum | `[builtin]` | `week_of_month(First)` |
| `hold_until` | 2→1 | none | `[registered]` | Control flow logic, stays |
| `switch` | 2→1 | none | `[registered]` | Control flow logic, stays |
| `turn_of_month` | 0→2 | days_before, days_after | `[macro]` | 2 outputs (start signal, end signal) |
| `is_period_boundary` | 1→1 | many options | `[registered]` | Options-heavy |
| `cusum` | 1→5 | threshold, drift, std_multiplier | `[macro]` | 5 outputs — CUSUM change detection |
| `bar_gap` | 4→5 | fill_percent, min_gap_size | `[macro]` | 5 outputs |
| `session_gap` | 4→5 | fill_percent | `[macro]` | 5 outputs |
| `session_window` | 6→9 | agg | `[macro]` | 9 outputs |
| `holiday` | 0→1 | calendar, days_before/after | `[registered]` | Calendar-dependent options |
| `is_asset_ref` | 0→1 | many filters | `[registered]` | Options-heavy asset filter |
| `keyword_match` | 1→1 | keywords (req) | `[registered]` | Required param |
| `string_check` | 1→1 | operation enum | `[registered]` | Stays |
| `string_contains` | 1→1 | operation, pattern | `[registered]` | Stays |
| `asset_spec` | 0→7 | ticker, asset class | `[registered]` | Datasource-like |

---

## DataSource (30)

| id | Decision | Notes |
|---|---|---|
| `market_data_source` | `[internal]` | Phase 1 — becomes `study_assets()` |
| `extended_market_data_source` | `[internal]` | Phase 1 — routed via `study_assets(trading_hours=...)` |
| `common_reference_stocks` | `[internal]` | Replaced by `reference_assets(stock(...))` macro |
| `common_fx_pairs` | `[internal]` | Replaced by `reference_assets(fx(...))` macro |
| `common_indices` | `[internal]` | Replaced by `reference_assets(index(...))` macro |
| `common_reference_futures` | `[internal]` | Replaced by `reference_assets(futures(...))` macro |
| `common_crypto_pairs` | `[internal]` | Replaced by `reference_assets(crypto(...))` macro |
| `common_indicators` | `[internal]` | Phase 3 — replaced by `macro_data` macro |
| `reference_stocks` | `[registered]` | Flexible non-common ticker access — stays |
| `reference_futures` | `[registered]` | Stays |
| `fx_pairs` | `[registered]` | Stays |
| `indices` | `[registered]` | Stays |
| `crypto_pairs` | `[registered]` | Stays |
| `earnings` | `[leave]` | Intent-named, stays |
| `analyst_ratings` | `[leave]` | Stays |
| `dividends` | `[leave]` | Stays |
| `news` | `[leave]` | Stays |
| `cs_news` | `[leave]` | Stays |
| `income_statement` | `[leave]` | Stays |
| `balance_sheet` | `[leave]` | Stays |
| `cash_flow` | `[leave]` | Stays |
| `economic_indicators` | `[leave]` | Stays |
| `economic_calendar` | `[leave]` | Stays |
| `economic_revisions` | `[leave]` | Stays |
| `ipos` | `[leave]` | Stays |
| `short_interest` | `[leave]` | Stays |
| `short_volume` | `[leave]` | Stays |
| `splits` | `[leave]` | Stays |
| `ticker_events` | `[leave]` | Stays |
| `common_treasury_auctions` | `[leave]` | Stays |

---

## Indicator (5)

| id | in→out | Params | Decision | Notes |
|---|---|---|---|---|
| `highestbars` | 1→1 | period | `[builtin]` | `highestbars(src, 14)` — bars since highest value |
| `lowestbars` | 1→1 | period | `[builtin]` | `lowestbars(src, 14)` — bars since lowest value |
| `intraday_returns` | 2→1 | return_type | `[builtin]` | `intraday_returns(close, open)` — return_type default simple |
| `pivot_point_sr` | 3→7 | none | `[macro]` | 7 outputs — Pivot Point support/resistance levels |
| `price_profile` | 4→6 | window, tick_size, value_area_pct | `[registered]` | Volume Profile — options-heavy |

---

## DataPrep (4)

| id | Decision | Notes |
|---|---|---|
| `downsample` | `[internal]` | Phase 1 — replaced by `resample` macro |
| `upsample` | `[internal]` | Phase 1 — replaced by `resample` macro |
| `upsample_by_interpolate` | `[registered]` | Interpolation method — different from ffill/bfill upsample, stays |
| `futures_continuation` | `[registered]` | Complex rollover logic, stays |

---

## EventMarker (1)

| id | Decision | Notes |
|---|---|---|
| `event_marker` | `[internal]` | Phase 3 — replaced by `marker` macro |

---

## Reporter (26), ML (13), Portfolio (12), Executor (11), Utility (10)

All `[leave]` — no changes to these categories.

**Reporter cs_*** — explicitly NOT scope variants (different chart types). Stay as-is.
**ML** — unique hyperparameter surfaces per algorithm. Stay as-is.
**Portfolio** — complex optimization. Stay as-is.
**Executor** — position sizing logic. Stay as-is.
**Utility** — `datetime_extract`, `keyword_score`, etc. Stay as-is.

---

## Full changeset summary

### Phase 5 — Classic indicators & TA builtins (NEW)

**New builtins from Trend MA aliases (10):**
`ema`, `sma`, `wma`, `hma`, `dema`, `tema`, `kama`, `trima`, `wilders`, `zlema`

**New builtins from Trend (single-output, period-only or no-param):**
`vwma`, `adx`, `adxr`, `dx`, `aroonosc`, `dpo`, `vhf`, `md`, `avgprice`, `medprice`, `typprice`, `wcprice`

**New builtins from Momentum:**
`rsi`, `cci`, `mfi`, `willr`, `stochrsi`, `trix`, `cmo`, `fosc`, `roc`, `rocr`, `ao`, `bop`, `psl`

**New builtins from Volatility:**
`atr`, `natr`, `tr`, `cvi`, `mass`, `ulcer_index`, `price_distance`, `bband_percent`, `bband_width`

**New builtins from Statistical:**
`corr`, `cov`, `percentrank`, `hurst_exponent`, `rolling_hurst_exponent`, `streak_length`, `nlargest`, `nsmallest`

**New builtins from Math:**
`decay`, `edecay`, `stderr`

**New builtins from Volume (no params):**
`obv`, `ad`, `emv`, `nvi`, `pvi`, `marketfi`, `wad`, `vwap`

**New builtins from PriceAction:**
`qstick`

**New builtins from ControlFlow:**
`rising`, `falling`, `day_of_week`, `month_of_year`, `quarter`, `week_of_month`

**New builtins from Indicator:**
`highestbars`, `lowestbars`, `intraday_returns`

**New macros from Trend:**
`aroon`, `di`, `dm`, `vortex`, `alligator`, `supertrend`, `ichimoku`

**New macros from Momentum:**
`macd`, `stoch`, `fisher`, `msw`, `qqe`

**New macros from Volatility:**
`bbands`, `donchian_channel`, `keltner_channels`, `acceleration_bands`, `chande_kroll_stop`, `chandelier_exit`, `elders_thermometer`

**New macros from Statistical:**
`cs_first_last`, `linear_fit`, `half_life_ar1`

**New macros from Math:**
`arg_minmax`

**New macros from PriceAction:**
`bos_choch`, `fair_value_gap`, `order_blocks`, `liquidity`, `swing_highs_lows`, `retracements`, `previous_high_low`

**New macros from ControlFlow:**
`turn_of_month`, `cusum`, `bar_gap`, `session_gap`, `session_window`

**New macros from Indicator:**
`pivot_point_sr`

**Additional internalUse (beyond Phases 1-4):**
`cs_momentum`, `cs_select`, `cs_rank_quantile`, `linreg`(impl), `linregslope`, `linregintercept`,
`rolling_corr`, `rolling_cov`, `beta`, `ewm_corr`,
`returns`(Math impl), `cumulative`(Math impl),
all 26 candlestick pattern impls,
`common_reference_stocks`, `common_fx_pairs`, `common_indices`, `common_reference_futures`, `common_crypto_pairs`

---

## Phase 5 counts

| Type | Count |
|---|---|
| New builtins | ~70 |
| New macros | ~25 |
| Additional internalUse | ~50 |

**After all phases: agents have ~100 clean single-stage names + the existing 20 builtins + 7 Phase 1-3 macros = ~127 total public Layer 1/2 constructs, replacing ~170+ fragmented impl nodes.**
