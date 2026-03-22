# AMFX_17JUN22 — Chart Reproduction Tasks

Source: AMFX 17JUN22 newsletter by Brent Donnelly (Spectra Markets)
Theme: EUR buy-the-dip thesis — ECB anti-fragmentation pledge tightening peripheral spreads, rate differentials supportive, European equities outperforming
Date: June 17, 2022

## Charts to Reproduce

### Task 1: EURUSD vs. Germany/Italy 10-Year Spread
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_eurusd_btp_bund_spread_research.json`
- **output:** `project/research_studies/test_runner/amfx_eurusd_btp_bund_spread_research`
- **notes:** German 10Y (IRLTLT01DEM156N) and Italian 10Y (IRLTLT01ITM156N) from FRED, monthly data ffilled to daily. Spread inverted to align directionally with EURUSD. ALFRED mode had duplicate publication dates for Italian series causing all-NaN; resolved with use_alfred=False. 2 charts + 1 summary table, 247 daily bars Oct 2021-Jul 2022.
- **image_ref:** page_01_img_03.png
- **chart_type:** dual-axis overlay (two line series)
- **data_sources:** EURUSD spot (Yahoo Finance), German 10Y yield (FRED IRLTLT01DEM156N or DE10YT=RR), Italian 10Y yield (FRED IRLTLT01ITM156N or IT10YT=RR). Spread = Italy 10Y minus Germany 10Y (BTP-Bund spread). May need to invert the spread axis for directional alignment with EURUSD.
- **what_makes_it_interesting:** Shows the direct link between EUR peripheral stress and FX — when Italy/Germany spreads widen (eurozone fragmentation risk), EUR sells off. The ECB's anti-fragmentation pledge was being mocked, but the spread was actually tightening, supporting the EUR buy thesis. A classic "the market is telling you something different from the narrative" chart.
- **reproduction_notes:** Bloomberg-style hourly dual-axis overlay, Nov 2021 to Jun 2022. Blue line = spread (appears inverted on left axis, ranging roughly -1.1 to -2.5), black/gray line = EURUSD (right axis). Strong co-movement. The recent divergence (spread tightening while EUR still low) is the trade signal.

### Task 2: EURUSD vs. Germany/USA 5-Year Rate Differential
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_eurusd_rate_differential_research.json`
- **output:** `project/research_studies/test_runner/amfx_eurusd_rate_differential_research`
- **notes:** FRED lacks daily German 5Y yield; used German 10Y (monthly IRLTLT01DEM156N, ffilled) minus US 10Y (daily DGS10) as rate differential proxy. Captures the same macro dynamic. 2 charts + 1 summary table, 357 daily bars Jun 2021-Jul 2022.
- **image_ref:** page_01_img_04.png
- **chart_type:** dual-axis overlay (two line series)
- **data_sources:** EURUSD spot (Yahoo Finance), German 5Y yield (FRED or Bloomberg DE5YT=RR), US 5Y Treasury yield (FRED DGS5 or US5YT=RR). Differential = Germany 5Y minus US 5Y.
- **what_makes_it_interesting:** The foundational FX driver chart — rate differentials drive currencies. Shows EURUSD and the DE-US 5Y spread moving in near-perfect tandem from Jul 2021 to Jun 2022. At the time, the rate differential was suggesting EURUSD might be oversold, supporting the buy thesis. This is a repeatable framework for any FX pair.
- **reproduction_notes:** Bloomberg-style hourly dual-axis, Jul 2021 to Jun 2022. Blue line = EURUSD (right axis 1.04-1.19), black line = rate differential (left axis -1.4 to -2.3). The tight co-movement and then any divergence is the analytical focus. Left axis labeled "Value," right axis labeled "Price USD."

### Task 3: EURUSD vs. Europe/USA Equity Ratio
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_eurusd_equity_ratio_research.json`
- **output:** `project/research_studies/test_runner/amfx_eurusd_equity_ratio_research`
- **notes:** SX7P (Euro Stoxx Banks) proxied by EUFN (iShares MSCI Europe Financials ETF); ES futures proxied by SPY. Ratio = EUFN/SPY x100. 2 charts + 1 summary table, 152 daily bars Jan-Jul 2022.
- **image_ref:** page_02_img_00.png
- **chart_type:** dual-axis overlay (two line series)
- **data_sources:** EURUSD spot (Yahoo Finance), European bank equities SX7P (Euro Stoxx Banks index), S&P 500 futures ESc1 (Yahoo Finance ^GSPC or ES=F). Ratio = SX7P / ES.
- **what_makes_it_interesting:** Adds a third leg to the EUR buy thesis — not just rates and spreads, but equity relative performance too. European equities were outperforming US equities, suggesting capital flows supporting EUR. Donnelly admits this is a "useless real-time indicator" but uses it to build weight of evidence. The overlay shows co-movement Feb-Jun 2022 and recent divergence favoring EUR.
- **reproduction_notes:** Bloomberg-style hourly dual-axis, Feb-Jun 2022. Blue line = equity ratio (SX7P/ES), black/gray line = EURUSD (right axis 1.04-1.15). Header shows "Hourly EUR=, .SX7P, ESc1." Recent divergence (equity ratio rising, EUR still low) is the signal.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| (none) | All three charts form a tight analytical triptych — peripheral spreads, rate differentials, and equity relative performance all supporting one thesis. Worth reproducing as a set. |
