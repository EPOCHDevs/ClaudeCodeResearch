# Overnight Anomaly

**Quantpedia ID**: #0004
**URL**: https://quantpedia.com/strategies/overnight-anomaly
**Status**: INELIGIBLE
**Linear Issue**: [ENG-15](https://linear.app/epoch-inc/issue/ENG-15/feature-request-market-on-closeopen-order-types-for-overnight)

## Overview
The US equity premium from the mid-90s was due solely to overnight returns. The equity premium in the adjacent open-to-close (daytime) period is zero or even negative, with first hour returns (AM) negative on average. This finding is consistent for equity indices, derived ETFs, derivatives (like futures), and also for individual stocks.

## Trading Rules
**Universe**: SPY ETF (S&P 500 SPDR)
**Signal**: Buy at market close, sell at market open
**Selection**: Single asset (SPY)
**Weighting**: 100% position
**Rebalancing**: Daily (intraday execution)

### Execution Details
1. Place Market-On-Close (MOC) order to buy SPY at ~15:44 ET (16 min before close)
2. Place Market-On-Open (MOO) order to sell SPY at market open next day
3. Repeat daily

## Fundamental Reason
1. Companies started publishing positive earnings surprises outside market hours in mid-90s
2. High opening prices from accumulation of market orders from market participants, which subsequently decline in the first hour of trading
3. Some degree of positive overnight returns from illiquidity premium (though liquidity can explain only a small portion)

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1993-2006 |
| Return | 14% p.a. |
| Volatility | Not stated |
| Max Drawdown | -35.3% |
| Sharpe Ratio | Not stated |

**Notes**: Data from Table 1 Panel C3 for SPY ETF: 0.0536% during night (~14% p.a.) vs. -0.0142% during day (~-3.5% p.a.)

## Source Paper
**Cliff, Cooper, Gulen: "Return Differences between Trading and Non-Trading Hours: Like Night and Day"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1004081

**Abstract**: We use transaction-level data and decompose the US equity premium into day (open to close) and night (close to open) returns. We document the striking result that the US equity premium over the last decade is solely due to overnight returns; the returns during the night are strongly positive, and returns during the day are close to zero and sometimes negative.

## Other Papers
- Branch, Ma: "The Overnight Return, One More Anomaly" (SSRN 937997)
- Berkman, Koch, Tuttle, Zhang: "Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open" (SSRN 1625495)
- Tao, Qiu: "The International Evidence of the Overnight Return Anomaly"
- Haghani, Ragulin, Dewey: "Night Moves: Is the Overnight Drift the Grandmother of All Market Anomalies" (SSRN 4139328)

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/overnight-anomaly/
#
# Buy SPY ETF at its closing price and sell it at the opening each day.
# Trading is simulated with no transaction fees.

from AlgorithmImports import *

class OvernightAnomaly(QCAlgorithm):
    def initialize(self) -> None:
        self.set_start_date(1998, 1, 2)
        self.set_cash(100_000)
        data: Equity = self.add_equity("SPY", Resolution.MINUTE)
        data.set_fee_model(CustomFeeModel())
        self._symbol: Symbol = data.symbol

        # MOC order 16 min before market close
        self.schedule.on(
            self.date_rules.every_day(self._symbol),
            self.time_rules.before_market_close(self._symbol, 16),
            self._before_market_close
        )

        # MOO order 15 min after market close (queued for next day)
        self.schedule.on(
            self.date_rules.every_day(self._symbol),
            self.time_rules.after_market_close(self._symbol, 15),
            self._after_market_close
        )

    def _before_market_close(self) -> None:
        if not self.portfolio.invested:
            q: int = self.portfolio.total_portfolio_value // self.securities[self._symbol].price
            self.market_on_close_order(self._symbol, q, tag='MOC')

    def _after_market_close(self) -> None:
        if self.portfolio[self._symbol].invested:
            q: int = self.portfolio[self._symbol].quantity
            self.market_on_open_order(self._symbol, -q, tag='MOO')

class CustomFeeModel(FeeModel):
    def get_order_fee(self, parameters):
        return OrderFee(CashAmount(0, "USD"))
```

## Eligibility Check

### Available
- **Assets**: SPY-Stocks available
- **Transforms**: session_gap (detects overnight gaps), bar_gap

### Missing (INELIGIBLE)
1. **Market-On-Close (MOC) order type** - Platform doesn't support MOC orders
2. **Market-On-Open (MOO) order type** - Platform doesn't support MOO orders
3. **Intraday execution scheduling** - Cannot schedule orders "16 minutes before market close"
4. **Minute-level execution** - Platform executes on bar close, not at specific intraday times

### Root Cause
The platform's execution model is based on daily (or other timeframe) bars where:
- Signals are evaluated at bar close
- Orders execute at the next bar's open

This strategy requires **within-bar execution** at specific intraday times (market close and market open), which is fundamentally different from the bar-based execution model.

## Alternative Approaches

### 1. Research-Only Implementation
Could implement as a **research study** to measure the overnight vs intraday return differential without actual trading:
```
overnight_return = (open - close >> 1) / (close >> 1)
intraday_return = (close - open) / open
```

### 2. Approximate Daily Implementation
Use daily bars with approximate logic (NOT equivalent to actual strategy):
- Enter at today's close (approximated by daily bar close)
- Exit at tomorrow's open (approximated by next bar's open)
- **Issue**: This doesn't capture the true MOC/MOO timing

### 3. Feature Request
Request implementation of:
- MOC order type
- MOO order type
- Intraday scheduled execution

## Implementation Notes
- Strategy has very high turnover (~252 trades/year per direction)
- Transaction costs significantly impact returns
- Paper shows theoretical potential without fees
- Practical implementation requires careful slippage management
- Strategy marked "Very Complex" due to execution challenges
