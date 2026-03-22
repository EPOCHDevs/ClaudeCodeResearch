# AMFX_12DEC25 — Chart Reproduction Tasks

Source: AMFX 12DEC25 newsletter by Brent Donnelly (Spectra Markets)
Theme: Rabbit Hole #14 — TIME Person of the Year as a contrarian stock market indicator; AI hype parallel to 1980s computer hardware
Date: December 12, 2025

## Charts to Reproduce

### Task 1: TIME Person of the Year — Corporate Leader Stock Performance Table
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_time_poty_contrarian_research.json`
- **output:** `project/research_studies/test_runner/amfx_time_poty_contrarian_research`
- **image_ref:** page_02_img_00.png
- **chart_type:** table (color-coded heatmap cells)
- **data_sources:** Historical stock price data (Yahoo Finance or similar) for Chrysler (1928-1930), RCA (1929-1931), GM (1955-1957), IBM/HP/AAPL/TXN/TAN/CBU basket (1982-1984), TBS/A (1991-1993), INTC (1997-1999), AMZN (1999-2001), TSLA (2021-2023), NVDA/TSLA/META/AMD/GOOG basket (2025-TBD).
- **what_makes_it_interesting:** A genuinely novel contrarian indicator with a 97-year backtest. The color-coded table immediately tells the story — green during the cover year, then a sea of red in the year after. Average -25.7% in the year after, only 13% up. The 2025 row with "?" for AI architects is a fantastic forward-looking call. This is Donnelly at his best — original research, well-presented, with a clear trading implication.
- **reproduction_notes:** Table with columns: Year, Person of the Year, Company, Stock Price Change During Cover Year (blue/green shading), In The Year After (red/pink shading for negative), 2 Years Later (red/pink). Summary row at bottom with Average, Median, % Up. Green = positive returns, red/pink = negative returns. The 2025 row lists NVDA, TSLA, META, AMD, GOOG with "?" for future returns. Clean, spreadsheet-style design with bold headers.
- **implementation_notes:** Uses TSLA, AMZN, INTC as live assets (2019-2024) to show rolling 1Y returns and price trends for the three most recent TIME cover stocks. Historical averages (1928-2025) hardcoded into a 3x3 summary_table showing Cover Year (+44.0% avg), Year After (-25.7% avg), and 2 Years Later (-16.7% avg) with Average/Median/% Up columns. Pre-1982 stocks (Chrysler, RCA, GM) and TBS/A not available in Polygon. Cards show current 1Y return, max drawdown from 52W high, and period peak for each asset.

### Task 2: TSLA Weekly Price Chart with TIME Cover Annotation
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_tsla_time_cover_research.json`
- **output:** `project/research_studies/test_runner/amfx_tsla_time_cover_research`
- **image_ref:** page_03_img_02.png
- **chart_type:** candlestick with annotation overlay
- **data_sources:** TSLA weekly OHLC data (Yahoo Finance), 2020-2023
- **what_makes_it_interesting:** The visual is immediately compelling — the TIME magazine cover photo of Musk is placed right at the price peak, with a red line showing the connection between the cover timing and the subsequent 65% crash. It is a single image that tells the entire contrarian indicator story. The candlestick format emphasizes the volatility and the magnitude of the collapse.
- **reproduction_notes:** TSLA weekly candlestick chart, mid-2020 to late 2023. Price range $0-$400. The TIME Person of the Year cover (December 2021) is annotated with a small inset image near the ~$380-400 peak. Red annotation lines connect the cover to the peak area. Black candlesticks on white background. X-axis shows Jul 2020, 2021, Jul 2021, 2022, Jul 2022, 2023, Jul 2023. Bloomberg-style formatting.
- **implementation_notes:** Uses TSLA-Stocks daily data (April 2020 to Jan 2024). Chart 1 shows TSLA close with 50d/200d MAs and a horizontal reference line at the cover date price (~$352). Chart 2 shows % distance from 52-week high, highlighting the -73% max drawdown. Cards show peak ($409.97), trough, and max drawdown. EpochScript does not support candlestick charts or image overlays, so the daily close line with MAs is the closest reproduction. The TV chart view does show native OHLC candlesticks.

### Task 3: Real Policy Rates Comparison Table (from AMFX_12DEC25 calendar context)
- **status:** BLOCKED
- **image_ref:** page_06_img_00.png
- **chart_type:** table (economic calendar)
- **data_sources:** Central bank schedules, economic release calendars
- **what_makes_it_interesting:** The visual hierarchy is excellent — font size scales with event importance (BOJ, BoE, ECB in huge bold red; secondary events in medium text; minor events in small text). The week of Dec 15-19, 2025 was described as "absolutely JAMMED" with Riksbank, Norges Bank, BoE, ECB, BOJ, plus US CPI and NFP all in one week. The design itself is a reusable template.
- **reproduction_notes:** Grid layout: rows = sessions (Before NY open, NY AM, NY PM, Asia), columns = Mon-Fri. Major events in large bold red text (central bank decisions), medium events in bold black (US CPI, NFP), minor events in regular text. All times NYC. Clean table borders, white background.
- **blocked_reason:** This is a static text calendar of economic events for a specific week (Dec 15-19, 2025). It is not data-driven -- the content is curated event names and times with visual hierarchy (font size, color, bold). EpochScript has no mechanism for rendering arbitrary text tables with formatting variations. There is no time-series data to compute or display. The calendar would need a custom HTML/CSS template, not an EpochScript research definition.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| Goldman Sachs 1987 DEC research note (page_04_img_00.jpeg) | Historical scanned document — interesting as a narrative parallel to AI hype, but it is a scanned typewriter-era research page, not a reproducible data visualization. The qualitative factor table (IBM's 9370, UNIX is for real, etc.) is text, not data. |
| Goldman Sachs 1987 Computer Hardware charts (page_05_img_00.jpeg) | Two charts from a 1987 GS research note ($/MIP price-performance and 32-bit micro evolution). Interesting historical artifact showing how hardware was commoditized, but the data is from 1987, low resolution scan, and the specific companies (DEC, Compaq, microVAXII) are all defunct. The narrative parallel to AI is valuable but the charts themselves are not worth reproducing — the insight lives in the text comparison, not the data. |
| TIME magazine covers (pages 1, 2, 3) | Decorative magazine cover images used as illustrations |
