# Insiders Trading Effect in Stocks

**Quantpedia ID**: #0035
**URL**: https://quantpedia.com/strategies/insiders-trading-effect-in-stocks
**Status**: INELIGIBLE
**Linear Issue**: [ENG-160](https://linear.app/epoch-inc/issue/ENG-160/feature-request-sec-form-4-insider-trading-data-for-0035)

## Overview

Strategy that follows corporate insider buying and selling patterns as a signal for future stock returns. Corporate insiders (executives, directors, large shareholders) have informational advantage about their companies. When insiders are net buyers, it's typically bullish; net sellers is bearish.

## Trading Rules

**Universe**: US stocks with insider trading activity
**Signal**: Net insider buying/selling
**Selection**: Long net insider buying, short net insider selling
**Weighting**: Equal weight
**Rebalancing**: Yearly

### Detailed Rules
1. Track SEC Form 4 filings for insider transactions
2. Calculate net insider buying (purchases - sales) by dollar value
3. Rank stocks by net insider activity
4. Long stocks with highest net buying
5. Short stocks with highest net selling
6. Rebalance annually

## Fundamental Reason

1. **Information Asymmetry**: Insiders know more about their company's prospects
2. **Signaling**: Insider buying signals confidence in future performance
3. **Legal Constraints**: Insiders face legal penalties for trading on material non-public info, making their trades more informative
4. **Skin in the Game**: Insider purchases represent real financial commitment

## Performance (Source)

| Metric | Value |
|--------|-------|
| Period | 1976-1995 |
| Return | 7.7% p.a. |
| Max Drawdown | -37.85% |

**Notes**: Premium strategy with negative OOS performance.

## Eligibility Check

### Required Capabilities
1. **SEC Form 4 Insider Trading Data**: Insider transaction filings
2. **Transaction Details**: Buy/sell, shares, price, insider role

### Available
- `analyst_ratings` - Related but different signal
- `short_interest` - Related alternative data
- Various fundamental data sources

### MISSING - Why INELIGIBLE

**Insider Trading Data Source**: No SEC Form 4 data available:
- Insider transaction dates
- Transaction type (buy/sell/option exercise)
- Dollar value of transactions
- Insider role (CEO, Director, 10% owner)
- Net insider activity calculations

The example in `datetime_diff` usage mentions `sec_insider_trading()` but this data source does not exist in the current platform.

## Implementation Notes

### If Insider Trading Data Becomes Available
1. **Net Buying Signal**:
   ```
   insider = sec_insider_trading()
   buy_value = sum(insider.shares * insider.price, where insider.type == 'P')
   sell_value = sum(insider.shares * insider.price, where insider.type == 'S')
   net_buying = buy_value - sell_value
   ```

2. **Ranking**:
   ```
   net_rank = cs_rank(net_buying)
   long_signal = net_rank >= percentile_90  # Top 10% net buyers
   short_signal = net_rank <= percentile_10  # Top 10% net sellers
   ```

3. **Alternative Metrics**:
   - Number of insiders buying vs selling
   - Ratio of buy to sell transactions
   - Officer vs director transactions

## Related Strategies

- Corporate event strategies
- Alternative data strategies
- Sentiment-based strategies

## Notes

This is a Premium Quantpedia strategy. OOS performance is negative (-5.5% Sharpe), suggesting the effect may have diminished. Requires SEC Form 4 data to implement.
