# Meta-Analysis Summary: FX Response to Macro News

**Source:** Bortnikova, Bajzik, Kocenda (2025) - IES Working Papers 1/2025

---

## Dataset Overview

- **807 estimates** from **25 studies** (1998-2023)
- Studies identified via Google Scholar using keywords: "forex", "event study", "trade news", "monetary policy", etc.
- All estimates recalculated to: % change in exchange rate per 1 std dev positive policy surprise

---

## Main Findings

### 1. Effect Size

| Metric | Value |
|--------|-------|
| Mean effect (unweighted) | -0.2% |
| Effect after bias correction | ~0% (negligible) |
| Publication bias coefficient | 0.266*** (FE model) |

**Key insight:** The true effect of macro announcements on FX is approximately zero after accounting for publication bias.

### 2. Event Window Analysis

| Window | N | Mean | Interpretation |
|--------|---|------|----------------|
| Immediate | 235 | -0.068% | Very small immediate response |
| Narrow (5-30 min) | 320 | -0.480% | Largest intraday effect |
| Hourly | 202 | -0.025% | Effect dissipates |
| Daily | 51 | +0.117% | Slight reversal at daily level |

**Implication for EUR/USD NFP study:** Focus on the narrow window (5-30 min) for maximum signal, but expect small absolute effects.

### 3. Announcement Type Does NOT Matter

From Table 2:
- Real economy announcements: mean = 0.099
- Price announcements: mean = -0.067
- Business climate announcements: mean = -0.106
- Monetary policy announcements: mean = -0.537

Despite monetary policy showing larger effect, the meta-analysis concludes that "the type of macroeconomic announcement does not systematically affect the variation in estimated effects."

**Implication:** NFP is not special - it's the surprise component that matters, not the announcement type.

### 4. What Actually Drives Heterogeneity

Variables with **highest posterior inclusion probability** (from Bayesian Model Averaging):

1. **Interest rate differential** - high differential amplifies response
2. **Inflation regime** - high inflation = larger effects
3. **Business cycle** - recession = larger effects (-0.284 mean)
4. **Data frequency** - intraday data shows different patterns than daily

### 5. Currency Pair Effects

| Base Currency | N | Mean Effect |
|---------------|---|-------------|
| USD | 352 | -0.158% |
| Euro | 130 | -0.963% |
| Japanese Yen | 150 | +0.166% |

**EUR shows larger negative response** to positive surprises compared to USD.

---

## Methodological Notes

### Surprise Calculation (Equation 1)

```
S_it = (A_it - E_{t-1}[A_it]) / σ_i
```

Where:
- A_it = actual announcement value
- E_{t-1}[A_it] = market consensus (median forecast)
- σ_i = sample standard deviation of announcement i

### Standard Event Study Model (Equation 2)

```
Δ(e_i) = β_0 + β_1 * PS_t + ε_i
```

Where:
- Δ(e_i) = % change in exchange rate in event window
- PS_t = policy/news surprise

---

## Implications for EUR/USD NFP Study

1. **Expect small effects** - literature shows ~0% after bias correction
2. **Focus on volatility** rather than directional moves
3. **Narrow window (5-30 min)** shows largest signal
4. **Daily timeframe** shows potential reversal
5. **Surprise magnitude** (vs consensus) is more important than the absolute NFP number
6. **Economic context matters** - check interest rate differential and inflation regime

---

## Key Studies to Reference

From Table 1 (most cited):
- Kearns & Manners (2006) - 137 citations
- Fatum & Scholnick (2008) - 58 citations
- Anderson et al. (2003) - significant reactions to employment and trade balance
- Ehrmann & Fratzscher (2005) - US news more significant than European news

---

## Data Sources for NFP Study

- NFP consensus forecasts: Bloomberg, Reuters
- Actual NFP data: Bureau of Labor Statistics
- EUR/USD tick data: needed for event windows <1 hour
- Release time: 8:30 AM ET (first Friday of month)
