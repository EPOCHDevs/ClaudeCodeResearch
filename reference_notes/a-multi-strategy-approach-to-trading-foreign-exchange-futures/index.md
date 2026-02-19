# A Multi Strategy Approach to Trading Foreign Exchange Futures

**Quantpedia ID**: #0436
**URL**: https://quantpedia.com/strategies/a-multi-strategy-approach-to-trading-foreign-exchange-futures
**Status**: INELIGIBLE
**Linear Issue**: [ENG-279](https://linear.app/epoch-inc/issue/ENG-279/feature-request-interest-rate-data-for-fx-carry-trade-0436)

## Overview
This strategy combines multiple FX trading approaches into a single portfolio. It uses Interest Rate Carry, Momentum, Mean Reversion, Equity Momentum, and Commodity Momentum signals, normalizes them, and combines via risk budgeting. The multi-strategy approach aims to improve Sharpe ratio over individual strategies.

## Trading Rules
**Universe**: 8 FX futures (AUD, GBP, CAD, EUR, JPY, MXN, NZD, CHF)

**Signal**: Multi-factor combination
1. Interest Rate Carry indicator
2. Momentum indicator
3. Mean Reversion indicator
4. Equity Momentum indicator (linked to country equities)
5. Commodity Momentum indicator

**Signal Processing**:
1. Normalize each indicator to [-0.5, +0.5] using percentile scoring
2. Apply risk budgeting with 10% annualized target
3. Combine strategies with equal weights

**Weighting**: Risk-budgeted, equal-weight combined
**Rebalancing**: Monthly

## Fundamental Reason
- Carry strategy exploits interest rate differentials
- Momentum captures trends in FX markets
- Mean reversion works for developed currency crosses
- Equity/commodity momentum linked to FX via global capital flows
- Multi-factor combination provides diversification

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1995-2019 |
| Return | 6.58% p.a. |
| Volatility | 13.16% |
| Max Drawdown | -25.74% |
| Sharpe Ratio | 0.50 |

Note: Data from Table 4, Equal weight approach.

**WARNING**: OOS (2009-2025) shows -0.5% return, -0.13 Sharpe, -25.6% max DD. Strategy alpha deteriorated.

## Source Paper
Srivastava, Sonam et al.: A Multi Strategy Approach to Trading Foreign Exchange Futures
- SSRN: https://ssrn.com/abstract=3322717

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238650/

## Eligibility Check
### Available
- **Transforms**:
  - `roc` - Momentum calculation
  - `sma` - Mean reversion signals
  - `std` - Risk budgeting
- **Assets** (all 8 FX pairs available):
  - ^AUDUSD-FX ✓
  - ^GBPUSD-FX ✓
  - ^CADUSD-FX ✓
  - ^EURUSD-FX ✓
  - ^JPYUSD-FX ✓
  - ^MXNUSD-FX ✓
  - ^NZDUSD-FX ✓
  - ^CHFUSD-FX ✓

### Missing
- **Interest Rate Data** - NOT AVAILABLE
  - Short-term interest rates per country
  - Interest rate differentials for carry calculation
  - Central bank policy rates
- **Cross-Asset Linkages** - COMPLEX
  - Country equity index momentum
  - Commodity momentum factors

## Implementation Notes
- Strategy is marked INELIGIBLE due to:
  1. Missing interest rate data for carry calculations (critical)
  2. Complex cross-asset factor requirements
- Confidence rating: Moderate (OOS shows deteriorating alpha)
- Complexity: Very Complex
- All FX pairs are available
- Could potentially implement simplified version with just momentum/mean reversion
- **WARNING**: Negative OOS performance (-0.13 Sharpe) suggests strategy alpha has eroded

