# Package Architecture: Transform + Skills + Metadata Co-location

## Context

Transform metadata is embedded inline in C++ `register.h` files, causing full rebuilds on any description change. Skills live in a separate repo (EpochAI) with no deterministic link to the transforms they describe. The `search` tool uses BM25 freeform search — the agent can't reliably load "everything about line charts" in one call.

**Goal**: Co-locate transforms, skills, and metadata in package directories within `epoch-script`. CMake collects non-C++ assets at build time. No rebuild for metadata/skill edits. Agent gets `import_package(PackageEnum)` instead of freeform search.

**Proven patterns in codebase:**
- `file(COPY files/ DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})` — epoch-script CMakeLists.txt:72-76
- `EPOCH_CHART_DEFINITIONS_DIR` compile definition — epoch-script CMakeLists.txt:82-87
- `YamlChartDefinitionRegistry` runtime directory loader — timeseries_chart_runtime/

**CMake approach:** Use `string(JSON)` (CMake 3.19+) to read metadata JSON at configure time and `configure_file()` to inject documentary fields into generated C++ headers. No runtime metadata loading needed — single JSON source, CMake generates the glue.

---

## Package Enum (20 packages)

```cpp
CREATE_ENUM(TransformPackage,
    Inbuilt,              // Grammar-level (Layer 1/2) — no package dir
    Lines,                // xy_lines, cs_lines, timeseries_lines, labeled variants
    Bars,                 // xy_bars, cs_bars, histogram
    Scatter,              // xy_scatter, cs_scatter, bubble, labeled variants
    Tables,               // summary_table, cs_summary_table, detailed_table, cs_detailed_table
    Cards,                // cards, cs_cards, gauge, cs_gauge, pie, cs_pie
    Heatmaps,             // heatmap, cs_heatmap
    Distributions,        // boxplot, cs_boxplot, bellcurve
    SMC,                  // bos_choch, fair_value_gap, order_blocks, liquidity, swing_highs_lows, retracements, previous_high_low
    PortfolioAllocation,  // hrp, herc, equal_weight, inv_vol_weight, risk_parity, risk_budgeting, max_sharpe, min_variance, min_cvar, min_semivariance, max_diversification, black_litterman
    Execution,            // long_and_short_zone, stop_loss, take_profit, trailing_stop, risk_unit, position_size, cppi, tipp, kelly, optimal_f, rollover_policy
    Econometrics,         // engle_granger, johansen, rolling_adf, rolling_arima, kalman_filter, multi_linear_fit, rolling_garch, frac_diff, half_life_ar1, linear_fit, finance_ratio, cs_factor_analysis
    MachineLearning,      // lightgbm_*, logistic_*, svr_*, ml_zscore, ml_minmax, ml_robust, kmeans, dbscan, hmm, pca
    Macroeconomics,       // economic_indicators, common_indicators, economic_calendar, economic_revisions, common_treasury_auctions
    Fundamental,          // earnings, analyst_ratings, dividends, income_statement, balance_sheet, cash_flow
    News,                 // news, cs_news
    CorporateEvents,      // ipos, short_interest, short_volume, splits, ticker_events
    MarketData,           // market_data_source, reference_*, common_*, futures_continuation, downsample, upsample
    Sessions,             // session_window, session_gap, holiday, is_period_boundary, turn_of_month, day/month/quarter/week calendar
    NLP,                  // keyword_match, keyword_count, keyword_score, topic_classify, string_case/trim/contains/check
    Compute               // Catch-all: ma, vidya, returns, cumulative, zscore, rolling_corr, cs_*, event_marker, etc.
);
```

---

## Sprint Breakdown

### Sprint 1: Directory Restructure — Package Folders

**Scope**: Move transform implementations from 22 flat component dirs into package-based dirs. This is the heaviest mechanical lift but has zero behavioral change — just `#include` path updates. Establishes the physical layout everything else hangs on.

**New directory layout:**
```
src/transforms/
├── packages/
│   ├── lines/
│   │   ├── impl/              # lines.h, labeled_lines.h (from reports/)
│   │   └── register.h
│   ├── bars/
│   │   ├── impl/
│   │   └── register.h
│   ├── scatter/
│   ├── tables/
│   ├── cards/
│   ├── heatmaps/
│   ├── distributions/
│   ├── smc/
│   ├── portfolio_allocation/
│   ├── execution/
│   ├── econometrics/
│   ├── machine_learning/
│   ├── macroeconomics/
│   ├── fundamental/
│   ├── news/
│   ├── corporate_events/
│   ├── market_data/
│   ├── sessions/
│   ├── nlp/
│   └── compute/              # Catch-all
├── inbuilt/                   # Tulip, operators, scalars (unchanged structure)
│   ├── tulip/
│   ├── operators/
│   ├── scalars/
│   └── hosseinmoein_inbuilt/  # Indicators migrating to Layer 1/2
├── compiler/
├── runtime/
└── registration.cpp
```

**Mechanical work:**
- Create package dirs + `impl/` subdirs
- Move `.h` files from old locations to `packages/<name>/impl/`
- Update `#include` paths across the codebase
- Update CMakeLists.txt `add_subdirectory` calls
- Update `registration.cpp` includes

**Deliverables:**
- All transforms in package-based directory structure
- Build passes with new paths
- All tests pass

**Verification:**
- Full build: `./cpp_tools/run_target.sh -j64 epoch_script`
- All test suites pass
- `git diff --stat` — only moves, no content changes to `.h` files

---

### Sprint 2: Metadata Externalization — JSON + CMake `configure_file`

**Scope**: Extract documentary metadata to JSON files inside the new package dirs. CMake reads JSON at configure time via `string(JSON)` and generates C++ headers with `configure_file()`. No runtime metadata loading needed. Edit JSON → re-configure → only the affected generated header recompiles (fast incremental).

**What moves to JSON:**
- `desc` (description string) — MOST FREQUENT edit
- `name` (display name)
- `tags` (semantic tags)
- `strategyTypes` (LLM hints)
- `relatedTransforms` (cross-references)
- `assetRequirements` (asset constraints)
- `options[].desc` (option descriptions)
- `options[].tuningGuidance` (tuning hints)

**What stays handwritten in C++ (affects compilation/validation):**
- `id`, `category`, `role`, `plotKind` (enums, dispatch)
- `options[].type`, `options[].elementType`, `options[].selectOption` (type system, grammar gen)
- `inputs`, `outputs` (I/O validation)
- `internalUse`, `hasNullTransform`, `nullPolicy`, `dataLengthPolicy` (compiler/runtime flags)
- `generic_alias`, `variadic_expansion_option` (compiler)

**JSON format per transform** (`packages/<name>/metadata/<transform_id>.json`):
```json
{
  "id": "xy_lines",
  "name": "XY Lines - ONE PER ASSET",
  "desc": "Render numeric X-Y data as line chart with optional area fills, reference lines, and plot bands.",
  "tags": ["visualization", "line-chart", "time-series", "overlay"],
  "strategyTypes": [],
  "relatedTransforms": ["cs_lines", "labeled_lines", "timeseries_lines"],
  "assetRequirements": ["single-asset"],
  "options_docs": {
    "title": "Chart title displayed above the visualization",
    "series": "Line series definitions with color, dash style, and area fill options"
  }
}
```

**CMake generation** — reusable function, defined once:
```cmake
# In packages/CMakeLists.txt
function(epoch_generate_metadata PACKAGE_NAME)
    file(GLOB _meta_files "${CMAKE_CURRENT_SOURCE_DIR}/${PACKAGE_NAME}/metadata/*.json")
    foreach(_meta ${_meta_files})
        file(READ ${_meta} _json)
        string(JSON _id GET ${_json} "id")
        string(JSON _name GET ${_json} "name")
        string(JSON _desc GET ${_json} "desc")
        # ... extract tags, strategyTypes, etc.

        set(TRANSFORM_ID ${_id})
        set(TRANSFORM_NAME ${_name})
        set(TRANSFORM_DESC ${_desc})

        configure_file(
            "${CMAKE_CURRENT_SOURCE_DIR}/docs_overlay.h.in"
            "${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_NAME}/${_id}_docs.generated.h"
            @ONLY
        )
    endforeach()
endfunction()
```

**Generated header template** (`docs_overlay.h.in`):
```cpp
// AUTO-GENERATED from @TRANSFORM_ID@.json — do not edit
meta.name = "@TRANSFORM_NAME@";
meta.desc = "@TRANSFORM_DESC@";
// tags, strategyTypes, etc. follow same pattern
```

**Usage in register.h** — structural stays handwritten, documentary injected:
```cpp
auto meta = TransformsMetaData{
    .id = "xy_lines",
    .category = TransformCategory::Reporter,
    .plotKind = TransformPlotKind::custom,
    .options = { /* types, enums — structural */ },
    .inputs = { /* I/O specs */ },
    .outputs = { /* I/O specs */ },
};
#include "xy_lines_docs.generated.h"  // injects name, desc, tags from JSON
RegisterMetadataWithEnums(meta);
```

**Deliverables:**
- ~250 `.json` metadata files in their package dirs
- CMake generates `_docs.generated.h` per transform at configure time
- `register.h` includes generated header — no inline documentary strings
- Edit a `.json` → `cmake` re-configures → only that register.h recompiles (fast)
- No runtime `MetadataOverlayRegistry` needed — all resolved at build time

**Verification:**
- `./cpp_tools/run_target.sh -j64 --run epoch_script_test`
- `./bin/export_transforms` — output identical to pre-sprint
- Edit a `.json` desc → re-run build → verify only minimal recompilation

---

### Sprint 3: TransformPackage Enum + Tags

**Scope**: Add the enum, tag every transform. Register.h files are already in their package dirs from Sprint 1, so tagging is trivial — each register.h just sets its own package.

**Files to modify:**
- `metadata.h` — add `TransformPackage` enum (20 values) + field to `TransformsMetaData`
- All package `register.h` files — add `.package = TransformPackage::X` to every metadata initializer
- `export_transforms.cpp` — include `package` field in JSON output
- Glaze serialization for the new enum

**Deliverables:**
- `transform_metadata.json` gains `"package": "Lines"` on every transform
- All tests pass unchanged
- Existing behavior identical

**Verification:**
- `./cpp_tools/run_target.sh -j64 --run epoch_script_test`
- `./bin/export_transforms` — diff output, only new `package` field added

---

### Sprint 4: Skills Migration — Co-locate with Packages

**Scope**: Move skills from `EpochAI/agent_src/prompts/skills/` to `epoch-script/src/transforms/packages/<name>/skills/`. CMake collects them.

**Mapping (339 skill files):**

| EpochAI Source | Target Package | Count |
|---|---|---|
| `reporting/lines/*` | `packages/lines/skills/` | 28 |
| `reporting/bars/*` | `packages/bars/skills/` | 27 |
| `reporting/scatter/*` + `reporting/bubble/*` | `packages/scatter/skills/` | 45 |
| `reporting/tables/*` + `S81_table_formatting` | `packages/tables/skills/` | 15 |
| `reporting/gauge/*` + `reporting/pie/*` | `packages/cards/skills/` | 26 |
| `reporting/heatmap/*` | `packages/heatmaps/skills/` | 21 |
| `reporting/histogram/*` + `reporting/boxplot/*` | `packages/distributions/skills/` | 21 |
| `S58, S59` (order flow/candlestick) | `packages/smc/skills/` | 2 |
| `execution/E01-E18` (minus E14, E15) | `packages/execution/skills/` | 15 |
| `S20-S23` (portfolio/weighting) | `packages/portfolio_allocation/skills/` | 4 |
| ML-related compute/signal skills | `packages/machine_learning/skills/` | 6 |
| `D07-D09, S31-S32, D21` | `packages/macroeconomics/skills/` | 6 |
| `D10-D11, S33, S29` | `packages/fundamental/skills/` | 4 |
| `D15, D12` | `packages/news/skills/` | 2 |
| `D01-D06, D13-D14, D18-D20, S24-S26, S44` | `packages/market_data/skills/` | 15 |
| `S13, E14-E15, S15, reporting/events/*` | `packages/sessions/skills/` | 6 |
| `S56-S57` | `packages/nlp/skills/` | 2 |
| Remaining compute/signal/design rules | `global_skills/` | ~38 |

**CMake — `epoch_package()` function handles everything per package:**
```cmake
# In packages/CMakeLists.txt — define once
set(EPOCH_SKILLS_DIR "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/skills" CACHE PATH "Collected skills")
set(EPOCH_METADATA_DIR "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/metadata" CACHE PATH "Collected metadata")

function(epoch_package NAME)
    # 1. Collect impl sources
    file(GLOB_RECURSE _sources "${CMAKE_CURRENT_SOURCE_DIR}/${NAME}/impl/*.cpp")
    if(_sources)
        target_sources(epoch_script PRIVATE ${_sources})
    endif()

    # 2. Copy skills preserving package structure
    file(GLOB _skills "${CMAKE_CURRENT_SOURCE_DIR}/${NAME}/skills/*.md")
    if(_skills)
        file(COPY ${_skills} DESTINATION "${EPOCH_SKILLS_DIR}/${NAME}")
    endif()

    # 3. Generate metadata headers from JSON (Sprint 2)
    epoch_generate_metadata(${NAME})

    # 4. Copy raw JSON for agent consumption
    file(GLOB _meta "${CMAKE_CURRENT_SOURCE_DIR}/${NAME}/metadata/*.json")
    if(_meta)
        file(COPY ${_meta} DESTINATION "${EPOCH_METADATA_DIR}/${NAME}")
    endif()
endfunction()

# Each package is one line:
epoch_package(lines)
epoch_package(bars)
epoch_package(scatter)
epoch_package(tables)
epoch_package(cards)
epoch_package(heatmaps)
epoch_package(distributions)
epoch_package(smc)
epoch_package(portfolio_allocation)
epoch_package(execution)
epoch_package(econometrics)
epoch_package(machine_learning)
epoch_package(macroeconomics)
epoch_package(fundamental)
epoch_package(news)
epoch_package(corporate_events)
epoch_package(market_data)
epoch_package(sessions)
epoch_package(nlp)
epoch_package(compute)

# Global skills (not package-bound)
file(GLOB _global_skills "${CMAKE_CURRENT_SOURCE_DIR}/../global_skills/*.md")
file(COPY ${_global_skills} DESTINATION "${EPOCH_SKILLS_DIR}/global")

target_compile_definitions(epoch_script PUBLIC
    EPOCH_SKILLS_DIR="${EPOCH_SKILLS_DIR}"
    EPOCH_METADATA_DIR="${EPOCH_METADATA_DIR}"
)
```

**Deliverables:**
- All 339 skills co-located with their package implementations
- `build/bin/skills/` has complete skill tree
- EpochAI can read from collected directory (or keep local copy during transition)

**Verification:**
- `ls -R build/bin/skills/` — all 339 files present
- Skill counts per package match audit
- EpochAI skill search still functional (reads from new path)

---

### Sprint 5: Agent Tool — `import_package`

**Scope**: Add `import_package(PackageEnum)` tool to EpochAI study agent v3. Package enum values available in agent context.

**Changes to EpochAI:**

1. **Package registry** — new file listing all packages with descriptions:
   ```python
   PACKAGES = {
       "Lines": {"desc": "Line charts: xy_lines, cs_lines, timeseries_lines, labeled variants", "transforms": [...]},
       "SMC": {"desc": "Smart Money Concepts: BOS/CHoCH, FVG, order blocks, liquidity", "transforms": [...]},
       ...
   }
   ```

2. **`import_package` tool** — loads from collected skills + metadata:
   ```python
   def import_package(package: str) -> dict:
       # Load all transform full signatures for this package
       transforms = load_transforms_by_package(package)
       # Load all skills from build/bin/skills/packages/<name>/
       skills = load_skills_for_package(package)
       # Bundle dependent schemas
       schemas = resolve_schemas(transforms)
       return {"transforms": transforms, "skills": skills, "schemas": schemas}
   ```

3. **Update catalog_builder.py** — package registry replaces flat catalog:
   ```python
   # Before: flat list of all transforms with options-only
   # After: package registry with 1-line descriptions per package
   ```

4. **Update v3 prompt** — add package awareness:
   - Package registry in context (20 entries with descriptions)
   - `import_package` tool documentation
   - Updated workflow: "identify needed packages → import → build"

**Deliverables:**
- Agent can call `import_package("Lines")` and get full transform specs + 28 skills + schemas
- Package registry in context replaces or supplements flat catalog
- Freeform `search` still available as fallback

**Verification:**
- Manual test: ask agent to build a line chart study → observes it calls `import_package("Lines")`
- Verify loaded context contains exact transforms + skills from audit
- Compare agent output quality before/after

---

### Sprint 6: Cleanup + Deprecation

**Scope**: Remove duplicated skills from EpochAI. Deprecate flat component dirs if all moved. Update docs.

- Remove `EpochAI/agent_src/prompts/skills/` (now in epoch-script)
- Update `SkillsSearchService` to read from collected output
- Remove old component dirs (if fully migrated)
- Update `CLAUDE.md` and related docs
- Update `/dump-metadata` skill to also collect skills

---

## Full Audit: Transform → Package Assignment

### Package: Inbuilt (100+ transforms)
All tulip indicators, all candlestick patterns, crossover/crossunder, all `internalUse=true` (operators, scalars, casts, selects, arithmetic, lag/ffill variants).

### Package: Lines (5 transforms)
`xy_lines`, `cs_lines`, `timeseries_lines`, `labeled_lines`, `cs_labeled_lines`
Source: `reports/lines.h`, `reports/labeled_lines.h`

### Package: Bars (4 transforms)
`xy_bars`, `cs_bars`, `histogram`, `cs_histogram`
Source: `reports/bars.h`, `reports/histogram.h`

### Package: Scatter (8 transforms)
`xy_scatter`, `cs_scatter`, `labeled_scatter`, `cs_labeled_scatter`, `bubble`, `cs_bubble`, `labeled_bubble`, `cs_labeled_bubble`
Source: `reports/scatter.h`, `reports/labeled_scatter.h`, `reports/bubble.h`, `reports/labeled_bubble.h`

### Package: Tables (4 transforms)
`summary_table`, `cs_summary_table`, `detailed_table`, `cs_detailed_table`
Source: `reports/table.h`

### Package: Cards (6 transforms)
`cards`, `cs_cards`, `gauge`, `cs_gauge`, `pie`, `cs_pie`
Source: `reports/table.h`, `reports/gauge.h`, `reports/pie.h`

### Package: Heatmaps (2 transforms)
`heatmap`, `cs_heatmap`
Source: `reports/heatmap.h`

### Package: Distributions (3 transforms)
`boxplot`, `cs_boxplot`, `bellcurve`
Source: `reports/boxplot.h`

### Package: SMC (7 transforms)
`bos_choch`, `fair_value_gap`, `order_blocks`, `liquidity`, `swing_highs_lows`, `retracements`, `previous_high_low`
Source: `price_actions/smc/`

### Package: PortfolioAllocation (12 transforms)
`equal_weight`, `inv_vol_weight`, `risk_parity`, `risk_budgeting`, `hrp`, `herc`, `min_variance`, `max_sharpe`, `max_diversification`, `min_cvar`, `min_semivariance`, `black_litterman`
Source: `weight_allocators/`

### Package: Execution (11 transforms)
`long_and_short_zone`, `stop_loss`, `take_profit`, `trailing_stop`, `risk_unit`, `position_size`, `cppi`, `tipp`, `kelly`, `optimal_f`, `rollover_policy`
Source: `executors/`

### Package: Econometrics (12 transforms)
`engle_granger`, `johansen`, `rolling_adf`, `rolling_arima`, `kalman_filter`, `multi_linear_fit`, `rolling_garch`, `frac_diff`, `half_life_ar1`, `linear_fit`, `finance_ratio`, `cs_factor_analysis`
Source: `hosseinmoein/statistics/`, `timeseries/`, `statistics/`

### Package: MachineLearning (13 transforms)
`lightgbm_classifier`, `lightgbm_regressor`, `logistic_l1`, `logistic_l2`, `svr_l1`, `svr_l2`, `ml_zscore`, `ml_minmax`, `ml_robust`, `kmeans`, `dbscan`, `hmm`, `pca`
Source: `ml/`

### Package: Macroeconomics (5 transforms)
`economic_indicators`, `common_indicators`, `economic_calendar`, `economic_revisions`, `common_treasury_auctions`
Source: `data_sources/`

### Package: Fundamental (6 transforms)
`earnings`, `analyst_ratings`, `dividends`, `income_statement`, `balance_sheet`, `cash_flow`
Source: `data_sources/`

### Package: News (2 transforms)
`news`, `cs_news`
Source: `data_sources/`

### Package: CorporateEvents (5 transforms)
`ipos`, `short_interest`, `short_volume`, `splits`, `ticker_events`
Source: `data_sources/`

### Package: MarketData (16 transforms)
`market_data_source`, `extended_market_data_source`, `reference_stocks`, `common_reference_stocks`, `reference_futures`, `common_reference_futures`, `fx_pairs`, `common_fx_pairs`, `indices`, `common_indices`, `crypto_pairs`, `common_crypto_pairs`, `futures_continuation`, `downsample`, `upsample`, `upsample_by_interpolate`
Source: `data_sources/`, `utility/`

### Package: Sessions (9 transforms)
`session_window`, `session_gap`, `holiday`, `is_period_boundary`, `turn_of_month`, `day_of_week`, `month_of_year`, `quarter`, `week_of_month`
Source: `calendar/`, `indicators/`

### Package: NLP (8 transforms)
`keyword_match`, `keyword_count`, `keyword_score`, `topic_classify`, `string_case`, `string_trim`, `string_contains`, `string_check`
Source: `nlp/`, `string/`

### Package: Compute (catch-all, ~50+ transforms)
`ma`, `vidya`, `returns`, `forward_returns`, `cumulative`, `arg_min`, `arg_max`, `arg_minmax`, `rolling_corr`, `rolling_cov`, `ewm_corr`, `ewm_cov`, `beta`, `zscore`, `winsorize`, `percentrank`, `hurst_exponent`, `rolling_hurst_exponent`, `streak_length`, `nlargest`, `nsmallest`, `barssince`, `valuewhen`, `rising`, `falling`, `highestbars`, `lowestbars`, `hold_until`, `calendar_shift`, `basic_volatility`, `volatility_estimator`, `cusum`, `bar_gap`, `intraday_returns`, `price_profile`, `supertrend`, `chandelier_exit`, `price_distance`, `cs_zscore`, `cs_winsorize`, `cs_rank`, `cs_rank_quantile`, `cs_select`, `cs_momentum`, `cs_agg`, `cs_quantile`, `cs_weighted_mean`, `cs_first_last`, `event_marker`, `is_asset_ref`, `asset_spec`, `datetime_extract`, `datetime_diff`, `index`, `pivot_longer`, `vwap`, `trade_count`, `adosc`, `kvo`, `vosc`, `bband_percent`, `bband_width`
Source: multiple component dirs

**Note**: Many Compute transforms migrate to Inbuilt during Phase 0-5. Compute is the "stdlib extension."
