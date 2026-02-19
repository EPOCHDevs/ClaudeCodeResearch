# Stock Return Reversal within Industries

**Quantpedia ID**: #0011
**URL**: https://quantpedia.com/strategies/stock-return-reversal-within-industries
**Status**: ELIGIBLE
**Linear Issue**: [ENG-23](https://linear.app/epoch-inc/issue/ENG-23/implement-stock-return-reversal-within-industries-0011)

## Overview
This strategy exploits intra-industry short-term reversal - the tendency for stocks that underperform their industry peers to subsequently outperform, and vice versa. By ranking stocks within industries rather than across the entire market, the reversal signal becomes stronger and more robust.

## Trading Rules
**Universe**: US stocks with price >= $3, divided into 24 industries

**Signal**:
- At month-end, rank stocks by their monthly return WITHIN each industry
- Identify top 20% (winners) and bottom 20% (losers) in each industry

**Position**:
- Long: Equal-weight portfolio of loser stocks (bottom 20%) across all industries
- Short: Equal-weight portfolio of winner stocks (top 20%) across all industries

**Weighting**: Equal weight within long and short portfolios
**Rebalancing**: Monthly

## Fundamental Reason
1. **Investor Overreaction**: Investors overreact to past information, creating temporary price dislocations that correct over short horizons.

2. **Industry-Level Focus**: Stocks in the same industry share common fundamental drivers (supply/demand, macro, regulatory). This makes intra-industry comparison more meaningful and strengthens the reversal effect.

3. **Liquidity Provision**: Reversal strategies effectively provide liquidity by buying stocks that have been oversold and selling stocks that have been overbought within their peer groups.

4. **Reduced Sector Exposure**: By operating within industries, the strategy maintains sector-neutral exposure, reducing systematic risk.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1968-2010 |
| Return | 16.78% p.a. |
| Volatility | 12.91% |
| Max Drawdown | -44.93% |
| Sharpe Ratio | 1.30 |

## Out-of-Sample Performance (Quantpedia)
| Metric | Value |
|--------|-------|
| Period | 2000-2025 |
| Return | 0.4% p.a. |
| Volatility | 15.07% |
| Max Drawdown | -49.98% |
| Sharpe Ratio | 0.027 |

**WARNING**: Out-of-sample performance is extremely poor compared to in-sample. This strategy may have been arbitraged away or requires additional refinements for modern markets.

## Source Paper
**Industries and Stock Return Reversals**
- Authors: Allaudeen Hameed, Joshua Huang, Guangzhou Mian
- Link: https://www.researchgate.net/publication/228258870_Industries_and_Stock_Return_Reversals
- Key Finding: Intra-industry reversals are stronger in magnitude (~1.5% monthly), robust to microstructure biases, and present across stocks including large, liquid, and low-volatility stocks.

## Eligibility Check
### Available
**Transforms:**
- `cs_select(direction, mode, k, group_by="industry")` - Cross-sectional selection with industry grouping
- `roc(close, 21)` - Monthly return calculation
- `cs_momentum(group_by="industry")` - Cross-sectional momentum with grouping

**Assets:**
- 13,145 US stocks available
- Industry classification in asset metadata (sector, industry fields)
- Multiple specific industries: Biotechnology, Banks-Regional, Software-Application, etc.

### Missing / Concerns
1. **Data Quality**: ~7,500 stocks classified as "Others" industry, limiting effective universe
2. **Poor OOS Performance**: 0.027 Sharpe in 2000-2025 period suggests strategy decay
3. **Minimum Stock Count per Industry**: Strategy needs ~50 stocks per industry for meaningful 20% selection

## Implementation Notes
1. **Timeframe**: Daily bars, signal calculated at month-end
2. **Signal Logic**:
   ```
   monthly_return = roc(close, 21)  # 21-day (~1 month) return

   # Select bottom 20% within each industry (losers to go long)
   long_mask = cs_select(monthly_return, direction=bottom, mode=percent, k=20, group_by=industry)

   # Select top 20% within each industry (winners to go short)
   short_mask = cs_select(monthly_return, direction=top, mode=percent, k=20, group_by=industry)
   ```
3. **Universe Filter**:
   - Filter stocks with price >= $3
   - Exclude stocks with "Others" industry classification
   - Consider filtering for liquidity (dollar volume)
4. **Position Management**:
   - Equal weight across all long positions
   - Equal weight across all short positions
   - Long portfolio: ~40-300 stocks depending on industries
   - Short portfolio: ~40-300 stocks
5. **Rebalance**: Monthly at month-end
6. **Risk Note**: Strategy is "short volatility" - can suffer significant losses during high-volatility periods. Consider risk management during market stress.

## Alternative Implementations
1. **Long-Only**: Only take the loser positions, avoiding short selling
2. **Single Industry Focus**: Trade only in select liquid industries with enough stocks
3. **Enhanced Signal**: Combine with inter-industry momentum for additional alpha
4. **VIX Filter**: Reduce position size when VIX is elevated (per Nagel's research)

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/stock-return-reversal-within-industries/
#
# The investment universe consists of US stocks and excludes stocks with a price of less than $3.
# The stocks are divided into 24 industries. At the end of each month, the top (winner) and bottom
# (loser) 20 percent of the stocks are identified based on their returns in that month.
# The contrarian strategy involves buying the equal-weight portfolio of loser stocks and selling
# the equal-weight portfolio of the winner stocks from industry and repeated in each industry.
#
# QC implementation changes:
# - Universe consists of 500 most liquid US stocks with a price of more than 3$.

#region imports
from AlgorithmImports import *
from typing import List, Dict, Tuple
from pandas.core.frame import DataFrame
from pandas.core.series import Series
#endregion

class StockReturnReversalIndustries(QCAlgorithm):
    def Initialize(self) -> None:
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100_000)
        self.fundamental_count: int = 500
        self.fundamental_sorting_key = lambda x: x.DollarVolume
        self.period: int = 21
        self.quantile: int = 5
        self.leverage: int = 5
        self.min_share_price: float = 3.
        self.long: List[Symbol] = []
        self.short: List[Symbol] = []

        # Daily price data.
        self.data: Dict[Symbol, SymbolData] = {}

        self.selection_flag: bool = True
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.FundamentalSelectionFunction)
        self.settings.daily_precise_end_time = False
        self.settings.minimum_order_margin_portfolio_percentage = 0.

        self.market: Symbol = self.AddEquity('SPY', Resolution.Daily).Symbol
        self.schedule.on(self.date_rules.month_start(self.market),
            self.time_rules.after_market_open(self.market), self.selection)

    def OnSecuritiesChanged(self, changes: SecurityChanges) -> None:
        for security in changes.AddedSecurities:
            security.SetFeeModel(CustomFeeModel())
            security.SetLeverage(self.leverage)

    def FundamentalSelectionFunction(self, fundamental: List[Fundamental]) -> List[Symbol]:
        if not self.selection_flag:
            return Universe.Unchanged

        # Update the rolling window every month.
        for stock in fundamental:
            symbol: Symbol = stock.Symbol
            # Store monthly price.
            if symbol in self.data:
                self.data[symbol].update(stock.AdjustedPrice)

        selected: List[Fundamental] = [
            x for x in fundamental if x.HasFundamentalData
            and x.Market == 'usa' and x.MarketCap != 0
            and x.AssetClassification.MorningstarIndustryGroupCode != 0
            and x.Price >= self.min_share_price
        ]

        if len(selected) > self.fundamental_count:
            selected = [x for x in sorted(selected,
                key=self.fundamental_sorting_key, reverse=True)[:self.fundamental_count]]

        groups: Dict[MorningstarIndustryGroupCode, List[Symbol]] = {}

        # Warmup price rolling windows.
        for stock in selected:
            symbol: Symbol = stock.Symbol
            if symbol not in self.data:
                self.data[symbol] = SymbolData(symbol, self.period)
                history: DataFrame = self.History(symbol, self.period, Resolution.Daily)
                if history.empty:
                    self.Log(f"Not enough data for {symbol} yet.")
                    continue
                closes: Series = history.loc[symbol].close
                for time, close in closes.items():
                    self.data[symbol].update(close)

            # Append symbols to industry groups.
            if self.data[symbol].is_ready():
                industry_group_code: MorningstarIndustryGroupCode = \
                    stock.AssetClassification.MorningstarIndustryGroupCode
                if industry_group_code not in groups:
                    groups[industry_group_code] = []
                groups[industry_group_code].append(symbol)

        # Sorting by performance.
        for industry_code in groups:
            if len(groups[industry_code]) >= self.quantile:
                sorted_by_ret: List[Tuple] = sorted(groups[industry_code],
                    key = lambda x: self.data[x].performance(), reverse = True)
                quantile: int = int(len(sorted_by_ret) / self.quantile)
                self.short = self.short + sorted_by_ret[:quantile]
                self.long = self.long + sorted_by_ret[-quantile:]

        return self.long + self.short

    def OnData(self, slice: Slice) -> None:
        if not self.selection_flag:
            return
        self.selection_flag = False

        # trade execution
        targets: List[PortfolioTarget] = []
        for i, portfolio in enumerate([self.long, self.short]):
            for symbol in portfolio:
                if symbol in slice and slice[symbol]:
                    targets.append(PortfolioTarget(symbol, ((-1) ** i) / len(portfolio)))

        self.SetHoldings(targets, True)

        self.long.clear()
        self.short.clear()

    def selection(self) -> None:
        self.selection_flag = True


class SymbolData():
    def __init__(self, symbol: Symbol, period: int):
        self._symbol: Symbol = symbol
        self._period: int = period
        self._price: RollingWindow = RollingWindow[float](period)

    def update(self, price: float) -> None:
        self._price.Add(price)

    def is_ready(self) -> bool:
        return self._price.IsReady

    # Monthly performance.
    def performance(self) -> float:
        return self._price[0] / self._price[self._period - 1] - 1


# Custom fee model.
class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters: OrderFeeParameters) -> OrderFee:
        fee: float = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))
```

## Related Research
- Intra-industry reversals are driven by order imbalances and non-informational shocks
- Reversals stronger following aggregate market declines and volatile times
- Inter-industry momentum and intra-industry reversals can be combined for ~2% monthly alpha
- Nagel's "Evaporating Liquidity" shows reversal returns are predictable with VIX
- Blitz et al. (2023): Classic short-term reversal has weakened; can be revived by countering tendency to go against short-term momentum in industry/factor returns
