# Value (Book-to-Market) Factor

**Quantpedia ID**: #0026
**URL**: https://quantpedia.com/strategies/value-book-to-market-factor
**Status**: ELIGIBLE
**Linear Issue**: [ENG-52](https://linear.app/epoch-inc/issue/ENG-52/implement-value-book-to-market-factor-0026)

## Overview

The Book-to-Market effect is one of the oldest documented anomalies in financial markets. It compares the book value of a company to the price of the stock (inverse of P/B ratio). The higher the book-to-market ratio, the more fundamentally cheap the company is considered. This anomaly was well-described in the classical Fama-French (1993) research paper.

Pure value effect portfolios go long stocks with the highest B/M ratio and short stocks with the lowest B/M ratio. However, pure value has substantial drawdowns (>50% in 1930s). The value factor remains a strong performance contributor in long-only portfolios.

## Trading Rules

**Universe**: All NYSE, AMEX, and NASDAQ stocks
**Signal**: Book-to-Market ratio (inverse of P/B)
**Selection**: Top quintile (long), bottom quintile (short)
**Weighting**: Equal weight
**Rebalancing**: Monthly

### Detailed Rules
1. Create universe of all stocks on NYSE, AMEX, NASDAQ
2. Calculate Book-to-Market ratio (B/M = 1/P/B)
3. Rank stocks by B/M ratio
4. **Long**: Stocks in highest B/M quintile (cheap/value stocks)
5. **Short**: Stocks in lowest B/M quintile (expensive/growth stocks)
6. Equal-weight within each quintile
7. Rebalance monthly

## Fundamental Reason

1. **Investor Overreaction**: Investors overreact to growth aspects for growth stocks, causing value stocks to be undervalued
2. **Risk Premium**: Low MV/BV stocks are often in financial distress; higher returns compensate for higher risk
3. **Behavioral Bias**: Suboptimal investor behavior creates mispricing opportunities
4. **Mean Reversion**: Cheap stocks tend to revert toward fair value over time

## Performance (Source Paper: Asness, Frazzini, Israel, Moskowitz 2015)

| Metric | Value |
|--------|-------|
| Period | 1926-2014 |
| Return | 3.6% p.a. |
| Volatility | 12.02% |
| Max Drawdown | -55.99% |
| Sharpe Ratio | 0.30 |

**Notes**: From exhibit 5 (HML column).

## Source Paper

**Asness, Frazzini, Israel, Moskowitz: "Fact, Fiction, and Value Investing"**
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2595747

**Abstract**: Value investing has been a part of the investment lexicon for at least the better part of a century. Yet, there are still many areas of confusion about value investing. In this article we aim to clarify many of these matters, focusing in particular on the diversified systematic value strategy, but also exploring how this strategy relates to its more concentrated implementation.

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/value-book-to-market-factor/
#
# The investment universe contains all NYSE, AMEX, and NASDAQ stocks. To represent "value" investing,
# HML portfolio goes long high book-to-price stocks and short low book-to-price stocks.
# The portfolio is equal-weighted and rebalanced monthly.
#
# QC implementation changes:
# - Quintile selection is done.

from AlgorithmImports import *
import numpy as np
from typing import List

class ValueBooktoMarketFactor(QCAlgorithm):
    def Initialize(self) -> None:
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100_000)
        self.UniverseSettings.Leverage = 5
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.FundamentalFunction)
        self.Settings.MinimumOrderMarginPortfolioPercentage = 0.0
        self.settings.daily_precise_end_time = False

        self.long_symbols: List[Symbol] = []
        self.short_symbols: List[Symbol] = []

        # Fundamental Filter Parameters
        self.exchange_codes: List[str] = ['NYS', 'NAS', 'ASE']
        self.quantile: int = 5
        self.rebalancing_month: int = 12

        self.selection_flag: bool = True

        self.exchange: Symbol = self.AddEquity('SPY', Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.MonthEnd(self.exchange), self.TimeRules.AfterMarketOpen(self.exchange), self.Selection)

    def FundamentalFunction(self, fundamental: List[Fundamental]) -> List[Symbol]:
        if not self.selection_flag:
            return Universe.Unchanged

        selected: List[Fundamental] = [
            f for f in fundamental
            if f.HasFundamentalData
            and f.SecurityReference.ExchangeId in self.exchange_codes
            and not np.isnan(f.ValuationRatios.PBRatio)
            and f.ValuationRatios.PBRatio != 0
        ]

        if len(selected) >= self.quantile:
            sorted_by_bm: List[Fundamental] = sorted(
                selected, key = lambda x:(1/x.ValuationRatios.PBRatio), reverse=True
            )
            quantile: int = int(len(sorted_by_bm) / self.quantile)
            self.long_symbols = [i.Symbol for i in sorted_by_bm[:quantile]]
            self.short_symbols = [i.Symbol for i in sorted_by_bm[-quantile:]]

        return self.long_symbols + self.short_symbols

    def OnData(self, slice: Slice) -> None:
        if not self.selection_flag:
            return
        self.selection_flag = False

        # Trade execution - Leveraged portfolio - 100% long, 100% short
        targets: List[PortfolioTarget] = []
        for i, portfolio in enumerate([self.long_symbols, self.short_symbols]):
            for symbol in portfolio:
                if slice.ContainsKey(symbol) and slice[symbol] is not None:
                    targets.append(PortfolioTarget(symbol, ((-1) ** i) / len(portfolio)))

        self.SetHoldings(targets, True)
        self.long_symbols.clear()
        self.short_symbols.clear()

    def Selection(self) -> None:
        if self.Time.month == self.rebalancing_month:
            self.selection_flag = True

    def OnSecuritiesChanged(self, changes: SecurityChanges) -> None:
        for security in changes.AddedSecurities:
            security.SetFeeModel(CustomFeeModel())


# Custom fee model
class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters: OrderFeeParameters) -> OrderFee:
        fee: float = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))
```

## Eligibility Check

### Required Capabilities
1. **Book-to-Market Ratio**: Needed to identify value vs growth stocks
2. **Cross-Sectional Ranking**: Needed to select quintiles
3. **Stock Universe**: Need broad US stock coverage

### Available
- `finance_ratio(ratio_type='book_to_market')` - Calculates B/M ratio
- `finance_ratio(ratio_type='price_to_book')` - Calculates P/B ratio (invert for B/M)
- `cs_rank` - Cross-sectional ranking transform
- 13,145 stocks in asset universe

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **Universe**: Use available stocks filtered by exchange
   - Filter: `exchange IN ('NYSE', 'NASDAQ', 'AMEX')`

2. **Signal Calculation**:
   - Option 1: Use `finance_ratio(ratio_type='book_to_market')` directly
   - Option 2: Use `1 / finance_ratio(ratio_type='price_to_book')`

3. **Ranking**: Use `cs_rank(book_to_market)` to rank stocks cross-sectionally

4. **Selection**:
   - Long: `cs_rank(B/M) > 4*N/5` (highest B/M quintile - value stocks)
   - Short: `cs_rank(B/M) <= N/5` (lowest B/M quintile - growth stocks)

5. **Weighting**: Equal weight within each quintile

6. **Rebalancing**: Monthly using `rebalance_interval='monthly'`

### Considerations
- Value has underperformed recently (since ~2007) - see Lev & Srivastava (2019)
- Consider combining with quality/momentum factors for better performance
- Long-only value may be more practical than long/short

## Related Strategies

- #0025 Size Factor - Small Capitalization Stocks Premium
- #0028 Value and Momentum Factors Across Asset Classes
- #0014 Momentum Factor Effect in Stocks

## Related Papers

1. **Fama, French (1992)**: "The Cross-Section of Expected Stock Returns"
2. **Asness, Frazzini (2013)**: "The Devil in HML's Details"
3. **Arnott, Harvey, et al. (2020)**: "Reports of Value's Death May Be Greatly Exaggerated"
