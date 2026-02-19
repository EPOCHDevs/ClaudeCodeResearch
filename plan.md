# Donchian-Chandelier Breakout Strategy — Implementation Plan

## Strategy Summary

Trend-following breakout strategy combining 20-day Donchian Channel entries with Chandelier trailing stops and volatility-adjusted position sizing across three futures markets.

## Assets

| Asset | ID | Description |
|-------|-----|-------------|
| Gold | `GC-Futures` | Gold futures (COMEX) |
| Nasdaq | `NQ-Futures` | Nasdaq 100 E-Mini (GBLX) |
| Micro Bitcoin | `BA-Futures` | Bitcoin Micro (GBLX) |

## Rules (from user spec)

### Entry
- **Close > Prior 20-day Donchian Upper Band** → Buy Long
- Lag band by 1 bar (`>> 1`) to avoid look-ahead bias

### Position Sizing (Volatility Targeting)
- Risk 2% of equity per trade
- Stop Distance = 3 × ATR(5)
- Size = (Account × 0.02) / (Stop Distance × contract_multiplier)
- `lot_size=1` for whole contracts

### Exits (Two-Stage)
- **Exit A — Protective Stop (Shield):** `trailing_stop()` at 3 × ATR(5) from highest high since entry. Activates immediately, can trigger intrabar.
- **Exit B — Technical Signal:** Close < Prior 20-day Donchian Lower Band. Confirms trend is over.
- Whichever fires first closes the position.

## EpochScript Structure

```
1. Data source (1D timeframe)
2. Donchian Channel (window=20), lag by 1 bar
3. ATR (period=5), stop_distance = 3 × ATR
4. Entry signal: close > upper_band_prior
5. Exit signal: close < lower_band_prior
6. hold_until(enter=entry, exit=exit_donchian)
7. long_and_short_zone(long_entry=held)
8. risk_unit(risk_pct=2, stop_distance=stop_dist, lot_size=1)
9. trailing_stop(distance=stop_dist)
10. Event markers for entries and exits
```

## Template

Based on existing working definition `24f1f265-...json` (Donchian Breakout with Volatility-Adjusted Sizing), adapted for futures assets with whole-contract lot sizing.

## Execution

1. Write definition JSON to `project/definitions/test_runner/`
2. Run via `/run-job-data` with `--cash 100000`
3. Validate via `/study-reports`
