# The Equity Differential Factor in Currencies

**Quantpedia ID**: #0439
**URL**: https://quantpedia.com/strategies/the-equity-differential-factor-in-currencies
**Status**: ELIGIBLE
**Linear Issue**: [ENG-282](https://linear.app/epoch-inc/issue/ENG-282/implement-equity-differential-factor-in-currencies-0439)

## Overview
This strategy predicts currency returns using the differential in trailing 12-month equity index returns across countries. Currencies of countries with stronger equity performance tend to appreciate. The strategy buys currencies with high equity differentials and sells those with low differentials.

## Trading Rules
**Universe**: 45 currency pairs (G10 currencies)

**Signal**: Equity differential
1. Calculate 12-month trailing equity index returns for each G10 country
2. Calculate equity differential for each currency pair
3. Orient each pair to represent positive equity differential
4. Equal weight all pairs (or select largest differentials)
5. Net currency exposures across pairs

**Selection**:
- Long currencies with high trailing equity returns
- Short currencies with low trailing equity returns

**Weighting**: Equal-weighted
**Rebalancing**: Monthly

## Fundamental Reason
- Equity index returns indicate country-level risk and returns
- Higher long-run equity premiums correlate with currency risk
- Investor demand flows to countries with outperforming equity markets
- Effect independent of carry, trend, and valuation factors

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1990-2017 |
| Return | 1.9% p.a. |
| Volatility | 3.1% |
| Max Drawdown | -9.2% |
| Sharpe Ratio | 0.61 |

Note: Data from Table 1, Equity Differential.

**WARNING**: OOS (2004-2025) shows -0.1% return, -0.05 Sharpe. Strategy alpha essentially zero.

## Source Paper
Turkington, Yazdani: The Equity Differential Factor in Currency Markets
- DOI: https://www.tandfonline.com/doi/full/10.1080/0015198X.2020.1712924

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238661/

## Eligibility Check
### Available
- **Transforms**:
  - `roc(period=252)` - 12-month equity returns
  - Cross-sectional ranking available
- **Country ETFs** (G10 proxies):
  - EWA-Stocks (Australia) ✓
  - EWC-Stocks (Canada) ✓
  - EWG-Stocks (Germany/Eurozone) ✓
  - EWJ-Stocks (Japan) ✓
  - EWU-Stocks (UK) ✓
  - EWL-Stocks (Switzerland) ✓
  - EWD-Stocks (Sweden) ✓
  - NORW-Stocks (Norway) ✓
  - ENZL-Stocks (New Zealand) ✓
  - SPY-Stocks (US) ✓
- **FX Pairs** (G10 currencies):
  - ^EURUSD-FX, ^GBPUSD-FX, ^JPYUSD-FX ✓
  - ^AUDUSD-FX, ^CADUSD-FX, ^NZDUSD-FX ✓
  - ^CHFUSD-FX and others ✓

### Formula
```
# 12-month equity returns for each G10 country
equity_return = roc(period=252)(country_etf)

# For each currency pair, calculate equity differential
equity_diff = equity_return_country_A - equity_return_country_B

# Long positive differential, short negative
# Net exposures across all 45 pairs
```

## Implementation Notes
- Strategy is marked ELIGIBLE with all G10 country ETFs and FX pairs available
- Confidence rating: Moderate
- Complexity: Simple
- **WARNING**: Near-zero OOS Sharpe (-0.05) suggests very low priority
- Not recommended for implementation due to poor recent performance
- Could combine with other factors (carry, momentum) for improvement

