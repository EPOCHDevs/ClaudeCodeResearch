# Analyst Days

**Quantpedia ID**: #0417
**URL**: https://quantpedia.com/strategies/analyst-days
**Status**: INELIGIBLE
**Linear Issue**: [ENG-241](https://linear.app/epoch-inc/issue/ENG-241/feature-request-analyst-day-event-data-for-0417)

## Overview
This strategy exploits the market underreaction to analyst day events. An analyst day is a firm-hosted gathering where equity analysts and institutional investors receive information about corporate strategy, financial performance, and product development. Firms holding these events typically disclose positive information, leading to significant post-event abnormal returns.

## Trading Rules
**Universe**: NYSE, AMEX, NASDAQ stocks

**Signal**: Analyst day events
1. Identify analyst days from 8-K filings in SEC's EDGAR system or press releases
2. Must be publicly disclosed per Regulation Fair Disclosure

**Selection**:
1. Buy stock on the analyst day event date
2. Hold for 20 trading days (approximately one month)
3. Exit after holding period

**Weighting**: Value-weighted
**Rebalancing**: Daily (as analyst days occur)

## Fundamental Reason
Firms that pay the costs of hosting analyst days are likely to disclose positive information, since negative information could be disclosed through less conspicuous channels like press releases. Market participants significantly underreact to analyst day information because:
1. Investors may not initially find all information credible
2. Analyst days don't receive enough market attention
3. True impact is only revealed over following days

Abnormal returns remain elevated for up to 60 trading days after events, with no evidence of mean reversion.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2004-2015 |
| Return | 18.3% p.a. |
| Volatility | 24.82% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.59 |

Note: Data from Table 3, Window (0,+20). Market-adjusted return of 1.41% for 20-day window, annualized.

## Source Paper
Wu, Di and Yaron, Amir: Analyst Days, Stock Prices, and Firm Performance
- SSRN: https://ssrn.com/abstract=3272367

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810857/

## Eligibility Check
### Available
- **Transforms**:
  - `market_cap` - For value-weighting
- **Assets**: US Stocks available (NYSE, AMEX, NASDAQ)

### Missing
- **Analyst Day Event Data** - NOT AVAILABLE
  - Requires dates of analyst day events for each company
  - Must be extracted from 8-K filings or press releases
  - SEC EDGAR parsing not available
- **Event Scheduling Data** - NOT AVAILABLE
  - Alternative would be corporate event calendars
  - Typically requires specialized data vendors

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing analyst day event data
- Confidence rating: Strong
- Complexity: Simple
- Alternative data required: 8-K filing parsing or corporate event calendars
- Long-only strategy (cannot be used as market hedge)
- Average ~20 stocks held at any time

