# Size Factor - Small Capitalization Stocks Premium

**Quantpedia ID**: #0025
**URL**: https://quantpedia.com/strategies/small-capitalization-stocks-premium-anomaly
**Status**: ELIGIBLE
**Linear Issue**: [ENG-47](https://linear.app/epoch-inc/issue/ENG-47/implement-size-factor-small-cap-premium-0025)

## Overview

The small-capitalization stocks premium (size effect) is one of the most well-documented anomalies in finance. It states that low capitalization stocks earn substantial premiums against stocks with large capitalization without additional risk. This anomaly was first described in the classical Fama and French (1993) research paper. Pure small-cap effect portfolios go long stocks with the lowest capitalization and short stocks with the largest capitalization.

Note: The pure small-cap long/short strategy had significant drawdowns (~80% in the 90s), but small-cap exposure remains a strong performance contributor in long-only portfolios and as a catalyst for other factors.

## Trading Rules

**Universe**: All NYSE, AMEX, and NASDAQ stocks
**Signal**: Market capitalization ranking
**Selection**: Bottom decile (long), top decile (short)
**Weighting**: Equal weight within each decile
**Rebalancing**: Yearly

### Detailed Rules
1. Create a universe of all tradable stocks on NYSE, AMEX, NASDAQ
2. Rank stocks by market capitalization at year end
3. Form decile portfolios based on market cap
4. **Long**: Stocks in the smallest decile (bottom 10%)
5. **Short**: Stocks in the largest decile (top 10%)
6. Hold for one year, rebalance annually

## Fundamental Reason

1. **Illiquidity Premium**: Small companies have higher trading costs, compensating investors with higher returns
2. **Growth Potential**: Smaller companies have more room to grow compared to large caps
3. **Flexibility**: Greater agility during business cycles and economic changes
4. **Innovation**: Higher inside innovation gives small-caps an advantage
5. **Higher Risk**: Simply higher risk involved in small-cap companies (risk premium)

## Performance (Source Paper: Alquist, Israel, Moskowitz 2018)

| Metric | Value |
|--------|-------|
| Period | 1926-2017 |
| Return | 6.1% p.a. |
| Volatility | 25.6% |
| Max Drawdown | -39.68% |
| Sharpe Ratio | 0.24 |

**Notes**: Data from table on page 8. OOS performance shows deteriorating alpha.

**QuantConnect Out-of-Sample (2000-2025)**:
| Metric | Value |
|--------|-------|
| CAGR | 2.94% |
| Sharpe Ratio | 0.0 |
| Drawdown | 37% |
| Win Rate | 44% |

## Source Paper

**Alquist, Israel, Moskowitz: "Fact, Fiction, and Size Effect"**
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3177539

**Abstract**: In the earliest days of empirical work in academic finance, the size effect was the first market anomaly to challenge the standard asset pricing model and prompt debates about market efficiency. The notion that small stocks have higher average returns than large stocks, even after risk-adjustment, was a pathbreaking discovery. Despite its long and illustrious history in academia and its commonplace acceptance in practice, there is still confusion and debate about the size effect. We examine many claims about the size effect and aim to clarify some of the misunderstanding surrounding it.

## QuantConnect Reference Code

```python
# https://quantpedia.com/strategies/small-capitalization-stocks-premium-anomaly/
#
# The investment universe contains all NYSE, AMEX, and NASDAQ stocks. Decile portfolios are formed based on the market capitalization
# of stocks. To capture "size" effect, SMB portfolio goes long small stocks (lowest decile) and short big stocks (highest decile).
#
# QC implementation changes:
# - The investment universe contains 3000 largest stocks traded on NYSE, AMEX, and NASDAQ with price >= 2$.

from AlgorithmImports import *
from typing import List

class SizeFactorSmallCapitalizationStocksPremium(QCAlgorithm):
    def Initialize(self) -> None:
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100_000)
        self.UniverseSettings.Leverage = 5
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.FundamentalFunction)
        self.Settings.MinimumOrderMarginPortfolioPercentage = 0.0

        self.long_symbols: List[Symbol] = []
        self.short_symbols: List[Symbol] = []

        # Fundamental Filter Parameters
        self.exchange_codes: List[str] = ['NYS', 'NAS', 'ASE']
        self.fundamentals_count: int = 3_000
        self.min_share_price: float = 2.
        self.quantile: int = 10
        self.rebalancing_month: int = 12

        self.selection_flag: bool = True

        exchange: Symbol = self.AddEquity('SPY', Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.MonthEnd(exchange), self.TimeRules.AfterMarketOpen(exchange), self.Selection)
        self.settings.daily_precise_end_time = False

    def FundamentalFunction(self, fundamental: List[Fundamental]) -> List[Symbol]:
        if not self.selection_flag:
            return Universe.Unchanged

        filtered: List[Fundamental] = [
            f for f in fundamental
            if f.HasFundamentalData
            and f.SecurityReference.ExchangeId in self.exchange_codes
            and f.price >= self.min_share_price
        ]

        sorted_by_market_cap: List[Fundamental] = sorted(
            filtered, key = lambda x: x.MarketCap, reverse=True)[:self.fundamentals_count]

        if len(sorted_by_market_cap) >= self.quantile:
            quintile: int = int(len(sorted_by_market_cap) / self.quantile)
            self.long_symbols = [i.Symbol for i in sorted_by_market_cap[-quintile:]]
            self.short_symbols = [i.Symbol for i in sorted_by_market_cap[:quintile]]

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
1. **Market Cap Data**: Needed to rank stocks by size
2. **Cross-Sectional Ranking**: Needed to select deciles
3. **Stock Universe**: Need broad US stock coverage

### Available
- `finance_ratio(ratio_type='market_cap')` - Calculates market cap from fundamental data
- `cs_rank` - Cross-sectional ranking transform
- 13,145 stocks in asset universe (NYSE, NASDAQ, AMEX coverage)

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **Universe**: Use available stocks filtered by exchange
   - Filter: `exchange IN ('NYSE', 'NASDAQ', 'AMEX')`

2. **Signal Calculation**: Use `finance_ratio(ratio_type='market_cap')` to get market cap

3. **Ranking**: Use `cs_rank(market_cap)` to rank stocks cross-sectionally

4. **Selection**:
   - Long: `cs_rank(market_cap) <= N/10` (smallest decile)
   - Short: `cs_rank(market_cap) > 9*N/10` (largest decile)

5. **Weighting**: Equal weight within each decile using `equal_weight()`

6. **Rebalancing**: Yearly using `rebalance_interval='yearly'`

### Considerations
- OOS performance shows deteriorating alpha (Sharpe ~0.0 since 2000)
- Consider controlling for quality/junk factors (Asness et al. research shows this revives size premium)
- May be more useful as a catalyst for other factors (value, momentum) than as standalone strategy

## Related Strategies

- #0028 Value and Momentum Factors Across Asset Classes
- #0013 Short Term Reversal Effect in Stocks
- Fama-French factor strategies

## Related Papers

1. **Fama, French (1992)**: "The Cross-Section of Expected Stock Returns"
2. **Asness, Frazzini, Israel, Moskowitz, Pedersen**: "Size Matters, If You Control Your Junk"
3. **Israel, Moskowitz**: "The Role of Shorting, Firm Size, and Time on Market Anomalies"
