# International Volatility Arbitrage

**Quantpedia ID**: #0402
**URL**: https://quantpedia.com/strategies/international-volatility-arbitrage
**Status**: INELIGIBLE
**Linear Issue**: [ENG-51](https://linear.app/epoch-inc/issue/ENG-51/feature-request-options-data-for-volatility-strategies-0402)

## Overview
An options-based volatility arbitrage strategy that exploits mispricing in international ETF options. The strategy sorts options by ex-ante volatility returns and trades a long-short portfolio based on implied vs realized volatility deviations.

## Trading Rules
**Universe**: 29 International ETF Options (country-level equity ETFs)
**Signal**: Volatility return = 1 - (12M realized volatility / current implied volatility)
**Selection**:
1. Compute implied volatility returns for each option
2. Sort in descending order
3. Assign to tercile portfolios
**Weighting**: Equal weighted within terciles
**Rebalancing**: Monthly (4th Friday)

**Long**: Cheap tercile (low implied vs realized)
**Short**: Expensive tercile (high implied vs realized)
Trade ATM straddles for each position.

## Fundamental Reason
Large volatility deviations exist in international options due to:
- Substantial heterogeneity in contract specifications
- Recent issuance of international ETP products
- Hedge funds focus on domestic options, neglecting international arbitrage
Returns are positively skewed with low volatility and neutral equity exposure.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2006-2015 |
| Return | 16.38% p.a. |
| Volatility | 8.93% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 1.83 |

**Note**: Quantpedia rates confidence as "Weak" - extremely sensitive to bid-ask spread, unable to replicate OOS results due to slippage costs.

## Source Paper
Tosi, Adriano: International Volatility Arbitrage
- SSRN: https://ssrn.com/abstract=3203445

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810798/59feb0f648f0608ccc2d270614c3a794/

## Eligibility Check
### Available
- Transforms: `std` (realized volatility calculation)
- Assets: Some international equity ETFs available

### Missing
- **Options data**: Required for the entire strategy - NOT AVAILABLE
- **Implied volatility**: Core signal component - NOT AVAILABLE
- **ATM straddle pricing**: Execution instrument - NOT AVAILABLE
- **International ETF options chain**: Full options chain data - NOT AVAILABLE

## Implementation Notes
- This is a pure options strategy - cannot be implemented without options data
- Even with options data, Quantpedia notes it's extremely sensitive to slippage/bid-ask
- OOS backtest failed to replicate paper results
- Would require comprehensive international options data source
