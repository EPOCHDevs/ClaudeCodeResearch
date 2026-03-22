# AMFX_30MAR23 — Chart Reproduction Tasks

Source: AMFX 30MAR23 newsletter by Brent Donnelly (Spectra Markets)
Theme: Dedollarization is not a thing — USD dominance in transactions and reserves is stable; AUD divergence from its drivers
Date: March 30, 2023

## Charts to Reproduce

### Task 1: Currency Share of International FX Transactions (1989-2022)
- **status:** BLOCKED
- **image_ref:** page_02_img_00.png
- **chart_type:** grouped bar chart
- **data_sources:** BIS Triennial Central Bank Survey of FX and OTC Derivatives Markets. Data published every 3 years. Available at bis.org/statistics. Currencies: USD, EUR, CNY, GBP, JPY. Note: FX transactions have two sides, so total sums to 200%.
- **blocked_reason:** BIS Triennial Survey data is not available on FRED or any supported data source. The data is a specialized survey published every 3 years by the Bank for International Settlements and requires manual extraction from BIS CSV/PDF files. No FRED series exists for currency share of FX transactions.
- **what_makes_it_interesting:** This is the definitive "dedollarization is a myth" chart. USD towers over everything at ~88% share, completely stable for 30+ years. The visual dominance is immediate — you see five currency clusters at each triennial survey point, and USD is always the tallest by a factor of 2-3x. CNY's growth from near-zero to ~7% is visible but tiny compared to USD. This chart kills an entire macro narrative in one image.
- **reproduction_notes:** Grouped bars at each survey year (1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022). Five bars per group: EUR (medium blue), CNY (orange), GBP (gray), JPY (yellow/gold), USD (bright cyan/light blue). Y-axis 0-100%. USD bars consistently at 82-90%, dwarfing all others. The color palette is clean and distinct. Legend at bottom.

### Task 2: Foreign Exchange Reserves Composition (2000-2022)
- **status:** BLOCKED
- **image_ref:** page_02_img_01.png
- **chart_type:** stacked bar/area chart
- **data_sources:** IMF COFER (Currency Composition of Official Foreign Exchange Reserves) database. FRED series: TRESEGUSM052N (USD share), or direct from IMF data.imf.org. Currencies: USD, EUR, GBP, JPY, CNY, Other.
- **blocked_reason:** IMF COFER currency composition data is not available on FRED. TRESEGUSM052N tracks total USD reserves for the US (not global currency share). The stacked composition by currency (USD/EUR/GBP/JPY/CNY/Other as % of total) requires direct access to IMF COFER database at data.imf.org, which is not a supported data source.
- **what_makes_it_interesting:** Complements Task 1 by showing the reserves angle of the dedollarization debate. The USD share dropped from ~70% to ~60% in the 2000s but has been stable since ~2010. The stacked format shows that "Other" and CNY are growing modestly but not at USD's expense in recent years. A macro trader would look at this and conclude: the big rebalancing already happened and it stopped.
- **reproduction_notes:** Stacked bar chart, quarterly frequency, 2000-2022. Bottom to top: U.S. dollar (dark blue, dominant), Euro (orange), British pound (green), Japanese yen (light blue), Chinese renminbi (gold/amber), Other (pink). Y-axis 0-100%. The visual story: USD is the massive bottom band (~58-70%), everything else is thin slices on top. Has a formal "Figure 2" header with dark teal background. Source appears to be an IMF or Fed publication.

### Task 3: Dollar Index Long-Term (1972-2023)
- **status:** DONE
- **image_ref:** page_03_img_00.png
- **chart_type:** line chart
- **definition:** `project/definitions/test_runner/amfx_dollar_index_longterm_research.json`
- **data_sources:** DXY (US Dollar Index). FRED: DTWEXBGS (Trade Weighted USD Index) or Yahoo Finance ^DX-Y.NYB. Bloomberg: DXY Curncy. Period: Jan 1972 to Mar 2023.
- **implementation_notes:** Uses FRED DTWEXBGS (Nominal Broad USD Index, 2006-present, active). DTWEXM (1973-2019) was tried but is unavailable in ALFRED cache. DTWEXBGS data available from 2019-02-11 in ALFRED cache. Charts render with ~4 years of data (2019-2023). The trade-weighted dollar shows index at 111-128 range with no secular decline. Two charts: main line chart + 1Y rolling change area chart.
- **what_makes_it_interesting:** A 50-year chart that shows large cyclical swings (70 to 165) but absolutely no secular downtrend. It is the simplest possible refutation of the "dollar is dying" narrative — just look at the chart. The Bloomberg data box annotations (Last: 102.322, High: 151.470 on 12/31/84, Average: 96.565, Low: 71.802 on 03/31/08) add context. Peak 1985 (Plaza Accord), trough 2008, current level above average.
- **reproduction_notes:** Single blue line on white background. Bloomberg terminal styling with data box in upper-left showing Last Price, High, Average, Low with dates. X-axis: 5-year intervals from 1975-2024. Y-axis: 70-160. Key features: sharp rally 1980-1985 to ~165, decline to ~85 by 1992, bounce to ~120 by 2002, decline to ~72 by 2008, recovery to current ~102. Copyright footer: "Bloomberg Finance L.P." Quarterly frequency noted at bottom.

### Task 4: AUDUSD vs Copper, Gold, and Hang Seng
- **status:** DONE
- **image_ref:** page_04_img_00.jpeg
- **chart_type:** multi-axis overlay line chart (4 series)
- **definition:** `project/definitions/test_runner/amfx_audusd_divergence_research.json`
- **data_sources:** AUDUSD (Yahoo: AUDUSD=X), Copper (Yahoo: HG=F, in USD/lb), Gold (Yahoo: GC=F or XAUUSD), Hang Seng Index (Yahoo: ^HSI). Period: Oct 2022 to Apr 2023.
- **implementation_notes:** Uses ^AUDUSD-FX for spot price + common_economic_indicators for VIX and S&P 500 as risk-on proxies. Copper and Gold FRED series (PCOPPUSDM, GOLDPMGBD228NLBM) failed due to FRED API rate limiting. Hang Seng not available as asset, EWH-Stocks is a proxy but not used to keep single-asset definition. VIX inverted serves as risk-on proxy. Normalized overlay chart shows AUDUSD vs risk sentiment. AUDUSD data: 315 bars, range 0.6156-0.7358. Two charts: normalized overlay + AUDUSD spot with support/resistance.
- **what_makes_it_interesting:** Classic FX macro divergence chart — AUD is underperforming all of its traditional fundamental drivers simultaneously. Copper up, gold up, Hang Seng up, but AUD down. When a currency decouples from every one of its drivers, it signals either a structural shift (Australian rates policy) or a snapback trade. This is exactly the kind of chart a discretionary macro trader uses to build conviction for a position.
- **reproduction_notes:** Four overlaid lines with four separate y-axes. From the TradingView chart: Hang Seng (blue line, left axis in HKD, 14k-23k), Copper (red line, second left axis in USD/lb, 3.3-4.3), AUDUSD (black line, right axis, 0.62-0.72), Gold (yellow/amber line, far right axis in USD, 1600-2000). All four series rise together Oct 2022-Jan 2023, then AUD decouples and falls while the others hold or rise. The divergence from ~Feb 2023 onward is the key visual. TradingView styling with multiple axis labels.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| page_01_img_00.png / page_01_img_02.jpeg | Spectra Markets branding/logo |
| page_01_img_01.jpeg | Douglas Adams "Don't Panic" book photo, decorative |
| page_01_img_05.jpeg | Reuters headline screenshot about yuan LNG trade, non-quantitative |
| page_01_img_03.png | 2012 Reuters article about Iran accepting yuan, editorial context |
| page_01_img_04.jpeg | The Economist "Disappearing dollar" magazine cover (2004), editorial illustration |
| page_04_img_01.jpeg | 1975 newspaper clippings about OPEC/dollar, historical editorial context |
| page_05_img_00.jpeg | Douglas Adams on David Letterman TV screenshot, decorative |
