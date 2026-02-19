# Short Interest Effect - Long Only Version

**Quantpedia ID**: #0046
**URL**: https://quantpedia.com/strategies/short-interest-effect-long-only-version
**Status**: ELIGIBLE
**Linear Issue**: [ENG-173](https://linear.app/epoch-inc/issue/ENG-173)

## Overview

Long-only variant of the short interest effect. Goes long stocks with the lowest short interest, avoiding the need to short high-short-interest stocks.

## Trading Rules

**Universe**: US stocks
**Signal**: Short interest ratio
**Selection**: Long lowest quintile by short interest
**Weighting**: Equal weight
**Rebalancing**: Monthly

## Performance

| Metric | Value |
|--------|-------|
| Period | 1988-2005 |
| Return | 26.8% p.a. |
| Max Drawdown | -33.29% |

## Eligibility Check

### Required Capabilities
- `short_interest` data source - Available

### Missing
None - all required capabilities are available.

## Implementation Notes

```
si = short_interest()
rank = cs_rank(si.short_percent_float)
long_signal = rank <= percentile_20  # Bottom quintile
```
