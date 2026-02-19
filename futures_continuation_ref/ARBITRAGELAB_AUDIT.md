# Arbitragelab vs EpochBackend: Full Audit

## Executive Summary

**arbitragelab**: 14 modules, 143+ classes, ~50K LOC (Python) - Statistical arbitrage research library
**EpochBackend**: 304 transforms across 16 categories (C++) - Production trading platform

---

## Part 1: Existing Overlaps (Cross-Validated)

### 1.1 Engle-Granger Cointegration

| Aspect | arbitragelab | EpochBackend | Verdict |
|--------|-------------|-------------|---------|
| **OLS Step** | No intercept by default | Always includes intercept | **Epoch better** (more robust) |
| **ADF Critical Values** | Standard ADF (statsmodels) | MacKinnon 2010 cointegration-specific | **Epoch better** (correct for residual ADF) |
| **ADF Regression** | Delegates to statsmodels (constant included) | Manual impl, **missing constant** | **BUG in Epoch** - needs fix |
| **Rolling** | Static only | Rolling window | **Epoch better** |
| **Outputs** | hedge_ratio, residuals, ADF stats | hedge_ratio, intercept, spread, ADF + p-value + is_cointegrated | **Epoch better** (decision-ready) |

**Action**: ~~Fix ADF regression to include constant term~~ **FIXED** — Replaced manual OLS with `adf::compute_adf("c")` from `adf_core.h`, which includes constant + uses Armadillo pinv. All 23 cointegration tests pass (342 assertions).

### 1.2 Johansen Cointegration

| Aspect | arbitragelab | EpochBackend | Verdict |
|--------|-------------|-------------|---------|
| **VECM Math** | Identical | Identical | **Match** |
| **Eigendecomp** | statsmodels (LAPACK) | Armadillo eig_gen + clamping [0,1) | **Epoch more stable** |
| **Critical Values** | Dynamic (statsmodels) | Hard-coded Osterwald-Lenum tables (3 cases) | Both valid |
| **Cointegrating Vectors** | All vectors stored | First (strongest) only | Different use cases |
| **Rolling** | Static only | Rolling window | **Epoch better** |
| **Variables** | 1-12+ | 2-10 | Sufficient |

**Action**: None required. Both correct, Epoch has production advantages.

### 1.3 Kalman Filter

| Aspect | arbitragelab | EpochBackend | Verdict |
|--------|-------------|-------------|---------|
| **Algorithm** | Simplified (combined predict/update) | **Standard Kalman** (separate predict/update) | **Epoch correct** |
| **State-Space** | Fixed 2D (hedge ratio + intercept) | Configurable (1D/2D/custom) | **Epoch more flexible** |
| **Cov Update** | P - K*F*R (simplified) | **Joseph form**: (I-K*H)*P*(I-K*H)' + K*R*K' | **Epoch more stable** |
| **Matrix Naming** | Non-standard (F for obs, R for pred) | Standard (F=trans, H=obs, Q=proc, R=meas) | **Epoch correct** |
| **Log-Likelihood** | None | Computed for model comparison | **Epoch better** |
| **Pairs Trading** | Native support | Custom model only | arbitragelab more convenient |

**Action**: Consider adding a `kalman_regression` model type for pairs trading.

### 1.4 Half-Life of Mean Reversion

| Aspect | arbitragelab | EpochBackend | Verdict |
|--------|-------------|-------------|---------|
| **Model** | Velocity eq: Ay(t) on y(t-1) | AR(1): y(t) on y(t-1) | Different parameterizations |
| **Formula** | hl = -ln(2) / beta | hl = -ln(2) / ln(phi) | Both correct (equivalent for small dt) |
| **Window** | Expanding (all data) | Rolling (default 60 bars) | **Epoch better** for live trading |
| **MR Check** | None built-in | is_mean_reverting (0 < phi < 1) | **Epoch better** |

**Action**: None. Different but equivalent approaches.

### 1.5 Hurst Exponent

| Aspect | arbitragelab | EpochBackend | Verdict |
|--------|-------------|-------------|---------|
| **Method** | Simplified R/S (tau = sqrt(std)) | **True R/S analysis** (rescaled range) | **Epoch more rigorous** |
| **Output** | slope * 2.0 (non-standard) | slope (standard) | **Epoch correct** |
| **Lag Grid** | Fixed 2 to max_lags | Power-of-2 grid | Epoch more principled |
| **Variants** | One (expanding) | Expanding + Rolling | **Epoch better** |

**Action**: None. Epoch implementation is superior.

### 1.6 Other Overlaps (Matching)

| Transform | arbitragelab | EpochBackend | Match? |
|-----------|-------------|-------------|--------|
| **ADF Test** | statsmodels adfuller | rolling_adf (MacKinnon tables) | Methodology matches, rolling in Epoch |
| **PCA** | PCAStrategy (eigenportfolio) | pca (sklearn-like) | Same concept, different scope |
| **ARIMA** | AutoARIMAForecast | rolling_arima (walk-forward) | Epoch is rolling, arb is static |
| **HMM** | RegimeSwitchingArbitrageRule | hmm (Hidden Markov Model) | Same concept |
| **DBSCAN** | OPTICSDBSCANPairsClustering | dbscan | Same algorithm |
| **K-means** | (via ML module) | kmeans | Same algorithm |
| **Futures Rolling** | BaseFuturesRoller + per-commodity | futures_continuation (3 methods) | **Epoch more flexible** |
| **Z-Score** | BollingerBandsTradingRule | zscore + bbands | Same |
| **Linear Regression** | OLS hedge ratio | linear_fit (rolling OLS) | Same + Epoch is rolling |
| **GARCH** | Not present | rolling_garch | **Epoch only** |
| **Fractional Diff** | Not present | frac_diff | **Epoch only** |

---

## Part 2: Arbitragelab Modules NOT in EpochBackend

### Priority Tier 1: HIGH VALUE - Should Implement

#### 1. Ornstein-Uhlenbeck Optimal Entry/Exit
**Module**: `optimal_mean_reversion/ou_model.py`
**What**: MLE-fitted OU process with closed-form optimal entry/exit levels
**Why**: Replaces ad-hoc z-score thresholds with mathematically optimal boundaries
**Effort**: Medium (offline Python fit + EpochScript entry/exit signals)
**Implementation**: Python warmup script exports JSON params -> EpochScript strategy imports
**Key formulas**:
- Entry: solve F(a, r) = (a - c) * F'(a, r)
- Exit: solve G(b, r) equation
- Half-life: ln(2) / mu

#### 2. Spread Construction Helpers
**Module**: `hedge_ratios/` (6 methods)
**What**: OLS, TLS, Johansen, Box-Tiao, ADF-optimal, min-half-life hedge ratios
**Why**: Better hedge ratio = better spread = better mean reversion signal
**Epoch has**: linear_fit (OLS), johansen (vector)
**Missing**: TLS, Box-Tiao, ADF-optimal, min-half-life
**Effort**: Low-Medium per method

#### 3. Distance-Based Pair Selection
**Module**: `distance_approach/basic_distance_approach.py`
**What**: Gatev et al. (2006) normalized distance method for pair screening
**Why**: Standard pair selection technique, good for universe screening
**Effort**: Low (simple cross-sectional transform)
**EpochScript mapping**: Cross-sectional transform with rolling normalization

### Priority Tier 2: MEDIUM VALUE - Consider Implementing

#### 4. Copula Dependence (Gaussian only)
**Module**: `copula_approach/`
**What**: Bivariate Gaussian copula for pair quality scoring
**Why**: More sophisticated than linear correlation for tail dependence
**NOT worth**: Student-t (too expensive), Archimedean (marginal value)
**Effort**: Medium (~500 LOC for Gaussian + ECDF)
**Use case**: Pair screening metric (SIC/AIC), NOT direct trading signals

#### 5. Codependence Measures
**Module**: `codependence/`
**What**: Angular distance, distance correlation, mutual information, optimal transport
**Why**: Alternative to Pearson correlation for non-linear dependencies
**Epoch has**: rolling_corr, ewm_corr, rolling_cov
**Missing**: Distance correlation, mutual information, angular distance
**Effort**: Low per measure

#### 6. Sparse Mean Reversion Portfolio
**Module**: `cointegration_approach/sparse_mr_portfolio.py`
**What**: Box-Tiao canonical decomp, LASSO, SDP for sparse cointegrating portfolios
**Why**: Find mean-reverting portfolios from large universes
**Effort**: High (requires convex optimization)

#### 7. Minimum Profit Trading Rule
**Module**: `trading/minimum_profit.py`
**What**: AR(1) optimal bounds for mean reversion entry/exit
**Why**: Simpler than full OU model but theoretically grounded
**Effort**: Low

### Priority Tier 3: LOW VALUE - Not Recommended

#### 8. Vine Copulas
**Why not**: Academic, high complexity, minimal trading edge

#### 9. Stochastic Control (Jurek, Mudchanatongsuk)
**Why not**: Requires dynamic optimization unsuitable for bar-by-bar EpochScript

#### 10. Neural Networks (MLP, LSTM, Pi-Sigma)
**Why not**: Epoch already has LightGBM, SVR; keras-based NNs are fragile

#### 11. Tearsheet Module
**Why not**: Epoch has full tearsheet system already

---

## Part 3: Bugs & Issues Found

### In EpochBackend (from cross-validation)

| # | Transform | Issue | Severity | Fix |
|---|-----------|-------|----------|-----|
| 1 | `engle_granger` | ADF regression missing constant term | **HIGH** | ~~Add constant column to X matrix~~ **FIXED** — replaced manual OLS with `adf::compute_adf("c")` |
| 2 | `engle_granger` | P-value uses linear interpolation (not polynomial) | LOW | Approximate, acceptable |
| 3 | `kalman_filter` | No pairs trading model type | FEATURE | Add `kalman_regression` model |
| 4 | `futures_continuation` | Null propagation (contracts/day correlation) | **HIGH** | Fix BuildBars() + searchsorted |

### In arbitragelab (for reference)

| # | Module | Issue | Notes |
|---|--------|-------|-------|
| 1 | `engle_granger` | Default no intercept | Unusual choice, most practitioners use intercept |
| 2 | `kalman_filter` | Incorrect predict/update cycle | Combined step, not standard Kalman |
| 3 | `kalman_filter` | Non-standard matrix naming | F for observation, R for prediction |
| 4 | `hurst_exponent` | slope * 2.0 scaling | Non-standard output |
| 5 | `copula_approach` | Deprecated pandas API (fillna) | pandas 2.1+ compatibility |

---

## Part 4: Implementation Roadmap

### Immediate (Bug Fixes)
1. ~~Fix `engle_granger` ADF constant term~~ **DONE**
2. Fix `futures_continuation` null propagation

### Short Term (1-2 weeks)
3. Add TLS hedge ratio transform
4. Add ADF-optimal hedge ratio transform
5. Add distance-based pair selection (cross-sectional)
6. Add Minimum Profit trading rule (from OU thresholds)

### Medium Term (2-4 weeks)
7. OU Model integration (Python warmup + EpochScript template)
8. Gaussian copula for pair screening
9. Distance correlation codependence measure
10. Mutual information codependence measure

### Long Term (Backlog)
11. Box-Tiao hedge ratio
12. Sparse MR portfolio
13. Kalman regression model type
14. Min-half-life hedge ratio

---

## Part 5: What Epoch Has That Arbitragelab Doesn't

| Capability | Epoch Count | arbitragelab |
|------------|------------|-------------|
| Technical Indicators | 84 | 0 |
| Candlestick Patterns | 34 | 0 |
| Portfolio Optimization | 12 | 0 |
| Position Management | 11 | 0 |
| ML Models | 14 | ~9 (different models) |
| Visualization | 24 | 1 (tearsheet) |
| Data Sources | 27 | 1 (Yahoo Finance) |
| Calendar/Time | 10+ | 0 |
| GARCH | 1 | 0 |
| Fractional Differentiation | 1 | 0 |
| Rolling everything | Yes | Mostly static |
| Cross-sectional analysis | 33 transforms | 0 |
| Intraday support | Yes | No |
| Production C++ | Yes | Python only |

**Conclusion**: EpochBackend is a comprehensive production platform. Arbitragelab is a specialized statistical arbitrage research library. The overlap is small (cointegration, hedge ratios, Kalman, Hurst) but the gaps in Epoch are meaningful for pairs/stat-arb strategies (OU optimal thresholds, distance-based pair selection, codependence measures).
