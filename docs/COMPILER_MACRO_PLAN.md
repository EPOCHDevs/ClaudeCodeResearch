# EpochScript Compiler Macro & Builtin Expansion — Index

**Status:** Pre-implementation — full design locked
**Principle:** Zero new runtime nodes. All new constructs are compile-time: either single-stage builtin aliases or macros that expand to existing impl nodes.

---

## Migration Criteria

A transform migrates **COMPLETE** or **PARTIAL** to grammar (Layer 1/2), or stays **Layer 3 only**.

### Decision Flow

```
Is it ML / Portfolio / Executor / Reporter?
  → YES: LAYER 3 (it's a subsystem, not a function)

Is it a DataSource with List-type filter params (query builder)?
  → YES: LAYER 3 (e.g. news, cs_news, economic_calendar)

Is it a DataSource with zero or simple enum/string options?
  → MIGRATE to builtin (e.g. earnings, balance_sheet, economic_indicators)

Does it have a required param with no default where the choice IS the research?
  → YES: LAYER 3 (e.g. vidya alpha, futures_continuation rollover_method)

Would an agent need to read docs to pick correct params?
  → YES: LAYER 3 (e.g. kalman_filter, engle_granger, rolling_garch)

Otherwise → MIGRATE:
  Single output?  → COMPLETE Builtin
  Multi-output?   → COMPLETE Macro

  Does the registered form have valid configs the builtin can't express?
    → YES: downgrade to PARTIAL (keep registered form public alongside builtin)
```

### COMPLETE — Builtin or Macro replaces registered form

Registered form → `internalUse=true`. Grammar one-liner is the only public form.

**The test:** Can `fn(inputs, options) → Type` in grammar tell an agent everything it needs?

Grammar now includes types, so nothing is excluded by return type. All of these pass:

```python
rsi(close, 14)                    # period-only param
apo(close, 12, 26)                # multi-period
arg_max(src) → Timestamp          # non-Decimal return
is_month_start(offset=-1)         # Boolean generator
calendar_shift(src, "1M")         # Duration param
zscore(src, 60, cross_sectional=True, group_by=GroupBy.sector)  # scope flag
switch(index, a, b, c)            # variadic
macd(close) → (line, signal, histogram)  # multi-output macro
```

### PARTIAL — Builtin added, registered form stays public

Builtin covers common cases. Full registered form stays `internalUse=false` for advanced configs the builtin syntax can't express.

```python
# Builtin covers 90%:
is_month_start()
is_opex()
# Registered form needed for "2nd Tuesday of March with offset -1 in US/Eastern":
is_period_boundary(period=year, month_anchor=3, ordinal=second, day_anchor=tuesday, offset=-1, timezone="America/New_York")(ts)
```

### LAYER 3 only — no builtin/macro

The transform stays two-stage `fn(opts)(inputs)`. Agent uses `find_by_id()` for schema.

**Stays Layer 3 if any of:**
1. **Subsystem** — ML, Portfolio, Executor, Reporter
2. **Query-builder DataSource** — List-type filter params (news, cs_news, economic_calendar)
3. **Choice IS the research** — required param, no universal default, domain decision
4. **Needs docs** — params are model specifications, not tuning knobs
5. **Genuinely niche** — agent wouldn't know it without looking it up

### What the criteria eliminated

Early criteria that are now **irrelevant** (grammar types removed the constraint):
- ~~"Surprising return type"~~ — grammar documents `→ Timestamp`, `→ Int`, `→ Boolean`
- ~~"Too many params"~~ — `ultosc(h, l, c, 7, 14, 28)` is fine as a one-liner
- ~~"Deep enum"~~ — `is_study_asset(sector="Technology")` works with named params
- ~~"Option-heavy"~~ — decompose into named builtins (`is_period_boundary` → 8 builtins + `is_opex`)

---

## Architecture: Three Layers

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: BUILTIN FUNCTIONS  (single-stage, inputs-first)       │
│  fn(inputs..., options...)  →  compiler maps to impl node       │
│  Grammar one-liner with → Type is the contract.                 │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: COMPILER MACROS  (single-stage, inputs-first)         │
│  fn(inputs..., options...)  →  expander emits N impl nodes      │
│  Grammar documents output tuple.                                │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: REGISTERED TRANSFORMS  (two-stage, metadata-driven)   │
│  fn(opts)(inputs)  →  single impl node, full metadata           │
│  ML, Portfolio, Executor, Reporter, query DataSources, niche.   │
└─────────────────────────────────────────────────────────────────┘
```

**Call shape is the signal:** single-stage = compile-time (Layer 1 or 2). Two-stage = registered transform (Layer 3 only).

### Dispatch Architecture (Phase 0e)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BuiltinRegistry (singleton, single source of truth)                    │
│  ├── builtins_: map<name, unique_ptr<IBuiltinLowering>>               │
│  └── macros_:   map<name, unique_ptr<IMacroExpander>>                  │
├─────────────────────────────────────────────────────────────────────────┤
│  IBuiltinLowering::Lower(name, args, kwargs, ctx) → LoweringResult     │
│  IMacroExpander::Expand(name, args, kwargs, ctx)   → ExpansionResult   │
├─────────────────────────────────────────────────────────────────────────┤
│  11 reusable strategies cover ~90% of builtins:                         │
│    SameNamePeriodLowering (45)  │  SameNameNoParamLowering (20)        │
│    MaAliasLowering (10)         │  AliasLowering (4)                   │
│    MultiPeriodLowering (7)      │  ArithmeticLowering (10)             │
│    PeriodBoundaryLowering (9)   │  EnumGatedLowering (4)               │
│    DataSourceLowering (14)      │  SingleImplMultiOutputExpander (36)  │
│    VariadicInputExpander (2)                                            │
│  + 6 custom strategies for special cases (agg, resample, marker, etc.) │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key design principles:**
- `constructor_parser.cpp` is a thin dispatcher (~30 lines) — no if/else chains
- Each strategy class has single responsibility and is unit-testable in isolation
- Registration is declarative in `InitializeTransforms()` — adding a builtin is one line
- Grammar arrays derived from registry — single source of truth
- Follows existing patterns: `OptionTypeFactory`/`OptionTypeRegistry`, `ISpecialNodeValidator`/`SpecialNodeValidatorRegistry`

---

## Grammar & Search Index

**Grammar includes types** — every builtin/macro one-liner documents `→ Type`:
- `BUILTIN_FUNCTIONS[]` — parser routes these names to single-stage path
- `COMPILER_MACROS[]` — same for Layer 2
- EBNF comment blocks with typed signatures

**Search index is complete** (`transforms_items.json`):
- Layer 3: already there
- Layer 1 builtins: ADD entries — same `find_by_id()` tool
- Layer 2 macros: ADD entries — same `find_by_id()` tool

---

## DSL Surface — All Layers

```python
# ── Layers 1 & 2: single-stage, inputs-first ─────────────────────

# Aggregation (enum-gated, shape determines axis)
peak_52w    = agg(close, 52, Agg.Max)
roll_std    = agg(returns, 20, Agg.Std)
sec_mean    = agg(momentum, Agg.Mean, GroupBy.sector)

# Classic TA builtins (Phase 5)
rsi_val     = rsi(close, 14)
score       = zscore(signal, 60)
cs_score    = zscore(signal, cross_sectional=True, group_by=GroupBy.sector)
peak_date   = arg_max(close)                    # → Timestamp
rebal       = is_month_start(offset=-1)         # → Boolean
mom_12m     = close / calendar_shift(close, "12M")
held        = hold_until(entry_sig, exit_sig)   # → Boolean

# Multi-output macros (Phase 5)
macd_line, signal_line, hist = macd(close)
upper, middle, lower         = bbands(close, 20, 2.0)
tenkan, kijun, span_a, span_b, chikou = ichimoku(high, low, close)

# Time-series / signal primitives (Phase 2)
entry_px    = valuewhen(signal, close)
age         = barssince(signal)
chg         = diff(close, 5)
clean       = nz(eps_surprise, 0)

# Data sources (Phase 1)
src                  = study_assets()
spy, eur             = reference_assets(stock("SPY"), fx("EURUSD"))

# DataSource builtins (Phase 1)
earn                 = earnings()
surprise             = earn.eps_surprise_percent
bs                   = balance_sheet(period=BalanceSheetTimeframe.quarterly)
current_ratio        = bs.current_assets / bs.current_liabilities
cpi_data             = economic_indicators(series_id="CPIAUCSL")
t10y                 = common_treasury_auctions(auction_type=TreasuryAuctionType.Note10Y)

# Macros (Phase 3)
cpi, pce, unemp      = macro_data(Macro.CPI, Macro.PCE, Macro.Unemployment)
doji_s, hammer_s     = candlestick_pattern(o, h, l, c, patterns=[Pattern.doji, Pattern.hammer])
vol_ts               = volatility(close, method=VolMethod.annualized, period=14)

# ── Layer 3: two-stage — ML, Portfolio, Executor, niche stats ────
clusters = kmeans(n_clusters=3)((returns_a, returns_b, returns_c))
weights  = hrp()(returns_matrix)
kf_val   = kalman_filter(observation_noise=0.1, transition_noise=0.01)(spread)
```

---

## Phase Files

| Phase | File | Focus | Status |
|---|---|---|---|
| 0 | [PHASE_0_GRAMMAR_FOUNDATION.md](PHASE_0_GRAMMAR_FOUNDATION.md) | Grammar routing + visualization enums + `BuiltinRegistry` dispatch architecture | Not started |
| 1 | [PHASE_1_FOUNDATION.md](PHASE_1_FOUNDATION.md) | `resample` macro + `study_assets` trading_hours + 14 DataSource builtins | Not started |
| 2 | [PHASE_2_BUILTINS.md](PHASE_2_BUILTINS.md) | `agg` + 19 time-series/quant/logic builtins | Not started |
| 3 | [PHASE_3_MACROS.md](PHASE_3_MACROS.md) | `marker`, `candlestick_pattern`, `macro_data`, `pair_stat`, `volatility`, `select` | Not started |
| 4 | [PHASE_4_CS_SCOPE.md](PHASE_4_CS_SCOPE.md) | `zscore`, `winsorize`, `rank` builtins with `cross_sectional` flag | Not started |
| 5 | [PHASE_5_INDICATORS.md](PHASE_5_INDICATORS.md) | ~99 classic TA builtins + ~36 multi-output macros | Not started |

---

## Transform Savings Summary

| Group | Transforms hidden | New public construct |
|---|---|---|
| Rolling primitives (max/min/sum/stddev/var) | 5 → internalUse | `agg` builtin |
| Cross-sectional agg (`cs_agg`) | 1 → internalUse | merged into `agg` |
| `mom` | 1 → internalUse | `diff` builtin |
| Candlestick patterns (26) | 26 → internalUse | `candlestick_pattern` macro |
| Pair statistics (rolling_corr/cov/beta/ewm_corr) | 4 → internalUse | `pair_stat` macro |
| Resample (downsample/upsample) | 2 → internalUse | `resample` macro |
| DataSource builtins (14 promoted) | 14 → internalUse | `earnings`, `analyst_ratings`, `ipos`, `splits`, `ticker_events`, `short_interest`, `short_volume`, `balance_sheet`, `cash_flow`, `income_statement`, `dividends`, `economic_indicators`, `economic_revisions`, `common_treasury_auctions` |
| Reference DataSources (replaced by `reference_assets`) | 5 → internalUse | — (no new construct, covered by `reference_assets`) |
| Macro data (common_indicators) | 1 → internalUse | `macro_data` macro |
| Volatility (volatility + basic_volatility) | 2 → internalUse | `volatility` macro |
| cs_* statistical (5 variants) | 5 → internalUse | scope flag on base transform |
| event_marker | 1 → internalUse | `marker` macro |
| valuewhen / barssince (two-stage) | 2 → internalUse | builtins (same name) |
| New time-series builtins (no old transform) | — | `returns`, `cum`, `linreg`, `lag`, `prev`, `ratio`, `normalize`, `drawdown`, `to_int`, `relu`, `between`, `isna`, `notna` |
| Utility builtins | — | `nz`, `clamp`, `sign` |
| **Phases 0–4 total** | **69 transforms → internalUse** | **41 new public constructs** |
| Phase 5 — MA aliases (10 MA types) | — | `ema`, `sma`, `wma`, `hma`, `dema`, `tema`, `kama`, `trima`, `wilders`, `zlema` |
| Phase 5 — Classic TA builtins | ~30 → internalUse | `rsi`, `atr`, `cci`, `obv`, `corr`, `cov`, `adx`, `arg_max`, `arg_min`, + 58 more |
| Phase 5 — Period boundary decompositions | — (is_period_boundary stays public) | `is_month_start`, `is_month_end`, `is_quarter_start`, ..., `is_opex` (9) |
| Phase 5 — Calendar shift + audit promotions | — | `calendar_shift`, `apo`, `ppo`, `ultosc`, `psar`, `adosc`, `kvo`, `vosc`, `hold_until`, `trade_count`, `forward_returns`, `switch`, `is_study_asset` |
| Phase 4 — CS builtins | 2 → internalUse | `zscore`, `winsorize` builtins with `cross_sectional` flag |
| Phase 5 — Multi-output macros | ~20 → internalUse | `macd`, `bbands`, `stoch`, `ichimoku`, `aroon`, `supertrend`, + 30 more |
| **All phases total** | **~201 transforms → internalUse** | **~178 public Layer 1/2 constructs** |
