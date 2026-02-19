# FX Carry Trade

**Quantpedia ID**: #0005
**URL**: https://quantpedia.com/strategies/fx-carry-trade
**Status**: ELIGIBLE
**Linear Issue**: [ENG-20](https://linear.app/epoch-inc/issue/ENG-20/implement-fx-carry-trade-0005)

## Overview
The FX carry trade is one of the most well-known currency strategies. It systematically sells low-interest-rate currencies and buys high-interest-rate currencies, capturing the spread between rates. The strategy exploits the "forward premium puzzle" - the forward rate is not an unbiased estimate of future spot rates.

## Trading Rules
**Universe**: 8 currency futures (G10 + Mexico)
**Signal**: 3-month interbank interest rates from FRED
**Selection**: Long top 3 highest rates, short bottom 3 lowest rates
**Weighting**: Equal weight within long/short legs
**Rebalancing**: Monthly

### Currency Universe
| Future | Currency | FRED Interest Rate Series |
|--------|----------|--------------------------|
| A6-Futures | Australian Dollar | IR3TIB01AUM156N |
| B6-Futures | British Pound | LIOR3MUKM |
| D6-Futures | Canadian Dollar | IR3TIB01CAM156N |
| E6-Futures | Euro FX | IR3TIB01EZM156N |
| J6-Futures | Japanese Yen | IR3TIB01JPM156N |
| M6-Futures | Mexican Peso | IR3TIB01MXM156N |
| N6-Futures | New Zealand Dollar | IR3TIB01NZM156N |
| S6-Futures | Swiss Franc | IR3TIB01CHM156N |

## Fundamental Reason
According to uncovered interest rate parity (UIP), carry trades should not yield predictable profit because the interest rate differential should equal the expected currency depreciation. However, high-interest-rate currencies often don't fall enough to offset the yield difference because:
1. Inflation is lower than expected in high-rate countries
2. Carry trading weakens borrowed currencies as investors convert to high-yielding currencies
3. Investors are compensated for taking currency risk

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1989-2009 |
| Return | 7.27% p.a. |
| Volatility | 9.6% |
| Max Drawdown | -32.05% |
| Sharpe Ratio | 0.29 |

**Note**: Performance calculated from Deutsche Bank Currency Carry USD Index.

## Source Paper
**Deutsche Bank: "Currency Returns"**
- URL: http://globalmarkets.db.com/new/docs/dbCurrencyReturns_March2009.pdf

**Abstract**: Carry - One of the most widely known and profitable strategies in currency markets are carry trades, where one systematically sells low interest rate currencies and buys high interest rate currencies. Such a strategy exploits what academics call "forward-rate bias" or the "forward premium puzzle".

## Other Papers
- Lustig, Roussanov, Verdelhan: "Common Risk Factors in Currency Markets" (SSRN 1139447)
- Acemoglu, Rogoff, Woodford: "Carry Trades and Currency Crashes" (NBER c7288)
- Daniel, Hodrick, Lu: "The Carry Trade: Risks and Drawdowns" (SSRN 2486275)

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/fx-carry-trade/
#
# Universe: 8 currency futures
# Signal: 3-month interbank rates from FRED
# Selection: Long top 3, short bottom 3 by rate
# Rebalance: Monthly

class ForexCarryTrade(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)

        # Currency futures and their FRED interest rate series
        self.tickers = {
            "CME_AD1": "IR3TIB01AUM156N",  # Australian Dollar
            "CME_BP1": "LIOR3MUKM",         # British Pound
            "CME_CD1": "IR3TIB01CAM156N",  # Canadian Dollar
            "CME_EC1": "IR3TIB01EZM156N",  # Euro FX
            "CME_JY1": "IR3TIB01JPM156N",  # Japanese Yen
            "CME_MP1": "IR3TIB01MXM156N",  # Mexican Peso
            "CME_NE1": "IR3TIB01NZM156N",  # New Zealand Dollar
            "CME_SF1": "IR3TIB01CHM156N"   # Swiss Franc
        }

        self.traded_count = 3
        self.leverage = 3
        self.recent_month = -1

    def OnData(self, data):
        if self.Time.month == self.recent_month:
            return
        self.recent_month = self.Time.month

        # Get interest rates for each currency
        rate = {}
        for ticker, int_rate in self.tickers.items():
            if self.Securities[int_rate].GetLastData():
                rate[ticker] = self.Securities[int_rate].Price

        if len(rate) >= self.traded_count:
            # Sort by interest rate
            sorted_by_rate = sorted(rate, key=rate.get, reverse=True)
            long = sorted_by_rate[:self.traded_count]
            short = sorted_by_rate[-self.traded_count:]

            # Equal weight long/short
            for symbol in long:
                self.SetHoldings(symbol, 1 / len(long))
            for symbol in short:
                self.SetHoldings(symbol, -1 / len(short))
```

## Eligibility Check

### Available
**Currency Futures**:
- A6-Futures (Australian Dollar)
- B6-Futures (British Pound)
- D6-Futures (Canadian Dollar)
- E6-Futures (Euro FX)
- J6-Futures (Japanese Yen)
- M6-Futures (Mexican Peso)
- N6-Futures (New Zealand Dollar)
- S6-Futures (Swiss Franc)

**Interest Rate Data (via FRED)**:
```
economic_indicators(series_id="IR3TIB01AUM156N")  # Australia
economic_indicators(series_id="LIOR3MUKM")        # UK
economic_indicators(series_id="IR3TIB01CAM156N")  # Canada
economic_indicators(series_id="IR3TIB01EZM156N")  # Eurozone
economic_indicators(series_id="IR3TIB01JPM156N")  # Japan
economic_indicators(series_id="IR3TIB01MXM156N")  # Mexico
economic_indicators(series_id="IR3TIB01NZM156N")  # New Zealand
economic_indicators(series_id="IR3TIB01CHM156N")  # Switzerland
```

**Transforms**:
- `cs_rank` - Cross-sectional ranking
- `cs_select` - Cross-sectional selection (top/bottom)
- `equal_weight` - Equal weighting

### EpochScript Implementation Approach
```python
# Data sources
src = market_data_source(timeframe=1D)()

# Interest rates from FRED (need separate data source per currency)
au_rate = economic_indicators(series_id="IR3TIB01AUM156N")().result
uk_rate = economic_indicators(series_id="LIOR3MUKM")().result
ca_rate = economic_indicators(series_id="IR3TIB01CAM156N")().result
eu_rate = economic_indicators(series_id="IR3TIB01EZM156N")().result
jp_rate = economic_indicators(series_id="IR3TIB01JPM156N")().result
mx_rate = economic_indicators(series_id="IR3TIB01MXM156N")().result
nz_rate = economic_indicators(series_id="IR3TIB01NZM156N")().result
ch_rate = economic_indicators(series_id="IR3TIB01CHM156N")().result

# Rank by interest rate (cross-sectional)
rate_rank = cs_rank(method=RankMethod.average, ascending=False)(rate_signal)

# Select top 3 and bottom 3
long_mask = rate_rank <= 3
short_mask = rate_rank >= 6  # bottom 3 of 8

# Equal weight
long_weight = equal_weight()(active_mask=long_mask)
short_weight = equal_weight()(active_mask=short_mask)

# Monthly rebalance
is_new_month = ...
position_size(type="percent")(size=(long_weight - short_weight) * 100, rebalance_on=is_new_month)
```

## Implementation Notes
- Strategy has significant drawdown risk (-32%) due to correlation with risk-off events
- Currency carry tends to unwind during market stress (not a hedge for equities)
- Consider leverage carefully - QuantConnect uses 3x leverage
- Interest rates are published monthly, use point-in-time FRED data to avoid look-ahead bias
- FX futures have different contract sizes and margin requirements

## Risk Considerations
- **Crash Risk**: Carry trades are subject to sudden unwinding during market stress
- **Correlation**: Highly correlated with business cycle and equity markets
- **Leverage**: Strategy often uses leverage to enhance returns
- **Negative Skewness**: Returns exhibit negative skewness due to crash risk
