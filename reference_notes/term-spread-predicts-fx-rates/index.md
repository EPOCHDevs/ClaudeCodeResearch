# Term Spread Predicts FX Rates

**Quantpedia ID**: #0048
**URL**: https://quantpedia.com/strategies/term-spread-predicts-fx-rates
**Status**: ELIGIBLE
**Linear Issue**: [ENG-175](https://linear.app/epoch-inc/issue/ENG-175)

## Overview

FX strategy using term spread (10Y-2Y yield) as predictor. Countries with steeper yield curves tend to have strengthening currencies.

## Trading Rules

**Universe**: G10 FX pairs
**Signal**: Term spread (10Y - 2Y yield)
**Selection**: Long currencies with steep curves, short flat/inverted
**Rebalancing**: Monthly

## Performance

| Metric | Value |
|--------|-------|
| Period | 1975-2009 |
| Return | 6.66% p.a. |
| Volatility | 3.94% |
| Sharpe Ratio | 0.68 |

## Eligibility Check

### Available
- `fx_pairs` - FX currency pairs
- `economic_indicators` - Spread10Y2Y available
- Treasury yields for manual calculation

### Missing
None.

## Implementation Notes

```
spread = economic_indicators(category='Spread10Y2Y')
# Compare US spread to foreign spreads
# Long USD when US spread higher
```
