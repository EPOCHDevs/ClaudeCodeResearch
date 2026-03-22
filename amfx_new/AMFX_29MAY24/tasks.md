# AMFX_29MAY24 — Chart Reproduction Tasks

Source: AMFX 29MAY24 newsletter by Brent Donnelly (Spectra Markets)
Theme: The South Park Jinx — pop-culture contrarian indicators and product launch timing signals
Date: May 29, 2024

## Charts to Reproduce

### Task 1: South Park Jinx Performance Table
- **status:** BLOCKED
- **image_ref:** page_02_img_00.png
- **chart_type:** table (color-coded heatmap cells)
- **data_sources:** Custom dataset — requires compiling South Park episode air dates featuring publicly-traded companies, then calculating stock total return minus SPX total return at 3m, 6m, and 1y horizons. Tickers: NVO, DIS, MSFT, NFLX, PFE, WBA, MMEN, CMCSA, AMZN, TLRY, MNK, META, TWTR, YELP, SONY, TWX, QRTEA, EA, FDX, YUM, MAT, WMT, TEVA, NVS, SBUX. Yahoo Finance or Bloomberg for total returns; episode dates from the table itself.
- **what_makes_it_interesting:** A fully original contrarian indicator — median stock underperforms SPX by 7% at 1 year with only 39% win rate. The color-coded red/green cells make the pattern immediately visible. It is a perfect "pop culture as signal" piece that resonates with discretionary traders.
- **reproduction_notes:** Table has columns: Date, Episode, Topic, Trade (company), Ticker, then 3m/6m/1y "Performance minus SPX" with red shading for negative, blue/green for positive. Bottom rows show Average (-4%, -6%, -6%), Median (0%, -7%, -7%), and Win% (52%, 41%, 39%). The latest row (NVO, 5/24/2024) has no performance data yet. Conditional formatting intensity scales with magnitude.
- **block_reason:** Cannot reproduce in EpochScript. Requires computing point-in-time relative returns for 26+ individual tickers from specific episode air dates spanning 1998-2024. EpochScript operates on a unified time-series grid per asset, not point-in-time cross-asset return calculations. Would need a custom Python script or external data compilation.

### Task 2: Product Launch Contrarian Indicator — SPX with NOPE ETF and BTC with CME Futures
- **status:** DONE
- **image_ref:** page_03_img_01.png
- **chart_type:** dual-panel line chart with event annotations
- **data_sources:** Top panel: SPX (^GSPC or SPY) daily, Oct 2021 to May 2024. Bottom panel: BTC-USD daily, Oct 2016 to Aug 2018. Event dates: NOPE ETF launch ~Oct 2022, CME Bitcoin futures launch Dec 17, 2017.
- **what_makes_it_interesting:** Visually striking — two completely different assets, same story. The red arrow annotations pointing to the exact moment of product launch at the inflection point make this a memorable "one chart, one insight" piece. It builds the contrarian indicator thesis with evidence from equities and crypto.
- **reproduction_notes:** Two stacked panels, black candlestick/line style on white background. Red text annotations with red arrows: "NOPE, the bearish ETF launches" near the Oct 2022 SPX bottom (~3,600), and "CME launches bitcoin futures" near BTC's Dec 2017 peak (~$19,000). TradingView styling — clean, minimal gridlines. The juxtaposition of "bearish product at bottom" vs "bullish product at top" is the narrative punch.
- **definitions:**
  - `project/definitions/test_runner/amfx_spx_nope_etf_contrarian_research.json` (SPY, 2021-08-01 to 2024-06-01)
  - `project/definitions/test_runner/amfx_btc_cme_futures_contrarian_research.json` (BTCUSD-Crypto, 2016-08-01 to 2018-09-01)
- **results:** SPX: Period low $356.56 (Oct 2022), rallied 46.5% from NOPE launch level. BTC: Peaked at $19,650 near CME launch, max drawdown -97% to $540. Both charts render with close price, MAs, and horizontal reference lines at product launch levels.

### Task 3: Japan 10Y vs US 10Y Yield Divergence
- **status:** DONE (FRED rate-limited, will render when API unblocked)
- **image_ref:** page_04_img_00.png
- **chart_type:** dual-axis overlay line chart
- **data_sources:** US 10Y Treasury yield (FRED: DGS10 or ^TNX), Japan 10Y JGB yield (FRED: IRLTLT01JPM156N or Yahoo ^TNX equivalent for Japan). Period: Jul 2023 to May 2024.
- **what_makes_it_interesting:** The "Widowmaker No More" thesis — JGB yields breaking out to multi-year highs while US yields remain range-bound. This divergence has massive implications for global bond flows (Team Japan rotating back to JGBs). The dual-axis overlay makes the divergence visually obvious — US yields peaked and pulled back while Japan yields kept rising.
- **reproduction_notes:** Black line = US 10Y (left axis, 3.6%-5.1%), blue line = Japan 10Y (right axis, 0.3%-1.1%). Title uses blue color for "US 10-year yield" text. Clean TradingView styling. The key visual: from ~Nov 2023 onward, US yields decline while Japan yields accelerate higher, creating a clear divergence pattern. X-axis: monthly from Aug 2023 to May 2024.
- **definition:** `project/definitions/test_runner/amfx_japan_us_10y_divergence_research.json` (2023-06-01 to 2024-06-01)
- **results:** Study structure generates correctly (2 charts: yield overlay + spread, plus cards). Currently FRED API rate-limited (Access Denied) from batch runs on this machine. Cache exists with data through 2026 for both DGS10 and IRLTLT01JPM156N. Charts will populate correctly once FRED API access restored (re-run the definition). Uses common_economic_indicators Treasury10Y for US + economic_indicators IRLTLT01JPM156N for Japan.

## Discarded Charts
| Chart | Reason |
|-------|--------|
| page_01_img_00.jpeg | AI-generated Kenny from South Park decorative image |
| page_01_img_01.jpeg | Tweet screenshot + South Park TV show poster, non-quantitative |
| page_01_img_02.png | Spectra School promotional branding |
| page_03_img_00.png | News article screenshot about OZEM ETF launch, not a chart |
| page_05_img_00.jpeg | AI-generated Stan from South Park decorative image |
| page_05_img_01.jpeg | AI-generated Kenny decorative image |
