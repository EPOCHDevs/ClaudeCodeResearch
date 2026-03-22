# AMFX_27SEP23 — Chart Reproduction Tasks

Source: AMFX 27SEP23 newsletter by Brent Donnelly (Spectra Markets)
Theme: Pre-election year equity seasonality and the "is rate normalization good or bad?" debate
Date: September 27, 2023

## Charts to Reproduce

### Task 1: Pre-Election Year Seasonal Path — Four Major Equity Indices (2x2 Grid)
- **status:** DONE
- **image_ref:** page_01_img_02.png
- **chart_type:** multi-panel line chart (2x2 grid)
- **data_sources:** Yahoo Finance or Bloomberg: ^GSPC (S&P 500), ^IXIC (NASDAQ), ^RUT (Russell 2000), ^GDAXI (DAX). Pre-election years: 1999, 2003, 2007, 2011, 2015, 2019, 2023 (plus any others back to 1998)
- **what_makes_it_interesting:** All four indices — including international (DAX) — show the SAME seasonal pattern in pre-election years: trough in early October, then rally hard into year-end. The consistency across US large cap, US tech, US small cap, and European equities makes this more convincing than single-index seasonality. The annotated entry dates (09OCT, 02OCT, 08OCT) with red arrows are clean design touches that make the chart immediately actionable.
- **reproduction_notes:** 2x2 grid. Top-left: S&P 500 (0-9% y-axis). Top-right: NASDAQ (0-16% y-axis). Bottom-left: Russell 2000 (0-10% y-axis). Bottom-right: DAX (0-9% y-axis). Each panel shows the average cumulative return path from Jan-Dec across pre-election years. X-axis: months (Jan-Dec). Purple/lavender title text. Red arrows and dates annotating the October trough. Thin black line for the average path. Clean white background.
- **definitions:**
  - `project/definitions/test_runner/amfx_preelection_seasonal_spx_research.json` — S&P 500 (via common_indices SPX)
  - `project/definitions/test_runner/amfx_preelection_seasonal_ndx_research.json` — NASDAQ (via common_indices NDX)
  - `project/definitions/test_runner/amfx_preelection_seasonal_rut_research.json` — Russell 2000 (via common_indices RUT)
  - `project/definitions/test_runner/amfx_preelection_seasonal_dax_research.json` — DAX (EWG proxy, ^GDAXI unavailable)
- **notes:** Original 2x2 grid reproduced as 4 separate definitions (one per index). Each shows 2023 path vs avg pre-election year path (2003-2019). DAX uses EWG (iShares MSCI Germany ETF) as proxy since ^GDAXI index data not available in Polygon. Pre-election years: year%4==3. Data from 2003 (Polygon start) covers 2003, 2007, 2011, 2015, 2019 pre-election years for averaging.

### Task 2: US 10-Year Yield — 60-Year History with Regime Annotations
- **status:** DONE
- **image_ref:** page_02_img_00.png
- **chart_type:** line chart with hand-drawn annotations
- **data_sources:** FRED: DGS10 (10-Year Treasury Constant Maturity Rate, daily) or GS10 (monthly)
- **what_makes_it_interesting:** A 60-year chart with three circled regimes that reframes the entire rate debate. Instead of asking "are rates too high?", it asks "which period was the anomaly?" The three zones — (1) Oil shock/wage-price spiral (1975-1985, 8-16%), (2) "The normal, properly-functioning zone" (1960-1975 and 1990-2005, 4-8%), and (3) Post-GFC secular stagnation (2009-2021, 0-3%) — suggest that 4.5% yields might be NORMAL, not restrictive. This reframing is the entire intellectual contribution of the chart.
- **reproduction_notes:** Bloomberg-style chart with dark line on tan/beige background. Y-axis: 0-16%. X-axis: 1960-2025, labeled in 5-year intervals. Three large red hand-drawn circles/ovals with annotations: "Oil shock, wage-price spiral zone" (top, 1975-1985), "The normal, properly-functioning zone?" (center, spanning 4-8% range across most of the timeline), "Post-GFC secular stagnation zone" (bottom-right, 2009-2021). Stats box in upper-left: Last Price 4.4990, High 15.8420 (09/30/81), Average 5.8637, Low 0.6561 (06/30/20). The annotations are what make this chart special — without them it's just a yield chart.
- **definition:** `project/definitions/test_runner/amfx_us10y_regime_zones_research.json`
- **notes:** Uses FRED DGS10 series. SPY data starts 2003, so chart covers 2003-2023 (~20 years) instead of full 60 years. Three regime zones represented as horizontal reference lines at 8% (Oil Shock floor), 4% (Normal zone floor), 3% (Stagnation ceiling), plus historical average at 5.86%. Includes regime-era bar chart showing average yield by era and summary statistics table. Hand-drawn circle annotations from original cannot be reproduced programmatically but reference lines convey the same regime boundaries.

## Discarded Charts

| Chart | Reason |
|-------|--------|
| (none) | Both charts in this newsletter are high-quality and worth reproducing. The RAS violations humor page and ATM meme are non-quantitative. |
