# AMFX_16JUN22 — Chart Reproduction Tasks

Source: AMFX 16JUN22 newsletter by Brent Donnelly (Spectra Markets)
Theme: Central bank convergence — synchronized global hawkishness (Fed, SNB surprise 50bp, BOJ) could cap the dollar; crypto bear market flow dynamics and forced liquidation mechanics
Date: June 16, 2022

## Charts to Reproduce

### Task 1: AUDUSD Hourly Chart with Fed Event Annotations
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_audusd_fomc_pattern_research.json`
- **date_range:** 2022-03-15 to 2022-07-31
- **image_ref:** page_01_img_03.png
- **chart_type:** line (hourly intraday) with text annotations
- **data_sources:** AUDUSD hourly spot rate (Yahoo Finance or similar), FOMC meeting dates (April-June 2022)
- **what_makes_it_interesting:** Brilliantly shows how the Fed's forward guidance was not credible — AUDUSD "did exactly the same thing" at two consecutive FOMC meetings: ripped higher on dovish throwaway lines, peaked at 10pm NY, then reversed hard. Powell said "75bps isn't being actively considered" then hiked 75bps. A masterclass in annotated price charts that tell a narrative about central bank credibility.
- **reproduction_notes:** Daily timeframe approximation of original hourly chart. Shows AUDUSD close price + 20d MA + daily range volatility chart. The FOMC event patterns (May 4 and Jun 15 rallies/reversals) are visible at daily resolution. Original had hourly granularity with text annotations.

### Task 2: US 10-Year Yields vs. NYMEX Crude Overlay
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_yields_vs_crude_research.json`
- **date_range:** 2021-07-01 to 2022-07-15
- **image_ref:** page_02_img_00.png
- **chart_type:** dual-axis overlay (two line series)
- **data_sources:** US 10Y yield (FRED DGS10 or ^TNX), NYMEX Crude front-month (CL=F via Yahoo Finance)
- **what_makes_it_interesting:** Classic macro overlay showing yields and oil marching in lockstep during the inflation/tightening cycle. The thesis — aggressive tightening eventually breaks commodity prices and becomes good for bonds — is a foundational macro trading framework. Blue line (crude) and black line (yields) are highly correlated, and the author is watching for divergence.
- **reproduction_notes:** Z-score normalized overlay of CL-Futures (via futures_continuation) and DGS10 FRED yield. Three charts: (1) normalized overlay showing co-movement, (2) raw crude price, (3) raw 10Y yield. No dual-axis available so z-score normalization puts both on comparable scale.

### Task 3: BTC Cumulative Performance by Day of Month
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_btc_day_of_month_research.json`
- **date_range:** 2021-11-01 to 2022-06-30
- **image_ref:** page_03_img_00.png
- **chart_type:** line (day-of-month seasonal pattern)
- **data_sources:** Bitcoin daily prices (Yahoo Finance BTC-USD), compute average cumulative return by day of month from Nov 2021 to Jun 2022
- **what_makes_it_interesting:** Reveals the institutional flow signature in crypto during a bear market — steady selling throughout the month with a bounce in the final week from new allocations being deployed. The shape is striking: starts at 0%, grinds to -17% by day 25, then bounces. This is genuine alpha insight about flow dynamics.
- **reproduction_notes:** Bar chart of average daily return by day-of-month using xy_bars with Mean aggregation. Original showed cumulative returns; this shows daily returns which capture the same insight (negative returns early/mid month, positive at month end). Uses crypto_pairs(ticker='BTCUSD') for BTC data + datetime_extract for day-of-month grouping.

### Task 4: BTC Price with End-of-Month Periods Circled
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_btc_eom_bounce_research.json`
- **date_range:** 2021-11-01 to 2022-06-30
- **image_ref:** page_03_img_01.png
- **chart_type:** area chart (shaded) with circle annotations
- **data_sources:** Bitcoin daily prices (BTC-USD), calendar month boundaries
- **what_makes_it_interesting:** The companion chart to Task 3 — shows the actual BTC price from $69K peak to $21K crash with circles highlighting end-of-month bounce windows. Black circles = pattern working, red circles = pattern failing (LUNA/Celsius/3AC forced liquidations overwhelmed normal flows). The black-to-red circle transition tells the story of systemic contagion.
- **reproduction_notes:** Area chart with blue fill for BTC price + band series marking end-of-month periods (day >= 25). Second chart compares 5-day returns during EOM vs non-EOM periods. Uses is_band LineSeriesSpec feature for highlighting. Original had hand-drawn circles; we use EOM band overlay.

### Task 5: Weekly Crypto Asset Flows Bar Chart
- **status:** BLOCKED
- **image_ref:** page_04_img_00.png
- **chart_type:** bar chart (weekly flows)
- **data_sources:** CoinShares weekly digital asset fund flow data (publicly available reports), or approximate with Bitcoin ETF flow data
- **blocked_reason:** CoinShares weekly crypto fund flow data is proprietary and not available through FRED, Polygon, or any data source accessible via EpochScript transforms. No suitable proxy data source exists. Bitcoin ETFs did not exist until January 2024, so cannot approximate 2021-2022 flows.
- **what_makes_it_interesting:** Shows the anatomy of a bubble unwind through institutional flows. The massive 1447M inflow bar at the peak (late 2021) dwarfs everything else, followed by the slow transition from inflows to outflows. The delayed allocation pattern (brief surge Q1 2022 from approvals that were months in the pipeline) reveals how institutional money works with lag.
- **reproduction_notes:** Dark navy bars, positive above zero line, negative below. X-axis is week number (41 through 24, spanning Q4 2021 to Q2 2022). Y-axis US$m (-300 to +500), with the 1447 bar labeled as outlier. CoinShares attribution. Clean, simple bar chart.

### Task 6: EURJPY vs. HYG During Bear Stearns Crisis (2008)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_eurjpy_hyg_bear_stearns_research.json`
- **date_range:** 2007-11-01 to 2008-04-30
- **image_ref:** page_05_img_00.png
- **chart_type:** dual-axis overlay (candlestick + line) with text annotations
- **data_sources:** EURJPY daily (Yahoo Finance or FRED), HYG ETF daily prices, Feb-Apr 2008
- **what_makes_it_interesting:** A legendary forced-liquidation case study. When JPM bought Bear Stearns and liquidated ~10B EURJPY over 3 days, the pair decoupled completely from risk assets — HYG and risky assets V-bottomed while EURJPY kept getting hammered. The annotations tell the story of forced selling overriding all correlations. This is a timeless chart about market microstructure during crises.
- **reproduction_notes:** Z-score normalized overlay of EURJPY (via fx_pairs) and HYG (via market_data_source). Three charts: (1) normalized overlay showing divergence during forced liquidation, (2) raw EURJPY, (3) raw HYG. Uses zscore(window=60) for normalization. HYG data starts Apr 2007 so Nov 2007 start date gives sufficient warmup.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| (none) | All KEPT charts are worth reproducing — this issue is exceptionally rich in reproducible macro insights |
