# Computing Power Factor in Cryptocurrencies

**Quantpedia ID**: #0433
**URL**: https://quantpedia.com/strategies/computing-power-factor-in-cryptocurrencies
**Status**: INELIGIBLE
**Linear Issue**: [ENG-276](https://linear.app/epoch-inc/issue/ENG-276/feature-request-blockchain-mining-data-and-dash-crypto-for-0433)

## Overview
This strategy uses a computing power factor derived from blockchain mining data to predict cryptocurrency returns. Computing power (hash rate × blocks mined) serves as a proxy for miner activity and network security, providing fundamental valuation signals in crypto markets.

## Trading Rules
**Universe**: 5 cryptocurrencies (Bitcoin, Ethereum, Litecoin, Monero, Dash)

**Signal**: Computing Power Factor
1. Collect daily mining difficulty and blocks mined for each crypto
2. Calculate computing power = difficulty × blocks mined
3. Run OLS regression: Crypto returns vs computing power factor
4. Create factor-mimicking portfolio using regression weights
5. Go long/short based on factor loading

**Selection**:
- Long cryptos with positive factor loading
- Short cryptos with negative factor loading

**Weighting**: OLS regression-based weights
**Rebalancing**: Weekly

## Fundamental Reason
- Mining difficulty reflects network security and miner commitment
- Computing power is a fundamental metric for blockchain valuation
- Miners invest real resources (electricity, hardware) based on expected returns
- High computing power indicates strong network fundamentals
- Factor captures cross-sectional differences in blockchain health

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2015-2019 |
| Return | 35.56% p.a. |
| Volatility | 24.74% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 1.44 |

Note: Data from paper, in-sample period.

**OOS (2015-2025)**: 16.1% return, 0.57 Sharpe. Positive alpha retained but reduced.

## Source Paper
Liu, Yukun and Tsyvinski, Aleh: Risks and Returns of Cryptocurrency
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3226952

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810906/

## Eligibility Check
### Available
- **Assets** (4 of 5 cryptos):
  - ^BTCUSD-Crypto (Bitcoin) ✓
  - ^ETHUSD-Crypto (Ethereum) ✓
  - ^LTCUSD-Crypto (Litecoin) ✓
  - ^XMRUSD-Crypto (Monero) ✓

### Missing
- **Dash Cryptocurrency** - NOT AVAILABLE
  - DASH-Stocks exists but is DoorDash stock
  - No DASH-Crypto trading pair
- **Blockchain Mining Data** - NOT AVAILABLE
  - Mining difficulty data
  - Hash rate data
  - Blocks mined count
  - Computing power metric
  - No on-chain/blockchain fundamental data

## Implementation Notes
- Strategy is marked INELIGIBLE due to:
  1. Missing Dash cryptocurrency (only 4 of 5 cryptos available)
  2. Missing blockchain/mining fundamental data (critical)
- Confidence rating: Strong
- Complexity: Complex (OLS regression, factor-mimicking portfolio)
- Positive OOS (0.57 Sharpe) suggests potential value if implementable
- Would require external data provider for blockchain fundamentals
- Could potentially simplify with available cryptos only

