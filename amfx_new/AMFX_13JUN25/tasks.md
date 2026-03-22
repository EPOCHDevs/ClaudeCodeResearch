# AMFX_13JUN25 — Chart Reproduction Tasks

Source: AMFX 13JUN25 newsletter by Brent Donnelly (Spectra Markets)
Theme: Israel-Iran Natanz strike market reactions, central bank real policy rate divergence, super-busy CB week ahead
Date: June 13, 2025

## Charts to Reproduce

### Task 1: NASDAQ Sep-Nov 2024 with Geopolitical Event Annotations
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_nasdaq_geopolitical_2024_research.json`
- **output:** `project/research_studies/test_runner/amfx_nasdaq_geopolitical_2024_research/`
- **image_ref:** page_01_img_02.png
- **chart_type:** line chart with annotated event markers
- **data_sources:** QQQ-Stocks (NASDAQ 100 proxy), daily, Sep 15 to Nov 15 2024.
- **what_makes_it_interesting:** The annotations transform a simple price chart into a geopolitical narrative. Each red annotation (Iran missiles, Israel bombing, US election, MSFT/META disappointing) tells you what moved the market and — more importantly — what did NOT stick. The Iran/Israel events barely registered while earnings and the election drove the real moves. This is a macro trader's way of saying "geopolitics is noise, fundamentals matter."
- **reproduction_notes:** QQQ daily close line with 20d MA. Daily returns bar chart shows event impact magnitude. Cards show period high ($514.14), low ($471.44), and return. Original uses TradingView-style red text annotations which we approximate with reference lines and chart titles. 2 charts + 1 card set.
- **date_range:** 2024-09-15 to 2024-11-15

### Task 2: Crude Oil — Oct 2024 vs. Jun 2025 Geopolitical Reaction Comparison
- **status:** DONE (top panel only)
- **definition:** `project/definitions/test_runner/amfx_crude_geopolitical_2024_research.json`
- **output:** `project/research_studies/test_runner/amfx_crude_geopolitical_2024_research/`
- **image_ref:** page_01_img_01.png
- **chart_type:** stacked dual-panel line chart with annotations
- **data_sources:** CL-Futures (NYMEX WTI Crude Oil), daily, Sep 25 to Nov 25 2024.
- **what_makes_it_interesting:** The juxtaposition is the insight — the same $10 move (68 to 78) that took weeks in Oct 2024 happened in one hour in Jun 2025. We reproduce the Oct-Nov 2024 panel showing the multi-week rally. The Jun 2025 intraday panel (bottom half of original) is omitted as it requires Jun 2025 intraday futures data.
- **reproduction_notes:** WTI close line with $68 and $78 reference lines marking the key range. Daily range bar chart shows volatility spikes around geopolitical events. Cards show period high ($76.47), low ($66.92), last close ($68.94). The Jun 2025 intraday comparison panel is NOT reproduced — would require 1-min CL-Futures data for Jun 12-13, 2025.
- **date_range:** 2024-09-25 to 2024-11-25

### Task 3: Real Policy Rates Using Core CPI — Multi-Line Time Series
- **status:** BLOCKED (FRED rate-limiting)
- **definition:** `project/definitions/test_runner/amfx_real_policy_rates_research.json`
- **output:** `project/research_studies/test_runner/amfx_real_policy_rates_research/` (partial)
- **image_ref:** page_02_img_00.png
- **chart_type:** multi-line time series
- **data_sources:** Fed Funds Rate (FEDFUNDS via economic_indicators, cached), Core CPI (CPILFESL via common_economic_indicators, cache exists but FRED ALFRED refresh blocked). Original needs 10 central banks x 2 series each (policy rate + core CPI).
- **what_makes_it_interesting:** This is a signature macro chart — 10 central banks' real policy rates on one chart, spanning from pre-COVID through the inflation cycle and back. The dramatic plunge to -6%/-7% in 2021-2022 and the subsequent divergent recovery paths tell the entire post-COVID monetary policy story in one image.
- **blocking_reasons:**
  1. **FRED API rate-limiting:** FRED is returning "Access Denied" for all API requests. This blocks CPILFESL (Core CPI) and all international series. FedFunds loads from non-ALFRED cache (Mar 10), but CoreCPI ALFRED cache refresh fails.
  2. **International data gaps:** FRED does not have policy rate series for Sweden (Riksbank), Norway (Norges), Switzerland (SNB), Australia (RBA), or New Zealand (RBNZ). Only US, ECB, Canada, Japan, and UK (through 2017 only) have policy rate data on FRED.
  3. **Multi-country scope:** Original requires 10 countries x 2 series = 20 FRED series. Even without rate-limiting, 5 countries lack policy rate data on FRED.
- **reproduction_notes:** Definition is correctly written for US Fed real rate (FEDFUNDS - CoreCPI YoY). When FRED rate-limiting clears, the US-focused version will render correctly. Full 10-country reproduction requires non-FRED data sources.
- **date_range:** 2019-01-01 to 2025-06-13

### Task 4: Real Policy Rates Current Readings — Ranked Table
- **status:** BLOCKED (depends on Task 3 data)
- **image_ref:** page_02_img_01.png
- **chart_type:** table (color-coded heatmap)
- **data_sources:** Same as Task 3 — current snapshot of (policy rate minus core CPI) for each central bank.
- **blocking_reasons:**
  1. **Depends on Task 3:** Requires the same 10 countries' policy rates and core CPI data.
  2. **FRED rate-limiting:** Same FRED "Access Denied" issue as Task 3.
  3. **Static values:** The table shows specific point-in-time values (Riksbank 1.9%, Fed 1.7%, etc.) that are essentially static as of Jun 13, 2025. Even if data were available, EpochScript computes from time series — a `summary_table` with `Last` aggregation could show current values, but only for countries where data exists.
  4. **Color gradient not supported:** The green-to-red conditional heatmap coloring in the original table is not directly supported by EpochScript summary_table formatting.
- **reproduction_notes:** Could be added as a `summary_table` to the Task 3 definition once FRED data loads. Would show Fed, ECB, BoC, and BOJ real rates (4 of the 10 countries).

### Task 5: GameStop 1-Minute Chart — Microstructure Anomaly
- **status:** DONE
- **definition:** `project/definitions/test_runner/amfx_gme_microstructure_research.json`
- **output:** `project/research_studies/test_runner/amfx_gme_microstructure_research/`
- **image_ref:** page_03_img_01.png
- **chart_type:** intraday line chart (1-minute)
- **data_sources:** GME-Stocks, 1-minute, Jun 11-13 2025.
- **what_makes_it_interesting:** Shows one of the most unusual microstructure patterns — a massive resting bid that created a perfectly flat line at $21.54, absorbing all selling for an extended period. Donnelly called it "one of the weirdest 1-minute charts I have seen in a while."
- **reproduction_notes:** GME 1-minute close line chart with $21.54 reference line marking the massive bid wall. Second chart shows 1-min bar range to highlight compression at the support level. Cards show session high ($29.67), low ($21.82), last close ($22.93). The data covers Jun 11-12, 2025 (2 days, 1048 bars). The flat line at $21.54 and the steep decline from ~$24+ are visible in the data.
- **date_range:** 2025-06-11 to 2025-06-13

## Summary

| Task | Status | Definition |
|------|--------|------------|
| 1. NASDAQ Geopolitical 2024 | DONE | `amfx_nasdaq_geopolitical_2024_research.json` |
| 2. Crude Oil Geopolitical 2024 | DONE (top panel) | `amfx_crude_geopolitical_2024_research.json` |
| 3. Real Policy Rates Time Series | BLOCKED (FRED) | `amfx_real_policy_rates_research.json` |
| 4. Real Policy Rates Table | BLOCKED (data) | not created |
| 5. GameStop 1-Min Microstructure | DONE | `amfx_gme_microstructure_research.json` |

## Discarded Charts
| Chart | Reason |
|-------|--------|
| Trading calendar (page_04_img_00.png) | Well-designed economic calendar table for Jun 16-20 2025 (FOMC, BOJ, Riksbank, SNB, Norges, BoE all in one week), but calendars are time-specific operational tools, not reproducible research. The design template is noted for reference. |
| Donkey Kong screenshots (page_03) | Decorative gaming images relating to the "DK" section header |
| Ticker symbol meme (page_01) | Humorous non-quantitative content |
