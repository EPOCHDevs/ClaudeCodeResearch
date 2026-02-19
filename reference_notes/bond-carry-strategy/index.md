# Bond Carry Strategy

**Quantpedia ID**: #0006
**URL**: https://quantpedia.com/strategies/bond-carry-strategy
**Status**: INELIGIBLE
**Linear Issue**: [ENG-18](https://linear.app/epoch-inc/issue/ENG-18/feature-request-international-bond-futures-and-yield-data-for-carry)

## Overview
Value approach to global sovereign bonds. Sort government bonds from 30 countries by nominal yield, buy the highest-yielding ones. High yields are associated with non-diversifiable risk factors such as political turmoil, wavering property rights, or persistently high inflation - so high yields involve a risk premium.

## Trading Rules
**Universe**: Government bonds of 30 countries (implemented with 7 country bond futures)
**Signal**: Sort by nominal bond yield at end of month
**Selection**: Top 33% (1/3) of countries with highest yields
**Weighting**: Equal weight
**Rebalancing**: Monthly

### Implementation (QuantConnect)
Uses bond futures from 7 countries:
- Australia (ASX_XT1 → AU10YT)
- Canada (MX_CGB1 → CA10YT)
- Germany (EUREX_FGBL1 → DE10YT)
- UK (LIFFE_R1 → GB10YT)
- Italy (EUREX_FBTP1 → IT10YT)
- Japan (SGX_JB1 → JP10YT)
- USA (CME_TY1 → US10YT)

## Fundamental Reason
High yields are associated with non-diversifiable risk factors:
- Political turmoil
- Wavering property rights
- Persistently high inflation

Therefore, high yields represent a risk premium that can be harvested systematically.

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1950-2012 |
| Return | 9.91% p.a. |
| Volatility | 8.63% |
| Max Drawdown | -14.31% |
| Sharpe Ratio | 0.68 |

## Source Paper
**Faber: "Finding Yield in a 2% World"**
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2724737

**Abstract**: Many investors are surprised to learn that the largest asset class in the world is foreign debt. US investors often allocate very little to foreign bonds, and when they do, it is through capitalization weighted indexes. These indexes allocate the highest weighting to countries with the most debt outstanding. Is there a better way to invest in global bonds? We examine a simple value approach applied to global sovereign bonds and find that it works well across decades.

## Other Papers
- Ilmanen et al: "Factor Premia and Factor Timing: A Century of Evidence" (SSRN 3400998)
- Min, Dong: "The Drivers of Global Government Bond Returns" (SSRN 4948827)

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/bond-carry-strategy/
# Universe: 7 country bond futures
# Signal: Sort by bond yield, select top 33%
# Rebalance: Monthly

class BondCarryStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)

        self.symbols = {
            "ASX_XT1" : "AU10YT",   # Australia
            "MX_CGB1" : "CA10YT",   # Canada
            "EUREX_FGBL1" : "DE10YT",  # Germany
            "LIFFE_R1" : "GB10YT",  # UK
            "EUREX_FBTP1" : "IT10YT",  # Italy
            "SGX_JB1" : "JP10YT",   # Japan
            "CME_TY1" : "US10YT"    # USA
        }

        self.quantile = 3  # Top 33%

        for bond_future, bond_yield_symbol in self.symbols.items():
            # Add futures data (from Quantpedia external source)
            self.AddData(QuantpediaFutures, bond_future, Resolution.Daily)
            # Add bond yield data (from Quantpedia external source)
            self.AddData(QuantpediaBondYield, bond_yield_symbol, Resolution.Daily)

        self.recent_month = -1

    def OnData(self, slice):
        # Monthly rebalance
        if self.Time.month == self.recent_month:
            return
        self.recent_month = self.Time.month

        # Get bond yields
        b_yield = {}
        for bond_future, bond_yield_symbol in self.symbols.items():
            if data_available:
                b_yield[bond_future] = self.Securities[bond_yield_symbol].Price

        # Select top 33% by yield
        if len(b_yield) >= self.quantile:
            sorted_by_yield = sorted(b_yield.items(), key=lambda x:x[1], reverse=True)
            quantile = int(len(sorted_by_yield) / self.quantile)
            long = [x[0] for x in sorted_by_yield[:quantile]]

        # Equal weight allocation
        for symbol in long:
            self.SetHoldings(symbol, 1 / len(long))
```

## Eligibility Check

### Available
- **US Bond Futures**: ZN-Futures (10-Year T-Note), ZB-Futures (30-Year Bond)
- **Japan Bond Futures**: JB-Futures
- **US Bond ETFs**: IEF-Stocks, TLT-Stocks, BND-Stocks

### Bond Yield Data (Available via FRED)
The platform has FRED economic data via `economic_indicators`:

| Country | FRED Series | Access |
|---------|-------------|--------|
| USA | DGS10 | `common_economic_indicators(category="Treasury10Y")` |
| Germany | IRLTLT01DEM156N | `economic_indicators(series_id="IRLTLT01DEM156N")` |
| UK | IRLTLT01GBM156N | `economic_indicators(series_id="IRLTLT01GBM156N")` |
| Japan | IRLTLT01JPM156N | `economic_indicators(series_id="IRLTLT01JPM156N")` |
| Australia | IRLTLT01AUM156N | `economic_indicators(series_id="IRLTLT01AUM156N")` |
| Canada | IRLTLT01CAM156N | `economic_indicators(series_id="IRLTLT01CAM156N")` |
| Italy | IRLTLT01ITM156N | `economic_indicators(series_id="IRLTLT01ITM156N")` |

**Note**: FRED international yields are monthly, published with lag. US yields (DGS10) are daily.

### Missing (INELIGIBLE)

#### International Bond Futures (5 of 7 countries missing)
| Country | Required | Status |
|---------|----------|--------|
| Australia | ASX_XT1 | Missing |
| Canada | MX_CGB1 | Missing |
| Germany | EUREX_FGBL1 | Missing |
| UK | LIFFE_R1 | Missing |
| Italy | EUREX_FBTP1 | Missing |
| Japan | SGX_JB1 | Available (JB-Futures) |
| USA | CME_TY1 | Available (ZN-Futures) |

### Root Cause
**Missing international futures coverage** - Only 2 of 7 required country bond futures available. Bond yield data IS available via FRED, so the sole blocker is the futures data.

## Alternative Approaches

### 1. US-Japan Only (Partial Implementation)
Could implement with available futures (ZN, JB) + FRED yields:
- Rank US vs Japan by 10Y yield
- Long the higher-yielding country
- **Issue**: Only 2 countries, not statistically robust

### 2. US-Only Carry (Different Strategy)
Use US Treasury ETFs with different maturities as proxy:
- IEF (7-10 year), TLT (20+ year), SHY (1-3 year)
- Rank by yield spread or duration
- **Issue**: This is curve positioning, not cross-country carry

### 3. ETF Proxy with FRED Yields
If international bond ETFs become available, could use:
- BWX (International Treasury), IGOV (International Government)
- Rank by FRED yield data (already available)
- **Issue**: ETFs like BWX/IGOV not currently in asset universe

### 4. Feature Request
**Add international bond futures** (EUR, GBP, AUD, CAD exchanges) - yield data already available via FRED

## Implementation Notes
- Strategy is "Simple" in logic but requires specialized data
- Carry strategies rely on fundamental data (yields) not just prices
- 30 countries in full paper, 7 in QuantConnect implementation
- Monthly rebalance keeps turnover manageable
- No hedge for stock market downturns (high-yield bonds are risky)
