# Investment-Momentum Strategy

**Quantpedia ID**: #0432
**URL**: https://quantpedia.com/strategies/investment-momentum-strategy
**Status**: INELIGIBLE
**Linear Issue**: [ENG-275](https://linear.app/epoch-inc/issue/ENG-275/feature-request-lag-function-and-bid-ask-spread-data-for-0432)

## Overview
This strategy combines price momentum with corporate investment levels. It exploits two dimensions of market inefficiency: momentum (price continuation) and investment anomaly (overinvesting firms are overpriced). By buying winners with low investment and selling losers with high investment, the strategy generates stronger and more persistent returns than either factor alone.

## Trading Rules
**Universe**: NYSE/AMEX common stocks, price > $5, lowest third by bid-ask spread (~1000 stocks)

**Signal**: Double-sort on Momentum + Investment-to-Assets (I/A)
1. Filter to lowest bid-ask spread tercile (liquidity filter)
2. Calculate 6-month momentum (month -5 to 0)
3. Calculate I/A ratio:
   - I/A = (ΔPP&E + ΔInventories) / Lagged Total Assets
   - Where Δ = annual change
4. Independent quintile sort on momentum (5 groups)
5. Independent quintile sort on I/A (5 groups)
6. Creates 5×5 = 25 portfolios

**Selection**:
- Long: Winners (high momentum) with low investment
- Short: Losers (low momentum) with high investment

**Weighting**: Equally-weighted
**Rebalancing**: Every 6 months (skip 1 month: hold month 2 to 7)

## Fundamental Reason
- Momentum driven by behavioral biases (herding, under/overreaction, confirmation bias)
- Investment anomaly: aggressive investments don't improve near-term returns
- Two-dimensional inefficiency exploitation is stronger and more persistent
- Strategy maintains performance even when individual factors show weakness
- Works in universe of low bid-ask spread stocks (liquid)

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1965-2015 |
| Return | 8.99% p.a. |
| Volatility | 11.66% |
| Max Drawdown | -77.57% |
| Sharpe Ratio | 0.77 |

Note: Data from Table 5, Panel A low, annualized monthly return (0.72%).

**OOS (2000-2025)**: 6.6% return, 0.25 Sharpe, -60.4% max DD. Positive but reduced alpha.

## Source Paper
Xu, Fangming and Zhao, Huainan and Zheng, Liyi: Investment-Momentum: A Two-Dimensional Behavioral Strategy
- SSRN: https://ssrn.com/abstract=3346289

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238633/

## Eligibility Check
### Available
- **Transforms**:
  - `roc(period=126)` - 6-month momentum
  - `cs_quantile` - Cross-sectional quintile sorting
- **Fundamental Data** (via balance_sheet):
  - `ppe_net` - Property, Plant & Equipment (Net)
  - `inventories` - Inventories
  - `total_assets` - Total Assets
- **Assets**: US Stocks available

### Missing
- **Year-over-Year Change Calculation** - COMPLEX
  - I/A requires: (ΔPP&E + ΔInventories) / Lagged Assets
  - Need lag/shift function for annual changes (~252 days)
  - No direct `lag()` or `shift()` transform found
- **Bid-Ask Spread Data** - NOT AVAILABLE
  - Strategy filters to lowest third by bid-ask spread
  - Required for liquidity filtering
  - We don't have microstructure/quote data

## Implementation Notes
- Strategy is marked INELIGIBLE due to:
  1. Missing lag function for computing annual changes in fundamentals
  2. Missing bid-ask spread data for liquidity filtering
- Confidence rating: Strong
- Complexity: Complex
- Positive OOS (0.25 Sharpe) suggests potential value if implementable
- Could approximate with:
  - Skip bid-ask filter (use market cap as liquidity proxy)
  - Use `roc` on fundamentals if supported, or compute changes differently
- Deep max drawdown (-77% IS, -60% OOS) requires careful position sizing

