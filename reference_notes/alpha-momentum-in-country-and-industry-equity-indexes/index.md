# Alpha Momentum in Country and Industry Equity Indexes

**Quantpedia ID**: #0404
**URL**: https://quantpedia.com/strategies/alpha-momentum-in-country-and-industry-equity-indexes
**Status**: ELIGIBLE
**Linear Issue**: [ENG-122](https://linear.app/epoch-inc/issue/ENG-122/implement-alpha-momentum-in-country-and-industry-equity-indexes-0404)

## Overview
This strategy exploits alpha momentum in international country equity indexes. Past short-term alphas (12-month) positively predict future returns. The strategy computes CAPM alphas, scales them by volatility to create an alpha score, then ranks countries and goes long the highest quintile while shorting the lowest quintile.

## Trading Rules
**Universe**: 51 country indexes (developed and emerging markets) - implementable with ~25 available ETFs
- EWJ (Japan), EZU (Eurozone), EFNL (Finland), EWW (Mexico), IVV (S&P 500)
- AAXJ (Asia ex-Japan), EWQ (France), EWH (Hong Kong), EPI (India), EIDO (Indonesia)
- EWI (Italy), ENZL (New Zealand), NORW (Norway), EWY (South Korea), EWP (Spain)
- EWD (Sweden), EWL (Switzerland), GXC (China), EWC (Canada), EWZ (Brazil)
- ARGT (Argentina), AIA (Asia 50), EWO (Austria), EWK (Belgium), ECH (Chile)

**Signal**: Alpha Momentum
1. Compute alphas using CAPM model: R_i = alpha + beta * R_market + epsilon
2. Calculate alpha score = alpha / volatility (volatility-adjusted alpha)
3. Alpha momentum = volatility-adjusted alpha estimated during months t-12 to t-1

**Selection**:
1. At month end, compute alpha score for each country index
2. Rank indexes by alpha score
3. Long highest quintile (top 20%)
4. Short lowest quintile (bottom 20%)

**Weighting**: Value-weighted (equal-weighted also tested)
**Rebalancing**: Monthly

## Fundamental Reason
Alpha-based strategies adjust past returns for systematic risk (market factor). By using alpha instead of raw returns, the strategy disentangles momentum from risk factor effects. The strategy benefits from mispricing by going long undervalued assets (positive alphas) and short overvalued ones (negative alphas). Behavioral explanation: investor irrationality creates persistent alpha patterns that cannot be easily arbitraged away.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1973-2018 |
| Return | 6.3% p.a. |
| Volatility | 20.02% |
| Max Drawdown | -79.73% |
| Sharpe Ratio | 0.31 |

Note: Data from Table 3, Countries, T-B portfolio (Top minus Bottom quintile)

## Source Paper
Zaremba, Adam and Umutlu, Mehmet and Karathanasopoulos, Andreas: Alpha Momentum and Alpha Reversal in Country and Industry Equity Indexes
- SSRN: https://ssrn.com/abstract=3235350

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238480/cacbb14de812a255b7f0ddb574ca9c6b/

## Eligibility Check
### Available
- **Transforms**:
  - `multilinear_fit` - Multi-variate OLS regression for CAPM alpha calculation
  - `stddev` - Standard deviation for volatility scaling
  - `cs_rank` - Cross-sectional ranking
  - `roc` / `momentum` - Rate of change / momentum
  - `cs_zscore` - Cross-sectional z-score normalization
- **Assets**: 25+ country ETFs available:
  - EWJ, EZU, EFNL, EWW, IVV, AAXJ, EWQ, EWH, EPI, EIDO
  - EWI, ENZL, NORW, EWY, EWP, EWD, EWL, GXC, EWC, EWZ
  - ARGT, AIA, EWO, EWK, ECH

### Missing (Non-critical)
- ERUS (Russia), GAF (Middle East/Africa), EGPT (Egypt), ADRU (Europe ADR), BRAQ (Brazil Consumer), CHIB (China Tech)
- These 6 missing ETFs are not critical - strategy can be implemented with available 25+ ETFs

## Implementation Notes
- Strategy is marked ELIGIBLE with reduced universe (25+ ETFs instead of 51)
- Confidence rating: Strong
- Complexity: Complex (requires CAPM regression)
- All core transforms available for CAPM alpha computation
- Monthly rebalancing is straightforward
- Consider using `multilinear_fit` with market returns as the x variable to compute rolling alpha
- Alpha score = alpha output / stddev(returns)
- Use `cs_rank` for quintile portfolio construction
