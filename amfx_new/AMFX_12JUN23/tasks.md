# AMFX_12JUN23 — Chart Reproduction Tasks

Source: AMFX 12JUN23 newsletter by Brent Donnelly (Spectra Markets)
Theme: EURGBP rate differential reconvergence, USDCAD vs. oil setup, NASDAQ quarterly OPEX reversal pattern
Date: June 12, 2023

## Charts to Reproduce

### Task 1: EURGBP vs. Germany/UK 10-Year Rate Differential
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_eurgbp_rate_diff_research.json`
- **image_ref:** page_01_img_02.png (top half)
- **chart_type:** dual-axis overlay line chart
- **data_sources:** EURGBP spot (^EURGBP-FX from Polygon), German 10-year Bund yield (FRED: IRLTLT01DEM156N, monthly), UK 10-year Gilt yield (FRED: IRLTLT01GBM156N, monthly). Spread = Germany minus UK.
- **date_range:** 2023-03-01 to 2023-06-30
- **notes:** German and UK 10Y yields are only available monthly on FRED (not daily like the TradingView chart). Forward-filled to daily resolution. The rate differential trend is still visible but appears as steps rather than smooth daily movement. Charts render correctly with 2 xy_lines charts + summary table.
- **what_makes_it_interesting:** Classic FX-rates dislocation trade visualization. The divergence after UK CPI release (annotated with red arrow) and subsequent reconvergence tells a complete trade story — the "sell gilts, sell GBP" knee-jerk faded as higher UK yields attracted capital. The dual-axis overlay is the bread-and-butter of macro FX analysis. The red annotation line for "UK CPI release" adds narrative clarity.
- **reproduction_notes:** Two overlaid lines on dual y-axes. EURGBP on right axis (~0.85-0.90 range), rate differential on left axis. Time range Mar-Jun 2023. Blue/dark line for rate diff, lighter line for EURGBP. Red annotation arrow marking "UK CPI release" event. TradingView-style formatting with grid background.

### Task 2: GBPUSD vs. UK/USA 10-Year Rate Differential
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_gbpusd_rate_diff_research.json`
- **image_ref:** page_01_img_02.png (bottom half)
- **chart_type:** dual-axis overlay line chart
- **data_sources:** GBPUSD spot (^GBPUSD-FX from Polygon), UK 10-year Gilt yield (FRED: IRLTLT01GBM156N, monthly), US 10-year Treasury yield (FRED: DGS10 via MacroEconomicsIndicator.Treasury10Y, daily). Spread = UK minus US.
- **date_range:** 2023-03-01 to 2023-06-30
- **notes:** UK 10Y yield is monthly on FRED, US 10Y is daily. The rate differential updates when the UK monthly value updates. Reconvergence narrative is captured. Charts render correctly with 2 xy_lines charts + summary table.
- **what_makes_it_interesting:** Companion to the EURGBP chart above — together they build the narrative that GBP is no longer dislocated vs. rates. The reconvergence pattern is even cleaner on this pair. Showing both EURGBP and GBPUSD rate diff charts side by side is a masterclass in building a multi-chart argument for squaring a position.
- **reproduction_notes:** Same dual-axis overlay format as Task 1. GBPUSD on right axis (~1.18-1.27), rate differential on left. Time range Mar-Jun 2023. The two series should show reconvergence by June 2023. TradingView style.

### Task 3: USDCAD vs. NYMEX Crude Oil (Inverted)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_usdcad_oil_research.json`
- **image_ref:** page_02_img_00.jpeg
- **chart_type:** dual-axis overlay line chart (one axis inverted)
- **data_sources:** USDCAD spot (^USDCAD-FX from Polygon), WTI Crude Oil (FRED: DCOILWTICO, daily).
- **date_range:** 2022-11-01 to 2023-06-30
- **notes:** Oil price is negated to simulate inverted axis (oil down = line moves up, matching USDCAD direction). Original chart uses hourly data; this reproduction uses daily. The visual correlation and May 2023 decoupling are clearly visible. Second chart shows USDCAD with support/resistance reference lines.
- **what_makes_it_interesting:** Beautifully executed inverted overlay — oil (red line) is plotted on an inverted right axis so that USDCAD (black) and oil visually move together (oil down = CAD weaker = USDCAD up). The visual immediately shows the historically tight correlation and the May 2023 decoupling. The high-frequency (hourly) data gives it texture. This is a signature Donnelly chart type — FX vs. commodity with inverted axis.
- **reproduction_notes:** Black line = USDCAD (left axis, 1.32-1.39). Red line = NYMEX crude (right axis INVERTED, showing 65-90 USD/bbl with 90 at bottom, 65 at top). Hourly data from Nov 2022 to Jun 2023. TradingView watermark visible. The inverted axis is critical to the visual story.

### Task 4: NASDAQ with Quarterly OPEX Week Markers
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_nasdaq_opex_markers_research.json`
- **image_ref:** page_03_img_00.png
- **chart_type:** line chart with vertical event markers
- **data_sources:** QQQ-Stocks (NASDAQ 100 ETF proxy), quarterly OPEX dates computed via datetime_extract (month/day/day_of_week).
- **date_range:** 2021-01-01 to 2023-06-30
- **notes:** OPEX Monday identified as: quarterly month (3/6/9/12), day_of_week=0 (Monday), day 11-17 (3rd week). Vertical black bands via is_band=true on LineSeriesSpec. Second chart shows 10-day momentum normalized 0-1 (252-day min/max) with same OPEX bands. Pattern clearly visible: NASDAQ reverses near each vertical marker.
- **what_makes_it_interesting:** The vertical lines marking quarterly OPEX Mondays visually demonstrate a striking pattern — the NASDAQ reversed direction near every single quarterly expiry from Jan 2022 through Jun 2023 (seven consecutive quarters). Even if the sample is small, the visual is compelling enough to make a trader pay attention. Purple line on white with bold black vertical markers is clean.
- **reproduction_notes:** Purple/blue NASDAQ line (left axis, 9,000-17,000). Black vertical lines at Monday of each quarterly OPEX week. Right axis appears to show a 0-1 indicator (possibly a momentum measure). Time range: 2021 to mid-2023. The pattern to highlight: price reverses direction right around each vertical line.

### Task 5: P&L of Fading 10-Day NASDAQ Momentum Before Quarterly OPEX
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_nasdaq_opex_fade_pnl_research.json`
- **image_ref:** page_03_img_01.png
- **chart_type:** step/line chart (cumulative P&L)
- **data_sources:** QQQ-Stocks, quarterly OPEX dates via datetime_extract. Strategy: on OPEX Monday, fade prior 10-day return, hold 10 trading days (via << lead operator).
- **date_range:** 2020-06-01 to 2023-06-30
- **notes:** Strategy logic implemented fully in EpochScript: 10-day lookback return via >> lag operator, 10-day forward return via << lead operator, conditional fade direction, cumulative sum via cumulative(agg=Sum). Step function via StepType.StepLeft. Second chart shows individual trade returns as scatter with markers. Extra start buffer (2020-06-01) for warmup data before first 2021 OPEX.
- **what_makes_it_interesting:** This is a backtestable strategy with clear rules and a dramatic cumulative P&L chart. The step-function shape (flat between quarterly trades, then jumps up or down) is distinctive. The strategy went from -20% to +43% in cumulative returns, with seven consecutive winning quarters. Even if the sample is small, the chart format and strategy concept are directly reproducible in EpochScript.
- **reproduction_notes:** Blue step-function line on white background. Y-axis: -25% to +45%. X-axis: 2021 to mid-2023. Each step represents one quarterly trade. Strategy starts losing (down to ~-15% by early 2022), then wins consecutively climbing to ~43% by Jun 2023. The step shape is important — flat lines between trades, vertical jumps at trade resolution.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| (none) | All five charts are worth reproducing — this is a strong issue with directly applicable FX and equity market content |
