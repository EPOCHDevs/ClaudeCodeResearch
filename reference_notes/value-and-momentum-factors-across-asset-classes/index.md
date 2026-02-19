# Value and Momentum Factors Across Asset Classes

**Quantpedia ID**: #0028
**URL**: https://quantpedia.com/strategies/value-and-momentum-factors-across-asset-classes
**Status**: ELIGIBLE
**Linear Issue**: [ENG-100](https://linear.app/epoch-inc/issue/ENG-100/implement-value-and-momentum-factors-across-asset-classes-0028)

## Overview

Multi-asset tactical allocation strategy that combines value and momentum factors across stocks, bonds, and REITs. The strategy exploits the observation that value and momentum effects exist not just in individual stocks but across asset classes. By combining these two complementary signals, the strategy achieves diversification benefits since value and momentum tend to be negatively correlated.

## Trading Rules

**Universe**: Multi-asset (US stocks, international stocks, REITs, government bonds, corporate bonds)
**Signal**: Combined value (50%) and momentum (50%) score
**Selection**: Long top quartile, short bottom quartile per asset class
**Weighting**: Equal weight within selection
**Rebalancing**: Monthly

### Signal Components
1. **12-month Momentum** (25% weight): Past 12-month return excluding last month
2. **1-month Momentum** (25% weight): Past 1-month return
3. **Value** (50% weight): Asset class-specific yield measures
   - Stocks: Earnings yield (E/P)
   - Bonds: Yield-to-maturity or credit spread
   - REITs: Dividend yield

### Trading Logic
1. Calculate momentum signals (12-month and 1-month returns) for each asset
2. Calculate value signal (yield measure) for each asset
3. Combine signals: 0.25 * mom_12m + 0.25 * mom_1m + 0.50 * value
4. Rank assets by combined score within each asset class
5. Long top quartile, short bottom quartile
6. Equal weight positions
7. Rebalance monthly

## Fundamental Reason

1. **Momentum Effect**: Price trends persist across asset classes due to slow information diffusion
2. **Value Effect**: High-yield assets tend to outperform as prices mean-revert to fundamentals
3. **Negative Correlation**: Value and momentum are negatively correlated, providing diversification
4. **Cross-Asset Diversification**: Applying factors across multiple asset classes reduces strategy risk

## Performance (Source Paper: Asness, Moskowitz, Pedersen 2013)

| Metric | Value |
|--------|-------|
| Period | 1986-2007 |
| Return | 11.9% p.a. |
| Volatility | 10.0% |
| Sharpe Ratio | 0.79 |

**Notes**: From AQR research paper "Value and Momentum Everywhere"

## Source Paper

**Asness, Moskowitz, Pedersen: "Value and Momentum Everywhere"**
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2174501

**Abstract**: We study the relationship between value and momentum return premia across eight diverse markets and asset classes. We find consistent value and momentum return premia in every asset class. Moreover, we find that value and momentum are negatively correlated across and within asset classes.

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/value-and-momentum-factors-across-asset-classes/
#
# Multi-asset strategy combining value and momentum across:
# - US stocks (SPY), International stocks (EFA, EEM)
# - Government bonds (TLT, IEF), Corporate bonds (LQD, HYG)
# - REITs (VNQ)
#
# Signal: 25% * 12m momentum + 25% * 1m momentum + 50% * value
# Selection: Long top quartile, short bottom quartile

from AlgorithmImports import *
import numpy as np
from typing import List, Dict

class ValueMomentumAcrossAssetClasses(QCAlgorithm):
    def Initialize(self) -> None:
        self.SetStartDate(2007, 1, 1)
        self.SetCash(100_000)

        # Multi-asset ETF universe
        self.etf_tickers = [
            'SPY',   # US Large Cap
            'EFA',   # International Developed
            'EEM',   # Emerging Markets
            'TLT',   # Long-term Treasuries
            'IEF',   # Intermediate Treasuries
            'LQD',   # Investment Grade Corporate
            'HYG',   # High Yield Corporate
            'VNQ',   # REITs
        ]

        self.symbols = {}
        for ticker in self.etf_tickers:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol

        self.lookback_12m = 252
        self.lookback_1m = 21

        self.Schedule.On(
            self.DateRules.MonthEnd('SPY'),
            self.TimeRules.AfterMarketOpen('SPY'),
            self.Rebalance
        )

    def Rebalance(self) -> None:
        signals = {}

        for ticker, symbol in self.symbols.items():
            history = self.History(symbol, self.lookback_12m + 1, Resolution.Daily)
            if len(history) < self.lookback_12m + 1:
                continue

            prices = history['close'].values

            # 12-month momentum (excluding last month)
            mom_12m = (prices[-22] / prices[0]) - 1

            # 1-month momentum
            mom_1m = (prices[-1] / prices[-22]) - 1

            # Value proxy (using inverse price as simple proxy)
            # Note: Real implementation should use actual yield data
            value = 1 / prices[-1]  # Placeholder

            # Combined signal
            signals[ticker] = 0.25 * mom_12m + 0.25 * mom_1m + 0.50 * value

        if len(signals) < 4:
            return

        # Rank and select
        sorted_signals = sorted(signals.items(), key=lambda x: x[1], reverse=True)
        n_quartile = len(sorted_signals) // 4

        long_tickers = [t for t, s in sorted_signals[:n_quartile]]
        short_tickers = [t for t, s in sorted_signals[-n_quartile:]]

        # Execute trades
        targets = []
        for ticker in long_tickers:
            targets.append(PortfolioTarget(self.symbols[ticker], 1.0 / n_quartile))
        for ticker in short_tickers:
            targets.append(PortfolioTarget(self.symbols[ticker], -1.0 / n_quartile))

        self.SetHoldings(targets, True)
```

## Eligibility Check

### Required Capabilities
1. **Momentum Calculation**: 12-month and 1-month returns
2. **Value Signals**: Earnings yield, dividend yield, bond yields
3. **Multi-Asset ETF Universe**: US, international, bonds, REITs

### Available
- `roc` - Rate of change for momentum signals
- `finance_ratio(ratio_type='earnings_yield')` - Earnings yield for stocks
- `cs_rank` - Cross-sectional ranking
- Multi-asset ETFs: SPY, EFA, EEM, TLT, IEF, LQD, HYG, VNQ all available
- `HighYieldSpread` - Economic indicator for credit spreads

### Partially Available
- Dividend yield for REITs - may need to use price-based proxy or alternative
- Bond ETF yields - may need alternative proxies (like spread indicators)

### Missing
None critical - momentum signals and stock value signals fully available. Bond/REIT value signals may require proxy approaches.

## Implementation Notes

1. **Universe**: Multi-asset ETF approach
   ```
   assets = ['SPY', 'EFA', 'EEM', 'TLT', 'IEF', 'LQD', 'HYG', 'VNQ']
   ```

2. **Momentum Signals**:
   ```
   mom_12m = roc(close, 252) - roc(close, 21)  # 12m ex last month
   mom_1m = roc(close, 21)  # 1 month
   ```

3. **Value Signals**:
   - Stocks: `finance_ratio(ratio_type='earnings_yield')`
   - Bonds: Consider using inverse price momentum as proxy, or HighYieldSpread
   - REITs: Consider using inverse price as proxy

4. **Combined Signal**:
   ```
   signal = 0.25 * z_score(mom_12m) + 0.25 * z_score(mom_1m) + 0.50 * z_score(value)
   ```

5. **Selection**: Use `cs_rank` to identify top/bottom quartiles

6. **Rebalancing**: Monthly using `rebalance_interval='monthly'`

### Considerations
- Simplified version could use momentum-only signals for bonds/REITs
- Alternative: Use credit spread indicators as value proxy for bonds
- Consider separate factor portfolios per asset class before combining

## Related Strategies

- #0014 Momentum Factor Effect in Stocks
- #0021 Momentum Effect in Commodities
- #0026 Value (Book-to-Market) Factor

## Related Papers

1. **Fama, French (1992)**: "The Cross-Section of Expected Stock Returns"
2. **Jegadeesh, Titman (1993)**: "Returns to Buying Winners and Selling Losers"
3. **Asness, Frazzini (2013)**: "The Devil in HML's Details"
