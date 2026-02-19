# Liquidity Effect in Stocks

**Quantpedia ID**: #0018
**URL**: https://quantpedia.com/strategies/liquidity-effect-in-stocks
**Status**: ELIGIBLE
**Linear Issue**: [ENG-33](https://linear.app/epoch-inc/issue/ENG-33/implement-quantpedia-strategy-0018-liquidity-effect-in-stocks)

## Overview
Liquidity factor strategy that exploits the illiquidity premium in equities. Less liquid stocks (low turnover) tend to outperform more liquid stocks (high turnover) because investors require compensation for holding assets that are harder to trade. The strategy focuses on the smallest market cap quartile where the liquidity effect is strongest.

## Trading Rules
**Universe**: Top 3,500 US stocks by market cap (NYSE, AMEX, NASDAQ)
- Price >= $2
- Market cap >= $10 million
- Excludes: REITs, warrants, ADRs, ETFs, closed-end funds

**Filtering**:
1. Divide stocks into quartiles by market capitalization
2. Select lowest market cap quartile (smallest 875 stocks)
3. Within that quartile, divide by annual turnover (shares traded / shares outstanding)

**Signal**: 12-month turnover (cumulative volume / shares outstanding)

**Selection**:
- Long: Lowest turnover quartile (least liquid)
- Short: Highest turnover quartile (most liquid)

**Weighting**: Equal weight

**Rebalancing**: Yearly (December)

## Fundamental Reason
1. **Illiquidity Premium**: Less liquid assets are discounted in price because investors require compensation for the difficulty of trading. This creates higher expected returns for illiquid stocks.

2. **Transaction Cost Risk**: Illiquid stocks have higher bid-ask spreads and price impact, creating a risk that investors are compensated for bearing.

3. **Independent Risk Factor**: Academic research (Ibbotson, Chen, Hu) shows liquidity is an independent factor alongside value, momentum, and size.

4. **Small-Cap Concentration**: The effect is strongest in small-cap stocks where liquidity differences are most pronounced.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1972-2011 |
| Return | 6.68% p.a. (alpha) |
| Volatility | 11.87% |
| Max Drawdown | -79.86% |
| Sharpe Ratio | 0.56 |

**Note**: Performance from small-cap liquidity factor portfolio (Table 7 of source paper).

## Out-of-Sample Performance (Quantpedia)
| Metric | Value |
|--------|-------|
| Period | 2005-2025 |
| Return | -0.8% p.a. |
| Volatility | 17.93% |
| Max Drawdown | -70.71% |
| Sharpe Ratio | -0.04 |

**WARNING**: OOS performance is negative. Strategy appears to have stopped working in the post-2005 period.

## Source Paper
**Ibbotson, Chen, Hu: "Liquidity as an Investment Style"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1817889
- Key Finding: Liquidity is an economically significant indicator of long-term returns, independent of size, value, and momentum. Low turnover stocks outperform high turnover stocks, especially in small caps.

## Other Papers
- Amihud: "Illiquidity and Stock Returns: A Revisit" (SSRN 3257038)
- Pastor, Stambaugh: "Liquidity Risk After 20 Years" (SSRN 3371948)

## Eligibility Check

### ELIGIBLE

All required components are available in the platform:

| Component | Required | Platform Capability | Status |
|-----------|----------|---------------------|--------|
| Market Cap | Quartile ranking | `finance_ratio(ratio_type=market_cap)` | ✅ |
| Shares Outstanding | For turnover calc | `income_statement().basic_shares` | ✅ |
| Volume | Cumulative annual | `volume` field + `sum()` | ✅ |
| Turnover Calculation | volume/shares | Arithmetic operations | ✅ |
| Quartile Selection | Top/bottom 25% | `cs_select(mode=percent, k=25)` | ✅ |
| Equal Weighting | Per leg | `equal_weight` transform | ✅ |
| Yearly Rebalancing | December | Supported timeframe | ✅ |

### Implementation Approach

```
# Step 1: Get market cap for universe ranking
market_cap = finance_ratio(ratio_type=market_cap, period=trailing_twelve_months)

# Step 2: Select bottom quartile by market cap (smallest 25%)
small_cap = cs_select(market_cap, direction=bottom, mode=percent, k=25)

# Step 3: Calculate annual turnover
shares = income_statement(period=trailing_twelve_months).basic_shares
annual_volume = sum(volume, 252)  # Rolling 252-day sum
turnover = annual_volume / shares

# Step 4: Within small-cap, select by turnover
# Long: lowest turnover quartile
long_signal = cs_select(turnover, direction=bottom, mode=percent, k=25, filter=small_cap)

# Short: highest turnover quartile
short_signal = cs_select(turnover, direction=top, mode=percent, k=25, filter=small_cap)

# Step 5: Combine signals
signal = if(long_signal, 1, if(short_signal, -1, 0))
weight = equal_weight(signal)
```

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/liquidity-effect-in-stocks/
#
# The top 3 500 companies from NYSE, AMEX and NASDAQ with the highest market
# capitalization are part of the investment universe (price >= $2, market cap
# >= $10 million; excludes REITs, warrants, ADRs, ETFs, closed-end funds).
# Stocks are divided into quartiles by market cap. Stocks from the lowest
# market-cap quartile are again divided into quartiles by turnover.
# Long: lowest turnover. Short: highest turnover.
# Rebalance yearly (December). Equal weight.
#
# QC changes:
# - Universe: 1000 most liquid stocks with price >= $5

from AlgorithmImports import *
from typing import List, Dict
import numpy as np

class LiquidityEffectinStocks(QCAlgorithm):

    def Initialize(self) -> None:
        self.SetStartDate(2005, 1, 1)
        self.SetCash(100_000)

        self.UniverseSettings.Leverage = 10
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.FundamentalSelectionFunction)
        self.Settings.MinimumOrderMarginPortfolioPercentage = 0.0
        self.settings.daily_precise_end_time = False

        self.daily_volume: Dict[Symbol, RollingWindow[float]] = {}
        self.long_symbols: List[Symbol] = []
        self.short_symbols: List[Symbol] = []
        self.selection_flag: bool = True

        self.exchange = self.AddEquity('SPY', Resolution.Daily).Symbol
        self.Schedule.On(
            self.DateRules.MonthStart(self.exchange),
            self.TimeRules.AfterMarketOpen(self.exchange),
            self.Rebalance
        )

        # Fundamental Filter Parameters
        self.exchange_codes: List[str] = ['NYS', 'NAS', 'ASE']
        self.fundamental_count: int = 1_000
        self.min_market_cap: int = 10_000_000
        self.min_price: int = 5
        self.period: int = 12 * 21
        self.turonver_quantile: int = 4
        self.market_cap_quantile: int = 4
        self.rebalancing_month: int = 12

    def FundamentalSelectionFunction(self, fundamental: List[Fundamental]) -> List[Symbol]:
        # Update rolling window every day
        for f in fundamental:
            if f.Symbol in self.daily_volume:
                self.daily_volume[f.Symbol].Add(f.Volume)

        if not self.selection_flag:
            return Universe.Unchanged

        filtered: List[Fundamental] = [
            f for f in fundamental
            if f.HasFundamentalData
            and f.MarketCap > self.min_market_cap
            and f.Price > self.min_price
            and f.SecurityReference.ExchangeId in self.exchange_codes
            and not f.CompanyReference.IsREIT
            and not f.SecurityReference.IsDepositaryReceipt
            and not np.isnan(f.EarningReports.BasicAverageShares.TwelveMonths)
            and f.EarningReports.BasicAverageShares.TwelveMonths != 0
        ]

        sorted_by_dollar_volume = sorted(
            filtered, key=lambda f: f.DollarVolume, reverse=True
        )[:self.fundamental_count]

        sorted_by_market_cap = sorted(
            sorted_by_dollar_volume, key=lambda f: f.MarketCap, reverse=True
        )

        # Warmup price rolling windows
        for security in sorted_by_market_cap:
            if security.Symbol in self.daily_volume:
                continue
            self.daily_volume[security.Symbol] = RollingWindow[float](self.period)
            history = self.History[TradeBar](security.Symbol, self.period, Resolution.Daily)
            if not history:
                continue
            for trade_bar in history:
                self.daily_volume[security.Symbol].Add(trade_bar.Volume)

        ready_data = [s for s in sorted_by_market_cap if self.daily_volume[s.Symbol].IsReady]

        # Bottom quartile by market cap
        bottom_by_market_cap = []
        if len(ready_data) >= self.market_cap_quantile:
            count = int(len(ready_data) / self.market_cap_quantile)
            bottom_by_market_cap = ready_data[-count:]

        # Calculate turnover
        turnover: Dict[Symbol, float] = {}
        for security in bottom_by_market_cap:
            sum_volume = np.sum([x for x in self.daily_volume[security.Symbol]])
            shares_outstanding = security.EarningReports.BasicAverageShares.TwelveMonths
            turnover[security.Symbol] = sum_volume / shares_outstanding

        # Select by turnover quartiles
        if len(turnover) >= self.turonver_quantile:
            sorted_by_turnover = sorted(turnover, key=turnover.get, reverse=True)
            quantile = int(len(sorted_by_turnover) / self.turonver_quantile)
            self.long_symbols = sorted_by_turnover[-quantile:]  # Lowest turnover
            self.short_symbols = sorted_by_turnover[:quantile]  # Highest turnover

        return self.long_symbols + self.short_symbols

    def OnData(self, slice: Slice) -> None:
        if not self.selection_flag:
            return
        self.selection_flag = False

        invested = [x.Key for x in self.Portfolio if x.Value.Invested]
        for symbol in invested:
            if symbol not in self.long_symbols + self.short_symbols:
                self.Liquidate(symbol)

        for i, portfolio in enumerate([self.long_symbols, self.short_symbols]):
            for symbol in portfolio:
                if slice.ContainsKey(symbol) and slice[symbol] is not None:
                    self.SetHoldings(symbol, ((-1) ** i) / len(portfolio))

        self.long_symbols.clear()
        self.short_symbols.clear()

    def Rebalance(self) -> None:
        if self.Time.month == self.rebalancing_month:
            self.selection_flag = True

    def OnSecuritiesChanged(self, changes: SecurityChanges) -> None:
        for security in changes.AddedSecurities:
            security.SetFeeModel(CustomFeeModel())


class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters: OrderFeeParameters) -> OrderFee:
        fee = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))
```

## Implementation Notes

1. **Two-Stage Filtering**: First filter by market cap (bottom quartile), then by turnover within that subset.

2. **Turnover Calculation**: `turnover = sum(volume, 252) / shares_outstanding`. Requires fundamental data for shares.

3. **Small-Cap Focus**: Strategy works best in small caps where liquidity differences are most pronounced.

4. **Annual Rebalancing**: Only rebalance in December. Very low turnover strategy.

5. **Large Universe**: Up to ~500 stocks per leg (depends on universe size).

## Risk Considerations

- **NEGATIVE OOS PERFORMANCE**: Strategy shows -0.8% return since 2005. May no longer work.
- **Small-Cap Risk**: Concentrated in smallest, least liquid stocks
- **High Drawdown**: -79.86% max drawdown reflects small-cap and crisis exposure
- **Execution Risk**: Illiquid stocks may be hard to trade at scale
- **Market Impact**: Large positions in illiquid stocks can move prices

## Strategy Health Warning
The OOS Sharpe of -0.04 suggests this strategy has experienced significant alpha decay or regime change. Consider:
- Reduced allocations
- Additional filters (quality, momentum overlay)
- Alternative liquidity measures (Amihud illiquidity ratio)
