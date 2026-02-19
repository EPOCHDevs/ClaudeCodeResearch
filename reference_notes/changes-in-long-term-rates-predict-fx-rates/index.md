# Changes in Long Term Rates Predict FX Rates

**Quantpedia ID**: #0047
**URL**: https://quantpedia.com/strategies/changes-in-long-term-rates-predict-fx-rates
**Status**: ELIGIBLE
**Linear Issue**: [ENG-174](https://linear.app/epoch-inc/issue/ENG-174)

## Overview

FX strategy based on changes in long-term interest rates. Currencies of countries with rising long-term rates tend to appreciate.

## Trading Rules

**Universe**: G10 FX pairs
**Signal**: Change in 10-year government bond yield
**Selection**: Long currencies with rising rates, short those with falling rates
**Rebalancing**: Monthly

## Performance

| Metric | Value |
|--------|-------|
| Period | 1975-2009 |
| Return | 5.92% p.a. |
| Volatility | 3.67% |
| Sharpe Ratio | 0.52 |

## Eligibility Check

### Available
- `fx_pairs` - FX currency pairs
- `economic_indicators` - Treasury yields (Treasury10Y, etc.)
- Rate of change transforms

### Missing
None - can implement with available FX and rate data.

## Implementation Notes

```
us_10y = economic_indicators(series='Treasury10Y')
rate_change = roc(us_10y, 21)  # Monthly change
# Similar for other countries
# Long USD if US rate rising faster than foreign
```
