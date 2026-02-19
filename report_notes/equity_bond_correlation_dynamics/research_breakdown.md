# Stock-Bond Correlation Regime Analysis - Research Breakdown

**Linear Issue:** ENG-609
**Source Article:** Larry Swedroe - "Implications of Regime-Shifting Stock and Bond Correlations"
**Based on:** AQR Research "Changing Stock–Bond Correlation: Drivers and Implications"

---

## Hypotheses & Implementation Checklist

### H1: SBC is Regime-Dependent, Not Constant
- [x] **Chart 1:** Rolling SBC time series (2003-present using SPY/TLT)
- **Claim:** Correlation shifts between +0.18 (1926-1999) and -0.20 (2000-2022)
- **Chart Type:** `xy_lines` time series
- **Data:** SPY (S&P 500 ETF), TLT (20-Year Treasury ETF), rolling correlation
- **Results:** Mean SBC -0.20 (matches AQR's 21st century average), range -0.91 to +0.86
- **Definition:** `project/definitions/test_runner/eng609_stock_bond_correlation_regime.json`

### H2: SBC Shift Increases 60/40 Portfolio Volatility by ~20%
- [x] **Chart 2:** Portfolio volatility vs SBC level (scatter + time series)
- **Claim:** Vol increases ~20% as SBC rises from -0.5 to +0.5
- **Chart Type:** `xy_scatter` (SBC vs Vol) + `xy_lines` (Vol over time)
- **Data:** Rolling 52-week volatilities and correlation from SPY/TLT
- **Results:** Portfolio vol 7.5% at low SBC, 12.1% at high SBC (~60% increase)
- **Definition:** `project/definitions/test_runner/eng609_stock_bond_correlation_regime.json`

### H3: Higher SBC Reduces Portfolio Expected Returns
- [ ] **Chart 3:** Expected return vs SBC level
- **Claim:** Excess return drops from 3.5% to 3.0% at constant risk
- **Chart Type:** Line chart
- **Data:** Risk-adjusted allocation weights at each correlation level

### H4: Opposite Growth Sensitivity, Same Inflation Sensitivity
- [ ] **Chart 4:** Sharpe ratio by regime (growth up/down, inflation up/down)
- **Claim:** Stocks prefer growth up; Bonds prefer inflation down; Both dislike inflation up
- **Chart Type:** Grouped bar chart
- **Data:** Returns segmented by economic regime

### H5: Inflation Uncertainty Explains 71% of SBC (R²=0.71)
- [ ] **Chart 5a:** Model inputs - rolling volatilities
- [ ] **Chart 5b:** Model inputs - growth-inflation correlation
- [ ] **Chart 7:** Model fit - Forecast vs Realized SBC
- **Claim:** 3-factor model (inflation vol, growth vol, growth-inflation corr) explains SBC
- **Chart Type:** Dual-panel time series
- **Data:** FRED CPIAUCSL, FRED INDPRO, 10-year rolling calculations

### H6: Inflation Uncertainty is Dominant Driver
- [ ] **Chart 6:** Variance decomposition table
- **Claim:** Inflation uncertainty > growth-inflation correlation > growth uncertainty
- **Chart Type:** Table or stacked bar
- **Data:** Regression decomposition from H5 model

### H7: Inflation Uncertainty is Rising
- [ ] **Chart 8:** Inflation uncertainty trend (recent uptick)
- **Claim:** Current inflation uncertainty trending up → positive SBC likely to persist
- **Chart Type:** Time series with recent period highlighted
- **Data:** Rolling CPI volatility

### H8: SBC Exhibits Autocorrelation
- [ ] **Analysis:** Lag-1 autocorrelation of SBC series
- **Claim:** Last month's SBC predicts next month's SBC
- **Data:** Rolling monthly SBC, autocorrelation calculation

---

## Data Requirements

| Asset/Indicator | Source | Symbol | Frequency |
|-----------------|--------|--------|-----------|
| US Stocks | Yahoo | SPY / ^GSPC | Daily/Weekly |
| Long-Term Treasuries | Yahoo | TLT / Custom | Daily/Weekly |
| CPI | FRED | CPIAUCSL | Monthly |
| Industrial Production | FRED | INDPRO | Monthly |
| 10-Year Treasury Yield | FRED | DGS10 | Daily |

---

## Calculations Reference

### Rolling Stock-Bond Correlation
```
stock_ret = pct_change(spy, 1)
bond_ret = pct_change(tlt, 1)
sbc = rolling_corr(stock_ret, bond_ret, 52)  # 52-week rolling
```

### Inflation Uncertainty (10-year rolling CPI volatility)
```
cpi_yoy = pct_change(cpi, 12)  # 12-month change
inflation_vol = rolling_std(cpi_yoy, 120)  # 120 months = 10 years
```

### Growth Uncertainty (10-year rolling INDPRO volatility)
```
indpro_yoy = pct_change(indpro, 12)
growth_vol = rolling_std(indpro_yoy, 120)
```

### Growth-Inflation Correlation
```
growth_inf_corr = rolling_corr(cpi_yoy, indpro_yoy, 120)
```

### 60/40 Portfolio Volatility at Different SBC Levels
```
port_vol = sqrt(0.36 * stock_vol^2 + 0.16 * bond_vol^2 + 2 * 0.6 * 0.4 * sbc * stock_vol * bond_vol)
```

---

## Implementation Priority

| Priority | Chart | Hypothesis | Complexity |
|----------|-------|------------|------------|
| 1 | Chart 1 | H1 - SBC Time Series | Low |
| 2 | Chart 5a/5b | H5 - Model Inputs | Medium |
| 3 | Chart 7 | H5 - Model Fit | Medium |
| 4 | Chart 8 | H7 - Rising Uncertainty | Low |
| 5 | Chart 4 | H4 - Regime Sensitivity | High |
| 6 | Chart 2 | H2 - Portfolio Vol | Medium |
| 7 | Chart 3 | H3 - Portfolio Return | Medium |
| 8 | Chart 6 | H6 - Variance Decomp | High |

---

## Original Article Charts

| File | Description |
|------|-------------|
| swedroeregime1.png | Rolling SBC showing regime shifts |
| swedroeregime2.png | 60/40 portfolio volatility vs SBC |
| swedroeregime3.png | Portfolio expected return vs SBC |
| swedroeregime4.png | Sharpe ratio by growth/inflation regime |
| swedroeregime5.png | Model inputs (Panel A: volatilities, Panel B: correlation) |
| swedroeregime6.png | Variance decomposition table |
| swedroeregime7.png | Model fit: Forecast vs Realized SBC |
| swedroeregime8.png | Inflation uncertainty trend |

---

## Notes

- Time period for analysis: 1936-2022 (matches AQR paper)
- Rolling windows: 10-year for uncertainty measures, shorter for SBC visualization
- Monthly data for FRED series, weekly for market data
