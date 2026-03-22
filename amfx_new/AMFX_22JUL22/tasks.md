# AMFX_22JUL22 — Chart Reproduction Tasks

Source: AMFX 22JUL22 newsletter by Brent Donnelly (Spectra Markets)
Theme: Soft data leads hard data — ISM New Orders vs Initial Claims divergence as a recession leading indicator; BOJ YCC expectations survey
Date: July 22, 2022

## Charts to Reproduce

### Task 1: Initial Claims vs ISM New Orders Percentile Ranking (1996-2022)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_claims_vs_ism_percentile_research.json`
- **notes:** ISM New Orders sub-index (NAPMNOI) discontinued on FRED. Used Industrial Production (INDPRO) as proxy for manufacturing activity indicator. ICSA (Initial Claims) inverted via `100 - percentrank`. Rolling 750-day (~3yr) percentile. Data range 2003-2022 (SPY cache starts 2003-09-10, ICSA ALFRED starts 2009-06-04). Charts render correctly with dual percentile overlay and spread.
- **image_ref:** page_01_img_03.png
- **chart_type:** dual line overlay with letter annotations
- **data_sources:** ISM Manufacturing New Orders (FRED: NEWORDER or ISM direct), Initial Jobless Claims (FRED: ICSA); both converted to percentile rankings within the 1996-2022 window
- **what_makes_it_interesting:** This is one of the best "soft leads hard" charts. Two series transformed to percentile rankings so they share a common scale — ISM New Orders (soft/survey data, black) consistently leads Initial Claims (hard/labor data, orange) at economic turning points. The annotated letter labels (A through I) walk through each historical episode: true signals (A, C-D, E, H) vs false alarms (B, F, G). The current reading "I" sits at the critical question mark. The chart design is outstanding — high contrast orange vs black, large bold annotations, clear "Strong employment / strong new orders" and "Weak employment / weak new orders" labels at top and bottom.
- **reproduction_notes:** Orange line = Initial Claims percentile (inverted — high = strong employment). Black line = ISM New Orders percentile. Y-axis: implied 0-100 percentile scale. X-axis: 1996-2022 biannual labels. Green letter annotations (A-I) at turning points with descriptive labels. Top label: "Strong employment / strong new orders" (green/orange). Bottom label: "Weak employment / weak new orders" (green/orange). Legend at bottom: orange box "Initial Claims", black line "ISM New Orders". This is a reusable framework — the percentile transformation is the key innovation.

### Task 2: BOJ Yield Curve Control Survey Results
- **status:** BLOCKED
- **reason:** Static one-time poll data (51.5%/30.3%/18.2%) from Fred Goodwin weekly survey. No FRED series or time-series data available. EpochScript requires time-series market data to generate charts — cannot reproduce a static categorical horizontal bar chart from a single survey snapshot.
- **image_ref:** page_03_img_00.png
- **chart_type:** horizontal bar
- **data_sources:** Fred Goodwin weekly poll data (specific to July 2022 survey); for reproduction, could use any sentiment survey or create a generic YCC expectation tracker
- **what_makes_it_interesting:** Simple but captures a moment in time — the market had largely given up on YCC ending in 2022 (51.5% unchanged, only 18.2% abandoned). With hindsight, this was wrong — BOJ surprised with a YCC tweak just 5 months later in December 2022. The chart shows how consensus gets lulled into complacency. The clean teal gradient on the bars is visually appealing.
- **reproduction_notes:** Three horizontal bars in teal/dark blue gradient. "Remain unchanged 51.5%" (largest, with checkmark icon), "Get Tweaked 30.3%" (medium), "Be Abandoned 18.2%" (smallest). X-axis: 0% to 55% in 5% increments. Title: "Japan's YCC for the rest of 2022 will:". Clean white background. The poll format is a useful template for capturing market consensus at any point in time.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| "Who Americans spend their time with, by age" (page 4) | Social/demographic line chart from Our World in Data. Interesting lifestyle observation (time with friends declines after age 18) but purely sociological, not financial data. Used as a sidebar fun fact, not market analysis. |
