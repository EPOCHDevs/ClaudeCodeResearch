# Momentum Effect Combined with Term Structure in Commodities

**Quantpedia ID**: #0023
**URL**: https://quantpedia.com/strategies/momentum-effect-combined-with-term-structure-in-commodities
**Status**: INELIGIBLE
**Linear Issue**: [ENG-44](https://linear.app/epoch-inc/issue/ENG-44/feature-request-futures-term-structure-carry-data-for-0022) (blocked by same feature)

## Overview

Double-sort strategy that combines both momentum and term structure signals in commodity futures. First sorts commodities by roll return (term structure), then within each tercile sorts by past momentum. Buys "High-Winner" (high roll return + strong momentum) and shorts "Low-Loser" (low roll return + weak momentum). Significantly outperforms either factor alone with 21.8% annual return vs. ~10-12% for individual factors.

## Trading Rules

**Universe**: ~30 commodity futures
**Signal 1**: Roll return (term structure)
**Signal 2**: 1-month momentum (past return)
**Selection**: Double-sort methodology
**Weighting**: Equal weight
**Rebalancing**: Monthly

### Detailed Rules
1. Compute roll-returns for each commodity future at month end
2. Split futures into 3 portfolios by roll return: Low, Mid, High
3. Within High portfolio, sort by past month return:
   - High-Winner: highest roll return + best momentum
   - High-Loser: highest roll return + worst momentum
4. Within Low portfolio, sort by past month return:
   - Low-Winner: lowest roll return + best momentum
   - Low-Loser: lowest roll return + worst momentum
5. **Long**: High-Winner portfolio
6. **Short**: Low-Loser portfolio
7. Hold for one month

## Fundamental Reason

1. **Double Alpha**: Combines two independent sources of abnormal returns
2. **Momentum Effect**: Exploits price continuation (behavioral underreaction)
3. **Term Structure Effect**: Captures risk premium from backwardation/contango
4. **Synergy**: High-Winner = backwardated AND trending up = strongest signal
5. **Diversification**: Returns uncorrelated with traditional asset classes

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1979-2004 |
| Return | 21.8% p.a. |
| Volatility | 27.6% |
| Max Drawdown | -83.35% |
| Sharpe Ratio | 0.79 |

**Notes**: 1-month holding period, 1-month ranking period. Data from Table 6.

**Comparison to Single Factors**:
- Momentum alone: 10.14% alpha
- Term Structure alone: 12.66% alpha
- Combined: 21.02% alpha

## Source Paper

**Fuertes, Miffre, Rallis: "Tactical Allocation in Commodity Futures Markets: Combining Momentum and Term Structure Signals"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1127213

**Abstract**: This paper examines the combined role of momentum and term structure signals for the design of profitable trading strategies in commodity futures markets. With significant annualized alphas of 10.14% and 12.66% respectively, the momentum and term structure strategies appear profitable when implemented individually. With an abnormal return of 21.02%, a novel double-sort strategy that exploits both momentum and term structure signals clearly outperforms the single-sort strategies.

## Eligibility Check

### Required Capabilities
1. **Momentum (ROC)**: Available - roc transform exists
2. **Term Structure (Roll Return)**: NOT Available - requires multi-maturity futures data

### Available
- Momentum transforms: roc, cs_momentum
- Cross-sectional ranking: cs_rank
- Commodity futures: 288 continuous contracts

### MISSING - Why INELIGIBLE

**Same as #0022**: Term structure / roll return calculation requires:
- Near-month contract price (F1)
- Distant-month contract price (F2)
- Roll return = F1/F2 - 1

Our platform only has continuous contracts, not individual expiry data.

### Blocked By
- ENG-44: [Feature Request] Futures Term Structure / Carry Data

## Implementation Notes

If term structure data becomes available:

1. **First Sort (Term Structure)**:
   ```
   roll_return = near_price / far_price - 1
   tercile = cs_rank(roll_return) / count(universe) * 3
   high_roll = tercile >= 2
   low_roll = tercile < 1
   ```

2. **Second Sort (Momentum)**:
   ```
   momentum = roc(close, 21)  # 1-month
   # Within high_roll group:
   high_winner = high_roll AND cs_rank(momentum, mask=high_roll) <= N/2
   # Within low_roll group:
   low_loser = low_roll AND cs_rank(momentum, mask=low_roll) > N/2
   ```

3. **Signal**:
   ```
   long_signal = high_winner
   short_signal = low_loser
   ```

## Related Strategies

- #0021 Momentum Effect in Commodities (ELIGIBLE)
- #0022 Term Structure Effect in Commodities (INELIGIBLE - same blocker)
