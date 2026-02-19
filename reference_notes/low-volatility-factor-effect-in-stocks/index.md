# Low Volatility Factor Effect in Stocks

**Quantpedia ID**: #0007
**URL**: https://quantpedia.com/strategies/low-volatility-factor-effect-in-stocks
**Status**: ELIGIBLE
**Linear Issue**: [ENG-19](https://linear.app/epoch-inc/issue/ENG-19/implement-low-volatility-factor-effect-in-stocks-0007)

## Overview
This anomaly-based approach exploits the empirical finding that "stocks with low volatility earn high risk-adjusted returns" compared to market benchmarks. The strategy challenges traditional CAPM by demonstrating that lower-risk securities consistently outperform without requiring leverage.

## Trading Rules
**Universe**: Global large-cap stocks (or US large-cap stocks, ~3000 stocks filtered by market cap)
**Signal**: Rank stocks by past 3-year volatility of weekly returns
**Selection**: Lowest volatility decile (D1) - approximately 50 stocks for S&P 500 universe
**Weighting**: Equal weight within decile
**Rebalancing**: Monthly
**Optional Extension**: Long-short (long D1, short D10) for 12% annual alpha spread

## Fundamental Reason
1. **Leverage Constraints**: Many investors cannot or will not use leverage needed to arbitrage away the opportunity, leaving low-volatility stocks underexploited.

2. **Benchmark-Driven Behavior**: Asset managers face incentives to tilt toward high-beta stocks to generate above-average returns, leading to overpricing of risky assets and underpricing of low-risk stocks.

3. **Behavioral Biases**: Private investors overpay for volatile stocks perceived as lottery tickets, seeking high returns in short timeframes.

4. **Market Mispricing**: Research suggests the anomaly reflects valuation inefficiencies rather than compensation for systematic risk.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1986-2006 |
| Return | 11.3% p.a. |
| Volatility | 10.1% |
| Max Drawdown | -45.92% |
| Sharpe Ratio | 0.72 |
| Alpha Spread (L/S) | 12% annually |

## Out-of-Sample Performance (Quantpedia)
| Metric | Value |
|--------|-------|
| Period | 2000-2025 |
| Return | 11.2% p.a. |
| Volatility | 14.05% |
| Max Drawdown | -44.83% |
| Sharpe Ratio | 0.80 |

## Source Paper
**The Volatility Effect: Lower Risk Without Lower Return**
- Authors: David Blitz, Pim van Vliet
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=980865
- Key Finding: "The annual alpha spread of global low versus high volatility decile portfolios amounts to 12% over the 1986-2006 period."

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/low-volatility-factor-effect-in-stocks-long-only-version/
#
# The investment universe consists of global large-cap stocks (or US large-cap stocks).
# At the end of each month, the investor constructs equally weighted decile portfolios
# by ranking the stocks on the past three-year volatility of weekly returns.
# The investor goes long stocks in the top decile (stocks with the lowest volatility).
#
# QC implementation changes:
# - Top quartile (stocks with the lowest volatility) instead of decile.

from AlgorithmImports import *
import numpy as np
from typing import List, Dict

class LowVolatilityFactorEffectStocks(QCAlgorithm):
    def Initialize(self) -> None:
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100_000)
        self.symbol: Symbol = self.AddEquity('SPY', Resolution.Daily).Symbol
        self.period: int = 12 * 21  # ~12 months daily data
        self.fundamental_count: int = 3000
        self.quantile: int = 4
        self.leverage: int = 10
        self.data: Dict[Symbol, SymbolData] = {}
        self.long: List[Symbol] = []
        self.selection_flag: bool = True
        self.UniverseSettings.Resolution = Resolution.Daily
        self.Settings.MinimumOrderMarginPortfolioPercentage = 0.
        self.settings.daily_precise_end_time = False
        self.AddUniverse(self.FundamentalSelectionFunction)
        self.Schedule.On(self.DateRules.MonthEnd(self.symbol),
                        self.TimeRules.AfterMarketOpen(self.symbol), self.Selection)

    def FundamentalSelectionFunction(self, fundamental: List[Fundamental]) -> List[Symbol]:
        # Update rolling windows daily
        for stock in fundamental:
            symbol: Symbol = stock.Symbol
            if symbol in self.data:
                self.data[symbol].update(stock.AdjustedPrice)

        if not self.selection_flag:
            return Universe.Unchanged

        # Filter US large-cap stocks
        fundamental = [x for x in fundamental if x.HasFundamentalData
                      and x.Market == 'usa' and x.MarketCap != 0]
        if len(fundamental) > self.fundamental_count:
            fundamental = sorted(fundamental, key=lambda x: x.MarketCap,
                               reverse=True)[:self.fundamental_count]

        # Calculate weekly volatility for each stock
        weekly_vol: Dict[Symbol, float] = {}
        for stock in fundamental:
            symbol = stock.Symbol
            if symbol not in self.data:
                self.data[symbol] = SymbolData(self.period)
            # Warmup with history if needed
            if self.data[symbol].is_ready():
                weekly_vol[symbol] = self.data[symbol].volatility()

        if len(weekly_vol) >= self.quantile:
            # Sort by volatility (ascending) and select lowest quartile
            sorted_by_vol = sorted(weekly_vol.items(), key=lambda x: x[1], reverse=True)
            quantile = int(len(sorted_by_vol) / self.quantile)
            self.long = [x[0] for x in sorted_by_vol[-quantile:]]  # Lowest vol

        return self.long

    def OnData(self, data: Slice) -> None:
        if not self.selection_flag:
            return
        self.selection_flag = False

        # Liquidate positions not in selection
        invested = [x.Key for x in self.Portfolio if x.Value.Invested]
        for symbol in invested:
            if symbol not in self.long:
                self.Liquidate(symbol)

        # Equal weight new positions
        for symbol in self.long:
            if symbol in data and data[symbol]:
                self.SetHoldings(symbol, 1. / len(self.long))

        self.long.clear()

class SymbolData():
    def __init__(self, period: int) -> None:
        self.price: RollingWindow = RollingWindow[float](period)

    def update(self, value: float) -> None:
        self.price.Add(value)

    def is_ready(self) -> bool:
        return self.price.IsReady

    def volatility(self) -> float:
        closes = [x for x in self.price]
        # Weekly volatility calculation
        separate_weeks = [closes[x:x+5] for x in range(0, len(closes), 5)]
        weekly_returns = [(x[0] - x[-1]) / x[-1] for x in separate_weeks]
        return np.std(weekly_returns)
```

## Eligibility Check
### Available
**Transforms:**
- `volatility(close, period=156)` - Annualized Historical Volatility (3-year = 156 weeks on weekly data)
- `cs_rank(ascending=true)` - Cross-Sectional Rank (lowest volatility gets rank 1)
- `cs_select(direction=bottom, mode=percent, k=10)` - Select bottom 10% (lowest volatility decile)

**Assets:**
- Individual stocks available: AAPL-Stocks, MSFT-Stocks, GOOGL-Stocks, etc.
- Low vol ETF proxies: SPLV-Stocks, USMV-Stocks
- Broad market: SPY-Stocks, IWM-Stocks

### Missing
None - all required components available.

## Implementation Notes
1. **Timeframe**: Use weekly bars for volatility calculation (or daily with weekly aggregation)
2. **Lookback**: 156 weeks (3 years) for volatility calculation
3. **Signal Logic**:
   - Calculate `volatility(close, 156)` for each stock
   - Apply `cs_rank(volatility, ascending=true)` to rank by volatility (lowest = rank 1)
   - Apply `cs_select(rank, direction=bottom, mode=percent, k=10)` to select bottom decile
4. **Position Management**: Equal weight across selected stocks (~50 positions for S&P 500)
5. **Rebalance Trigger**: Monthly at month-end
6. **Universe Considerations**:
   - Minimum of 100+ stocks needed for decile portfolios
   - Filter for liquidity (market cap > threshold)
   - QC implementation uses top 3000 by market cap, then quartile selection

## ETF Implementation Alternative
For simplified implementation without individual stock selection:
- SPLV (Invesco S&P 500 Low Volatility ETF)
- USMV (iShares MSCI USA Min Vol Factor ETF)

## Related Research
- Effect persists across US, European, and Japanese markets independently
- Not explained by value or size factors
- Low turnover due to long-term volatility measurement (~30% annual)
- Partial crisis hedge - low-vol stocks typically outperform in downturns
- Concerns about high valuations when factor becomes popular
