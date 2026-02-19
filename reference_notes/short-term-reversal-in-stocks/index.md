# Short Term Reversal Effect in Stocks

**Quantpedia ID**: #0013
**URL**: https://quantpedia.com/strategies/short-term-reversal-in-stocks
**Status**: ELIGIBLE
**Linear Issue**: [ENG-28](https://linear.app/epoch-inc/issue/ENG-28/implement-quantpedia-strategy-0013-short-term-reversal-effect-in)

## Overview
Classic short-term reversal strategy that exploits the tendency of stocks to mean-revert over weekly horizons. Based on the well-documented phenomenon that last week's losers tend to outperform last week's winners in the subsequent week. This strategy captures returns from investor overreaction and liquidity provision.

## Trading Rules
**Universe**: 100 biggest US companies by market capitalization

**Signal**: Weekly return (prior week performance)

**Selection**:
- Long: 10 stocks with lowest weekly performance (biggest losers)
- Short: 10 stocks with highest weekly performance (biggest winners)

**Weighting**: Equal weight within long/short legs

**Rebalancing**: Weekly

## Fundamental Reason
1. **Investor Overreaction**: Short-term price movements often overshoot due to behavioral biases, creating predictable reversals.

2. **Liquidity Provision**: Reversal strategies effectively provide liquidity by buying oversold stocks and selling overbought ones.

3. **Bid-Ask Bounce**: Part of the reversal effect comes from bid-ask bounce, where prices oscillate between bid and ask prices.

4. **Market Microstructure**: Short-term price impact of large trades creates temporary mispricings that revert.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1990-2009 |
| Return | 16.25% p.a. |
| Volatility | 14.94% |
| Max Drawdown | -52.94% |
| Sharpe Ratio | 1.09 |

## Out-of-Sample Performance (Quantpedia)
| Metric | Value |
|--------|-------|
| Period | 2000-2025 |
| Return | 16.1% p.a. |
| Volatility | 24.92% |
| Max Drawdown | -46.56% |
| Sharpe Ratio | 0.65 |

**Note**: OOS Sharpe ratio has declined from 1.09 to 0.65, consistent with strategy becoming more crowded over time.

## Source Paper
**Short Term Reversal**
- Authors: Jegadeesh, Titman (original academic documentation)
- Based on "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency"
- Key Finding: Stocks exhibit negative serial correlation at weekly frequencies, allowing profitable contrarian strategies.

## Eligibility Check

### ELIGIBLE

All required components are available in the platform:

| Component | Required | Platform Capability | Status |
|-----------|----------|---------------------|--------|
| Stock Universe | 100 largest by market cap | 13,000+ stocks available | ✅ |
| Weekly Returns | `roc(5)` or similar | `roc` transform | ✅ |
| Bottom 10 Selection | Worst performers | `cs_select(direction=bottom, k=10)` | ✅ |
| Top 10 Selection | Best performers | `cs_select(direction=top, k=10)` | ✅ |
| Equal Weighting | Per leg | `equal_weight` transform | ✅ |
| Weekly Rebalancing | Every week | Supported timeframe | ✅ |

### Implementation Approach

```
# Universe: 100 largest stocks by market cap
# (Configured in study definition asset selection)

# Calculate weekly returns
weekly_return = roc(close, 5)

# Long leg: bottom 10 performers (biggest losers)
long_signal = cs_select(weekly_return, direction=bottom, k=10)

# Short leg: top 10 performers (biggest winners)
short_signal = cs_select(weekly_return, direction=top, k=10)

# Combined signal: +1 for long, -1 for short
signal = if(long_signal, 1, if(short_signal, -1, 0))

# Equal weight within each leg
weight = equal_weight(signal)
```

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/short-term-reversal-in-stocks/
#
# The investment universe consists of 100 biggest companies by market
# capitalization. At the beginning of each week, the investor goes long
# on the ten stocks with the lowest performance in the previous week and
# short on the ten stocks with the highest performance in the previous week.
#
# QC changes:
# - Universe consists of 100 stocks with highest market capitalization from
#   NYSE, NASDAQ, and AMEX.
# - Price is adjusted by the SPY price when sorting is performed.

#region imports
from AlgorithmImports import *
import numpy as np
#endregion

class ShortTermReversalEffectinStocks(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetCash(100000)

        # Daily price data.
        self.data:dict = {}
        self.period:int = 5
        self.leverage:int = 5
        self.traded_count:int = 10

        self.spy:Symbol = self.AddEquity('SPY', Resolution.Daily).Symbol
        self.data[self.spy] = RollingWindow[float](self.period)

        self.fundamental_count:int = 100
        self.fundamental_sorting_key = lambda x: x.MarketCap

        self.week:int = -1
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.FundamentalSelectionFunction)
        self.Settings.MinimumOrderMarginPortfolioPercentage = 0.
        self.settings.daily_precise_end_time = False

    def FundamentalSelectionFunction(self, fundamental: List[Fundamental]) -> List[Symbol]:
        if self.week == self.Time.isocalendar()[1]:
            return Universe.Unchanged
        self.week = self.Time.isocalendar()[1]

        selected:List[Fundamental] = [x for x in fundamental if x.HasFundamentalData and x.MarketCap > 0]
        selected = [x for x in sorted(selected, key=self.fundamental_sorting_key, reverse=True)[:self.fundamental_count]]

        for stock in selected:
            symbol:Symbol = stock.Symbol
            if symbol not in self.data:
                self.data[symbol] = RollingWindow[float](self.period)
                history = self.History(symbol, self.period, Resolution.Daily)
                if history.empty:
                    self.Log(f"Not enough data for {symbol} yet")
                    continue
                closes = history.loc[symbol].close
                for time, close in closes.items():
                    self.data[symbol].Add(close)

        return [x.Symbol for x in selected]

    def OnSecuritiesChanged(self, changes: SecurityChanges) -> None:
        for security in changes.AddedSecurities:
            security.SetFeeModel(CustomFeeModel())
            security.SetLeverage(self.leverage)

    def OnData(self, data: Slice) -> None:
        # Update rolling windows.
        for symbol, rolling_window in self.data.items():
            if symbol in data and data[symbol]:
                rolling_window.Add(data[symbol].Close)

        if self.week == self.Time.isocalendar()[1]:
            return

        # Make sure SPY data is ready.
        if not self.data[self.spy].IsReady:
            return

        perf = {}
        for symbol, rolling_window in self.data.items():
            # Skip SPY.
            if symbol == self.spy:
                continue

            if rolling_window.IsReady:
                closes_list:List = list(rolling_window)
                # Performance calculation.
                current_price:float = closes_list[0]
                last_weeks_price:float = closes_list[-1]

                # Divide by index.
                spy_closes_list:List = list(self.data[self.spy])
                current_spy_price:float = spy_closes_list[0]
                last_weeks_spy_price:float = spy_closes_list[-1]

                perf[symbol] = (current_price/current_spy_price) / (last_weeks_price/last_weeks_spy_price) - 1

        # Long and short sorting.
        if len(perf) >= self.traded_count * 2:
            sorted_by_perf:List = [x[0] for x in sorted(perf.items(), key=lambda x: x[1])]
            long:List = sorted_by_perf[:self.traded_count]
            short:List = sorted_by_perf[-self.traded_count:]

            # Trade execution.
            invested:List = [x.Key for x in self.Portfolio if x.Value.Invested]
            for symbol in invested:
                if symbol not in long + short + [self.spy]:
                    self.Liquidate(symbol)

            for symbol in long:
                self.SetHoldings(symbol, 1 / len(long))
            for symbol in short:
                self.SetHoldings(symbol, -1 / len(short))

# Custom fee model.
class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters):
        fee = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))
```

## Implementation Notes

1. **Universe Selection**: Use market cap ranking to select top 100 stocks. Platform supports this via study definition.

2. **SPY-Adjusted Returns**: The QC code adjusts stock returns by SPY to capture relative performance. This can be implemented using:
   ```
   relative_return = roc(close, 5) - roc(spy_close, 5)
   ```

3. **Weekly Rebalancing**: Strategy trades once per week at market open.

4. **Leverage**: QC implementation uses 5x leverage for both long and short legs.

5. **Transaction Costs**: Strategy is turnover-intensive (weekly rebalancing of 20 positions). Consider transaction cost impact.

## Risk Considerations

- **High Turnover**: Weekly rebalancing creates significant transaction costs
- **Crowding Risk**: Strategy is well-known, may be less profitable when crowded
- **Short Squeeze Risk**: Shorting recent winners can be painful during momentum runs
- **Drawdowns**: -52.94% max drawdown in paper, -46.56% OOS

## Related Research
- Jegadeesh (1990): "Evidence of Predictable Behavior of Security Returns"
- Lehmann (1990): "Fads, Martingales, and Market Efficiency"
- De Bondt & Thaler (1985): "Does the Stock Market Overreact?"
- Lo & MacKinlay (1990): "When Are Contrarian Profits Due to Stock Market Overreaction?"
