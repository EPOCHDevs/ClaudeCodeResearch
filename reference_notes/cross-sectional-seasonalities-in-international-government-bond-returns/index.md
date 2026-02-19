# Cross-Sectional Seasonalities in International Government Bond Returns

**Quantpedia ID**: #0403
**URL**: https://quantpedia.com/strategies/cross-sectional-seasonalities-in-international-government-bond-returns
**Status**: INELIGIBLE
**Linear Issue**: [ENG-53](https://linear.app/epoch-inc/issue/ENG-53/feature-request-international-government-bond-futures-data-0403)

## Overview
A cross-sectional seasonality strategy applied to international government bonds. Bonds with high average same-calendar-month returns historically tend to outperform in that month going forward. The strategy sorts 22 country bond buckets by their "SAME" measure and trades long-short.

## Trading Rules
**Universe**: 22 country government bond buckets (10+ year maturity)
- Australia, Austria, Belgium, Canada, China, Denmark, France, Germany, India, Ireland, Italy, Japan, South Korea, Mexico, Netherlands, Portugal, South Africa, Spain, Sweden, Switzerland, UK, US

**Signal**: SAME = Average return in same calendar month over past 20 years
**Selection**:
1. At month end, compute SAME for each bond bucket
2. Sort bonds by SAME
3. Use 20% cutoff for quintile portfolios
**Weighting**: Equal weighted
**Rebalancing**: Monthly

**Long**: Highest SAME quintile
**Short**: Lowest SAME quintile

Paper recommends using futures for easier application.

## Fundamental Reason
Behavioral explanation - cyclical swings in investor mood create calendar patterns. Anomaly is pronounced during high investor sentiment periods and in market segments with elevated limits to arbitrage.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1980-2018 |
| Return | 5.41% p.a. |
| Volatility | 11.07% |
| Max Drawdown | -26.17% |
| Sharpe Ratio | 0.49 |

**WARNING**: Quantpedia rates confidence as "Weak" - OOS backtest shows significantly negative performance. In-sample results may have been data mined.

## Source Paper
Zaremba, Adam: Cross-Sectional Seasonalities in International Government Bond Returns
- SSRN: https://ssrn.com/abstract=3212995

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238469/101222805b287282402080cb032609d5/

## Eligibility Check
### Available
- Transforms: Monthly returns, averaging, percentile ranking
- Assets: US Treasury futures only (ZT, ZB, ZF, ZN, TN, ZE, ZZ, UD)

### Missing
- **International government bond futures**: Required for 21 of 22 countries - NOT AVAILABLE
  - Missing: Australia, Austria, Belgium, Canada, China, Denmark, France, Germany, India, Ireland, Italy, Japan, South Korea, Mexico, Netherlands, Portugal, South Africa, Spain, Sweden, Switzerland, UK
- Only have US Treasury futures
- 20+ years of historical data required for proper SAME calculation

## Implementation Notes
- Even if assets were available, Quantpedia OOS shows significantly NEGATIVE performance
- High turnover strategy - transaction costs matter significantly
- Paper may have been data mined
- NOT RECOMMENDED for implementation even if assets become available
