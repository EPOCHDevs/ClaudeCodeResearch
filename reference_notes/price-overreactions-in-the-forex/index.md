# Price Overreactions in the Forex

**Quantpedia ID**: #0435
**URL**: https://quantpedia.com/strategies/price-overreactions-in-the-forex
**Status**: INELIGIBLE
**Linear Issue**: [ENG-278](https://linear.app/epoch-inc/issue/ENG-278/feature-request-intraday-fx-data-for-0435)

## Overview
This strategy exploits intraday momentum following price overreactions in forex markets. When a currency pair's return exceeds average + 2 standard deviations, prices tend to continue moving in that direction for the remainder of the day. The strategy opens positions at 17:00 when overreaction is detected.

## Trading Rules
**Universe**: AUD/USD (paper also covers EURUSD, USDJPY, USDCAD, EURJPY)

**Signal**: Intraday overreaction detection
1. Calculate daily return at 17:00 (price / open - 1)
2. Calculate 50-day rolling average and standard deviation
3. Overreaction = return > (avg + 2 * std)
4. Open position at 17:00 in direction of overreaction
5. Close position at end of day

**Selection**:
- Long on positive overreaction
- Short on negative overreaction

**Weighting**: Single position
**Rebalancing**: Intraday (at 17:00)

## Fundamental Reason
- Price overreactions driven by behavioral biases
- Intraday momentum effect on overreaction days
- Prices tend to continue in overreaction direction until end of day
- Effect becomes clear at start of US trading session
- Evidence against market efficiency

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2008-2018 |
| Return | 4.78% p.a. |
| Volatility | 6.3% |
| Max Drawdown | -41.99% |
| Sharpe Ratio | 0.76 |

Note: Data from Table 4, AUDUSD, Strategy 1.

**WARNING**: OOS (2009-2025) shows -0.9% return, -0.11 Sharpe, -40.8% max DD. Strategy appears data-mined.

## Source Paper
Caporale, Guglielmo Maria and Plastun, Oleksiy: Price Overreactions in the Forex and Trading Strategies
- SSRN: https://ssrn.com/abstract=3362142

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/27238645/

## Eligibility Check
### Available
- **Transforms**:
  - `roc` - Return calculation
  - `sma` - Average return
  - `std` - Standard deviation
- **Assets** (FX pairs available):
  - ^AUDUSD-FX ✓
  - ^EURUSD-FX ✓
  - ^USDJPY-FX ✓

### Missing
- **Intraday Data** - NOT AVAILABLE
  - Strategy requires hourly bars
  - Specific timing: 17:00 entry, end-of-day exit
  - Current focus is primarily on daily data
- **Intraday Execution** - NOT AVAILABLE
  - Time-specific order execution needed

## Implementation Notes
- Strategy is marked INELIGIBLE due to:
  1. Missing intraday data (hourly bars required)
  2. Intraday execution timing (17:00 entry)
- Confidence rating: Weak (data-mined)
- Complexity: Simple
- All FX pairs are available for daily data
- **WARNING**: Negative OOS performance (-0.11 Sharpe) suggests in-sample overfitting
- Not recommended for implementation even if intraday data available

