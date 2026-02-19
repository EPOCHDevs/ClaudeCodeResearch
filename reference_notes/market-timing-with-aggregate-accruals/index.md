# Market Timing with Aggregate Accruals

**Quantpedia ID**: #0039
**URL**: https://quantpedia.com/strategies/market-timing-with-aggregate-accruals
**Status**: ELIGIBLE
**Linear Issue**: [ENG-168](https://linear.app/epoch-inc/issue/ENG-168)

## Overview

Market timing strategy using aggregate (market-wide) accruals as a predictor. High aggregate accruals predict poor market returns; low accruals predict strong returns.

## Trading Rules

**Universe**: S&P 500 / broad market
**Signal**: Aggregate market accrual ratio
**Selection**: Long when low accruals, reduce exposure when high
**Rebalancing**: Yearly

## Performance

| Metric | Value |
|--------|-------|
| Period | 1980-2005 |
| Return | 34.0% p.a. |
| Volatility | 37.7% |
| Sharpe Ratio | 0.8 |

## Eligibility Check

### Available
- `cash_flow.net_income`, `cash_flow.cfo` for accrual calculation
- `balance_sheet.total_assets`
- Cross-sectional aggregation (`cs_mean`)

### Missing
None - can aggregate individual stock accruals.

## Implementation Notes

```
# Calculate individual accruals
accrual = (net_income - cfo) / total_assets
# Aggregate across market
agg_accrual = cs_mean(accrual)
# Timing signal
low_accrual = agg_accrual < threshold
long_signal = low_accrual
```
