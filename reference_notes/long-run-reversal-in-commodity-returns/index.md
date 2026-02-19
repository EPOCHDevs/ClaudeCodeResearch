# Long-Run Reversal in Commodity Returns

**Quantpedia ID**: #0424
**URL**: https://quantpedia.com/strategies/long-run-reversal-in-commodity-returns
**Status**: ELIGIBLE
**Linear Issue**: [ENG-267](https://linear.app/epoch-inc/issue/ENG-267/implement-long-run-reversal-in-commodity-returns-0424)

## Overview
This strategy exploits the long-run reversal effect in commodity markets. Commodities that have performed well over the past 3 years tend to underperform in the future, while underperformers tend to outperform. This is a pure price-based anomaly driven by long-term supply and demand cycles rather than macroeconomic risks.

## Trading Rules
**Universe**: 52 commodity futures

**Signal**: 3-year cumulative return
1. Calculate 3-year cumulative return for each commodity
2. Rank commodities by past 3-year returns
3. Sort into quintiles

**Selection**:
- Short top quintile (past winners)
- Long bottom quintile (past losers)

**Weighting**: Equally-weighted
**Rebalancing**: Yearly

## Fundamental Reason
- Long-run reversal driven by supply/demand cycles, not macroeconomic risks
- High prices signal low supply relative to demand, leading to subsequent supply increases
- Low prices signal abundant supply, leading to subsequent supply decreases
- Effect is strongest in high-idiosyncratic-volatility commodities
- Independent of market state (bull/bear) and volatility regime
- Observed across all centuries from 1265 to 2017

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1900-2017 |
| Return | 16.03% p.a. |
| Volatility | 19.37% |
| Max Drawdown | -91.46% |
| Sharpe Ratio | 0.83 |

Note: Data from Table 5, 20th-21st century.

**WARNING**: OOS backtest (1992-2025) shows lower performance: 4.9% return, 0.01 Sharpe ratio. Strategy alpha may be deteriorating.

## Source Paper
Zaremba, Adam and Bianchi, Robert J. and Mikutowski, Mateusz: Long-Run Reversal in Commodity Returns: Insights from Seven Centuries of Evidence
- SSRN: https://ssrn.com/abstract=3314834

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238564/

## Eligibility Check
### Available
- **Transforms**:
  - `roc(period=756)` - 3-year return calculation (~756 trading days)
  - `cs_rank` - Cross-sectional ranking for quintile sorting
  - `cs_quantile` - Quantile filtering
- **Assets**:
  - GC-Futures (Gold)
  - CL-Futures (Crude Oil)
  - NG-Futures (Natural Gas)
  - ZC-Futures (Corn)
  - ZS-Futures (Soybeans)
  - ZW-Futures (Wheat)
  - SI-Futures (Silver)
  - HG-Futures (Copper)
  - And many more commodity futures

### Formula
```
# 3-year cumulative return
reversal_signal = roc(period=756)

# Rank commodities
ranks = cs_rank()(reversal_signal)

# Long bottom quintile, Short top quintile
long_signal = cs_quantile(quantile=0.2)(reversal_signal)
short_signal = cs_quantile(quantile=0.8)(reversal_signal)
```

## Implementation Notes
- Strategy is marked ELIGIBLE with all required transforms available
- Confidence rating: Moderate (OOS shows lower performance)
- Complexity: Simple (yearly rebalancing, quintile sorting)
- Works as hedge during recessions
- May not have full 52 commodities - implement with available futures
- Yearly rebalancing keeps turnover very low
- Deep max drawdown (-91%) - consider position sizing

