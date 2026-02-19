---
url: https://quantpedia.com/how-to-build-mean-reversion-strategies-in-currencies/
title: How to Build Mean Reversion Strategies in Currencies
domain: quantpedia
crawled_at: 2026-02-01T12:00:00Z
---

# How to Build Mean Reversion Strategies in Currencies

**25 October 2024**

Tags: currency investing, factor investing, forex system, FX anomaly, own-research, reversal, smart beta

## Introduction

Mean reversion is a fundamental concept in financial markets that suggests asset prices and returns eventually move back toward their historical average or mean level over time. This phenomenon can be observed across various asset classes, including equities, commodities, and currencies – particularly in currency pairs within FX markets.

Instead of solely focusing on spot exchange rates, it is often more beneficial to use FX futures for analyses. **The reason for this is that FX futures continuous data series incorporate the interest rate differentials between currencies, automatically including the carry return.** If we rely solely on spot rates, such as EUR/USD, we would need to manually calculate and adjust for swap points to account for the costs or benefits of holding a higher-yielding currency against a lower-yielding one.

By analyzing a basket of currencies, we can calculate an average exchange rate and identify which currencies have deviated significantly from this mean. Those that move too far from the mean have a tendency to revert, creating an opportunity to buy undervalued currencies and short overvalued ones, which is in line with the natural mean-reverting tendency of FX pairs.

**Hypothesis:** If we construct a simple strategy that goes long on undervalued currencies and short on overvalued ones, we will generate excess returns that exceed average expected returns, regardless of market movements or the benchmark. In other words, we aim to achieve pure alpha performance.

## Strategy Analysis

For this strategy, we used daily adjusted prices of FX futures traded on derivatives exchanges:
- AD1 (futures on the Australian Dollar)
- BF1 (futures on the British Pound)
- CD1 (futures on the Canadian Dollar)
- EC1 (futures on the Euro)
- SF1 (futures on the Swiss Franc)
- JY1 (futures on the Japanese Yen)

We are using the continuous futures for our analysis. The dataset covers the period from February 13, 2007 to September 5, 2024, during which only the last available price of each month was selected for the subsequent analyses.

In the first step, we calculated the cumulative return of each FX future on the last trading day of the month and created an "average futures" series, that's used over the course of the analysis as an anchor towards which all individual continuous FX futures tend to mean revert.

**Figure 1:** Cumulative return for individual continuous futures and their average, from 2007 to 2024.

If an individual FX future exceeded the average (it's an overvalued currency), we went short; otherwise, if it was below the average (it's an undervalued currency), we went long.

## Position Sizing Methods

### Linear Position Sizing

In linear position sizing, we used the difference between the given continuous futures series and the average futures series as the weight for the short/long position. For example, if the continuous futures series of a currency is 20% higher (20% lower) than the average of all futures series, then we go short 20% of the currency (go 20% long), and so on.

### Exponential Position Sizing

In the exponential approach, we also utilized the difference between the individual continuous futures and the average data series, but this time, the weight for the short/long position is set in the exponential style:
- 20% deviation → 40% position
- 30% deviation → 90% position
- 40% deviation → 160% position

## Performance Comparison

| Metric | Linear | Exponential |
|--------|--------|-------------|
| Performance | Low | High |
| Std Dev | Low | Higher |
| Max DD | Small | Deeper |
| Sharpe Ratio | 0.12 | 0.35 |
| Calmar Ratio | 0.05 | Higher |

The linear strategy appears stable, with insignificant drawdowns but no tendency to grow. The value of the linear strategy portfolio has fluctuated around 1.1 for 10 years.

**On the other hand, the trading strategy with the exponential position sizing portfolio delivers attractive positive excess returns with a Sharpe ratio of 0.35.**

## Conclusion

The mean reversion behavior is a well-utilizable feature in many fields of the investing world, and as we have observed, it also applies to currency FX futures. By leveraging this property, we can build a profitable strategy, particularly in combination with the exponential position sizing method.

However, nothing is free, and there is a risk that its application could create uncontrollable leverage. Our exponential position sizing doesn't have excessively high total leverage (450% in the maximum point), so if smart risk management is used, the simple mean reversion strategies in currencies can be used as a diversifier or source of an additional uncorrelated return in the broader multi-asset multi-strategy portfolio.
