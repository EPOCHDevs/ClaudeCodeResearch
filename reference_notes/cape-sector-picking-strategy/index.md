# CAPE Sector Picking Strategy

**Quantpedia ID**: #0429
**URL**: https://quantpedia.com/strategies/cape-sector-picking-strategy
**Status**: INELIGIBLE
**Linear Issue**: [ENG-272](https://linear.app/epoch-inc/issue/ENG-272/feature-request-sector-level-cape-ratio-data-for-0429)

## Overview
This strategy uses the Cyclically Adjusted Price-to-Earnings (CAPE) ratio to identify undervalued sectors. CAPE, also known as Shiller P/E, uses 10-year average inflation-adjusted earnings to smooth cyclical fluctuations. The strategy selects undervalued sectors while filtering out those with poor momentum.

## Trading Rules
**Universe**: 10 sector ETFs (XLK, XLF, XLE, XLV, XLP, XLI, XLY, XLB, XLU, XLC)

**Signal**: Relative CAPE + Momentum Filter
1. Calculate CAPE ratio for each of the 10 sectors
2. Calculate relative CAPE (sector CAPE vs. historical average)
3. Select 5 most undervalued sectors (lowest relative CAPE)
4. Remove the sector with lowest 12-month momentum from those 5
5. Hold remaining 4 sectors equally weighted

**Selection**:
- Long 4 sectors (most undervalued + momentum filter)
- Long-only strategy

**Weighting**: Equally-weighted
**Rebalancing**: Monthly

## Fundamental Reason
- CAPE is a robust measure of under/overpricing equities
- Uses 10-year average earnings to smooth cyclical fluctuations
- Consistently displays economic and statistical significance in forecasting returns
- Relative valuation approach avoids timing issues with absolute CAPE levels
- Momentum filter removes value traps (cheap but deteriorating sectors)

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2002-2017 |
| Return | 14.23% p.a. |
| Volatility | 17.98% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.79 |

Note: Data from Table 7.

**Note**: No OOS data available in CSV.

## Source Paper
Farouk Jivraj, Robert J. Shiller: The Many Colours of CAPE
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3258404

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810901/

## Eligibility Check
### Available
- **Transforms**:
  - `roc(period=252)` - 12-month momentum calculation
  - `cs_rank` - Cross-sectional ranking
  - Standard financial ratios (P/B, P/S, B/M)
- **Assets** (all 10 sector ETFs available):
  - XLK-Stocks (Technology)
  - XLF-Stocks (Financials)
  - XLE-Stocks (Energy)
  - XLV-Stocks (Health Care)
  - XLP-Stocks (Consumer Staples)
  - XLI-Stocks (Industrials)
  - XLY-Stocks (Consumer Discretionary)
  - XLB-Stocks (Materials)
  - XLU-Stocks (Utilities)
  - XLC-Stocks (Communication Services)

### Missing
- **CAPE Ratio Data** - NOT AVAILABLE
  - Cyclically Adjusted Price-to-Earnings ratio at sector level
  - Requires 10-year average of inflation-adjusted earnings
  - Specialized data typically from Shiller/Barclays or specialty providers
  - Not computable from standard fundamental data we have

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing CAPE ratio data
- Confidence rating: Strong
- Complexity: Simple
- All sector ETFs are available
- Momentum filter is implementable with `roc(period=252)`
- Key blocker: CAPE ratio requires specialized historical earnings data
- Could potentially approximate with standard P/E if CAPE not available (reduced accuracy)
- Long-only strategy (no hedge capability)

