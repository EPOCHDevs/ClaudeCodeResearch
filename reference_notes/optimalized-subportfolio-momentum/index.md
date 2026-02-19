# Optimalized Subportfolio Momentum

**Quantpedia ID**: #0437
**URL**: https://quantpedia.com/strategies/optimalized-subportfolio-momentum
**Status**: ELIGIBLE
**Linear Issue**: [ENG-280](https://linear.app/epoch-inc/issue/ENG-280/implement-optimalized-subportfolio-momentum-0437)

## Overview
This strategy applies momentum to a portfolio of sector ETFs with dynamic optimization of lookback period and number of positions. It uses EMAR (exponential moving average of returns) and compares each sector's momentum to cash returns. Sectors underperforming cash are replaced with cash allocation. The lookback period is optimized monthly for best Sharpe ratio.

## Trading Rules
**Universe**: 10 sector ETFs (French's industrial sectors)

**Signal**: Optimized momentum with cash filter
1. Maximum lookback period: 18 months
2. Calculate EMAR (exponential moving average of monthly returns) for each sector
3. For each month, optimize:
   - Number of sectors to hold
   - Lookback period
   - Target: Maximum Sharpe ratio
4. Sector must beat cash momentum to be held
5. Replace underperforming sectors with cash

**Selection**:
- Long sectors with momentum > cash momentum
- Cash for sectors underperforming cash

**Weighting**: Equal-weighted (among held sectors)
**Rebalancing**: Monthly

## Fundamental Reason
- Momentum anomaly well-established in academic literature
- Dynamic lookback optimization adapts to market conditions
- Cash filter avoids holding declining sectors during crashes
- Strategy avoided 2007-2008 crisis by moving to cash
- Optimization across combinations improves risk-adjusted returns

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1937-2017 |
| Return | 19.8% p.a. |
| Volatility | 23.25% |
| Max Drawdown | -30.79% |
| Sharpe Ratio | 0.85 |

Note: Data from Figure 2, column 6.

**OOS (2013-2025)**: 10.0% return, 0.63 Sharpe. Strong positive alpha retained.

## Source Paper
O'Connor, Michael C.: Fund and Subportfolio Momentum
- SSRN: https://ssrn.com/abstract=3364124

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238652/

## Eligibility Check
### Available
- **Transforms**:
  - `roc` - Monthly return calculation
  - `ema` - Exponential moving average
  - `cs_rank` - Cross-sectional ranking
- **Assets** (all 10 sector ETFs):
  - XLK-Stocks (Technology) ✓
  - XLF-Stocks (Financials) ✓
  - XLE-Stocks (Energy) ✓
  - XLV-Stocks (Health Care) ✓
  - XLP-Stocks (Consumer Staples) ✓
  - XLI-Stocks (Industrials) ✓
  - XLY-Stocks (Consumer Discretionary) ✓
  - XLB-Stocks (Materials) ✓
  - XLU-Stocks (Utilities) ✓
  - XLC-Stocks (Communication Services) ✓

### Formula
```
# EMAR (Exponential Moving Average of Returns)
monthly_return = roc(period=21)
emar = ema(period=lookback)(monthly_return)

# Cash comparison (T-bills or money market proxy)
# Hold sector if emar > cash_return

# Optimize lookback from 1-18 months for best Sharpe
```

## Implementation Notes
- Strategy is marked ELIGIBLE with all 10 sector ETFs available
- Confidence rating: Strong
- Complexity: Complex (dynamic optimization required)
- Good OOS (0.63 Sharpe) indicates robust alpha
- Key implementation challenges:
  1. Dynamic lookback optimization
  2. Cash return comparison (need T-bill or money market proxy)
  3. Walk-forward Sharpe optimization
- Long-only with cash allocation (no hedge capability)
- Suitable for implementation priority: HIGH

