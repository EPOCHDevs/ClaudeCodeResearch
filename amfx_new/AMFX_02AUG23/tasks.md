# AMFX_02AUG23 — Chart Reproduction Tasks

Source: AMFX 02AUG23 newsletter by Brent Donnelly (Spectra Markets)
Theme: US fiscal policy regime break + energy fundamentals tightening (crude inventory record draw, breakout setup)
Date: August 2, 2023

## Charts to Reproduce

### Task 1: US Unemployment vs Budget Deficit Scatter (by Decade)
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_unemployment_deficit_scatter_research.json`
- **notes:** Uses xy_scatter with 6 decade-split Y series (1970s-2020s), each colored per original (Green, Cyan, Yellow, Gray, Orange, Blue). show_trend_line=True adds OLS regression from first series (1970s). FYFSGDA188S (annual deficit % GDP) + UNRATE (monthly unemployment) both forward-filled to daily. Date range 1970-01-01 to 2023-08-02 in run_config. SPY dummy asset may only provide grid from ~1993, limiting to 4 decades (1990s-2020s) -- still captures the key regime break.
- **image_ref:** page_01_img_03.png
- **chart_type:** scatter (color-coded by decade, with regression line + annotations)
- **data_sources:** FRED: UNRATE (unemployment rate), FYFSGDA188S (federal surplus/deficit as % GDP)
- **what_makes_it_interesting:** Shows a 50-year macro regime break at a glance. The 2020s dots are completely off the historical regression line — procyclical fiscal policy is a new thing. Visually immediate.
- **reproduction_notes:** Color dots by decade (1970s green, 1980s cyan, 1990s yellow, 2000s gray, 2010s orange, 2020s blue). Add regression line through 1970s-2010s data. Annotate "Countercyclical orthodox Keynesian policy" along line, "Peak COVID" outlier, "You are here: Procyclical MMT-style policies" on the 2020s cluster. Y-axis is deficit (inverted — deficit is negative). X-axis is unemployment rate 0-16%.

### Task 2: API Crude Oil Inventory 2023 (Weekly Bar Chart)
- **status:** BLOCKED (definition removed)
- **image_ref:** page_02_img_00.png
- **chart_type:** bar (positive/negative, with data labels on each bar)
- **data_sources:** API (American Petroleum Institute) weekly crude oil inventory draws/builds
- **blocker:** No FRED series for weekly crude oil inventory stocks. Exhaustive search confirmed: WCESTUS1 does not exist, no proxy available. Would require EIA API (api.eia.gov) which is not available through economic_indicators().

### Task 3: API Crude Oil Inventory 2018-Now (Long-Term Line)
- **status:** BLOCKED (definition removed)
- **image_ref:** page_02_img_01.png
- **chart_type:** line (single series, weekly)
- **data_sources:** Same as Task 2 — API weekly crude oil inventory
- **blocker:** Same as Task 2 — no FRED series, no proxy.

### Task 4: ISM Manufacturing PMI vs New Orders (Lead-Lag Overlay)
- **status:** BLOCKED (definition removed)
- **image_ref:** page_02_img_02.png
- **chart_type:** dual-line overlay (two Y-axes)
- **data_sources:** ISM Manufacturing PMI + New Orders sub-index (proprietary, Institute for Supply Management)
- **blocker:** NAPM and NAPMNOI do not exist on FRED. ISM PMI data is proprietary — not available through economic_indicators(). No adequate FRED proxy (regional Fed surveys like Philly Fed are different indices).

### Task 5: Crude Oil 2022-Now with Equilibrium Zones
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_crude_equilibrium_zones_research.json`
- **run_config_override:** start=2022-01-01, end=2023-09-30
- **image_ref:** page_03_img_00.jpeg
- **chart_type:** line with horizontal reference lines
- **data_sources:** CL-Futures (via futures_continuation, LiquidityBased rollover, NoAdjustment)
- **reproduction_notes:** Single close price line with 4 reference lines at 63.50, 76.70, 83.50, 93.50. Text annotations cannot be rendered — reference line titles provide partial equivalent.

### Task 6: RBOB Gasoline 2023 Bull Flag
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_rbob_bull_flag_research.json`
- **run_config_override:** start=2022-12-01, end=2023-08-31
- **image_ref:** page_03_img_01.jpeg
- **chart_type:** line with horizontal reference lines
- **data_sources:** RB-Futures (via futures_continuation, LiquidityBased rollover, NoAdjustment)
- **reproduction_notes:** Single close price line with 3 reference lines at 2.90 (flag high), 2.60 (flag low), 2.20 (pole base). Diagonal trendlines for the converging flag pattern not supported — horizontal lines bracket the zone.

## Discarded Charts

| Chart | Reason |
|-------|--------|
| (none) | All 6 charts retained — they build a coherent discretionary narrative |
