# AMFX_23NOV22 — Chart Reproduction Tasks

Source: AMFX 23NOV22 newsletter by Brent Donnelly (Spectra Markets)
Theme: Recession probability scorecard — for and against arguments with data visualization
Date: November 23, 2022

## Charts to Reproduce

### Task 1: S&P Performance Around Thanksgiving (Color-Coded Heatmap Table)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_sp500_thanksgiving_research.json`
- **notes:** Scatter chart + summary table. Wed avg +0.31%, Fri avg -0.19% (directionally matches newsletter). Mon/Tue detection captures 19 instances (5 extra non-Thanksgiving matches due to date-range overlap).
- **image_ref:** page_01_img_03.png
- **chart_type:** heatmap table
- **data_sources:** S&P 500 daily returns (Yahoo: ^GSPC or SPY); US Thanksgiving calendar dates
- **what_makes_it_interesting:** Clean color-coded table showing seasonal returns around a specific holiday with summary stats. The Black Friday weakness (38% hit rate, -0.3% median) is a surprising, actionable finding for short-term traders. Great design — red/blue shading makes patterns jump out immediately.
- **reproduction_notes:** Rows = years (2009-2022), columns = t-1 (Wed), t+1 (Fri), t+2 (Mon), t+3 (Tue). Red shading for negative returns, blue for positive. Bottom rows show Average, Median, and "% of time stocks higher." Need to map exact Thanksgiving dates to trading days for each year.

### Task 2: Yield Curve Inversion to Recession Lead Time Table
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_yield_curve_recession_research.json`
- **notes:** 2 charts + cards. 10Y-3M spread line with inversion threshold + inversion depth chart. Data limited to 2003+ (SPY data availability). Current spread -1.18%, deepest -1.32%, max 3.85%.
- **image_ref:** page_03_img_00.png
- **chart_type:** table
- **data_sources:** FRED: T10Y3M (3M-10Y spread); NBER recession dates
- **what_makes_it_interesting:** Perfect track record — 8 for 8 inversions preceded recessions. The variable lag (140-487 days, avg 311) is the key insight. Clean, well-structured table that immediately communicates both the reliability and the timing uncertainty of the signal.
- **reproduction_notes:** Table with 4 columns: Date of Inversion, Consecutive Trading Days Inverted, Date of Next Recession, Calendar Days to Recession. Highlight the average row. Include footnotes about intermittent inversions (1969, 1989). Source: Jim Bianco Research. Can extend to include 2022 inversion.

### Task 3: NFIB Optimism Index — Hard vs Soft Components Divergence
- **status:** BLOCKED
- **reason:** Individual NFIB component series (Hard vs Soft decomposition) are not available via FRED or the platform's common_economic_indicators. The NFIB publishes aggregate index data but the individual component breakdown required for this chart is only available directly from NFIB or via Bloomberg.
- **image_ref:** page_03_img_01.png
- **chart_type:** dual line chart
- **data_sources:** NFIB Small Business Optimism Index components (NFIB website or FRED); decomposition into hard (Job Creation Plans, Job Openings, Inventory Plans, Earnings, CapEx Plans) and soft (Expected Business Conditions, Outlook for Expansion, Expected Real Sales, Expected Credit Conditions, Inventory Satisfaction)
- **what_makes_it_interesting:** The hard vs soft divergence is a powerful visualization of the "vibes recession" phenomenon. Soft data (expectations) collapsed to -100 while hard data stayed near 0. This split between what businesses ARE doing vs what they EXPECT to happen is a leading indicator debate in one chart. The 2022 divergence was historically extreme.
- **reproduction_notes:** Two line series: Hard (bold black) and Soft (thinner gray/black). Y-axis: Percent (-150 to +150). X-axis: 1986-2022. Title is "OPTIMISM INDEX COMPONENTS" with component lists in subtitle. No color — monochrome design. The key visual is the unprecedented gap between the two lines in 2022.

### Task 4: Conference Board LEI vs Recessions (1960 to Now)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_lei_vs_recessions_research.json`
- **notes:** 2 charts + cards. Uses Industrial Production YoY % and 10Y-2Y Spread as proxies for Conference Board LEI (OECD CLI via economic_indicators returned all NaN due to uncached FRED data). Recession probability shading via RecessionProb. IP YoY -0.03%, Spread -0.69%, Recession Prob 0.4%.
- **image_ref:** page_04_img_00.png
- **chart_type:** line chart with recession shading
- **data_sources:** FRED: USSLIND (Conference Board LEI, 6-month annualized change); USREC (NBER recessions)
- **what_makes_it_interesting:** One of the cleanest leading indicator visualizations in macro. The LEI has NEVER gone to -2.7 without a recession following. 60+ years of data, perfect track record. Gray recession bars make the pattern viscerally obvious. The 2022 reading plunging to -10 while calling "no recession" was the key tension.
- **reproduction_notes:** Blue line for LEI (YoY or 6m annualized change), gray vertical bars for NBER recessions. Y-axis: -25 to +20. X-axis: 1960-2022, labeled every 2 years. Add horizontal reference line at -2.7 threshold. Clean, classic macro chart design.

### Task 5: Tech Layoffs in 2022 (Dual-Axis Bar Chart)
- **status:** BLOCKED
- **reason:** layoffs.fyi data is not available in any standard financial data source (FRED, Polygon, or platform common_economic_indicators). This is a proprietary dataset scraped from company announcements. Would require manual data entry or a custom web scraper.
- **image_ref:** page_04_img_01.png
- **chart_type:** grouped bar chart (dual-axis)
- **data_sources:** layoffs.fyi historical data (monthly aggregated tech layoffs)
- **what_makes_it_interesting:** The acceleration pattern is dramatic — near zero in Jan 2022, exploding to 45,000+ by November. The dual-axis showing both employee count and company count tells a richer story than either alone. November 2022 spike is visually shocking. Good example of using a bar chart to show acceleration.
- **reproduction_notes:** Coral/salmon bars for "Employees Laid Off" (left axis: 0-50,000), light blue bars for "Companies w/ Layoffs" (right axis: 0-300). X-axis: Jan-Nov 2022. Source labeled: layoffs.fyi. Grouped bars (not stacked). The Nov spike in employees but NOT companies shows a few mega-layoffs (Meta, Amazon, Twitter).

### Task 6: JOLTS Job Openings (2001 to Now)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_jolts_job_openings_research.json`
- **notes:** 1 chart + cards. Uses common_economic_indicators(MacroEconomicsIndicator.JobOpenings). Latest 10,458, High 11,549, Low 2,760, Avg 5,913. Reference line at 4,400 pre-recession level.
- **image_ref:** page_05_img_00.png
- **chart_type:** line chart
- **data_sources:** FRED: JTSJOL (JOLTS Total Nonfarm Job Openings, thousands, SA)
- **what_makes_it_interesting:** The sheer scale of the post-COVID job openings spike is the most powerful counter-argument to the recession thesis. At 10.7M openings vs 4.4M going into prior recessions, the labor market buffer is unprecedented. The visual makes this obvious — the 2021-2022 spike dwarfs everything before it. A macro trader seeing this would immediately question any recession call.
- **reproduction_notes:** Single line, warm tan/gold background (Bloomberg style). Y-axis: 2,000-12,000. X-axis: 2001-2022. Add annotations: "Mid Price 10717.0", "High on 03/31/22: 11855.0", "Average: 5049.4", "Low on 07/31/09: 2232.0". Large bold title overlaid on chart. Bloomberg copyright footer.

## Discarded Charts

| Chart | Reason |
|-------|--------|
| Bloomberg Market Profile (page_02_img_00.png) | Highly specialized Bloomberg MKTP chart with letter-based volume distribution — impossible to reproduce without Bloomberg's market profile engine. The chart type (volume-at-price with time letters) has no equivalent in standard charting. Also very date-specific. |
| US 10Y Yields longer-term (page_02_img_01.jpeg) | Standard TradingView price chart with moving averages and a horizontal line. No unique data or insight beyond basic technical analysis. Any trader can pull this up instantly. |
| Google Trends "recession" (page_03_img_02.png) | While conceptually interesting, it's a direct Google Trends screenshot with no transformation or overlay. Trivially reproducible by anyone visiting trends.google.com. No quantitative depth beyond the raw search index. |
