# Momentum Factor Effect in Country Equity Indexes

**Quantpedia ID**: #0015
**URL**: https://quantpedia.com/strategies/momentum-factor-effect-in-country-equity-indexes
**Status**: ELIGIBLE
**Linear Issue**: [ENG-30](https://linear.app/epoch-inc/issue/ENG-30/implement-quantpedia-strategy-0015-momentum-factor-effect-in-country)

## Overview
Cross-sectional momentum strategy applied to country equity ETFs. Exploits the well-documented momentum anomaly at the country index level, where past winners tend to continue outperforming. The strategy ranks country ETFs by their trailing returns and goes long the top performers.

## Trading Rules
**Universe**: 24 country equity ETFs (iShares MSCI country index funds)

**Signal**: 6-month trailing return (ROC)

**Selection**: Top 5 countries with best momentum

**Weighting**: Equal weight (20% each)

**Rebalancing**: Monthly

### ETF Universe
| Ticker | Country | Full Name |
|--------|---------|-----------|
| EWA | Australia | iShares MSCI Australia Index ETF |
| EWO | Austria | iShares MSCI Austria Investable Mkt Index ETF |
| EWK | Belgium | iShares MSCI Belgium Investable Market Index ETF |
| EWZ | Brazil | iShares MSCI Brazil Index ETF |
| EWC | Canada | iShares MSCI Canada Index ETF |
| FXI | China | iShares China Large-Cap ETF |
| EWQ | France | iShares MSCI France Index ETF |
| EWG | Germany | iShares MSCI Germany ETF |
| EWH | Hong Kong | iShares MSCI Hong Kong Index ETF |
| EWI | Italy | iShares MSCI Italy Index ETF |
| EWJ | Japan | iShares MSCI Japan Index ETF |
| EWM | Malaysia | iShares MSCI Malaysia Index ETF |
| EWW | Mexico | iShares MSCI Mexico Inv. Mt. Idx |
| EWN | Netherlands | iShares MSCI Netherlands Index ETF |
| EWS | Singapore | iShares MSCI Singapore Index ETF |
| EZA | South Africa | iShares MSCI South Africa Index ETF |
| EWY | South Korea | iShares MSCI South Korea ETF |
| EWP | Spain | iShares MSCI Spain Index ETF |
| EWD | Sweden | iShares MSCI Sweden Index ETF |
| EWL | Switzerland | iShares MSCI Switzerland Index ETF |
| EWT | Taiwan | iShares MSCI Taiwan Index ETF |
| THD | Thailand | iShares MSCI Thailand Index ETF |
| EWU | United Kingdom | iShares MSCI United Kingdom Index ETF |
| SPY | United States | SPDR S&P 500 ETF |

## Fundamental Reason
1. **Behavioral Biases**: Investor herding, over/underreaction, and confirmation bias cause momentum to persist.

2. **Macroeconomic Momentum**: Country returns relate to macroeconomic conditions. Misreaction to macro news creates predictable patterns (Bhorjaj & Swaminathan).

3. **Larger Market Cap = More Persistent**: Country indices have larger underlying market caps than individual stocks, making momentum effects more persistent and less likely to be "traded out."

4. **ETF Accessibility**: Exchange-traded funds provide low-cost, liquid access to country momentum without needing to trade individual stocks.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1968-2009 |
| Return | 17.7% p.a. |
| Volatility | N/A |
| Max Drawdown | -65.39% |
| Sharpe Ratio | N/A |

**Note**: Performance from 39-year study. Strategy of holding top 4 MSCI country indices over previous 11 months outperformed equal-weighted benchmark by ~10% p.a.

## Out-of-Sample Performance (Quantpedia)
| Metric | Value |
|--------|-------|
| Period | 2000-2025 |
| Return | 5.1% p.a. |
| Volatility | 21.7% |
| Max Drawdown | -65.39% |
| Sharpe Ratio | 0.23 |

**Note**: Significant alpha decay in OOS period. Strategy is long-only with full equity exposure.

## Source Paper
**Muller, Ward: "Momentum effects in country equity indexes"**
- URL: http://repository.up.ac.za/bitstream/handle/2263/14149/Muller_Momentum%282010%29.pdf?sequence=1
- Key Finding: Strategy of holding for one month a portfolio of the four best performing MSCI country indices over the previous 11 months persistently outperformed an equal weighted benchmark by around 10% per annum over 39 years (1970-2009).

## Other Papers
- Bhorjaj, Swaminathan: "Macromomentum: Evidence of Predictability in International Equity Markets" (SSRN 273569)
- Balvers, Wu: "Momentum and mean reversion across national equity markets"
- Andreu, Swinkels, Tjong-A-Tjoe: "Can exchange-traded funds be used to exploit country and industry momentum?" (SSRN 1150972)
- Zaremba: "Country Selection Strategies Based on Value, Size and Momentum" (SSRN 2521026)

## Eligibility Check

### ELIGIBLE

All required components are available in the platform:

| Component | Required | Platform Capability | Status |
|-----------|----------|---------------------|--------|
| Country ETFs | 24 ETFs | All available in assets.json | ✅ |
| 6-month momentum | `roc(126)` | `roc` transform | ✅ |
| Top 5 selection | Best performers | `cs_select(direction=top, k=5)` | ✅ |
| Equal weighting | 20% each | `equal_weight` transform | ✅ |
| Monthly rebalancing | Monthly | Supported timeframe | ✅ |

### Available ETFs (verified in assets.json)
- EWA-Stocks, EWO-Stocks, EWK-Stocks, EWZ-Stocks
- EWC-Stocks, FXI-Stocks, EWQ-Stocks, EWG-Stocks
- EWH-Stocks, EWI-Stocks, EWJ-Stocks, EWM-Stocks
- EWW-Stocks, EWN-Stocks, EWS-Stocks, EZA-Stocks
- EWY-Stocks, EWP-Stocks, EWD-Stocks, EWL-Stocks
- EWT-Stocks, THD-Stocks, EWU-Stocks, SPY-Stocks

### Implementation Approach

```
# Universe: 24 country equity ETFs
assets = [EWA, EWO, EWK, EWZ, EWC, FXI, EWQ, EWG, EWH, EWI,
          EWJ, EWM, EWW, EWN, EWS, EZA, EWY, EWP, EWD, EWL,
          EWT, THD, EWU, SPY]

# Calculate 6-month momentum
momentum = roc(close, 126)

# Select top 5 countries
long_signal = cs_select(momentum, direction=top, k=5)

# Equal weight allocation
weight = equal_weight(long_signal)
```

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/momentum-factor-effect-in-country-equity-indexes/
#
# The investment universe consists of ETFs (funds) which invest in individual
# countries' equity indexes. The top 5 countries with the best X-month
# (where X depends on investors choice, studies show X to be best as 10-12)
# momentum are chosen as an investment, and portfolio is rebalanced monthly.

from AlgorithmImports import *

class MomentumFactorEffectinCountryEquityIndexes(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)

        # Daily ROC data.
        self.perf = {}
        self.period = 6 * 21
        self.SetWarmUp(self.period, Resolution.Daily)

        self.symbols = [
            "EWA",  # iShares MSCI Australia Index ETF
            "EWO",  # iShares MSCI Austria Investable Mkt Index ETF
            "EWK",  # iShares MSCI Belgium Investable Market Index ETF
            "EWZ",  # iShares MSCI Brazil Index ETF
            "EWC",  # iShares MSCI Canada Index ETF
            "FXI",  # iShares China Large-Cap ETF
            "EWQ",  # iShares MSCI France Index ETF
            "EWG",  # iShares MSCI Germany ETF
            "EWH",  # iShares MSCI Hong Kong Index ETF
            "EWI",  # iShares MSCI Italy Index ETF
            "EWJ",  # iShares MSCI Japan Index ETF
            "EWM",  # iShares MSCI Malaysia Index ETF
            "EWW",  # iShares MSCI Mexico Inv. Mt. Idx
            "EWN",  # iShares MSCI Netherlands Index ETF
            "EWS",  # iShares MSCI Singapore Index ETF
            "EZA",  # iShares MSCI South Africe Index ETF
            "EWY",  # iShares MSCI South Korea ETF
            "EWP",  # iShares MSCI Spain Index ETF
            "EWD",  # iShares MSCI Sweden Index ETF
            "EWL",  # iShares MSCI Switzerland Index ETF
            "EWT",  # iShares MSCI Taiwan Index ETF
            "THD",  # iShares MSCI Thailand Index ETF
            "EWU",  # iShares MSCI United Kingdom Index ETF
            "SPY",  # SPDR S&P 500 ETF
        ]

        self.traded_count = 5

        for symbol in self.symbols:
            data = self.AddEquity(symbol, Resolution.Minute)
            data.SetFeeModel(CustomFeeModel())
            data.SetLeverage(5)
            self.perf[symbol] = self.ROC(symbol, self.period, Resolution.Daily)

        self.recent_month = -1

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        if not (self.Time.hour == 9 and self.Time.minute == 31):
            return

        if self.Time.month == self.recent_month:
            return
        self.recent_month = self.Time.month

        sorted_by_momentum = sorted(
            [x for x in self.perf.items() if x[1].IsReady and x[0] in data and data[x[0]]],
            key=lambda x: x[1].Current.Value,
            reverse=True
        )

        long = []
        if len(sorted_by_momentum) >= self.traded_count:
            long = [x[0] for x in sorted_by_momentum[:self.traded_count]]

        # Trade execution
        invested = [x.Key for x in self.Portfolio if x.Value.Invested]
        for symbol in invested:
            if symbol not in long:
                self.Liquidate(symbol)

        for symbol in long:
            self.SetHoldings(symbol, 1 / len(long))


# Custom fee model
class CustomFeeModel(FeeModel):
    def GetOrderFee(self, parameters):
        fee = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))
```

## Implementation Notes

1. **Lookback Period**: Paper suggests 10-12 months is optimal. QC uses 6 months (126 days). Can experiment with different periods.

2. **Long-Only**: This is a long-only strategy with full equity exposure. No hedge during bear markets.

3. **Simple vs Complex**: Strategy is marked as "Simple" complexity - straightforward momentum ranking and selection.

4. **ETF Liquidity**: All ETFs in the universe are highly liquid iShares products.

5. **Rebalancing**: Monthly on first trading day.

## Risk Considerations

- **No Hedge**: Long-only strategy falls with equity markets during crashes
- **High Drawdown**: -65.39% max drawdown reflects full equity exposure
- **Emerging Market Risk**: Includes Brazil, China, South Africa, etc.
- **Momentum Crashes**: Momentum strategies can suffer sharp reversals
- **Alpha Decay**: OOS Sharpe of 0.23 suggests diminished returns

## Related Strategies
- #0003 Sector Momentum - Rotational System (sector-level momentum)
- #0008 Currency Momentum Factor (FX momentum)
- #0016 Reversal Effect in International Equity ETFs (contrarian approach)
