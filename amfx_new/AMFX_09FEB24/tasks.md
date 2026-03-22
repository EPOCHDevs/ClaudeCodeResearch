# AMFX_09FEB24 — Chart Reproduction Tasks

Source: AMFX 09FEB24 newsletter by Brent Donnelly (Spectra Markets)
Theme: Rabbit Hole #11 — The negative externalities of smartphones and social media on teenage mental health (cross-post from 13D Research & Strategy by Kiril Sokoloff)
Date: February 15, 2024

## Charts to Reproduce

### Task 1: US Polycrisis Dashboard — Four-Panel Macro Trends
- **status:** DONE (partial — Panel 4 only)
- **definition:** `project/definitions/test_runner/amfx_us_federal_debt_research.json`
- **image_ref:** page_02_img_00.png
- **chart_type:** multi-panel (stacked bar, line, bar)
- **data_sources:** NOAA (billion-dollar disasters CPI-adjusted), US Customs & Border Protection (migrant encounters), CDC WONDER (drug overdose deaths), CBO (federal debt held by public). Original slides from Bruce Mehlman/Mehlman Consulting.
- **what_makes_it_interesting:** Four accelerating negative trends presented side-by-side create a visceral "polycrisis" narrative. The visual rhythm of all four charts bending upward/rightward simultaneously is powerful. Great macro dashboard design — each panel uses the right chart type for its data (stacked bars for composition, line for trend, bars for magnitude, bars with projection for forward-looking).
- **reproduction_notes:** Panel 1 (Natural Disasters) = stacked bar by disaster type (drought, flooding, freeze, tropical cyclone, severe storm, wildfire, winter storm), 1980-2023, CPI-adjusted, y-axis in billions. Panel 2 (Illegal Immigration) = stacked bar (port of entry vs. between ports), 1960-2023, annotation "2023 saw 2.5 million". Panel 3 (Drug Overdose Deaths) = bar chart with data labels, 2015-2023, in thousands. Panel 4 (Debt) = bar chart, 2013-2028, "You Are Here" annotation, y-axis in trillions. Color palette varies by panel. Sources at bottom.
- **implementation_notes:** Only Panel 4 (Federal Debt) was reproducible. FRED series FYGFDPUN (quarterly, millions) converted to trillions, plus FYGFGDQ188S (debt as % GDP) for context. Panels 1-3 blocked because:
  - Panel 1 (Natural Disasters): NOAA NCEI billion-dollar disaster data NOT available on FRED
  - Panel 2 (Illegal Immigration): CBP migrant encounter data NOT available on FRED
  - Panel 3 (Drug Overdose Deaths): CDC WONDER overdose data NOT available on FRED
- **output:** 2 charts (debt level line, debt/GDP % area) + 4 cards (current $28.3T, peak, debt/GDP 96.5%, YoY change $1.98T). Date range: 2013-01-01 to 2024-12-31.

### Task 2: Smartphone Usage vs. Mental Health Outcomes (Six-Panel Dose-Response)
- **status:** BLOCKED
- **image_ref:** page_06_img_00.png
- **chart_type:** multi-panel line chart with confidence intervals
- **data_sources:** PLOS One (Hanyang University Medical Center study of 50,000+ Korean adolescents, published Dec 2023). Raw data likely not publicly available — would need to reproduce from published figures.
- **what_makes_it_interesting:** A beautifully structured six-panel dose-response visualization. The exponential curve in Panel F (Smartphone Overdependence, odds ratio shooting to 5-6x at >8 hours) is visually arresting. The confidence interval bands add credibility. Each panel uses the same axis structure but tells a different story — stress is relatively flat, but sleep, suicide, and substance use all curve upward.
- **reproduction_notes:** Six panels (A-F): Stress, Sleep dissatisfaction, Depressive symptoms, Suicide (3 lines: idea/attempt/plan), Substance use (alcohol/smoking), Smartphone overdependence. X-axis = smartphone hours (0, 0-2, 2-4, 4-6, 6-8, >8). Y-axis = odds ratio (most panels 0-2, Panel F goes to 6). Each line has shaded 95% CI band. Different colors per series within panels (red, green, blue for suicide; yellow, purple for substance use; cyan for others). Background colors differ by panel.
- **blocked_reason:** This is cross-sectional academic survey data (odds ratios from a Korean adolescent health study), NOT time-series data. EpochScript operates on time-series bars (daily/intraday). The x-axis is categorical (smartphone usage hours: 0, 0-2, 2-4, 4-6, 6-8, >8), not temporal. There is no FRED series, no market data feed, and no API endpoint that provides this data. The raw study data is not publicly available — only the published figures exist.

### Task 3: Mental Wellbeing vs. Age of First Smartphone (Sapien Labs)
- **status:** BLOCKED
- **image_ref:** page_07_img_00.png
- **chart_type:** dual-panel line chart with legend scale
- **data_sources:** Sapien Labs / Global Mind Project (28,000 individuals ages 18-24, 41 countries). Published data from The Global Mind Report.
- **what_makes_it_interesting:** The dual-panel design is elegant — left panel shows the absolute score (MHQ), right panel shows the distress rate, and the bottom legend explains the MHQ scale. The gender gap widening with earlier smartphone adoption is a striking finding. The monotonic improvement from age 5 to age 18 is visually clear and persuasive.
- **reproduction_notes:** Left panel: Average MHQ score by age of first smartphone (5-18), two lines (Males 18-24 in dark blue, Females 18-24 in light blue). Males range from ~-10 to ~45, Females from ~-18 to ~25. Right panel: % Distressed/Struggling by age, same two lines. Females from ~75% down to ~45%, Males from ~55% down to ~35%. Bottom: MHQ scale legend bar from -100 (Distressed) through Struggling, Enduring, Managing, Succeeding, to 200 (Thriving). Clean black-and-blue color scheme.
- **blocked_reason:** This is cross-sectional survey data from Sapien Labs Global Mind Project (28,000 individuals across 41 countries), NOT time-series data. EpochScript operates on time-series bars. The x-axis is "age of first smartphone ownership" (5-18), not temporal. The MHQ scores and distress percentages are survey aggregates, not available as any financial/economic time series. No FRED series, no market data feed exists for this data.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| Brain neuroimaging (page_10_img_00.jpeg) | Scientific fMRI brain scan — visually interesting but not reproducible with financial/economic data. This is a neuroscience figure, not a data visualization we can build. |
| Stock photos (pages 1, 4, 5, 11) | Decorative photography, no data content |
| Logos/branding (all pages) | Newsletter design elements |
