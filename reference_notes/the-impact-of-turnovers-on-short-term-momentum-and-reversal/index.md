# The Impact of Turnovers on Short-Term Momentum and Reversal

**Quantpedia ID**: #0410
**URL**: https://quantpedia.com/strategies/the-impact-of-turnovers-on-short-term-momentum-and-reversal
**Status**: ELIGIBLE
**Linear Issue**: [ENG-167](https://linear.app/epoch-inc/issue/ENG-167/implement-the-impact-of-turnovers-on-short-term-momentum-and-reversal)

## Overview
This strategy exploits the relationship between stock turnover and short-term return patterns. High-turnover stocks exhibit short-term momentum (information gradually diffusing), while low-turnover stocks exhibit short-term reversal (noise trading correcting). The strategy combines both effects by going long winners/short losers in high-turnover stocks and long losers/short winners in low-turnover stocks.

## Trading Rules
**Universe**: All common shares on NYSE, AMEX, NASDAQ
- Filter to large caps only (above median NYSE market cap)

**Signal**: Double-sort on prior month return and share turnover
- Prior return: Return from t-1 to t
- Turnover: Volume / Shares Outstanding

**Selection**:
1. Sort stocks into large/small caps (median NYSE market cap breakpoint)
2. Use large caps only
3. Sort by prior month return into quintiles (20th/80th percentile for NYSE)
4. Within each, sort by turnover (20th/80th percentile for NYSE)

**Portfolio Construction** (two equally-weighted components):
1. **Low Turnover (Reversal)**: Long losers, short winners
2. **High Turnover (Momentum)**: Long winners, short losers

**Weighting**: Value-weighted within each leg
**Rebalancing**: Monthly

## Fundamental Reason
Two competing forces coexist in short-term returns:
1. **Low turnover stocks** - Price movements driven by noise trading; subsequent correction leads to reversal
2. **High turnover stocks** - Price movements reflect private information gradually diffusing; leads to momentum

High turnover indicates investor disagreement about informativeness of signals. When informed investors trade on new private information, turnover rises and prices move but don't fully incorporate information (momentum). When uninformed noise traders dominate (low turnover), prices deviate from fundamentals and subsequently correct (reversal).

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1963-2016 |
| Return | 9.51% p.a. |
| Volatility | Not stated |
| Max Drawdown | -48.04% |
| Sharpe Ratio | Not stated |

Note: Data from Table IX, Panel A, Liquid stocks, annualized average monthly return of 0.76% (avg of 0.88% and 0.64%).

## Source Paper
Medhat, Mamdouh and Schmeling, Maik: Short-Term Momentum
- SSRN: https://ssrn.com/abstract=3150525

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238501/

## Eligibility Check
### Available
- **Transforms**:
  - `roc` - Prior month return calculation
  - `cs_rank` - Cross-sectional ranking for quintile sorting
  - `market_cap` - Market cap for size filtering
  - `shares_outstanding` - For turnover calculation
  - Volume data via `src.v`
- **Assets**: US Stocks available (NYSE, AMEX, NASDAQ universe)

### Formula
```
Turnover = Volume / Shares_Outstanding

Portfolio = 0.5 * Low_Turnover_Reversal + 0.5 * High_Turnover_Momentum

Low_Turnover_Reversal = Long(Low_Return, Low_Turnover) - Short(High_Return, Low_Turnover)
High_Turnover_Momentum = Long(High_Return, High_Turnover) - Short(Low_Return, High_Turnover)
```

## Implementation Notes
- Strategy is marked ELIGIBLE with all required data available
- Confidence rating: Strong
- Complexity: Complex (requires double-sort and combined portfolio)
- Works best on large, liquid stocks
- Use NYSE breakpoints for percentile ranking (20th/80th)
- Strategy has been tested internationally in 22 developed markets
- Monthly rebalancing is straightforward

