# Net Current Asset Value Effect

**Quantpedia ID**: #0037
**URL**: https://quantpedia.com/strategies/net-current-asset-value-effect
**Status**: ELIGIBLE
**Linear Issue**: [ENG-164](https://linear.app/epoch-inc/issue/ENG-164/implement-net-current-asset-value-effect-0037)

## Overview

Benjamin Graham's classic deep value strategy. Buy stocks trading below their Net Current Asset Value (NCAV) - the liquidation value of current assets minus all liabilities. These "net-nets" are extreme value plays where the market prices the company below its bankruptcy liquidation value.

## Trading Rules

**Universe**: European stocks (original paper)
**Signal**: NCAV / Market Cap ratio
**Selection**: Stocks trading below NCAV (Price < NCAV per share)
**Weighting**: Equal weight
**Rebalancing**: Yearly

### Detailed Rules
1. Calculate NCAV = Current Assets - Total Liabilities
2. Calculate NCAV per share = NCAV / Shares Outstanding
3. Identify stocks where Price < NCAV per share (or Price < 2/3 NCAV for Graham's original criterion)
4. Long these "net-net" stocks
5. Hold for one year or until price exceeds NCAV
6. Rebalance annually

### Signal Calculation
```
NCAV = Current Assets - Total Liabilities
NCAV/MV Ratio = NCAV / Market Cap
Net-Net = NCAV/MV Ratio > 1 (trading below liquidation value)
```

## Fundamental Reason

1. **Margin of Safety**: Buying below liquidation value provides downside protection
2. **Mean Reversion**: Extreme undervaluation tends to correct
3. **Acquisition Target**: Companies below NCAV are attractive acquisition targets
4. **Activist Potential**: Low prices invite activist investors to unlock value

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1980-2005 |
| Return | 31.19% p.a. |
| Max Drawdown | -76.86% |

**Notes**: European stocks. Very high returns but also high drawdowns.

## Source Paper

**Oppenheimer: "Ben Graham's Net Current Asset Values: A Performance Update"**
- Financial Analysts Journal, 1986

## Eligibility Check

### Required Capabilities
1. **Current Assets**: Balance sheet data
2. **Total Liabilities**: Balance sheet data
3. **Market Cap**: For comparison
4. **Cross-Sectional Selection**

### Available
- `balance_sheet.current_assets` - Current assets
- `balance_sheet.total_liabilities` - Total liabilities
- `balance_sheet.current_liabilities` - Current liabilities
- `finance_ratio(ratio_type='market_cap')` - Market cap
- `cs_rank` - Cross-sectional ranking

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **NCAV Calculation**:
   ```
   bs = balance_sheet(period='quarterly')
   ncav = bs.current_assets - bs.total_liabilities
   ```

2. **NCAV/MV Ratio**:
   ```
   market_cap = finance_ratio(ratio_type='market_cap')
   ncav_ratio = ncav / market_cap
   ```

3. **Selection**:
   ```
   # Graham's criterion: Price < 2/3 NCAV
   net_net = ncav_ratio > 1.5  # NCAV 1.5x market cap

   # Or less strict: Any stock below NCAV
   cheap = ncav_ratio > 1.0
   ```

4. **Ranking** (if too many candidates):
   ```
   # Rank by NCAV ratio, select cheapest
   ncav_rank = cs_rank(ncav_ratio)
   long_signal = ncav_rank >= percentile_90
   ```

5. **Rebalancing**: Yearly using `rebalance_interval='yearly'`

### Considerations
- Very few stocks qualify (net-nets are rare)
- Often small/micro caps with liquidity issues
- High drawdowns require conviction
- May need to expand universe (US + Europe)
- Consider additional quality screens to avoid value traps

## Related Strategies

- #0026 Value (Book-to-Market) Factor
- Deep value strategies
- Distressed investing

## Related Papers

1. **Graham, Dodd (1934)**: "Security Analysis"
2. **Graham (1949)**: "The Intelligent Investor"
3. **Greenblatt (1999)**: "You Can Be a Stock Market Genius"
