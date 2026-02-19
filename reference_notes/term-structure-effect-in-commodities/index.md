# Term Structure Effect in Commodities

**Quantpedia ID**: #0022
**URL**: https://quantpedia.com/strategies/term-structure-effect-in-commodities
**Status**: INELIGIBLE
**Linear Issue**: [ENG-44](https://linear.app/epoch-inc/issue/ENG-44/feature-request-futures-term-structure-carry-data-for-0022)

## Overview

Commodity carry/term structure strategy that exploits the relationship between spot and futures prices. Buys commodities in backwardation (futures price < spot price, positive roll return) and shorts commodities in contango (futures price > spot price, negative roll return). Based on Keynes' theory of normal backwardation where speculators earn a premium for providing insurance to hedgers.

## Trading Rules

**Universe**: ~20 commodity futures
**Signal**: Roll return (near contract price / distant contract price - 1)
**Selection**: Top 20% (long), bottom 20% (short)
**Weighting**: Equal weight within quintiles
**Rebalancing**: Monthly

### Roll Return Calculation
```
roll_return = near_contract_price / distant_contract_price - 1
```
- Positive roll return = backwardation (buy)
- Negative roll return = contango (sell)

## Fundamental Reason

1. **Normal Backwardation Theory**: Keynes (1930) and Cootner (1960) argued that hedgers (net short) transfer risk to speculators who are compensated with positive expected returns.

2. **Convenience Yield**: Backwardated commodities have high convenience yield, reflecting scarcity. Low inventories drive spot prices above futures.

3. **Roll Yield**: Buying backwardated contracts and rolling to next month captures the convergence of futures to spot price.

4. **Lower Drawdowns**: Term structure strategies show lower maximum drawdowns and higher reward-to-risk ratios than momentum strategies.

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1979-2004 |
| Return | 11.73% p.a. |
| Volatility | 23.84% |
| Max Drawdown | -78.06% |
| Sharpe Ratio | 0.49 |

**Notes**: 1-month rebalancing period. Data from Table 3.

## Source Paper

**Fuertes, Miffre, Rallis: "Tactical Allocation in Commodity Futures Markets: Combining Momentum and Term Structure Signals"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1127213

**Abstract**: This paper examines the combined role of momentum and term structure signals for the design of profitable trading strategies in commodity futures markets. With significant annualized alphas of 10.14% and 12.66% respectively, the momentum and term structure strategies appear profitable when implemented individually. With an abnormal return of 21.02%, a novel double-sort strategy that exploits both momentum and term structure signals clearly outperforms the single-sort strategies.

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/term-structure-effect-in-commodities/
#
# This simple strategy buys each month the 20% of commodities with the highest roll-returns
# and shorts the 20% of commodities with the lowest roll-returns.

from AlgorithmImports import *

class TermStructureEffectinCommodities(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2009, 1, 1)
        self.SetCash(100000)

        symbols: Dict[str, str] = {
            'CME_S1': Futures.Grains.Soybeans,
            'CME_W1': Futures.Grains.Wheat,
            'CME_GC1': Futures.Metals.Gold,
            'CME_SI1': Futures.Metals.Silver,
            'CME_CL1': Futures.Energies.CrudeOilWTI,
            'CME_NG1': Futures.Energies.NaturalGas,
            # ... more commodities
        }

        self.futures_info: Dict[str, FuturesInfo] = {}
        self.quantile: int = 5

        for qp_symbol, qc_future in symbols.items():
            future: Future = self.AddFuture(qc_future, Resolution.Daily)
            future.SetFilter(timedelta(days=2), timedelta(days=360))
            self.futures_info[future.Symbol.Value] = FuturesInfo(data.Symbol)

    def OnData(self, slice: Slice) -> None:
        roll_return: Dict[Symbol, float] = {}

        for symbol, futures_info in self.futures_info.items():
            if futures_info.is_initialized():
                near_c = futures_info.near_contract
                dist_c = futures_info.distant_contract

                # Roll return = near_price / distant_price - 1
                raw_price1 = self.Securities[near_c.Symbol].Close
                raw_price2 = self.Securities[dist_c.Symbol].Close

                if raw_price1 != 0 and raw_price2 != 0:
                    roll_return[symbol] = raw_price1 / raw_price2 - 1

        # Rank by roll return, long top 20%, short bottom 20%
        sorted_by_roll = sorted(roll_return.items(), key=lambda x: x[1], reverse=True)
        quantile = int(len(sorted_by_roll) / self.quantile)
        long = [x[0] for x in sorted_by_roll[:quantile]]
        short = [x[0] for x in sorted_by_roll[-quantile:]]
```

## Eligibility Check

### Required Capabilities
1. **Multiple Contract Maturities**: Need access to both near-month and distant-month futures contracts to calculate roll return
2. **Carry/Basis Transform**: A pre-computed term structure signal

### Available
- Commodity futures continuous contracts (GC-Futures, CL-Futures, etc.)
- Cross-sectional ranking (cs_rank)

### MISSING - Why INELIGIBLE

1. **Multiple Maturity Contracts**: Our futures data only provides continuous contracts (single price series per commodity). The strategy requires:
   - Near-month contract price (F1)
   - Distant-month contract price (F2)
   - Roll return = F1/F2 - 1

2. **Carry/Basis/Term Structure Transform**: No transform exists to calculate:
   - Roll return
   - Basis (spot - futures)
   - Term structure slope

### Feature Request Required
To implement this strategy, the platform needs one of:
- **Option A**: Individual futures contract expiry data (F1, F2, F3 per commodity)
- **Option B**: Pre-computed "carry" or "roll_return" transform for continuous contracts

## Implementation Notes

If multi-maturity data becomes available:
1. **Universe**: Use available commodity futures from assets.json
2. **Signal**: Calculate roll_return = near_price / far_price - 1
3. **Ranking**: Use cs_rank(roll_return)
4. **Selection**:
   - Long: cs_rank <= N/5 (highest roll return = backwardation)
   - Short: cs_rank > 4*N/5 (lowest roll return = contango)
5. **Rebalancing**: Monthly

## Related Strategies

- #0021 Momentum Effect in Commodities (ELIGIBLE)
- #0023 Momentum + Term Structure Combined (depends on #0022)
