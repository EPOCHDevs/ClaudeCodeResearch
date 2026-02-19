# Post-Loss/Profit Announcement Drift in Stocks

**Quantpedia ID**: #0034
**URL**: https://quantpedia.com/strategies/post-loss-profit-announcement-drift-in-stocks
**Status**: ELIGIBLE
**Linear Issue**: [ENG-159](https://linear.app/epoch-inc/issue/ENG-159/implement-post-lossprofit-announcement-drift-0034)

## Overview

Variant of PEAD that focuses on the absolute profitability signal - specifically whether a company reports a profit or a loss. Stocks announcing unexpected losses drift lower, while those reporting unexpected profits drift higher. The strategy captures the market's delayed reaction to the fundamental signal of profitability.

## Trading Rules

**Universe**: US stocks with earnings announcements
**Signal**: Profit vs Loss announcement
**Selection**: Long unexpected profits, short unexpected losses
**Weighting**: Equal weight
**Rebalancing**: Daily/Event-based

### Detailed Rules
1. Monitor earnings announcements
2. Identify stocks reporting:
   - Unexpected profit: Actual EPS > 0 when estimate was negative (or large beat)
   - Unexpected loss: Actual EPS < 0 when estimate was positive (or large miss)
3. Go long stocks with surprise profits
4. Go short stocks with surprise losses
5. Hold for drift period (~60 days)

## Fundamental Reason

1. **Profitability Signal**: Profit/loss is the most fundamental business signal
2. **Investor Anchoring**: Investors slow to update beliefs about profitability
3. **Analyst Inertia**: Analysts slow to revise estimates after loss/profit transitions
4. **Loss Aversion**: Stronger reaction to loss announcements creates drift

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1976-2005 |
| Return | 26.0% p.a. |
| Volatility | 5.0% |
| Sharpe Ratio | 4.4 |
| Max Drawdown | -34.67% |

**Notes**: Premium strategy. Exceptionally high reported Sharpe requires further validation.

## Eligibility Check

### Required Capabilities
1. **Earnings Data**: Actual EPS to determine profit/loss
2. **Surprise Detection**: Compare actual vs expected
3. **Event-Based Trading**: Trade after announcements

### Available
- `earnings` data source with:
  - `actual_eps` - Actual reported EPS (positive = profit, negative = loss)
  - `estimated_eps` - Consensus estimate
  - `eps_surprise` - Surprise magnitude
  - `eps_surprise_percent`
- Cross-sectional ranking
- Event markers

### Missing
None - all required capabilities are available.

## Implementation Notes

1. **Profit/Loss Signal**:
   ```
   earn = earnings()
   actual_profit = earn.actual_eps > 0
   expected_loss = earn.estimated_eps < 0

   # Unexpected profit: was expected to lose, but reported profit
   unexpected_profit = actual_profit AND expected_loss

   # Unexpected loss: was expected to profit, but reported loss
   actual_loss = earn.actual_eps < 0
   expected_profit = earn.estimated_eps > 0
   unexpected_loss = actual_loss AND expected_profit
   ```

2. **Alternative - Magnitude Based**:
   ```
   # Large positive surprise = profit confirmation
   # Large negative surprise = loss confirmation
   big_beat = earn.eps_surprise_percent > 0.20  # >20% beat
   big_miss = earn.eps_surprise_percent < -0.20  # >20% miss
   ```

3. **Position Sizing**:
   ```
   long_signal = unexpected_profit
   short_signal = unexpected_loss
   ```

4. **Rebalancing**: Event-based or daily for new announcements

### Considerations
- High Sharpe (4.4) in paper seems unusually high - validate carefully
- Transaction costs from frequent trading
- Consider combining with other factors
- Focus on clear profit/loss transitions

## Related Strategies

- #0033 Post-Earnings Announcement Effect (PEAD)
- Earnings momentum strategies
- SUE-based strategies

## Notes

This is a Premium Quantpedia strategy. Uses same `earnings` data source as #0033 but focuses specifically on profit vs loss transitions.
