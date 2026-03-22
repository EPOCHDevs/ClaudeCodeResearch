# AMFX 20JAN23 - Analysis

## PDF Title and Date
**Title:** Five Main Outcomes
**Date:** January 20, 2023
**Author:** Brent Donnelly, Spectra Markets

## Summary
The newsletter frames the macro outlook through a Bayesian lens of five possible outcomes: (1) No landing, (2) Soft landing, (3) Recession lite, (4) Hard landing, (5) Crash landing. Donnelly assigns evolving probabilities to each scenario (approximately 5/15/40/30/10 at time of writing). The key debate is between soft data (weak sentiment, weak housing) and hard data (strong labor market, falling inflation). He discusses UK retail sales weakness, central bank forward guidance credibility (Fed and ECB), and implied overnight rate pricing. The sidebar features an intergenerational employment mobility chart. The fun fact covers Australia vs. the Moon size comparison.

---

## Visual Elements Inventory

| # | Page | Element | Classification | Image File | Reason |
|---|------|---------|---------------|------------|--------|
| 1 | 1 | Spectra Markets logo/header | DISCARD | page_01_img_02.jpeg | Branding logo |
| 2 | 1 | am/FX logo | DISCARD | page_01_img_00.png | Branding logo |
| 3 | 1 | Sidebar: Proportion of sons employed chart (small thumbnail) | **KEEP** | page_01_img_01.png | Economic mobility data (intergenerational employment) |
| 4 | 1 | 6-month rolling sum of MoM Retail Sales in the UK | **KEEP** | page_01_img_03.png | Long-term economic data time series |
| 5 | 2 | Spectra Markets logo/header | DISCARD | not extracted (below size threshold) | Branding logo |
| 6 | 2 | Implied Overnight Rate & Number of Hikes/Cuts chart | **KEEP** | page_02_img_00.png | Central bank rate expectations chart |
| 7 | 3 | Spectra Markets logo/header | DISCARD | not extracted (below size threshold) | Branding logo |
| 8 | 3 | Proportion of sons employed (full-size version) | **KEEP** | not extracted (below size threshold) | Economic mobility scatter plot (same data as thumbnail) |
| 9 | 4 | Spectra Markets logo/header | DISCARD | not extracted (below size threshold) | Branding logo |
| 10 | 4 | Disclaimer page | DISCARD | not extracted (below size threshold) | Legal disclaimer |

---

## Detailed Analysis of KEPT Items

### Chart 1: 6-Month Rolling Sum of MoM Retail Sales in the UK

- **type:** Bar chart (time series / vertical bars)
- **image_file:** page_01_img_03.png
- **title:** 6-month rolling sum of MoM Retail Sales in the UK
- **page:** 1
- **data:** UK monthly retail sales month-over-month changes, accumulated as a 6-month rolling sum
- **assets/instruments:** UK Retail Sales (economic indicator)
- **transforms/calculations:** 6-month rolling sum of month-over-month percentage changes; 2020 and 2021 are cut out to avoid y-axis dilation (noted in chart annotation)
- **metrics:** Current reading at extreme negative levels (approximately -4.0 to -5.0), comparable only to the 2008/2009 financial crisis period; historical range approximately -5.0 to +3.0
- **time_range:** 1988 to 2022 (labels: 1988, 1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022)
- **x_axis:** Date (biannual from 1988 to 2022)
- **y_axis:** 6-month rolling sum of MoM retail sales (ranging from approximately -5.00 to +3.00)
- **insight:** UK retail sales are at historically extreme negative levels. In a world of 6% inflation, negative nominal retail sales implies a real drop of approximately 12%. This is "almost unbelievably bad" and supports the bearish economic outlook. The chart distortion note about removing 2020/2021 is important context.
- **source:** Not explicitly stated; likely ONS (UK Office for National Statistics) data via Bloomberg

---

### Chart 2: Implied Overnight Rate & Number of Hikes/Cuts

- **type:** Dual-axis line/bar chart
- **image_file:** page_02_img_00.png
- **title:** Implied Overnight Rate & Number of Hikes/Cuts
- **page:** 2
- **data:** Implied policy rate (left axis, line) and number of implied rate hikes/cuts (right axis, bars) from fed funds futures or OIS market
- **assets/instruments:** Fed Funds futures / OIS implied rates
- **transforms/calculations:** Market-implied forward overnight rate; implied number of 25bp hikes or cuts priced into the curve
- **metrics:** Implied policy rate appears around 4.5-4.9%; number of cuts priced in appears to be approximately -0.5 to -1.0 (i.e., market pricing rate cuts despite Fed promising to hold)
- **time_range:** Approximately mid-2022 to early 2024 (forward-looking from Jan 2023 perspective)
- **x_axis:** Date (appears to show forward dates for meetings/contracts)
- **y_axis:** Left axis: Implied policy rate (approximately 4.3-5.0%); Right axis: Number of hikes/cuts (approximately -0.5 to 0)
- **insight:** Despite the Fed promising to hold rates for most of 2023, the market is pricing in rate cuts. This illustrates the "forward guidance is just extrapolation bias" thesis -- markets have learned not to trust central bank guidance and are instead pricing based on data trajectory. When the Fed eventually capitulates, it will be a watershed moment driving yields sharply lower.
- **source:** Not explicitly stated; likely Bloomberg or CME FedWatch

---

### Chart 3: Proportion of Sons Employed at Father's Employer (Full Size)

- **type:** Scatter/line plot
- **image_file:** page_01_img_01.png (thumbnail from page 1 sidebar; full-size version on page 3 not extracted)
- **title:** Proportion of sons employed currently or at some point in the past with an employer their fathers had worked for at any time in the past for each percentile of the father's earning distribution
- **page:** 3 (thumbnail also on page 1 sidebar)
- **data:** Intergenerational employment mobility -- the proportion of sons who have worked at the same employer as their father, by father's earnings percentile
- **assets/instruments:** N/A (labor economics data, not financial instruments)
- **transforms/calculations:** Proportion (0 to 1 scale) calculated by earnings percentile bucket
- **metrics:**
  - For most of the distribution (0th to ~85th percentile): proportion hovers around 0.35-0.45
  - Sharp increase above 90th percentile: jumps from ~0.45 to ~0.50 at 90th, ~0.53 at 95th, peaks at ~0.67 at 100th percentile
- **time_range:** N/A (cross-sectional study)
- **x_axis:** Father's earnings percentile (0 to 100)
- **y_axis:** Incidence of same firm employment (0.30 to 0.70)
- **insight:** While the proportion of sons working at the same employer as their father is relatively flat across most of the income distribution (~40%), it spikes dramatically for the top 5-10% of earners. At the 100th percentile, nearly 70% of sons have worked at the same employer. This illustrates that dynastic employment/nepotism is concentrated among the highest earners, supporting the E.B. White quote: "Luck is not something you can mention in the presence of self-made men."
- **source:** Academic research paper (linked as "Source" below chart)
