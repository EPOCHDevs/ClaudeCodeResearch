# Reversal Effect in International Equity ETFs

**Quantpedia ID**: #0016
**URL**: https://quantpedia.com/strategies/mean-reversion-effect-in-country-equity-indexes
**Status**: ELIGIBLE
**Linear Issue**: [ENG-31](https://linear.app/epoch-inc/issue/ENG-31/implement-reversal-effect-in-international-equity-etfs-0016)

## Overview
Long-term mean reversion in international country equity indexes. Countries that have been "losers" over the past 3 years tend to outperform "winners" over the subsequent 3 years. This is a contrarian strategy exploiting winner-loser reversals at the country level.

## Trading Rules
**Universe**: 24 country ETFs (iShares MSCI country funds + SPY)
**Signal**: 36-month cumulative return
**Selection**: Long bottom 4 countries (worst performers), short top 4 countries (best performers)
**Weighting**: Equal weighted within long/short legs
**Rebalancing**: Every 3 years

### ETF Universe
| ETF | Country |
|-----|---------|
| EWA | Australia |
| EWO | Austria |
| EWK | Belgium |
| EWZ | Brazil |
| EWC | Canada |
| FXI | China |
| EWQ | France |
| EWG | Germany |
| EWH | Hong Kong |
| EWI | Italy |
| EWJ | Japan |
| EWM | Malaysia |
| EWW | Mexico |
| EWN | Netherlands |
| EWS | Singapore |
| EZA | South Africa |
| EWY | South Korea |
| EWP | Spain |
| EWD | Sweden |
| EWL | Switzerland |
| EWT | Taiwan |
| THD | Thailand |
| EWU | United Kingdom |
| SPY | United States |

## Fundamental Reason
- **Mean reversion**: Relative stock index prices tend to revert to fundamental values
- **Contrarian investing**: Buy underperforming countries, sell outperforming countries
- **Market imperfections**: Smaller markets may have larger reversals due to liquidity constraints
- **Investor behavior**: Cross-border equity flows may be insufficient to remove mispricing
- **Long horizon**: Half-life of 3-3.5 years for mean reversion

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1969-1995 |
| Return | 6.4% p.a. |
| Volatility | Not stated |
| Max Drawdown | -80.98% |
| Sharpe Ratio | Not stated |

**Confidence**: WEAK - OOS backtest shows significantly negative performance. In-sample results may have been data-mined.

**OOS Performance (2003-2025)**:
- Return: -4.6% p.a.
- Volatility: 18.9%
- Sharpe: -0.24
- Max DD: -81.0%

## Source Paper
**Richards: "Winner-Loser Reversals in National Stock Market Indices: Can They be Explained?"**
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=883937

**Abstract**: This paper examines possible explanations for "winner-loser reversals" in the national stock market indices of 16 countries. There is no evidence that loser countries are riskier than winner countries either in terms of standard deviations, covariance with the world market or other risk factors, or performance in adverse economic states of the world. While there is evidence that small markets are subject to larger reversals than large markets, perhaps because of some form of market imperfection, the reversals are not just a small-market phenomenon. The apparent anomaly of winner-loser reversals in national market indices therefore remains unresolved.

## Other Papers
- Balvers, Wu: "Momentum and mean reversion across national equity markets"
- Balvers, Wu, Gilliland: "Stock Markets and Parametric Contrarian Investment Strategies"
- Spierdijk, Bikker, Van den Hoek: "Mean Reversion in International Stock Markets: An Empirical Analysis of the 20th Century"

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/mean-reversion-effect-in-country-equity-indexes/
#
# Universe: 24 country ETFs
# Signal: 36-month cumulative return
# Selection: Long bottom 4 countries, short top 4 countries
# Rebalance: Every 3 years

class ReversalEffectinInternationalEquityETFs(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)

        self.perf = {}
        self.period = 36 * 21  # 36 months of trading days

        self.symbols = [
            "EWA",  # Australia
            "EWO",  # Austria
            "EWK",  # Belgium
            "EWZ",  # Brazil
            "EWC",  # Canada
            "FXI",  # China
            "EWQ",  # France
            "EWG",  # Germany
            "EWH",  # Hong Kong
            "EWI",  # Italy
            "EWJ",  # Japan
            "EWM",  # Malaysia
            "EWW",  # Mexico
            "EWN",  # Netherlands
            "EWS",  # Singapore
            "EZA",  # South Africa
            "EWY",  # South Korea
            "EWP",  # Spain
            "EWD",  # Sweden
            "EWL",  # Switzerland
            "EWT",  # Taiwan
            "THD",  # Thailand
            "EWU",  # United Kingdom
            "SPY",  # United States
        ]

        for symbol in self.symbols:
            data = self.AddEquity(symbol, Resolution.Daily)
            data.SetLeverage(15)
            self.perf[symbol] = self.ROC(symbol, self.period, Resolution.Daily)

        self.month = 36
        self.recent_month = -1

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        if self.Time.month == self.recent_month:
            return
        self.recent_month = self.Time.month

        self.month += 1
        if self.month > 36:
            self.month = 1
        else:
            return

        # Rank by 36-month return
        sorted_by_momentum = sorted(
            [x for x in self.perf.items() if x[1].IsReady and x[0] in data],
            key=lambda x: x[1].Current.Value,
            reverse=True
        )

        long = [x[0] for x in sorted_by_momentum[-4:]]   # Bottom 4 (losers)
        short = [x[0] for x in sorted_by_momentum[:4]]   # Top 4 (winners)

        # Liquidate positions not in long or short
        invested = [x.Key.Value for x in self.Portfolio if x.Value.Invested]
        for symbol in invested:
            if symbol not in long + short:
                self.Liquidate(symbol)

        # Equal weight long/short
        for symbol in long:
            self.SetHoldings(symbol, 1 / len(long))
        for symbol in short:
            self.SetHoldings(symbol, -1 / len(short))
```

## Eligibility Check

### Available
**Data Sources**:
- All 24 country ETFs available: EWA, EWO, EWK, EWZ, EWC, FXI, EWQ, EWG, EWH, EWI, EWJ, EWM, EWW, EWN, EWS, EZA, EWY, EWP, EWD, EWL, EWT, THD, EWU, SPY
- Daily OHLCV data for all ETFs

**Transforms**:
- `roc(period=756)` - 36-month rate of change (756 trading days)
- `cs_rank(ascending=True)` - Cross-sectional ranking (low = losers)
- `cs_select(quantile=6, select_quantile=1)` - Select bottom 4 of 24 (losers)
- `cs_select(quantile=6, select_quantile=6)` - Select top 4 of 24 (winners)
- `equal_weight` - Equal weighting within portfolios

**Universe**:
- All required iShares MSCI country ETFs available
- SPY available for US exposure

### Implementation Approach
```python
# Get price data for all 24 country ETFs
price = market_data_source(timeframe=1D)().c

# Calculate 36-month return
returns_36m = roc(period=756)(price)

# Rank by 36-month return (ascending so low rank = losers)
reversal_rank = cs_rank(ascending=True)(returns_36m)

# Select bottom 4 (losers - long) and top 4 (winners - short)
losers = cs_select(quantile=6, select_quantile=1)(returns_36m)
winners = cs_select(quantile=6, select_quantile=6)(returns_36m)

# Long losers, short winners
long_weight = equal_weight()(active_mask=losers)
short_weight = -equal_weight()(active_mask=winners)
total_weight = long_weight + short_weight

# Rebalance every 3 years (36 months)
# Use month counter or time_feature with year % 3 logic
position_size(type="percent")(size=total_weight * 100, rebalance_on=rebalance_trigger)
```

## Implementation Notes
- Original paper used 16 national stock market indices (1969-1995)
- QC implementation uses 24 country ETFs for broader coverage
- Extremely long rebalancing period (3 years) means very few trades
- Long-short implementation requires shorting capability
- High leverage (15x in QC code) used to amplify returns

## Risk Considerations
- **WEAK confidence**: OOS performance is significantly negative (-4.6% p.a.)
- **Data mining concerns**: In-sample results may not generalize
- **Extreme drawdown**: -81% max DD in both in-sample and OOS periods
- **Long horizon risk**: 3-year holding period means extended exposure to losers
- **Not a hedge**: Strong equity market exposure, not suitable for hedging
- **Regime dependence**: Mean reversion speed varies with economic uncertainty

## Performance Warning
This strategy shows **significantly negative OOS performance** (Sharpe -0.24). The original academic finding from 1969-1995 may have been:
1. Data-mined
2. Arbitraged away since publication
3. Specific to that time period

Consider this strategy with extreme caution. Academic research since the original paper shows mixed results, with mean reversion speed highly variable across different time periods.

## Comparison Notes
This is a **long-term contrarian/reversal** strategy at the country level. Compare with:
- #0015 Momentum Factor Effect in Country Equity Indexes (opposite signal - momentum instead of reversal)
- Combining momentum and mean reversion may work better than pure contrarian (Balvers & Wu)
