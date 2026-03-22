# AMFX_20JAN23 — Chart Reproduction Tasks

Source: AMFX 20JAN23 newsletter by Brent Donnelly (Spectra Markets)
Theme: Five macro scenarios (no landing to crash landing) with Bayesian probability framework; UK retail sales at crisis levels; Fed forward guidance credibility gap
Date: January 20, 2023

## Charts to Reproduce

### Task 1: UK Retail Sales 6-Month Rolling Sum (1988-2022)
- **status:** DONE
- **image_ref:** page_01_img_03.png
- **chart_type:** bar (vertical bars, time series)
- **data_sources:** FRED series GBRSLRTTO01GPSAM (OECD UK Retail Trade Volume, Growth Rate Previous Period, use_alfred=False)
- **definition:** `project/definitions/test_runner/amfx_uk_retail_sales_rolling_sum_research.json`
- **date_range:** 2003-10-01 to 2023-01-20 (SPY-Stocks data starts 2003; original chart goes to 1988)
- **what_makes_it_interesting:** Current reading at extreme negative levels only seen during 2008/2009 GFC. In a 6% inflation environment, negative NOMINAL retail sales implies ~12% real drop — "almost unbelievably bad." The chart makes the severity viscerally obvious through the vertical bar format showing how far below zero the current reading plunges compared to 35 years of history.
- **reproduction_notes:** Bar chart with blue bars, 2020-2021 excluded via COVID filter. Zero reference line. 194 monthly bars from 2003-2022. Rolling 6-month sum computed via coalesce(NaN,0) + sum(period=132). Values match original: worst reading ~-5.8% in mid-2022. Limitation: data starts 2003 not 1988 due to SPY-Stocks anchor asset availability.

### Task 2: Implied Overnight Rate & Number of Hikes/Cuts Priced In
- **status:** BLOCKED
- **image_ref:** page_02_img_00.png
- **chart_type:** dual-axis overlay (bar + line)
- **data_sources:** Fed Funds Futures (CME), OIS rates; CME FedWatch implied rates by meeting date
- **block_reason:** Requires a forward curve snapshot of multiple Fed Funds futures contract months at a single point in time (Jan 2023). The platform's futures_continuation produces a single continuous time series, not a cross-sectional term structure. Each x-axis point represents a different contract expiry (FOMC meeting date), not a time progression. This data structure is not supported.
- **what_makes_it_interesting:** Shows the credibility gap between Fed forward guidance ("we'll hold all 2023") and market pricing (cuts by year-end). This is the visual proof of Donnelly's thesis that forward guidance is just extrapolation bias. The bell-curve shape of the bars (rates peak mid-2023, then decline) tells the whole story at a glance.
- **reproduction_notes:** Blue bars = implied policy rate (left axis, 4.2-5.0%). Orange line = number of hikes/cuts priced in (right axis, -0.5 to +2.5). X-axis labels are Fed meeting dates from Current through 01/31/2024. Clean dual-axis design with legend at bottom.

### Task 3: Intergenerational Employment Mobility by Earnings Percentile
- **status:** BLOCKED
- **image_ref:** page_01_img_01.png
- **chart_type:** line (connected scatter)
- **data_sources:** Academic paper (cross-sectional labor economics data)
- **block_reason:** This is academic labor economics data from a published research paper, not financial market data. The platform has no data source for intergenerational employment statistics. Would require manually hardcoded data points or an external dataset not available through FRED, Polygon, or any integrated data provider.
- **what_makes_it_interesting:** The hockey-stick shape at the top of the earnings distribution is striking — flat at ~40% across most percentiles, then spikes to ~70% at the 100th percentile. Visually demolishes the "self-made" narrative. Not financial data but the kind of chart that makes you think differently — exactly what Donnelly's sidebar is for.
- **reproduction_notes:** Black line with dots at each percentile. X-axis: father's earnings percentile (0-100). Y-axis: incidence of same-firm employment (0.30-0.70). Horizontal dashed gridlines. The sharp upward inflection above the 90th percentile is the key visual feature. Source is an academic paper — may be difficult to get raw data.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| (none) | All extracted charts are worth reproducing |
