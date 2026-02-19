# Alpha Cloning - Following 13F Filings

**Quantpedia ID**: #0042
**URL**: https://quantpedia.com/strategies/alpha-cloning-following-13f-fillings
**Status**: INELIGIBLE
**Linear Issue**: [ENG-177](https://linear.app/epoch-inc/issue/ENG-177)

## Overview

Replicates positions of top hedge fund managers by following their quarterly 13F SEC filings. Copy the long positions of successful funds.

## Trading Rules

**Universe**: Stocks held by top hedge funds
**Signal**: 13F filing changes
**Rebalancing**: Quarterly (after 13F publication)

## Performance

| Metric | Value |
|--------|-------|
| Period | 1991-2005 |
| Return | 20.21% p.a. |

## Why INELIGIBLE

Requires:
1. **13F Filing Data**: Not available
   - Institutional holdings by fund
   - Filing dates
   - Position changes
2. **Fund Performance Data**: To identify top managers

Would need SEC EDGAR 13F data integration.
