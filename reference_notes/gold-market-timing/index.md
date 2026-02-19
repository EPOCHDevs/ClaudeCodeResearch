# Gold Market Timing

**Quantpedia ID**: #0043
**URL**: https://quantpedia.com/strategies/gold-market-timing
**Status**: ELIGIBLE
**Linear Issue**: [ENG-170](https://linear.app/epoch-inc/issue/ENG-170)

## Overview

Market timing strategy for gold using various indicators (momentum, trend, macro signals).

## Trading Rules

**Universe**: GLD (Gold ETF)
**Signal**: Momentum or trend-following
**Rebalancing**: Monthly

## Performance

| Metric | Value |
|--------|-------|
| Period | 1968-2005 |
| Return | 31.0% p.a. |
| Volatility | 29.63% |
| Sharpe Ratio | 0.91 |

## Eligibility Check

### Available
- GLD ETF available
- Momentum transforms (`roc`, `sma`)
- Trend indicators

### Missing
None - basic gold timing is implementable.

## Implementation Notes

```
gld_mom = roc(gld.close, 252)  # 12-month momentum
long_signal = gld_mom > 0
# Or SMA crossover:
long_signal = close > sma(close, 200)
```
