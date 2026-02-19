# 1 Month Momentum in Commodities

**Quantpedia ID**: #0428
**URL**: https://quantpedia.com/strategies/1-month-momentum-in-commodities
**Status**: ELIGIBLE
**Linear Issue**: [ENG-271](https://linear.app/epoch-inc/issue/ENG-271/implement-1-month-momentum-in-commodities-0428)

## Overview
This strategy exploits short-term momentum in commodity futures. Contrary to individual stock-level evidence showing short-term reversals, commodities exhibit a striking short-term momentum pattern: the most recent month's return positively predicts future cross-sectional performance. The effect is independent of traditional 12-month momentum and robust across market conditions.

## Trading Rules
**Universe**: 48 commodities (agricultural, industrials, energy, precious metals) - implementable with ~20 futures

**Signal**: Past 1-month return
1. Calculate past 1-month return for each commodity
2. Sort commodities into quintiles by past month return
3. Long top quintile (highest returns in previous month)
4. Short bottom quintile (lowest returns in previous month)

**Selection**:
- Long top quintile (winners)
- Short bottom quintile (losers)

**Weighting**: Equally-weighted
**Rebalancing**: Monthly

## Fundamental Reason
- Short-term momentum is an independent phenomenon not explained by traditional 12-month momentum
- Effect remains significant after controlling for market beta, idiosyncratic volatility, value, skewness, or seasonality
- Short-run momentum strategies across commodities, equities, bonds, and currencies display commonality
- Effect is strongest among assets of high idiosyncratic volatility and in periods of elevated return dispersion
- Partially serves as hedge for stocks (uncorrelated to equity market factor)

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1961-2018 |
| Return | 21.12% p.a. |
| Volatility | 20.86% |
| Max Drawdown | -80.18% |
| Sharpe Ratio | 1.01 |

Note: Data from Table 8, 1961-2018, annualized monthly return (1.61%).

**WARNING**: OOS (1991-2025) shows -0.3% return, -0.01 Sharpe, -80.3% max drawdown. Strategy alpha has deteriorated completely.

## Source Paper
Zaremba, Adam and Karathanasopoulos, Andreas and Long, Huaigang: Short-Term Momentum (Almost) Everywhere
- SSRN: https://ssrn.com/abstract=3340085

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238621/

## Eligibility Check
### Available
- **Transforms**:
  - `roc(period=21)` - 1-month return calculation
  - `cs_rank` - Cross-sectional ranking
  - `cs_quantile` - Quintile filtering
- **Assets** (~20 commodity futures available):
  - **Energy**: CL-Futures (Crude Oil), NG-Futures (Natural Gas)
  - **Precious Metals**: GC-Futures (Gold), SI-Futures (Silver), PA-Futures (Palladium), PL-Futures (Platinum)
  - **Base Metals**: HG-Futures (Copper)
  - **Grains**: ZC-Futures (Corn), ZS-Futures (Soybeans), ZW-Futures (Wheat), ZM-Futures (Soybean Meal), ZL-Futures (Soybean Oil), ZO-Futures (Oats)
  - **Softs**: KC-Futures (Coffee), SB-Futures (Sugar), CC-Futures (Cocoa), CT-Futures (Cotton)
  - **Meats**: LH-Futures (Lean Hogs), LE-Futures (Live Cattle), LC-Futures (Live Cattle), HE-Futures (Lean Hogs)

### Formula
```
# 1-month return for each commodity
mom_signal = roc(period=21)

# Rank by past month return
ranks = cs_rank()(mom_signal)

# Long top quintile, Short bottom quintile
long_signal = cs_quantile(quantile=0.8)(mom_signal)
short_signal = cs_quantile(quantile=0.2)(mom_signal)
```

## Implementation Notes
- Strategy is marked ELIGIBLE with ~20 commodity futures available (vs. 48 in original)
- Confidence rating: Strong (but OOS is essentially flat/negative)
- Complexity: Simple
- All required transforms are available
- Can implement with reduced universe of available commodity futures
- Extreme max drawdown (-80%) in both IS and OOS periods
- Poor OOS performance (-0.01 Sharpe) suggests very low implementation priority
- Strategy alpha appears completely eroded in recent years

