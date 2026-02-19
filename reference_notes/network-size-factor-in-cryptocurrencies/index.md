# Network Size Factor in Cryptocurrencies

**Quantpedia ID**: #0434
**URL**: https://quantpedia.com/strategies/network-size-factor-in-cryptocurrencies
**Status**: INELIGIBLE
**Linear Issue**: [ENG-277](https://linear.app/epoch-inc/issue/ENG-277/feature-request-blockchain-network-data-and-dash-crypto-for-0434)

## Overview
This strategy uses a network size factor derived from blockchain adoption metrics. Network size (unique active addresses transacting on blockchain) serves as a proxy for cryptocurrency adoption and liquidity. Large networks indicate greater adoption, and prices cointegrate with network size in the long run.

## Trading Rules
**Universe**: 4 cryptocurrencies (Bitcoin, Ethereum, Litecoin, Dash)

**Signal**: Network Size Factor
1. Obtain daily network values (unique active addresses)
2. Calculate natural log, average over 7-day periods (ending Friday)
3. Calculate first difference to get network growth
4. Run OLS regression: Network growth vs cryptocurrency returns
5. Create factor-mimicking portfolio using regression coefficients
6. Weight by ranked relative market cap

**Selection**:
- Long/short based on factor loading

**Weighting**: OLS regression-based weights, scaled by market cap rank
**Rebalancing**: Weekly

## Fundamental Reason
- Network size is a fundamental factor for cryptocurrency valuation
- Large network indicates greater adoption and liquidity
- Price and network cointegrate (don't drift too far apart)
- Pro-cyclical asset pricing factor with positive risk premia
- Network factor adds value beyond Bitcoin return and momentum factors

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2015-2019 |
| Return | 15.6% p.a. |
| Volatility | 10.82% |
| Max Drawdown | -18.16% |
| Sharpe Ratio | 1.44 |

Note: Data from Table 4, FmpNET, only 10% of portfolio invested.

**OOS (2015-2025)**: 5.3% return, 0.67 Sharpe. Positive alpha retained.

## Source Paper
Bhambhwani, Siddharth and Delikouras, Stefanos and Korniotis, George M.: Do Fundamentals Drive Cryptocurrency Prices?
- SSRN: https://ssrn.com/abstract=3342842

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238642/

## Eligibility Check
### Available
- **Assets** (3 of 4 cryptos):
  - ^BTCUSD-Crypto (Bitcoin) ✓
  - ^ETHUSD-Crypto (Ethereum) ✓
  - ^LTCUSD-Crypto (Litecoin) ✓

### Missing
- **Dash Cryptocurrency** - NOT AVAILABLE
  - DASH-Stocks exists but is DoorDash stock
  - No DASH-Crypto trading pair
- **Blockchain Network Data** - NOT AVAILABLE
  - Active unique addresses (network size)
  - Network growth metrics
  - No on-chain/blockchain adoption data

## Implementation Notes
- Strategy is marked INELIGIBLE due to:
  1. Missing Dash cryptocurrency (3 of 4 available)
  2. Missing blockchain network data (critical)
- Confidence rating: Strong
- Complexity: Complex (OLS regression, factor-mimicking portfolio)
- Good OOS (0.67 Sharpe) suggests value if implementable
- Same blockers as #0433 (Computing Power Factor)
- Would require external blockchain data provider

