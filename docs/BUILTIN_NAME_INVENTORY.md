# Builtin Name Inventory

Source survey across pandas, NumPy, Pine Script, TA-Lib, and quant finance libraries.
Used to decide canonical builtin names for Phase 2. No decisions made here — inventory only.

---

## pandas (Series methods)

### Difference / change
| pandas name | formula | notes |
|---|---|---|
| `.diff(N=1)` | `src - src[N]` | absolute difference |
| `.pct_change(N=1)` | `(src - src[N]) / abs(src[N])` | simple percentage return |
| `.shift(N=1)` | `src[N]` | lag by N periods |

### Cumulative
| pandas name | formula |
|---|---|
| `.cumsum()` | cumulative sum from start |
| `.cumprod()` | cumulative product from start |
| `.cummax()` | running maximum from start |
| `.cummin()` | running minimum from start |

### Rolling window (via `.rolling(N).`)
| pandas name | notes |
|---|---|
| `.mean()` | rolling mean |
| `.std(ddof=1)` | rolling std dev |
| `.var(ddof=1)` | rolling variance |
| `.min()` | rolling min |
| `.max()` | rolling max |
| `.sum()` | rolling sum |
| `.median()` | rolling median |
| `.skew()` | rolling skewness |
| `.kurt()` | rolling kurtosis |
| `.quantile(q)` | rolling quantile |
| `.corr(other)` | rolling correlation |
| `.cov(other)` | rolling covariance |
| `.rank(pct=False)` | rolling rank |
| `.apply(func)` | custom function — not applicable |

### Expanding window (via `.expanding().`)
| pandas name | notes |
|---|---|
| `.mean()` | expanding mean |
| `.sum()` | expanding sum (same as cumsum) |
| `.min()` | expanding min (same as cummin) |
| `.max()` | expanding max (same as cummax) |
| `.std()` | expanding std |
| `.var()` | expanding var |
| `.skew()` | expanding skew |
| `.kurt()` | expanding kurtosis |

### EWM (via `.ewm(span).`)
| pandas name | notes |
|---|---|
| `.mean()` | exponentially weighted mean |
| `.std()` | EWM std dev |
| `.var()` | EWM variance |
| `.corr(other)` | EWM correlation |
| `.cov(other)` | EWM covariance |

### Null handling
| pandas name | formula/notes |
|---|---|
| `.fillna(value)` | replace NaN with value |
| `.ffill()` | forward fill NaN |
| `.bfill()` | backward fill NaN |
| `.isna()` / `.isnull()` | is null → Boolean |
| `.notna()` / `.notnull()` | is not null → Boolean |
| `.clip(lo, hi)` | clamp to range |

### Boolean / selection
| pandas name | notes |
|---|---|
| `.where(cond, other)` | keep if cond else other |
| `.mask(cond, other)` | replace if cond else keep |
| `.between(lo, hi)` | lo <= src <= hi → Boolean |

### Rank / normalization
| pandas name | notes |
|---|---|
| `.rank()` | integer rank |
| `.rank(pct=True)` | percentile rank [0,1] |

### Math
| pandas name | notes |
|---|---|
| `.abs()` | absolute value |
| `.round(N)` | round to N decimals |

---

## NumPy

### Difference / change
| numpy name | formula |
|---|---|
| `np.diff(src, n=1)` | `src[i] - src[i-n]` — absolute diff |
| `np.log(src / np.roll(src, N))` | log return (no native function) |

### Cumulative
| numpy name | formula |
|---|---|
| `np.cumsum(src)` | cumulative sum |
| `np.cumprod(src)` | cumulative product |

### Math
| numpy name | notes |
|---|---|
| `np.abs(src)` | absolute value |
| `np.sign(src)` | -1, 0, 1 |
| `np.clip(src, lo, hi)` | clamp |
| `np.log(src)` | natural log |
| `np.log10(src)` | log base 10 |
| `np.exp(src)` | e^x |
| `np.sqrt(src)` | square root |
| `np.power(src, N)` | src^N |
| `np.maximum(a, b)` | element-wise max |
| `np.minimum(a, b)` | element-wise min |
| `np.where(cond, a, b)` | conditional |
| `np.isnan(src)` | is NaN |
| `np.nan_to_num(src, nan=0)` | replace NaN with 0 |

---

## TradingView Pine Script v5

### Change / momentum
| pine name | formula | notes |
|---|---|---|
| `ta.change(src, N=1)` | `src - src[N]` | absolute change |
| `ta.mom(src, N)` | `src - src[N]` | same as change, different name |
| `ta.roc(src, N)` | `(src - src[N]) / src[N] * 100` | % rate of change × 100 |

### Lag
| pine name | formula |
|---|---|
| `src[N]` | lag — direct indexing syntax |

### Rolling stats
| pine name | notes |
|---|---|
| `ta.highest(src, N)` | rolling max |
| `ta.lowest(src, N)` | rolling min |
| `ta.highestbars(src, N)` | bars since rolling high |
| `ta.lowestbars(src, N)` | bars since rolling low |
| `ta.stdev(src, N)` | rolling std dev |
| `ta.variance(src, N)` | rolling variance |
| `ta.sma(src, N)` | simple moving average |
| `ta.ema(src, N)` | exponential moving average |
| `ta.wma(src, N)` | weighted moving average |
| `ta.vwma(src, N)` | volume-weighted MA |
| `ta.correlation(src1, src2, N)` | rolling Pearson correlation |
| `ta.covariance(src1, src2, N)` | rolling covariance |

### Signal / control flow
| pine name | notes |
|---|---|
| `ta.crossover(a, b)` | a crosses above b |
| `ta.crossunder(a, b)` | a crosses below b |
| `ta.cross(a, b)` | either cross |
| `ta.barssince(cond)` | bars since condition |
| `ta.valuewhen(cond, src, N)` | value at Nth most recent True |

### Null handling
| pine name | notes |
|---|---|
| `nz(src, default=0)` | replace na with default |
| `na(src)` | is NA → Boolean |
| `fixnan(src)` | forward fill (same as ffill) |

### Math
| pine name | notes |
|---|---|
| `math.abs(src)` | absolute value |
| `math.sign(src)` | sign |
| `math.log(src)` | natural log |
| `math.log10(src)` | log base 10 |
| `math.exp(src)` | e^x |
| `math.sqrt(src)` | square root |
| `math.pow(base, exp)` | power |
| `math.max(a, b, ...)` | maximum |
| `math.min(a, b, ...)` | minimum |
| `math.round(src, N)` | round |
| `math.floor(src)` | floor |
| `math.ceil(src)` | ceiling |

---

## TA-Lib (relevant non-indicator functions)

### Math operators (TALIB MATH group)
| talib name | notes |
|---|---|
| `ADD(a, b)` | addition |
| `DIV(a, b)` | division |
| `MULT(a, b)` | multiplication |
| `SUB(a, b)` | subtraction |
| `SUM(src, N)` | rolling sum |
| `MAX(src, N)` | rolling max |
| `MIN(src, N)` | rolling min |
| `MAXINDEX(src, N)` | index of rolling max |
| `MININDEX(src, N)` | index of rolling min |
| `SQRT(src)` | square root |
| `LN(src)` | natural log |
| `LOG10(src)` | log base 10 |
| `EXP(src)` | e^x |
| `ABS(src)` | absolute value |
| `ACOS/ASIN/ATAN/COS/SIN/TAN` | trig |

### Momentum group — rate of change variants
| talib name | formula | notes |
|---|---|---|
| `MOM(src, N)` | `src - src[N]` | absolute |
| `ROC(src, N)` | `(src - src[N]) / src[N] * 100` | percentage × 100 |
| `ROCP(src, N)` | `(src - src[N]) / src[N]` | percentage (not × 100) |
| `ROCR(src, N)` | `src / src[N]` | ratio |
| `ROCR100(src, N)` | `src / src[N] * 100` | ratio × 100 |

### Stat functions
| talib name | notes |
|---|---|
| `LINEARREG(src, N)` | linear regression value |
| `LINEARREG_SLOPE(src, N)` | slope of linear regression |
| `LINEARREG_INTERCEPT(src, N)` | intercept |
| `LINEARREG_ANGLE(src, N)` | angle of regression line |
| `STDDEV(src, N)` | rolling std dev |
| `VAR(src, N)` | rolling variance |
| `CORREL(src1, src2, N)` | rolling Pearson correlation |
| `BETA(src1, src2, N)` | rolling beta |
| `TSF(src, N)` | time series forecast (1-bar ahead) |

---

## Quant finance (empyrical, pyfolio, common conventions)

### Return series
| name | formula | notes |
|---|---|---|
| `simple_return` / `returns` | `(src - src[1]) / src[1]` | 1-period simple return |
| `log_return` | `ln(src / src[1])` | 1-period log return |
| `cum_return` | `cumprod(1 + returns) - 1` | cumulative return from start |
| `total_return` | same as cum_return | |
| `annualized_return` | `(1 + cum_return) ^ (252/N) - 1` | complex, needs period assumption |

### Drawdown
| name | formula | notes |
|---|---|---|
| `drawdown` | `(src - cummax(src)) / cummax(src)` | current drawdown from peak |
| `max_drawdown(N)` | `min(drawdown over N bars)` | rolling max drawdown |
| `underwater` | same as drawdown | alternative name |

### Normalization / scaling
| name | formula | notes |
|---|---|---|
| `normalize` / `minmax` | `(src - min(N)) / (max(N) - min(N))` | min-max to [0,1] |
| `zscore` | already a registered transform | |
| `rank_pct` | cs_rank as percentile [0,1] | |

### Ratio to prior
| name | formula | notes |
|---|---|---|
| `ratio(src, N=1)` | `src / src[N]` | same as ROCR |
| `relative(src, base)` | `src / base` | relative to another series |

---

## Summary — operations without a clean EpochScript path today

| Operation | Natural names | Formula |
|---|---|---|
| Absolute diff | diff, change, mom | `src - src[N]` |
| Pct change | pct_change, returns, ret, simple_return, rocp | `(src - src[N]) / src[N]` |
| Log return | log_return, log_ret | `ln(src / src[N])` |
| Ratio | ratio, rocr, rel | `src / src[N]` |
| Lag | lag, shift, prev (N=1) | `src[N]` |
| Cum sum | cumsum | expanding sum |
| Cum product | cumprod | expanding product |
| Cum max | cummax, running_max | expanding max |
| Cum min | cummin, running_min | expanding min |
| Bool → int | to_int, indicator, int_val | `where(cond, 1, 0)` |
| ReLU / zero floor | relu, positive, clip_zero | `max(src, 0)` |
| Min-max scale | normalize, minmax_scale | `(src-min(N))/(max(N)-min(N))` |
| Drawdown | drawdown, underwater | `(src - cummax) / cummax` |
| Pct ROC × 100 | roc_pct | `(src - src[N]) / src[N] * 100` |
| Linear reg value | linreg, tsf | forecast from linear reg |
| Is null | isna, isnull, na | Boolean |
| Is not null | notna, notnull | Boolean |
| Between | between, in_range | `lo <= src <= hi` |
