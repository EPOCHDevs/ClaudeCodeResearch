# Accrual Anomaly

**Quantpedia ID**: #0038
**URL**: https://quantpedia.com/strategies/accrual-anomaly
**Status**: ELIGIBLE
**Linear Issue**: [ENG-165](https://linear.app/epoch-inc/issue/ENG-165/implement-accrual-anomaly-0038)

## Overview

The Accrual Anomaly exploits the difference between accounting earnings and cash flows. High accruals (earnings exceeding cash flows) tend to predict poor future returns, while low accruals (cash flows exceeding earnings) predict strong returns. The market overweights accruals relative to cash flows.

## Trading Rules

**Universe**: US stocks
**Signal**: Accruals = Net Income - Cash from Operations
**Selection**: Long low accruals (high quality), short high accruals (low quality)
**Weighting**: Equal weight
**Rebalancing**: Yearly

### Detailed Rules
1. Calculate accruals = Net Income - CFO
2. Scale by total assets for comparability
3. Rank stocks by accrual ratio
4. Long stocks in lowest accrual decile (cash-rich earnings)
5. Short stocks in highest accrual decile (accrual-heavy earnings)
6. Rebalance annually

### Signal Calculation
```
Accruals = Net Income - Cash from Operations
Accrual Ratio = Accruals / Total Assets
```

## Fundamental Reason

1. **Earnings Quality**: Cash-based earnings are more persistent than accrual-based
2. **Manipulation**: High accruals may signal earnings management
3. **Mean Reversion**: Accruals tend to reverse (working capital normalizes)
4. **Investor Fixation**: Investors focus on earnings, not cash flow quality

## Performance (Source Paper: Sloan 1996)

| Metric | Value |
|--------|-------|
| Period | 1966-2003 |
| Return | 7.5% p.a. |
| Volatility | 10.26% |
| Sharpe Ratio | 0.34 |
| Max Drawdown | -35.58% |

**Notes**: Effect has weakened post-publication.

## Source Paper

**Sloan: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?"**
- The Accounting Review, 1996

**Abstract**: This paper shows that stock prices act as if investors "fixate" on earnings, failing to fully distinguish between the cash flow and accrual components of current earnings. We show that the persistence of current earnings performance is decreasing in the magnitude of the accrual component of earnings and increasing in the magnitude of the cash flow component.

## Eligibility Check

### Required Capabilities
1. **Net Income**: From income statement or cash flow
2. **Cash from Operations (CFO)**: From cash flow statement
3. **Total Assets**: For scaling
4. **Cross-Sectional Ranking**

### Available
- `cash_flow.net_income` - Net income
- `cash_flow.cfo` - Cash from operating activities
- `balance_sheet.total_assets` - Total assets
- `cs_rank` - Cross-sectional ranking

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **Accrual Calculation**:
   ```
   cf = cash_flow(period='trailing_twelve_months')
   accruals = cf.net_income - cf.cfo
   ```

2. **Scaled Accruals**:
   ```
   bs = balance_sheet(period='quarterly')
   accrual_ratio = accruals / bs.total_assets
   ```

3. **Ranking and Selection**:
   ```
   accrual_rank = cs_rank(accrual_ratio)
   # Low accruals = high quality = long
   long_signal = accrual_rank <= percentile_10
   # High accruals = low quality = short
   short_signal = accrual_rank >= percentile_90
   ```

4. **Rebalancing**: Yearly using `rebalance_interval='yearly'`

### Considerations
- Effect has weakened since discovery (Sloan 1996)
- OOS Sharpe is negative (-0.7%)
- May need to combine with other quality factors
- Consider using rolling accruals rather than point-in-time

## Related Strategies

- Quality/profitability factor strategies
- Cash flow-based strategies
- Earnings manipulation detection

## Related Papers

1. **Sloan (1996)**: "Do Stock Prices Fully Reflect Information in Accruals"
2. **Richardson, Sloan, et al. (2005)**: "Accrual Reliability, Earnings Persistence and Stock Prices"
3. **Dechow, Dichev (2002)**: "The Quality of Accruals and Earnings"
