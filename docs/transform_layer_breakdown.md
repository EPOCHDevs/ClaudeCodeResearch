# EpochScript Transform ID → Layer Mapping

3 sections. L1/L2 show the lowered (runtime) ID and the builtin/alias to use.
L3 shows directly-callable transform IDs (two-stage syntax).

## L1/L2 — Lowered ID → Builtin / Alias

These runtime IDs are wrapped by builtins. Use the builtin name in EpochScript.

| Lowered (runtime) ID | Builtin / Alias | Syntax |
|---------------------|----------------|--------|
| `abs` | `abs` | L1 direct component fn(src) |
| `acos` | `acos` | L1 direct component fn(src) |
| `ad` | `ad` | L1 no-param |
| `adosc` | `adosc` | L1 fn(h,l,c,v,short,long) |
| `adx` | `adx` | L1 fn(inputs, N) |
| `adxr` | `adxr` | L1 fn(inputs, N) |
| `agg` | `agg` | L1 |
| `analyst_ratings` | `analyst_ratings` | L1 DataSource |
| `ao` | `ao` | L1 no-param |
| `apo` | `apo` | L1 fn(src, short, long) |
| `arg_max` | `arg_max` | L1 fn(src) |
| `arg_min` | `arg_min` | L1 fn(src) |
| `aroon` | `aroon` | L2 macro multi-output |
| `aroonosc` | `aroonosc` | L1 fn(inputs, N) |
| `asin` | `asin` | L1 direct component fn(src) |
| `atan` | `atan` | L1 direct component fn(src) |
| `atr` | `atr` | L1 fn(inputs, N) |
| `avgprice` | `avgprice` | L1 no-param |
| `balance_sheet` | `balance_sheet` | L1 DataSource |
| `barssince` | `barssince` | L1 |
| `bband_percent` | `bband_percent` | L1 no-param |
| `bband_width` | `bband_width` | L1 no-param |
| `bbands` | `bbands` | L2 macro multi-output |
| `beta` | `beta` | L1 beta(a, b, window=252) |
| `bop` | `bop` | L1 no-param |
| `bottom_k` | `select` | L2 select(..., direction=SelectDirection.Bottom) |
| `bottom_k_percent` | `select` | L2 (percent mode via cs_select L3) |
| `calendar_shift` | `calendar_shift` | L1 fn(src, duration) |
| `candlestick_pattern` | `candlestick_pattern` | L2 macro |
| `cash_flow` | `cash_flow` | L1 DataSource |
| `cci` | `cci` | L1 fn(inputs, N) |
| `ceil` | `ceil` | L1 direct component fn(src) |
| `cmo` | `cmo` | L1 fn(src, N) |
| `coalesce` | `nz / coalesce` | L1 |
| `common_crypto_pairs` | `reference_assets` | L1 (use reference_assets) |
| `common_fx_pairs` | `reference_assets` | L1 (use reference_assets) |
| `common_indicators` | `reference_assets` | L1 (use reference_assets) |
| `common_indices` | `reference_assets` | L1 (use reference_assets) |
| `common_reference_futures` | `reference_assets` | L1 (use reference_assets) |
| `common_reference_stocks` | `reference_assets` | L1 (use reference_assets) |
| `common_treasury_auctions` | `reference_assets` | L1 (use reference_assets) |
| `conditional_select_boolean` | `conditional_select` | L1 |
| `conditional_select_number` | `conditional_select` | L1 |
| `conditional_select_string` | `conditional_select` | L1 |
| `conditional_select_timestamp` | `conditional_select` | L1 |
| `cos` | `cos` | L1 direct component fn(src) |
| `cosh` | `cosh` | L1 direct component fn(src) |
| `crossany` | `crossany` | L1 direct component fn(a, b) |
| `crossover` | `crossover` | L1 direct component fn(a, b) |
| `crossunder` | `crossunder` | L1 direct component fn(a, b) |
| `cs_agg` | `agg` | L1 agg(src, AggregationType.X, cross_sectional=True) |
| `cs_momentum` | `momentum` | L1 momentum(src) |
| `cs_quantile` | `quantile` | L1 quantile(src, q=0.5) |
| `cs_rank` | `rank` | L1 rank(src, ascending=True) |
| `cs_rank_quantile` | `rank_quantile` | L1 rank_quantile(src, ascending=True) |
| `cs_select` | `select` | L2 select(src, n=K, direction=SelectDirection.Top) |
| `cs_weighted_mean` | `weighted_mean` | L1 weighted_mean(src, weights) |
| `cs_winsorize` | `winsorize` | L3 winsorize(cross_sectional=True)(src) |
| `cs_zscore` | `zscore` | L3 zscore(cross_sectional=True)(src) |
| `cumulative` | `cumulative` | L1 cumulative(src, agg=AggregationType.Sum) |
| `cvi` | `cvi` | L1 fn(inputs, N) |
| `day_of_week` | `day_of_week` | L1 calendar gate |
| `decay` | `decay` | L1 fn(src, N) |
| `di` | `di` | L2 macro → plus_di, minus_di |
| `dividends` | `dividends` | L1 DataSource |
| `dm` | `dm` | L2 macro → plus_dm, minus_dm |
| `donchian_channel` | `donchian_channel` | L2 macro multi-output |
| `downsample` | `resample` | L2 (internal) |
| `dpo` | `dpo` | L1 fn(src, N) |
| `dx` | `dx` | L1 fn(inputs, N) |
| `earnings` | `earnings` | L1 DataSource |
| `economic_calendar` | `economic_calendar` | L1 DataSource |
| `economic_indicators` | `economic_indicators` | L1 DataSource |
| `economic_revisions` | `economic_revisions` | L1 DataSource |
| `edecay` | `edecay` | L1 fn(src, N) |
| `emv` | `emv` | L1 no-param |
| `ewm_cov` | `ewm_cov` | L1 ewm_cov(a, b, span=20) |
| `exp` | `exp` | L1 direct component fn(src) |
| `extended_market_data_source` | `study_assets` | L1 (use study_assets) |
| `falling` | `falling` | L1 fn(src, N) |
| `ffill_boolean` | `ffill` | L1 |
| `ffill_day_boolean` | `ffill_day` | L1 |
| `ffill_day_number` | `ffill_day` | L1 |
| `ffill_day_string` | `ffill_day` | L1 |
| `ffill_day_timestamp` | `ffill_day` | L1 |
| `ffill_number` | `ffill` | L1 |
| `ffill_string` | `ffill` | L1 |
| `ffill_timestamp` | `ffill` | L1 |
| `fisher` | `fisher` | L2 macro → fisher, fisher_signal |
| `floor` | `floor` | L1 direct component fn(src) |
| `forward_returns` | `forward_returns` | L1 fn(src, N) |
| `fosc` | `fosc` | L1 fn(src, N) |
| `frac_diff` | `frac_diff` | L1 frac_diff(src, d=0.5, threshold=1e-5) |
| `highestbars` | `highestbars` | L1 fn(src, N) |
| `hold_until` | `hold_until` | L1 fn(enter, exit) |
| `hurst_exponent` | `hurst_exponent` | L1 fn(src, min_period) |
| `ichimoku` | `ichimoku` | L2 macro multi-output |
| `income_statement` | `income_statement` | L1 DataSource |
| `index` | `index` | L1 index() |
| `intraday_returns` | `intraday_returns` | L1 fn(c,o) |
| `ipos` | `ipos` | L1 DataSource |
| `is_asset_ref` | `is_study_asset` | L1 is_study_asset() |
| `is_null` | `isna / is_null` | L1 |
| `is_period_boundary` | `is_month_start / is_month_end / is_quarter_start / is_quarter_end / is_year_start / is_year_end / is_week_start / is_week_end / is_opex` | L1 period builtins |
| `is_valid` | `notna / is_valid` | L1 |
| `keltner_channels` | `keltner_channels` | L2 macro multi-output |
| `kvo` | `kvo` | L1 fn(c,v,short,long) |
| `lag_boolean` | `prev` | L1 |
| `lag_number` | `prev` | L1 prev(src) |
| `lag_string` | `prev` | L1 |
| `lag_timestamp` | `prev` | L1 |
| `linreg` | `linreg` | L1 fn(src, N) |
| `linregintercept` | `linregintercept` | L1 fn(src, N) |
| `linregslope` | `linregslope` | L1 fn(src, N) |
| `ln` | `ln` | L1 direct component fn(src) |
| `log10` | `log10` | L1 direct component fn(src) |
| `logical_and_not` | `logical_and_not` | L1 direct component fn(a, b) |
| `logical_xor` | `logical_xor` | L1 direct component fn(a, b) |
| `lowestbars` | `lowestbars` | L1 fn(src, N) |
| `ma` | `ema/sma/wma/hma/dema/tema/kama/trima/wilders/zlema` | L1 alias(src, N) |
| `macd` | `macd` | L2 macro multi-output |
| `macro_data` | `macro_data` | L2 macro |
| `market_data_source` | `study_assets` | L1 (use study_assets) |
| `marketfi` | `marketfi` | L1 no-param |
| `mass` | `mass` | L1 fn(inputs, N) |
| `md` | `md` | L1 fn(src, N) |
| `medprice` | `medprice` | L1 no-param |
| `mfi` | `mfi` | L1 fn(h,l,c,v,N) |
| `mom` | `diff` | L1 diff(src, N) |
| `month_of_year` | `month_of_year` | L1 calendar gate |
| `msw` | `msw` | L2 macro → msw_sine, msw_lead |
| `natr` | `natr` | L1 fn(inputs, N) |
| `nlargest` | `nlargest` | L1 fn(src, n) |
| `nsmallest` | `nsmallest` | L1 fn(src, n) |
| `nvi` | `nvi` | L1 no-param |
| `obv` | `obv` | L1 no-param |
| `pair_stat` | `pair_stat` | L2 macro |
| `percentrank` | `percentrank` | L1 fn(src, N) |
| `pivot_point_sr` | `pivot_point_sr` | L2 macro multi-output |
| `ppo` | `ppo` | L1 fn(src, short, long) |
| `price_distance` | `price_distance` | L1 no-param |
| `psar` | `psar` | L1 fn(h,l) |
| `psl` | `psl` | L1 fn(inputs, N) |
| `pvi` | `pvi` | L1 no-param |
| `qstick` | `qstick` | L1 fn(inputs, N) |
| `quarter` | `quarter` | L1 calendar gate |
| `resample` | `resample` | L2 macro → downsample/upsample |
| `returns` | `returns` | L1 returns(src, period, type) |
| `rising` | `rising` | L1 fn(src, N) |
| `roc` | `roc` | L1 fn(src, N) |
| `rocr` | `rocr` | L1 fn(src, N) |
| `rolling_corr` | `corr` | L1 corr(a, b, window=60) |
| `rolling_cov` | `cov` | L1 cov(a, b, window=60) |
| `rolling_hurst_exponent` | `rolling_hurst_exponent` | L1 fn(src, N) |
| `round` | `round` | L1 direct component fn(src) |
| `rsi` | `rsi` | L1 fn(src, N) |
| `short_interest` | `short_interest` | L1 DataSource |
| `short_volume` | `short_volume` | L1 DataSource |
| `sin` | `sin` | L1 direct component fn(src) |
| `sinh` | `sinh` | L1 direct component fn(src) |
| `splits` | `splits` | L1 DataSource |
| `sqrt` | `sqrt` | L1 direct component fn(src) |
| `stderr` | `stderr` | L1 fn(src, N) |
| `stoch` | `stoch` | L2 macro multi-output |
| `stochrsi` | `stochrsi` | L1 fn(src, N) |
| `str` | `str` | L1 |
| `streak_length` | `streak_length` | L1 fn(src) |
| `supertrend` | `supertrend` | L2 macro multi-output |
| `switch_boolean` | `switch` | L1 variadic |
| `switch_number` | `switch` | L1 variadic |
| `switch_string` | `switch` | L1 variadic |
| `switch_timestamp` | `switch` | L1 variadic |
| `tan` | `tan` | L1 direct component fn(src) |
| `tanh` | `tanh` | L1 direct component fn(src) |
| `ticker_events` | `ticker_events` | L1 DataSource |
| `todeg` | `todeg` | L1 direct component fn(src) |
| `top_k` | `select` | L2 select(..., direction=SelectDirection.Top) |
| `top_k_percent` | `select` | L2 (percent mode via cs_select L3) |
| `torad` | `torad` | L1 direct component fn(src) |
| `tr` | `tr` | L1 no-param |
| `trade_count` | `trade_count` | L1 fn() |
| `trix` | `trix` | L1 fn(src, N) |
| `trunc` | `trunc` | L1 direct component fn(src) |
| `tsf` | `tsf` | L1 fn(src, N) |
| `typprice` | `typprice` | L1 no-param |
| `ulcer_index` | `ulcer_index` | L1 fn(src, N) |
| `ultosc` | `ultosc` | L1 fn(h,l,c,short,med,long) |
| `upsample` | `resample` | L2 (internal) |
| `upsample_by_interpolate` | `resample` | L2 (internal) |
| `valuewhen_boolean` | `valuewhen` | L1 |
| `valuewhen_number` | `valuewhen` | L1 |
| `valuewhen_string` | `valuewhen` | L1 |
| `valuewhen_timestamp` | `valuewhen` | L1 |
| `vhf` | `vhf` | L1 fn(src, N) |
| `vidya` | `vidya` | L1 vidya(src, short_period=14, long_period=14, alpha=0.2) |
| `volatility` | `volatility` | L2 macro |
| `vortex` | `vortex` | L2 macro → plus_indicator, minus_indicator |
| `vosc` | `vosc` | L1 fn(v,short,long) |
| `vwap` | `vwap` | L1 no-param |
| `vwma` | `vwma` | L1 fn(inputs, N) |
| `wad` | `wad` | L1 no-param |
| `wcprice` | `wcprice` | L1 no-param |
| `week_of_month` | `week_of_month` | L1 calendar gate |
| `where_boolean` | `where` | L1 |
| `where_number` | `where` | L1 |
| `where_string` | `where` | L1 |
| `where_timestamp` | `where` | L1 |
| `willr` | `willr` | L1 fn(inputs, N) |

## L3 — Direct Transforms (`fn(opts)(inputs)`)

111 transforms grouped by package.

### Bars (2)

- `cs_bars` — Cross-Sectional Bars - ONE FOR ALL ASSETS
- `xy_bars` — XY Bars - ONE PER ASSET

### Cards (4)

- `cs_gauge` — Cross-Sectional Gauge - ONE FOR ALL ASSETS
- `cs_pie` — Cross-Sectional Pie Chart - ONE FOR ALL ASSETS
- `gauge` — Gauge Chart - ONE PER ASSET
- `pie` — Pie Chart - ONE PER ASSET

### Compute (27)

- `acceleration_bands` — Acceleration Bands
- `alligator` — Bill Williams Alligator
- `arg_minmax` — ArgMinMax (Timestamps)
- `bar_gap` — Bar Gap
- `chande_kroll_stop` — Chande Kroll Stop
- `chandelier_exit` — Chandelier Exit
- `cs_factor_analysis` — Cross-Sectional Factor Analysis
- `cs_first_last` — Cross-Sectional First/Last
- `cusum` — CUSUM Change Point Detector
- `datetime_diff` — Datetime Difference
- `datetime_extract` — Datetime Extract
- `elders_thermometer` — Elder's Market Thermometer
- `engle_granger` — Engle-Granger Cointegration
- `finance_ratio` — Financial Ratio
- `half_life_ar1` — Half-Life AR(1)
- `johansen` — Johansen Cointegration
- `kalman_filter` — Kalman Filter
- `linear_fit` — Linear Fit (Rolling OLS)
- `multi_linear_fit` — Multi-Linear Fit (Multi-Factor Regression)
- `price_profile` — Price Profile
- `qqe` — Quantitative Qualitative Estimation (QQE)
- `rolling_adf` — Rolling ADF Test
- `rolling_arima` — Rolling ARIMA Forecast
- `rolling_garch` — Rolling GARCH Volatility
- `volatility_estimator` — Volatility Estimator
- `winsorize` — Winsorize (Time-Series)
- `zscore` — Z-Score

### Distributions (4)

- `boxplot` — Boxplot - ONE PER ASSET
- `cs_boxplot` — Cross-Sectional Boxplot - ONE FOR ALL ASSETS
- `cs_histogram` — Cross-Sectional Histogram - ONE FOR ALL ASSETS
- `histogram` — Histogram - ONE PER ASSET

### EventMarkers (1)

- `event_marker` — Event Marker

### Execution (11)

- `cppi` — CPPI
- `kelly` — Kelly
- `long_and_short_zone` — Long & Short Zone
- `optimal_f` — Optimal f
- `position_size` — Position Size
- `risk_unit` — Risk Unit
- `rollover_policy` — Rollover Policy
- `stop_loss` — Stop Loss
- `take_profit` — Take Profit
- `tipp` — TIPP
- `trailing_stop` — Trailing Stop

### Heatmaps (2)

- `cs_heatmap` — Cross-Sectional Heatmap - ONE FOR ALL ASSETS
- `heatmap` — Heatmap - ONE PER ASSET

### Lines (4)

- `cs_labeled_lines` — Cross-Sectional Labeled Lines - ONE FOR ALL ASSETS
- `cs_lines` — Cross-Sectional Lines - ONE FOR ALL ASSETS
- `labeled_lines` — Labeled Lines - ONE PER ASSET
- `xy_lines` — XY Lines - ONE PER ASSET

### MachineLearning (13)

- `dbscan` — DBSCAN
- `hmm` — Hidden Markov Model
- `kmeans` — K-Means Clustering
- `lightgbm_classifier` — LightGBM Classifier
- `lightgbm_regressor` — LightGBM Regressor
- `logistic_l1` — Logistic L1
- `logistic_l2` — Logistic L2
- `ml_minmax` — ML Min-Max
- `ml_robust` — ML Robust
- `ml_zscore` — ML Z-Score
- `pca` — PCA
- `svr_l1` — SVR L1
- `svr_l2` — SVR L2

### MarketData (1)

- `futures_continuation` — Futures Continuation

### NLP (8)

- `keyword_count` — Keyword Count
- `keyword_match` — Keyword Match
- `keyword_score` — Keyword Score
- `string_case` — String Case
- `string_check` — String Check
- `string_contains` — String Contains
- `string_trim` — String Trim
- `topic_classify` — Topic Classify

### PortfolioAllocation (12)

- `black_litterman` — Black-Litterman
- `equal_weight` — Equal Weight
- `herc` — Hierarchical Equal Risk Contribution
- `hrp` — Hierarchical Risk Parity
- `inv_vol_weight` — Inverse Volatility Weight
- `max_diversification` — Maximum Diversification
- `max_sharpe` — Maximum Sharpe Ratio
- `min_cvar` — Minimum CVaR
- `min_semivariance` — Minimum Semivariance
- `min_variance` — Minimum Variance
- `risk_budgeting` — Risk Budgeting
- `risk_parity` — Risk Parity

### SMC (7)

- `bos_choch` — Break of Structure & Change of Character
- `fair_value_gap` — Fair Value Gap
- `liquidity` — Liquidity
- `order_blocks` — Order Blocks
- `previous_high_low` — Previous High Low
- `retracements` — Retracements
- `swing_highs_lows` — Swing Highs and Lows

### Scatter (8)

- `bubble` — Bubble Chart - ONE PER ASSET
- `cs_bubble` — Cross-Sectional Bubble Chart - ONE FOR ALL ASSETS
- `cs_labeled_bubble` — Cross-Sectional Labeled Bubble - ONE FOR ALL ASSETS
- `cs_labeled_scatter` — Cross-Sectional Labeled Scatter - ONE FOR ALL ASSETS
- `cs_scatter` — Cross-Sectional Scatter - ONE FOR ALL ASSETS
- `labeled_bubble` — Labeled Bubble - ONE PER ASSET
- `labeled_scatter` — Labeled Scatter - ONE PER ASSET
- `xy_scatter` — XY Scatter - ONE PER ASSET

### Sessions (5)

- `holiday` — Holiday Effect
- `is_period_boundary` — Is Period Boundary
- `session_gap` — Session Gap
- `session_window` — Session Window
- `turn_of_month` — Turn of Month

### Tables (2)

- `cs_summary_table` — Cross-Sectional Summary Table - ONE FOR ALL ASSETS
- `summary_table` — Summary Table - ONE PER ASSET

## Counts

- L1/L2 lowered IDs: 208
- L3 direct transforms: 111
- Total: 319

## Grammar ↔ Breakdown Cross-Reference

BUILTIN_FUNCTIONS (167 entry points) + COMPILER_MACROS (20 entry points) = 187 grammar entries.
These map to 208 runtime rows because:
- Type-suffixed variants: `where` → 4 rows, `switch` → 4 rows, `ffill` → 4 rows, `ffill_day` → 4 rows, `prev` → 4 rows, `valuewhen` → 4 rows, `conditional_select` → 4 rows (+21 extra rows)
- Cross-sectional aliases: `rank`→`cs_rank`, `quantile`→`cs_quantile`, `weighted_mean`→`cs_weighted_mean`, `momentum`→`cs_momentum`, `rank_quantile`→`cs_rank_quantile`, `agg`→`cs_agg`, `winsorize`→`cs_winsorize`, `zscore`→`cs_zscore` (+8)
- Select expansion: `select`→`top_k`/`bottom_k`/`top_k_percent`/`bottom_k_percent`/`cs_select` (+4)
- Reference asset aliases: 7 `common_*` rows
- Internal aliases: `market_data_source`, `extended_market_data_source`, `downsample`, `upsample`, `upsample_by_interpolate` (+5)
- Compiler specials: `index`, `is_asset_ref` (+2)
- Lowered renames: `diff`→`mom`, `returns`→`returns`, `corr`→`rolling_corr`, `cov`→`rolling_cov` (+2 extra runtime IDs)
- MA aliases (10 entry points) → 1 `ma` row (net −9)
- Period boundary (9 entry points) → 1 `is_period_boundary` row (net −8)
- nz/isna/notna aliases → merged into coalesce/is_null/is_valid rows (net −3)
