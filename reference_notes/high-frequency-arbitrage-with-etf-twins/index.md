# High-Frequency Arbitrage with ETF Twins

**Quantpedia ID**: #0040
**URL**: https://quantpedia.com/strategies/high-frequency-arbitrage-with-etf-twins
**Status**: INELIGIBLE
**Linear Issue**: [ENG-176](https://linear.app/epoch-inc/issue/ENG-176)

## Overview

High-frequency pairs trading between similar ETFs (e.g., SPY/IVV, QQQ/QQQM). Exploits short-term mispricings between nearly identical ETFs.

## Trading Rules

**Universe**: ETF pairs tracking same index
**Signal**: Spread deviation from fair value
**Rebalancing**: Intraday (milliseconds)

## Performance

| Metric | Value |
|--------|-------|
| Period | 2004-2010 |
| Return | 28.91% p.a. |
| Volatility | 14.69% |
| Sharpe Ratio | 1.7 |

## Why INELIGIBLE

Requires:
1. **Intraday/millisecond data**: Not available (daily only)
2. **HFT infrastructure**: Co-location, low latency
3. **Real-time quotes**: Not available

This is a true HFT strategy that cannot be implemented on daily data.
