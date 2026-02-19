# Currency Momentum Factor

**Quantpedia ID**: #0008
**URL**: https://quantpedia.com/strategies/currency-momentum-factor
**Status**: IN_REVIEW

## Definitions
- Strategy: `project/definitions/test_runner/currency_momentum_strategy.json`
**Linear Issue**: [ENG-563](https://linear.app/epoch-inc/issue/ENG-563/implement-currency-momentum-factor-0008)

## Important Note

Quantpedia explicitly warns: "OOS back-test shows slightly negative performance. It looks, that strategy's alpha is deteriorating in the out-of-sample period."

## Overview

Currency momentum strategy that exploits the trend-following behavior in FX markets. Go long currencies with highest recent momentum against USD and short currencies with lowest momentum.

## Trading Rules

**Universe**: 8 Currency Pairs vs USD
- AUD/USD - Australian Dollar
- GBP/USD - British Pound
- CAD/USD - Canadian Dollar
- EUR/USD - Euro
- JPY/USD - Japanese Yen
- MXN/USD - Mexican Peso
- NZD/USD - New Zealand Dollar
- CHF/USD - Swiss Franc

**Signal**: 12-month momentum (252-day Rate of Change)

**Selection**:
- Long: Top 3 currencies by momentum
- Short: Bottom 3 currencies by momentum

**Weighting**: Equal weight within long and short portfolios

**Rebalancing**: Monthly

## Fundamental Reason

- Momentum is a well-researched anomaly present in FX markets
- Investor underreaction to new information
- Segmentation of currency market where some participants act quickly while others respond slowly
- Exchange rates trend on multi-year basis
- Global political risk affects currency momentum returns

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1989-2009 |
| Return | 7.61% p.a. |
| Volatility | 10.22% |
| Max Drawdown | -45.87% |
| Sharpe Ratio | 0.30 |

Note: Performance from Deutsche Bank Currency Momentum USD Index. OOS shows slightly negative performance - alpha may be deteriorating.

## Source Paper

**Deutsche Bank: Currency Returns**
- URL: http://globalmarkets.db.com/new/docs/dbCurrencyReturns_March2009.pdf

> Abstract: Momentum - A widely observed feature of currency markets is that many exchange rates trend on a multi-year basis. Therefore a strategy that follows the trend typically makes positive returns over time. The segmentation of currency market participants with some acting quickly on news while others respond more slowly is one reason why trends emerge and can be protracted.

## Related Papers

1. Menkhoff, Sarno, Schmeling, Schrimpf: "Currency Momentum Strategies" - http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1809776
2. Accominotti, Chambers: "Out-of-Sample Evidence on the Returns to Currency Trading" - https://research.mbs.ac.uk/accounting-finance/Portals/0/docs/Out-of-Sample%20Evidence%20on%20the%20Returns.pdf
3. Geczy, Samonov: "215 Years of Global Multi-Asset Momentum" - http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2607730
4. Bae, Elkamhi: "Global Equity Correlation in Carry and Momentum Trades" - http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2521608

## Keywords

momentum, FX anomaly, forex system, factor investing, smart beta

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/currency-momentum-factor/
#
# Create an investment universe consisting of several currencies (10-20).
# Go long three currencies with the highest 12-month momentum against USD
# and go short three currencies with the lowest 12-month momentum against USD.
# Cash not used as margin invest on overnight rates. Rebalance monthly.

from AlgorithmImports import *

class CurrencyMomentumFactor(QCAlgorithm):
    def initialize(self) -> None:
        self.set_start_date(2000, 1, 1)
        self.set_cash(100_000)

        period: int = 12 * 21
        self.set_warm_up(period, Resolution.DAILY)

        tickers: List[str] = [
            "CME_AD1",  # Australian Dollar Futures
            "CME_BP1",  # British Pound Futures
            "CME_CD1",  # Canadian Dollar Futures
            "CME_EC1",  # Euro FX Futures
            "CME_JY1",  # Japanese Yen Futures
            "CME_MP1",  # Mexican Peso Futures
            "CME_NE1",  # New Zealand Dollar Futures
            "CME_SF1"   # Swiss Franc Futures
        ]

        self._securities: List[Security] = []
        self._traded_count: int = 3

        for symbol in tickers:
            data = self.add_data(QuantpediaFutures, symbol, Resolution.DAILY)
            data.set_fee_model(CustomFeeModel())
            data.set_leverage(5)
            data.roc = self.ROC(symbol, period, Resolution.DAILY)
            self._securities.append(data)

        self._recent_month: int = -1

    def on_data(self, slice: Slice) -> None:
        if self.is_warming_up:
            return

        # rebalance monthly
        if self.time.month == self._recent_month:
            return
        self._recent_month = self.time.month

        perf = {
            sec.symbol: sec.roc.current.value
            for sec in self._securities
            if sec.roc.is_ready and slice.contains_key(sec.symbol) and slice[sec.symbol]
        }

        long = []
        short = []

        if len(perf) >= self._traded_count * 2:
            sorted_by_performance = sorted(perf, key=perf.get, reverse=True)
            long = sorted_by_performance[:self._traded_count]
            short = sorted_by_performance[-self._traded_count:]

        # trade execution
        targets = []
        for i, portfolio in enumerate([long, short]):
            for symbol in portfolio:
                targets.append(PortfolioTarget(symbol, ((-1) ** i) / len(portfolio)))

        self.set_holdings(targets, True)
```

## Implementation Notes

- Uses 12-month (252 trading days) momentum
- This is a LONG-SHORT strategy (different from previous strategies)
- Need to handle different quote conventions (XXX/USD vs USD/XXX)
- Monthly rebalancing on first trading day of month
- Equal weight: 1/3 for each long position, -1/3 for each short position

## Epoch Implementation

**Period**: 2000-01-01 to 2025-12-31
- All FX pairs have data from 2000

**Asset IDs** (all XXX/USD convention):
- ^AUDUSD-FX (AUD/USD)
- ^EURUSD-FX (EUR/USD)
- ^GBPUSD-FX (GBP/USD)
- ^CADUSD-FX (CAD/USD)
- ^JPYUSD-FX (JPY/USD)
- ^MXNUSD-FX (MXN/USD)
- ^NZDUSD-FX (NZD/USD)
- ^CHFUSD-FX (CHF/USD)

### Backtest Results (2000-2025)

| Metric | Value |
|--------|-------|
| Annual Return | -0.41% |
| Cumulative Returns | -8.95% |
| Annual Volatility | 3.99% |
| Max Drawdown | -18.76% |
| Sharpe Ratio | -0.08 |
| Round Trips | 222 |

**Comparison with Source Paper (1989-2009):**
- Source paper showed 7.61% p.a. return with 0.30 Sharpe
- Our results confirm Quantpedia's warning about OOS deterioration
- Strategy alpha has significantly deteriorated post-2009
- Lower volatility (3.99% vs 10.22%) due to dollar-neutral long-short structure
- This is a known phenomenon in currency momentum literature
