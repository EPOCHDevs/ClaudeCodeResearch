# Pairs Trading with Stocks

**Quantpedia ID**: #0012
**URL**: https://quantpedia.com/strategies/pairs-trading-with-stocks
**Status**: INELIGIBLE
**Linear Issue**: [ENG-25](https://linear.app/epoch-inc/issue/ENG-25/feature-request-cross-sectional-pairwise-distance-transform-for-pairs)

## Overview
Classic pairs trading strategy that exploits mean reversion in the spread between two historically correlated stocks. When prices diverge beyond normal levels, the strategy bets on convergence - shorting the relative winner and going long the relative loser. This is a market-neutral strategy that profits from the relative mispricing of close substitutes.

## Trading Rules
**Universe**: NYSE, AMEX, NASDAQ stocks (500 most liquid, price > $5)

**Formation Period**: 12 months
- Normalize prices to $1 at start
- Calculate sum of squared deviations between all pairs
- Select top 20 pairs with minimum distance

**Trading Period**: 6 months

**Entry Signal**:
- Open long-short position when pair spread diverges by 2 standard deviations
- Long the underperformer, short the outperformer

**Exit Signal**:
- Close when spread reverts to mean (z-score crosses 0)

**Weighting**: Equal dollar allocation per leg
**Rebalancing**: Daily monitoring, 6-month pair reformation

## Fundamental Reason
1. **Investor Overreaction**: Undisciplined investors overreact to news, creating temporary mispricings that disciplined pairs traders exploit.

2. **Common Factor Exposure**: Stocks that historically move together share common fundamental drivers. Temporary divergences from this relationship present statistical arbitrage opportunities.

3. **Mean Reversion**: Spreads between close substitutes tend to revert to their historical mean, providing predictable trading opportunities.

4. **Liquidity Provision**: Pairs traders effectively provide liquidity by buying oversold stocks and selling overbought ones.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1962-2002 |
| Return | 11.16% p.a. |
| Volatility | 5.85% |
| Max Drawdown | -17% |
| Sharpe Ratio | 1.22 |

## Out-of-Sample Performance (Quantpedia)
| Metric | Value |
|--------|-------|
| Period | 2010-2025 |
| Return | 3.8% p.a. |
| Volatility | 7.73% |
| Max Drawdown | -20.62% |
| Sharpe Ratio | 0.49 |

**Note**: Returns have diminished significantly over time as the strategy became widely known (consistent with adaptive market hypothesis).

## Source Paper
**Pairs Trading: Performance of a Relative Value Arbitrage Rule**
- Authors: Gatev, Goetzmann, Rouwenhorst
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=141615
- Key Finding: Simple trading rule yields annualized excess returns of up to 11% for self-financing portfolios. Bootstrap results confirm pairs effect differs from standard reversal profits.

## Eligibility Check

### INELIGIBLE - Missing Cross-Sectional Pairwise Transform

The original Gatev methodology requires **automated pair formation** across a large universe:
1. Compute distances for ALL N*(N-1)/2 pairs (~125,000 for 500 stocks)
2. Rank pairs by minimum sum of squared deviations
3. Select top 20 pairs
4. Reform pairs every 6 months

This capability is **NOT available** in the platform.

### Available (for trading a single pre-defined pair)
| Transform | Purpose |
|-----------|---------|
| `engle_granger(A, B)` | Cointegration test between 2 specific assets |
| `rolling_corr(A, B)` | Correlation between 2 specific assets |
| `zscore(window)` | Rolling z-score for spread |
| `mean_reversion_half_life()` | Mean reversion speed |

### Missing (required for full implementation)
| Capability | Status |
|------------|--------|
| Pairwise distance for ALL N assets | ❌ Not available |
| Rank pairs by distance/correlation | ❌ Not available |
| Select top K pairs dynamically | ❌ Not available |

### Feature Request
**ENG-25**: Proposed `cs_pair_distance` transform that:
- Takes N assets, computes all pairwise distances
- Supports SSD, correlation, cointegration methods
- Outputs ranked pair list with top-K selection

## Implementation Notes
1. **Pair Trading Logic** (for pre-selected pair A, B):
   ```
   # Compute spread using cointegration
   coint = engle_granger(close_A, close_B, window=252)
   spread = coint.spread

   # Normalize spread
   spread_zscore = zscore(spread, window=60)

   # Entry signals
   long_A_short_B = spread_zscore < -2
   short_A_long_B = spread_zscore > 2

   # Exit signal
   exit_signal = cross(spread_zscore, 0)
   ```

2. **Half-Life Check**:
   ```
   # Only trade pairs with reasonable mean reversion speed
   hl = mean_reversion_half_life(spread)
   tradeable = hl > 5 and hl < 60  # 5-60 days half-life
   ```

3. **Position Sizing**:
   - Equal dollar amounts per leg
   - Max 5 pairs traded simultaneously
   - Leverage: 5x

4. **Risk Management**:
   - Stop loss if spread continues diverging (e.g., 3+ std dev)
   - Maximum holding period (e.g., 60 days)
   - Monitor for structural breaks in cointegration

## Alternative Pair Selection Approaches
1. **Sector-Based**: Pairs from same industry (banks, utilities, oil)
2. **ETF Constituents**: Pairs from same ETF holdings
3. **Cointegration-First**: Screen for cointegrated pairs, then trade
4. **Correlation Threshold**: Pairs with 90%+ historical correlation
5. **Fundamental Matching**: Similar market cap, P/E, sector exposure

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/pairs-trading-with-stocks/
#
# The investment universe consists of stocks from NYSE, AMEX, and NASDAQ.
# Pairs are formed over twelve months (formation period) and traded in the
# next six-month period. Top 20 pairs with smallest historical distance are
# traded. Long-short position opened when spread diverges by 2 std dev,
# closed when prices revert.
#
# QC changes:
# - Universe consists of top 500 most liquid US stocks with price > 5$.
# - Maximum number of pairs traded at one time is set to 5.

#region imports
from AlgorithmImports import *
import numpy as np
import itertools as it
from pandas.core.frame import DataFrame
#endregion

class PairsTradingwithStocks(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetCash(100_000)
        self.market: Symbol = self.AddEquity('SPY', Resolution.Daily).Symbol

        # Daily price data.
        self.history_price: Dict[Symbol, RollingWindow] = {}
        self.period: int = 12 * 21
        self.leverage: int = 5
        self.min_share_price: float = 5.
        self.selection_month: int = 6

        # Equally weighted brackets.
        self.max_traded_pairs: int = 5
        self.traded_pairs:List = []
        self.traded_quantity: Dict = {}
        self.sorted_pairs: List = []

        self.fundamental_count: int = 500
        self.fundamental_sorting_key = lambda x: x.DollarVolume

        self.month: int = 6
        self.selection_flag: bool = True
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.FundamentalSelectionFunction)
        self.Settings.MinimumOrderMarginPortfolioPercentage = 0.
        self.settings.daily_precise_end_time = False

        self.Schedule.On(self.DateRules.MonthStart(self.market),
            self.TimeRules.AfterMarketOpen(self.market), self.Selection)

    def OnSecuritiesChanged(self, changes: SecurityChanges) -> None:
        for security in changes.AddedSecurities:
            security.SetFeeModel(CustomFeeModel())
            security.SetLeverage(self.leverage)

        for security in changes.RemovedSecurities:
            symbol: Symbol = security.Symbol
            if symbol in self.history_price:
                del self.history_price[symbol]

        symbols: List[Symbol] = [x for x in self.history_price.keys() if x != self.market]
        self.symbol_pairs = list(it.combinations(symbols, 2))

        # minimize the sum of squared deviations
        distances: Dict = {}
        for pair in self.symbol_pairs:
            if self.history_price[pair[0]].IsReady and self.history_price[pair[1]].IsReady:
                distances[pair] = self.Distance(self.history_price[pair[0]],
                                                 self.history_price[pair[1]])

        if len(distances) != 0:
            self.sorted_pairs = [x[0] for x in
                sorted(distances.items(), key = lambda x: x[1])[:20]]

        self.Liquidate()
        self.traded_pairs.clear()
        self.traded_quantity.clear()

    def FundamentalSelectionFunction(self, fundamental: List[Fundamental]) -> List[Symbol]:
        # Update the rolling window every day.
        for stock in fundamental:
            symbol: Symbol = stock.Symbol
            if symbol in self.history_price:
                self.history_price[symbol].Add(stock.AdjustedPrice)

        if not self.selection_flag:
            return Universe.Unchanged

        self.selection_flag = False

        selected: List[Fundamental] = [
            x for x in fundamental if x.HasFundamentalData
            and x.Price > self.min_share_price and x.Market == 'usa'
        ]

        if len(selected) > self.fundamental_count:
            selected = [x for x in sorted(selected,
                key=self.fundamental_sorting_key, reverse=True)[:self.fundamental_count]]

        # Warmup price rolling windows.
        for stock in selected:
            symbol: Symbol = stock.Symbol
            if symbol in self.history_price:
                continue

            self.history_price[symbol] = RollingWindow[float](self.period)
            history: DataFrame = self.History(symbol, self.period, Resolution.Daily)
            if history.empty:
                self.Log(f"Not enough data for {symbol} yet")
                continue

            closes: Series = history.loc[symbol].close
            for time, close in closes.items():
                self.history_price[symbol].Add(close)

        return [x.Symbol for x in selected if self.history_price[x.Symbol].IsReady]

    def OnData(self, data: Slice) -> None:
        if self.sorted_pairs is None:
            return

        pairs_to_remove:List = []
        for pair in self.sorted_pairs:
            # Calculate the spread of two price series.
            price_a: List[float] = list(self.history_price[pair[0]])
            price_b: List[float] = list(self.history_price[pair[1]])
            norm_a: np.ndarray = np.array(price_a) / price_a[-1]
            norm_b: np.ndarray = np.array(price_b) / price_b[-1]
            spread: np.ndarray = norm_a - norm_b
            mean: float = np.mean(spread)
            std: float = np.std(spread)
            actual_spread: float = spread[0]

            # Long-short position is opened when spread diverges by 2 std dev.
            traded_portfolio_value: float = self.Portfolio.TotalPortfolioValue / self.max_traded_pairs
            if actual_spread > mean + 2*std or actual_spread < mean - 2*std:
                if pair not in self.traded_pairs:
                    # open new position for pair, if there's place for it.
                    if len(self.traded_pairs) < self.max_traded_pairs:
                        symbol_a: Symbol = pair[0]
                        symbol_b: Symbol = pair[1]
                        a_price_norm: float = norm_a[0]
                        b_price_norm: float = norm_b[0]
                        a_price: float = price_a[0]
                        b_price: float = price_b[0]

                        # a stock's price > b stock's price
                        if a_price_norm > b_price_norm:
                            if b_price != 0 and a_price != 0:
                                long_q: float = traded_portfolio_value / b_price
                                short_q: float = -traded_portfolio_value / a_price
                                if self.Securities.ContainsKey(symbol_a) and \
                                   self.Securities.ContainsKey(symbol_b) and \
                                   self.Securities[symbol_a].Price != 0 and \
                                   self.Securities[symbol_a].IsTradable and \
                                   self.Securities[symbol_b].Price != 0 and \
                                   self.Securities[symbol_b].IsTradable:
                                    self.MarketOrder(symbol_a, short_q)
                                    self.MarketOrder(symbol_b, long_q)
                                    self.traded_quantity[pair] = (short_q, long_q)
                                    self.traded_pairs.append(pair)
                        else:
                            if b_price != 0 and a_price != 0:
                                long_q: float = traded_portfolio_value / a_price
                                short_q: float = -traded_portfolio_value / b_price
                                if self.Securities.ContainsKey(symbol_a) and \
                                   self.Securities.ContainsKey(symbol_b) and \
                                   self.Securities[symbol_a].Price != 0 and \
                                   self.Securities[symbol_a].IsTradable and \
                                   self.Securities[symbol_b].Price != 0 and \
                                   self.Securities[symbol_b].IsTradable:
                                    self.MarketOrder(symbol_a, long_q)
                                    self.MarketOrder(symbol_b, short_q)
                                    self.traded_quantity[pair] = (long_q, short_q)
                                    self.traded_pairs.append(pair)
            else:
                if pair in self.traded_pairs and pair in self.traded_quantity:
                    # close position
                    self.MarketOrder(pair[0], -self.traded_quantity[pair][0])
                    self.MarketOrder(pair[1], -self.traded_quantity[pair][1])
                    pairs_to_remove.append(pair)

        for pair in pairs_to_remove:
            self.traded_pairs.remove(pair)
            del self.traded_quantity[pair]

    def Distance(self, price_a, price_b) -> float:
        # Sum of squared deviations between normalized price series.
        price_a: List = list(price_a)
        price_b: List = list(price_b)
        norm_a: np.ndarray = np.array(price_a) / price_a[-1]
        norm_b: np.ndarray = np.array(price_b) / price_b[-1]
        return sum((norm_a - norm_b)**2)

    def Selection(self) -> None:
        if self.month == self.selection_month:
            self.selection_flag = True

        self.month += 1
        if self.month > 12:
            self.month = 1


# Custom fee model.
class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters):
        fee = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))
```

## Related Research
- Do & Faff: Pairs trading profitability declining but still viable with enhancements
- Cointegration-based pair selection outperforms distance method
- Returns higher during market stress (liquidity provision)
- Profits driven by common factor exposure, not pure reversal
- Half-life of 10-30 days optimal for trading
