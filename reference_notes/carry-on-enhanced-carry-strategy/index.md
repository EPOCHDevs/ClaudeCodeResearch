# Carry On - Enhanced Carry Strategy

**Quantpedia ID**: #0401
**URL**: https://quantpedia.com/strategies/carry-on-enhanced-carry-strategy
**Status**: INELIGIBLE
**Linear Issue**: [ENG-49](https://linear.app/epoch-inc/issue/ENG-49/feature-request-fx-forward-rates-interest-rate-differentials-0401)

## Overview
An enhanced FX carry strategy that addresses the post-2008 decline in traditional carry trade profitability. The strategy focuses on high-volatility currency pairs and uses a market turbulence filter (based on Mahalanobis distance) to avoid positions during turbulent markets.

## Trading Rules
**Universe**: 45 G10 currency pairs (AUD, CAD, CHF, EUR, GBP, JPY, SEK, NOK, NZD, USD)
**Signal**: Interest rate differential ranking + volatility filtering + turbulence measure
**Selection**:
1. Align each pair so long position yields positive interest rate differential
2. Select 27 pairs with largest differentials
3. Divide into low/high volatility groups (9 pairs each)
4. Apply turbulence filter using 30-day rolling average of Mahalanobis distance
5. Scale position size (100%/75%/50%/25%/0%) based on turbulence percentile rank
**Weighting**: Based on turbulence signal
**Rebalancing**: Monthly

## Fundamental Reason
Carry profits exist to compensate for currency risk. High-volatility carry currencies exhibit expected risk premium characteristics (undervalued on average, boom/bust cycles aligned with crowding). Low-volatility carry has opposite characteristics and hasn't worked since 2008. The turbulence filter anticipates and avoids crash periods.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1984-2017 |
| Return | 2.03% p.a. |
| Volatility | 2.47% |
| Max Drawdown | -14.07% |
| Sharpe Ratio | 0.82 |

## Source Paper
Czasonis, Megan and Pamir, Baykan and Turkington, David: Carry On
- SSRN: https://ssrn.com/abstract=3178314
- State Street White Paper

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238463/7d4dcb4eea206aa10136c90839ac39c2/

## Eligibility Check
### Available
- Transforms: `std` (volatility), covariance matrix computation, percentile ranking
- Assets: G10 FX pairs available (spot rates)

### Missing
- **Forward FX rates**: Required for computing interest rate differentials - NOT AVAILABLE
- **Interest rate differentials**: Core signal for carry trade - NOT AVAILABLE (only have FRED macro rates, not pair-specific)
- Without forward rates, cannot implement the core carry signal

## Implementation Notes
- Very Complex strategy requiring multiple advanced calculations
- Mahalanobis distance calculation for turbulence is computationally feasible
- Core issue: We only have spot FX rates, not forward rates needed for carry
- Would require adding FX forward rate data source or interest rate data by country
