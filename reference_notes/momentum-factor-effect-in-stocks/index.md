# Momentum Factor Effect in Stocks

**Quantpedia ID**: #0014
**URL**: https://quantpedia.com/strategies/momentum-factor-effect-in-stocks
**Status**: ELIGIBLE
**Linear Issue**: [ENG-29](https://linear.app/epoch-inc/issue/ENG-29/implement-momentum-factor-effect-in-stocks-0014)

## Overview
Stocks which have performed well in the past 12 months (skipping the most recent month) continue to perform well, while past losers continue to underperform. This is one of the most academically studied anomalies with strong persistence across global markets.

## Trading Rules
**Universe**: NYSE, AMEX, NASDAQ stocks (top 500 by market cap or dollar volume)
**Signal**: Past 12-month return, skipping most recent month (to avoid microstructure biases)
**Selection**: Long top quintile (winners), short bottom quintile (losers)
**Weighting**: Equal weighted within long/short legs
**Rebalancing**: Monthly

### Momentum Calculation
- Formation period: Months t-12 to t-2 (skip month t-1)
- Calculate cumulative return over this period
- Rank stocks cross-sectionally
- Top 20% = Winners (long), Bottom 20% = Losers (short)

## Fundamental Reason
- **Investor underreaction**: Prices react only partially to good/bad news
- **Behavioral biases**: Herding, overreaction, confirmation bias
- **Information diffusion**: Some information takes time to be reflected in prices
- **Risk exposure**: Momentum may capture time-varying systematic risk

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1927-2013 |
| Return | 8.3% p.a. |
| Volatility | 16.6% |
| Max Drawdown | -87.41% |
| Sharpe Ratio | 0.50 |

**Note**: The -87% drawdown occurred in 2009 ("momentum crash").

**OOS Performance (2000-2025)**:
- Return: -2.0% p.a.
- Volatility: 26%
- Sharpe: -0.08
- Max DD: -86.9%

**Note**: Recent OOS performance is negative, likely due to momentum crashes and increased arbitrage activity.

## Source Paper
**Asness, Frazzini, Israel, Moskowitz: "Fact, Fiction and Momentum Investing"**
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2435323

**Abstract**: It's been over 20 years since the academic discovery of momentum investing (Jegadeesh and Titman (1993), Asness (1994)), yet much confusion and debate remains regarding its efficacy and its use as a practical investment tool. In some cases "confusion and debate" is us attempting to be polite, as it is near impossible for informed practitioners and academics to still believe some of the myths uttered about momentum — but that impossibility is often belied by real world statements. In this article, we aim to clear up much of the confusion by documenting what we know about momentum and disproving many of the often-repeated myths. We highlight ten myths about momentum and refute them.

## Other Papers
- Jagadeesh, Titman: "Momentum" (SSRN 299107)
- Barroso, Santa-Clara: "Managing the Risk of Momentum" (SSRN 2041429)
- Israel, Moskowitz: "The Role of Shorting, Firm Size, and Time on Market Anomalies" (SSRN 2089466)

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/momentum-factor-effect-in-stocks/
#
# Universe: NYSE, AMEX, NASDAQ stocks (top 500 by market cap)
# Signal: 12-month return, skip most recent month
# Selection: Long top quintile, short bottom quintile
# Rebalance: Monthly

class MomentumFactorEffectinStocks(QCAlgorithm):
    def initialize(self) -> None:
        self.set_start_date(2000, 1, 1)
        self.set_cash(100_000)

        self.weight: Dict[Symbol, float] = {}
        self.data: Dict[Symbol, RollingWindow] = {}
        self.period: int = 12 * 21  # 12 months of trading days
        self.quantile: int = 5
        self.leverage: int = 5
        self.exchange_codes: List[str] = ['NYS', 'NAS', 'ASE']
        self.fundamental_count: int = 500
        self.fundamental_sorting_key = lambda x: x.dollar_volume
        self.selection_flag: bool = False

        self.universe_settings.resolution = Resolution.DAILY
        self.add_universe(self.fundamental_selection_function)
        self._recent_month: int = -1

    def fundamental_selection_function(self, fundamental: List[Fundamental]) -> List[Symbol]:
        # update the rolling window every day
        [self.data[stock.symbol].add(stock.adjusted_price)
         for stock in fundamental if stock.symbol in self.data]

        if self._recent_month == self.time.month:
            return Universe.UNCHANGED
        self._recent_month = self.time.month
        self.selection_flag = True

        selected: List[Fundamental] = [
            x for x in fundamental if x.has_fundamental_data
            and x.market_cap != 0 and x.market == 'usa'
            and x.security_reference.exchange_id in self.exchange_codes
        ]

        if len(selected) > self.fundamental_count:
            selected = sorted(selected, key=self.fundamental_sorting_key,
                            reverse=True)[:self.fundamental_count]

        # warmup price rolling windows
        for stock in selected:
            symbol: Symbol = stock.symbol
            if symbol not in self.data:
                self.data[symbol] = RollingWindow[float](self.period)

            history: DataFrame = self.history(symbol, self.period, Resolution.DAILY)
            if history.empty:
                continue
            closes: Series = history.loc[symbol].close
            for time, close in closes.items():
                self.data[symbol].add(close)

        # Calculate 12-month momentum
        perf: Dict[Symbol, float] = {
            stock.symbol: self.data[stock.symbol][0] / self.data[stock.symbol][self.period - 1] - 1
            for stock in selected if self.data[stock.symbol].is_ready
        }

        if len(perf) >= self.quantile:
            sorted_by_perf: List = sorted(perf, key=perf.get)
            quantile: int = int(len(sorted_by_perf) / self.quantile)
            long: List[Symbol] = sorted_by_perf[-quantile:]   # Top performers
            short: List[Symbol] = sorted_by_perf[:quantile]   # Bottom performers

            for i, portfolio in enumerate([long, short]):
                for symbol in portfolio:
                    self.weight[symbol] = ((-1) ** i) / len(portfolio)

        return list(self.weight.keys())

    def on_data(self, slice: Slice) -> None:
        if not self.selection_flag:
            return
        self.selection_flag = False

        portfolio: List[PortfolioTarget] = [
            PortfolioTarget(symbol, w) for symbol, w in self.weight.items()
            if slice.contains_key(symbol)
        ]
        self.set_holdings(portfolio, True)
        self.weight.clear()
```

## Eligibility Check

### Available
**Data Sources**:
- `market_data_source()` - OHLCV data for all US stocks (13,145 available)
- S&P 500 index constituents for universe filtering
- Price data for momentum calculation

**Transforms**:
- `roc(period=252)` - Rate of change for 12-month return
- `lag(periods=21)` - Skip most recent month
- `cs_rank(ascending=False)` - Cross-sectional ranking by momentum
- `cs_select(quantile=5, select_quantile=5)` - Select top quintile (winners)
- `cs_select(quantile=5, select_quantile=1)` - Select bottom quintile (losers)
- `equal_weight` - Equal weighting within portfolios
- `time_feature(component=TimeFeature.month)` - Monthly rebalancing trigger

**Universe**:
- US stocks available (NYSE, AMEX, NASDAQ equivalents)
- 13,145 stocks in platform universe
- S&P 500 constituents available for filtering

### Implementation Approach
```python
# Get price data
price = market_data_source(timeframe=1D)().c

# Calculate 12-month return, skip last month
returns_12m = roc(period=252)(price)
lagged_returns = lag(periods=21)(returns_12m)

# Rank stocks by momentum
momentum_rank = cs_rank(ascending=False)(lagged_returns)

# Select top and bottom quintiles
winners = cs_select(quantile=5, select_quantile=5)(lagged_returns)
losers = cs_select(quantile=5, select_quantile=1)(lagged_returns)

# Equal weight long winners, short losers
long_weight = equal_weight()(active_mask=winners)
short_weight = -equal_weight()(active_mask=losers)
total_weight = long_weight + short_weight

# Monthly rebalance
is_new_month = time_feature(component=TimeFeature.month)().changed()
position_size(type="percent")(size=total_weight * 100, rebalance_on=is_new_month)
```

## Implementation Notes
- Original strategy trades ~1000 stocks; QC uses 500 for practicality
- 12-1 momentum (skip last month) reduces reversal and microstructure effects
- Long-short implementation requires shorting capability
- Long-only version also profitable but lower Sharpe
- High correlation to equity market in up-markets, but crashes in reversals
- 2009 momentum crash: -87% drawdown when market rebounded

## Risk Considerations
- **Momentum crashes**: Can lose 50%+ in sharp market reversals
- **2009 crash**: -87% max drawdown when market rebounded after 2008 crisis
- **Time-varying risk**: Momentum has negative beta following bear markets
- **Transaction costs**: High turnover with monthly rebalancing
- **Alpha decay**: Recent OOS shows negative returns, arbitrage may have increased
- **Negative skewness**: Short periods of extreme losses

## Strategy Enhancements
Several papers suggest improvements:
1. **Risk-managed momentum** (Barroso, Santa-Clara): Scale by volatility to reduce crashes
2. **Quality momentum** (Vogel, Gray): Use path of returns, not just endpoint
3. **Industry momentum**: Momentum at sector level
4. **Long-only momentum**: Avoids shorting costs and momentum crash risk

## Comparison Notes
This is the **classic cross-sectional momentum** strategy. Pure long-short implementation has extreme crash risk. Long-only versions are more practical for most investors. Consider risk-managed versions for better risk-adjusted returns.
