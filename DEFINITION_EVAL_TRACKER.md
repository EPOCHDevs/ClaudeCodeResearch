# Definition Evaluation Tracker

Rubric: [DEFINITION_RUBRIC.md](DEFINITION_RUBRIC.md)

---

## Progress Summary

| Category | Total | PASS | NEEDS_FIX |
|----------|-------|------|-----------|
| Research | 56 | 56 | 0 |
| Strategy | 17 | 17 | 0 |
| **Total** | **73** | **73** | **0** |

---

## Fixes Applied (2026-02-26)

All 40 previously failing definitions have been fixed.

### B1: Removed redundant timeframe= (13 definitions, 25 removals)

Removed `timeframe=` from `futures_continuation`, `market_data_source`, and transform nodes where it matched `global_timeframe`.

| Definition | Removals |
|-----------|----------|
| t1_02b_zb_cpi_intraday | 2 (MDS + futures_continuation) |
| t1_05b_gc_nfp_intraday | 2 (MDS + futures_continuation) |
| es_nfp_intraday_reaction | 2 (MDS + futures_continuation) |
| eurusd_nfp_reaction | 1 (MDS) |
| eurusd_nfp_volatility_decay | 1 (MDS) |
| eurusd_nfp_volatility_figure1 | 1 (MDS) |
| rs007_fx_monthly_seasonality | 1 (MDS) |
| quarterly_opex_momentum_reversal | 1 (MDS) |
| es_continuation_analysis | 7 (MDS + 6 futures_continuation) |
| sma_crossover_futures | 2 (MDS + futures_continuation) |
| fx_carry_trade | 2 (MDS + futures_continuation) |
| term_structure_commodities | 2 (MDS + futures_continuation) |

Note: rs010_eurusd_monthly_seasonality was already clean (no redundant timeframe=).

### C2: Added missing colors/dash styles (8 definitions)

| Definition | Fix |
|-----------|-----|
| ct_es_page1_auction_opening | Added `fill_color` (Green/Red) + `x_axis_format` to histograms |
| es_nfp_intraday_reaction | Added colors to 24 BarSeriesSpec across 4 charts |
| eurusd_nfp_reaction | Added colors to 10 BarSeriesSpec across 2 charts |
| eurusd_nfp_volatility_figure1 | Added `default_color`/`fill_color` to lines + bars |
| rs007_fx_monthly_seasonality | Added `fill_color` to 2 bar charts |
| rs010_eurusd_monthly_seasonality | Added `fill_color` to 3 bar charts |
| eng609_stock_bond_correlation_regime | Added `dash_style=DashStyle.Dash` to 6 reference lines |
| sp500_worst_performers | Added `fill_color`/`line_color` to boxplot |

### C3: Added color_by_value (1 definition)

| Definition | Fix |
|-----------|-----|
| tsla_sentiment_vs_fundamental_deterioration | Added `color_by_value=True` to 3 xy_bars with signed values |

### E1: Fixed manifest mismatch (1 definition)

| Definition | Fix |
|-----------|-----|
| tradingview_technicals_slv | Changed `data.assets` from TSLA-Stocks to SLV-Stocks |

### A1/A2: Converted card overloads to summary_table (23 definitions)

Reduced card cells from 138 to 39 (all blocks now 1-3 max). Added 25 summary_table() calls.

| Definition | Cards Before | Cards After | Tables Added |
|-----------|-------------|-------------|-------------|
| ct_es_volume_range_distributions | 10 | 1 | 1 |
| ct_ib_close_analysis | 5 | 1 | 1 |
| ct_session_structure | 21 | 2-3 | 3 |
| ib_20_session_analysis | 11 | 4 | 2 |
| volume_profile_confluence | 5 | 2 | 1 |
| volume_profile_multi_session_analysis | 21 | 3 | 4 |
| t2_03_nvda_earnings_volatility | 4 | 2 | 1 |
| t2_05_tsla_short_interest_earnings | 4 | 1 | 1 |
| aapl_valuation_multiples_peer_comparison | 5 | 2 | 1 |
| amzn_downside_rate_shock_scenario | 19 | 3 | 3 |
| msft_return_decomposition | 7 | 3 | 1 |
| tsla_sentiment_vs_fundamental_deterioration | 6 | 1 | 1 |
| eng600_currency_commodity_correlations | 12 | 1 | 1 |
| eng609_stock_bond_correlation_regime | 0 | 3 | 1 (added) |
| eurusd_nfp_volatility_figure1 | 6 | 2 | 1 |
| rs007_fx_monthly_seasonality | 6 | 3 | 1 |
| rs010_eurusd_monthly_seasonality | 8 | 3 | 1 |
| quarterly_opex_momentum_reversal | 5 | 3 | 1 |
| spy_morning_dip (research) | 8 | 3 | 1 |
| spy_morning_dip_window_analysis | 20 | 2 | 1 |
| spx_opening_range_breakout | 17 | 3 | 3 |
| nasdaq_ib_low_break_reversal | 11 | 3 | 2 |
| es_continuation_analysis | 0 | 2 | 2 (added) |

### D1/D2: Added stats diversity (15 definitions)

Added median, stddev, min/max alongside mean. Fixed aggregation types (Sum for counts, Last for current values, Mean/Median/Std for returns).

| Definition | Additions |
|-----------|-----------|
| t2_01_aapl_earnings_rating_double_event | Mean/Median/Std return tables + Min/Max extremes + Last cards |
| t2_02_tlt_cpi_fed_double_event | Mean/Median/Std return tables + Min/Max extremes + Last cards |
| t2_03_nvda_earnings_volatility | Mean/Median/Std vol + return tables + Min/Max + Last cards |
| t2_04_spy_claims_yield_curve | Mean/Median/Std return tables + Min/Max extremes + Last cards |
| t2_05_tsla_short_interest_earnings | Mean/Median/Std return tables + Min/Max extremes + Last cards |
| t2_06_aapl_gross_margin_drift | Mean/Median/Std return + margin tables + Min/Max + Last cards |
| nvda_earnings_revenue_acceleration | Mean/Median/Std/Count tables + deceleration histograms |
| tsla_sentiment_vs_fundamental_deterioration | Mean/Median/Std/Count post-event return table |
| msft_return_decomposition | Daily component stats + rate sensitivity tables |
| eng600_commodity_correlation_scatter | USD + SPY correlation stats (Mean/Median/Std/Last/Min/Max) |
| eng600_currency_commodity_correlations | Expanded from 3 to 5 columns (added Median/Std) |
| eng609_stock_bond_correlation_regime | Expanded SBC table + weekly return stats |
| eurusd_nfp_volatility_decay | Expanded from 1 to 5 rows (Mean/Median/Std/Max/Count) |
| spy_morning_dip (research) | Added Triggered/Median/StdDev rows to stats table |
| spy_morning_dip_window_analysis | Added return stats table (Mean/Median/Std/Min/Max) |

---

## All Definitions (73 PASS)

### Research (56)

| # | Definition | Category |
|---|-----------|----------|
| 1 | ct_es_overnight_ib_close | Microstructure |
| 2 | ct_es_page1_auction_opening | Microstructure |
| 3 | ct_es_page2_open_vs_prev_range | Microstructure |
| 4 | ct_es_volume_range_distributions | Microstructure |
| 5 | ct_ib_close_analysis | Microstructure |
| 6 | ct_opening_level_touch | Microstructure |
| 7 | ct_session_structure | Microstructure |
| 8 | ib_20_session_analysis | Microstructure |
| 9 | volume_profile_confluence | Microstructure |
| 10 | volume_profile_multi_session_analysis | Microstructure |
| 11 | volume_profile_session_analysis | Microstructure |
| 12 | vpoc_tracking_naked_vpoc | Microstructure |
| 13 | vwap_vpoc_convergence_analysis | Microstructure |
| 14 | t1_01_aapl_post_earnings_drift_surprise | Event Study T1 |
| 15 | t1_02_tlt_cpi_impact | Event Study T1 |
| 16 | t1_02b_zb_cpi_intraday | Event Study T1 |
| 17 | t1_03_spy_fed_rate_decision | Event Study T1 |
| 18 | t1_04_aapl_analyst_rating_drift | Event Study T1 |
| 19 | t1_05_gc_nfp_gold_impact | Event Study T1 |
| 20 | t1_05b_gc_nfp_intraday | Event Study T1 |
| 21 | t1_06_spy_dividend_exdate | Event Study T1 |
| 22 | t1_07_spy_yield_curve_inversion | Event Study T1 |
| 23 | t1_08_spy_ism_manufacturing | Event Study T1 |
| 24 | t1_08b_spy_ism_intraday | Event Study T1 |
| 25 | t1_09_eurusd_cpi_impact | Event Study T1 |
| 26 | t1_09b_eurusd_cpi_intraday | Event Study T1 |
| 27 | t1_10_tsla_short_volume_spike | Event Study T1 |
| 28 | t2_01_aapl_earnings_rating_double_event | Event Study T2 |
| 29 | t2_02_tlt_cpi_fed_double_event | Event Study T2 |
| 30 | t2_03_nvda_earnings_volatility | Event Study T2 |
| 31 | t2_04_spy_claims_yield_curve | Event Study T2 |
| 32 | t2_05_tsla_short_interest_earnings | Event Study T2 |
| 33 | t2_06_aapl_gross_margin_drift | Event Study T2 |
| 34 | aapl_valuation_multiples_peer_comparison | Fundamental |
| 35 | amzn_downside_rate_shock_scenario | Fundamental |
| 36 | msft_return_decomposition | Fundamental |
| 37 | nvda_earnings_revenue_acceleration | Fundamental |
| 38 | tsla_sentiment_vs_fundamental_deterioration | Fundamental |
| 39 | eng600_commodity_correlation_scatter | Correlation |
| 40 | eng600_currency_commodity_correlations | Correlation |
| 41 | eng609_stock_bond_correlation_regime | Correlation |
| 42 | es_nfp_intraday_reaction | NFP Intraday |
| 43 | eurusd_nfp_reaction | NFP Intraday |
| 44 | eurusd_nfp_volatility_decay | NFP Intraday |
| 45 | eurusd_nfp_volatility_figure1 | NFP Intraday |
| 46 | rs007_fx_monthly_seasonality | Seasonality |
| 47 | rs010_eurusd_monthly_seasonality | Seasonality |
| 48 | quarterly_opex_momentum_reversal | Seasonality |
| 49 | spy_morning_dip (research) | Intraday |
| 50 | spy_morning_dip_window_analysis | Intraday |
| 51 | spx_opening_range_breakout | Intraday |
| 52 | nasdaq_ib_low_break_reversal | Intraday |
| 53 | sp500_worst_performers | Screening |
| 54 | tradingview_technicals_slv | Technical |
| 55 | es_continuation_analysis | Other |
| 56 | fc_multi_timeframe_test | Other (compiler test) |

### Strategy (17)

| # | Definition | Category |
|---|-----------|----------|
| 57 | asset_class_trend_following | Trend Following |
| 58 | donchian_chandelier | Trend Following |
| 59 | sma_crossover_futures | Trend Following |
| 60 | currency_momentum | Cross-Sectional |
| 61 | low_volatility_factor | Cross-Sectional |
| 62 | post_earnings_drift | Cross-Sectional |
| 63 | sector_momentum | Cross-Sectional |
| 64 | short_interest_effect | Cross-Sectional |
| 65 | stock_reversal_within_sectors | Cross-Sectional |
| 66 | value_book_to_market | Cross-Sectional |
| 67 | fed_model | Macro Regime |
| 68 | fx_carry_trade | Macro Regime |
| 69 | sector_rotation_monetary_policy | Macro Regime |
| 70 | term_structure_commodities | Carry |
| 71 | dividend_month_anomaly | Seasonality |
| 72 | sector_seasonality_momentum | Seasonality |
| 73 | spy_morning_dip (strategy) | Intraday |
