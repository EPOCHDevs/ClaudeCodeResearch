# Merger Arbitrage

**Quantpedia ID**: #0024
**URL**: https://quantpedia.com/strategies/merger-arbitrage
**Status**: INELIGIBLE
**Linear Issue**: [ENG-46](https://linear.app/epoch-inc/issue/ENG-46/feature-request-manda-deal-announcements-data-for-0024)

## Overview

Event-driven market-neutral strategy that exploits price inefficiencies in announced M&A deals. When a merger is announced, the target stock typically trades at a discount to the offer price due to deal completion uncertainty. Arbitrageurs profit by buying the target (long) and shorting the acquirer (in stock deals) to capture the spread as the deal closes.

## Trading Rules

**Universe**: All announced mergers meeting liquidity criteria
**Signal**: Deal spread (offer price vs. current target price)
**Selection**: Deals with positive arbitrage potential
**Weighting**: Equal weight
**Rebalancing**: Daily

### Deal Criteria
- Target market cap > $500M
- Sufficient trading volume
- Acquirer stock easy to borrow (for stock deals)
- Positive acquisition premium
- Offer for substantially all shares
- Acquirer doesn't already own target substantially

### Position Structure
- **Cash Deals**: Long target only
- **Stock Deals**: Long target, short acquirer (hedge ratio based on exchange ratio)

## Fundamental Reason

1. **Deal Uncertainty Premium**: Target trades at discount due to risk of deal failure
2. **Time Value**: Spread compensates for capital tied up during deal process
3. **Event Risk**: Regulatory, financing, or shareholder approval risks
4. **Quasi-Market Neutral**: Simultaneous long/short reduces market exposure

## Performance (Source: Credit Suisse Merger Arbitrage Liquid Index)

| Metric | Value |
|--------|-------|
| Period | 1998-2010 |
| Return | 6.86% p.a. |
| Volatility | 4.72% |
| Sharpe Ratio | 0.61 |

## Source Paper

**Credit Suisse: "Liquid Alternative Beta - Merger Arbitrage"**
- Link: https://quantpedia.com/www/Credit_Suisse_Merger_Arbitrage_Liquid_Index.pdf

## Eligibility Check

### Required Capabilities

1. **M&A Deal Announcements Database**: Need structured data on announced deals including:
   - Announcement date
   - Target and acquirer tickers
   - Deal terms (cash/stock, exchange ratio, premium)
   - Expected close date
   - Deal status (pending, closed, terminated)

2. **Deal Status Updates**: Real-time tracking of deal progress

3. **Stock Borrow Data**: For shorting acquirer in stock deals

### Available
- Stock price data for target/acquirer
- Basic corporate events (IPO, ticker changes)
- News data (could filter for M&A topics)

### MISSING - Why INELIGIBLE

1. **M&A Deal Announcements Data**: No structured database of:
   - Announced mergers and acquisitions
   - Deal terms and consideration type
   - Expected/actual close dates
   - Deal status tracking

2. **No ETF Proxy**: Could alternatively track merger arb via ETF (e.g., MNA, MERFX) but need to verify availability

## Implementation Notes

### Alternative: ETF-Based Approach
If merger arbitrage ETFs are available in our asset universe:
- MNA (IQ Merger Arbitrage ETF)
- MERFX (Credit Suisse merger arb index)

Check: `Grep "MNA-" or "merger" in assets.json`

### If M&A Data Becomes Available
1. Filter deals meeting liquidity criteria
2. Calculate deal spread: `spread = offer_price - target_price`
3. Rank by spread attractiveness
4. Size positions by expected close date (shorter = higher weight)
5. For stock deals: hedge with acquirer short

## Related Strategies

- Event-driven strategies
- Pairs trading (similar long/short structure)
- Arbitrage strategies
