# Timing Commodities and S&P 500 with COT Report

**Quantpedia ID**: #0030
**URL**: https://quantpedia.com/strategies/timing-commodities-and-sp500-with-cot-report
**Status**: INELIGIBLE
**Linear Issue**: [ENG-116](https://linear.app/epoch-inc/issue/ENG-116/feature-request-cftc-cot-commitment-of-traders-data-for-0029) (blocked by same feature)

## Overview

Market timing strategy that uses CFTC Commitment of Traders (COT) report data to time exposure to both commodities and S&P 500. Uses the positioning of commercial hedgers and speculators as a contrarian indicator.

## Trading Rules

**Universe**: S&P 500 + Commodities (various futures)
**Signal**: COT positioning ratios
**Selection**: Binary timing (long or flat)
**Weighting**: Risk parity or equal weight
**Rebalancing**: Weekly

### Signal Components
1. **COT Commercial Net Position**: Net longs of commercial hedgers
2. **COT Speculator Net Position**: Net longs of large speculators
3. **Positioning Ratio**: Commercial / (Commercial + Speculator)

### Trading Logic
- Extreme commercial long positioning → bullish signal
- Extreme speculator long positioning → bearish signal (contrarian)
- Apply across both equity and commodity markets

## Fundamental Reason

1. **Commercial Smart Money**: Hedgers have informational advantage
2. **Speculator Contrarian**: Speculators often wrong at extremes
3. **Multi-Asset Application**: Same logic applies across asset classes
4. **Weekly Signal**: Less noise than daily data

## Performance (Source)

| Metric | Value |
|--------|-------|
| Period | 2000-2006 |
| Return | 16.8% p.a. |
| Volatility | 10.3% |
| Sharpe Ratio | 1.24 |
| Max Drawdown | -27.36% |

**Notes**: Premium strategy - full details require Quantpedia Premium access.

## Eligibility Check

### Required Capabilities
1. **COT Report Data**: CFTC positioning data for multiple futures
2. **S&P 500 Data**: Available
3. **Commodity Data**: Available (288 futures contracts)

### Available
- SPY and commodity futures price data
- Various commodity ETFs and futures

### MISSING - Why INELIGIBLE

**Same as #0029**: COT (Commitment of Traders) Report Data
- Commercial hedger net positioning
- Non-commercial (speculator) net positioning
- Open interest by trader category
- Weekly CFTC reports

Blocked by: ENG-116 (CFTC COT Data feature request)

## Implementation Notes

### If COT Data Becomes Available
1. **COT Signal per Asset**:
   ```
   cot_ratio = commercial_net / (commercial_net + abs(speculator_net))
   cot_z = z_score(cot_ratio, window=52)  # 1-year z-score
   ```

2. **Trading Signal**:
   ```
   bullish = cot_z > 1.5  # Commercials extremely long
   bearish = cot_z < -1.5  # Speculators extremely long
   ```

3. **Apply to Multiple Assets**:
   - S&P 500: ES futures COT data
   - Gold: GC futures COT data
   - Oil: CL futures COT data
   - etc.

## Related Strategies

- #0029 Market Timing S&P 500 with VIX and COT Report (same blocker)
- Sentiment-based market timing strategies

## Notes

This is a Premium Quantpedia strategy. Requires COT data which is not currently available. Feature request filed under ENG-116.
