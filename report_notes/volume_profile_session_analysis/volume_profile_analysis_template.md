# Volume Profile Session Analysis — Equity RTH

## Overview

Comprehensive volume profile analysis framework for US equities. Analyzes the most recent completed Regular Trading Hours (RTH) session using Market Profile / Auction Market Theory principles.

**Applicable tickers:** Any liquid US equity or ETF (SPY, QQQ, AAPL, etc.)
**Session:** Equity RTH (09:30–16:00 ET)
**Initial Balance:** First 30 minutes (09:30–10:00 ET) — standard for equities
**Data resolution:** 1-minute or 5-minute bars

---

## Section 1: Session Overview

| Metric | Description |
|--------|-------------|
| **Session Date** | Date of the analyzed trading session |
| **Open** | First trade price at 09:30 ET |
| **High** | Highest price during RTH |
| **Low** | Lowest price during RTH |
| **Close** | Last trade price at 16:00 ET |
| **Session Range** | High minus Low (points and % of close) |
| **Total Volume** | Total shares traded during RTH |
| **Volume vs 20-Day Average** | Session volume / 20-day mean volume (ratio) |
| **Volume Conviction** | Low (<0.8x avg), Normal (0.8–1.2x), High (>1.2x), Extreme (>1.5x) |

---

## Section 2: Volume Profile Metrics

### Core Levels

| Metric | Description |
|--------|-------------|
| **VPOC** | Volume Point of Control — single price level with highest traded volume |
| **Value Area High (VAH)** | Upper boundary of the 70% volume value area |
| **Value Area Low (VAL)** | Lower boundary of the 70% volume value area |
| **Value Area Width** | VAH minus VAL (points and % of close) |

### Secondary Volume Nodes

| Metric | Description |
|--------|-------------|
| **High Volume Nodes (HVN)** | Price levels with locally elevated volume — secondary support/resistance |
| **Low Volume Nodes (LVN)** | Thin areas between volume clusters — prices tend to move quickly through these |
| **Single Prints** | Price levels visited only once with minimal volume — magnets for future revisit |

---

## Section 3: Initial Balance (IB)

The Initial Balance represents the first 30 minutes of RTH trading (09:30–10:00 ET). This is the range established by local/pit traders before larger timeframe participants typically enter.

| Metric | Description |
|--------|-------------|
| **IB High** | Highest price during 09:30–10:00 ET |
| **IB Low** | Lowest price during 09:30–10:00 ET |
| **IB Width** | IB High minus IB Low (points and % of close) |
| **IB vs 20-Day Average IB** | Current IB width / 20-day mean IB width (ratio) |

---

## Section 4: Opening Type Classification

Classify the opening based on market behavior in the first 15–30 minutes:

| Type | Description | Implication |
|------|-------------|-------------|
| **Open-Drive** | Market opens and moves directionally without looking back; no test of the open price | Strong conviction from one side; often leads to trend day |
| **Open-Test-Drive** | Opens, tests one direction briefly, then drives the other way with commitment | Participants confirmed their conviction; directional day likely |
| **Open-Rejection-Reverse** | Opens, drives in one direction, then sharply reverses through the opening price | Failed auction; the initial move was rejected by responsive participants |
| **Open-Auction** | Rotational, balanced activity around the open with no clear direction | Two-way trade; often a range-bound or normal day |

---

## Section 5: Close Analysis

### Close Relative to Key Levels

| Metric | Description |
|--------|-------------|
| **Close vs Value Area** | Inside (between VAL and VAH), Above (>VAH), or Below (<VAL) |
| **Close vs VPOC** | Above or Below the Volume Point of Control |
| **Close Percentile** | Where close falls within the session range: 0% = low, 100% = high |
| **Close vs IB** | Inside IB, Above IB High, Below IB Low |

**Formula:** Close Percentile = (Close - Low) / (High - Low) * 100

### Context Interpretation

| Close Position | Market Implication |
|----------------|-------------------|
| Close above VAH | Buyers in control; potential continuation higher |
| Close below VAL | Sellers in control; potential continuation lower |
| Close inside VA, above VPOC | Slight bullish lean, balanced session |
| Close inside VA, below VPOC | Slight bearish lean, balanced session |
| Close in upper 25% of range | Strong close, bullish |
| Close in lower 25% of range | Weak close, bearish |

---

## Section 6: Excess and Tails

| Metric | Description |
|--------|-------------|
| **Upper Tail** | Distance from session high down to the highest HVN (points) |
| **Lower Tail** | Distance from session low up to the lowest HVN (points) |
| **Poor High** | Session high has significant volume (no rejection) — incomplete auction, magnet for revisit |
| **Poor Low** | Session low has significant volume (no rejection) — incomplete auction, magnet for revisit |
| **Excess at High** | Long upper tail (>IB width / 2) — strong rejection of highs by responsive sellers |
| **Excess at Low** | Long lower tail (>IB width / 2) — strong rejection of lows by responsive buyers |

---

## Section 7: Day Type Classification (Dalton)

Based on range extension relative to the Initial Balance:

| Day Type | Criteria | Typical Behavior |
|----------|----------|------------------|
| **Normal Day** | Range extends ~1x IB on one side | Limited range expansion; balanced trade |
| **Normal Variation Day** | Range extends 1.5–2x IB on one side | Moderate directional conviction with rotation |
| **Trend Day** | Range extends >2x IB; single-direction movement; late close near extreme | Strongest directional conviction; one-timeframe activity |
| **Neutral Day** | Range extends equally on both sides of IB; close near IB midpoint | Equal buying and selling; pure rotation |
| **Non-Trend Day** | Narrow range, entirely within IB or barely extending | Very low conviction; compressed volatility, often precedes expansion |

### Extension Metrics

| Metric | Description |
|--------|-------------|
| **Upside Extension** | Session High minus IB High (points) |
| **Downside Extension** | IB Low minus Session Low (points) |
| **Extension Ratio (Up)** | Upside Extension / IB Width |
| **Extension Ratio (Down)** | Downside Extension / IB Width |

---

## Section 8: Profile Shape Classification

Based on volume distribution across the session's price range:

| Shape | Volume Distribution | Implication |
|-------|-------------------|-------------|
| **P-shape** | Heavy volume at highs, thin at lows | Short covering or late buying; price was auctioned up through low-volume area to find resistance at highs |
| **b-shape** | Heavy volume at lows, thin at highs | Long liquidation or responsive selling; price was auctioned down through thin area, found acceptance at lows |
| **D-shape** | Bell curve — volume concentrated in the middle, tapering at extremes | Balanced two-way trade; healthy price discovery. Neither buyers nor sellers dominated |
| **B-shape** | Double distribution — two distinct volume clusters with thin zone between | Two-timeframe activity; different participant groups active at different price levels. Thin zone = migration area |
| **Elongated / Trending** | Volume spread relatively evenly across a wide range | Sustained directional movement; one-timeframe participants in control. Classic trend day shape |

---

## Section 9: Prior Session Context

| Metric | Description |
|--------|-------------|
| **Prior Session VPOC** | Previous day's VPOC level |
| **VPOC Migration** | Did today's VPOC move higher, lower, or overlap with prior VPOC? |
| **Gap from Prior VA** | Distance from today's open to prior session's VAH/VAL |
| **Gap Type** | Open above prior VAH (gap up), below prior VAL (gap down), or inside prior VA (no gap) |
| **Gap Fill** | Did price revisit the prior session's value area? (Yes/No) |
| **Prior Day High/Low** | Reference for breakout/failed breakout analysis |
| **Acceptance/Rejection** | Did price spend >30 minutes inside the prior value area (acceptance) or quickly leave (rejection)? |

---

## Section 10: Volume Delta (if available)

| Metric | Description |
|--------|-------------|
| **Session Cumulative Delta** | Total buy volume minus total sell volume for the session |
| **Delta at VPOC** | Net buying/selling pressure at the highest-volume price |
| **Delta Direction** | Positive = buyers dominated, Negative = sellers dominated |
| **Delta vs Price Direction** | Confirming (delta aligns with price move) or Diverging (delta opposes price move) |

*Note: Delta requires tick-level or trade-level data with buy/sell classification. May not be available for all data sources.*

---

## Section 11: Composite Assessment

### Who Was in Control?

Based on the combined evidence from profile shape, close position, IB extension, and opening type:

| Assessment | Evidence Pattern |
|------------|-----------------|
| **Buyers dominated** | P-shape or Trend up; close above VAH; extension >2x IB upward; Open-Drive up |
| **Sellers dominated** | b-shape or Trend down; close below VAL; extension >2x IB downward; Open-Drive down |
| **Balanced / Rotational** | D-shape; close inside VA; extensions roughly equal; Neutral or Non-Trend day |
| **Two-timeframe battle** | B-shape; close near migration zone; opposing IB extensions; Open-Auction |

### Actionable Context for Next Session

| Scenario | Setup to Watch |
|----------|----------------|
| Close above VAH | Continuation bias; look for acceptance above or rejection back into VA |
| Close below VAL | Continuation bias; look for acceptance below or rejection back into VA |
| Poor high/low | Likely revisited; magnet for price in next session |
| Single prints | Likely filled; watch for price to return to these levels |
| Trend day close at extreme | Follow-through expected; fading is high-risk |
| Narrow IB + Non-Trend day | Volatility expansion likely next session; breakout setup |

---

## Output Format Summary

When running this analysis, return all sections above populated with actual data. Present as:

1. **Hero cards** — Session OHLC, VPOC, VAH, VAL, Volume conviction
2. **IB cards** — IB High, IB Low, IB Width, Opening Type
3. **Close analysis cards** — Close vs VA, Close vs VPOC, Close percentile, Day type
4. **Profile shape card** — Classification with explanation
5. **Prior session context cards** — VPOC migration, gap status, acceptance/rejection
6. **Timeseries chart** — Price with VPOC, VAH, VAL, IB High, IB Low overlaid
7. **Volume profile histogram** — Volume distribution by price level (horizontal)
8. **Event markers** — Key levels breached (IB break, VA break, prior day high/low test)
9. **Summary table** — All metrics in structured grid
10. **Composite assessment** — Plain-text interpretation of who controlled the session

---

## Ticker Parameterization

Replace `[TICKER]` with the target equity. Recommended liquid names:

| Ticker | Description | Why |
|--------|-------------|-----|
| SPY | S&P 500 ETF | Most liquid equity, benchmark |
| QQQ | NASDAQ 100 ETF | Tech-heavy, high volume |
| IWM | Russell 2000 ETF | Small cap proxy |
| AAPL | Apple Inc | Most liquid single stock |
| TSLA | Tesla Inc | High volume, wide ranges |
| NVDA | NVIDIA Corp | High volume, trending |
