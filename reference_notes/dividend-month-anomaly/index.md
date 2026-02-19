# Dividend Month Anomaly

**Quantpedia ID**: #0019
**URL**: https://quantpedia.com/strategies/dividend-month-anomaly
**Status**: ELIGIBLE
**Linear Issue**: [ENG-27](https://linear.app/epoch-inc/issue/ENG-27/implement-dividend-month-anomaly-0019)

## Overview
Companies have positive abnormal returns in months when a dividend is predicted. The anomaly is as large as the value premium but less volatile. The premium is consistent with price pressure from dividend-seeking investors who bid up prices before dividend payment.

## Trading Rules
**Universe**: NYSE, AMEX, NASDAQ stocks with price > $5 (top 500 by liquidity)
**Signal**: Predicted dividend payment in current month based on historical dividend patterns
**Selection**: Long stocks expected to pay dividend this month
**Weighting**: Equal weighted
**Rebalancing**: Monthly

### Dividend Prediction Logic
A company has a "predicted dividend" in month t if it paid:
- Quarterly dividend in months t-3, t-6, t-9, or t-12
- Semi-annual dividend in months t-6 or t-12
- Annual dividend in month t-12
- Dividend of unknown frequency in months t-3, t-6, t-9, or t-12

## Fundamental Reason
- **Dividend clienteles**: Investors who need dividend income bid up prices before payment
- **Tax treatment**: Different tax rates on dividends create investor preferences
- **Income needs**: Retirees and income funds require dividend streams
- **Positive surprise**: Investors may underestimate probability of dividend maintenance

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1927-2009 |
| Return | 17.9% p.a. |
| Volatility | 20% |
| Max Drawdown | -56.02% |
| Sharpe Ratio | 0.70 |

**OOS Performance (2000-2025)**:
- Return: 8.8% p.a.
- Volatility: 18%
- Sharpe: 0.49
- Max DD: -55.7%

## Source Paper
**Hartzmark, Solomon: "The Dividend Month Premium"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1930620

**Abstract**: We document an asset-pricing anomaly whereby companies have positive abnormal returns in months when a dividend is predicted. Abnormal returns in predicted dividend months are high relative to other companies, and relative to dividend-paying companies in months without a predicted dividend, making risk-based explanations unlikely. The anomaly is as large as the value premium, but less volatile. The premium is consistent with price pressure from dividend-seeking investors.

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/dividend-month-anomaly/
#
# Universe: Top 500 most liquid stocks from NYSE, AMEX, NASDAQ (price > $5)
# Signal: Predict dividend payment based on historical patterns
# Selection: Long stocks with expected dividend this month
# Rebalance: Monthly

class DividendMonthAnomaly(QCAlgorithm):
    def Initialize(self) -> None:
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.FundamentalFunction)

        self.exchange_codes = ['NYS', 'NAS', 'ASE']
        self.min_price = 5
        self.fundamental_count = 500
        self.period = 4  # Track last 4 dividends

        self.divident_dates = {}
        self.selection_flag = False

        exchange = self.AddEquity('SPY', Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.MonthEnd(exchange),
                        self.TimeRules.AfterMarketOpen(exchange),
                        self.Selection)

    def FundamentalFunction(self, fundamental):
        if not self.selection_flag:
            return Universe.Unchanged

        filtered = [
            f for f in fundamental
            if f.HasFundamentalData
            and f.Price > self.min_price
            and f.SecurityReference.ExchangeId in self.exchange_codes
        ]

        sorted_fundamentals = sorted(filtered, key=lambda f: f.DollarVolume, reverse=True)
        return [f.Symbol for f in sorted_fundamentals[:self.fundamental_count]]

    def OnData(self, slice):
        # Update dividend dates from slice.Dividends
        for symbol, dividend in slice.Dividends.items():
            if symbol not in self.divident_dates:
                self.divident_dates[symbol] = deque(maxlen=self.period)
            self.divident_dates[symbol].append(self.Time)

        if not self.selection_flag:
            return
        self.selection_flag = False

        long_symbols = []
        for symbol, dates in self.divident_dates.items():
            if len(dates) == self.period:
                # Check if dividend pattern is consistent (quarterly, semi-annual, annual)
                d1 = self.diff_month(self.Time, dates[-1])
                d2 = self.diff_month(self.Time, dates[-2])
                d3 = self.diff_month(self.Time, dates[-3])
                d4 = self.diff_month(self.Time, dates[-4])

                dates_diff = np.diff([d1, d2, d3, d4])

                # Quarterly (3), semi-annual (6), or annual (12) pattern
                if (all(diff == 3 for diff in dates_diff) or
                    all(diff == 6 for diff in dates_diff) or
                    all(diff == 12 for diff in dates_diff)):
                    long_symbols.append(symbol)

        # Equal weight portfolio
        portfolio = []
        for symbol in long_symbols:
            if slice.ContainsKey(symbol) and slice[symbol] is not None:
                portfolio.append(PortfolioTarget(symbol, 1 / len(long_symbols)))

        self.SetHoldings(portfolio, True)

    def Selection(self):
        self.selection_flag = True

    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month
```

## Eligibility Check

### Available
**Data Sources**:
- `dividends()` - Historical dividend data with:
  - `cash_amount` - Dividend amount
  - `split_adjusted_cash_amount` - Adjusted amount
  - `declaration_date` - Announcement date
  - `record_date` - Record date
  - Ex-dividend dates, payment dates
  - Dividend type filtering (CD, LT, SC, ST)

- `market_data_source()` - OHLCV data for:
  - Price filtering (> $5)
  - Volume for liquidity ranking

**Transforms**:
- `cs_rank` - Cross-sectional ranking for liquidity
- `cs_select` - Cross-sectional selection (top N)
- `equal_weight` - Equal weighting
- Time-based lookback for dividend pattern detection

**Universe**:
- US stocks available (NYSE, AMEX, NASDAQ equivalents)

### Implementation Approach
```python
# Get dividend data
div_data = dividends(dividend_type="CD")()

# Track dividend payment months
# Use lag() to check t-3, t-6, t-9, t-12 patterns

# Filter: price > 5
price = market_data_source(timeframe=1D)().c
valid_price = price > 5

# Rank by dollar volume
dollar_volume = price * market_data_source(timeframe=1D)().v
liquidity_rank = cs_rank(ascending=False)(dollar_volume)
top_500 = liquidity_rank <= 500

# Combine filters
universe = valid_price & top_500 & has_predicted_dividend

# Equal weight, monthly rebalance
weight = equal_weight()(active_mask=universe)
is_new_month = time_feature(component=TimeFeature.month)().changed()
position_size(type="percent")(size=weight * 100, rebalance_on=is_new_month)
```

## Implementation Notes
- Strategy trades ~1000 stocks in original paper, QC uses 500 for practicality
- Dividend prediction requires tracking last 4 dividend payments per stock
- Monthly rebalancing at month end
- Long-only strategy (long-short version available in paper)
- High correlation to equity market (0.94)
- Drawdown similar to market during crises

## Risk Considerations
- **Market correlation**: 0.94 correlation to SPY - not a hedge
- **Large drawdowns**: -56% max DD similar to market
- **Dividend cuts**: Strategy assumes dividend continuation
- **Transaction costs**: Monthly rebalancing of large universe
- **Capacity**: Trading many small-cap dividend payers may have liquidity constraints

## Comparison Notes
This is a **seasonality/calendar** strategy based on corporate actions (dividends), not a technical or fundamental factor strategy. Requires tracking dividend payment history and predicting future payments.
