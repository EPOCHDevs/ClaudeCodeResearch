# Momentum Effect in Commodities

**Quantpedia ID**: #0021
**URL**: https://quantpedia.com/strategies/momentum-effect-in-commodities
**Status**: ELIGIBLE
**Linear Issue**: [ENG-43](https://linear.app/epoch-inc/issue/ENG-43/implement-momentum-effect-in-commodities-0021)

## Overview

Commodity futures momentum strategy that exploits short-term price continuation in commodity markets. Based on Miffre & Rallis research showing that momentum strategies consistently profit by buying backwardated contracts (winners) and selling contangoed contracts (losers). The strategy ranks commodity futures by 12-month performance and holds positions for 1 month. Momentum returns have low correlations with traditional asset classes, making commodity-based relative-strength portfolios excellent candidates for diversified portfolios.

## Trading Rules

**Universe**: ~30 commodity futures (grains, meats, metals, energies, softs)
**Signal**: 12-month Rate of Change (ROC) ranking
**Selection**: Top quintile (long), bottom quintile (short)
**Weighting**: Equal weight within each quintile
**Rebalancing**: Monthly

### Detailed Rules
1. Create a universe of tradable commodity futures
2. Rank futures performance for each commodity for the last 12 months
3. Divide ranked commodities into quintiles
4. Go long on the quintile with the highest momentum
5. Go short on the quintile with the lowest momentum
6. Rebalance each month

## Fundamental Reason

1. **Backwardation/Contango Relationship**: Momentum profits are linked to buying backwardated contracts and selling contangoed contracts, related to Keynes (1930) and Hicks (1939) theory of normal backwardation.

2. **Behavioral Underreaction**: Market participants irrationally underreact to information and trends, consistent with behavioral finance models.

3. **Low Transaction Costs**: Commodity markets trade liquid contracts with nearby maturities, minimizing implementation costs.

4. **No Short-Selling Restrictions**: Unlike equities, commodity futures have no short-selling constraints.

5. **Concentrated Universe**: Only ~31 commodities (vs. thousands of stocks) means abnormal returns less likely to be eroded by implementation costs.

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1979-2004 |
| Return | 14.6% p.a. |
| Volatility | 25.57% |
| Max Drawdown | -79.75% |
| Sharpe Ratio | 0.57 |

**Notes**: 12-month ranking period, 1-month holding period. Data from Table 1.

## Source Paper

**Miffre, Rallis: "Momentum in Commodity Futures Markets"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=702281

**Abstract**: The article tests for the presence of short-term continuation and long-term reversal in commodity futures prices. While contrarian strategies do not work, the article identifies 13 profitable momentum strategies that generate 9.38% average return a year. A closer analysis reveals we buy backwardated contracts and sell contangoed contracts with high volatilities. The correlation between the momentum returns and the returns of traditional asset classes is also found to be low.

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/1-month-momentum-in-commodities/
#
# Create a universe of tradable commodity futures. Rank futures performance for each commodity
# for the last 12 months and divide them into quintiles.
# Go long on the quintile with the highest momentum and go short on the quintile with the
# lowest momentum. Rebalance each month.

from AlgorithmImports import *

class MomentumEffectCommodities(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)

        tickers: List[str] = [
            "CME_S1",   # Soybean Futures
            "CME_W1",   # Wheat Futures
            "CME_SM1",  # Soybean Meal Futures
            "CME_BO1",  # Soybean Oil Futures
            "CME_C1",   # Corn Futures
            "CME_O1",   # Oats Futures
            "CME_LC1",  # Live Cattle Futures
            "CME_FC1",  # Feeder Cattle Futures
            "CME_LN1",  # Lean Hog Futures
            "CME_GC1",  # Gold Futures
            "CME_SI1",  # Silver Futures
            "CME_PL1",  # Platinum Futures
            "CME_CL1",  # Crude Oil Futures
            "CME_HG1",  # Copper Futures
            "CME_LB1",  # Lumber Futures
            "CME_NG1",  # Natural Gas Futures
            "CME_PA1",  # Palladium Futures
            "CME_RR1",  # Rough Rice Futures
            "CME_DA1",  # Class III Milk Futures
            "ICE_RS1",  # Canola Futures
            "ICE_GO1",  # Gas Oil Futures
            "CME_RB2",  # Gasoline Futures
            "CME_KW2",  # Wheat Kansas Futures
            "ICE_WT1",  # WTI Crude Futures
            "ICE_CC1",  # Cocoa Futures
            "ICE_CT1",  # Cotton Futures
            "ICE_KC1",  # Coffee Futures
            "ICE_O1",   # Heating Oil Futures
            "ICE_OJ1",  # Orange Juice Futures
            "ICE_SB1",  # Sugar Futures
        ]

        self.period: int = 12 * 21  # 12 months in trading days
        self.quantile: int = 5

        self.SetWarmUp(self.period, Resolution.Daily)

        self.data: Dict[Symbol, RateOfChange] = {}
        for ticker in tickers:
            data: Security = self.AddData(QuantpediaFutures, ticker, Resolution.Daily)
            data.SetFeeModel(CustomFeeModel())
            data.SetLeverage(5)
            self.data[data.Symbol] = self.ROC(ticker, self.period, Resolution.Daily)

        self.recent_month: int = -1

    def OnData(self, slice: Slice) -> None:
        if self.IsWarmingUp:
            return

        # Rebalance once a month
        if self.recent_month == self.Time.month:
            return
        self.recent_month = self.Time.month

        perf: Dict[Symbol, float] = {
            x[0]: x[1].Current.Value for x in self.data.items()
            if self.data[x[0]].IsReady and x[0] in slice and slice[x[0]]
        }

        long: List[Symbol] = []
        short: List[Symbol] = []

        if len(perf) >= self.quantile:
            sorted_by_performance: List[Symbol] = sorted(perf, key=perf.get, reverse=True)
            quintile: int = int(len(sorted_by_performance) / self.quantile)
            long = sorted_by_performance[:quintile]
            short = sorted_by_performance[-quintile:]

        # Trade execution
        invested: List[Symbol] = [x.Key for x in self.Portfolio if x.Value.Invested]
        for symbol in invested:
            if symbol not in long + short:
                self.Liquidate(symbol)

        for symbol in long:
            self.SetHoldings(symbol, 1 / len(long))
        for symbol in short:
            self.SetHoldings(symbol, -1 / len(short))
```

## Eligibility Check

### Available Transforms
- `roc` - Rate of Change (for 12-month momentum calculation)
- `cs_momentum` - Cross-Sectional Momentum (for relative ranking)
- `cs_rank` - Cross-sectional ranking

### Available Assets (288 Futures total)
Key commodities available:
- GC-Futures (Gold)
- SI-Futures (Silver)
- CL-Futures (Crude Oil)
- NG-Futures (Natural Gas)
- HG-Futures (Copper)
- ZC-Futures (Corn)
- ZS-Futures (Soybeans)
- ZW-Futures (Wheat)

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **Universe**: Use available commodity futures from assets.json. Map QuantConnect tickers to Epoch asset IDs.

2. **Signal Calculation**: Use `roc(period=252)` for 12-month momentum (252 trading days).

3. **Ranking**: Use `cs_rank(roc(...))` to rank commodities cross-sectionally.

4. **Selection**:
   - Long: `cs_rank <= N/5` (top quintile)
   - Short: `cs_rank > 4*N/5` (bottom quintile)

5. **Weighting**: Equal weight within each quintile using `equal_weight()`.

6. **Rebalancing**: Monthly using `rebalance_interval='monthly'`.

## Related Strategies

- #0022 Term Structure Effect in Commodities
- #0023 Momentum + Term Structure Combined
- #0028 Value and Momentum Factors Across Asset Classes
