# AMFX_25OCT22 — Chart Reproduction Tasks

Source: AMFX 25OCT22 newsletter by Brent Donnelly (Spectra Markets)
Theme: Housing leads labor leads recession — the macro causal chain from NAHB to Initial Claims to Unemployment Rate
Date: October 25, 2022

## Charts to Reproduce

### Task 1: US Initial Claims vs Unemployment Rate (Lead-Lag with Annotations)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_claims_vs_unemployment_research.json`
- **output:** `project/research_studies/test_runner/amfx_claims_vs_unemployment_research`
- **notes:** No dual-axis support in xy_lines, so both series normalized to inverted percentile rankings (0-100 scale). Raw series on separate charts plus percentile overlay. ICSA data cached from 2009-06-04; SPY from 2003-09-10, so historical range limited vs original 1980-2019.
- **image_ref:** page_01_img_03.png
- **chart_type:** dual-axis line chart with text annotations
- **data_sources:** FRED: ICSA (Initial Jobless Claims, weekly SA), UNRATE (Unemployment Rate, monthly SA)
- **what_makes_it_interesting:** The annotated lead times at each cycle turn (3, 13, 22, 13, 8, 7, 5 months) make this chart far more valuable than a simple overlay. It proves Claims is a leading indicator, not just a coincident one. The visual correlation is tight, and the annotations quantify exactly HOW MUCH lead time you get. A macro trader would use this to know: "once Claims turn, I have 3-22 months before unemployment spikes." Excellent chart design — the annotations transform a good chart into a great one.
- **reproduction_notes:** Blue line: Initial Claims (left axis: 150-650). Black line: Unemployment Rate (right axis: 3.00-12.00%). Lead time annotations in bold black at each turning point. X-axis: 1980-2019 (exclude 2020 COVID spike). Both axes should be scaled so the series track visually. Claims on left, UR on right. The key is getting the annotation placements right at each cycle turn.

### Task 2: US Initial Claims vs Nonfarm Payrolls (NFP is Noise)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_claims_vs_nfp_research.json`
- **output:** `project/research_studies/test_runner/amfx_claims_vs_nfp_research`
- **notes:** NFP month-over-month change computed via returns(type=monetary) on PAYEMS levels. Both series on separate charts plus percentile overlay. Uses current revised PAYEMS (first-release data not available on FRED).
- **image_ref:** page_01_img_04.jpeg
- **chart_type:** dual-axis line chart
- **data_sources:** FRED: ICSA (Initial Claims, weekly SA), PAYEMS or BLS NFP actual release (not revised — use first-release data if available, otherwise BLS current series)
- **what_makes_it_interesting:** Makes the "NFP is 86% noise and 14% signal" argument visually. The orange NFP line is wildly jagged and noisy while the blue Claims line is cleaner. Both tell the same story at turns, but Claims tells it with less noise and more timeliness. This changes how a trader should weight the monthly NFP report vs weekly Claims data.
- **reproduction_notes:** Orange line: NFP Actual Release (left axis: -900 to 500). Blue line: Initial Claims (right axis: inverted, 150-650). X-axis: 1996-2019. NFP should use INITIAL release values where possible (not revised). Claims axis is INVERTED so higher claims = lower on chart, maintaining visual correlation with NFP.

### Task 3: US Initial Claims vs 3-Month Average of NFP
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_claims_vs_nfp_3mma_research.json`
- **output:** `project/research_studies/test_runner/amfx_claims_vs_nfp_3mma_research`
- **notes:** NFP 3MMA computed as ma(period=63) on daily-ffilled NFP change. Separate charts plus percentile overlay. Demonstrates that even smoothing doesn't make NFP as timely as Claims.
- **image_ref:** page_02_img_00.png
- **chart_type:** dual-axis line chart
- **data_sources:** FRED: ICSA (Initial Claims, weekly SA), PAYEMS (3-month moving average of month-over-month change)
- **what_makes_it_interesting:** The punchline to the "NFP is noise" argument. Even after smoothing NFP with a 3-month average (which most economists recommend), it's STILL not as timely as raw weekly Claims. The visual comparison makes this immediately obvious. If you're a macro trader watching the labor market, Claims wins on every dimension.
- **reproduction_notes:** Same format as Task 2 but with NFP 3-month MA instead of raw NFP. Orange line: NFP 3MMA (left axis: -700 to 500). Blue line: Initial Claims (right axis: inverted, 150-650). X-axis: 1996-2019. The 3MMA smooths the NFP noise but still lags Claims at turns.

### Task 4: NAHB Housing Index vs Initial Claims (The Key Chart)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_nahb_vs_claims_research.json`
- **output:** `project/research_studies/test_runner/amfx_nahb_vs_claims_research`
- **notes:** NAHB Housing Market Index not available on FRED. Substituted with Housing Starts (HOUST) as the hard-data counterpart — closely correlated with NAHB and also a leading indicator of Claims. Uses percentile normalization for overlay. Includes lead-lag spread chart.
- **image_ref:** page_02_img_01.png
- **chart_type:** dual-axis line chart with text annotations
- **data_sources:** FRED: NAHB Housing Market Index (HOUSINGNSA or from NAHB directly), ICSA (Initial Claims, weekly SA)
- **what_makes_it_interesting:** This is the crown jewel of the newsletter — the full causal chain. NAHB leads Claims by 6-24 months at most turns, giving traders an even earlier warning signal than Claims alone. The "???" annotation at 2022 is genius: NAHB had already collapsed but Claims hadn't turned yet, putting us in the "danger zone." The annotated lead times (6 months, Messy, 14 months, 24 months, 3 months, 2 months, Minus 4 months) show both the power and the variability of the relationship.
- **reproduction_notes:** Red line: NAHB Housing Index (right axis: 5-85). Blue line: Initial Claims (left axis: INVERTED, 150-700). X-axis: 1985-2022. Lead time annotations at each turn. The "???" at far right (2022) is the key narrative moment. Claims axis is inverted so visual correlation is maintained (rising NAHB = falling Claims = good economy). Both lines should visually track well together.

### Task 5: Housing Share of GDP (Stacked Area)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_housing_gdp_share_research.json`
- **output:** `project/research_studies/test_runner/amfx_housing_gdp_share_research`
- **notes:** Residential Fixed Investment share from A011RE1Q156NBEA (direct %). Housing & Utilities Services share computed as DHUTRC1Q027SBEA / GDP * 100. Stacked area chart with NormalStack. Components also shown separately on second chart. Data range limited by SPY availability (2003+).
- **image_ref:** page_03_img_00.jpeg
- **chart_type:** stacked area chart
- **data_sources:** BEA/FRED: PRFI (Private Residential Fixed Investment as % of GDP) and Housing Services component (DHSGRC1Q027SBEA or similar)
- **what_makes_it_interesting:** Shows housing's true footprint in the economy is 16-18% of GDP — much larger than most people realize. The blue (Residential Fixed Investment) and red (Housing Services) stacking reveals that most of housing's GDP impact is services (rent), not construction. The 2005-2006 spike in Residential Fixed Investment is the bubble signature. Clean visualization of a structural macro fact.
- **reproduction_notes:** Blue stacked area: Residential Fixed Investment (bottom). Red stacked area: Housing Services (top). Y-axis: 0-20% of GDP. X-axis: 1980-2021. The chart should show total housing ~16-18% with Residential FI ~3-6% and Housing Services ~12-13%.

### Task 6: Residential Investment as % of GDP — US, Canada, Ireland, Spain
- **status:** BLOCKED
- **blocked_reason:** Cross-country residential investment data (Canada, Ireland, Spain) requires OECD/World Bank/Refinitiv Datastream sources which are not available through FRED or the current data infrastructure. Only US data (A011RE1Q156NBEA) is accessible. Original source was Refinitiv Datastream via acornmc.co.uk.
- **image_ref:** page_03_img_01.png
- **chart_type:** multi-line chart (4 countries)
- **data_sources:** OECD or World Bank: Gross Fixed Capital Formation (Residential) as % of GDP for USA, Canada, Ireland, Spain
- **what_makes_it_interesting:** The most powerful chart in the Canadian housing bear case. Canada's residential investment at 9.7% of GDP is AT THE SAME LEVEL Ireland and Spain reached before their housing bubbles burst catastrophically. Ireland went from 12% to 1.5%, Spain from 11% to 4%. The implication — Canada could face a similar collapse — is visually obvious without saying a word. The cross-country comparison is the entire argument.
- **reproduction_notes:** Four lines: Canada (navy blue, left axis), US (red), Ireland (gray), Spain (green). Dual y-axis. X-axis: 1985-2022. Legend with latest values: Canada 9.7%, US 4.7%, Ireland 1.5%, Spain 5.0%. Source: Refinitiv Datastream / acornmc.co.uk. The Ireland and Spain lines show the "what could happen" scenario for Canada.

### Task 7: USDCNH vs US/China 10-Year Rate Differential
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_usdcnh_rate_spread_research.json`
- **output:** `project/research_studies/test_runner/amfx_usdcnh_rate_spread_research`
- **notes:** China 10Y yield not available on FRED. Used US 10Y yield (DGS10) as proxy since it was the dominant driver of spread widening 2021-2022. USDCNH not available as Polygon FX asset; used FRED DEXCHUS (Chinese Yuan per USD, daily) as proxy. Percentile overlay shows the lead-lag relationship. Period: Feb 2021 to Nov 2022.
- **image_ref:** page_04_img_00.png
- **chart_type:** dual-axis line chart with annotations
- **data_sources:** FRED or Bloomberg: US 10Y yield minus China 10Y yield; USDCNH spot rate (Yahoo: CNH=X or similar)
- **what_makes_it_interesting:** Illustrates one of trading's deepest lessons: "early is a synonym for wrong." The rate spread moved first and USDCNH lagged for months before violently catching up. The "Evergrande is China's Lehman moment!" annotation marks a false alarm; the real move came later driven by rate differentials, not headlines. A macro trader would use this to understand that FX eventually follows rates, but timing matters enormously.
- **reproduction_notes:** Two lines on TradingView-style chart. Left axis: Rate differential (US 10Y - China 10Y), range -2.0% to +1.5%. Right axis: USDCNH, range 6.30-7.40. Two bold text annotations with arrows: "Evergrande is China's Lehman moment!" and "Rate spreads are ripping!" X-axis: Feb 2021 to Nov 2022. The divergence period (mid-2021 to early 2022) and convergence (mid-2022) are the key visual features.

## Discarded Charts

| Chart | Reason |
|-------|--------|
| USDCAD price chart (page_05_img_00.jpeg) | Standard annotated candlestick chart of USDCAD with BoC event labels. While the narrative (CAD driven by USD not Canada) is interesting, the chart itself is a basic price chart with text boxes. No unique data transformation. |
| Canada 2Y yield with MAs (page_05_img_01.jpeg) | Standard TradingView yield chart with 40-day and 80-day moving averages. No unique visualization — any trader can pull up yields with MAs. The "macro view with tech trigger" concept is interesting but the chart itself is generic. |
