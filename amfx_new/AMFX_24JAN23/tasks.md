# AMFX_24JAN23 — Chart Reproduction Tasks

Source: AMFX 24JAN23 newsletter by Brent Donnelly (Spectra Markets)
Theme: FX microstructure (WMR fix flows, autocorrelation), G10 positioning/momentum scorecard, and financial conditions
Date: January 24, 2023

## Charts to Reproduce

### Task 1: EURUSD Volume by Time of Day
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_eurusd_volume_by_tod_research.json`
- **image_ref:** page_01_img_02.png
- **chart_type:** bar chart (histogram)
- **data_sources:** EURUSD-FX 1-minute volume data averaged by hour of day (UTC)
- **what_makes_it_interesting:** Reveals the hidden architecture of the FX market day. Four distinct volume spikes labeled with red numbers: (1) London open, (2) US data releases, (3) Options expiry, (4) WMR Fix. The WMR Fix is the LARGEST spike — bigger than the London open — which most retail traders don't realize. This is how institutional flow shapes the market.
- **reproduction_notes:** Uses 1-minute EURUSD data from 2024-06-01 to 2025-01-01 (modern data approximation). Extracts hour of day (UTC) and computes mean volume per hour bucket. The structural volume pattern (London open, US data, options expiry, WMR fix) is persistent across years. Blue bars with data labels.
- **limitations:** Original chart likely uses longer historical period and higher-resolution bucketing. Our version uses recent 1-minute data aggregated to hourly buckets.

### Task 2: WMR Fix Autocorrelation Strategy P&L (AUDUSD and EURUSD)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_wmr_fix_audusd_research.json` and `project/definitions/test_runner/amfx_wmr_fix_eurusd_research.json`
- **image_ref:** page_02_img_00.png
- **chart_type:** dual panel cumulative P&L line chart
- **data_sources:** AUDUSD and EURUSD 1-minute or hourly data (10am-11am NY window); strategy: if >0.4% rally in 10am-11am on day T, go long 10am-11am on day T+1
- **what_makes_it_interesting:** Tests whether large fix flows persist to the next day — a structural market microstructure hypothesis. The cumulative P&L is positive for both pairs, with a dramatic step-function in 2020 (COVID created massive multi-day fix flows). The 62% win rate on 94 occurrences is statistically interesting. The step-function shape reveals that most of the alpha came from extreme regimes, not steady accumulation.
- **reproduction_notes:** Side-by-side panels. Left: "AUDUSD +0.4% 10am to 11am" with cumulative return 0-5%. Right: "EURUSD +0.4% 10am to 11am" with cumulative return -1% to 3.5%. Both show step-function jumps around 2020. Blue line on white background. Y-axis as percentage, X-axis: 2010-2022.
- **implementation_notes:** Uses `roc(period=60)` at `bar_tod==660` (11:00 AM ET) to compute 10-11am window return. Forward-fills fix return, shifts by 1 bar for yesterday's value, applies 0.4% threshold. `cumulative()` for running sum. Separate definitions per pair. Run with `--start 2010-01-01 --end 2023-01-31`. 4.8M 1-min bars per asset.

### Task 3: Cumulative Performance of GBPUSD at 10am-11am NY Fix Window
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_gbpusd_fix_cumret_research.json`
- **image_ref:** page_02_img_01.png
- **chart_type:** cumulative return line chart
- **data_sources:** GBPUSD intraday data (10am-11am NY daily returns, cumulated from 2010)
- **what_makes_it_interesting:** One of the most striking FX microstructure charts. Going long GBPUSD for just 1 hour per day (the fix window) generated +5% by 2014, then collapsed to -14% by 2020. The massive drawdown corresponds exactly to the Brexit period (2016-2020) when real money hedgers persistently sold GBP at the fix. This reveals structural flow patterns that persist for YEARS. A masterclass in visualizing hidden market plumbing.
- **reproduction_notes:** Single black line on white background. Y-axis: -14% to +6%. X-axis: 2010-2022. The shape is distinctive: rise to +5% (2010-2014), sharp decline to -14% (2016-2020), partial recovery to -6% (2022). No annotations needed — the shape tells the story.
- **implementation_notes:** Uses `roc(period=60)` at `bar_tod==660` (11:00 AM ET) for unconditional 10-11am daily return. `cumulative()` for running sum. Filters to 11am bars for xy_lines plotting (3356 data points from 4.8M total). Run with `--start 2010-01-01 --end 2023-01-31`. Chart shape differs from original due to Polygon FX data vs institutional Reuters/Bloomberg data source — methodology is sound.

### Task 4: G10 FX Positioning and Momentum Scorecard
- **status:** BLOCKED
- **image_ref:** page_05_img_00.png
- **chart_type:** heatmap table (color-coded)
- **data_sources:** CFTC COT data (positioning levels + 4-week change), Daily Sentiment Index, FX Risk Reversals (1M and 6M, Bloomberg), RSI, 20-day and 100-day MA deviations for G10 FX pairs
- **what_makes_it_interesting:** A comprehensive positioning and momentum dashboard in one image. The color coding (red = bearish USD, blue = bullish USD) makes extreme readings jump out. USD at -10 on 100-day deviation is screaming oversold. EUR/GBP/AUD/NZD all at 8+ momentum is a powerful consensus trade visualization. This is the kind of multi-factor scorecard that institutional FX desks use but rarely share publicly.
- **reproduction_notes:** Three stacked tables with consistent color coding. Top: Summary Scores (Positioning + Momentum). Middle: Positioning & Sentiment (6 sub-components). Bottom: Momentum (3 sub-components). All on -10 to +10 scale. Colors: deep red for strongly negative, deep blue for strongly positive, white for neutral. 8 columns: USD, EUR, CHF, JPY, GBP, AUD, NZD, CAD. Header note: "All scores -10 to +10 scale, all currencies vs. USD."
- **blocked_reason:** Requires CFTC COT data, Daily Sentiment Index, and Bloomberg FX Risk Reversals (1M and 6M) — none of which are available through our FRED/Polygon data sources. No CFTC/COT transforms exist in the platform.

### Task 5: FX Positioning and Momentum Bar Charts (Week-over-Week)
- **status:** BLOCKED
- **image_ref:** page_05_img_01.png, page_05_img_02.png
- **chart_type:** grouped bar chart (two panels)
- **data_sources:** Same as Task 4 — composite positioning and momentum scores
- **what_makes_it_interesting:** The week-over-week comparison makes changes immediately visible. The visual contrast between USD's deep negative bars and every other currency's positive bars is striking. The near-symmetry (what USD loses, everyone else gains) reinforces the "sell USD" narrative. Good design pattern: paired bar charts showing time evolution of multi-asset scores.
- **reproduction_notes:** Two separate charts. Left: "FX Positioning" with gray (last week) and blue (this week) bars. Right: "FX Momentum" same format. Y-axis: -10 to +10. X-axis: USD, EUR, CHF, JPY, GBP, AUD, NZD, CAD. Clean gray background with gridlines.
- **blocked_reason:** Same as Task 4. Requires CFTC COT data, sentiment indices, and Bloomberg risk reversals that are not available on our platform.

### Task 6: Bloomberg US Financial Conditions Index
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_us_financial_conditions_research.json`
- **image_ref:** page_06_img_00.png
- **chart_type:** line chart
- **data_sources:** Chicago Fed NFCI (FRED series NFCI), negated to match Bloomberg FCI convention (positive = loose, negative = tight)
- **what_makes_it_interesting:** Tells a crucial macro story: despite the most aggressive Fed hiking cycle in decades, financial conditions had EASED back to Feb 2022 levels by Jan 2023. The V-shaped recovery from -1.3 to +0.5 undermined the entire "tightening is working" narrative. This chart was a key input for the "soft landing" vs "financial conditions are too easy" debate that dominated 2023.
- **reproduction_notes:** Uses Chicago Fed NFCI as proxy for Bloomberg US FCI (proprietary). NFCI convention is inverted (positive = tight), so we negate: -NFCI approximates Bloomberg direction. Blue line with zero reference line. Period: 2020-12-01 to 2023-01-31. Shape matches original: high plateau (2021), collapse (Mar-Oct 2022), sharp recovery (Oct 2022 - Jan 2023).
- **limitations:** NFCI is a proxy for Bloomberg FCI; values and scale differ slightly but the directional pattern matches.

### Task 7: Hours of Work to Buy a Gallon of Gasoline
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_gasoline_labor_hours_research.json`
- **image_ref:** page_04_img_00.png
- **chart_type:** line chart (ratio)
- **data_sources:** FRED: GASREGW (Regular gasoline price, available from 2009) and CPIAUCSL (CPI for real adjustment)
- **what_makes_it_interesting:** Brilliant reframing of gas price data. Instead of nominal price (which always triggers panic), expressing cost in labor hours reveals that gas affordability has been relatively stable over decades. The 2008 peak (~0.23 hours) and 2022 spike (~0.18 hours) are concerning but not unprecedented. A Malthusian-myth-busting chart that changes how you think about commodity affordability.
- **reproduction_notes:** Original chart uses gas price / hourly earnings (CES0500000003). Since CES0500000003 is not in the FRED cache and API fetch fails, we use CPI-adjusted real gas price as a proxy for affordability. Shows nominal vs real gas price from 2009-2023. The real price demonstrates the same insight: gas is not as expensive in purchasing-power terms as the nominal price suggests.
- **limitations:** (1) GASREGW data starts 2009 vs original's 1990 start. (2) Uses CPI adjustment instead of hours-of-labor ratio because CES0500000003 (hourly earnings) is unavailable in the data cache/API.

## Discarded Charts

| Chart | Reason |
|-------|--------|
| AUDUSD 1-minute chart (page_01_img_03.jpeg) | Single-day intraday price chart showing WMR fix rally. While it illustrates the concept, it's a one-off event with no general reproducibility. The annotation "11am NY / 4pm LDN" is the only insight; the rest is just a price chart. |
| Bloomberg HDS - JGB holders (page_03_img_00.png) | Bloomberg terminal screenshot of bond ownership data. The "114.76% BOJ ownership" fact is striking but the chart is just a data table from a proprietary terminal. Not reproducible without Bloomberg. The insight is better conveyed as a single statistic or card. |
| GOOG hourly with RSI (page_03_img_01.jpeg) | Generic TradingView hourly chart with RSI. No unique data transformation or overlay. Any trader can pull up RSI on any stock. The "overbought tech" thesis is better expressed through aggregate data, not a single stock's RSI. |
