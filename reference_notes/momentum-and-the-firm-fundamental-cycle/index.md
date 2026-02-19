# Momentum and the Firm Fundamental Cycle

**Quantpedia ID**: #0418
**URL**: https://quantpedia.com/strategies/momentum-and-the-firm-fundamental-cycle
**Status**: INELIGIBLE
**Linear Issue**: [ENG-261](https://linear.app/epoch-inc/issue/ENG-261/feature-request-partial-least-squares-pls-transform-for-0418)

## Overview
This strategy exploits the cyclical behavior of firm fundamentals to generate momentum signals. Rather than using price momentum, it constructs a fundamental momentum index using 13 financial ratios across profitability, leverage, efficiency, and quality dimensions. The strategy uses Partial Least Squares (PLS) to aggregate these ratios and forecast returns.

## Trading Rules
**Universe**: NYSE, AMEX, NASDAQ stocks
- Exclude: REITs, closed-end funds, ADRs, foreign stocks, price < $1

**Signal**: Fundamental PLS Index using 13 ratios:
1. **Profitability**: ROA, ROE, Operating Profit, EBITDA/TA, Cash Flow Margin
2. **Leverage**: Debt Ratio, CF to Debt, LT Debt to Equity, FCF to OCF
3. **Efficiency**: Inventory Turnover, Asset Turnover, Sales to Invested Capital
4. **Quality**: Accruals Ratio

**Process**:
1. Seasonally adjust each ratio (subtract 4-year same-quarter average)
2. Calculate quarter-over-quarter changes
3. Aggregate using PLS method to create index
4. Forecast returns using regression on past 10 quarters
5. Sort stocks into deciles by forecasted returns

**Selection**:
- Long top decile (highest forecasted returns)
- Short bottom decile (lowest forecasted returns)

**Weighting**: Not specified (likely equal or value-weighted)
**Rebalancing**: Quarterly

## Fundamental Reason
Firms experience cycles in fundamentals driven by:
1. Technological breakthroughs that eventually slow due to competition
2. Poor performance corrected by management changes
3. Commodity price cycles affecting related businesses

Investors rationally respond to unanticipated positive/negative shocks, creating momentum during the upward/downward trajectory and reversal when the cycle turns. This is fundamentals-driven momentum rather than behavioral bias.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1970-2015 |
| Return | 8.8% p.a. |
| Volatility | 6.82% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.70 |

Note: Data from Table 10, FPLS10. Doubles Sharpe Ratio vs traditional momentum and avoids crashes.

## Source Paper
Han, Yufeng and Huang, Zhaodan and Tian, Weidong and Zhou, Guofu: Momentum, Reversal, and the Firm Fundamental Cycle
- SSRN: https://ssrn.com/abstract=3282420

## QuantConnect Reference Code
Not available on Quantpedia

## Eligibility Check
### Available
- **Transforms**:
  - `income_statement` - Income statement data
  - `balance_sheet` - Balance sheet data
  - `cash_flow` - Cash flow statement data
  - `fin_ratio` - Financial ratio calculations
  - `roa`, `roe`, `debt_ratio` - Individual ratios
  - `cs_rank` - Cross-sectional ranking
- **Assets**: US Stocks available

### Missing
- **PLS (Partial Least Squares)** - NOT AVAILABLE
  - Central methodology for aggregating 13 ratios
  - Requires statistical implementation
  - Not a standard financial transform
- **Some specific ratios** may need custom computation:
  - Cash Flow Margin
  - Sales to Invested Capital
  - Accruals Ratio

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing PLS transform
- Confidence rating: Strong
- Complexity: Very Complex (requires PLS + regression forecasting)
- Quarterly rebalancing is straightforward
- Superior to price momentum (2x Sharpe, no crashes)
- Would require implementing PLS as custom transform

