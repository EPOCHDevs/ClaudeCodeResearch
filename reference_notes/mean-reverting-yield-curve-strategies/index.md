# Mean-Reverting Yield Curve Strategies

**Quantpedia ID**: #0084
**URL**: https://quantpedia.com/strategies/mean-reverting-yield-curve-strategies
**Status**: ELIGIBLE
**Linear Issue**: [ENG-233](https://linear.app/epoch-inc/issue/ENG-233)

## Overview

Yield curve mean reversion strategy that trades deviations from typical yield curve shapes. When the yield curve becomes unusually steep or flat compared to historical norms, the strategy positions for reversion to mean.

## Trading Rules

**Universe**: Treasury bond ETFs (TLT, IEF, SHY) or bond futures
**Signal**: Z-score of yield curve slope/curvature vs historical mean
**Selection**:
- Long duration when curve is unusually steep
- Short duration when curve is unusually flat
**Rebalancing**: Monthly

## Performance

| Metric | Value |
|--------|-------|
| Period | 1973-2004 |
| Return | 3.73% p.a. |

## Eligibility Check

### Available
- `economic_indicators` - Full Treasury yield curve (Treasury1M through Treasury30Y)
- `economic_indicators` - Yield spreads (Spread10Y2Y, Spread10Y3M)
- `zscore` - Time-series z-score for mean reversion signals
- Bond ETFs: TLT (20Y+), IEF (7-10Y), SHY (1-3Y), IEI (3-7Y), TLH (10-20Y)

### Missing
None - all required data sources available.

## Implementation Notes

```
# Get yield curve data
spread_10y2y = economic_indicators(category='Spread10Y2Y')
treasury_10y = economic_indicators(category='Treasury10Y')
treasury_2y = economic_indicators(category='Treasury2Y')

# Calculate z-score of curve steepness
curve_zscore = zscore(spread_10y2y, 252)  # 1-year lookback

# Trade mean reversion
long_duration = curve_zscore > 2   # Unusually steep curve
short_duration = curve_zscore < -2  # Unusually flat/inverted curve
```
