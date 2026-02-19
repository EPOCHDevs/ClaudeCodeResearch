# Volatility Risk Premium Effect

**Quantpedia ID**: #0020
**URL**: https://quantpedia.com/strategies/volatility-risk-premium-effect
**Status**: INELIGIBLE
**Linear Issue**: [ENG-26](https://linear.app/epoch-inc/issue/ENG-26/feature-request-options-trading-for-volatility-risk-premium-0020)

## Overview
The implied volatility from stock options is usually bigger than actual historical volatility. This creates a systematic risk premium that can be earned by selling at-the-money options short-term. Selling put options gives average returns of 0.5% to 1.5% per day, but with extreme negative skewness (potential -800% losses). This is an insurance-selling strategy.

## Trading Rules
**Universe**: S&P 500 index options (SPY)
**Signal**: Volatility risk premium (implied > realized volatility)
**Entry**: Each month, sell at-the-money straddle with 1 month maturity
**Hedge**: Buy 15% out-of-the-money put as crash protection
**Investment**: Invest remaining cash + option premium in the index
**Rebalancing**: Monthly

### Position Structure
1. **Short ATM straddle**: Sell at-the-money call + put (same strike, ~30 days to expiry)
2. **Long OTM put**: Buy 15% OTM put as insurance
3. **Long index**: Invest remaining capital in SPY

## Fundamental Reason
- **Insurance premium**: Investors dislike negative returns and pay premium for portfolio protection
- **Overpriced puts**: Put options systematically trade above fair value
- **Peso problem**: Risk of rare but catastrophic events may not be fully represented in sample
- **Behavioral**: Investors overestimate probability of extreme events

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1986-1995 |
| Return | 26% p.a. |
| Volatility | 19% |
| Max Drawdown | -24.07% |
| Sharpe Ratio | 1.16 |

**Note**: Includes 1987 crash in backtest period.

**OOS Performance (2012-2025)**:
- Return: 10.9% p.a.
- Volatility: 15.8%
- Max DD: -37.4%

## Source Paper
**Coval, Shumway: "Expected Option Returns"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=189840

**Abstract**: Under mild assumptions, call options have expected returns which exceed those of their underlying security and which are increasing in their strike prices. Likewise, put options have expected returns which are below the risk-free rate and which are also increasing in their strike prices. Zero-beta, at-the-money straddle positions produce average losses of approximately three percent per week. These findings suggest that some additional factor, such as systematic stochastic volatility, is priced in option returns.

## Other Papers
- Carr, Wu: "Variance Risk Premia" (SSRN 375784)
- Bondarenko: "Why are Put Options So Expensive?" (SSRN 375784)
- Israelov, Nielsen: "Covered Calls Uncovered" (SSRN 2444999)
- Ilmanen: "Do Financial Markets Reward Buying or Selling Insurance and Lottery Tickets?"

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/volatility-risk-premium-effect/
#
# Each month:
# 1. Sell at-the-money straddle (call + put at same strike, ~30 days expiry)
# 2. Buy 15% out-of-the-money put as crash protection
# 3. Invest remaining cash in the index

class VolatilityRiskPremiumEffect(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2012, 1, 1)
        self.SetCash(100000)

        data = self.AddEquity("SPY", Resolution.Minute)
        data.SetLeverage(5)
        self.symbol = data.Symbol

        # Add SPY options
        option = self.AddOption("SPY", Resolution.Minute)
        option.SetFilter(-20, 20, 25, 35)

        self.last_day = -1

    def OnData(self, slice):
        if self.Time.day == self.last_day:
            return
        self.last_day = self.Time.day

        for i in slice.OptionChains:
            chains = i.Value

            if not self.Portfolio.Invested:
                calls = list(filter(lambda x: x.Right == OptionRight.Call, chains))
                puts = list(filter(lambda x: x.Right == OptionRight.Put, chains))

                if not calls or not puts:
                    return

                underlying_price = self.Securities[self.symbol].Price
                expiries = [i.Expiry for i in puts]
                expiry = min(expiries, key=lambda x: abs((x.date()-self.Time.date()).days-30))

                strikes = [i.Strike for i in puts]
                strike = min(strikes, key=lambda x: abs(x-underlying_price))
                otm_strike = min(strikes, key=lambda x: abs(x - 0.85 * underlying_price))

                atm_call = [i for i in calls if i.Expiry == expiry and i.Strike == strike]
                atm_put = [i for i in puts if i.Expiry == expiry and i.Strike == strike]
                otm_put = [i for i in puts if i.Expiry == expiry and i.Strike == otm_strike]

                if atm_call and atm_put and otm_put:
                    options_q = int(self.Portfolio.MarginRemaining / (underlying_price * 100))

                    # Sell at-the-money straddle
                    self.Sell(atm_call[0].Symbol, options_q)
                    self.Sell(atm_put[0].Symbol, options_q)

                    # Buy 15% OTM put as insurance
                    self.Buy(otm_put[0].Symbol, options_q)

                    # Buy index
                    self.SetHoldings(self.symbol, 1)
```

## Eligibility Check

### Available
**Assets**:
- SPY-Stocks (underlying index ETF)
- VIX-related ETFs: VIXY, VXX, UVXY, SVIX, UVIX

**Transforms**:
- Standard technical indicators
- VIX data via `common_economic_indicators(category="VIX")`

### Missing (INELIGIBLE)

#### Options Trading Capability
The strategy **requires options trading** which is not supported on the platform:

| Requirement | Available | Status |
|-------------|-----------|--------|
| Options chains data | No | Missing |
| Sell call options | No | Missing |
| Sell put options | No | Missing |
| Buy put options | No | Missing |
| Options strike selection | No | Missing |
| Options expiry selection | No | Missing |
| Options Greeks | No | Missing |
| Options margin/collateral | No | Missing |

### Root Cause
**Platform does not support options trading** - only spot assets (stocks, ETFs, futures, crypto). This is a fundamental platform limitation, not a data availability issue.

## Alternative Approaches

### 1. VIX-Based Proxy (Partial)
Could approximate volatility risk premium using VIX products:
```python
# Long equity + short VIX futures proxy
long_weight = 0.9  # SPY
short_vol_weight = 0.1  # SVIX (short VIX ETF)
```
**Issues**:
- Not equivalent payoff structure
- VIX ETFs have contango decay
- No crash protection component

### 2. Covered Call ETFs
Use existing covered call ETFs as proxy:
- XYLD - S&P 500 Covered Call ETF
- QYLD - Nasdaq 100 Covered Call ETF
- JEPI - JPMorgan Equity Premium Income ETF

**Issues**:
- Different strike selection methodology
- No OTM put protection
- Passively managed, no timing

### 3. Put-Write ETFs
Use put-write index ETFs:
- PUTW - WisdomTree PutWrite ETF

**Issues**:
- Systematic put selling only
- No crash protection hedge

## Risk Considerations
- **Fat tails**: Strategy can lose -800% in crashes
- **Serial correlation**: Large negative days cluster together
- **Margin requirements**: Substantial reserves needed for naked options
- **Not a hedge**: Loses significantly during market stress
- **Volatility clustering**: Losses come when you can least afford them

## Related Strategies
- #0506 Volatility Risk Premium in Commodities
- #0507 Volatility Risk Premium in Currencies
- #0669 Volatility Risk Premium in Currencies 2
- Exploiting Term Structure of VIX Futures (may be more feasible with VIX ETFs)
