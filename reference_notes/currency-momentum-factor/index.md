# Currency Momentum Factor

**Quantpedia ID**: #0008
**URL**: https://quantpedia.com/strategies/currency-momentum-factor
**Status**: ELIGIBLE
**Linear Issue**: [ENG-22](https://linear.app/epoch-inc/issue/ENG-22/implement-currency-momentum-factor-0008)

## Overview
Currency momentum is a well-documented anomaly where currencies that have performed well recently continue to outperform, while poor performers continue to underperform. The strategy exploits investors' underreaction to news - the segmentation of currency market participants where some act quickly on news while others respond more slowly creates trends that can be protracted.

## Trading Rules
**Universe**: 8 currency futures (G10 + Mexico)
**Signal**: 12-month price momentum (Rate of Change)
**Selection**: Long top 3 highest momentum, short bottom 3 lowest momentum
**Weighting**: Equal weight within long/short legs
**Rebalancing**: Monthly

### Currency Universe
| Future | Currency | CME Symbol |
|--------|----------|------------|
| A6-Futures | Australian Dollar | CME_AD1 |
| B6-Futures | British Pound | CME_BP1 |
| D6-Futures | Canadian Dollar | CME_CD1 |
| E6-Futures | Euro FX | CME_EC1 |
| J6-Futures | Japanese Yen | CME_JY1 |
| M6-Futures | Mexican Peso | CME_MP1 |
| N6-Futures | New Zealand Dollar | CME_NE1 |
| S6-Futures | Swiss Franc | CME_SF1 |

## Fundamental Reason
The momentum anomaly works due to:
1. **Investor underreaction** - failing to incorporate news fully into prices
2. **Market segmentation** - some participants act quickly on news while others respond slowly
3. **Behavioral shortcomings** - investor herding, over/under-reaction, confirmation bias
4. **Risk compensation** - investors following momentum strategies are compensated for exposure to global political risk

Note: Currency momentum has very different properties from the carry trade (#0005) - it's driven by return continuation in spot rates, not interest rate differentials.

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1989-2009 |
| Return | 7.61% p.a. |
| Volatility | 10.22% |
| Max Drawdown | -45.87% |
| Sharpe Ratio | 0.30 |

**Note**: Performance calculated from Deutsche Bank Currency Momentum USD Index.

**Confidence Note**: OOS back-test shows slightly negative performance. Strategy's alpha may be deteriorating in out-of-sample period.

## Source Paper
**Deutsche Bank: "Currency Returns"**
- URL: http://globalmarkets.db.com/new/docs/dbCurrencyReturns_March2009.pdf

**Abstract**: Momentum - A widely observed feature of currency markets is that many exchange rates trend on a multi-year basis. Therefore a strategy that follows the trend typically makes positive returns over time. The segmentation of currency market participants with some acting quickly on news while others respond more slowly is one reason why trends emerge and can be protracted.

## Other Papers
- Menkhoff, Sarno, Schmeling, Schrimpf: "Currency Momentum Strategies" (SSRN 1809776)
- Bianchi, Drew, Polichronis: "A Test of Momentum Trading Strategies in Foreign Exchange Markets"
- Geczy, Samonov: "215 Years of Global Multi-Asset Momentum: 1800-2014" (SSRN 2607730)
- Ilmanen et al: "Factor Premia and Factor Timing: A Century of Evidence" (SSRN 3400998)

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/currency-momentum-factor/
#
# Universe: 8 currency futures
# Signal: 12-month momentum (Rate of Change)
# Selection: Long top 3, short bottom 3 by momentum
# Rebalance: Monthly

class CurrencyMomentumFactor(QCAlgorithm):
    def initialize(self) -> None:
        self.set_start_date(2000, 1, 1)
        self.set_cash(100_000)

        period: int = 12 * 21  # 12 months in trading days
        self.set_warm_up(period, Resolution.DAILY)

        tickers: List[str] = [
            "CME_AD1",  # Australian Dollar
            "CME_BP1",  # British Pound
            "CME_CD1",  # Canadian Dollar
            "CME_EC1",  # Euro FX
            "CME_JY1",  # Japanese Yen
            "CME_MP1",  # Mexican Peso
            "CME_NE1",  # New Zealand Dollar
            "CME_SF1"   # Swiss Franc
        ]

        self._securities: List[Security] = []
        self._traded_count: int = 3

        for symbol in tickers:
            data: Security = self.add_data(QuantpediaFutures, symbol, Resolution.DAILY)
            data.set_leverage(5)
            data.roc: RateOfChange = self.ROC(symbol, period, Resolution.DAILY)
            self._securities.append(data)

        self._recent_month: int = -1

    def on_data(self, slice: Slice) -> None:
        if self.is_warming_up:
            return

        # Rebalance monthly
        if self.time.month == self._recent_month:
            return
        self._recent_month = self.time.month

        # Calculate momentum for each currency
        perf: Dict[Symbol, float] = {
            sec.symbol: sec.roc.current.value
            for sec in self._securities
            if sec.roc.is_ready and slice.contains_key(sec.symbol)
        }

        long: List[Symbol] = []
        short: List[Symbol] = []

        if len(perf) >= self._traded_count * 2:
            sorted_by_performance = sorted(perf, key=perf.get, reverse=True)
            long = sorted_by_performance[:self._traded_count]
            short = sorted_by_performance[-self._traded_count:]

        # Execute trades
        targets: List[PortfolioTarget] = []
        for i, portfolio in enumerate([long, short]):
            for symbol in portfolio:
                targets.append(PortfolioTarget(symbol, ((-1) ** i) / len(portfolio)))

        self.set_holdings(targets, True)
```

## Eligibility Check

### Available
**Currency Futures** (same as #0005 FX Carry Trade):
- A6-Futures (Australian Dollar)
- B6-Futures (British Pound)
- D6-Futures (Canadian Dollar)
- E6-Futures (Euro FX)
- J6-Futures (Japanese Yen)
- M6-Futures (Mexican Peso)
- N6-Futures (New Zealand Dollar)
- S6-Futures (Swiss Franc)

**Transforms**:
- `roc` - Rate of Change (momentum calculation)
- `cs_rank` - Cross-sectional ranking
- `cs_select` - Cross-sectional selection (top/bottom N)
- `equal_weight` - Equal weighting

### EpochScript Implementation Approach
```python
# Data source
src = market_data_source(timeframe=1D)()
close = src.c

# 12-month momentum (252 trading days)
momentum_12m = roc(period=252)(close)

# Rank by momentum (cross-sectional)
momentum_rank = cs_rank(method=RankMethod.average, ascending=False)(momentum_12m)

# Select top 3 and bottom 3 of 8 currencies
long_mask = momentum_rank <= 3
short_mask = momentum_rank >= 6  # bottom 3 of 8

# Equal weight
long_weight = equal_weight()(active_mask=long_mask)
short_weight = equal_weight()(active_mask=short_mask)

# Monthly rebalance
is_new_month = time_feature(component=TimeFeature.month)().changed()
position_size(type="percent")(size=(long_weight - short_weight) * 100, rebalance_on=is_new_month)
```

## Implementation Notes
- Strategy has significant drawdown risk (-45.87%) - higher than FX Carry Trade
- Momentum and carry trades have LOW correlation - can be combined for diversification
- OOS performance shows alpha degradation - consider robustness testing
- 12-month lookback is standard but other periods (6M, 3M) could be tested
- Unlike carry trade, this does NOT require fundamental data (interest rates)

## Risk Considerations
- **Alpha Decay**: Quantpedia notes OOS performance is slightly negative
- **Crash Risk**: Momentum strategies can experience sudden reversals
- **Transaction Costs**: Monthly rebalancing incurs costs
- **Negative Skewness**: Like carry, momentum can have sudden drawdowns

## Comparison with FX Carry Trade (#0005)

| Aspect | Carry Trade | Momentum |
|--------|-------------|----------|
| Signal | Interest rate differential | Price return |
| Data Required | FRED interest rates | Price only |
| Correlation | Higher with risk assets | Low correlation with carry |
| Implementation | Requires fundamental data | Pure price-based |
| Combined Use | Yes - diversification benefit | Yes - different risk factors |
