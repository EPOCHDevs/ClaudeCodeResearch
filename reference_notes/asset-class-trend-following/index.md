# Asset Class Trend-Following

**Quantpedia ID**: #0001
**URL**: https://quantpedia.com/strategies/asset-class-trend-following
**Status**: ELIGIBLE
**Linear Issue**: [ENG-11](https://linear.app/epoch-inc/issue/ENG-11/implement-asset-class-trend-following-0001)

## Overview
Asset class trend-following exploits momentum anomalies through market timing across multiple asset classes. The approach identifies periods when asset classes are more likely to outperform by using moving average filters, allowing investors to gain exposure during favorable conditions while maintaining cash during unfavorable periods. This tactical overlay aims to deliver equity-like returns with bond-like volatility and drawdowns.

## Trading Rules
**Universe**: 5 ETFs - SPY (US stocks), EFA (foreign stocks), BND (bonds), VNQ (REITs), GSG (commodities)
**Signal**: Hold each asset only when trading above its 10-month simple moving average; otherwise maintain cash position
**Selection**: All assets meeting signal criteria
**Weighting**: Equal weight (20% each when held)
**Rebalancing**: Monthly

## Fundamental Reason
The strategy works by identifying market regimes with lower performance and higher volatility. During these periods, the moving average filter signals exit to cash. Conversely, when momentum is positive, allocations remain invested. This regime-dependent approach captures diversification benefits from low correlation between assets while avoiding significant bear market drawdowns.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1973-2008 |
| Return | 11.27% p.a. |
| Volatility | 6.87% |
| Max Drawdown | -29.43% |
| Sharpe Ratio | 1.06 |

## Out-of-Sample Performance (Quantpedia)
| Metric | Value |
|--------|-------|
| Period | 2000-2025 |
| Return | 6.2% p.a. |
| Volatility | 12.42% |
| Max Drawdown | -29.43% |
| Sharpe Ratio | 0.50 |

## Source Paper
**A Quantitative Approach to Tactical Asset Allocation**
- Author: Mebane Faber
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
- Abstract: Updated 2006 white paper with 2008-2012 data examining whether a "simple quantitative method improves risk-adjusted returns across various asset classes." Results confirmed the strategy achieved equity-like returns with bond-like volatility and drawdowns in real-time.

## QuantConnect Reference Code
Strategy has QuantConnect code available on Quantpedia (subscription: Free).

## Eligibility Check
### Available
**Transforms:**
- `ma` (Moving Average) - supports `sma` type with configurable period (1-500)
  - Usage: `ma(close, period=10, type=sma)` for 10-month SMA

**Assets:**
- SPY-Stocks (US Equities)
- EFA-Stocks (Foreign Developed Equities)
- BND-Stocks (US Aggregate Bonds)
- VNQ-Stocks (REITs)
- GSG-Stocks (Commodities)

### Missing
None - all required components available.

## Implementation Notes
1. **Timeframe**: Use monthly bars for 10-period SMA calculation
2. **Signal Logic**: `close > ma(close, 10, sma)` = hold asset; otherwise cash
3. **Position Management**: Equal weight allocation across qualifying assets
4. **Cash Handling**: When asset below MA, allocate that portion to cash (or short-term bonds)
5. **Rebalance Trigger**: Monthly at month-end

## Related Strategies
- Dual Momentum (Gary Antonacci)
- GTAA (Global Tactical Asset Allocation)
- Ivy Portfolio variants
