# Short Term Trend Following with Small Volatile Stocks

**Quantpedia ID**: #0060
**URL**: https://quantpedia.com/strategies/short-term-trend-following-with-small-volatile-stocks
**Status**: ELIGIBLE
**Linear Issue**: [ENG-210](https://linear.app/epoch-inc/issue/ENG-210)

## Overview

Short-term momentum strategy focusing on small-cap, high-volatility stocks that exhibit strong trend-following behavior over intraday or very short holding periods.

## Trading Rules

**Universe**: Small-cap US stocks with high volatility
**Signal**: Short-term price momentum (intraday or 1-day)
**Selection**: Buy stocks with strong upward momentum, filter by market cap and volatility
**Holding Period**: Intraday to few days
**Rebalancing**: Daily

## Performance

| Metric | Value |
|--------|-------|
| Period | 2004-2009 |
| Return | 23.0% p.a. |

## Eligibility Check

### Available
- `finance_ratio(ratio_type='market_cap')` for small-cap filtering
- `stdev` for volatility calculation
- `roc` for short-term momentum
- Cross-sectional ranking with `cs_rank`
- Daily OHLCV data

### Missing
None - can implement with available data using daily frequency.

## Implementation Notes

```
# Filter small caps (bottom quartile by market cap)
mkt_cap = finance_ratio(ratio_type='market_cap')
small_cap = cs_rank(mkt_cap) <= 0.25

# High volatility filter
volatility = stdev(close, 21)
high_vol = cs_rank(volatility) >= 0.75

# Short-term momentum signal
momentum = roc(close, 1)  # 1-day return
long_signal = small_cap & high_vol & (momentum > 0)
```
