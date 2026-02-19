# Using Baltic Dry Index to Trade Tanker Shipping Companies

**Quantpedia ID**: #0416
**URL**: https://quantpedia.com/strategies/using-baltic-dry-index-to-trade-tanker-shipping-companies
**Status**: INELIGIBLE
**Linear Issue**: [ENG-234](https://linear.app/epoch-inc/issue/ENG-234/feature-request-baltic-tanker-index-data-for-0416)

## Overview
This strategy trades a portfolio of tanker shipping stocks using the Baltic Tanker Index as a timing signal. The cointegrating relationship between freight rates and shipping stock returns allows for a market timing strategy using a simple moving average crossover on the Baltic Tanker Index.

## Trading Rules
**Universe**: 4 tanker shipping stocks
- DHT Holdings
- Teekay Corporation
- Tsakos Energy Navigation
- Capital Product Partners

**Signal**: Moving average crossover on Baltic Tanker Index
1. Compute BT(t) = natural log of Baltic Tanker Index
2. Calculate MA(1) = 1-week moving average (short-term)
3. Calculate MA(6) = 6-week moving average (long-term)
4. Buy signal when MA(1) > MA(6)
5. Sell signal when MA(1) < MA(6)

**Selection**:
- Long portfolio of 4 tanker stocks when buy signal
- Exit/cash when sell signal

**Weighting**: Equally-weighted
**Rebalancing**: On signal change

## Fundamental Reason
Freight rates are the predominant factor affecting the performance of shipping companies. From a financial accounting perspective, freight rates largely determine the income received by shipping companies. The Baltic Tanker Index and tanker shipping stock portfolios share a cointegrating relationship in the long run. A trading strategy based on this close association between freight rates and stock returns can be profitable.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2013-2017 |
| Return | 3.86% p.a. |
| Volatility | Not stated |
| Max Drawdown | Not stated |
| Sharpe Ratio | Not stated |

Note: Data from text, page 6. Annualized from 19.5% over 4.7 years.

**WARNING**: Quantpedia rates confidence as "Moderate" - OOS backtest shows slightly negative performance.

## Source Paper
Michail, Nektarios and Melas, Konstantinos: A Cointegrating Stock Trading Strategy for Tanker Shipping Companies
- SSRN: https://ssrn.com/abstract=3275126

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810852/

## Eligibility Check
### Available
- **Transforms**:
  - `sma` - Moving average calculation
  - `log` - Natural logarithm
- **Assets**:
  - DHT-Stocks (DHT Holdings)
  - Teekay Tankers
  - Tsakos Energy Navigation

### Missing
- **Baltic Tanker Index** - NOT AVAILABLE
  - Requires daily Baltic Tanker Index (BTI) data
  - Published by Baltic Exchange
  - Not available in standard market data feeds
- **Capital Product Partners (CPLP)** - NOT FOUND
  - One of the 4 required stocks

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing Baltic Tanker Index data
- Confidence rating: Moderate (OOS shows slightly negative performance)
- Complexity: Simple
- Even if data available, Quantpedia recommends using as long-only (not long-short)
- Alternative data required: Baltic Exchange freight rate indices
- Potential data sources: Baltic Exchange, Bloomberg

