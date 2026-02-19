# Buy-Side Competition and Momentum Profits

**Quantpedia ID**: #0412
**URL**: https://quantpedia.com/strategies/buy-side-competition-and-momentum-profits
**Status**: INELIGIBLE
**Linear Issue**: [ENG-183](https://linear.app/epoch-inc/issue/ENG-183/feature-request-mutual-fund-holdings-13f-institutional-data-0412)

## Overview
This strategy enhances traditional momentum by filtering for stocks with low "buy-side competition" - stocks where fewer mutual funds are competing for momentum profits. Momentum generates larger profits when buy-side competition is low because investing rents are limited when investors compete more vigorously.

## Trading Rules
**Universe**: All common stocks on NYSE, AMEX, NASDAQ (excluding financials and price < $1)

**Signal**: Momentum with buy-side competition filter
1. Obtain mutual fund holdings data
2. Compute 12-month momentum (t-12 to t-2) for each stock
3. Standardize each stock's return to a z-score (momentum space)
4. Locate each mutual fund in momentum space based on value-weighted holdings
5. Define competitors: funds with inter-fund distance <= threshold
6. Compute competition measure = competition averaged across all funds holding each stock

**Selection**:
1. Sort stocks into terciles by momentum competition
2. Within lowest competition tercile, sort into quintiles by 12-month momentum
3. Long highest quintile (high momentum, low competition)
4. Short lowest quintile (low momentum, low competition)

**Weighting**: Value-weighted
**Rebalancing**: Monthly

## Fundamental Reason
If profit opportunities exist, buy-side investors will exploit them. Buy-side price pressure is stronger when more investors target the same opportunity. Momentum should generate larger profits when competition is low because:
1. Investing rents are limited when investors compete vigorously
2. Low competition stocks have momentum that cannot be easily arbitraged away
3. Correlated signals among rival funds reduce individual fund's edge

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1980-2018 |
| Return | 14.27% p.a. |
| Volatility | 22.98% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.58 |

Note: Data from Table 4, Panel A, Low Competition, 5-1 Quintile, annualized monthly return (1.118%).

## Source Paper
Hoberg, Gerard and Kumar, Nitin and Prabhala, Nagpurnanand: Buy-Side Competition and Momentum Profits
- SSRN: https://ssrn.com/abstract=3132378

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810817/

## Eligibility Check
### Available
- **Transforms**:
  - `roc` / `momentum` - 12-month momentum calculation
  - `cs_zscore` - Cross-sectional z-score normalization
  - `cs_rank` - Cross-sectional ranking for quintile sorting
  - `market_cap` - For value-weighting

### Missing
- **Mutual Fund Holdings Data** - NOT AVAILABLE
  - Requires portfolio-level holdings from actively managed US equity mutual funds
  - Need to know which stocks each fund holds and their weights
  - Source paper used CRSP Survivor-Bias Free U.S. Mutual Fund database
- **13F Institutional Holdings** - Could be alternative but also NOT AVAILABLE
  - Would need quarterly 13F filings from institutional investors

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing mutual fund holdings data
- Confidence rating: Strong
- Complexity: Very Complex (requires computing buy-side competition metric)
- Alternative data required: Mutual fund holdings or 13F institutional data
- The paper's competition metric computation is complex (see pages 11-12 of source paper)
- Even with data, implementation is challenging

