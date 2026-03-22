# AMFX_21DEC22 — Chart Reproduction Tasks

Source: AMFX 21DEC22 newsletter by Brent Donnelly (Spectra Markets)
Theme: Five contrarian bullish arguments for equities despite overwhelming bearish consensus; "optimism feels crazy right now" as a reason to be optimistic; Japan repatriation myth; 1994/95 rate cycle analog
Date: December 21, 2022

## Charts to Reproduce

### Task 1: SPX with Gas Price Drop Event Markers
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_spx_gas_price_drop_research.json`
- **image_ref:** page_01_img_03.png
- **chart_type:** line with vertical event bands
- **data_sources:** S&P 500 (Yahoo: ^GSPC or FRED: SP500), US gasoline prices (FRED: GASREGW or EIA weekly retail gasoline)
- **what_makes_it_interesting:** Elegant event study visualization — blue vertical bands mark every period when gas prices fell 15%+ in 60 days, overlaid on the SPX price history. The visual pattern is immediate: most blue bands cluster near equity bottoms or early recovery phases. Simple but powerful — the kind of chart that changes how you think about the current gas price decline.
- **reproduction_notes:** Black line for SPX price (log scale implied by long time series). Thick blue vertical bands as event markers. X-axis yearly labels 2004-2022. No y-axis labels visible on SPX (focus is on the pattern, not levels). Clean, minimal design — the blue bands do all the talking.
- **implementation_notes:** Uses SPY-Stocks close price with FRED GASREGW gasoline data. roc(period=60) computes 60-day rate of change (returns fraction, not percentage). Threshold at -0.15 for 15% drop. is_band=true on LineSeriesSpec creates x_plot_bands. GASREGW cache starts from 2009-10, so bands cover 2012-2022 (10 bands found: 2014-2016 oil crash, 2018 Q4 selloff, COVID 2020, 2022 bear). Original chart goes back to 2004 but partial coverage is acceptable.

### Task 2: NASDAQ 1996-2004 Dot-Com Bubble Round Trip
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_nasdaq_dotcom_roundtrip_research.json`
- **image_ref:** page_03_img_00.png
- **chart_type:** line/area with annotations
- **data_sources:** NASDAQ Composite (Yahoo: ^IXIC or Bloomberg: CCMP Index)
- **what_makes_it_interesting:** Beautifully annotated historical analog. The orange/peach shaded area below the peak creates a visual "volume" of excess that had to be unwound. The LTCM bailout horizontal reference line and "Round trip complete" vertical line are key annotations that frame the argument: NASDAQ was still at 3000 going into 2001 (massive premium remaining), unlike current bubble stocks which have already round-tripped. The chart design itself is the argument.
- **reproduction_notes:** Line chart with peach/orange area fill below the price. Blue horizontal line at ~1500 labeled "LTCM bailout." Black vertical line at the round-trip completion point labeled "Round trip complete." Y-axis: 1000-5000. X-axis: 1996-2004 yearly labels. Bloomberg watermark and date stamp at bottom. The area fill between peak and the LTCM level is the visual centerpiece.
- **implementation_notes:** Uses `assets: []` with `economic_indicators(series_id='NASDAQCOM', use_alfred=False)`. Key fix: ALFRED only tracks NASDAQCOM from 2014, but regular FRED mode (`use_alfred=False`) has full history back to 1971. Removed SPY anchor — empty assets + FRED observation dates builds the grid. 2371 data points covering full 1996-2004 dot-com cycle.

### Task 3: Japan Foreign Bond Sales vs USD Cash Holdings (Deutsche Bank)
- **status:** BLOCKED
- **image_ref:** page_04_img_00.jpeg
- **chart_type:** dual-panel line charts
- **data_sources:** Japanese MOF International Securities Transactions data (monthly), BOJ flow of funds; Deutsche Bank research data; potentially FRED or BOJ statistical database for Japanese net purchases of foreign securities and USD cash holdings
- **what_makes_it_interesting:** Debunks the popular JPY repatriation trade in two panels. Left panel shows record selling of foreign bonds (bearish for foreign assets). Right panel is the twist: proceeds kept in USD cash, NOT converted to JPY. The two-panel design with red annotations creates a "yes, but..." narrative structure. This is the kind of data that separates informed traders from consensus followers.
- **reproduction_notes:** Two side-by-side panels. Left: "Japan has already sold foreign bonds" — line chart of 12m change in Japanese net purchases (yen trillions), range -30 to +40, with red annotation arrow. Right: "But Japan has not bought JPY" — USD cash held by Japanese (12m change, bn $), range -100 to +150, with red annotation. Both have Source: Deutsche Bank, Bloomberg Finance.
- **blocked_reason:** Deutsche Bank proprietary research data. Japanese MOF International Securities Transactions and BOJ flow of funds data not available through FRED or polygon. No programmatic data source for these specific capital flow metrics.

### Task 4: G10 FX Positioning and Momentum Scorecard
- **status:** BLOCKED
- **image_ref:** page_05_img_00.png, page_05_img_01.png, page_05_img_02.png
- **chart_type:** heatmap table + grouped bar charts
- **data_sources:** CFTC Commitments of Traders (positioning), RSI calculations, 20-day and 100-day moving average deviations, risk reversals (options market), Daily Sentiment Index
- **what_makes_it_interesting:** Comprehensive FX positioning dashboard combining 6 positioning inputs and 3 momentum inputs into a single -10 to +10 scoring framework. The color-coded heatmap table makes extreme readings pop visually. The paired bar charts (positioning vs momentum, last week vs this week) show direction of change. This is a reusable template — the METHODOLOGY is as valuable as any single snapshot.
- **reproduction_notes:** Three-part composite. (1) Heatmap tables: blue = positive, red = negative, white = neutral. Rows: CFTC Level, CFTC 4-Week Change, DSI, Risk Reversal 1m/6m, Spectra FX Positioning; Momentum: RSI, Dev from 20-Day, Dev from 100-Day. Columns: USD, EUR, CHF, JPY, GBP, AUD, NZD, CAD. (2) Grouped bar chart "FX Positioning" — gray (last week) vs blue (this week). (3) Grouped bar chart "FX Momentum" — same format. All on -10 to +10 scale.
- **blocked_reason:** Spectra Markets proprietary scoring system. Data inputs include CFTC COT (available), but the -10 to +10 scoring methodology, Daily Sentiment Index, risk reversal lookback normalization, and Spectra FX Positioning index are all proprietary. The composite score cannot be reconstructed from public data alone.

### Task 5: FX Strategy Bulls and Bears for 2023
- **status:** BLOCKED
- **image_ref:** page_06_img_00.png
- **chart_type:** horizontal diverging bar chart
- **data_sources:** Compilation of bank FX strategy team year-ahead forecasts (manual aggregation from published research)
- **what_makes_it_interesting:** Captures the consensus trade at a glance — JPY massively bullish, USD massively bearish. The diverging bar format (green = bull, pink/red = bear) makes the skew in consensus immediately visible. As a contrarian tool, this is gold: when EVERYONE agrees, the trade is likely crowded. The chart is simple but the data aggregation is the value.
- **reproduction_notes:** Horizontal bars centered on zero. Green bars extend right (bulls), pink bars extend left (bears). Currencies on y-axis: JPY, AUD, NZD, EUR, CAD, CHF, NOK, SEK, GBP, USD. X-axis: -15 to +15. Title: "G10 Bull / Bear." Clean white background.
- **blocked_reason:** Manual aggregation of bank FX strategy team year-ahead forecasts. This is a one-time editorial compilation, not a data feed. No programmatic way to reconstruct the bull/bear counts per currency from public data.

### Task 6: SPX vs US 2-Year Yield 1992-1998 (Rate Cycle Analog)
- **status:** DONE
- **image_ref:** page_06_img_01.png
- **chart_type:** dual-axis overlay (line + line)
- **data_sources:** S&P 500 (Yahoo: ^GSPC or FRED: SP500), US 2-Year Treasury Yield (FRED: DGS2 or Bloomberg: USGG2YR)
- **what_makes_it_interesting:** The 1994/95 analog is the contrarian bull case in one chart. Stocks struggled during rate hikes (1994), then exploded upward once the Fed pivoted — "massive bull market." The annotated dual-axis overlay with black (SPX) and orange (2Y yield) makes the lead-lag relationship obvious. The annotations ("Stocks struggled as rates went up dramatically in 1994" and "As soon as the Fed turned... Massive bull market") convert the chart from data into narrative.
- **reproduction_notes:** Black line = SPX (left axis, ~400 to 1200). Orange line = USGG2YR (right axis, ~4% to 14%). Two red text annotations with arrows. Bloomberg format with last price legend box. X-axis: 1992-1998 yearly. The key visual: 2Y yield peaks in 1994, SPX accelerates from 1995 onward.
- **implementation_notes:** Uses `assets: []` with FRED SP500 + DGS2 loaded via common_economic_indicators. Empty assets array means no SPY grid dependency. FRED data covers 1991-1998 via cached SP500/DGS2 series. Study renders with 1979 data points — full coverage of the 1994 rate cycle analog.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| AMZN 2018-2022 (page_02_img_00.png) | TradingView candlestick with annotations — interesting narrative (bubble round-trip) but the annotations are highly specific to Dec 2022 context. The data (AMZN price) is trivially available. The NASDAQ 1996-2004 chart makes the same point more powerfully with historical perspective. |
| ARKK 2018-2022 (page_02_img_01.jpeg) | Same as AMZN — TradingView candlestick showing bubble deflation. The magazine cover overlay is amusing but not reproducible as a quantitative chart. Redundant with the NASDAQ analog. |
| Nike 1-month chart (page_03_img_01.jpeg) | Extremely short-term candlestick (1 month) with a single purple dot marking pre-market level. Too ephemeral — the insight is "earnings surprised positively" which is a text observation, not a reproducible chart pattern. |
| FedEx 1-month chart (page_03_img_02.png) | Same as Nike — short-term candlestick with pre-market annotation. No lasting analytical value. |
