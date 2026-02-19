# Market Seasonality Effect in World Equity Indexes

**Quantpedia ID**: #0031
**URL**: https://quantpedia.com/strategies/market-seasonality-effect-in-world-equity-indexes
**Status**: ELIGIBLE
**Linear Issue**: [ENG-139](https://linear.app/epoch-inc/issue/ENG-139/implement-market-seasonality-effect-in-world-equity-indexes-0031)

## Overview

Classic "Sell in May and Go Away" strategy (also known as the Halloween Effect). The strategy exploits the well-documented pattern that equity markets tend to perform better from November to April and underperform from May to October. By being long only during the favorable months, the strategy captures seasonal alpha while reducing drawdowns.

## Trading Rules

**Universe**: World equity indexes (S&P 500, international indexes)
**Signal**: Calendar month
**Selection**: Long during favorable months, cash during unfavorable
**Weighting**: All-in or cash
**Rebalancing**: Semi-annual (May and November)

### Detailed Rules
1. At the end of October: Go long equity indexes
2. Hold from November through April (6 months)
3. At the end of April: Exit to cash
4. Stay in cash from May through October (6 months)
5. Repeat annually

### Calendar
- **Long Months**: November, December, January, February, March, April
- **Cash Months**: May, June, July, August, September, October

## Fundamental Reason

1. **Holiday Effect**: Strong performance around year-end holidays (Christmas, New Year)
2. **Tax-Loss Selling**: January effect from tax-related selling in December
3. **Bonus Investments**: Year-end bonuses invested in January
4. **Summer Lull**: Reduced trading activity during vacation months
5. **Behavioral Patterns**: Investor sentiment and attention cycles

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1970-2003 |
| Return | 8.8% p.a. |
| Max Drawdown | -36.58% |

**Notes**: Data from Bouman and Jacobsen (2002) research.

## Source Paper

**Bouman, Jacobsen: "The Halloween Indicator, 'Sell in May and Go Away'"**
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=76248

**Abstract**: We document a strong seasonal effect in stock returns that is puzzling given rational asset pricing. Across 37 countries stock market returns are significantly higher in the period November-April than in May-October.

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/market-seasonality-effect-in-world-equity-indexes/
#
# "Sell in May and Go Away" / Halloween Effect
# Long equities November-April, cash May-October

from AlgorithmImports import *

class MarketSeasonalityEffect(QCAlgorithm):
    def Initialize(self) -> None:
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100_000)

        self.spy = self.AddEquity('SPY', Resolution.Daily).Symbol

        # Long months: November (11) through April (4)
        self.long_months = [11, 12, 1, 2, 3, 4]

        # Schedule rebalancing at start of each month
        self.Schedule.On(
            self.DateRules.MonthStart('SPY'),
            self.TimeRules.AfterMarketOpen('SPY'),
            self.Rebalance
        )

    def Rebalance(self) -> None:
        current_month = self.Time.month

        if current_month in self.long_months:
            # Long during favorable months
            self.SetHoldings(self.spy, 1.0)
        else:
            # Cash during unfavorable months
            self.Liquidate()

    def OnData(self, slice: Slice) -> None:
        pass  # All logic in scheduled rebalance
```

## Eligibility Check

### Required Capabilities
1. **Calendar/Month Detection**: Identify current month for switching
2. **Equity Index Data**: S&P 500 or world equity indexes
3. **Position Switching**: Ability to go long or flat

### Available
- `month_of_year` - Detects specific months of the year
- `quarter` - Detects quarters (alternative approach)
- `week_of_month` - Finer-grained calendar detection
- SPY and international equity ETFs available
- Position sizing and rebalancing controls

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **Month Detection**:
   ```
   # Check if in "winter" months (Nov-Apr)
   is_nov = month_of_year(month='November')
   is_dec = month_of_year(month='December')
   is_jan = month_of_year(month='January')
   is_feb = month_of_year(month='February')
   is_mar = month_of_year(month='March')
   is_apr = month_of_year(month='April')

   long_signal = is_nov OR is_dec OR is_jan OR is_feb OR is_mar OR is_apr
   ```

2. **Alternative - Quarter-Based**:
   ```
   # Q4 + Q1 approximation
   is_q4 = quarter(quarter='Q4')
   is_q1 = quarter(quarter='Q1')
   long_signal = is_q4 OR is_q1
   ```

3. **Position Sizing**:
   ```
   weight = conditional_select(long_signal, 1.0, 0.0)
   ```

4. **Rebalancing**: Use `rebalance_interval='monthly'` with the month check

### Considerations
- Effect has weakened over time as it became widely known
- Consider combining with other signals for robustness
- Transaction costs are minimal (2 trades per year)
- Can be enhanced by varying leverage based on other factors

## Related Strategies

- #0032 Combining Seasonality and Momentum in US Equity Sectors
- Turn of the month effect
- January effect strategies

## Related Papers

1. **Bouman, Jacobsen (2002)**: "The Halloween Indicator, Sell in May and Go Away"
2. **Jacobsen, Visaltanachoti (2009)**: "The Halloween Effect in U.S. Sectors"
3. **Andrade, Chhaochharia, Fuerst (2013)**: "Sell in May and Go Away Just Won't Go Away"
