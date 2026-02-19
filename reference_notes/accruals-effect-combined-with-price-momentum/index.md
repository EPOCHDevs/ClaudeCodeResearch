# Accruals Effect Combined with Price Momentum

**Quantpedia ID**: #0400
**URL**: https://quantpedia.com/strategies/accruals-effect-combined-with-price-momentum
**Status**: INELIGIBLE
**Linear Issue**: [ENG-47](https://linear.app/epoch-inc/issue/ENG-47/feature-request-bid-ask-spread-data-for-liquidity-filtering-0400)

## Overview
This strategy combines two well-known anomalies - momentum and accruals effects. Research shows that accruals and cash flows have significant explanatory power for future returns. By conditioning momentum on accruals, investors can achieve higher returns with smaller drawdowns and nearly double the Sharpe ratio compared to simple momentum.

## Trading Rules
**Universe**: All common stocks on NYSE/AMEX, excluding stocks with price < $5
**Signal**: Double sort on 6-month momentum and accruals
**Selection**:
- First filter by low bid-ask spread (liquidity)
- Sort into 5x5 portfolios based on past 6-month returns and accruals
**Weighting**: Equal weighted
**Rebalancing**: Monthly (with 6-month overlapping holding periods)

**Long**: Momentum winners with lowest accruals
**Short**: Momentum losers with highest accruals

## Fundamental Reason
Both momentum and accruals anomalies are well-researched. The combination works because investors fail to appreciate the lower persistence of accruals vs cash flows. This negligence leads to stock mispricing that exacerbates momentum payoffs. The enhanced strategy outperforms across different market states and investor sentiment levels.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1965-2015 |
| Return | 10.43% p.a. |
| Volatility | 10.82% |
| Max Drawdown | -54.47% |
| Sharpe Ratio | 0.59 |

## Source Paper
Xu, Fangming and Zeng, Cheng and Zheng, Liyi: Persistence of Earnings Components and Price Momentum
- SSRN: https://ssrn.com/abstract=3207098

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238459/a746eb67279edf1982e008c2dbea0d35/

## Eligibility Check
### Available
- Transforms: `roc` (momentum), `balance_sheet`, `income_statement`, `cash_flow` (for computing accruals)
- Assets: US Stocks available

### Missing
- **Bid-ask spread data**: Required for liquidity filtering - NOT AVAILABLE
- The strategy specifically requires filtering stocks into low/high bid-ask spread portfolios before the momentum/accruals sort

## Implementation Notes
- Could potentially implement a simplified version without the bid-ask spread filter
- Alternative: Use trading volume or market cap as proxy for liquidity
- Accruals can be computed as: (Change in Non-Cash Current Assets) - (Change in Current Liabilities) - Depreciation
