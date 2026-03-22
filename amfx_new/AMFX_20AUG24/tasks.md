# AMFX_20AUG24 — Chart Reproduction Tasks

Source: AMFX 20AUG24 newsletter by Brent Donnelly (Spectra Markets)
Theme: Big levels in FX — USDCAD at critical 1.3600 support, EURUSD in "rarified air" above 1.1100; JPY positioning undergoes biggest shift in 20+ years
Date: August 20, 2024

## Charts to Reproduce

### Task 1: Distribution of Daily EURUSD Closes Above 1.08
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_eurusd_close_distribution_research.json`
- **output:** `project/research_studies/test_runner/amfx_eurusd_close_distribution_research`
- **image_ref:** page_02_img_00.png
- **chart_type:** histogram / bar chart (frequency distribution)
- **data_sources:** EURUSD daily close prices (Yahoo Finance EURUSD=X), Aug 2022 to Aug 2024 (~2 years)
- **what_makes_it_interesting:** Brilliant way to show "rarified air" — instead of a price chart, Donnelly shows the DISTRIBUTION of closes, making it visually obvious that closes above 1.1100 are extremely rare (only 9 in 2 years). The long right tail tapering to near-zero is the visual punchline. This is a repeatable chart type for any asset approaching statistical extremes.
- **reproduction_notes:** Blue/teal vertical bars on white, x-axis bins are 50-pip increments from 1.0805 to 1.1395+, y-axis count 0-12. Filter to only closes above 1.08. Peak frequency around 1.0850 (11 closes). The sparse bars above 1.1100 make the statistical rarity visually obvious. Title: "Distribution of daily EURUSD closes >1.08 since Aug2022."

### Task 2: JPY Positioning Z-Score — Biggest Shift in 20+ Years
- **status:** BLOCKED
- **blocked_reason:** CFTC Commitments of Traders data is not available through FRED or any other data source in the platform. The economic_indicators transform only covers FRED series; CFTC COT positioning data (weekly net speculative contracts by currency) is a separate dataset not present in the system.
- **image_ref:** page_04_img_00.jpeg
- **chart_type:** line (time series, z-score oscillator)
- **data_sources:** CFTC Commitments of Traders data — JPY net speculative positioning (available from CFTC website). Compute 6-week change, then z-score with 2-year lookback window. Data from 2002-2024.
- **what_makes_it_interesting:** Shows that the JPY positioning shift (from mega-short to long) was a nearly 5.5 sigma event — the most extreme since September 2003. Visually, the spike at the right edge of a 22-year oscillator is immediately striking. This is genuine positioning alpha — extreme shifts have historically been directionally predictive.
- **reproduction_notes:** Dense black oscillator line, 2002-2024 on x-axis, z-score roughly -4 to +6 on y-axis. The current spike at the far right dwarfs almost everything in the series. Bloomberg attribution. Title: "Abrupt Shift — The biggest yen positioning adjustment in more than 20 years." Subtitle: "6-week change in IMM JPY spec positioning z-score."

### Task 3: CFTC Speculative JPY Position (30-Year History)
- **status:** BLOCKED
- **blocked_reason:** Same as Task 2. CFTC Commitments of Traders net speculative positioning data (contracts) is not available through FRED or any platform data source. Would need a dedicated CFTC/COT data feed or Quandl integration.
- **image_ref:** page_06_img_01.png
- **chart_type:** line (long-term time series)
- **data_sources:** CFTC Commitments of Traders — JPY net speculative position (contracts), 1992-2024. Available from CFTC website or Quandl.
- **what_makes_it_interesting:** The 30+ year view puts the 2022-2024 JPY short in historical context — it was approaching the deepest short positioning EVER (~-180K contracts), and the snap back to long is circled in red at the far right. Seeing this in a multi-decade context makes the regime change visceral. A macro trader looks at this and knows something fundamental has changed.
- **reproduction_notes:** Gray line chart, 1992-2024, y-axis -250K to +100K contracts. Red circle annotation at the far right highlighting the flip from extreme short to long. Title: "CFTC Speculative JPY Position." The visual drama is in the depth of the 2022-2024 trough and the sharp recovery.

### Task 4: Extreme Futures Positioning Z-Score Shifts Table
- **status:** BLOCKED
- **blocked_reason:** Requires CFTC COT positioning data across multiple futures contracts (EUR, AUD, NZD, TY, NQ, DOW, RTY, VIX). Same data unavailability as Tasks 2 and 3. Additionally, the table format with hardcoded historical outcomes would need a static table approach, but the underlying z-score computation requires the raw CFTC data.
- **image_ref:** page_06_img_00.png
- **chart_type:** table
- **data_sources:** CFTC Commitments of Traders data across multiple contracts (EUR, AUD, NZD, TY, NQ, DOW, RTY, VIX IMM futures). Z-score of 6-week net positioning change. Historical instances where z-score exceeded +/-5.
- **what_makes_it_interesting:** A rare dataset — only 9 instances of 5+ sigma positioning shifts across all major futures contracts since 2002. The outcomes column shows that price generally followed the direction of the positioning shift, providing evidence that extreme positioning changes are directionally predictive. This is a quantifiable framework, not just a narrative.
- **reproduction_notes:** Simple table with columns: CONTRACT, DATE, Z-SCORE CHG, OUTCOME. 9 rows of data. Bold headers, clean formatting. Key examples: EUR IMM -6.31 (EUR -4% next 2M), AUD IMM +5.17 (AUD +8% next 2M), NQ +5.76 (NQ +20% in 3M).

### Task 5: G10 FX Positioning and Momentum Scorecard
- **status:** BLOCKED
- **blocked_reason:** Requires multiple unavailable data sources: (1) CFTC positioning (% of OI, 4-week change) -- not on FRED, (2) Daily Sentiment Index -- proprietary data from Jake Bernstein, (3) Risk reversals (1M, 6M) -- options market data not available, (4) Spectra FX Positioning -- proprietary Spectra Markets data. Only the momentum components (RSI, MA deviations) could be computed from price data, but without positioning/sentiment data the scorecard cannot be reproduced.
- **image_ref:** page_07_img_00.png, page_07_img_01.png, page_07_img_02.png
- **chart_type:** heatmap tables + grouped bar charts
- **data_sources:** Composite of CFTC positioning (% of OI, 4-week change), Daily Sentiment Index, risk reversals (1M and 6M), RSI, deviation from 20-day and 100-day moving averages. All G10 currencies vs. USD.
- **what_makes_it_interesting:** A comprehensive positioning and momentum dashboard that is both visually appealing (color-coded heatmap with red/blue shading on -10 to +10 scale) and analytically rich. The two bar charts (Positioning and Momentum, this week vs. last week) provide instant visual comparison. USD momentum at -8 vs. JPY at +9 tells the whole macro story at a glance.
- **reproduction_notes:** Three components: (1) Summary scores table with Positioning and Momentum rows, (2) Detailed Positioning & Sentiment table (6 rows) and Momentum table (3 rows), both color-coded red (negative) to blue (positive), (3) Two side-by-side grouped bar charts showing "Last week" (gray) vs. "This week" (light blue) for each currency. The heatmap coloring is the key visual feature — strong blue for positive, strong red for negative, white for neutral.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| USDCAD Daily price chart (page_01_img_01.png) | Standard price chart with horizontal support/resistance lines at 1.36, 1.39, 1.40. Clean execution but generic technical analysis — the levels are interesting but the chart is just annotated price action with no overlay, ratio, or statistical insight. Not worth reproducing. |
| USDCAD Hourly price chart (page_01_img_02.png) | Zoomed-in version of the daily showing 1.3600 as support/resistance flip. Same issue — clean but purely technical with no additional analytical layer. |
| EURUSD Daily price chart (page_03_img_00.png) | Standard daily candlestick with 1.1140 resistance line drawn. Useful for context but just annotated price — the histogram (Task 1) tells the same story much more powerfully with statistical rigor. |
| Dollar Bears Emerged in 2003 — USDJPY historical (page_05_img_00.jpeg) | Historical analog chart showing USDJPY 2003-2004 after similar positioning shift. Interesting as context for the JPY thesis but it is just a single price chart with an arrow — the positioning z-score chart (Task 2) is the more powerful version. The analog comparison could be reproduced as an overlay if needed but is lower priority. |
