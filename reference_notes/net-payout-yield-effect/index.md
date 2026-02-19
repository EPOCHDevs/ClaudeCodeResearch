# Net Payout Yield Effect

**Quantpedia ID**: #0036
**URL**: https://quantpedia.com/strategies/net-payout-yield-effect
**Status**: ELIGIBLE
**Linear Issue**: [ENG-162](https://linear.app/epoch-inc/issue/ENG-162/implement-net-payout-yield-effect-0036)

## Overview

The Net Payout Yield effect extends the traditional dividend yield anomaly by including share repurchases. Companies that return more cash to shareholders through dividends AND buybacks tend to outperform. This captures the full shareholder yield, which has become more important as companies shift from dividends to buybacks.

## Trading Rules

**Universe**: US stocks
**Signal**: Net Payout Yield = (Dividends + Net Repurchases) / Market Cap
**Selection**: Long highest net payout yield quintile
**Weighting**: Equal weight
**Rebalancing**: Yearly

### Detailed Rules
1. Calculate dividends from cash flow statement
2. Calculate net repurchases from change in shares outstanding
3. Compute Net Payout Yield = (Div + Repurchases) / Market Cap
4. Rank stocks by net payout yield
5. Long stocks in highest quintile
6. Rebalance annually

### Signal Calculation
```
Net Payout = Dividends + (Decrease in Shares × Price)
Net Payout Yield = Net Payout / Market Cap
```

## Fundamental Reason

1. **Shareholder Returns**: High net payout signals strong cash generation
2. **Management Confidence**: Buybacks signal management believes stock is undervalued
3. **Capital Discipline**: High payout reduces agency costs and empire building
4. **Earnings Quality**: Companies paying out cash have less accounting manipulation

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1984-2003 |
| Return | 22.13% p.a. |
| Max Drawdown | -52.5% |

**Notes**: Boudoukh, Michaely, Richardson, Roberts (2007)

## Source Paper

**Boudoukh, Michaely, Richardson, Roberts: "On the Importance of Measuring Payout Yield"**
- Journal of Finance, 2007

**Abstract**: We examine the predictive power of payout yield for the cross-section of stock returns. We find that payout yield is a more comprehensive measure of shareholder yield than dividend yield alone, and has stronger predictive power for returns.

## Eligibility Check

### Required Capabilities
1. **Dividends Paid**: From cash flow statement
2. **Share Repurchases**: From change in shares outstanding
3. **Market Cap**: For yield calculation
4. **Cross-Sectional Ranking**

### Available
- `cash_flow.dividends` - Dividends paid
- `ipos.shares_outstanding` or balance sheet shares - Change in shares
- `finance_ratio(ratio_type='market_cap')` - Market cap
- `cs_rank` - Cross-sectional ranking

### Missing
None - all required capabilities are available through proxies.

## Implementation Notes

1. **Dividends**:
   ```
   cf = cash_flow(period='trailing_twelve_months')
   dividends = cf.dividends
   ```

2. **Net Repurchases** (approximation from shares outstanding change):
   ```
   # Get shares outstanding from IPO/fundamental data
   current_shares = shares_outstanding
   prior_shares = lag(shares_outstanding, 252)  # 1 year ago
   share_change = current_shares - prior_shares
   # Negative change = buyback
   net_repurchases = -share_change * close  # Dollar value
   ```

3. **Net Payout Yield**:
   ```
   market_cap = finance_ratio(ratio_type='market_cap')
   net_payout = dividends + net_repurchases
   net_payout_yield = net_payout / market_cap
   ```

4. **Ranking and Selection**:
   ```
   yield_rank = cs_rank(net_payout_yield)
   long_signal = yield_rank >= percentile_80  # Top quintile
   ```

5. **Rebalancing**: Yearly using `rebalance_interval='yearly'`

### Considerations
- Share repurchase proxy may miss some buyback transactions
- Consider filtering for profitable companies
- May need to handle negative payouts (net issuance) separately
- Combines well with other quality/value factors

## Related Strategies

- #0026 Value (Book-to-Market) Factor
- Dividend yield strategies
- Shareholder yield strategies

## Related Papers

1. **Fama, French (2001)**: "Disappearing Dividends"
2. **Grullon, Michaely (2002)**: "Dividends, Share Repurchases, and the Substitution Hypothesis"
