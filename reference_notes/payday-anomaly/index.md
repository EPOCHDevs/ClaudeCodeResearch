# Payday Anomaly

**Quantpedia ID**: #0419
**URL**: https://quantpedia.com/strategies/payday-anomaly
**Status**: ELIGIBLE
**Linear Issue**: [ENG-262](https://linear.app/epoch-inc/issue/ENG-262/implement-payday-anomaly-0419)

## Overview
This strategy exploits the mid-month payday effect. The 16th day of the month shows abnormal positive returns, likely due to semi-monthly paycheck distribution and subsequent retirement contribution flows into the market. This is an extension of the well-known turn-of-the-month anomaly.

## Trading Rules
**Universe**: S&P 500 Index (via SPY ETF, futures, or CFDs)

**Signal**: Calendar day = 16
1. Identify the 16th calendar day of each month
2. Buy S&P 500 at market open
3. Sell at market close (same day)

**Selection**: 100% S&P 500 on the 16th, cash otherwise

**Weighting**: 100% equity or 100% cash
**Rebalancing**: Daily

## Fundamental Reason
Many companies pay employees semi-monthly on the 15th and end of month. Retirement contributions from these paychecks reach financial institutions by end of day on the 15th and are invested on the 16th. A significant portion flows into broad-market index funds like S&P 500, creating buying pressure. The 16th is the 3rd best day of the month overall, after the 1st and 2nd.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1980-2010 |
| Return | 2.57% p.a. |
| Volatility | 4.31% |
| Max Drawdown | -12.06% |
| Sharpe Ratio | 0.60 |

Note: Data from Table 4, Panel B. Annualized mean return of 0.214% per occurrence.

## Source Paper
Ma, Aixin and Pratt, William Robert: Payday Anomaly
- SSRN: https://ssrn.com/abstract=3257064

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238560/

## Eligibility Check
### Available
- **Transforms**:
  - `datetime_extract` - Extract day of month from bar timestamps
  - `index()` - Access bar timestamps
  - Calendar-based signal generation
- **Assets**:
  - `SPY-Stocks` - S&P 500 ETF

### Formula
```
day_of_month = datetime_extract(component='day')(index())
signal = day_of_month == 16
Long SPY when signal == true
```

## Implementation Notes
- Strategy is marked ELIGIBLE with all required data available
- Confidence rating: Strong
- Complexity: Simple (single instrument, calendar-based signal)
- Only in market 1 day per month (~12 days/year)
- Low market exposure reduces drawdowns
- Related to Turn-of-Month anomaly
- Effect may weaken as firms transition to bi-weekly pay schedules

