# Momentum Asset Allocation Strategy

**Quantpedia ID**: #0002
**URL**: https://quantpedia.com/strategies/asset-class-momentum-rotational-system
**Status**: IN_PROGRESS

## Definitions
- Research: `project/definitions/test_runner/momentum_asset_allocation_research.json`
- Strategy: `project/definitions/test_runner/momentum_asset_allocation_strategy.json`
**Linear Issue**: [ENG-10](https://linear.app/epoch-inc/issue/ENG-10/implement-momentum-asset-allocation-strategy-0002)

## Overview

Rotational momentum system that compares performance of all asset classes and picks only the best-performing assets into the portfolio. Based on Mebane Faber's research.

## Trading Rules

**Universe**: 5 ETFs
- SPY - US stocks
- EFA - Foreign stocks
- BND - Bonds (changed from IEF to match Quantpedia text)
- VNQ - REITs
- GSG - Commodities

**Signal**: 12-month momentum (Rate of Change)

**Selection**: Pick top 3 ETFs by momentum

**Weighting**: Equal weight (1/3 each)

**Rebalancing**: Monthly

## Fundamental Reason

- Momentum is one of the strongest return-generating factors
- Various asset classes have different sensitivity to business cycles
- Rotate between asset classes to hold only those with highest probability of returns and lowest probability of losses

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1973-2009 |
| Return | 14.49% p.a. |
| Volatility | 11% |
| Max Drawdown | -47.77% |
| Sharpe Ratio | 0.78 |

## Source Paper

**Mebane Faber: "Relative Strength Strategies for Investing"**
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1585517

> Abstract: The purpose of this paper is to present simple quantitative methods that improve risk-adjusted returns for investing in US equity sectors and global asset class portfolios. A relative strength model is tested on the French-Fama US equity sector data back to the 1920s that results in increased absolute returns with equity-like risk. The relative strength portfolios outperform the buy and hold benchmark in approximately 70% of all years and returns are persistent across time.

## Related Papers

1. Antonacci: "Optimal Momentum" - http://www.naaim.org/files/2011/F2011_OptimalMomentum2_garyantonacci.pdf
2. Kessler, Scherer: "Macro Momentum and the Economy" - https://workspace.imperial.ac.uk/business-school/Public/research/annadvanceshedgefunds5/12_Kessler.pdf
3. Antonacci: "Risk Premia Harvesting Through Dual Momentum" - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2042750
4. Keller, Van Putten: "Generalized Momentum and Flexible Asset Allocation (FAA)" - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2193735
5. Geczy, Samonov: "215 Years of Global Multi-Asset Momentum" - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2607730

## Keywords

momentum, asset class picking, rotational system

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/asset-class-momentum-rotational-system/
#
# Use 5 ETFs (SPY - US stocks, EFA - foreign stocks, IEF - bonds, VNQ - REITs, GSG - commodities).
# Pick 3 ETFs with strongest 12 month momentum into your portfolio and weight them equally.
# Hold for 1 month and then rebalance.

from AlgorithmImports import *

class MomentumAssetAllocationStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)

        self.data: dict[str, RateOfChange] = {}
        period: int = 12 * 21  # 12 months
        self.SetWarmUp(period, Resolution.Daily)

        self.traded_count: int = 3
        self.symbols: List[str] = ["SPY", "EFA", "IEF", "VNQ", "GSG"]

        for symbol in self.symbols:
            self.AddEquity(symbol, Resolution.Minute)
            self.data[symbol] = self.ROC(symbol, period, Resolution.Daily)

        self.recent_month: int = -1

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        if not (self.Time.hour == 9 and self.Time.minute == 31):
            return

        # Rebalance once a month
        if self.Time.month == self.recent_month:
            return
        self.recent_month = self.Time.month

        # Select assets with valid data
        selected: dict[str, RateOfChange] = {}
        for symbol, roc in self.data.items():
            if symbol in data and data[symbol] and roc.IsReady:
                selected[symbol] = roc

        # Sort by momentum (ROC)
        sorted_by_momentum = sorted(
            selected.items(),
            key=lambda x: x[1].Current.Value,
            reverse=True
        )

        # Pick top N
        long: List[str] = []
        if len(sorted_by_momentum) >= self.traded_count:
            long = [x[0] for x in sorted_by_momentum][:self.traded_count]

        # Liquidate positions not in long list
        invested = [x.Key.Value for x in self.Portfolio if x.Value.Invested]
        for symbol in invested:
            if symbol not in long:
                self.Liquidate(symbol)

        # Equal weight allocation
        for symbol in long:
            self.SetHoldings(symbol, 1 / len(long))
```

## Implementation Notes

- The strategy uses 12-month (252 trading days) momentum
- Rebalancing happens at market open on the first trading day of each month
- Top 3 assets are selected regardless of whether momentum is positive or negative
- Consider adding absolute momentum filter (only go long if momentum > 0)

## Epoch Implementation

**Period**: 2007-01-01 to 2025-12-31 (limited by BND ETF inception 2007-04-10)
- QuantConnect code uses 2000-01-01 but BND didn't exist then

**Asset Change**: Using BND (Total Bond Market ETF) instead of IEF (7-10 Year Treasury Bond ETF)
- Matches Quantpedia text description
- Both provide fixed income exposure
