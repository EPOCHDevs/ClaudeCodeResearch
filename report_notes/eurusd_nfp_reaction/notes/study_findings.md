# EUR/USD NFP Study Findings

**Study:** `eurusd_nfp_reaction_research`
**Period:** 2020-01-01 to 2024-12-31
**Data:** ^EURUSD-FX 5-minute bars (369,002 observations)

---

## Key Results

### 1. NFP Friday vs Other Fridays (8:30-8:35 AM ET Window)

| Metric | NFP Friday (n=57) | Other Friday (n=198) |
|--------|-------------------|---------------------|
| Avg Immediate Range | **5.32 bps** | 5.75 bps |
| Std Immediate Range | 2.34 bps | 2.38 bps |
| Avg Narrow Range | **11.04 bps** | 11.55 bps |
| Avg Immediate Return | **+0.065 bps** | -0.078 bps |
| Max Immediate Range | 13.79 bps | 14.07 bps |

**Surprising finding:** NFP Fridays show **LOWER** average volatility than other Fridays in the 8:30-8:35 window.

### 2. Year-by-Year Volatility (Immediate Window Range in bps)

| Year | NFP Friday | Other Friday | NFP Higher? |
|------|------------|--------------|-------------|
| 2020 | 5.65 | 4.93 | **Yes** (COVID) |
| 2021 | 4.51 | 4.95 | No |
| 2022 | 6.58 | 8.06 | No |
| 2023 | 5.38 | 5.98 | No |
| 2024 | 4.56 | 4.80 | No |

Only 2020 (COVID year) showed higher NFP volatility.

### 3. Day of Week Analysis (All Days)

| Day | Avg Immediate Return | Avg Narrow Return | Avg Immediate Range |
|-----|---------------------|-------------------|---------------------|
| Monday | +0.0009% | +0.007% | 5.65 bps |
| Tuesday | -0.0025% | -0.002% | 5.62 bps |
| Wednesday | +0.0009% | +0.0008% | 5.56 bps |
| Thursday | +0.0006% | -0.003% | 5.86 bps |
| Friday | -0.0005% | +0.007% | 5.66 bps |

Friday shows the **largest narrow window return (+0.007%)** - potentially from NFP effect.

---

## Interpretation

### Consistent with Meta-Analysis (Bortnikova 2025)

1. **Near-zero mean return**: Average returns are negligible (< 0.01%)
2. **No systematic announcement type effect**: NFP doesn't produce significantly different patterns
3. **Narrow window shows largest signal**: 8:35-9:00 AM ET shows most activity
4. **Publication bias concern**: Reported effects in literature likely overstated

### Why NFP Volatility May Be Lower Than Expected

1. **Market anticipation**: Traders position before release, reducing surprise impact
2. **High EUR/USD liquidity**: Major pair absorbs shocks efficiently
3. **24-hour FX market**: No gap risk like equity markets
4. **Spread widening vs price volatility**: Liquidity providers may widen spreads without actual price moves
5. **Algorithmic trading**: Fast price discovery reduces range

---

## Comparison to Literature

| Study | Finding | This Study |
|-------|---------|-----------|
| Bortnikova (2025) | Narrow window: -0.48% | Narrow: +0.007% (Friday) |
| Bortnikova (2025) | Hourly: slight reversal | Hourly: -0.007% (reversal) |
| Rezania (2010) | EUR/USD -0.3% per surprise | Cannot measure (no consensus data) |
| Rezania (2010) | Vol decay α ≈ 0.05 | Need further analysis |

---

## Limitations

1. **No consensus data**: Cannot calculate surprise direction/magnitude
2. **Approximate NFP detection**: Using "first Friday with day ≤ 7"
3. **2020 COVID impact**: Unusual volatility patterns
4. **5-minute resolution**: May miss sub-minute spikes

---

## Volatility Decay Analysis (Rezania Table 7 Replication)

**Study:** `eurusd_nfp_volatility_decay`
**Methodology:** Session windows capturing high-low range (bps) in 5-min intervals after 8:30 AM ET

### Time Window Results (Median Values)

| Window | Minutes After 8:30 | NFP Friday | Other Friday | Ratio |
|--------|-------------------|------------|--------------|-------|
| range0 | 0-5 min | 4.77 bps | 5.17 bps | 0.92 |
| range1 | 5-10 min | 5.01 bps | 5.53 bps | 0.91 |
| range2 | 10-15 min | 4.98 bps | 5.38 bps | 0.92 |
| range3 | 15-20 min | 4.91 bps | 5.06 bps | 0.97 |
| range4 | 20-25 min | 4.42 bps | 4.81 bps | 0.92 |
| range5 | 25-30 min | 4.92 bps | 4.72 bps | 1.04 |

### Comparison to Rezania (2010)

| Metric | Rezania (2002-2005) | This Study (2020-2024) |
|--------|---------------------|------------------------|
| Peak volatility increase | 847% | **-8%** (lower than baseline) |
| Decay rate α | 0.049 | Not observable |
| Half-life | 14.1 minutes | N/A |

### Why the Discrepancy?

1. **Data resolution**: Rezania used tick-level data with wavelet estimators; we use 5-min OHLC
2. **Market evolution**: 20 years of algorithmic trading and faster price discovery
3. **Range measure**: High-low range may miss sub-minute volatility spikes
4. **Pre-positioning**: Modern markets may incorporate NFP expectations before release

### Notable Observations

- March 2020 NFP: 13.79 bps range (highest in dataset) - methodology captures extremes correctly
- No clear exponential decay pattern visible in 5-min data
- NFP/baseline ratio consistently ~0.92 across most windows

---

## Next Steps

1. Add external NFP consensus data for surprise calculation
2. Analyze specific high-impact NFP releases (e.g., March 2020)
3. Compare EUR/USD to other pairs (USD/JPY, GBP/USD)
4. Try 1-minute data for finer granularity
5. Compute return-based volatility (std dev) instead of range
