# Overnight Momentum Strategy

**Quantpedia ID**: #0300
**URL**: https://quantpedia.com/strategies/overnight-momentum-strategy
**Status**: ELIGIBLE
**Linear Issue**: [ENG-48](https://linear.app/epoch-inc/issue/ENG-48/implement-overnight-momentum-strategy-0300)

## Overview
This strategy exploits the difference between overnight and intraday stock returns. Research shows that momentum profits accrue entirely overnight while other trading strategies profit primarily intraday. The strategy sorts stocks by their one-month overnight returns and goes long winners/short losers, holding positions only during the overnight session (from market close to market open).

## Trading Rules
**Universe**: NYSE, AMEX, NASDAQ stocks with price > $5, sorted by dollar volume (top 100)
**Signal**: One-month accumulated overnight returns (close-to-open)
**Selection**: Sort into deciles by overnight returns; long top decile, short bottom decile
**Weighting**: Market-cap weighted
**Rebalancing**: Monthly stock selection, daily position entry/exit

## Fundamental Reason
Momentum effect in stocks arises from investors' underreaction to news. Overnight momentum is stronger because institutional investors mostly trade intraday and, on average, trade against momentum. Individual investors trade more overnight when institutions are absent.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1993-2013 |
| Return | 50.58% p.a. |
| Volatility | 11.24% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 4.04 |

**WARNING**: OOS backtest shows significantly negative performance. In-sample results appear data-mined.

## Source Paper
Lou, Polk and Skouras: A Tug of War: Overnight Versus Intraday Expected Returns
- http://personal.lse.ac.uk/loud/ATugofWar.pdf
- http://personal.lse.ac.uk/polk/research/OvernightMom20160115.pdf

## QuantConnect Reference Code
```python
# See Quantpedia page for full implementation
# Key elements:
# - Universe: 100 most liquid US stocks with price > $5
# - Calculate overnight returns: (open / prev_close) - 1
# - Monthly ranking by accumulated overnight returns
# - Market-on-close orders to enter, market-on-open to exit
# - Value-weighted portfolios
```

## Eligibility Check
### Available Transforms
- `session_gap` - Detects overnight gaps, provides gap_size and prior session close
- `session_window` - Computes OHLCV for custom sessions (can get open prices)
- `cs_rank` - Cross-sectional ranking for sorting stocks into deciles
- `cs_momentum` - Cross-sectional momentum scoring
- `roc` - Rate of change for returns calculation

### Available Assets
- 13,000+ US stocks including NYSE (2,935), NASDAQ (4,866), AMEX
- Minute-level data available (minute_start/minute_end fields in assets)

### Technical Eligibility: ELIGIBLE
All required capabilities are available in Epoch:

1. **Overnight Returns**: `session_gap.gap_size` or calculate via `(open/lag(close,1))-1`
2. **Cross-Sectional Ranking**: `cs_rank` transform for decile sorting
3. **Stock Universe**: 13,000+ US stocks with NYSE/NASDAQ/AMEX coverage
4. **Minute Data**: Available for all stocks (minute_start/minute_end fields)
5. **Session Timing**: `session_window` for precise market open/close

**Note**: Quantpedia rates confidence as "Weak" with negative OOS performance, but technical implementation is feasible.

## Implementation Notes
If future research validates this effect or a simplified version is desired, the following transforms could be used:
- Use `session_gap.gap_size` or calculate `(open/lag(close,1))-1` for overnight returns
- Use `cs_rank` to sort stocks by accumulated overnight momentum
- Use `session_window` for precise session timing
