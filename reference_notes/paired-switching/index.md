# Paired Switching

**Quantpedia ID**: #0044
**URL**: https://quantpedia.com/strategies/paired-switching
**Status**: ELIGIBLE
**Linear Issue**: [ENG-171](https://linear.app/epoch-inc/issue/ENG-171)

## Overview

Simple momentum-based asset rotation between two asset classes (typically stocks and bonds). Holds the asset with better recent returns.

## Trading Rules

**Universe**: SPY (stocks) + TLT/AGG (bonds)
**Signal**: 3-month momentum comparison
**Selection**: Long the asset with higher past return
**Rebalancing**: Quarterly

## Performance

| Metric | Value |
|--------|-------|
| Period | 1991-2011 |
| Return | 11.3% p.a. |
| Volatility | 9.3% |
| Sharpe Ratio | 0.78 |

## Eligibility Check

### Available
- `roc` for momentum calculation
- SPY, TLT, AGG ETFs available
- Conditional selection transforms

### Missing
None.

## Implementation Notes

```
spy_mom = roc(spy.close, 63)  # 3-month
tlt_mom = roc(tlt.close, 63)
long_spy = spy_mom > tlt_mom
long_tlt = tlt_mom > spy_mom
```
