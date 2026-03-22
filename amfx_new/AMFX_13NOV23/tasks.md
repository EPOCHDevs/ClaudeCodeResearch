# AMFX_13NOV23 — Chart Reproduction Tasks

Source: AMFX 13NOV23 newsletter by Brent Donnelly (Spectra Markets)
Theme: 2024 Almanac promotion showcasing 2023 seasonality trade performance (60.6% win rate, +190% cumulative return)
Date: November 13, 2023

## Charts to Reproduce

### Task 1: Cumulative Return of Almanac Seasonality Trades YTD
- **status:** DONE
- **image_ref:** page_02_img_00.png
- **chart_type:** line (cumulative return time series)
- **data_sources:** Proprietary Spectra Markets data — would need to reconstruct with a portfolio of seasonal trades across FX, equities, commodities, bonds. Could approximate with known seasonal patterns (e.g., sell-in-May, January effect, TLT seasonality, GBPUSD seasonality)
- **what_makes_it_interesting:** Shows a real out-of-sample equity curve for a seasonal trading system. The sharp drawdown in Jan-Feb followed by a massive March rally (SVB crisis) and then steady uptrend is a compelling narrative about seasonal signals capturing macro dislocations.
- **reproduction_notes:** Clean dark blue line on white background, y-axis from -50% to +200%, x-axis monthly labels Jan 2023 to Nov 2023. The SVB crisis spike in March is the dominant visual feature. This is more of a "concept to replicate" than exact data — we could build our own seasonal signal portfolio and track cumulative returns.
- **definition:** `project/definitions/test_runner/amfx_seasonal_cumret_research.json`
- **output:** `project/research_studies/test_runner/amfx_seasonal_cumret_research`
- **implementation_notes:** Approximation using SPY with two known calendar effects (Halloween effect: long Nov-Apr; Turn-of-Month: last 2 + first 3 trading days). Shows cumulative return of seasonal windows vs non-seasonal windows vs buy-and-hold. Original chart uses proprietary multi-asset Spectra Markets Almanac data (+190% cumret from 109 trades across FX/equities/commodities/bonds), so magnitude differs but the concept and chart format match.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| 2023 Almanac Seasonality Trade Statistics table | Summary stats table (win rate 60.6%, avg return 1.20%) — useful context but a simple table, not a chart worth reproducing as standalone. The metrics are interesting but better shown as cards alongside the cumulative return chart. |
| This week's calendar (Nov 13-17, 2023) (page_03_img_00.png) | Event calendar specific to one week in 2023 — date-specific, no lasting analytical value. The seasonality highlights (TLT bullish, GBPUSD seasonal low) are interesting but better as separate seasonal studies. |
