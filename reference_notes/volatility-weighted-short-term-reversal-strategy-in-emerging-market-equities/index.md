# Volatility-Weighted Short-Term Reversal Strategy in Emerging Market Equities

**Quantpedia ID**: #0430
**URL**: https://quantpedia.com/strategies/volatility-weighted-short-term-reversal-strategy-in-emerging-market-equities
**Status**: ELIGIBLE
**Linear Issue**: [ENG-273](https://linear.app/epoch-inc/issue/ENG-273/implement-volatility-weighted-short-term-reversal-in-em-equities-0430)

## Overview
This strategy applies a volatility-weighted reversal approach to emerging market country ETFs. It goes long when current month returns are below the 3-month average (expecting mean reversion) and allocates capital using inverse volatility weighting to focus on markets where timing has the most impact.

## Trading Rules
**Universe**: 15 emerging market ETFs (implementable with 13+)

**Signal**: Short-term reversal with volatility weighting
1. Calculate current month return for each country ETF
2. Calculate 3-month average return for each country
3. Go long when current month return < 3-month average (reversal signal)
4. Go to cash when current month return > 3-month average
5. Weight country bets by inverse volatility of markets

**Selection**:
- Long countries with reversal signal (current return below average)
- Cash for countries without signal

**Weighting**: Inverse volatility weighted
**Rebalancing**: Monthly

## Fundamental Reason
- Volatility-weighted bets improve exploitation of market timing
- Higher volatility markets offer more opportunity for mean reversion
- Tilting bets to more volatile markets captures bigger returns
- Avoids wasting effort on small, insignificant deviations
- Decreases overall risk compared to equally-weighted approach
- Effect is stronger in emerging markets with higher volatility

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2005-2017 |
| Return | 6.14% p.a. |
| Volatility | 9.1% |
| Max Drawdown | -47.86% |
| Sharpe Ratio | 0.67 |

Note: Data from Table 4.

**WARNING**: OOS (2012-2025) shows -0.2% return, -0.01 Sharpe, -49.3% max drawdown. Strategy alpha has deteriorated.

## Source Paper
Kaloyan Petkov, Plamen Patev: Maximize Market Timing Returns: Implementing Volatility-Weighted Bets
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3339268

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238630/

## Eligibility Check
### Available
- **Transforms**:
  - `roc(period=21)` - Monthly return calculation
  - `sma(period=63)` or `ma` - 3-month average return
  - `std` - Volatility calculation for weighting
- **Assets** (13+ EM country ETFs available):
  - **Asia**: FXI (China), EWH (Hong Kong), EWT (Taiwan), EWS (Singapore), EWM (Malaysia), THD (Thailand), EIDO (Indonesia), EPHE (Philippines)
  - **Americas**: EWZ (Brazil), ARGT (Argentina), ECH (Chile)
  - **EMEA**: TUR (Turkey), EPOL (Poland)
  - **Broad**: EEM, VWO (Emerging Markets)

### Missing
- Romania and Lithuania ETFs (very small frontier markets)

### Formula
```
# Current month return
current_return = roc(period=21)

# 3-month average return
avg_return = sma(period=63)(close) / lag(sma(period=63)(close), 63) - 1

# Or simpler: compare current 1-mo return to 3-mo average
reversal_signal = current_return < avg_return

# Volatility for weighting
vol = std(period=63)

# Inverse volatility weight
weight = 1 / vol
```

## Implementation Notes
- Strategy is marked ELIGIBLE with 13+ EM ETFs available (vs. 15 in original)
- Confidence rating: Moderate (OOS shows poor performance)
- Complexity: Simple
- Missing only Romania and Lithuania (frontier markets)
- All required transforms are available
- Long-only strategy (no hedge capability)
- Poor OOS performance (-0.01 Sharpe) suggests low implementation priority
- Could combine with other factors to improve performance

