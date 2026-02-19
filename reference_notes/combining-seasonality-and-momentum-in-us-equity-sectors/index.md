# Combining Seasonality and Momentum in US Equity Sectors

**Quantpedia ID**: #0032
**URL**: https://quantpedia.com/strategies/combining-seasonality-and-momentum-in-us-equity-sectors
**Status**: ELIGIBLE
**Linear Issue**: [ENG-144](https://linear.app/epoch-inc/issue/ENG-144/implement-combining-seasonality-and-momentum-in-us-equity-sectors-0032)

## Overview

Sector rotation strategy that combines seasonality and momentum signals to select US equity sectors. Different sectors exhibit distinct seasonal patterns (e.g., Technology strong in Q4, Energy in Q1). By combining these seasonal patterns with momentum confirmation, the strategy aims to achieve higher returns than either signal alone.

## Trading Rules

**Universe**: US Equity Sector ETFs (XLK, XLP, XLF, XLB, XLV, XLE, XLI, XLY, XLC, XLU)
**Signal**: Seasonality + Momentum composite
**Selection**: Top sectors by combined score
**Weighting**: Equal weight among selected sectors
**Rebalancing**: Monthly

### Detailed Rules
1. Calculate seasonal score for each sector based on historical monthly returns
2. Calculate momentum score (past 12-month return excluding last month)
3. Combine: 50% seasonality + 50% momentum
4. Long top N sectors by combined score
5. Rebalance monthly

### Sector ETFs
- XLK: Technology
- XLY: Consumer Discretionary
- XLI: Industrials
- XLF: Financials
- XLV: Healthcare
- XLP: Consumer Staples
- XLE: Energy
- XLB: Materials
- XLU: Utilities
- XLC: Communication Services

## Fundamental Reason

1. **Sector Seasonality**: Different sectors perform better in different months/quarters
2. **Momentum Confirmation**: Momentum validates seasonal expectations
3. **Diversification**: Using both signals reduces false signals from either alone
4. **Economic Cycles**: Seasonal patterns often align with economic calendar events

## Performance (Source)

| Metric | Value |
|--------|-------|
| Period | 1970-2008 |
| Return | 12.9% p.a. |
| Volatility | 17.0% |
| Sharpe Ratio | 0.52 |

**Notes**: Premium strategy - full details require Quantpedia Premium access.

## Eligibility Check

### Required Capabilities
1. **Seasonality Detection**: Calendar-based month detection
2. **Momentum Calculation**: Past returns
3. **Cross-Sectional Ranking**: Sector selection
4. **Sector ETF Universe**: US sector ETFs

### Available
- `month_of_year` - Month detection for seasonality
- `roc` - Momentum calculation
- `cs_rank` - Cross-sectional ranking
- Sector ETFs: XLK, XLP, XLF, XLB, XLV, XLE, XLI, XLY, XLC, XLU all available

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **Universe**:
   ```
   sectors = ['XLK', 'XLP', 'XLF', 'XLB', 'XLV', 'XLE', 'XLI', 'XLY', 'XLC', 'XLU']
   ```

2. **Seasonal Score**:
   Option A - Historical average return by month:
   ```
   # Pre-compute average return for each sector by month
   # Use month_of_year to apply appropriate weight
   jan_weight = month_of_year(month='January') * historical_jan_return
   feb_weight = month_of_year(month='February') * historical_feb_return
   # ... combine for seasonal_score
   ```

   Option B - Simple seasonal pattern:
   ```
   # Use known patterns: Tech strong Q4, Energy Q1, etc.
   tech_season = month_of_year(month='October') OR month_of_year(month='November') OR month_of_year(month='December')
   ```

3. **Momentum Score**:
   ```
   mom_12m = roc(close, 252) - roc(close, 21)  # 12m excluding last month
   mom_score = cs_rank(mom_12m) / cs_count(mom_12m)  # Normalize to 0-1
   ```

4. **Combined Signal**:
   ```
   combined = 0.5 * seasonal_score + 0.5 * mom_score
   long_signal = cs_rank(combined) >= threshold
   ```

5. **Rebalancing**: Monthly using `rebalance_interval='monthly'`

### Considerations
- Requires pre-computed seasonal patterns per sector
- Seasonality effects may have weakened over time
- Consider equal weighting among top 3-5 sectors

## Related Strategies

- #0014 Momentum Factor Effect in Stocks
- #0031 Market Seasonality Effect in World Equity Indexes
- Sector rotation strategies

## Notes

This is a Premium Quantpedia strategy. The implementation above is based on the strategy name and available transforms. Historical seasonal patterns by sector would need to be researched from academic literature.
