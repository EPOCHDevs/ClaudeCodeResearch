# Sector Momentum - Rotational System

**Quantpedia ID**: #0003
**URL**: https://quantpedia.com/strategies/sector-momentum-rotational-system
**Status**: IN_REVIEW

## Definitions
- Strategy: `project/definitions/test_runner/sector_momentum_strategy.json`
**Linear Issue**: [ENG-561](https://linear.app/epoch-inc/issue/ENG-561/implement-sector-momentum-strategy-0003)

## Overview

Rotational momentum system that compares performance of all US equity sectors and picks only the best-performing sectors into the portfolio. Based on Mebane Faber's research.

## Trading Rules

**Universe**: 10 US Sector ETFs
- VNQ - Real Estate (Vanguard Real Estate Index Fund)
- XLK - Technology (Technology Select Sector SPDR)
- XLE - Energy (Energy Select Sector SPDR)
- XLV - Health Care (Health Care Select Sector SPDR)
- XLF - Financials (Financial Select Sector SPDR)
- XLI - Industrials (Industrials Select Sector SPDR)
- XLB - Materials (Materials Select Sector SPDR)
- XLY - Consumer Discretionary (Consumer Discretionary Select Sector SPDR)
- XLP - Consumer Staples (Consumer Staples Select Sector SPDR)
- XLU - Utilities (Utilities Select Sector SPDR)

**Signal**: 12-month momentum (Rate of Change, 252 trading days)

**Selection**: Pick top 3 sectors by momentum

**Weighting**: Equal weight (1/3 each)

**Rebalancing**: Monthly

## Fundamental Reason

- Momentum is one of the most researched and profitable anomalies
- Industry momentum accounts for much of individual stock momentum (Moskowitz & Grinblatt)
- Different equity sectors have varying sensitivity to business cycles
- Rotate between sectors to hold only those with highest probability of returns

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1928-2009 |
| Return | 13.94% p.a. |
| Volatility | 18.38% |
| Max Drawdown | -46.29% |
| Sharpe Ratio | 0.54 |

Note: Outperformance nearly 4% vs simple buy-and-hold of US equity index

## Source Paper

**Mebane Faber: "Relative Strength Strategies for Investing"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1585517

> Abstract: The purpose of this paper is to present simple quantitative methods that improve risk-adjusted returns for investing in US equity sectors and global asset class portfolios. A relative strength model is tested on the French-Fama US equity sector data back to the 1920s that results in increased absolute returns with equity-like risk. The relative strength portfolios outperform the buy and hold benchmark in approximately 70% of all years and returns are persistent across time.

## Related Papers

1. Moskowitz, Grinblatt: "Do Industries Explain Momentum?" - http://faculty.chicagobooth.edu/tobias.moskowitz/research/industry.pdf
2. Chen, Jiang, Zhu: "Do Style and Sector Indexes Carry Momentum?" - http://www.apjfs.org/2009/cafm2009/04_03_Do%20Style%20and%20Sector%20Indexes.pdf
3. Andreu, Swinkels, Tjong-A-Tjoe: "Can exchange traded funds be used to exploit country and industry momentum?" - http://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2011-Braga/papers/0166.pdf
4. Geczy, Samonov: "215 Years of Global Multi-Asset Momentum" - http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2607730
5. Huhn: "Industry Momentum: The Role of Time-Varying Factor Exposures and Market Conditions" - http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2650378

## Keywords

momentum, rotational system, sector picking, equities

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/sector-momentum-rotational-system/
#
# Use ten sector ETFs. Pick 3 ETFs with the strongest 12-month momentum into
# your portfolio and weight them equally. Hold them for one month and then rebalance.

from AlgorithmImports import *

class SectorMomentumAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)

        # daily ROC data
        self.data: Dict[str, RateOfChange] = {}
        self.roc_period: int = 12 * 21
        self.SetWarmUp(self.roc_period, Resolution.Daily)

        self.selected_symbol_count: int = 3  # long symbol count
        self.long_universe: List[str] = [
            "VNQ",  # Vanguard Real Estate Index Fund
            "XLK",  # Technology Select Sector SPDR Fund
            "XLE",  # Energy Select Sector SPDR Fund
            "XLV",  # Health Care Select Sector SPDR Fund
            "XLF",  # Financial Select Sector SPDR Fund
            "XLI",  # Industrials Select Sector SPDR Fund
            "XLB",  # Materials Select Sector SPDR Fund
            "XLY",  # Consumer Discretionary Select Sector SPDR Fund
            "XLP",  # Consumer Staples Select Sector SPDR Fund
            "XLU"   # Utilities Select Sector SPDR Fund
        ]

        for ticker in self.long_universe:
            data = self.AddEquity(ticker, Resolution.Daily)
            data.SetLeverage(5)
            self.data[ticker] = self.ROC(ticker, self.roc_period, Resolution.Daily)

        self.data[self.long_universe[0]].Updated += self.OnROCUpdated
        self.recent_month: int = -1
        self.rebalance_flag: bool = False

    def OnROCUpdated(self, sender, updated) -> None:
        # set rebalance flag
        if self.recent_month != self.Time.month:
            self.recent_month = self.Time.month
            self.rebalance_flag = True

    def OnData(self, data: Slice) -> None:
        if self.IsWarmingUp:
            return

        # rebalance once a month
        if self.rebalance_flag:
            self.rebalance_flag = False

            # sort long universe by momentum
            sorted_by_momentum = sorted(
                [x for x in self.data.items() if x[1].IsReady and
                 x[0] in self.long_universe and
                 x[0] in data and data[x[0]]],
                key=lambda x: x[1].Current.Value,
                reverse=True
            )

            if len(sorted_by_momentum) < self.selected_symbol_count:
                self.Liquidate()
                return

            long = [x[0] for x in sorted_by_momentum[:self.selected_symbol_count]]

            # trade execution
            invested = [x.Key.Value for x in self.Portfolio if x.Value.Invested]
            for symbol in invested:
                if symbol not in long:
                    self.Liquidate(symbol)

            for ticker in long:
                self.SetHoldings(ticker, 1 / len(long))
```

## Implementation Notes

- The strategy uses 12-month (252 trading days) momentum
- Rebalancing happens on the first trading day of each month
- Top 3 sectors are selected regardless of whether momentum is positive or negative
- This is similar to strategy #0002 (Asset Class Momentum) but uses sector ETFs instead of asset class ETFs

## Epoch Implementation

**Period**: 2000-01-01 to 2025-12-31
- All sector ETFs have data from 2000 onwards

**Differences from QuantConnect:**
- None expected - same universe, same rules

### Backtest Results (2000-2025)

| Metric | Value |
|--------|-------|
| Annual Return | 8.35% |
| Cumulative Returns | 496.70% |
| Annual Volatility | 18.62% |
| Max Drawdown | -50.88% |
| Sharpe Ratio | 0.52 |

**Comparison with Source Paper (1928-2009):**
- Volatility and Sharpe ratio are very close to source paper values
- Lower returns expected due to different time period
- Source paper included pre-ETF era (1928-1998) when individual stocks or indexes were used
