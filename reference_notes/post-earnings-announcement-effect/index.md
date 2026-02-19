# Post-Earnings Announcement Effect

**Quantpedia ID**: #0033
**URL**: https://quantpedia.com/strategies/post-earnings-announcement-effect
**Status**: ELIGIBLE
**Linear Issue**: [ENG-158](https://linear.app/epoch-inc/issue/ENG-158/implement-post-earnings-announcement-effect-0033)

## Overview

The Post-Earnings Announcement Drift (PEAD) is one of the oldest and most robust market anomalies. After earnings are announced, stocks with positive earnings surprises tend to drift upward, while stocks with negative surprises drift downward. The market underreacts to earnings news, creating a trading opportunity in the days/weeks following announcements.

## Trading Rules

**Universe**: All US stocks with earnings announcements
**Signal**: Earnings surprise (actual vs estimated EPS)
**Selection**: Long positive surprises, short negative surprises
**Weighting**: Equal weight
**Rebalancing**: Quarterly (after each earnings season)

### Detailed Rules
1. Track earnings announcements for all stocks
2. Calculate standardized earnings surprise (SUE)
3. On announcement day +1:
   - Long stocks with large positive surprises (top quintile)
   - Short stocks with large negative surprises (bottom quintile)
4. Hold position for ~60 trading days (until next earnings)
5. Rebalance quarterly as new earnings come in

### Signal Calculation
```
SUE = (Actual EPS - Estimated EPS) / StdDev(Surprises)
```
Or simpler:
```
Surprise = (Actual EPS - Estimated EPS) / Estimated EPS
```

## Fundamental Reason

1. **Underreaction**: Investors are slow to fully incorporate earnings news into prices
2. **Confirmation Bias**: Investors anchor to prior beliefs about the company
3. **Analyst Lag**: Analysts slow to update forecasts after surprises
4. **Information Diffusion**: Takes time for news to reach all market participants
5. **Cognitive Biases**: Representativeness heuristic, conservatism

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1987-2004 |
| Return | 15.0% p.a. |
| Max Drawdown | -11.2% |

**Notes**: Classic PEAD documented by Bernard & Thomas (1989).

## Source Paper

**Bernard, Thomas: "Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?"**
- Journal of Accounting Research, 1989

**Abstract**: This paper examines the nature of post-earnings-announcement drift. We find that the drift in stock prices for at least 60 days following earnings announcements and that the drift is predictable based on the sign and magnitude of the earnings surprise.

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/post-earnings-announcement-effect/
#
# Post-Earnings Announcement Drift (PEAD)
# Long positive earnings surprises, short negative surprises

from AlgorithmImports import *
import numpy as np
from typing import List, Dict

class PostEarningsAnnouncementDrift(QCAlgorithm):
    def Initialize(self) -> None:
        self.SetStartDate(2015, 1, 1)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily

        self.AddUniverse(self.FundamentalFilter)

        self.long_symbols: List[Symbol] = []
        self.short_symbols: List[Symbol] = []

        self.earnings_data: Dict[Symbol, float] = {}

        self.Schedule.On(
            self.DateRules.Every(DayOfWeek.Monday),
            self.TimeRules.AfterMarketOpen('SPY'),
            self.Rebalance
        )

    def FundamentalFilter(self, fundamental: List[Fundamental]) -> List[Symbol]:
        # Filter to stocks with recent earnings
        selected = [
            f for f in fundamental
            if f.HasFundamentalData
            and f.EarningReports.BasicAverageShares.ThreeMonths > 0
        ]
        return [f.Symbol for f in selected[:500]]

    def OnData(self, slice: Slice) -> None:
        # Track earnings surprises from events
        pass

    def Rebalance(self) -> None:
        # Select based on recent earnings surprises
        if len(self.earnings_data) < 10:
            return

        sorted_surprises = sorted(
            self.earnings_data.items(),
            key=lambda x: x[1],
            reverse=True
        )

        n_quintile = len(sorted_surprises) // 5
        self.long_symbols = [s for s, _ in sorted_surprises[:n_quintile]]
        self.short_symbols = [s for s, _ in sorted_surprises[-n_quintile:]]

        # Execute trades
        targets = []
        for symbol in self.long_symbols:
            targets.append(PortfolioTarget(symbol, 1.0 / len(self.long_symbols)))
        for symbol in self.short_symbols:
            targets.append(PortfolioTarget(symbol, -1.0 / len(self.short_symbols)))

        self.SetHoldings(targets, True)
```

## Eligibility Check

### Required Capabilities
1. **Earnings Data**: Actual vs estimated EPS, announcement dates
2. **Surprise Calculation**: Compute standardized surprise
3. **Cross-Sectional Ranking**: Select top/bottom quintiles
4. **Event-Based Trading**: Trade after announcements

### Available
- `earnings` data source with:
  - `actual_eps` - Actual reported EPS
  - `estimated_eps` - Consensus estimate
  - `eps_surprise` - Raw surprise (actual - estimated)
  - `eps_surprise_percent` - Percentage surprise
  - `fiscal_period`, `fiscal_year`
  - `importance` rating
- `cs_rank` - Cross-sectional ranking
- Event markers for timing

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **Earnings Data Access**:
   ```
   earn = earnings()
   surprise = earn.eps_surprise_percent
   ```

2. **Signal Generation**:
   ```
   # Positive surprise = bullish
   # Negative surprise = bearish
   long_signal = earn.eps_surprise_percent > 0.05  # >5% beat
   short_signal = earn.eps_surprise_percent < -0.05  # >5% miss
   ```

3. **Cross-Sectional Ranking**:
   ```
   surprise_rank = cs_rank(earn.eps_surprise_percent)
   long_signal = surprise_rank >= percentile_80
   short_signal = surprise_rank <= percentile_20
   ```

4. **Holding Period**:
   - Hold for ~60 days (until next earnings)
   - Or use fixed holding period

5. **Rebalancing**: Use event-based or weekly rebalancing

### Considerations
- PEAD effect has weakened since discovery but still persists
- Transaction costs matter given frequent trading
- Consider market cap and liquidity filters
- Can combine with quality/momentum factors

## Related Strategies

- #0034 Post-Loss/Profit Announcement Drift
- Earnings momentum strategies
- SUE-based strategies

## Related Papers

1. **Bernard, Thomas (1989)**: "Post-Earnings-Announcement Drift"
2. **Ball, Brown (1968)**: "An Empirical Evaluation of Accounting Income Numbers"
3. **Chordia, Shivakumar (2006)**: "Earnings and Price Momentum"
