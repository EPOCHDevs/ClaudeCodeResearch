# 12 Month Seasonal Reversals

**Quantpedia ID**: #0413
**URL**: https://quantpedia.com/strategies/12-month-seasonal-reversals
**Status**: ELIGIBLE
**Linear Issue**: [ENG-198](https://linear.app/epoch-inc/issue/ENG-198/implement-12-month-seasonal-reversals-0413)

## Overview
This strategy exploits seasonal reversals in stock returns. Stocks that have historically high returns in a particular calendar month tend to have low returns in the other 11 months (and vice versa). The strategy sorts stocks by their average "other-calendar-month" returns and goes long stocks with low other-month returns while shorting those with high other-month returns.

## Trading Rules
**Universe**: Stocks on NYSE, AMEX, NASDAQ (ordinary common shares only)

**Signal**: Average other-calendar-month returns
1. At month t, compute each stock's average return in all months EXCEPT month t
2. Use last 20 years of data for formation
3. Example: In January, compute average of Feb-Dec returns over past 20 years

**Selection**:
1. Sort stocks into six portfolios by average other-calendar-month returns
2. Long two lowest-average portfolios
3. Short two highest-average portfolios

**Weighting**: Value-weighted
**Rebalancing**: Monthly

## Fundamental Reason
Return seasonalities (stocks outperforming in specific months) are balanced by seasonal reversals. If a stock outperforms in one particular month, its returns during remaining months must be below the excess return of that outperforming month. This "adding-up" constraint holds because:

1. Seasonalities likely caused by temporary mispricing rather than seasonal variation in risk
2. Risk-based explanations don't require seasonalities to add up to zero
3. Mispricing from traders systematically trading in same direction at same times causes price deviations
4. Seasonal reversals occur when temporary price deviations subside

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1963-2016 |
| Return | 5.54% p.a. |
| Volatility | 8.07% |
| Max Drawdown | -35.87% |
| Sharpe Ratio | 0.19 |

Note: Data from Table 7, Panel A, NANN factor, annualized monthly return (0.45%).

**WARNING**: Quantpedia rates confidence as "Moderate" - OOS backtest shows slightly negative performance.

## Source Paper
Keloharju, Matti and Linnainmaa, Juhani T. and Nyberg, Peter Mikael: Seasonal Reversals in Expected Stock Returns
- SSRN: https://ssrn.com/abstract=3276334

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238552/

## Eligibility Check
### Available
- **Transforms**:
  - `roc` - Monthly returns calculation
  - `month_of_year` - Calendar month extraction
  - `cs_rank` - Cross-sectional ranking for sextile sorting
  - `sma` / `rolling_mean` - For averaging returns over 20 years
  - `market_cap` - For value-weighting
- **Assets**: US Stocks available (NYSE, AMEX, NASDAQ universe)

### Formula
```
For each stock i at month t:
  other_month_avg[i] = mean(returns[i, all months except t] over past 20 years)

Long: Bottom 2 sextiles (low other_month_avg)
Short: Top 2 sextiles (high other_month_avg)
```

## Implementation Notes
- Strategy is marked ELIGIBLE with all required transforms and assets available
- Confidence rating: Moderate (OOS shows slightly negative performance)
- Complexity: Complex (requires 20-year lookback and calendar month grouping)
- Monthly rebalancing is straightforward
- Strongly negative correlation with equity market - can serve as hedge
- Distinct from long-term reversals despite superficial similarity
- Can be combined with same-month seasonality for enhanced strategy

