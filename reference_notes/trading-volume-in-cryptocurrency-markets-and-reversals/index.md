# Trading Volume in Cryptocurrency Markets and Reversals

**Quantpedia ID**: #0409
**URL**: https://quantpedia.com/strategies/trading-volume-in-cryptocurrency-markets-and-reversals
**Status**: ELIGIBLE
**Linear Issue**: [ENG-166](https://linear.app/epoch-inc/issue/ENG-166/implement-trading-volume-in-cryptocurrency-markets-and-reversals-0409)

## Overview
This strategy exploits the relationship between trading volume and return reversals in cryptocurrency markets. Research shows that low volume periods are followed by price reversals - cryptocurrencies with low prior returns and low volume tend to reverse upward, while those with high prior returns and low volume tend to reverse downward. The strategy implements a double-sort on returns and volume to capture this effect.

## Trading Rules
**Universe**: 26 cryptocurrency pairs (from Table 1 of source paper)
- Major cryptos: BTC, ETH, LTC, BCH, XRP, etc.

**Signal**: Double-sort on prior returns and volume shock
1. Compute prior return: Return from t-1 to t
2. Compute volume shock: log deviation of volume from rolling trend
   - Volume_shock = log(Volume_t) - log(Trend_t)
   - Trend estimated over rolling window

**Selection**:
1. Sort crypto pairs into 3 groups by prior return (low, mid, high)
2. Within each group, sort into 3 sub-groups by volume shock (low, mid, high)
3. 3x3 matrix: 9 portfolios
4. Long: Low return + Low volume portfolio
5. Short: High return + Low volume portfolio

**Weighting**: Equal-weighted
**Rebalancing**: Daily

## Fundamental Reason
Trading volume contains information about investor disagreement and noise trading. When volume is low (few noise traders), price deviations from fundamentals are more likely to correct. Reversals are stronger when volume shocks are negative because:
1. Low volume indicates reduced noise trading activity
2. Prices can deviate further from fundamentals without arbitrage
3. Subsequent correction generates predictable returns

The interaction between past returns and volume predicts future returns better than either alone.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2017-2019 |
| Return | 41.18% p.a. |
| Volatility | 7.84% |
| Max Drawdown | -16.67% |
| Sharpe Ratio | 5.25 |

Note: Data from Table 7, Panel B, 3x3 Sort, CL portfolio, net of 100bps transaction costs, only 10% of portfolio invested.

**WARNING**: Quantpedia rates confidence as "Moderate" - OOS backtest shows slightly negative performance. Strategy alpha may be deteriorating.

## Source Paper
Bianchi, Daniele and Dickerson, Alexander: Trading Volume in Cryptocurrency Markets
- SSRN: https://ssrn.com/abstract=3239670

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238495/

## Eligibility Check
### Available
- **Transforms**:
  - `roc` - Rate of change for prior returns
  - `linreg` - For computing volume trend
  - `dpo` - Detrended Price Oscillator (for detrending approach)
  - `cs_rank` - Cross-sectional ranking for 3x3 sort
  - Volume data via `src.v`
- **Assets**: 50+ crypto pairs available including:
  - `^BTCUSD-Crypto`, `^ETHUSD-Crypto`, `^LTCUSD-Crypto`
  - `^BCHUSD-Crypto`, `^XRPUSD-Crypto`, `^ADAUSD-Crypto`
  - `^DOGEUSD-Crypto`, `^DOTUSD-Crypto`, `^SOLUSD-Crypto`
  - And many more crypto-crypto and crypto-stablecoin pairs

## Implementation Notes
- Strategy is marked ELIGIBLE with all required transforms and assets available
- Confidence rating: Moderate (OOS shows slightly negative performance)
- Complexity: Complex (requires double-sort and volume detrending)
- Daily rebalancing in crypto markets is feasible
- Volume shock calculation: Use `linreg` to estimate trend, then compute log deviation
- Consider 3x3 sort using `cs_rank` with thresholds at 33% and 67%
- High transaction costs in crypto (100bps assumed in paper) - important to model
- Strategy may have suffered alpha decay since publication

