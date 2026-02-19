# Geographical Country Momentum

**Quantpedia ID**: #0420
**URL**: https://quantpedia.com/strategies/geographical-country-momentum
**Status**: INELIGIBLE
**Linear Issue**: [ENG-263](https://linear.app/epoch-inc/issue/ENG-263/feature-request-geographical-distance-and-gdp-data-for-0420)

## Overview
This strategy exploits the "gravity" effect in international equity markets - larger countries' returns lead smaller countries' returns, and this predictability is stronger for geographically closer countries. The strategy constructs a gravity-weighted momentum signal based on neighboring countries' past returns.

## Trading Rules
**Universe**: Equity market indices for 44 countries

**Signal**: Gravity measure (weighted momentum of neighbors)
1. Calculate aggregate distance between countries (population-weighted city distances)
2. Compute gravity Z-score based on:
   - Z-score of country size (log GDP)
   - Z-score of distance between countries
3. Total Gravity = Z(size) - Z(distance)
4. Calculate weights from gravity scores
5. Gravity measure = weighted sum of neighbors' past month returns

**Selection**:
1. Sort countries by Gravity measure into quintiles
2. Long top quintile (highest Gravity score)

**Weighting**: Value-weighted
**Rebalancing**: Monthly

## Fundamental Reason
Stronger economies influence their neighbors. The strength of economic links is captured by geographical distance (barrier to interaction due to language, institutional, regulatory, historical and cultural differences). Large countries' positive/negative news transmits to smaller nearby countries with a lag, creating predictability. This is a specific case of a more general pattern - Newton's law of universal gravitation applied to financial markets.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1990-2014 |
| Return | 12.69% p.a. |
| Volatility | 19.83% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.64 |

Note: Data from Table 14, Panel A, F-5.

## Source Paper
Bae, Joon Woo: Gravity in International Equity Markets
- SSRN: https://ssrn.com/abstract=3312433

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/24907737/

## Eligibility Check
### Available
- **Transforms**:
  - `roc` / `momentum` - Past return calculation
  - `cs_rank` - Cross-sectional ranking for quintile sorting
  - `cs_zscore` - Z-score normalization
- **Assets**: Some country ETFs available

### Missing
- **Bilateral Geographical Distance Data** - NOT AVAILABLE
  - Distance between largest cities of 44 countries
  - Population-weighted aggregate distances
- **Country GDP Data** - NOT AVAILABLE
  - Historical GDP for 44 countries
  - Used to compute economic size Z-scores
- **City Population Data** - NOT AVAILABLE
  - Used to weight inter-city distances
- **Complete Country Index Universe** - PARTIAL
  - Need 44 country equity indices
  - Many emerging markets may not be available

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing geographical/GDP data
- Confidence rating: Strong
- Complexity: Very Complex (requires gravity score computation)
- Alternative data required: CEPII GeoDist database, World Bank GDP
- Long-only variant cannot hedge equity risk

