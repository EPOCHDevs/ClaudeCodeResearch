# Cash-Based Operating Profitability

**Quantpedia ID**: #0406
**URL**: https://quantpedia.com/strategies/cash-based-operating-profitability
**Status**: ELIGIBLE
**Linear Issue**: [ENG-150](https://linear.app/epoch-inc/issue/ENG-150/implement-cash-based-operating-profitability-0406)

## Overview
This strategy combines the accruals anomaly with profitability factor research. Cash-based operating profitability (operating profitability minus accruals) better predicts future stock returns than measures that include accruals. The strategy goes long stocks with high cash-based profitability and shorts those with low values.

## Trading Rules
**Universe**: All stocks on NYSE, AMEX, NASDAQ (common shares only)

**Signal**: Cash-Based Operating Profitability (CBOP)
1. Filter to big stocks (above median NYSE market cap)
2. Calculate Operating Profitability = Revenue - COGS - SG&A
3. Remove accrual components to get Cash-Based Operating Profitability
4. CBOP = Operating Profitability - Accruals

**Selection**:
1. Sort stocks by CBOP
2. Long top decile (highest CBOP)
3. Short bottom decile (lowest CBOP)

**Weighting**: Value-weighted (by market cap)
**Rebalancing**: Yearly (December)

## Fundamental Reason
Cash-based operating profitability contains information about payment shocks and growth beyond just profitability. Unlike measures that include accruals, CBOP is devoid of accounting adjustments that can distort true economic performance. The accrual component is negatively correlated with future returns, so removing it creates a stronger predictor. The predictive power persists up to 10 years, suggesting either gradual correction of market underreaction to cash flow information or shared risk determinants.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1963-2014 |
| Return | 5% p.a. |
| Volatility | 11% |
| Max Drawdown | -51.7% |
| Sharpe Ratio | 0.45 |

Note: Data from Table 4, Panel B, Big stocks, Excess return

## Source Paper
Ball, Ray and Gerakos, Joseph J. and Linnainmaa, Juhani T. and Nikolaev, Valeri V.: Accruals, Cash Flows, and Operating Profitability in the Cross Section of Stock Returns
- SSRN: https://ssrn.com/abstract=2587199

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238490/06d02771e7c0138c3799a09a18c50491/

## Eligibility Check
### Available
- **Transforms**:
  - `income_statement` - Revenue, COGS, SG&A, Operating Income
  - `balance_sheet` - Total Assets, Current Assets/Liabilities for accruals
  - `cash_flow` - Operating cash flows
  - `cs_rank` - Cross-sectional ranking for decile sorting
- **Assets**: US Stocks available

### Formula
```
Operating Profitability = Revenue - COGS - SG&A
Accruals = (Change in Current Assets - Change in Cash) - (Change in Current Liabilities - Change in Short-term Debt) - Depreciation
CBOP = Operating Profitability - Accruals
```

## Implementation Notes
- Strategy is marked ELIGIBLE with all required fundamental data available
- Confidence rating: Strong
- Complexity: Complex (requires multiple fundamental data fields)
- Yearly rebalancing minimizes transaction costs
- Use income_statement transform for Revenue, COGS, SG&A
- Use balance_sheet transform for market cap filtering and accrual calculation
- QC implementation uses top 3000 stocks by market cap instead of all stocks
