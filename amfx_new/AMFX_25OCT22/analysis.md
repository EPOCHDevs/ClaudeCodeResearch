# AMFX 25OCT22 - Housing and Cycles

**Date:** October 25, 2022
**Author:** Brent Donnelly, Spectra Markets
**Pages:** 8

## Summary

The newsletter explores the relationship between housing and the labor market cycle. The core thesis is that housing leads the labor market: Initial Claims lead the Unemployment Rate, and the NAHB Housing Index leads Initial Claims. With NAHB having peaked in November 2020 and collapsing in early 2022, the author argues the US has entered the "danger zone" for rising jobless claims. The piece also discusses Canadian housing vulnerability and the USDCAD/USDCNH trade implications, advocating a "macro view with tech trigger" framework.

## Current Views (as of publication)

- Short USDNOK @ 10.56 (Stop 10.92, TP 9.88)
- Long a 3-month USDBRL 4.90 digital put at 20%

---

## Visual Elements Inventory

| # | Page | Element | Classification | Image File | Reason |
|---|------|---------|---------------|------------|--------|
| 1 | 1 | Spectra Markets logo/header | DISCARD | page_01_img_00.png, page_01_img_02.jpeg | Branding logo, appears on every page |
| 2 | 1 | Antarctica "The Confusing Continent" meme map | DISCARD | page_01_img_01.jpeg | Humor/meme image, non-quantitative |
| 3 | 1 | US Initial Claims vs. US Unemployment Rate chart | **KEEP** | page_01_img_03.png | Dual-axis time series showing leading indicator relationship |
| 4 | 1 | US Initial Claims vs. US Nonfarm Payrolls chart | **KEEP** | page_01_img_04.jpeg | Dual-axis time series comparing labor indicators |
| 5 | 2 | US Initial Claims vs. 3-month average of US Nonfarm Payrolls chart | **KEEP** | page_02_img_00.png | Smoothed comparison of labor market indicators |
| 6 | 2 | US Initial Claims vs. NAHB Housing Index chart | **KEEP** | page_02_img_01.png | Key chart showing housing-to-labor lead-lag relationship |
| 7 | 3 | Housing Share of GDP, 1980 to now (USA) stacked area chart | **KEEP** | page_03_img_00.jpeg | Macro structural chart showing housing contribution to GDP |
| 8 | 3 | Residential Investment as % of GDP (USA, Canada, Ireland, Spain) line chart | **KEEP** | page_03_img_01.png | Cross-country housing bubble comparison |
| 9 | 4 | Burning building photo (Canadian housing crash imagery) | DISCARD | not extracted (below size threshold) | Decorative/editorial photo |
| 10 | 4 | Maclean's magazine cover "Inside the Great Real Estate Crash of 2013" | DISCARD | page_04_img_01.jpeg | Magazine cover, editorial illustration |
| 11 | 4 | USDCNH vs. US/China 10-year rate differential chart | **KEEP** | page_04_img_00.png | Dual-axis FX vs. rates spread chart |
| 12 | 5 | USDCAD price chart with annotations | **KEEP** | page_05_img_00.jpeg | Annotated FX price chart showing BoC event reactions |
| 13 | 5 | Canada 2-year yield with 40-day and 80-day moving averages | **KEEP** | page_05_img_01.jpeg | Technical analysis chart with MA overlays |
| 14 | 6 | Spectra Markets Trader Handbook and Almanac 2023 book cover | DISCARD | page_06_img_00.png | Book promotion image |
| 15 | 7 | Antarctica "The Confusing Continent" meme map (full page) | DISCARD | page_07_img_00.jpeg | Humor/meme, same as sidebar thumbnail |
| 16 | 8 | Disclaimer page | DISCARD | not extracted (text only) | Legal text, no visual content |

---

## Detailed Analysis of KEPT Items

### Chart 1: US Initial Claims vs. US Unemployment Rate

- **type:** Dual-axis line chart
- **image_file:** page_01_img_03.png
- **title:** US Initial Claims vs. US Unemployment Rate (Marked with Initial Claims lead vs. UR at each turn)
- **page:** 1
- **data:** Weekly US Initial Jobless Claims and US Unemployment Rate (U3) over ~40 years
- **assets/instruments:** US Initial Jobless Claims (DOL), US Unemployment Rate U3 (BLS)
- **transforms/calculations:** Raw levels plotted; lead times annotated at each cycle turn (3 months, 13 months, 22 months, 8 months, 13 months, 7 months, 5 months)
- **metrics:** Lead time in months at each turning point
- **time_range:** ~1980 to 2019
- **x_axis:** Years (1980-2019)
- **y_axis:** Left: US Initial Claims (150-650); Right: US Unemployment Rate (3.00-12.00%)
- **insight:** Initial Claims consistently lead the Unemployment Rate at cycle turns. Claims are a more timely, less noisy indicator than UR for detecting labor market inflections.
- **source:** Not explicitly stated (likely BLS/DOL)

### Chart 2: US Initial Claims vs. US Nonfarm Payrolls

- **type:** Dual-axis line chart
- **image_file:** page_01_img_04.jpeg
- **title:** US Initial Claims vs. US Nonfarm Payrolls
- **page:** 1
- **data:** NFP actual release (not revised) vs. Initial Claims
- **assets/instruments:** US Nonfarm Payrolls (BLS), US Initial Jobless Claims (DOL)
- **transforms/calculations:** Raw NFP release (not revised), inverted Claims axis
- **metrics:** None explicitly labeled
- **time_range:** ~1996 to 2019 (2020 excluded due to COVID distortion)
- **x_axis:** Years (1996-2019)
- **y_axis:** Left: NFP Actual Release (-900 to 500); Right: US Initial Jobless Claims (inverted, 150-650)
- **insight:** NFP is 86% noise and 14% signal; Claims are less noisy and more timely. The two series are coincident but Claims is cleaner.
- **source:** BLS, DOL

### Chart 3: US Initial Claims vs. 3-month Average of US Nonfarm Payrolls

- **type:** Dual-axis line chart
- **image_file:** page_02_img_00.png
- **title:** US Initial Claims vs. 3-month average of US Nonfarm Payrolls
- **page:** 2
- **data:** 3-month moving average of NFP vs. Initial Claims
- **assets/instruments:** US Nonfarm Payrolls (3MMA), US Initial Jobless Claims
- **transforms/calculations:** 3-month moving average applied to NFP; raw Claims
- **metrics:** None explicitly labeled
- **time_range:** 1996 to 2019
- **x_axis:** Years (1996-2019)
- **y_axis:** Left: NFP Actual Release (-700 to 500); Right: US Initial Jobless Claims (inverted, 150-650)
- **insight:** Even after smoothing NFP with a 3-month average, the series is not as timely as raw weekly Initial Claims data. Supports the case for using Claims over NFP.
- **source:** BLS, DOL

### Chart 4: US Initial Claims vs. NAHB Housing Index

- **type:** Dual-axis line chart with annotated lead times
- **image_file:** page_02_img_01.png
- **title:** US Initial Claims vs. NAHB Housing Index
- **page:** 2
- **data:** NAHB Housing Market Index vs. Initial Claims (inverted)
- **assets/instruments:** NAHB Housing Market Index, US Initial Jobless Claims
- **transforms/calculations:** Claims axis inverted to show correlation; lead-lag annotations at cycle turns (6 months, "Messy", 14 months, 24 months, 3 months, 2 months, "Minus 4 months", "???")
- **metrics:** Lead time in months between NAHB turn and Claims turn at each cycle
- **time_range:** 1985 to ~2022
- **x_axis:** Years (1985-2021)
- **y_axis:** Left: Initial Claims (inverted, 150-700); Right: NAHB Housing Index (5-85)
- **insight:** NAHB usually leads the turn in Claims by 6-24 months. NAHB peaked in Nov 2020 and collapsed in early 2022, suggesting the US has entered the danger zone for rising Claims. The two series are coincident in recovery phases.
- **source:** NAHB, DOL

### Chart 5: Housing Share of GDP, 1980 to now (USA)

- **type:** Stacked area chart
- **image_file:** page_03_img_00.jpeg
- **title:** Housing Share of GDP, 1980 to now (USA)
- **page:** 3
- **data:** Housing's contribution to US GDP broken into Residential Fixed Investment and Housing Services
- **assets/instruments:** US GDP components (Residential Fixed Investment, Housing Services)
- **transforms/calculations:** Percentage of GDP calculation for each housing sub-component
- **metrics:** Total ~16-18% of GDP, with ~4.7% from Residential Fixed Investment
- **time_range:** 1980 to ~2021
- **x_axis:** Years (1980-2021)
- **y_axis:** % of GDP (0-20)
- **insight:** Housing influences around 16-18% of GDP. Housing's contribution has returned to its 1980-2006 average, making it a significant macro variable.
- **source:** Not explicitly stated (likely BEA)

### Chart 6: Residential Investment as % of GDP (USA, Canada, Ireland, Spain)

- **type:** Multi-line chart (4 countries)
- **image_file:** page_03_img_01.png
- **title:** Residential Investment as a % of GDP in USA, Canada, Ireland and Spain, 1985 to now
- **page:** 3
- **data:** Residential investment as percentage of GDP for four countries
- **assets/instruments:** Residential investment/GDP ratios for USA, Canada, Ireland, Spain
- **transforms/calculations:** Gross Fixed Capital Formation as % of GDP (nominal, last data point Q4 2021)
- **metrics:** Canada 9.7% of GDP, US 4.7%, Ireland 1.5%, Spain 5.0% (latest values)
- **time_range:** 1985 to ~2022
- **x_axis:** Years (1985-2020)
- **y_axis:** % of GDP (0-12, dual axis)
- **insight:** Canada's residential investment as a share of GDP is at the same levels Ireland and Spain reached before their housing bubbles popped. This supports the bear case for Canadian housing.
- **source:** acornmc.co.uk, Refinitiv Datastream; chart by Richard Dias CFA (via Twitter)

### Chart 7: USDCNH vs. US/China 10-year Rate Differential

- **type:** Dual-axis line chart with annotations
- **image_file:** page_04_img_00.png
- **title:** USDCNH vs. US / China 10-year rate differential
- **page:** 4
- **data:** USDCNH spot rate and the US-China 10-year government bond yield spread
- **assets/instruments:** USDCNH, US 10-year Treasury yield, China 10-year government bond yield
- **transforms/calculations:** Rate differential (US 10Y minus China 10Y, in percentage points)
- **metrics:** Rate spread range approximately -2.0% to +1.5%; USDCNH range 6.30-7.40
- **time_range:** ~Feb 2021 to Nov 2022
- **x_axis:** Months (Feb 2021 - Nov 2022)
- **y_axis:** Left: Rate differential (% -2.0 to 1.5); Right: USDCNH (6.30-7.40)
- **insight:** USDCNH lagged the rate differential for months but eventually caught up violently. Illustrates that "early is a synonym for wrong" in trading -- markets can stay disconnected from fundamentals before repricing suddenly. The "Evergrande is China's Lehman moment" annotation marks a false alarm; the real move came later as rate spreads ripped.
- **source:** TradingView

### Chart 8: USDCAD Price Chart with Annotations

- **type:** Candlestick/line chart with text annotations
- **image_file:** page_05_img_00.jpeg
- **title:** USDCAD has been driven by the US story, not the Canadian story
- **page:** 5
- **data:** USDCAD spot rate
- **assets/instruments:** USDCAD
- **transforms/calculations:** None (raw price)
- **metrics:** Range ~1.24 to 1.40
- **time_range:** ~March to November 2022
- **x_axis:** Months (Mar-Nov 2022)
- **y_axis:** USDCAD rate (1.24-1.40)
- **insight:** USDCAD has been driven primarily by the US dollar story (global risk, US yields) rather than domestic Canadian factors. BoC's hawkish path and surprise 100bp hike did not sustainably move CAD. This means if you want to express a bearish Canada housing view, the trade is in Canadian rates, not USDCAD.
- **source:** TradingView

### Chart 9: Canada 2-Year Yield with Moving Averages

- **type:** Line chart with moving average overlays
- **image_file:** page_05_img_01.jpeg
- **title:** Canada 2-year yield, July 2021 to now (with 40-day and 80-day moving averages)
- **page:** 5
- **data:** Canadian 2-year government bond yield with 40-day and 80-day simple moving averages
- **assets/instruments:** Canada 2-year government bond yield
- **transforms/calculations:** 40-day SMA, 80-day SMA
- **metrics:** Yield ~4.13% at time of writing; range 0.0% to 4.5%
- **time_range:** July 2021 to ~October 2022
- **x_axis:** Months (Jul 2021 - Nov 2022)
- **y_axis:** Yield (0.0% - 4.5%)
- **insight:** If Canadian housing causes a major economic downturn, the drop in yields could be fast and hard. The 40-day and 80-day MAs serve as technical triggers -- wait for yields to break below the 80-day MA before entering a "receive Canada" trade. At the time of writing, yields are far above both MAs, so no signal is imminent. Embodies the "macro view with tech trigger" framework.
- **source:** TradingView
