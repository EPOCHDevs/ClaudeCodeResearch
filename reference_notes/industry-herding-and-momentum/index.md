# Industry Herding and Momentum

**Quantpedia ID**: #0423
**URL**: https://quantpedia.com/strategies/industry-herding-and-momentum
**Status**: ELIGIBLE
**Linear Issue**: [ENG-266](https://linear.app/epoch-inc/issue/ENG-266/implement-industry-herding-and-momentum-0423)

## Overview
This strategy enhances industry momentum by filtering for low-herding industries. High herding helps incorporate information into prices and weakens momentum; low herding preserves momentum profitability. By identifying industries with low investor herding (high cross-sectional return dispersion), the strategy exploits stronger momentum effects.

## Trading Rules
**Universe**: 49 Fama-French industries (or sector ETFs)

**Signal**: CSSD (Cross-Sectional Standard Deviation) + Momentum
1. Calculate CSSD of individual stock returns within each industry (past 1 month)
2. Normalize CSSD: (CSSD - Mean) / StdDev
3. Top 30% by normalized CSSD = low herding industries
4. Calculate momentum (past 6-month returns, skip 1 month) for each industry
5. From low-herding industries:
   - Long top 50% by momentum
   - Short bottom 50% by momentum

**Selection**:
- Filter industries by herding level (low herding = high CSSD)
- Long/short based on momentum within low-herding set

**Weighting**: Equally-weighted
**Rebalancing**: Monthly

## Fundamental Reason
- High herding helps impound information into prices, making markets more efficient
- This weakens the momentum anomaly (prices already reflect information)
- Low herding = slower information incorporation = stronger momentum persistence
- By selecting low-herding industries, we capture stronger momentum effects
- Works as a hedge during economic crises (see Exhibit 5 of source paper)

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1980-2008 |
| Return | 14.43% p.a. |
| Volatility | 30.7% |
| Max Drawdown | -56.37% |
| Sharpe Ratio | 0.34 |

Note: Data from Exhibit 2, Low-herding winner - Low-herding loser spread.

**WARNING**: OOS backtest (2003-2025) shows -1.2% Sharpe and -52.5% max drawdown. Strategy alpha may have deteriorated.

## Source Paper
Yan, Zhipeng and Zhao, Yan and Sun, Libo Alice: Industry Herding and Momentum
- SSRN: https://ssrn.com/abstract=3309787

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238562/

## Eligibility Check
### Available
- **Transforms**:
  - `cs_agg(type=Std, group_by=industry)` - Cross-sectional std dev within industries
  - `cs_zscore` - Normalization of CSSD
  - `roc(period=126)` - 6-month momentum calculation
  - `cs_rank` - Cross-sectional ranking for quintile sorting
  - `cs_quantile` - Quantile filtering for top 30%
  - `sector` / `industry` grouping available
- **Assets**:
  - Sector ETFs: XLK, XLF, XLE, XLV, XLP, XLI, XLY, XLB, XLU, XLC
  - US Stocks with sector/industry classification

### Formula
```
# Step 1: CSSD within each industry
cssd = cs_agg(type=Std, group_by=industry)(roc(period=21))

# Step 2: Normalize CSSD
normalized_cssd = cs_zscore()(cssd)

# Step 3: Low herding = top 30% by CSSD (high dispersion)
low_herding = cs_quantile(quantile=0.7)(normalized_cssd)

# Step 4: Momentum for low-herding industries
momentum = roc(period=126)

# Step 5: Long top 50%, short bottom 50% within low herding
signal = where(low_herding, cs_rank()(momentum), null)
```

## Implementation Notes
- Strategy is marked ELIGIBLE with all required transforms available
- Confidence rating: Moderate (OOS shows negative performance)
- Complexity: Complex (two-stage filtering)
- Implementation approach:
  1. Use sector ETFs as tradeable universe
  2. For each sector, compute CSSD of constituent stock returns
  3. Rank sectors by normalized CSSD
  4. Apply momentum filter within low-herding sectors
- Consider using 11 GICS sectors instead of 49 Fama-French industries
- Poor OOS suggests strategy alpha may be gone

