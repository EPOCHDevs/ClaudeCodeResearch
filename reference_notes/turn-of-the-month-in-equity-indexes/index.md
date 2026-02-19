# Turn of the Month in Equity Indexes

**Quantpedia ID**: #0041
**URL**: https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes
**Status**: ELIGIBLE
**Linear Issue**: [ENG-169](https://linear.app/epoch-inc/issue/ENG-169)

## Overview

The Turn of Month (TOM) effect exploits the tendency for equity indexes to perform better during the last few days of each month and the first few days of the next month. This pattern is driven by institutional flows (pension fund contributions, mutual fund window dressing) and creates a reliable seasonal pattern.

## Trading Rules

**Universe**: S&P 500 (SPY)
**Signal**: Calendar - last N days + first M days of month
**Selection**: Long during TOM window, flat otherwise
**Weighting**: All-in or cash
**Rebalancing**: Daily

### Detailed Rules
1. Go long on trading day -1 before month end (or day -2 to -4)
2. Hold through first 3-4 trading days of new month
3. Exit to cash for remainder of month
4. Repeat monthly

### TOM Window
- Typical: Day -1 to Day +3 (5 trading days)
- Extended: Day -4 to Day +4 (9 trading days)

## Fundamental Reason

1. **Pension Flows**: Monthly contributions invested at month turn
2. **Window Dressing**: Fund managers adjust portfolios at month end
3. **Payroll Timing**: 401k contributions occur at month end
4. **Liquidity**: Institutional buying creates upward pressure

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1926-2005 |
| Return | 7.2% p.a. |
| Volatility | 6.9% |
| Sharpe Ratio | 1.04 |
| Max Drawdown | -20.79% |

## Eligibility Check

### Required Capabilities
- `turn_of_month` transform - Available
- SPY/equity index data - Available

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **TOM Signal**:
   ```
   tom = turn_of_month(days_before=1, days_after=3)
   long_signal = tom.is_active
   ```

2. **Position**:
   ```
   weight = conditional_select(long_signal, 1.0, 0.0)
   ```

## Related Strategies

- #0031 Market Seasonality Effect
- Holiday effect strategies
