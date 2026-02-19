# Market Timing with Aggregate and Idiosyncratic Stock Volatilities

**Quantpedia ID**: #0027
**URL**: https://quantpedia.com/strategies/market-timing-with-aggregate-and-idiosyncratic-stock-volatilities
**Status**: ELIGIBLE
**Linear Issue**: [ENG-59](https://linear.app/epoch-inc/issue/ENG-59/implement-market-timing-with-volatilities-0027)

## Overview

Market timing strategy that uses aggregate market volatility and idiosyncratic stock volatility to predict equity returns. The strategy is based on the observation that high idiosyncratic volatility often precedes poor market returns, while aggregate volatility has a different predictive relationship. By decomposing total volatility into systematic and idiosyncratic components, the strategy aims to time market exposure.

## Trading Rules

**Universe**: Equity market (SPY, equity indices)
**Signal**: Aggregate + Idiosyncratic volatility measures
**Selection**: Binary market timing (long market or risk-free)
**Weighting**: All-in or cash
**Rebalancing**: Quarterly

### Signal Components
1. **Aggregate Volatility**: Overall market volatility (e.g., VIX or realized volatility of market index)
2. **Idiosyncratic Volatility**: Cross-sectional dispersion of stock returns after removing market factor

### Trading Logic
- Calculate aggregate volatility from market index returns
- Calculate idiosyncratic volatility from residuals of stock returns vs market
- Use combined signal to determine market exposure
- High idiosyncratic volatility → reduce equity exposure
- Rebalance quarterly

## Fundamental Reason

1. **Idiosyncratic Vol as Predictor**: High dispersion in stock-specific returns often signals investor uncertainty and precedes market declines
2. **Aggregate vs Idiosyncratic**: These two components have different predictive power for future returns
3. **Risk-Return Trade-off**: Elevated volatility should be compensated with higher returns, but this relationship can be exploited for timing

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1968-2004 |
| Return | 20.07% p.a. |
| Volatility | 37.8% |
| Max Drawdown | -9.29% |
| Sharpe Ratio | 0.43 |

**Notes**: Premium strategy - full details require Quantpedia Premium access.

## Eligibility Check

### Required Capabilities
1. **Aggregate Volatility**: Calculate realized volatility of market index
2. **Idiosyncratic Volatility**: Compute residuals from market regression, then calculate cross-sectional volatility

### Available
- `multi_linear_fit` - Computes factor betas, residuals (idiosyncratic returns), R-squared
- `stddev` - Standard deviation for volatility calculation
- `rolling_ols` - Rolling OLS regression for dynamic beta/residuals
- `beta` - Rolling beta coefficient
- SPY and market index data available

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **Aggregate Volatility**:
   ```
   market_returns = roc(spy.close, 1)
   agg_vol = stddev(market_returns, window=63)  # Quarterly realized vol
   ```

2. **Idiosyncratic Volatility** (per stock):
   ```
   # Regress stock returns on market returns
   regression = multi_linear_fit(stock_returns, market_returns, window=252)
   residuals = regression.residual  # Idiosyncratic returns
   idio_vol = stddev(residuals, window=63)
   ```

3. **Cross-sectional Idiosyncratic Volatility**:
   ```
   avg_idio_vol = cs_mean(idio_vol)  # Cross-sectional average
   ```

4. **Signal Generation**:
   - Compare current idiosyncratic vol to historical average
   - High idio vol relative to aggregate vol → reduce exposure
   - Generate binary or scaled signal for market timing

5. **Rebalancing**: Quarterly using `rebalance_interval='quarterly'`

## Related Strategies

- #0020 Volatility Risk Premium Effect
- #0007 Low Volatility Factor Effect in Stocks
- VIX-based market timing strategies

## Notes

This is a Premium Quantpedia strategy. Full trading rules and source paper details require Quantpedia Premium access. The implementation notes above are based on the strategy name and available transforms.
