# Timing Betting Against Beta with Small Stocks

**Quantpedia ID**: #0407
**URL**: https://quantpedia.com/strategies/timing-betting-against-beta-with-small-stocks
**Status**: INELIGIBLE
**Linear Issue**: [ENG-161](https://linear.app/epoch-inc/issue/ENG-161/feature-request-aqr-factor-data-bab-smb-for-global-markets-0407)

## Overview
This strategy times the Betting-Against-Beta (BAB) factor using the short-term performance of small stocks. The performance of small firms in the stock market predicts future BAB returns. When small stocks outperform, BAB strategies tend to perform well subsequently due to improved funding conditions.

## Trading Rules
**Universe**: Stocks in 24 developed markets covered by AQR factors
- Australia, Austria, Belgium, Canada, Denmark, Finland, France, Germany, Greece, Hong Kong, Ireland, Israel, Italy, Japan, Netherlands, New Zealand, Norway, Portugal, Singapore, Spain, Sweden, Switzerland, UK, US

**Signal**: Trailing 3-month SMB (Small Minus Big) factor returns by country

**Selection**:
1. Each month, compute average SMB return for months t-3 to t-1 for each country
2. Sort countries by 3-month SMB return
3. Long BAB strategies in top 20% of countries (highest SMB)
4. Short BAB strategies in bottom 20% of countries (lowest SMB)

**Weighting**: Equal-weighted
**Rebalancing**: Monthly

## Fundamental Reason
There's a link between asset liquidity (manifested in small stock performance) and funding liquidity that affects low-beta strategy profitability. Rising small stock prices improve collateral values and funding conditions, creating additional demand for leveraged low-beta positions. This pushes low-beta stock prices higher, generating elevated BAB returns.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1989-2018 |
| Return | 22.42% p.a. |
| Volatility | 19.87% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 1.13 |

Note: Data from Table 4 Panel B, 20% of countries, H-L

## Source Paper
Zaremba, Adam: Small-Minus-Big Predicts Betting-Against-Beta: Implications for International Equity Allocation and Market Timing
- SSRN: https://ssrn.com/abstract=3227047

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810805/e3a77d7585ad78f32a74fc454c4dea6d/

## Eligibility Check
### Available
- **Transforms**:
  - `multilinear_fit` - For computing beta/factor exposures
  - `cs_rank` - For ranking countries
  - `roc` - For returns calculation
- **Assets**: Limited international country ETFs available

### Missing
- **AQR BAB (Betting Against Beta) factor returns for 24 countries** - NOT AVAILABLE
  - Would need pre-computed long low-beta / short high-beta factor portfolios for each country
- **AQR SMB (Small Minus Big) factor returns for 24 countries** - NOT AVAILABLE
  - Would need pre-computed long small cap / short large cap factor portfolios for each country
- **Full global equity data for 24 developed markets** - Limited coverage

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing AQR factor data
- Complexity rating: Very Complex
- Could theoretically construct factors from scratch if full global stock data was available
- Would require significant infrastructure to compute country-level BAB and SMB factors
- Alternative: Could simplify to use country ETFs as proxies for BAB/SMB exposure
