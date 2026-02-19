# Overnight-Intraday Daily Reversal in Commodities

**Quantpedia ID**: #0301
**URL**: https://quantpedia.com/strategies/overnight-intraday-daily-reversal-in-commodities
**Status**: ELIGIBLE
**Linear Issue**: [ENG-XX](pending)

## Overview
Short-term reversal strategy that exploits the difference between overnight (close-to-open) and intraday (open-to-close) returns in commodity futures. The strategy buys past overnight losers and sells past overnight winners, then holds positions during the intraday session. The CO-OC (close-to-open formation, open-to-close trading) reversal significantly outperforms traditional CC-CC reversal strategies.

## Trading Rules
**Universe**: 11 commodity futures (Corn, Ethanol CBOT, Lean Hogs, Live Cattle, Lumber, Oats, Pork Bellies, Rough Rice, Soybean Meal, Soybeans, Wheat CBOT)
**Signal**: Past overnight returns (close-to-open)
**Selection**: Zero-investment portfolio - long past overnight losers, short past overnight winners
**Weighting**: Weighted by overnight return magnitude (formulas 1 and 4 from paper)
**Rebalancing**: Daily (intraday trading period)

## Fundamental Reason
Reversal occurs due to investors' overreaction to asset-related news and subsequent price correction. Periodic market closures (overnight and weekends) are characterized by low trading activity and liquidity. The overnight increment of uncertainty (as measured by VIX) plays an important role in explaining CO-OC reversal profits. Hedging demands seem to induce CO-OC reversals consistent with the Hong and Wang (2000) model.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2007-2014 |
| Return | 45.75% p.a. |
| Volatility | 31.02% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 1.47 |

**WARNING**: OOS backtest shows significantly negative performance. In-sample results may be data-mined.

## Source Paper
Corte, Kosowski, Wang: Market Closure and Short-Term Reversal
- http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2730304
- https://quantpedia.com/www/Market_Closure_and_Short_Term_Reversal.pdf

## QuantConnect Reference Code
```python
# See Quantpedia page for full implementation
# Key elements:
# - Universe: 11 commodity futures from TickData database
# - Calculate overnight returns: (open / prev_close) - 1
# - Weight by overnight return magnitude (formulas 1 & 4)
# - Enter at open, exit at close (intraday trading)
# - Zero-investment portfolio (long losers, short winners)
```

## Eligibility Check
### Available Transforms
- `session_gap` - Detects overnight gaps, provides gap_size and prior session close
- `session_window` - Computes OHLCV for custom sessions (can get open prices)
- `cs_rank` - Cross-sectional ranking for sorting futures
- `roc` - Rate of change for returns calculation

### Available Assets
- 290 Futures available in Epoch including commodity futures
- Minute-level data available

### Technical Eligibility: ELIGIBLE
All required capabilities are available in Epoch:

1. **Overnight Returns**: `session_gap.gap_size` or calculate via `(open/lag(close,1))-1`
2. **Cross-Sectional Ranking**: `cs_rank` transform for weighting
3. **Commodity Futures**: Available in Epoch (290 futures)
4. **Intraday Data**: Minute data available for precise session timing
5. **Session Timing**: `session_window` for market open/close

## Implementation Notes
- Use `session_gap.gap_size` for overnight return calculation
- Use `cs_rank` to weight by overnight return magnitude
- Use `session_window` for precise intraday entry/exit timing
- Consider reducing position sizes given high volatility (31%)
