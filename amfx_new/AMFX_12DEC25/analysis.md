# AMFX 12DEC25 - Analysis

## PDF Metadata
- **Title:** Rabbit Hole #14 - Jinx: Time Person of the Year
- **Date:** December 12, 2025
- **Author:** Brent Donnelly, Spectra Markets
- **Pages:** 8
- **Read time:** 8 minutes
- **Theme:** Time Magazine's Person of the Year as a contrarian market indicator. When corporate leaders or specific industries are featured, the associated stocks tend to underperform significantly in the following 1-2 years. The 2025 cover features "The Architects of AI."

## Summary
Donnelly examines the historical track record of Time Magazine's Person of the Year when it features a corporate head, CEO, or industry leader. He identifies 9 such instances (1928-2025) and finds a strong contrarian pattern: stocks of featured companies/industries average +44% in the cover year but then decline -25.7% in the year after and -16.7% two years later. Only 13% of featured stocks are up one year after the cover. The 2025 cover features "The AI Architects" (Zuckerberg, Lisa Su, Musk, Jensen Huang, Sam Altman, Demis Hassabis, Dario Amodei, Fei-Fei Li), suggesting the MANTA basket (Meta, AMD, Nvidia, Tesla, Alphabet) may underperform in 2026. He also includes historical Goldman Sachs 1987 research notes on computer hardware to show parallels between tech hype cycles.

## Current Views (from sidebar)
- No tactical / short-term trades
- Medium-term: 03FEB25 USDCNH Put Fly 6.98/6.88/6.78, 1X2X1 for 15bps (7.0565 s/r)

---

## Visual Elements Inventory

### Page 1

| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 1 | Spectra Markets logo (header) | DISCARD | not extracted (below size threshold) | Company branding |
| 2 | am/FX logo | DISCARD | not extracted (below size threshold) | Newsletter branding |
| 3 | Time Magazine cover - Pokemon (1999) | DISCARD | page_01_img_00.jpeg | Historical magazine cover used as illustration (no chart data) |
| 4 | Time Magazine cover - Obesity in America (2004) | DISCARD | page_01_img_01.jpeg | Historical magazine cover used as illustration |
| 5 | Time Magazine Person of the Year 2025 cover - AI Architects | DISCARD | page_01_img_02.jpeg | Current magazine cover used as illustration |

### Page 2

| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 6 | "When TIME Person of the Year features a Corporate Leader or Specific Industry" performance table | **KEEP** | page_02_img_00.png | Quantitative data table showing stock performance before and after TIME covers |
| 7 | Time Magazine 1929 cover (Owen D. Young) | DISCARD | page_02_img_01.jpeg | Historical magazine cover thumbnail |

### Page 3

| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 8 | Time Magazine 1982 cover - "Machine of the Year: The Computer Moves In" | DISCARD | page_03_img_00.jpeg | Historical magazine cover (no chart data) |
| 9 | Time Magazine 1999 cover - Jeff Bezos (Person of the Year) | DISCARD | page_03_img_01.jpeg | Historical magazine cover photo |
| 10 | TSLA weekly price chart, 2020 to 2023 | **KEEP** | page_03_img_02.png | Price chart showing TSLA performance with TIME cover annotation |

### Page 4

| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 11 | Goldman Sachs 1987 Investment Research note (page with table) | **KEEP** | page_04_img_00.jpeg | Historical research document showing DEC market share factors table |
| 12 | Goldman Sachs 1987 note - "Factors Influencing DEC's Market Share and Margins Gains" table | **KEEP** | page_04_img_00.jpeg (same image as #11) | (Part of same document as #11 -- single scan with two visible sections) |

### Page 5

| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 13 | Goldman Sachs 1987 Research - Computer Hardware Industry charts (Relative Price/Performance + 32-Bit Multi-User Micro Evolution) | **KEEP** | page_05_img_00.jpeg | Two quantitative charts from 1987 GS research showing computer hardware price/performance and technology evolution |

### Page 6

| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 14 | Next week's trading calendar table | **KEEP** | page_06_img_00.png | Structured data table of upcoming economic events and central bank decisions |

### Page 7

| # | Element | Classification | Image File | Reason |
|---|---------|---------------|------------|--------|
| 15 | Time Magazine covers (Pokemon 1999 + Obesity 2004) - larger versions | DISCARD | not extracted (no separate images on page 7) | Repeat of magazine covers from page 1, decorative (captioned "There is nothing new under the sun") |

### Page 8

No visual elements (disclaimer page only).

---

## Detailed Analysis of KEPT Items

### KEPT #1: TIME Person of the Year - Corporate Leader Stock Performance Table

- **type:** Data table with color-coded cells
- **image_file:** page_02_img_00.png
- **title:** "When TIME Person of the Year features a Corporate Leader or Specific Industry"
- **page:** 2
- **data:** For each TIME Person of the Year cover featuring a corporate leader/industry (9 instances from 1928-2025), shows the year, person, associated company ticker, stock price change during the cover year, change in the year after, and change two years later.
- **assets/instruments:** Chrysler, RCA, GM, IBM/HP/AAPL/TXN/TAN/CBU (1982 "The Computer"), TBS/A (Ted Turner 1991), INTC (Andrew Grove 1997), AMZN (Jeff Bezos 1999), TSLA (Elon Musk 2021), and NVDA/TSLA/META/AMD/GOOG (2025 "The AI Architects" -- results TBD marked with "?")
- **transforms/calculations:** Stock price returns over three periods: during cover year, 1 year after, 2 years after. Summary statistics: Average, Median, % up.
- **metrics:**
  - **During cover year:** Average +44.0%, Median +40.4%, 88% up
  - **In the year after:** Average -25.7%, Median -7.6%, only 13% up
  - **Two years later:** Average -16.7%, Median -21.1%, 75% (but note: this mixes some recoveries)
  - Notable individual results:
    - 1928 Chrysler: +127.6% during, -49.2% after, -58.3% two years
    - 1929 RCA (Owen D. Young): -32.3% during, -59.1% after, -81.8% two years
    - 1999 Amazon (Bezos): +35.2% during, -85.8% after, -75.2% two years
    - 2021 Tesla (Musk): +40.4% during, -65.0% after, -29.5% two years
    - 1997 Intel (Grove): +7.0% during, +68.8% after, +134.4% two years (the ONLY positive outlier)
- **time_range:** 1928-2025 (historical sample of 9 instances over ~97 years)
- **x_axis:** N/A (table rows are individual cover year events)
- **y_axis:** N/A (table columns are return periods)
- **insight:** TIME Person of the Year is a strong contrarian indicator for stocks when it features corporate leaders or industries. The average stock declines 25.7% in the year following the cover. Only 1 out of 8 historical instances (Andrew Grove/Intel 1997) saw the stock rise in the following year -- and that was because Intel rode the dotcom bubble for two more years before crashing. The 2025 cover featuring "The AI Architects" suggests MANTA stocks (Meta, AMD, Nvidia, Tesla, Alphabet) could significantly underperform in 2026.
- **source:** Brent Donnelly's original research (stock returns compiled from historical data)

---

### KEPT #2: TSLA Weekly Price Chart, 2020 to 2023

- **type:** Candlestick/OHLC weekly price chart with annotation
- **image_file:** page_03_img_02.png
- **title:** "TSLA weekly, 2020 to 2023"
- **page:** 3
- **data:** Tesla (TSLA) weekly price data
- **assets/instruments:** TSLA (Tesla Inc.)
- **transforms/calculations:** None visible (raw price). The 2021 TIME Person of the Year cover (Elon Musk) is annotated on the chart with a small inset image of the cover placed near the price peak.
- **metrics:** Price range: approximately $40 to $400+. Peak near the cover annotation, followed by a crash to ~$100-120 area.
- **time_range:** Mid-2020 to late 2023 (approximately 3.5 years)
- **x_axis:** Time (monthly markers: Jul 2020, 2021, Jul 2021, 2022, Jul 2022, 2023, Jul 2023)
- **y_axis:** Price (USD, scale $0-$400)
- **insight:** Visually demonstrates the contrarian indicator in action. TSLA peaked near the time of Musk's 2021 TIME Person of the Year cover and subsequently fell approximately 65% in the following year. The cover perfectly marked the top.
- **source:** Not explicitly stated (likely Bloomberg terminal)

---

### KEPT #3: Goldman Sachs 1987 Research Note - DEC Market Share Analysis

- **type:** Scanned document with embedded table
- **image_file:** page_04_img_00.jpeg
- **title:** Goldman Sachs Investment Research - Table 6: "Factors Influencing DEC's Market Share and Margins Gains"
- **page:** 4
- **data:** Two-column table of Negative vs. Positive factors for Digital Equipment Corporation (DEC):
  - **Negative:** IBM's 9370/HP's Spectrum, More powerful micros, UNIX is for real, Competition for VARs
  - **Positive:** Lower dollar, U.S. economic improvement, Revenue/fixed cost growth, More new products
- **assets/instruments:** DEC (Digital Equipment Corporation), IBM, HP
- **transforms/calculations:** Qualitative factor analysis
- **metrics:** N/A (qualitative assessment)
- **time_range:** 1987 (publication date of the research note)
- **x_axis:** N/A
- **y_axis:** N/A
- **insight:** Included as a historical parallel to current AI hype. DEC was a dominant computer maker in the 1980s that eventually became obsolete. Goldman Sachs noted momentum was "likely to change very gradually" and would slow "before it is evident in reported numbers." This is a cautionary analogy for current AI leaders. Also demonstrates that research report formatting has been remarkably consistent for ~40 years.
- **source:** Goldman Sachs Investment Research (1987), archived at Computer History Museum

---

### KEPT #4: Goldman Sachs 1987 - Computer Hardware Industry Charts

- **type:** Two scatter/line charts in a single scanned page
- **image_file:** page_05_img_00.jpeg
- **title:** "Computer Hardware Industry - Relative Price/Performance" (top chart) and "32-Bit Multi-User Micro Evolution" (bottom chart)
- **page:** 5
- **data:**
  - Top chart: Relative price/performance ($/MIP) for computer hardware companies: IBM (highest price, ~$160-180), DEC (~$60-70), microVAXII (~$20-30), COMPAQ (~$6-10) plotted against MIPS (millions of instructions per second)
  - Bottom chart: 32-bit multi-user micro evolution over time (1979-1989), showing progression from MOT 68000 to Sun Microsystems, with various chips/systems plotted (MOT 68010/20, Intel 80386, Micro-VAX II, HP 850, MOT 68030, MIPS Family, Sun Microsystems)
- **assets/instruments:** IBM, DEC, COMPAQ, Sun Microsystems, Intel, Motorola
- **transforms/calculations:** Price/performance ratio ($/MIP on y-axis, log scale), MIPS throughput
- **metrics:** $/MIP ratios: IBM ~$160-180, DEC ~$60-70, microVAXII ~$20-30, COMPAQ ~$6-10. MIPS scale: 1-70 (top chart), 1-10 (bottom chart)
- **time_range:** Top chart: snapshot (circa 1987). Bottom chart: 1979-1989 (10 years)
- **x_axis:** Top: MIPS (millions of instructions per second, log scale 1-70). Bottom: Time (1979-1989)
- **y_axis:** Top: $/MIP (price per million instructions). Bottom: MIPS (performance level)
- **insight:** Historical parallel to current AI hardware competition. Shows how the computer hardware industry evolved rapidly in the 1980s with dramatic price/performance improvements and new entrants disrupting incumbents. IBM commanded a massive price premium despite similar performance, similar to how NVDA currently commands premium valuations. The rapid technology evolution eventually commoditized hardware margins.
- **source:** Goldman Sachs Investment Research (1987)

---

### KEPT #5: Next Week's Trading Calendar

- **type:** Structured data table (event calendar)
- **image_file:** page_06_img_00.png
- **title:** "Next week's trading calendar"
- **page:** 6
- **data:** Economic data releases and central bank decisions for the week of December 15-19, 2025, organized by time zone/session (Before NY open, NY AM, NY PM, Asia) and day of week (Monday-Friday)
- **assets/instruments:** Multiple currencies/economies: USD, GBP, EUR, CAD, JPY, AUD, NZD, NOK, SEK
- **transforms/calculations:** N/A
- **metrics:** Event names and times (all times NYC):
  - **Key events highlighted:**
    - Tuesday: US Nonfarm Payrolls 8:30, US Retail Sales 8:30, Germany PMIs 3:30, UK PMIs 4:30
    - Wednesday: UK CPI 2:00, Germany IFO 4:00, US 20-Year Bond Auction 13:01
    - Thursday: Riksbank/Norges Bank/BoE/ECB/BoJ interest rate decisions, US CPI 8:30, US Initial Claims
    - Friday: UK Retail Sales 2:00, Canada Retail Sales 8:30
- **time_range:** December 15-19, 2025
- **x_axis:** Day of week (Mon-Fri)
- **y_axis:** Session time (Before NY open, NY AM, NY PM, Asia)
- **insight:** Described as "absolutely JAMMED" -- an unusually dense week with multiple major central bank decisions (Riksbank, Norges Bank, BoE, ECB, BoJ) plus US CPI and Nonfarm Payrolls all in the same week. This concentration of risk events is notable for position management.
- **source:** Spectra Markets (Brent Donnelly)

---

## Quantitative Content Assessment

This issue is **highly relevant for quantitative research**. The centerpiece is original research on the TIME Person of the Year as a contrarian stock market indicator:

1. **Performance table (KEPT #1):** A backtest of 9 instances over 97 years showing strong contrarian signal (avg -25.7% in year after cover). This is directly reproducible and testable.
2. **TSLA chart (KEPT #2):** Visual confirmation of the most recent instance (2021 cover, 65% drawdown).
3. **Historical GS research (KEPT #3 and #4):** Parallel to current AI hype cycle, showing how dominant tech hardware companies were eventually disrupted.
4. **Trading calendar (KEPT #5):** Operational data for position management.

**Relevance for quant research:** High. The TIME Person of the Year contrarian indicator is a novel, testable hypothesis with clear rules: when TIME features a corporate leader or industry, go short the associated stocks. The small sample size (n=9) is a limitation but the effect size is large and consistent (7/8 negative in the year after, only exception was Intel riding into the dot-com peak).
