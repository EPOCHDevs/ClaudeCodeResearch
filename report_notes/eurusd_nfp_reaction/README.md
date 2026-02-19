# EUR/USD Post-NFP Price Action Research

**Linear Issue:** [ENG-612](https://linear.app/epoch-inc/issue/ENG-612/research-eurusd-post-nfp-price-action)

## Research Question
What happens to EUR/USD in the hour following US Non-Farm Payrolls releases?

## Folder Structure
```
eurusd_nfp_reaction/
├── papers/          # Academic papers and PDFs
├── charts/          # Screenshots, visualizations
├── notes/           # Analysis notes and summaries
└── README.md        # This file
```

---

## Downloaded Papers

### 1. How Do Event Studies Capture Impact of Macroeconomic News in Forex Market? (Meta-Analysis)
- **Authors:** Bortnikova, Bajzik, Kocenda (Charles University)
- **Date:** February 2025
- **Source:** IES Working Papers 1/2025
- **URL:** https://www.econstor.eu/bitstream/10419/315104/1/1918775818.pdf
- **Pages:** 49
- **Key Findings:**
  - Meta-analysis of **807 estimates from 25 studies**
  - Mean effect: **-0.2%** exchange rate change per 1 std dev positive surprise
  - Publication bias detected but effect remains small after correction
  - Interest rate differentials and inflation regimes drive heterogeneity
  - **Announcement type (NFP, CPI, etc.) does NOT systematically affect results**
  - Event windows: immediate (-0.07%), narrow (-0.48%), hourly (-0.03%), daily (+0.12%)
- **Local:** `papers/bortnikova_2025_forex_event_study_meta.pdf` ✓

### 2. Analysis of the Intraday Effects of Economic Releases on the Currency Market (KEY PAPER)
- **Authors:** Rezania, Rachev, Sun, Fabozzi (KIT)
- **Date:** August 2010
- **Source:** KIT Working Paper No. 3
- **URL:** https://econpapers.wiwi.kit.edu/downloads/KITe_WP_3.pdf
- **Pages:** 35
- **Key Findings:**
  - NFP rated "very important" by 100% of economists and traders (Table 2)
  - **NFP causes -0.298% EUR/USD change per 1σ surprise** (t=-6.02, Table 4)
  - Volatility decay rate α=0.049, half-life ~14 min (Table 7)
  - Peak volatility increase: 847% at release (Table 6)
  - Large surprises (>2σ) predict direction 84% of time (Table 8)
  - Wavelet estimator 39x more efficient than range (Table 5)
- **Local:** `papers/rezania_2010_intraday_fx_releases.pdf` ✓
- **Full Extraction:** `notes/rezania_2010_extraction.md` ✓

### 3. NFP Trading with Binary Options & Temporal Functionalities
- **Authors:** Vasiliki A. Basdekidou
- **Date:** 2017
- **Source:** Annales Universitatis Apulensis Series Oeconomica
- **URL:** https://newoeconomica.uab.ro/up/AUASO/articles/nonfarm_employment_report_trading_with_binary_options__temporal_functionalities-article-663b14a09164b.pdf
- **Pages:** 10
- **Key Findings:**
  - Short-term NFP trading strategy
  - Backtested on US markets 2000-2016
  - NFP creates significant market volatility
- **Local:** `papers/basdekidou_2017_nfp_binary_options.pdf` ✓

### 4. Crash Course to Become an NFP Expert (FXStreet Guide)
- **Source:** FXStreet
- **URL:** https://externalcontent.blob.core.windows.net/pdfs/Become_an_NFP_expert_updated.pdf
- **Pages:** 36
- **Key Findings:**
  - Pre-NFP indicators: ADP, Jobless Claims, ISM PMIs
  - Post-NFP analysis: deviation from consensus, revisions, unemployment rate
  - Average hourly earnings impact
- **Local:** `papers/fxstreet_nfp_expert_guide.pdf` ✓

---

## Papers to Download (Paywalled/Unavailable)

### Impact of Surprises in Macroeconomic Announcements on EUR-USD Volatility
- **Author:** Luis Daniel Gala (ITAM)
- **Date:** November 2023
- **Source:** SSRN (requires account)
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4646507

### The High-Frequency Response of Exchange Rates to Macroeconomic Announcements
- **Authors:** Faust, Rogers, Wang, Wright
- **Date:** 2007
- **Source:** Journal of Monetary Economics (paywalled)
- **Citations:** 255

### News Announcements, Market Activity and Volatility in Euro/Dollar
- **Authors:** Bauwens, Ben Omrane, Giot
- **Date:** 2005
- **Source:** Journal of International Money and Finance (paywalled)
- **Citations:** 152

---

## Quantpedia Resources

| Topic | URL | Notes |
|-------|-----|-------|
| FX Anomalies Overview | https://quantpedia.com/strategy-tags/fx-anomaly/ | General FX strategy catalog |
| Currency Momentum | https://quantpedia.com/strategies/currency-momentum-factor | Trend-following in FX |
| Mean Reversion in Currencies | https://quantpedia.com/how-to-build-mean-reversion-strategies-in-currencies/ | Post-spike reversal potential |
| FX Volatility & Time of Day | https://quantpedia.com/the-daily-volatility-of-foreign-exchange-rates-and-the-time-of-day/ | Intraday patterns |

---

## Key Insights from Literature

### From Meta-Analysis (Bortnikova et al. 2025)

1. **Effect Size is Small**
   - Mean effect: **-0.2%** exchange rate change per 1 std dev positive policy surprise
   - After correcting for publication bias, true effect approaches **zero**
   - Studies may overestimate impact due to selective reporting

2. **Event Window Effects (Table 2)**
   | Window Type | N Estimates | Mean Effect | 95% CI |
   |-------------|-------------|-------------|--------|
   | Immediate | 235 | -0.068 | [-1.60, 1.46] |
   | Narrow | 320 | -0.480 | [-3.65, 2.71] |
   | Hourly | 202 | -0.025 | [-1.65, 1.60] |
   | Daily | 51 | +0.117 | [-2.06, 2.30] |

3. **Announcement Type Doesn't Matter**
   - Real economy, inflation, and monetary policy announcements have similar effects
   - NFP is not systematically different from other macro releases
   - **Surprise magnitude** matters more than announcement type

4. **Economic Conditions Drive Heterogeneity**
   - Interest rate differentials significantly affect response
   - Inflation regime (high vs low) matters
   - Business cycle phase (recession vs recovery) affects magnitude

5. **Currency Pair Findings**
   - EUR and JPY more volatile to positive policy surprises than USD
   - US announcements have **less pronounced effects** than EU announcements
   - 43% of estimates use USD as base currency

### Practical Implications

1. **Time Windows**
   - Initial reaction (0-5 min): Sharp directional move
   - Consolidation (5-30 min): Often retracement or continuation
   - Post-reaction (30-60 min): Potential mean reversion
   - **Daily timeframe shows slight reversal** (+0.12% vs negative intraday)

2. **Volatility Clustering**
   - Elevated volatility persists beyond the release window
   - Important for position sizing and risk management

3. **Publication Bias Warning**
   - Academic studies may overstate effects by 2x
   - Real trading conditions likely show smaller moves

---

## NFP Release Schedule

- **When:** First Friday of each month
- **Time:** 8:30 AM ET (13:30 UTC in winter, 12:30 UTC in summer)
- **Data Source:** US Bureau of Labor Statistics

### NFP Dates (2023-2024)
```
2023: Jan 6, Feb 3, Mar 10, Apr 7, May 5, Jun 2, Jul 7, Aug 4, Sep 1, Oct 6, Nov 3, Dec 8
2024: Jan 5, Feb 2, Mar 8, Apr 5, May 3, Jun 7, Jul 5, Aug 2, Sep 6, Oct 4, Nov 1, Dec 6
```

---

## Next Steps

1. [x] Download PDFs of key papers (4 papers downloaded)
2. [x] Extract key insights from papers (see `notes/meta_analysis_summary.md`)
3. [x] Design study structure (see `notes/proposed_study_structure.md`)
4. [x] Build EUR/USD study with NFP event markers - `eurusd_nfp_reaction_research`
5. [x] Analyze price windows: 8:30-8:35, 8:35-9:00, 9:00-9:30 AM ET
6. [x] Compare to baseline (non-NFP Fridays) - see `notes/study_findings.md`
7. [ ] Add external NFP consensus data for surprise calculation
8. [ ] Analyze specific high-impact releases (March 2020)
9. [ ] Compare to other pairs (USD/JPY, GBP/USD)

---

## Study Results Summary

**Key Finding:** Contrary to expectations, NFP Fridays show **LOWER** average volatility than other Fridays in the 8:30-8:35 AM ET window (5.32 bps vs 5.75 bps).

| Metric | NFP Friday (n=57) | Other Friday (n=198) |
|--------|-------------------|---------------------|
| Avg Immediate Range | 5.32 bps | 5.75 bps |
| Avg Immediate Return | +0.065 bps | -0.078 bps |

**Consistent with Bortnikova (2025):** Near-zero mean returns, announcement type doesn't systematically matter.

See full analysis: `notes/study_findings.md`
