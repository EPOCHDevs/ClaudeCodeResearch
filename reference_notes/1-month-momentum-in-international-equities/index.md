# 1 Month Momentum in International Equities

**Quantpedia ID**: #0427
**URL**: https://quantpedia.com/strategies/1-month-momentum-in-international-equities
**Status**: ELIGIBLE
**Linear Issue**: [ENG-270](https://linear.app/epoch-inc/issue/ENG-270/implement-1-month-momentum-in-international-equities-0427)

## Overview
This strategy exploits short-term momentum in international equity markets. Contrary to individual stock-level evidence showing short-term reversals, equity country indices exhibit a striking short-term momentum pattern: the most recent month's return positively predicts future cross-sectional performance. The effect is independent of traditional 12-month momentum and robust across market states.

## Trading Rules
**Universe**: 45 equity markets (developed, emerging, frontier countries) - implementable with ~35 country ETFs

**Signal**: Past 1-month return
1. Calculate past 1-month return for each country equity index
2. Sort assets into quintiles by past month return
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
- Short-run momentum strategies across equities, bonds, and currencies display commonality
- Effect is strongest among assets of high idiosyncratic volatility and in periods of elevated return dispersion
- The true mechanism driving short-term momentum remains under investigation

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1961-2018 |
| Return | 16.21% p.a. |
| Volatility | 20.38% |
| Max Drawdown | -63.37% |
| Sharpe Ratio | 0.80 |

Note: Data from Table 8, 1961-2018, annualized monthly return (1.26%).

**WARNING**: OOS (2010-2025) shows -2.9% return, -0.17 Sharpe, -63.2% max drawdown. Strategy alpha has deteriorated significantly.

## Source Paper
Zaremba, Adam and Karathanasopoulos, Andreas and Long, Huaigang: Short-Term Momentum (Almost) Everywhere
- SSRN: https://ssrn.com/abstract=3340085

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238617/

## Eligibility Check
### Available
- **Transforms**:
  - `roc(period=21)` - 1-month return calculation
  - `cs_rank` - Cross-sectional ranking
  - `cs_quantile` - Quintile filtering
- **Assets** (~35 country/regional ETFs available):
  - **Americas**: SPY (US), EWC (Canada), EWW (Mexico), EWZ (Brazil), ARGT (Argentina), ECH (Chile)
  - **Europe**: EWG (Germany), EWU (UK), EWQ (France), EWI (Italy), EWP (Spain), EWN (Netherlands), EWL (Switzerland), EWK (Belgium), EWD (Sweden), EWO (Austria), EPOL (Poland), GREK (Greece), TUR (Turkey), VGK (Europe)
  - **Asia-Pacific**: EWJ (Japan), EWY (South Korea), EWT (Taiwan), EWH (Hong Kong), EWS (Singapore), EWA (Australia), ENZL (New Zealand), EWM (Malaysia), FXI (China), INDA (India), THD (Thailand), EIDO (Indonesia), EPHE (Philippines)
  - **Broad**: EFA (EAFE), EEM (Emerging Markets), VWO (Emerging Markets)

### Formula
```
# 1-month return for each country ETF
mom_signal = roc(period=21)

# Rank by past month return
ranks = cs_rank()(mom_signal)

# Long top quintile, Short bottom quintile
long_signal = cs_quantile(quantile=0.8)(mom_signal)
short_signal = cs_quantile(quantile=0.2)(mom_signal)
```

## Implementation Notes
- Strategy is marked ELIGIBLE with ~35 country ETFs available (vs. 45 in original)
- Confidence rating: Strong (but OOS is very negative)
- Complexity: Simple
- All required transforms are available
- Can implement with reduced universe of available country ETFs
- Deep max drawdown (-63%) in both IS and OOS periods
- Poor OOS performance (-0.17 Sharpe) suggests low implementation priority
- Consider hedging or position sizing due to extreme drawdowns

