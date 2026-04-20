# Phase 1 Implementation Plan

**Branch:** `feat/timeframe-resolve`
**Prereq:** Phase 0 committed (`51379a7d`, `ec2871fa`)
**Build:** `-j64` (m5.16xlarge, 64 vCPU, 246 GB RAM)

---

## Execution Order

Phase 1c first (14 DataSource builtins) — simplest, validates the full dispatch path end-to-end.
Then 1b (study_assets trading_hours) — enum gate on existing variadic macro.
Then 1a (resample) — most complex, needs direction inference + plurality validation.

Each sub-phase: implement → unit test → build → commit.

---

## Phase 1c — 14 DataSource Builtins

### Goal
Promote 14 DataSource transforms from two-stage `fn(opts)(inputs)` to single-stage `fn(opts)`.
Pure syntactic sugar — no new impl nodes, no runtime changes.

### Step 1: Wire dispatcher in constructor_parser.cpp

The current `ParseBuiltinFunctionCall` (~line 1175) handles existing math/logic builtins.
We need to add a dispatch path that checks `BuiltinRegistry::Instance().IsBuiltin(name)` and
routes to the registered `IBuiltinLowering::Lower()` strategy.

**File:** `constructor_parser.cpp`
**Change:** In `ParseBuiltinFunctionCall`, before the existing generic handling, add:

```cpp
auto& registry = BuiltinRegistry::Instance();
if (registry.IsBuiltin(ctor_name)) {
    auto& strategy = registry.GetBuiltin(ctor_name);
    // Extract args + kwargs from call AST
    // Call strategy.Lower(ctor_name, args, kwargs, ctx)
    // Convert LoweringResult → ConstructorParseResult (feed_steps)
    // Return
}
```

This is the "thin dispatcher" from Phase 0e acceptance criteria.

### Step 2: Register 14 DataSource builtins

**File:** `registration.cpp` (or new `builtin_registration.cpp`)
**Pattern:** Use existing `DataSourceLowering` strategy class from Phase 0.

```cpp
void RegisterPhase1Builtins() {
    auto& reg = BuiltinRegistry::Instance();

    // Event data (zero required args)
    reg.RegisterBuiltin("earnings", std::make_unique<DataSourceLowering>("earnings", ...));
    reg.RegisterBuiltin("analyst_ratings", std::make_unique<DataSourceLowering>("analyst_ratings", ...));
    // ... 12 more
}
```

Each `DataSourceLowering` needs: impl_node_id, accepted kwargs, required kwargs.

### Step 3: Add names to BUILTIN_FUNCTIONS array

**File:** `grammar_generator.cpp`
**Change:** Add 14 names to BUILTIN_FUNCTIONS vector:

```cpp
"earnings", "analyst_ratings", "ipos", "splits", "ticker_events",
"short_interest", "short_volume",
"balance_sheet", "cash_flow", "income_statement",
"dividends",
"economic_indicators", "economic_revisions",
"common_treasury_auctions",
```

### Step 4: Register 6 new enums for grammar inlining

**File:** `grammar_generator.cpp`
**Enums:**
- `BalanceSheetTimeframe` — annual, quarterly
- `ReportingPeriod` — annual, quarterly, trailing_twelve_months
- `DividendType` — CD, LT, SC, ST
- `EiaFrequency` — Annual, Daily, Monthly, Weekly
- `TreasuryAuctionType` — 15 values (Bill4W..TIPS30Y)
- `TradingHoursType` — RTH, Extended, PreMarket, PostMarket (for 1b, register now)

Check: these enums may already be registered via CREATE_ENUM. Verify before adding duplicates.
If they exist as C++ enums but not in the grammar generator's enum registry, add them.

### Step 5: Add EBNF documentation

**File:** `grammar_generator.cpp` → `GenerateEBNF()` function
**Add:** Tier D DataSources section in BUILTIN FUNCTIONS documentation.
Content: see PHASE_1_FOUNDATION.md lines 337-411.

### Step 6: Mark internalUse=true

**14 promoted DataSources** — find their metadata registration and add `.internalUse = true`.
Locations: `src/transforms/components/data_sources/` various metadata headers.

**5 reference DataSources** — already done in Phase 0 commit (reference_stocks, reference_futures,
fx_pairs, crypto_pairs, indices).

### Step 7: Unit tests

**New file:** `test/unit/compiler/datasource_builtins_test.cpp`

Tests:
1. `earnings()` compiles — zero args
2. `balance_sheet(period=BalanceSheetTimeframe.quarterly)` compiles — required arg
3. `balance_sheet()` without period → compile error
4. `economic_indicators(series_id="CPIAUCSL")` — string kwarg
5. `economic_indicators(eia_route="...", series_id="...")` — multiple kwargs
6. `dividends()` — optional type defaults to CD
7. `dividends(dividend_type=DividendType.LT)` — enum kwarg
8. Dot access: `earnings().eps_surprise` compiles
9. Regression: existing two-stage forms still work (if not internalUse)

### Step 8: Build + test + commit

```bash
ninja -C build -j64 epoch_script_test
./build/bin/epoch_script_test "[datasource_builtins]"
./build/bin/epoch_script_test "[compiler]"  # regression
```

---

## Phase 1b — study_assets trading_hours

### Goal
Add optional `trading_hours` kwarg to `study_assets()` for RTH/Extended/Pre/Post routing.

### Step 1: Register TradingHoursType enum

Already done in 1c Step 4 (registered for grammar inlining).

### Step 2: Add trading_hours option to study_assets metadata

**File:** Wherever `study_assets` metadata is defined (likely `src/transforms/components/data_sources/`).
**Add:** New `MetaDataOption` with id="trading_hours", type=Select, default="RTH".

### Step 3: Update constructor_parser routing

In the `study_assets` handling path, read `trading_hours` kwarg:
- RTH (default) → `market_data_source` impl node
- Extended → `extended_market_data_source` impl node
- PreMarket → `extended_market_data_source` with session option
- PostMarket → `extended_market_data_source` with session option

### Step 4: Unit tests

**Extend:** existing study_assets test file or new section.
1. `study_assets()` — default RTH, no regression
2. `study_assets(trading_hours=TradingHours.RTH)` — explicit RTH
3. `study_assets(trading_hours=TradingHours.Extended)` → extended_market_data_source

### Step 5: Build + test + commit

---

## Phase 1a — resample Compiler Macro

### Goal
Single-stage variadic macro with compile-time direction inference.

### Step 1: Add "resample" to COMPILER_MACROS

**File:** `grammar_generator.cpp`
**Change:** Uncomment `"resample"` in COMPILER_MACROS vector.

### Step 2: Create ResampleExpander

**New files:**
- `src/transforms/compiler/lowering_strategies/resample_expander.h`
- `src/transforms/compiler/lowering_strategies/resample_expander.cpp`

**Class:** `ResampleExpander : IMacroExpander`

**Expand() logic:**
1. Parse args: positional series inputs + kwargs (target_timeframe, agg, how)
2. Validate: target_timeframe required
3. Plurality check: `inputs.size() > 1 && tf_is_list` → error
4. Direction inference per (input, target_tf) pair:
   - Need source node's resolved timeframe from `CompilationContext`
   - Compare source_tf vs target_tf → downsample or upsample
   - Same TF → error
   - Unknown source TF → error
5. Conflict guards: agg+how, agg+upsample, how+downsample
6. Emit N `NodeSpec` entries: each is downsample or upsample impl node

**Key dependency:** Direction inference needs access to the source node's timeframe.
This requires `CompilationContext` to have resolved timeframes for upstream nodes.
Since `resample` is parsed after its inputs are already compiled (topological order),
the source timeframe should be available in `ctx.nodeTimeframes` or the node's metadata.

### Step 3: Register resample macro

**File:** `registration.cpp` or `builtin_registration.cpp`

```cpp
reg.RegisterMacro("resample", std::make_unique<ResampleExpander>());
```

### Step 4: Wire macro dispatch in constructor_parser.cpp

Similar to builtin dispatch but for macros:

```cpp
if (registry.IsMacro(ctor_name)) {
    auto& expander = registry.GetMacro(ctor_name);
    auto result = expander.Expand(ctor_name, args, kwargs, ctx);
    // Convert ExpansionResult → multiple ConstructorParseResult entries
    // Handle tuple unpacking for multi-output
}
```

### Step 5: Mark downsample/upsample internalUse=true

**Files:** downsample_metadata.h, upsample_metadata.h

### Step 6: EBNF documentation

**File:** `grammar_generator.cpp` → COMPILER MACROS section
Content: see PHASE_1_FOUNDATION.md lines 111-137.

### Step 7: Unit tests

**New file:** `test/unit/compiler/resample_expander_test.cpp`

10 test cases from spec:
1. Option-driven same direction (2 downsample nodes)
2. Input-driven (2 nodes, same TF)
3. Upsample direction inference
4. Downsample direction inference
5. Same-TF compile error
6. Both-plural compile error
7. Agg-how conflict error
8. Agg count mismatch error
9. Option-driven mixed direction
10. Mixed direction with agg conflict

### Step 8: Build + test + commit

---

## Critical Path Dependencies

```
Phase 1c (DataSource builtins)
  └─ Requires: thin dispatcher in constructor_parser.cpp (Step 1)
  └─ Requires: DataSourceLowering strategy (Phase 0, already exists)

Phase 1b (trading_hours)
  └─ Requires: TradingHoursType enum (done in 1c Step 4)
  └─ Requires: study_assets metadata location identified

Phase 1a (resample)
  └─ Requires: macro dispatch path in constructor_parser.cpp
  └─ Requires: source timeframe available in CompilationContext
  └─ Requires: ExpansionResult → multi-node emission working
```

## Files Changed (Summary)

| File | Phase | Change |
|------|-------|--------|
| `grammar_generator.cpp` | 1c | Add 14 names to BUILTIN_FUNCTIONS, 6 enums, EBNF docs |
| `grammar_generator.cpp` | 1a | Uncomment resample in COMPILER_MACROS, add EBNF |
| `constructor_parser.cpp` | 1c | Add thin dispatcher for builtins |
| `constructor_parser.cpp` | 1a | Add thin dispatcher for macros |
| `registration.cpp` | 1c+1a | RegisterBuiltin × 14, RegisterMacro × 1 |
| 14× data source metadata headers | 1c | `.internalUse = true` |
| `downsample_metadata.h` | 1a | `.internalUse = true` |
| `upsample_metadata.h` | 1a | `.internalUse = true` |
| study_assets metadata | 1b | Add trading_hours option |
| `lowering_strategies/CMakeLists.txt` | 1a | Add resample_expander.cpp |

## Files Created

| File | Phase |
|------|-------|
| `resample_expander.h` | 1a |
| `resample_expander.cpp` | 1a |
| `test/unit/compiler/datasource_builtins_test.cpp` | 1c |
| `test/unit/compiler/resample_expander_test.cpp` | 1a |

## Risk Areas

1. **Thin dispatcher**: Converting `LoweringResult` → existing `ConstructorParseResult` / feed_steps.
   Need to read how `ParseBuiltinFunctionCall` currently builds its return value.

2. **Direction inference**: Accessing source timeframe during macro expansion.
   TimeframeResolver runs after compilation — but `resample` needs TF info during compilation.
   May need to resolve source TF eagerly or store it on the node during compilation.

3. **DataSource builtins with no inputs**: Current `ParseBuiltinFunctionCall` may assume
   at least one positional arg (series). DataSource builtins have zero positional args.
   Need to handle this in the dispatcher.

4. **Enum registration**: Some enums may already exist as C++ types but not in the grammar
   generator's registry. Need to check for collisions with existing `CREATE_ENUM` registrations.
