# Currency Value Factor - PPP Strategy

**Quantpedia ID**: #0009
**URL**: https://quantpedia.com/strategies/currency-value-factor-ppp-strategy
**Status**: INELIGIBLE
**Linear Issue**: [ENG-24](https://linear.app/epoch-inc/issue/ENG-24/feature-request-oecd-ppp-data-for-currency-value-strategy-0009)

## Overview
Currency value strategy based on Purchasing Power Parity (PPP). Systematically buys "undervalued" currencies and sells "overvalued" currencies based on PPP fair value calculations. In the long run, currencies tend to move towards their fair value, making this a profitable medium-term strategy.

## Trading Rules
**Universe**: 7 currency futures (G10 excluding Mexico)
**Signal**: OECD PPP fair value vs USD, adjusted monthly by CPI changes
**Selection**: Long 3 most undervalued (lowest PPP), short 3 most overvalued (highest PPP)
**Weighting**: Equal weight within long/short legs
**Rebalancing**: Quarterly (or yearly in QC implementation)

### Currency Universe
| Future | Currency | PPP Symbol |
|--------|----------|------------|
| CME_AD1 | Australian Dollar | AUS_PPP |
| CME_BP1 | British Pound | GBR_PPP |
| CME_CD1 | Canadian Dollar | CAN_PPP |
| CME_EC1 | Euro FX | DEU_PPP |
| CME_JY1 | Japanese Yen | JPN_PPP |
| CME_NE1 | New Zealand Dollar | NZL_PPP |
| CME_SF1 | Swiss Franc | CHE_PPP |

**Note**: No Mexican Peso (unlike carry and momentum strategies) - PPP data not available.

## Fundamental Reason
- PPP theory states price differences between countries narrow over time via exchange rate movements
- Different countries consume different baskets of goods, but relative price levels can be assessed
- Currencies trading far from PPP fair value tend to revert toward equilibrium
- Captures risk premia from holding undervalued currencies

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1989-2009 |
| Return | 7.82% p.a. |
| Volatility | 9.33% |
| Max Drawdown | -39.38% |
| Sharpe Ratio | 0.36 |

**Note**: Performance from Deutsche Bank Currency Valuation USD Index.

**Confidence Note**: OOS back-test shows alpha deterioration - strategy may be losing efficacy.

## Source Paper
**Deutsche Bank: "Currency Returns"**
- URL: http://globalmarkets.db.com/new/docs/dbCurrencyReturns_March2009.pdf

**Abstract**: Valuation - In the long run, currencies tend to move towards their "fair value". Consequently, systematically buying "undervalued" currencies and selling "overvalued" currencies is profitable in the medium term. One of the strongest conclusions in academia is that fundamentals tend not to work for currencies in the short to medium term, yet they do long term. One of the oldest measures of "fair value", purchasing power parity, has been shown to work in the long run.

## Other Papers
- Menkhoff, Sarno, Schmeling, Schrimpf: "Currency Value" (SSRN 2492082)
- Kroencke, Schindler, Schrimpf: "International Diversification Benefits with Foreign Exchange Investment Styles"
- Lohre, Kolrep: "Currency Management with Style" (SSRN 3175387)

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/currency-value-factor-ppp-strategy/
#
# Universe: 7 currency futures
# Signal: OECD PPP fair value
# Selection: Long 3 most undervalued, short 3 most overvalued
# Rebalance: Yearly (January)

class CurrencyValueFactorPPPStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)

        self.leverage = 3
        self.traded_count = 3
        self.ppp_data = {}

        # Currency futures and PPP data symbols
        self.symbols = {
            "CME_AD1": "AUS_PPP",  # Australian Dollar
            "CME_BP1": "GBR_PPP",  # British Pound
            "CME_CD1": "CAN_PPP",  # Canadian Dollar
            "CME_EC1": "DEU_PPP",  # Euro FX (Germany as proxy)
            "CME_JY1": "JPN_PPP",  # Japanese Yen
            "CME_NE1": "NZL_PPP",  # New Zealand Dollar
            "CME_SF1": "CHE_PPP"   # Swiss Franc
        }

        for symbol, ppp_symbol in self.symbols.items():
            self.AddData(QuantpediaFutures, symbol, Resolution.Daily)
            self.AddData(PPPData, ppp_symbol, Resolution.Daily)

        self.recent_month = -1

    def OnData(self, data):
        # Collect PPP values
        for symbol, ppp_symbol in self.symbols.items():
            if ppp_symbol in data and data[ppp_symbol]:
                self.ppp_data[symbol] = data[ppp_symbol].Value

        if self.recent_month == self.Time.month:
            return
        self.recent_month = self.Time.month

        # January rebalance only
        if self.recent_month == 1:
            if len(self.ppp_data) >= self.traded_count * 2:
                # Sort by PPP (high = overvalued, low = undervalued)
                sorted_by_ppp = sorted(self.ppp_data.items(), key=lambda x: x[1], reverse=True)
                long = [x[0] for x in sorted_by_ppp[-self.traded_count:]]   # Most undervalued
                short = [x[0] for x in sorted_by_ppp[:self.traded_count]]   # Most overvalued

                # Execute trades
                for i, portfolio in enumerate([long, short]):
                    for symbol in portfolio:
                        self.SetHoldings(symbol, ((-1) ** i) / len(portfolio))

                self.ppp_data.clear()
```

## Eligibility Check

### Available
**Currency Futures** (7 of 8):
- A6-Futures (Australian Dollar)
- B6-Futures (British Pound)
- D6-Futures (Canadian Dollar)
- E6-Futures (Euro FX)
- J6-Futures (Japanese Yen)
- N6-Futures (New Zealand Dollar)
- S6-Futures (Swiss Franc)

**Transforms**:
- `cs_rank` - Cross-sectional ranking
- `cs_select` - Cross-sectional selection
- `equal_weight` - Equal weighting

### Missing (INELIGIBLE)

#### OECD PPP Data
The strategy requires **Purchasing Power Parity fair value data** for each country vs USD:

| Country | Required | FRED Availability |
|---------|----------|-------------------|
| Australia | AUS_PPP | PPPTTLAUA618NUPN (ends ~2010) |
| UK | GBR_PPP | PPPTTLGBA618NUPN (ends ~2010) |
| Canada | CAN_PPP | PPPTTLCAA618NUPN (ends ~2010) |
| Germany | DEU_PPP | PPPTTLDEA618NUPN (ends ~2010) |
| Japan | JPN_PPP | PPPTTLJPA618NUPN (ends ~2010) |
| New Zealand | NZL_PPP | PPPTTLNZA618NUPN (ends ~2010) |
| Switzerland | CHE_PPP | PPPTTLCHA618NUPN (ends ~2010) |

**Issues:**
1. FRED Penn World Table 7.1 data is **historical only** (ends ~2010)
2. No point-in-time PPP data with proper publication lag handling
3. Strategy needs rolling PPP calculations adjusted by monthly CPI

### Root Cause
**Missing OECD PPP data feed** - While FRED has historical Penn World Table data, it's not current enough for live trading. QuantConnect uses Quantpedia's proprietary PPP data source.

## Alternative Approaches

### 1. FRED Historical PPP + CPI Adjustment
Could use FRED Penn World Table + monthly CPI data to extend:
```python
# FRED series
ppp_base = economic_indicators(series_id="PPPTTLAUA618NUPN")  # Base PPP
cpi_au = economic_indicators(series_id="CPALTT01AUM661S")     # Australia CPI
cpi_us = economic_indicators(series_id="CPIAUCSL")            # US CPI
# Calculate rolling PPP: ppp_current = ppp_base * (cpi_au/cpi_us) ratio
```
**Issue**: Complex calculation, base PPP data ends 2010

### 2. Real Exchange Rate Proxy
Use real effective exchange rate (REER) from FRED as PPP proxy:
- FRED has REER series for major currencies
- Not exactly PPP but captures similar valuation concept
**Issue**: Different methodology, may not replicate strategy returns

### 3. Feature Request
Add OECD PPP data feed with:
- Current PPP exchange rates for G10 currencies
- Point-in-time publication dates
- Monthly or quarterly updates

## Comparison with Other FX Strategies

| Strategy | Signal | Data Required | Status |
|----------|--------|---------------|--------|
| #0005 FX Carry | Interest rates | FRED (available) | ELIGIBLE |
| #0008 FX Momentum | Price returns | Price only | ELIGIBLE |
| #0009 FX Value/PPP | PPP fair value | OECD PPP (missing) | INELIGIBLE |

**Note**: Value factor is complementary to carry and momentum - academic literature shows low correlation between these three FX factors.

## Implementation Notes
- This is the third FX factor (after carry and momentum) - all three have low correlation
- Value factor often goes negative during stress (undervalued currencies appreciate)
- Makes it a valuable hedge unlike carry and momentum
- Yearly rebalance sufficient due to slow-moving nature of PPP
- QC implementation uses Germany as Euro proxy (DEU_PPP for EUR)

## Risk Considerations
- **Slow Mean Reversion**: PPP works over years, not months
- **Fundamental Shifts**: Structural economic changes can invalidate PPP
- **Alpha Decay**: OOS performance suggests strategy may be losing efficacy
