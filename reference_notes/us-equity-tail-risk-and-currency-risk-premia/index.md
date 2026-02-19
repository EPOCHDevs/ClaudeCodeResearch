# US Equity Tail Risk and Currency Risk Premia

**Quantpedia ID**: #0438
**URL**: https://quantpedia.com/strategies/us-equity-tail-risk-and-currency-risk-premia
**Status**: INELIGIBLE
**Linear Issue**: [ENG-281](https://linear.app/epoch-inc/issue/ENG-281/feature-request-cboe-pput-index-data-for-0438)

## Overview
This strategy exploits the relationship between US equity tail risk and currency returns. It uses a tail risk factor (long CBOE PPut index, short S&P 500) to measure tail risk exposure. Currencies with high exposure to US tail risk are shorted, while those with low exposure are bought.

## Trading Rules
**Universe**: 14 developed market currencies (AUD, CAD, DKK, EUR, HKD, ILS, JPY, NZD, NOK, SGD, KRW, SEK, CHF, GBP)

**Signal**: US equity tail beta
1. Construct tail risk factor: Long CBOE PPut index, Short S&P 500
2. Calculate log return of tail risk factor
3. Run 60-month rolling regression: Currency returns vs S&P 500 + tail factor
4. Extract tail betas for each currency
5. Sort currencies into quintiles by tail beta

**Selection**:
- Long lowest tail beta quintile
- Short highest tail beta quintile

**Weighting**: Equal-weighted
**Rebalancing**: Monthly

## Fundamental Reason
- US equity developments affect global asset pricing
- Currencies that hedge US tail risk have lower expected returns
- Tail risk factor uses forward-looking option-implied information
- Currencies with high tail beta act as hedges and are overpriced
- Cross-sectional factor explains carry and momentum portfolios

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1989-2018 |
| Return | 4.57% p.a. |
| Volatility | 8.16% |
| Max Drawdown | -58.98% |
| Sharpe Ratio | 0.56 |

Note: Data from Table 2, Panel B, L-H.

**WARNING**: OOS shows -4.27% return, -0.38 Sharpe. Strategy alpha completely reversed.

## Source Paper
Fan, Zhenzhen et al.: US Equity Tail Risk and Currency Risk Premia
- SSRN: https://ssrn.com/abstract=3399980

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810913/

## Eligibility Check
### Available
- **Transforms**:
  - `roc` - Return calculation
  - Rolling regression possible with custom logic
- **Assets** (partial FX pairs):
  - ^AUDUSD-FX, ^CADUSD-FX, ^EURUSD-FX, ^JPYUSD-FX ✓
  - ^NZDUSD-FX, ^CHFUSD-FX, ^GBPUSD-FX ✓
  - SPY-Stocks (S&P 500 proxy) ✓

### Missing
- **CBOE PPut Index** - NOT AVAILABLE
  - CBOE Put Protection index (ticker: PPUT)
  - Protective put strategy on S&P 500
  - 5% OTM monthly SPX put options
  - Critical for tail risk factor construction
- **Some DM Currencies** - PARTIAL
  - Missing: DKK, HKD, ILS, SGD, KRW, SEK, NOK

## Implementation Notes
- Strategy is marked INELIGIBLE due to:
  1. Missing CBOE PPut index data (critical)
  2. Missing several developed market currencies
- Confidence rating: Moderate
- Complexity: Complex
- **WARNING**: Negative OOS performance (-0.38 Sharpe) suggests strategy is broken
- Not recommended for implementation even if data available

