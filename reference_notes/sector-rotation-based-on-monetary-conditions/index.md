# Sector Rotation based on Monetary Policy

**Quantpedia ID**: #0010
**URL**: https://quantpedia.com/strategies/sector-rotation-based-on-monetary-policy
**Status**: ELIGIBLE
**Linear Issue**: [ENG-21](https://linear.app/epoch-inc/issue/ENG-21/implement-sector-rotation-based-on-monetary-policy-0010)

## Overview
This strategy rotates between cyclical and defensive sector portfolios based on Federal Reserve monetary policy stance. During expansive monetary policy periods (rate cuts), the strategy holds cyclical sectors. During restrictive periods (rate hikes), it holds defensive sectors. The approach exploits the differential sensitivity of economic sectors to monetary conditions.

## Trading Rules
**Universe**: 10 U.S. sector groups divided into cyclical and defensive categories

**Cyclical Sectors (6)**:
- Consumer Discretionary (XLY)
- Communication Services (XLC)
- Industrials (XLI)
- Technology (XLK)
- Financials (XLF)
- Materials (XLB)

**Defensive Sectors (4)**:
- Energy (XLE)
- Consumer Staples (XLP)
- Healthcare (XLV)
- Utilities (XLU)

**Signal**: Federal Reserve monetary policy stance
- **Expansive** (Fed cutting rates): Hold cyclical sectors equally weighted
- **Restrictive** (Fed raising rates): Hold defensive sectors equally weighted

**Weighting**: Equal weight within selected sector group
**Rebalancing**: Yearly (or when Fed policy stance changes)

## Fundamental Reason
1. **Interest Rate Sensitivity**: Cyclical sectors (financials, consumer discretionary) benefit from lower rates and economic expansion, while defensive sectors (utilities, staples) are less sensitive to rate changes.

2. **Economic Cycle Alignment**: Fed typically cuts rates during economic weakness and raises during strength. Cyclical sectors outperform during recovery/expansion phases that follow rate cuts.

3. **Credit Conditions**: Lower rates improve credit availability, benefiting growth-oriented sectors that rely on borrowing for expansion.

4. **Valuation Impact**: Rate cuts reduce discount rates, disproportionately benefiting high-growth sectors with more distant cash flows.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1973-2005 |
| Return | 15.82% p.a. |
| Volatility | 15.5% |
| Max Drawdown | -62.84% |
| Sharpe Ratio | 0.76 |

## Out-of-Sample Performance (Quantpedia)
| Metric | Value |
|--------|-------|
| Period | 1999-2025 |
| Return | 9.3% p.a. |
| Volatility | 20.67% |
| Max Drawdown | -62.86% |
| Sharpe Ratio | 0.45 |

## Source Paper
**Sector Rotation and Monetary Conditions**
- Authors: C. Mitchell Conover, Gerald R. Jensen, Robert R. Johnson, Jeffrey M. Mercer
- Journal: Journal of Investing (2008)
- Key Finding: Cyclical sectors significantly outperform defensive sectors during expansive monetary policy periods, with the reverse during restrictive periods.

## Eligibility Check
### Available
**Transforms:**
- `common_economic_indicators(category="FedFunds")` - Federal Funds Effective Rate
- `common_economic_indicators(category="FedFundsTarget")` - Federal Funds Target Rate
- `roc(close, period)` - Rate of Change for detecting policy direction
- `diff()` - Difference for detecting rate changes

**Assets (Sector ETFs):**
- XLY-Stocks (Consumer Discretionary) - Cyclical
- XLC-Stocks (Communication Services) - Cyclical
- XLI-Stocks (Industrials) - Cyclical
- XLK-Stocks (Technology) - Cyclical
- XLF-Stocks (Financials) - Cyclical
- XLB-Stocks (Materials) - Cyclical
- XLE-Stocks (Energy) - Defensive
- XLP-Stocks (Consumer Staples) - Defensive
- XLV-Stocks (Healthcare) - Defensive
- XLU-Stocks (Utilities) - Defensive

### Missing
None - all required components available.

## Implementation Notes
1. **Timeframe**: Monthly bars for Fed Funds Rate monitoring
2. **Policy Detection Logic**:
   - Calculate `diff(common_economic_indicators(category="FedFunds"))` to detect rate changes
   - Alternatively, use `roc(fed_funds, 12)` to detect 12-month rate trend
   - Negative change/ROC = Expansive policy (rate cuts) = Hold cyclicals
   - Positive change/ROC = Restrictive policy (rate hikes) = Hold defensives
3. **Signal Logic**:
   ```
   fed_rate = common_economic_indicators(category="FedFunds")
   rate_change = diff(fed_rate, 1)  # or roc(fed_rate, 12)

   if rate_change < 0:  # Expansive - rates falling
       hold: XLY, XLC, XLI, XLK, XLF, XLB (equal weight)
   else:  # Restrictive - rates rising or flat
       hold: XLE, XLP, XLV, XLU (equal weight)
   ```
4. **Position Management**: Equal weight across 4-6 sectors depending on regime
5. **Rebalance Trigger**: Yearly or on policy regime change
6. **Lag Consideration**: Fed rate data has publication lag - use point-in-time data

## Alternative Implementations
1. **FOMC Meeting Based**: Trade around FOMC announcements rather than continuous monitoring
2. **Yield Curve Based**: Use Treasury spread (10Y-2Y) as proxy for monetary conditions
3. **Multiple Signal Confirmation**: Combine Fed Funds with yield curve and Fed balance sheet

## QuantConnect Reference Code
```python
# https://quantpedia.com/strategies/sector-rotation-based-on-monetary-policy/
#
# Stocks in the US equity market are divided into ten sectors: Resources, Noncyclical Consumer Goods,
# Noncyclical Services, and Utilities such as defense sectors and Cyclical Consumer Goods,
# Cyclical Services, General Industrials, Information Technology, Financials, and Basic Industries
# as cyclical sectors. As this allocation doesn't exactly fit a standard sector decomposition,
# it isn't possible to use conventional ten sector ETFs for all sectors, and some sectors used in
# this strategy must be created directly from stocks or industry ETFs or funds. The portfolio is
# then made up of equally-weighted six cyclical sectors during periods of expansive monetary policy
# and equally weighted four noncyclical sectors during periods of restrictive monetary policy.
# The period of the restrictive policy starts after the FED begins to raise rates and lasts until
# it starts to cut rates when we enter a period of the expansive policy.
#
# QC implementation changes:
# - Combination of set FED policy change dates and external FED rates is used to distinguish monetary policy.

from AlgorithmImports import *
from pandas.tseries.offsets import BDay

class SectorRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(1999, 1, 1)
        self.SetCash(100_000)

        self.cyclical: List[str] = ["XLY", "XLK", "XLF", "XLI"]
        self.defensive: List[str] = ["XLU", "XLP", "XLV", "XLB", "XLE"]

        for symbol in self.cyclical:
            self.AddEquity(symbol, Resolution.Daily)
        for symbol in self.defensive:
            self.AddEquity(symbol, Resolution.Daily)

        # changes in FED policy from restrictive to expansive dates
        dates_str: List[str] = ["24.08.1999", "03.01.2001", "30.06.2004", "18.09.2007", "14.12.2016", "31.7.2019"]
        self.dates: List[datetime.date] = [datetime.strptime(x, "%d.%m.%Y").date() for x in dates_str]

        # import quandl federal rate data
        self.target_rate: Symbol = self.AddData(FederalTargetRange, 'DFEDTARU', Resolution.Daily).Symbol

        self.restrictive_flag: bool = True  # from start of the algorithm
        self.last_target_rate: Union[None, float] = None
        self.external_restrictive_flag: Union[None, bool] = None

    def OnData(self, data: Slice) -> None:
        if self.target_rate in data and data[self.target_rate]:
            curr_target_rate: float = data[self.target_rate].Value
            curr_date: datetime.date = self.Time.date()
            restrictive_flag: Union[None, bool] = None

            # switch to external data source, when self.dates ends
            if self.Time.date() > self.dates[-1]:
                if self.last_target_rate:
                    if curr_target_rate > self.last_target_rate and self.restrictive_flag:
                        restrictive_flag = True
                        self.dates.append((curr_date + BDay(1)).date())
                    elif curr_target_rate < self.last_target_rate and not self.restrictive_flag:
                        restrictive_flag = False
                        self.dates.append((curr_date + BDay(1)).date())

                if restrictive_flag is not None:
                    self.external_restrictive_flag = restrictive_flag

            self.last_target_rate = curr_target_rate

        if self.Time.date() in self.dates:
            # if external data is present, trade out of it
            if self.external_restrictive_flag is not None:
                restrictive_flag: bool = self.external_restrictive_flag

                # end of quandl target rate data
                ftr_last_update_date: Dict[Symbol, datetime.date] = FederalTargetRange.get_last_update_date()
                if (self.Securities[self.target_rate].GetLastData() and
                    self.target_rate in ftr_last_update_date and
                    self.Time.date() >= ftr_last_update_date[self.target_rate]):
                    self.Liquidate()
                    return
            else:
                restrictive_flag: bool = self.restrictive_flag

            if restrictive_flag:
                for symbol in self.cyclical:
                    self.Liquidate(symbol)
                for symbol in self.defensive:
                    self.SetHoldings(symbol, 1/len(self.defensive))
                self.restrictive_flag = False
            else:
                for symbol in self.defensive:
                    self.Liquidate(symbol)
                for symbol in self.cyclical:
                    self.SetHoldings(symbol, 1/len(self.cyclical))
                self.restrictive_flag = True


# source: https://fred.stlouisfed.org/series/DFEDTARU
class FederalTargetRange(PythonData):
    def GetSource(self, config: SubscriptionDataConfig, date: datetime, isLiveMode: bool) -> SubscriptionDataSource:
        return SubscriptionDataSource(
            'data.quantpedia.com/backtesting_data/economic/DFEDTARU.csv',
            SubscriptionTransportMedium.RemoteFile,
            FileFormat.Csv
        )

    _last_update_date: Dict[Symbol, datetime.date] = {}

    @staticmethod
    def get_last_update_date() -> Dict[Symbol, datetime.date]:
        return FederalTargetRange._last_update_date

    def Reader(self, config: SubscriptionDataConfig, line: str, date: datetime, isLiveMode: bool) -> BaseData:
        data = FederalTargetRange()
        data.Symbol = config.Symbol

        if not line[0].isdigit():
            return None

        split = line.split(';')

        # Parse the CSV file's columns into the custom data class
        data.Time = datetime.strptime(split[0], "%Y-%m-%d") + timedelta(days=1)
        data.Value = float(split[1])

        if config.Symbol not in FederalTargetRange._last_update_date:
            FederalTargetRange._last_update_date[config.Symbol] = datetime(1, 1, 1).date()

        if data.Time.date() > FederalTargetRange._last_update_date[config.Symbol]:
            FederalTargetRange._last_update_date[config.Symbol] = data.Time.date()

        return data
```

## Related Research
- Conover et al. found 12% annual return difference between cyclical and defensive sectors based on monetary regime
- Effect is robust across different sector classification schemes
- Partial explanation for January effect (policy often changes early in year)
