# Impact of Overnight Returns and Daytime Reversals to Future Stock Returns

**Quantpedia ID**: #0425
**URL**: https://quantpedia.com/strategies/impact-of-overnight-returns-and-daytime-reversals-to-future-stock-returns
**Status**: INELIGIBLE
**Linear Issue**: [ENG-268](https://linear.app/epoch-inc/issue/ENG-268/feature-request-rolling-pattern-count-transform-for-0425)

## Overview
This strategy exploits the "tug of war" between overnight noise traders and daytime informed investors. Stocks with high frequency of positive overnight returns followed by negative daytime reversals (noise trader risk) outperform stocks with low frequency of such reversals. The abnormal frequency of negative daytime reversals predicts future returns.

## Trading Rules
**Universe**: NYSE, AMEX, NASDAQ stocks (exclude financial and utility)

**Signal**: Abnormal Frequency of Negative Daytime Reversals (AB_NR)
1. Decompose daily returns into overnight (close-to-open) and daytime (open-to-close)
2. Identify negative daytime reversals: positive overnight return followed by negative daytime return
3. Calculate NR = frequency (%) of negative daytime reversals in month t
4. AB_NR = NR / average(NR over past 12 months)
5. Sort stocks by AB_NR into quintiles
6. Double-sort by SIZE (market cap) into terciles

**Selection**:
- From large stocks (top tercile by size):
  - Long top AB_NR quintile (high reversal frequency)
  - Short bottom AB_NR quintile (low reversal frequency)

**Weighting**: Equally-weighted
**Rebalancing**: Monthly

## Fundamental Reason
- Positive overnight returns followed by negative daytime reversals suggest a daily tug of war between noise traders (overnight) and informed investors (daytime)
- High frequency of such reversals indicates persistent noise trader risk
- Investors demand a premium for trading stocks prone to noise trader risk
- The pattern persists over time, justifying the risk premium
- Retail investors comprise greater portion of volume during high-reversal months

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1993-2017 |
| Return | 5.28% p.a. |
| Volatility | 6.43% |
| Max Drawdown | -25.71% |
| Sharpe Ratio | 0.82 |

Note: Data from Table 3, Panel B, SIZE H (large stocks).

**WARNING**: OOS (2010-2025) shows -2.1% return, -0.02 Sharpe. Strategy alpha has deteriorated.

## Source Paper
Akbas, Ferhat and Boehmer, Ekkehart and Jiang, Chao and Koch, Paul D.: Overnight Returns, Daytime Reversals, and Future Stock Returns
- SSRN: https://ssrn.com/abstract=3324880

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238589/

## Eligibility Check
### Available
- **Transforms**:
  - `session_gap` - Provides prior session close (psc) for overnight calculation
  - OHLC bars with open/close for daytime return calculation
  - `cs_rank` - Cross-sectional ranking
  - `market_cap` - For size sorting
- **Assets**: US Stocks available

### Missing
- **Rolling Pattern Count** - NOT DIRECTLY AVAILABLE
  - Need to count frequency of specific pattern (positive overnight + negative daytime) in a month
  - Requires rolling window sum of boolean conditions
- **Rolling Normalization by Historical Average** - COMPLEX
  - AB_NR = NR / 12-month average NR
  - Requires rolling average of monthly counts
- **Intraday Return Decomposition Workflow** - COMPLEX
  - Overnight: (Open - psc) / psc
  - Daytime: (Close - Open) / Open
  - Identifying when overnight > 0 AND daytime < 0

## Implementation Notes
- Strategy is marked INELIGIBLE due to complexity of reversal frequency calculation
- Confidence rating: Strong (but OOS is negative)
- Complexity: Very Complex
- The building blocks exist but workflow is complex:
  1. Compute overnight return using session_gap.psc
  2. Compute daytime return from OHLC
  3. Count negative daytime reversals in a month
  4. Normalize by 12-month average
  5. Double-sort by AB_NR and SIZE
- Poor OOS performance suggests low implementation priority

