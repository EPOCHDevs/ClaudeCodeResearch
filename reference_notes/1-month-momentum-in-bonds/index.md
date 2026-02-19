# 1 Month Momentum in Bonds

**Quantpedia ID**: #0426
**URL**: https://quantpedia.com/strategies/1-month-momentum-in-bonds
**Status**: INELIGIBLE
**Linear Issue**: [ENG-269](https://linear.app/epoch-inc/issue/ENG-269/feature-request-global-government-bond-futures-data-for-0426)

## Overview
This strategy exploits short-term momentum in government bonds. Contrary to stock-level evidence showing short-term reversals, government bonds exhibit a striking short-term momentum pattern: the most recent month's return positively predicts future performance. The effect is not explained by established return predictors and is robust across asset classes.

## Trading Rules
**Universe**: 10-year government bonds from 54 countries

**Signal**: Past 1-month return
1. Calculate past 1-month return for each government bond
2. Sort assets into quintiles by past month return
3. Long top quintile (highest returns in previous month)
4. Short bottom quintile (lowest returns in previous month)

**Selection**:
- Long top quintile (winners)
- Short bottom quintile (losers)

**Weighting**: Equally-weighted
**Rebalancing**: Monthly

## Fundamental Reason
- Short-term momentum is an independent phenomenon not explained by traditional long-term 12-month momentum
- Effect remains significant after controlling for market beta, idiosyncratic volatility, value, skewness, or seasonality
- Short-run momentum strategies in equities, bonds, and bills display commonality, suggesting a potential common factor
- The effect is strongest among assets of high idiosyncratic volatility and in periods of elevated return dispersion
- Partially serves as hedge for stocks during bear markets due to low correlation to equity market factor

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1961-2018 |
| Return | 6.04% p.a. |
| Volatility | 9.69% |
| Max Drawdown | -26.72% |
| Sharpe Ratio | 0.62 |

Note: Data from Table 8, 1961-2018, annualized monthly return (0.49%).

**WARNING**: OOS (2000-2025) shows -1.6% return, -0.20 Sharpe, -39.2% max drawdown. Strategy alpha has deteriorated significantly.

## Source Paper
Zaremba, Adam and Karathanasopoulos, Andreas and Long, Huaigang: Short-Term Momentum (Almost) Everywhere
- SSRN: https://ssrn.com/abstract=3340085

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238599/

## Eligibility Check
### Available
- **Transforms**:
  - `roc(period=21)` - 1-month return calculation
  - `cs_rank` - Cross-sectional ranking
  - `cs_quantile` - Quintile filtering
- **Assets**:
  - ZB-Futures (US Treasury Bond)
  - ZN-Futures (US Treasury Note)

### Missing
- **Global Government Bond Futures** - NOT AVAILABLE
  - Strategy requires 10-year bonds from 54 countries
  - Only US Treasury futures available (ZB, ZN)
  - Missing: German Bund, UK Gilt, Japanese JGB, French OAT, Italian BTP, etc.
  - Need comprehensive global sovereign bond futures coverage

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing global government bond futures
- Confidence rating: Strong (but OOS is negative)
- Complexity: Simple
- The transforms are straightforward (`roc`, `cs_rank`, `cs_quantile`)
- Primary blocker is asset availability, not technical capability
- Poor OOS performance (-0.20 Sharpe) suggests low implementation priority even if assets become available
- Could implement simplified version with available US Treasury futures only

