# S&P 500 Index Addition Effect

**Quantpedia ID**: #0049
**URL**: https://quantpedia.com/strategies/sp-500-index-addition-effect
**Status**: ELIGIBLE
**Linear Issue**: [ENG-209](https://linear.app/epoch-inc/issue/ENG-209)

## Overview

Event-driven strategy exploiting the price pressure when stocks are added to the S&P 500 index. Index funds must buy these stocks, creating temporary demand that drives up prices.

## Trading Rules

**Universe**: US stocks announced for S&P 500 addition
**Signal**: Announcement of S&P 500 index inclusion
**Selection**: Buy stocks upon announcement, sell after inclusion date
**Holding Period**: ~5 days (announcement to effective date)
**Rebalancing**: Event-driven

## Performance

| Metric | Value |
|--------|-------|
| Period | 1993-2002 |
| Return | 114% (annualized equivalent of event returns) |

## Eligibility Check

### Available
- Stock universe with S&P 500 constituents tracking
- `index_constituents` data for S&P 500 membership changes
- Price and volume data for all US stocks
- Event-driven trading capabilities

### Missing
None - index constituent change data is available.

## Implementation Notes

```
# Monitor index_constituents for additions
sp500_additions = index_constituents_changes(index='SPX', change_type='addition')

# Buy on announcement
long_signal = is_new_addition(asset, sp500_additions)

# Hold until effective date (typically 5 trading days)
exit_signal = days_since_announcement >= 5
```
