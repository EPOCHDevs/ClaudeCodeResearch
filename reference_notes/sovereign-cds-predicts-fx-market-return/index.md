# Sovereign CDS Predicts FX Market Return

**Quantpedia ID**: #0415
**URL**: https://quantpedia.com/strategies/sovereign-cds-predicts-fx-market-return
**Status**: INELIGIBLE
**Linear Issue**: [ENG-232](https://linear.app/epoch-inc/issue/ENG-232/feature-request-sovereign-cds-spread-data-for-0415)

## Overview
This strategy exploits the predictive relationship between sovereign credit default swap (CDS) term premia and exchange rate returns. Countries with steeper CDS spread curves (higher term premia) tend to see their currencies appreciate against the USD. The CDS term structure reflects country-specific risk rather than global risk, making it useful for cross-sectional currency trading.

## Trading Rules
**Universe**: 29 USD currency pairs

**Signal**: CDS term premium
1. Compute CDS term premium = log(10-year CDS spread) - log(1-year CDS spread)
2. Higher term premium indicates reduced short-term risk or increased long-term risk

**Selection**:
1. At month-end, sort currencies into 3 portfolios by CDS term premia
2. Long the highest CDS term premium portfolio
3. Short the lowest CDS term premium portfolio

**Weighting**: Equally-weighted
**Rebalancing**: Monthly

## Fundamental Reason
The sovereign CDS term structure contains information on country-specific shocks rather than global systematic risk. A higher term premium can represent either reduced short-term risk or increased long-term risk. Empirically, the reduced short-term risk effect dominates - innovations in the CDS slope represent good news and predict subsequent currency appreciations. This pattern is robust and not related to the financial crisis.

From an asset pricing perspective, currencies are treated as financial assets. If investors consistently price assets across different markets, state variables from one market (CDS) can predict another (FX) due to shared risks in the stochastic discount factor.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2007-2017 |
| Return | 4.84% p.a. |
| Volatility | 5.92% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.82 |

Note: Data from Table 5, Panel A. Volatility computed from t-stat (2.53).

## Source Paper
Calice, Giovanni and Zeng, Ming: The Term Structure of Sovereign CDS and the Cross-Section Exchange Rate Predictability
- URL: http://www.bbk.ac.uk/ems/research/Seminar_info/spring-17-18/Giovanni%20CALICE%20-%20Paper_Sovereign_CDS_2018.pdf

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810839/

## Eligibility Check
### Available
- **Transforms**:
  - `log` - For log transformation of CDS spreads
  - `cs_rank` - Cross-sectional ranking for tercile sorting
- **Assets**: FX pairs available (but limited coverage)

### Missing
- **Sovereign CDS Spread Data** - NOT AVAILABLE
  - Requires 1-year and 10-year CDS spreads for 29 countries
  - Sovereign CDS is specialized credit derivatives data
  - Not available in standard market data feeds
- **Full FX Universe** - PARTIALLY AVAILABLE
  - Need 29 USD currency pairs
  - Many EM currencies may not be available

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing sovereign CDS data
- Confidence rating: Strong
- Complexity: Simple (only requires sorting on CDS term premium)
- Alternative data required: Sovereign CDS term structure data
- Potential data sources: Bloomberg, Markit, Refinitiv
- Even with data, requires matching CDS countries to FX pairs

