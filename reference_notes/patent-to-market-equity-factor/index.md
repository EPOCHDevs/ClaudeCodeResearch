# Patent-to-Market Equity Factor

**Quantpedia ID**: #0414
**URL**: https://quantpedia.com/strategies/patent-to-market-equity-factor
**Status**: INELIGIBLE
**Linear Issue**: [ENG-211](https://linear.app/epoch-inc/issue/ENG-211/feature-request-patent-grant-data-for-0414)

## Overview
This strategy exploits the relationship between a firm's patent portfolio value and its stock returns. Firms with high patent-to-market (PTM) ratios - where the cumulative market value of patents is high relative to market capitalization - tend to outperform firms with low PTM ratios. The market value of patents is estimated using stock price reactions around patent grant announcement dates.

## Trading Rules
**Universe**: Stocks on NYSE, AMEX, NASDAQ (only firms with at least one patent)

**Signal**: Patent-to-Market (PTM) ratio
1. Estimate market value of each patent using abnormal returns around patent grant dates
2. Compute cumulative market value of all patents for each firm
3. Calculate PTM ratio = Cumulative Patent Value / Market Cap

**Selection**:
1. Sort stocks into deciles by PTM ratio
2. Long highest decile (high PTM)
3. Short lowest decile (low PTM)

**Weighting**: Value-weighted
**Rebalancing**: Monthly

## Fundamental Reason
Patents represent intangible assets that are often undervalued by the market. Firms with valuable patent portfolios relative to their market cap may be underpriced because:
1. Accounting rules don't fully capture patent values on balance sheets
2. Investors may underreact to patent-related information
3. Patents provide competitive advantages and future cash flows not reflected in current valuations
4. The market slowly incorporates patent value information into stock prices

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1965-2011 |
| Return | 5.91% p.a. |
| Volatility | 11.70% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.16 |

Note: Data from Table 1, Panel B, PTM factor returns (annual 5.91%).

## Source Paper
Kogan, Leonid and Papanikolaou, Dimitris and Seru, Amit and Stoffman, Noah: Technological Innovation, Resource Allocation, and Growth
- SSRN: https://ssrn.com/abstract=2193068

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238519/

## Eligibility Check
### Available
- **Transforms**:
  - `cs_rank` - Cross-sectional ranking for decile sorting
  - `market_cap` - For value-weighting and PTM calculation
- **Assets**: US Stocks available (NYSE, AMEX, NASDAQ universe)

### Missing
- **Patent Grant Data** - NOT AVAILABLE
  - Requires USPTO patent grant dates for each firm
  - Need historical patent grant announcements
- **Patent Value Estimation** - NOT AVAILABLE
  - Requires abnormal returns around patent grant dates
  - Need event study methodology to estimate patent market value
- **Firm-Patent Mapping** - NOT AVAILABLE
  - Need to link patents to publicly traded companies

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing patent data
- Confidence rating: Strong
- Complexity: Very Complex (requires patent value estimation via event study)
- Alternative data required: USPTO patent grants + firm-patent linkage
- Even with data, implementation requires event study for each patent grant
- KPSS patent data available from authors' website but needs integration

