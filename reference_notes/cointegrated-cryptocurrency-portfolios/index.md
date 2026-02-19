# Cointegrated Cryptocurrency Portfolios

**Quantpedia ID**: #0408
**URL**: https://quantpedia.com/strategies/cointegrated-cryptocurrency-portfolios
**Status**: ELIGIBLE
**Linear Issue**: [ENG-163](https://linear.app/epoch-inc/issue/ENG-163/implement-cointegrated-cryptocurrency-portfolios-0408)

## Overview
This strategy applies pairs trading methodology to cryptocurrencies using cointegration analysis. It identifies cointegrated cryptocurrency pairs/portfolios and trades mean-reversion of the spread. The strategy constructs a stationary spread from multiple cryptocurrencies and trades deviations from the mean.

## Trading Rules
**Universe**: 4 major cryptocurrencies
- Bitcoin (BTC)
- Ethereum (ETH)
- Litecoin (LTC)
- Bitcoin Cash (BCH)

**Signal**: Cointegration-based spread using Engle-Granger approach
1. Test for cointegration among cryptocurrencies using Engle-Granger method
2. Construct spread: Spread = BTC + β₁*ETH + β₂*LTC + β₃*BCH
3. Compute z-score of spread: z = (spread - mean) / std

**Selection**:
1. Long spread when z-score < -c (spread below mean - c*std)
2. Short spread when z-score > +c (spread above mean + c*std)
3. Exit when z-score crosses zero

**Weighting**: Based on cointegration hedge ratios (betas)
**Rebalancing**: Daily

## Fundamental Reason
Cryptocurrencies share common factors driving their prices (market sentiment, regulatory news, adoption trends). When prices temporarily diverge from their equilibrium relationship, they tend to revert. Cointegration captures this long-run equilibrium, and the spread constructed from cointegrated assets is mean-reverting by definition.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2017-2018 |
| Return | 42.68% p.a. |
| Volatility | Not stated |
| Max Drawdown | -27.3% |
| Sharpe Ratio | Not stated |

**WARNING**: Quantpedia rates confidence as "Moderate" - OOS backtest shows slightly negative performance. Short backtest period and high volatility environment.

## Source Paper
Fil, Mats and Kristoufek, Ladislav: Pairs Trading in Cryptocurrency Markets
- SSRN: https://ssrn.com/abstract=3221148

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238498/

## Eligibility Check
### Available
- **Transforms**:
  - `engle_granger` - Two-step Engle-Granger cointegration test
  - `johansen` - Multivariate Johansen cointegration for 2-10 series
  - `half_life` - Mean-reversion half-life estimation
  - `linreg` - Rolling OLS regression
  - `z_score` / `cs_zscore` - Z-score calculation
  - `stddev` - Standard deviation
- **Assets**: All 4 cryptocurrencies available
  - `^BTCUSD-Crypto` (BTC-USD)
  - `^ETHUSD-Crypto` (ETH-USD)
  - `^LTCUSD-Crypto` (LTC-USD)
  - `^BCHUSD-Crypto` (BCH-USD)

## Implementation Notes
- Strategy is marked ELIGIBLE with all required transforms and assets available
- Confidence rating: Moderate (short backtest period, OOS shows slightly negative)
- Complexity: Complex (requires cointegration testing and spread construction)
- Use `johansen` for multivariate cointegration (better than pairwise Engle-Granger for 4 assets)
- `half_life` transform helps determine optimal holding period
- Consider using longer lookback windows (100+ bars) for stable cointegration estimates
- High transaction costs in crypto markets may erode profits
- Slippage significant during high volatility periods

