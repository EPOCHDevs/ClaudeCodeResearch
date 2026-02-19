# Market Timing S&P 500 with VIX and COT Report

**Quantpedia ID**: #0029
**URL**: https://quantpedia.com/strategies/market-timing-sp-500-with-vix-and-cot-report
**Status**: INELIGIBLE
**Linear Issue**: [ENG-116](https://linear.app/epoch-inc/issue/ENG-116/feature-request-cftc-cot-commitment-of-traders-data-for-0029)

## Overview

Market timing strategy that combines volatility (VIX) and sentiment (COT) signals to time S&P 500 exposure. Uses the Commitment of Traders report to gauge commercial hedger vs speculator positioning, combined with VIX levels to identify favorable market conditions.

## Trading Rules

**Universe**: S&P 500 (SPY)
**Signal**: VIX levels + COT positioning
**Selection**: Binary (long market or cash)
**Weighting**: All-in or cash
**Rebalancing**: Weekly

### Signal Components
1. **VIX Level**: Market fear/complacency indicator
2. **COT Report**: Net commercial positioning in S&P 500 futures
   - Commercial hedgers: "Smart money" positioning
   - Speculators: Often wrong at extremes

### Trading Logic
- When VIX is elevated AND commercials are net long → bullish signal
- When VIX is low AND speculators are extremely long → bearish signal
- Combine signals for market timing decisions

## Fundamental Reason

1. **VIX as Fear Gauge**: High VIX often precedes market bottoms
2. **COT Smart Money**: Commercial hedgers have superior information
3. **Contrarian Indicator**: Extreme speculator positioning often marks reversals
4. **Combined Signal**: Reduces false signals from either indicator alone

## Performance (Source)

| Metric | Value |
|--------|-------|
| Period | 2000-2005 |
| Return | 8.39% p.a. |
| Volatility | 12.08% |
| Sharpe Ratio | 0.44 |
| Max Drawdown | -6.74% |

**Notes**: Premium strategy - full details require Quantpedia Premium access.

## Eligibility Check

### Required Capabilities
1. **VIX Data**: Volatility index levels
2. **COT Report Data**: CFTC Commitment of Traders positioning data
3. **S&P 500 Data**: Price data for timing decisions

### Available
- VIX index data via `economic_data` (FRED VIX series)
- VIX ETFs: VIXY, VIXM, SVIX, UVIX available
- SPY price data available

### MISSING - Why INELIGIBLE

1. **COT (Commitment of Traders) Report Data**: No data source for:
   - Commercial hedger net positioning
   - Non-commercial (speculator) net positioning
   - Open interest by trader category
   - Weekly CFTC reports

The COT report is alternative data published weekly by the CFTC. Without this positioning data, the strategy cannot be implemented as designed.

## Implementation Notes

### If COT Data Becomes Available
1. **VIX Signal**:
   ```
   vix = economic_data(series_id='VIXCLS')  # VIX from FRED
   vix_z = z_score(vix, window=252)
   ```

2. **COT Signal**:
   ```
   commercial_net = cot_data(category='commercial', asset='ES')
   speculator_net = cot_data(category='speculator', asset='ES')
   cot_ratio = commercial_net / (commercial_net + speculator_net)
   ```

3. **Combined Signal**:
   ```
   bullish = vix_z > 1 AND cot_ratio > threshold
   bearish = vix_z < -1 AND cot_ratio < threshold
   ```

### Partial Implementation (VIX-Only)
A simplified version could use only VIX for market timing:
- VIX > 25 and declining → buy signal
- VIX < 15 → reduce exposure

## Related Strategies

- #0027 Market Timing with Aggregate and Idiosyncratic Stock Volatilities
- VIX-based strategies
- Sentiment-based market timing

## Notes

This is a Premium Quantpedia strategy. Full trading rules require Quantpedia Premium access. COT data would need to be added as a new data source to implement this strategy.
