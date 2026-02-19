# The Value Uncertainty Premium

**Quantpedia ID**: #0422
**URL**: https://quantpedia.com/strategies/the-value-uncertainty-premium
**Status**: INELIGIBLE
**Linear Issue**: [ENG-265](https://linear.app/epoch-inc/issue/ENG-265/feature-request-analyst-forward-earnings-estimates-ibes-style-for-0422)

## Overview
This strategy exploits the value uncertainty premium by trading on the time-series volatility of expected book-to-market (BM) ratios. Stocks with high UNC (high standard deviation of expected BM) earn a premium above standard risk factors, while low UNC stocks underperform. The premium is driven by exposure to productivity and consumption risks.

## Trading Rules
**Universe**: 500 largest NYSE stocks

**Signal**: Value Uncertainty (UNC)
1. Calculate expected book value at end of year:
   - Expected BV = Last book value + Estimated net income - Expected dividends
2. Compute expected BM ratio daily:
   - Expected BM = Expected BV / Market Cap
3. Calculate UNC over previous 12 months:
   - UNC = StdDev(Expected BM) / Mean(Expected BM)
4. Sort stocks into deciles by UNC

**Selection**:
- Long top decile (highest UNC)
- Short bottom decile (lowest UNC)

**Weighting**: Value-weighted
**Rebalancing**: Monthly

## Fundamental Reason
High-UNC stocks are connected with productivity and consumption risks:
1. If firm productivity covaries positively with consumption growth, high-UNC leads to high systematic risk exposure
2. Risk-averse investors demand higher expected returns for holding high-UNC stocks
3. High-UNC may be partly driven by lower information quality and higher uncertainty in future profitability
4. Alpha is driven by outperformance of high-UNC stocks (not underperformance of low-UNC)

The premium is robust to various scrutiny levels and is not driven by small/illiquid stocks.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1986-2016 |
| Return | 12.01% p.a. |
| Volatility | 14.62% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.55 |

Note: Data from Table A.4, Panel B (Largest 500 stocks). Alpha of 6-8% annually.

## Source Paper
Bali, Turan G. and Del Viva, Luca and El Hefnawy, Menna and Trigeorgis, Lenos: The Value Uncertainty Premium
- SSRN: https://ssrn.com/abstract=3299582

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/21685697/

## Eligibility Check
### Available
- **Transforms**:
  - `balance_sheet` - Book value (total_equity)
  - `dividends` - Historical dividend data
  - `market_cap` - Market capitalization
  - `std` - Standard deviation calculation
  - `cs_rank` - Cross-sectional ranking for decile sorting
- **Assets**: US Stocks available (NYSE)

### Missing
- **Analyst Forward Earnings Estimates** - NOT AVAILABLE
  - Daily analyst consensus estimates for net income
  - Required to compute "expected book value at end of year"
  - Typically sourced from IBES or similar services
  - We only have `estimated_eps` at earnings announcement time (not daily forward estimates)
- **Expected Dividends** - PARTIAL
  - Historical dividends available but not forward expectations
  - Need analyst dividend forecasts

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing analyst forward estimates
- Confidence rating: Strong
- Complexity: Complex
- Key missing data: IBES-style daily analyst estimates for net income
- Formula: UNC = StdDev(Expected BM) / Mean(Expected BM) over 12 months
- Works as hedge during bear markets (positive performance in bad economic states)
- Robust performance with highest 500 NYSE stocks (not small-cap driven)

