# Halloween Effect during Low and High CAPE Months

**Quantpedia ID**: #0411
**URL**: https://quantpedia.com/strategies/halloween-effect-during-low-and-high-cape-months
**Status**: INELIGIBLE
**Linear Issue**: [ENG-178](https://linear.app/epoch-inc/issue/ENG-178/feature-request-shiller-cape-ratio-data-0411)

## Overview
This strategy combines the Halloween effect ("Sell in May and go away") with the Shiller CAPE ratio for market timing. When CAPE is high in September, the Halloween effect is strong (hold stocks only Nov-Apr). When CAPE is low, hold stocks year-round. The CAPE ratio helps determine when the Halloween seasonal pattern is most reliable.

## Trading Rules
**Universe**: US Equity Market (via ETF, index fund, or futures)
- Single instrument: SPY, S&P 500 futures, or equivalent

**Signal**: CAPE ratio relative to 36-month median
1. Check CAPE ratio in September each year
2. Compare to 36-month trailing median of CAPE

**Selection**:
- **High CAPE** (CAPE > median): Apply Halloween effect
  - Hold stocks November through April (winter)
  - Stay in cash May through October (summer)
- **Low CAPE** (CAPE <= median): No Halloween effect
  - Hold stocks year-round (November to October next year)

**Weighting**: 100% equity or 100% cash
**Rebalancing**: Semi-annual (6 months)

## Fundamental Reason
The Halloween effect is mainly due to negative summer returns following high CAPE months. When market valuations are stretched (high CAPE), summer returns become riskier and more negative. The optimism cycle hypothesis suggests investors start each year optimistic but gradually become pessimistic by summer, leading to seasonal return patterns. This pattern is strongest when valuations are already elevated.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1926-2016 |
| Return | 12.24% p.a. |
| Volatility | 17.78% |
| Max Drawdown | -39.4% |
| Sharpe Ratio | 0.46 |

Note: Data from Appendix 1, Panel B, annualized returns of high CAPE winter, summer, and low CAPE months.

**WARNING**: Quantpedia rates confidence as "Weak" - OOS backtest shows significantly negative performance. In-sample results may have been data mined.

## Source Paper
Kim, Keunsoo and Byun, Jinho: Stock Return Predictability and Seasonality
- SSRN: https://ssrn.com/abstract=3180992

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238537/

## Eligibility Check
### Available
- **Transforms**:
  - `sma` / `median` - For computing 36-month median
  - Calendar-based timing (month detection)
- **Assets**:
  - SPY-Stocks (S&P 500 ETF)
  - S&P 500 futures

### Missing
- **Shiller CAPE Ratio data** - NOT AVAILABLE
  - CAPE = Price / (10-year average of real S&P 500 earnings)
  - Requires cyclically adjusted earnings data not typically available in standard feeds
  - Would need external data source (Shiller's dataset, Quandl, FRED)
- S&P 500 aggregate earnings data (for computing CAPE)

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing CAPE ratio data
- Confidence rating: Weak (OOS shows significantly negative performance)
- Even if CAPE data were available, Quantpedia's OOS backtest is negative
- NOT RECOMMENDED for implementation even if data becomes available
- Complexity: Simple (only 1 instrument, 6-month rebalancing)
- Alternative: Could potentially source CAPE from external feed or compute from fundamentals

