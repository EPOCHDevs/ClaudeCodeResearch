# Short Interest Effect - Long-Short Version

**Quantpedia ID**: #0045
**URL**: https://quantpedia.com/strategies/short-interest-effect-long-short-version
**Status**: ELIGIBLE
**Linear Issue**: [ENG-172](https://linear.app/epoch-inc/issue/ENG-172)

## Overview

Stocks with high short interest tend to underperform, while stocks with low short interest outperform. The strategy goes long low-short-interest stocks and short high-short-interest stocks.

## Trading Rules

**Universe**: US stocks
**Signal**: Short interest ratio (shares shorted / shares outstanding)
**Selection**: Long lowest decile, short highest decile
**Weighting**: Equal weight
**Rebalancing**: Monthly

## Performance

| Metric | Value |
|--------|-------|
| Period | 1988-2005 |
| Return | 19.7% p.a. |
| Volatility | 17.14% |
| Sharpe Ratio | 0.92 |

## Eligibility Check

### Required Capabilities
- `short_interest` data source - Available
- Cross-sectional ranking - Available

### Missing
None - all required capabilities are available.

## Implementation Notes

```
si = short_interest()
si_ratio = si.short_percent_float  # or calculate shares/float
rank = cs_rank(si_ratio)
long_signal = rank <= percentile_10
short_signal = rank >= percentile_90
```
