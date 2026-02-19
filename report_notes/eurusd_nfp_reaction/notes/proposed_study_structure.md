# EUR/USD Post-NFP Study Structure

**Based on:** Bortnikova (2025), Rezania (2010), FXStreet Guide

---

## 1. Data Requirements

### Price Data
| Asset | Timeframe | Source | Period |
|-------|-----------|--------|--------|
| EUR/USD | 1-minute | Polygon/Barchart | 2020-2024 |
| EUR/USD | 5-minute | Polygon/Barchart | 2020-2024 |

### Event Data
| Field | Source | Description |
|-------|--------|-------------|
| NFP Actual | BLS | Actual NFP change (thousands) |
| NFP Consensus | Bloomberg/Reuters | Median forecast |
| NFP Previous | BLS | Prior month (revised) |
| Release Time | BLS | 8:30 AM ET |

### Derived Fields
```
Surprise = Actual - Consensus
Standardized_Surprise = Surprise / StdDev(Historical_Surprises)
Deviation_Pct = (Actual - Consensus) / Consensus * 100
```

---

## 2. Time Windows

Based on Bortnikova (2025) event window analysis and Rezania (2010) 6-hour framework:

| Window | Start | End | Purpose |
|--------|-------|-----|---------|
| **Pre-Release** | T-30min | T | Baseline volatility, positioning |
| **Immediate** | T | T+5min | Initial spike, knee-jerk reaction |
| **Narrow** | T+5min | T+30min | Price discovery, largest signal |
| **Hourly** | T+30min | T+60min | Consolidation/continuation |
| **Extended** | T+60min | T+4h | Full session impact |

**T = 8:30 AM ET (release time)**

---

## 3. Metrics to Calculate

### A. Return Metrics (per window)
```
Return = (Close_end - Close_start) / Close_start * 100
Cumulative_Return = (Close_end - Close_T) / Close_T * 100
```

### B. Volatility Metrics
From Rezania (2010) - Range-based better than close-to-close:

```
True_Range = High - Low  (in pips)
Realized_Vol = StdDev(1-min returns) * sqrt(N)
Volatility_Ratio = Vol_window / Vol_pre_release
```

### C. Directional Metrics
```
Direction = Sign(Return)
Consistency = Direction matches Sign(Surprise) ? 1 : 0
Reversal = Sign(Return_immediate) != Sign(Return_hourly) ? 1 : 0
```

### D. Decay Analysis
From Rezania (2010) volatility decay model:
```
Vol(t) = Vol_0 * exp(-α * t)
```
Estimate decay rate α per release.

---

## 4. Analysis Framework

### Phase 1: Descriptive Statistics

| Metric | Calculation |
|--------|-------------|
| Mean Return per Window | By surprise direction (+/-) |
| Median True Range | By window |
| Win Rate | % times direction matches surprise |
| Reversal Rate | % times hourly reverses immediate |

### Phase 2: Conditional Analysis

Group by:
1. **Surprise Magnitude**: Small (<50K), Medium (50-100K), Large (>100K)
2. **Surprise Direction**: Positive (bullish USD), Negative (bearish USD)
3. **Market Regime**: VIX high/low, Fed policy stance

### Phase 3: Baseline Comparison

Compare NFP Fridays vs:
- Non-NFP Fridays (same time window)
- Random days (matched by volatility)

Metrics:
```
Excess_Return = Return_NFP - Return_baseline
Excess_Volatility = Vol_NFP / Vol_baseline
```

---

## 5. Chart Specifications

### Chart 1: Deviation History
- X: NFP release date
- Y: Actual - Consensus (thousands)
- Color: Green (positive), Red (negative)
- Reference: FXStreet guide deviation charts

### Chart 2: True Range by Window
- Bar chart: 15min, 30min, 60min, 4h ranges
- Grouped by surprise magnitude
- Shows volatility decay visually

### Chart 3: Return Distribution
- Histogram of returns per window
- Overlay: Normal distribution
- Separate panels for +/- surprise

### Chart 4: Cumulative Return Path
- Average cumulative return from T to T+60min
- Separate lines for: Large+, Small+, Small-, Large-
- Confidence bands (25th-75th percentile)

### Chart 5: Volatility Decay Curve
- X: Minutes post-release
- Y: Realized volatility (normalized)
- Fitted exponential decay curve

### Chart 6: Win Rate by Surprise Size
- X: Surprise magnitude buckets
- Y: % times direction matched surprise
- Separate bars per time window

---

## 6. Expected Findings

Based on literature:

| Finding | Source | Expected Result |
|---------|--------|-----------------|
| Mean return | Bortnikova | ~0% after bias correction |
| Narrow window effect | Bortnikova | -0.48% (largest) |
| Hourly reversal | Bortnikova | +0.12% (slight reversal) |
| EUR/USD response | Rezania | -0.3% per surprise unit |
| Volatility decay | Rezania | α ≈ 0.05 (EUR) |
| Directional accuracy | FXStreet | 60-70% when |surprise| large |

---

## 7. Implementation Steps

### Step 1: Data Preparation
- [ ] Load EUR/USD 1-min and 5-min data
- [ ] Build NFP calendar with consensus/actual
- [ ] Align timestamps to release times
- [ ] Filter trading hours only

### Step 2: Event Windows
- [ ] Define window boundaries around each NFP
- [ ] Calculate returns and ranges per window
- [ ] Handle missing data (holidays, early closes)

### Step 3: Analysis
- [ ] Compute descriptive statistics
- [ ] Group by surprise magnitude/direction
- [ ] Build baseline comparison (non-NFP Fridays)
- [ ] Fit volatility decay model

### Step 4: Visualization
- [ ] Generate charts 1-6
- [ ] Create summary tearsheet
- [ ] Export to charts/ folder

---

## 8. EpochScript Approach

For implementation via generate_job_data:

```
# Pseudo-structure for research study

Assets: EUR/USD (or proxy via EUR futures)
Timeframe: 1Min, 5Min

Transforms:
- NFP surprise (external calendar)
- Window flags (pre, immediate, narrow, hourly)
- True range
- Cumulative return from release

Event Markers:
- NFP release timestamp
- Window boundaries

Output:
- market_data with computed columns
- event_markers for analysis
```

---

## 9. Risk Considerations

From meta-analysis warnings:

1. **Publication bias**: True effects likely smaller than reported
2. **Survivorship**: Only successful trades get documented
3. **Regime change**: 2020+ may differ from historical
4. **Liquidity**: Spreads widen at release, execution differs

---

## 10. Success Criteria

| Criterion | Target |
|-----------|--------|
| Data coverage | 48+ NFP releases (4 years) |
| Window accuracy | Timestamps aligned to second |
| Baseline comparison | Statistically significant difference |
| Chart clarity | All 6 charts generated |

---

## References

1. Bortnikova et al. (2025) - Meta-analysis of 807 estimates
2. Rezania et al. (2010) - Intraday FX volatility analysis
3. FXStreet NFP Guide - Practical trading framework
