# AMFX 24JAN23 - AUD, GBP, JGBs and asteroids

**Date:** January 24, 2023
**Author:** Brent Donnelly, Spectra Markets
**Pages:** 8

## Summary

This newsletter covers multiple topics: large AUDUSD buying at the WMR Fix (4pm London), intraday FX volume patterns, an autocorrelation study of WMR fix flows, GBPUSD cumulative performance at the fix window, BOJ ownership of JGBs (114.76% of the 2030 issue), Google/GOOG overbought RSI analysis, the cost of gasoline in hours of labor, and the weekly FX Positioning and Momentum Report. Also discusses EURGBP thesis, Bloomberg Financial Conditions Index, China reopening, and Nick Bostrom's "Letter from Utopia."

**Current Views mentioned:** Long 07FEB EURGBP call spread 0.8870/0.8920 risking 22 GBP bps to make 50 (spot ref 0.8850).

---

## Visual Elements Inventory

### Page 1
| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 1 | Spectra Markets logo/header | DISCARD | page_01_img_01.jpeg | Company branding logo |
| 2 | amFX logo | DISCARD | page_01_img_00.png | Newsletter branding |
| 3 | EURUSD volume by time of day bar chart | **KEEP** | page_01_img_02.png | Intraday volume distribution chart |
| 4 | AUDUSD 1-minute chart (Jan 23, 2023) | **KEEP** | page_01_img_03.jpeg | Intraday price chart showing WMR fix rally |

### Page 2
| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 5 | Spectra Markets header | DISCARD | not extracted (below size threshold) | Company branding logo |
| 6 | P&L of autocorrelation buy strategy - AUDUSD and EURUSD (dual chart) | **KEEP** | page_02_img_00.png | Cumulative P&L chart for a systematic FX strategy |
| 7 | Cumulative performance of GBPUSD 10am-11am NY (2010 to now) | **KEEP** | page_02_img_01.png | Cumulative return time series showing fix window performance |

### Page 3
| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 8 | Spectra Markets header | DISCARD | not extracted (below size threshold) | Company branding logo |
| 9 | Bloomberg HDS page - 2030 JGB holders table | **KEEP** | page_03_img_00.png | Holdings/ownership data table for JGB |
| 10 | GOOG hourly chart with RSI | **KEEP** | page_03_img_01.jpeg | Technical price chart with momentum indicator |

### Page 4
| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 11 | Spectra Markets header | DISCARD | not extracted (below size threshold) | Company branding logo |
| 12 | "How many hours to buy a gallon of gasoline?" line chart | **KEEP** | page_04_img_00.png | Long-term economic ratio time series |

### Page 5
| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 13 | Spectra Markets header | DISCARD | not extracted (below size threshold) | Company branding logo |
| 14 | G10 FX Positioning and Momentum - Summary Scores table | **KEEP** | page_05_img_00.png | Multi-currency positioning/momentum scorecard |
| 15 | G10 FX Positioning and Momentum - Positioning and Sentiment table | **KEEP** | page_05_img_00.png | Detailed positioning breakdown table |
| 16 | G10 FX Positioning and Momentum - Momentum table | **KEEP** | page_05_img_00.png | Momentum indicators table |
| 17 | FX Positioning bar chart (Last week vs This week) | **KEEP** | page_05_img_01.png | Comparative bar chart of positioning scores |
| 18 | FX Momentum bar chart (Last week vs This week) | **KEEP** | page_05_img_02.png | Comparative bar chart of momentum scores |

### Page 6
| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 19 | Spectra Markets header | DISCARD | not extracted (below size threshold) | Company branding logo |
| 20 | Bloomberg US Financial Conditions Index chart | **KEEP** | page_06_img_00.png | Time series of financial conditions |

### Page 7
| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 21 | Spectra Markets header | DISCARD | not extracted (below size threshold) | Company branding logo |
| 22 | AI-generated "futuristic spreadsheet" image | DISCARD | page_07_img_00.jpeg | AI-generated art, decorative, non-quantitative |

### Page 8
| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 23 | Spectra Markets header | DISCARD | not extracted (below size threshold) | Company branding logo |

*Page 8 is the standard disclaimer page.*

---

## Kept Items - Detailed Analysis

### Item 1: EURUSD Volume by Time of Day

- **type:** Bar chart (vertical bars)
- **image_file:** page_01_img_02.png
- **title:** "Volume by time of day - EURUSD currency spot"
- **page:** 1
- **data:** Average EURUSD spot trading volume distributed by time of day, showing intraday volume pattern
- **assets/instruments:** EURUSD spot
- **transforms/calculations:** Volume aggregation by time of day (likely averaged over many days)
- **metrics:** Four labeled volume spikes:
  1. London open (~7:00 GMT / 2:00 NYC)
  2. US economic data releases (~13:30 GMT / 8:30 NYC)
  3. Options expiry (~14:00-15:00 GMT / 9:00-10:00 NYC)
  4. WMR Fix (~16:00 GMT / 11:00 NYC) - the largest spike
- **time_range:** Intraday (24-hour cycle), averaged over historical period
- **x_axis:** Time of day (dual labels: GMT top row, NYC time bottom row, from 0:00 to 17:00 NYC)
- **y_axis:** Volume (appears to be indexed or in arbitrary units, range ~20 to 120)
- **insight:** The WMR Fix at 4pm London / 11am NY is the single highest volume moment of the FX trading day. Most currencies (including AUDUSD) follow a similar pattern, though USDJPY sees its largest volume at the Tokyo fix (9:55am Tokyo). Large hedgers and real money use the fix window to benchmark and execute large trades. This explains why large flows at the fix can create significant short-term price impact.
- **source:** Not explicitly stated (likely EBS/Reuters or Bloomberg)

---

### Item 2: AUDUSD 1-Minute Chart (January 23, 2023)

- **type:** Candlestick chart (1-minute bars)
- **image_file:** page_01_img_03.jpeg
- **title:** "1-minute chart of AUDUSD yesterday" (January 23, 2023)
- **page:** 1
- **data:** AUDUSD intraday price action showing a sharp rally into the 4pm London fix
- **assets/instruments:** AUDUSD spot
- **transforms/calculations:** None (raw price data)
- **metrics:**
  - Rally magnitude: approximately 0.8% in one hour (from ~0.6900 to ~0.7050 area)
  - Key level annotated: "11am NY / 4pm LDN" marking the WMR fix time
- **time_range:** January 23, 2023 (single trading day, approximately 15:00 to 02:00 next day)
- **x_axis:** Time (intraday, labeled approximately every 3 hours)
- **y_axis:** AUDUSD price (range ~0.6900 to 0.7050)
- **insight:** Demonstrates the impact of large fix flows. A large buyer (suspected dividend payment from miners like BHP, Rio) pushed AUDUSD up 0.8% in one hour into the fix. When there is a massive fix one day, the market gets edgy the next day wondering if there will be another one, since extremely large flows are sometimes chunked into multiple days.
- **source:** Bloomberg (implied)

---

### Item 3: P&L of Autocorrelation Buy Strategy - AUDUSD and EURUSD (2010 to now)

- **type:** Dual cumulative P&L line charts (side by side)
- **image_file:** page_02_img_00.png
- **title:** "P&L of autocorrelation buy strategy in AUDUSD and EURUSD (2010 to now)"
- **page:** 2
- **data:** Cumulative P&L of a simple strategy: if currency rallies more than 0.4% between 10am and 11am on day T, go long from 10am to 11am on day T+1
- **assets/instruments:** AUDUSD spot, EURUSD spot
- **transforms/calculations:** Autocorrelation-based strategy. Entry condition: >0.4% rally in 10am-11am window. Position: long next day same window. Cumulative P&L computed from 2010 to present.
- **metrics:**
  - AUDUSD +0.4% strategy: Cumulative return ~4% from 2010 to 2022, with significant spike during 2020 (COVID)
  - EURUSD +0.4% strategy: Cumulative return ~3.5% from 2010 to 2022, much smoother profile
  - Win rate for AUDUSD: 62% (if rallied >0.4% from 10am-11am, 62% chance it went higher next day in same window)
  - Sample size: 94 occurrences back to 2010
- **time_range:** 2010 to January 2023
- **x_axis:** Year (2010 through 2022)
- **y_axis:** Cumulative return (%) - AUDUSD: -0.5% to 4.0%; EURUSD: 0.0% to 3.5%
- **insight:** There is mild evidence of autocorrelation in fix flows, particularly during 2020 when COVID-era volatility created large multi-day fix flows. The strategy shows positive returns but a lot of the win rate is concentrated in recent years. This supports the theory that very large flows get split up into chunks over multiple WMR fixes. For bearish AUD/NZD traders: watch out for spikes to sell into at 11am NY / 4pm LDN.
- **source:** Spectra Markets analysis

---

### Item 4: Cumulative Performance of GBPUSD, 10am to 11am NY (2010 to now)

- **type:** Cumulative return line chart
- **image_file:** page_02_img_01.png
- **title:** "Cumulative performance of GBPUSD, 10am to 11am NY, 2010 to now"
- **page:** 2
- **data:** Cumulative return of going long GBPUSD every day from 10am to 11am NY time
- **assets/instruments:** GBPUSD spot
- **transforms/calculations:** Daily return from 10am to 11am NY aggregated cumulatively over ~13 years
- **metrics:**
  - Peak positive: ~+4% (around 2014-2015)
  - Trough: approximately -13% to -14% (around 2020)
  - Current: approximately -6% to -7%
  - Notable drawdown period: 2016 through 2020 (Brexit era)
- **time_range:** 2010 to January 2023
- **x_axis:** Year (2010 through 2022)
- **y_axis:** Cumulative return (%) ranging from -14% to +6%
- **insight:** This chart reveals persistent real money selling of GBPUSD through the WMR fix window during the Brexit period (2016-2020). The strategy of simply being long GBPUSD during the fix hour generated significant losses during Brexit as real money hedgers consistently sold GBP. This demonstrates structural flow patterns in FX that can persist for years and are driven by fundamental hedging needs, not speculation.
- **source:** Spectra Markets analysis

---

### Item 5: Bloomberg HDS - 2030 JGB Holders

- **type:** Data table (Bloomberg terminal screenshot)
- **image_file:** page_03_img_00.png
- **title:** "JGB 0.1 03/20/30 #358 - JAPAN GOVT 10-YR" Security Ownership
- **page:** 3
- **data:** Ownership breakdown of the 2030 Japanese Government Bond showing institutional holders
- **assets/instruments:** JGB 0.1% 03/20/2030 (CUSIP RHS27948, 10-year JGB)
- **transforms/calculations:** Position sizes, percentage of outstanding, latest changes
- **metrics:**
  - Bank of Japan: 7,874,000,000 position, **114.76%** of outstanding (due to repo/lending)
  - Government Pension Investment: 281,529,000 (4.10%)
  - Vanguard Group Inc/The: 23,405,863 (0.34%)
  - Nomura Holdings Inc: 6,869,386 (0.10%)
  - Multiple other holders with smaller positions
  - BOJ latest change: +3,621,600,000 (massive accumulation)
- **time_range:** As of January 20, 2023 (file dates visible)
- **x_axis:** N/A (table format)
- **y_axis:** N/A (table format)
- **insight:** The BOJ owns 114.76% of this particular JGB issue - more than 100% because of repo and lending arrangements. This extreme level of central bank ownership illustrates the unprecedented distortions created by yield curve control (YCC). The BOJ has essentially cornered the market in this bond, which has implications for market functioning and the sustainability of YCC policy.
- **source:** Bloomberg Terminal (HDS function)

---

### Item 6: GOOG Hourly Chart with RSI

- **type:** Price chart with RSI indicator panel
- **image_file:** page_03_img_01.jpeg
- **title:** "GOOG hourly chart with RSI"
- **page:** 3
- **data:** Google (GOOG) hourly price chart from approximately August 2022 to January 2023, with Relative Strength Index (RSI) in lower panel
- **assets/instruments:** GOOG (Alphabet Inc.)
- **transforms/calculations:** RSI (Relative Strength Index) - likely 14-period on hourly bars
- **metrics:**
  - Current price: $101.19 (closed at $101, trading $99.50 premarket)
  - RSI reading: 77.47 (overbought, above 80 threshold recently)
  - Price range visible: approximately $80 to $123
- **time_range:** August 2022 to January 2023
- **x_axis:** Date (15, Sep, 19, Oct, 17, Nov, 14, Dec, 19, 2023, 13)
- **y_axis:** Price in USD (top panel: $60-$125); RSI value (bottom panel: 20-80+ range)
- **insight:** Just about every tech stock RSI went >80 on hourly charts. Google is "particularly interesting" given declining ad revenues, multiple investigations (including BOJ), and the challenge from GPT-3/4/5 to its search dominance. The overbought technical condition suggests potential for a pullback. The chart captures the sharp rally from ~$83 lows in late 2022 to $101 by late January 2023.
- **source:** TradingView (watermark visible)

---

### Item 7: Hours of Work to Buy a Gallon of Gasoline

- **type:** Time series line chart
- **image_file:** page_04_img_00.png
- **title:** "How many hours does an average American have to work to buy a gallon of gasoline?"
- **page:** 4
- **data:** Ratio of gasoline price to average hourly wage, expressed in hours of labor per gallon
- **assets/instruments:** Gasoline (consumer commodity), US average hourly earnings
- **transforms/calculations:** Ratio = gasoline price per gallon / average hourly earnings. Expressed in hours (or fraction of an hour) of work required.
- **metrics:**
  - Range: approximately 0.02 to 0.25 hours per gallon
  - Notable peaks: ~0.22 hours (early 1980s oil crisis), ~0.20 hours (2008 oil spike), ~0.18 hours (2022)
  - Current level: appears to be declining from the 2022 peak
  - Long-term trend: relatively stable around 0.05-0.15 hours
- **time_range:** 1990 to 2022 (x-axis labels show every 2 years from 1990)
- **x_axis:** Year (1990, 1992, 1994, ..., 2022)
- **y_axis:** Hours of work per gallon (0 to 0.25)
- **insight:** Framing gasoline prices in terms of labor hours worked provides a real purchasing power perspective. Despite high nominal prices in 2022, the ratio has historically been higher (1980s). The chart supports the "Malthusian theories are always wrong" framing - resources become more affordable over time in real terms due to productivity gains. Current levels are elevated but not unprecedented.
- **source:** Not explicitly stated (likely BLS average hourly earnings + EIA gasoline prices)

---

### Item 8: G10 FX Positioning and Momentum - Summary Scores Table

- **type:** Data table (color-coded heatmap style)
- **image_file:** page_05_img_00.png
- **title:** "G10 FX Positioning and Momentum - Summary scores"
- **page:** 5
- **data:** Composite positioning and momentum scores for G10 currencies on a -10 to +10 scale (all currencies vs USD, where JPY means yen, not USDJPY)
- **assets/instruments:** USD, EUR, CHF, JPY, GBP, AUD, NZD, CAD
- **transforms/calculations:** Composite scoring system aggregating multiple indicators
- **metrics:**
  | Currency | Positioning | Momentum |
  |----------|------------|----------|
  | USD | -3 | -8 |
  | EUR | 4 | 8 |
  | CHF | 0 | 4 |
  | JPY | 2 | 5 |
  | GBP | 2 | 8 |
  | AUD | 3 | 8 |
  | NZD | 4 | 8 |
  | CAD | 1 | 4 |
- **time_range:** Week of January 24, 2023
- **x_axis:** Currency
- **y_axis:** Score (-10 to +10)
- **insight:** Strongly bearish USD positioning (-3) and momentum (-8). EUR, GBP, AUD, NZD all show very high momentum scores (8). This reflects the broad "sell USD" theme driven by soft landing expectations, China reopening, and hawkish ECB. The positioning is less extreme than momentum, suggesting the move has more room to run but crowding risk is building.
- **source:** Spectra Markets proprietary model

---

### Item 9: G10 FX Positioning and Sentiment - Detailed Breakdown Table

- **type:** Data table (color-coded)
- **image_file:** page_05_img_00.png
- **title:** "Positioning and Sentiment"
- **page:** 5
- **data:** Six sub-components of the positioning and sentiment score for each G10 currency
- **assets/instruments:** USD, EUR, CHF, JPY, GBP, AUD, NZD, CAD
- **transforms/calculations:** Individual indicator scores on -10 to +10 scale
- **metrics:**
  | Indicator | USD | EUR | CHF | JPY | GBP | AUD | NZD | CAD |
  |-----------|-----|-----|-----|-----|-----|-----|-----|-----|
  | CFTC Level (% of OI) | 2 | 4 | -3 | 0 | -1 | -6 | 0 | -6 |
  | CFTC 4-Week Change | 2 | -3 | -4 | 5 | -5 | 0 | -1 | -3 |
  | Daily Sentiment Index | -2 | 5 | -2 | 3 | 3 | 2 | 5 | -2 |
  | Risk Reversal (1-month) | -5 | 3 | 3 | -8 | 8 | 10 | 10 | 8 |
  | Risk Reversal (6-month) | -9 | 9 | 6 | 7 | 9 | 10 | 10 | 9 |
  | Spectra FX Positioning | -5 | 5 | 0 | 6 | -1 | 5 | 0 | 2 |
- **time_range:** Week of January 24, 2023
- **x_axis:** Currency
- **y_axis:** Indicator name
- **insight:** Risk reversals show extreme skew against USD (1M: -5, 6M: -9) and strongly favor AUD and NZD (both 10 on 1M and 6M). JPY risk reversal is mixed (-8 on 1M but +7 on 6M). CFTC positioning shows AUD and CAD still have room to build long positions (both at -6). The Spectra FX proprietary positioning estimate shows JPY surprisingly positioned at +6 (long yen), suggesting BOJ hawkish expectations.
- **source:** Spectra Markets, CFTC, Bloomberg (risk reversals)

---

### Item 10: G10 FX Momentum Table

- **type:** Data table (color-coded)
- **image_file:** page_05_img_00.png
- **title:** "Momentum"
- **page:** 5
- **data:** Three momentum indicators for each G10 currency
- **assets/instruments:** USD, EUR, CHF, JPY, GBP, AUD, NZD, CAD
- **transforms/calculations:** RSI, deviation from 20-day MA, deviation from 100-day MA, each scored -10 to +10
- **metrics:**
  | Indicator | USD | EUR | CHF | JPY | GBP | AUD | NZD | CAD |
  |-----------|-----|-----|-----|-----|-----|-----|-----|-----|
  | RSI | -8 | 8 | 3 | 3 | 7 | 7 | 7 | 4 |
  | Deviation from 20-Day | -7 | 6 | 2 | 2 | 7 | 8 | 7 | 5 |
  | Deviation from 100-Day | -10 | 9 | 7 | 10 | 9 | 8 | 9 | 3 |
- **time_range:** Week of January 24, 2023
- **x_axis:** Currency
- **y_axis:** Momentum indicator
- **insight:** USD momentum is at extreme negative levels across all three indicators (RSI: -8, 20D dev: -7, 100D dev: -10). JPY deviation from 100-day MA is at +10 (maximum bullish momentum). EUR, GBP, AUD, NZD all show strong positive momentum across all measures. This is consistent with a broad, powerful USD downtrend.
- **source:** Spectra Markets

---

### Item 11: FX Positioning Bar Charts (Last Week vs This Week)

- **type:** Grouped bar chart (two charts side by side)
- **image_file:** page_05_img_01.png, page_05_img_02.png
- **title:** "FX Positioning" (left) and "FX Momentum" (right)
- **page:** 5
- **data:** Week-over-week comparison of positioning and momentum scores for each G10 currency
- **assets/instruments:** USD, EUR, CHF, JPY, GBP, AUD, NZD, CAD
- **transforms/calculations:** Composite scores from the tables above, displayed as bar charts comparing last week to this week
- **metrics:**
  - FX Positioning: USD moved from ~-2 to -3 (more bearish); EUR stable at ~4-5; JPY moved higher
  - FX Momentum: USD at -8 (extreme); EUR/GBP/AUD/NZD all at 8 (extreme bullish)
- **time_range:** Two weeks comparison (week of Jan 17 vs week of Jan 24, 2023)
- **x_axis:** Currency (USD, EUR, CHF, JPY, GBP, AUD, NZD, CAD)
- **y_axis:** Score (-10 to +10)
- **insight:** Visual representation showing the week-over-week changes. The bar charts make it easy to see that USD positioning and momentum have deteriorated further, while most other currencies are near their highs. The lack of significant movement in positioning despite strong momentum suggests the trend has room to continue, but could also signal complacency.
- **source:** Spectra Markets

---

### Item 12: Bloomberg US Financial Conditions Index

- **type:** Time series line chart
- **image_file:** page_06_img_00.png
- **title:** "Bloomberg US Financial Conditions Index"
- **page:** 6
- **data:** Bloomberg US Financial Conditions Index from late 2020 to January 2023
- **assets/instruments:** Composite index of financial conditions (stocks, credit spreads, money market rates, yields, etc.)
- **transforms/calculations:** Bloomberg's proprietary financial conditions index (higher = looser conditions, lower = tighter)
- **metrics:**
  - Current level: approximately +0.5 to +0.8 (as loose as February 2022)
  - Trough: approximately -1.3 (around September/October 2022)
  - Recovery from trough of ~1.8 index points
  - Peak: approximately +1.3 (early 2021)
- **time_range:** December 31, 2020 to January 2023 (x-axis labels show quarterly dates)
- **x_axis:** Date (12/31/2020, 3/31/2021, 6/30/2021, 9/30/2021, 12/31/2021, 3/31/2022, 6/30/2022, 9/30/2022, 12/31/2022)
- **y_axis:** Index value (range -1.5 to +1.5)
- **insight:** Financial conditions have eased substantially and are now as loose as they were in February 2022, despite the Fed's aggressive rate hikes. This is not just about stocks going up - credit spreads and other contributors to financial conditions are showing even more optimism than equity markets. This supports the soft landing / risk-on narrative but raises questions about whether the Fed will need to do more to tighten conditions.
- **source:** Bloomberg

---
