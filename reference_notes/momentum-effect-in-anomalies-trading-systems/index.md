# Momentum Effect in Anomalies/Trading Systems

**Quantpedia ID**: #0017
**URL**: https://quantpedia.com/strategies/momentum-effect-in-anomalies-trading-systems
**Status**: ELIGIBLE (with factor ETF proxy)
**Linear Issue**: [ENG-32](https://linear.app/epoch-inc/issue/ENG-32/implement-momentum-effect-in-anomaliestrading-systems-0017)

## Overview
A meta-strategy that applies momentum to the selection of trading anomalies/factors. Instead of applying momentum to stocks, this strategy applies momentum to the performance of published anomalies, selecting the best performing strategy from the past 2 years to trade in the following year. This is essentially "factor momentum" or "factor rotation."

## Trading Rules
**Universe**: Published equity anomalies/trading strategies (QC uses Quantpedia data)
**Signal**: 2-year cumulative return of each anomaly's equity curve
**Selection**: Invest 100% in the best performing anomaly from past 2 years
**Weighting**: 100% allocation to single best performer
**Rebalancing**: Yearly (January)

### Original Implementation
The QC implementation uses Quantpedia's proprietary equity curve data for each published strategy.

### Factor ETF Proxy Implementation
Use factor ETFs as proxies for different anomalies:
| Factor | ETF | Description |
|--------|-----|-------------|
| Momentum | MTUM | iShares MSCI USA Momentum Factor |
| Value | VLUE | iShares MSCI USA Value Factor |
| Quality | QUAL | iShares MSCI USA Quality Factor |
| Size | SIZE | iShares MSCI USA Size Factor |
| Low Volatility | USMV | iShares MSCI USA Min Vol Factor |
| Wide Moat | MOAT | VanEck Morningstar Wide Moat |
| Dividend Growth | DGRO | iShares Core Dividend Growth |
| Buyback | PKW | Invesco Buyback Achievers |
| Momentum (small cap) | DWAS | Invesco DWA SmallCap Momentum |

## Fundamental Reason
- **Anomaly persistence**: Published anomalies don't vanish immediately after publication
- **Investor slow adaptation**: Investors are slow to incorporate information about anomalies
- **Momentum in factors**: Factor returns exhibit positive autocorrelation
- **Regime dependence**: Different factors work in different market regimes

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1972-2008 |
| Return | 13.76% p.a. |
| Volatility | Not stated |
| Max Drawdown | -33.28% |
| Sharpe Ratio | Not stated |

**Note**: Market benchmark return was 9.49% during same period.

**OOS Performance (2011-2025)**:
- Return: 4.8% p.a.
- Volatility: 22.3%
- Sharpe: 0.22
- Max DD: -40.0%

## Source Paper
**Huang: "Real-Time Profitability of Published Anomalies: An Out-of-Sample Test"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1571706

**Abstract**: Empirical evidence on the out-of-sample performance of asset-pricing anomalies is mixed so far and arguably is often subject to data-snooping bias. This paper proposes a method that can significantly reduce this bias. Specifically, we consider a long-only strategy that involves only published anomalies and non-forward-looking filters and that each year recursively picks the best past-performer among such anomalies over a given training period. We find that this strategy can outperform the equity market even after transaction costs. Overall, our results suggest that published anomalies persist even after controlling for data-snooping bias.

## Other Papers
- Ehsani: "Factor Momentum and the Momentum Factor" (SSRN 3014521)
- Zaremba, Shemer: "Is there Momentum in Factor Premia?" (SSRN 3332927)
- Geczy, Samonov: "215 Years of Global Multi-Asset Momentum: 1800-2014" (SSRN 2607730)

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/momentum-effect-in-anomalies-trading-systems/
#
# Uses Quantpedia's proprietary equity curve data for each strategy
# Investment universe: Quantpedia's equity long-short anomalies
# Signal: 2-year momentum on strategy equity curves
# Selection: Best performing strategy from past 2 years
# Rebalance: Yearly (January)

class MomentumEffectinAnomaliesTradingSystems(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetCash(100_000)

        self.backtest_to = {}
        self.perf = {}
        self.period = 2 * 12 * 21  # 2 years of trading days

        # Load Quantpedia strategy data
        csv_string_file = self.Download('data.quantpedia.com/backtesting_data/equity/quantpedia_strategies/backtest_end_year.csv')
        lines = csv_string_file.split('\r\n')

        for line in lines[1:]:
            split = line.split(';')
            id = str(split[0])
            backtest_to = int(split[1])

            data = self.AddData(QuantpediaEquity, id, Resolution.Daily)
            data.SetLeverage(5)
            self.backtest_to[id] = backtest_to
            self.perf[id] = self.ROC(id, self.period, Resolution.Daily)

        self.recent_month = -1

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        if self.Time.month == self.recent_month:
            return
        self.recent_month = self.Time.month

        if self.Time.month != 1:  # Only rebalance in January
            return

        # Calculate performance of published strategies
        performance = {
            x: self.perf[x].Current.Value for x in self.perf
            if self.perf[x].IsReady and self.backtest_to[x] < self.Time.year
        }

        if len(performance) != 0:
            sorted_by_perf = sorted(performance.items(), key=lambda x: x[1], reverse=True)
            top_performer_id = sorted_by_perf[0][0]

            if not self.Portfolio[top_performer_id].Invested:
                self.Liquidate()
                self.SetHoldings(top_performer_id, 1)
        else:
            self.Liquidate()
```

## Eligibility Check

### Available
**Factor ETFs (for proxy implementation)**:
- MTUM-Stocks (Momentum)
- VLUE-Stocks (Value)
- QUAL-Stocks (Quality)
- SIZE-Stocks (Size)
- USMV-Stocks (Low Volatility)
- MOAT-Stocks (Wide Moat)
- PKW-Stocks (Buyback)
- PDP-Stocks (Momentum)
- DWAS-Stocks (Small Cap Momentum)
- SPHQ-Stocks (Quality)
- PRF-Stocks (Fundamental)

**Transforms**:
- `roc(period=504)` - 2-year rate of change
- `cs_rank(ascending=False)` - Cross-sectional ranking
- `cs_select(quantile=N, select_quantile=N)` - Select top performer

### Implementation Considerations
**Original Strategy Requirements**:
- Quantpedia's proprietary equity curve data for each published anomaly
- This data is NOT available on Epoch platform

**Proxy Implementation**:
Use factor ETFs as proxies. This captures "factor momentum" concept but differs from original:
1. Factor ETFs may not perfectly replicate academic anomalies
2. Limited number of factors vs. dozens of anomalies in original
3. ETF inception dates limit lookback period

### Implementation Approach (Factor ETF Proxy)
```python
# Define universe of factor ETFs
factor_etfs = ['MTUM', 'VLUE', 'QUAL', 'SIZE', 'USMV', 'MOAT', 'PKW', 'DWAS']

# Get price data
price = market_data_source(timeframe=1D)().c

# Calculate 2-year momentum for each factor
momentum_2y = roc(period=504)(price)

# Rank factors by momentum
factor_rank = cs_rank(ascending=False)(momentum_2y)

# Select top performer (100% allocation)
top_factor = cs_select(quantile=len(factor_etfs), select_quantile=len(factor_etfs))(momentum_2y)

# Weight: 100% to top performer
weight = equal_weight()(active_mask=top_factor)

# Yearly rebalance in January
is_january = time_feature(component=TimeFeature.month)() == 1
is_new_year = time_feature(component=TimeFeature.year)().changed()
rebalance_trigger = is_january & is_new_year

position_size(type="percent")(size=weight * 100, rebalance_on=rebalance_trigger)
```

## Implementation Notes
- Original uses Quantpedia's proprietary anomaly equity curves
- Proxy implementation uses factor ETFs (MTUM, VLUE, QUAL, etc.)
- Factor ETF approach is simpler but may not capture all anomalies
- Single concentrated bet (100% in one factor) is high risk
- Consider diversifying to top 2-3 factors instead of just top 1
- Very low turnover (yearly rebalance)

## Risk Considerations
- **Concentration risk**: 100% allocation to single factor
- **Regime changes**: Factor that worked last 2 years may not work next year
- **Factor crowding**: Popular factors may become overcrowded
- **Implementation gap**: Factor ETFs may not perfectly replicate anomalies
- **Limited diversification**: Only 8-10 factor ETFs vs. dozens of anomalies

## Alternative Implementations
1. **Top 3 factors**: Spread allocation across top 3 performing factors
2. **Momentum + Value**: Combine factor momentum with value screening
3. **Dynamic allocation**: Use momentum strength to size positions
4. **Risk parity**: Weight by inverse volatility rather than equal weight

## Comparison Notes
This is a **factor allocation/rotation** strategy applying momentum to factor selection. Related strategies:
- #0001 Asset Class Trend-Following (momentum applied to asset classes)
- #0015 Momentum Factor Effect in Country Equity Indexes (momentum applied to countries)
- Factor momentum literature (Ehsani, Gupta, etc.)
