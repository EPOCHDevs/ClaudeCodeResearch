---
name: publish-research
description: Publish an EpochScript template (research or strategy) to a project definition and manifest entry.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
argument-hint: "<script_name> [--type research|strategy] [--assets ASSET1,ASSET2] [--timeframe 1D|1Min] [--project project]"
---

# Publish Research / Strategy

Copy an EpochScript template into a runnable JSON definition and add/update its manifest entry.
Supports both **research** (analysis/charts only) and **strategy** (trading/backtesting) templates.

## Usage

```bash
# Publish research (default type)
/publish-research audnzd_macro_fair_value

# Publish strategy
/publish-research asset_class_trend_following --type strategy

# With explicit assets and timeframe
/publish-research audnzd_macro_fair_value --assets AUDNZD-FX --timeframe 1D

# Target a different project folder (default: project)
/publish-research audnzd_macro_fair_value --project futures-project
```

## Type Detection

If `--type` is not specified, auto-detect:
1. Check if `ScriptTemplates/research/<name>.epochscript` exists → research
2. Check if `ScriptTemplates/strategy/<name>.epochscript` exists → strategy
3. If neither exists, report error and stop

## Research vs Strategy Differences

| Aspect | Research | Strategy |
|--------|----------|----------|
| Source dir | `ScriptTemplates/research/` | `ScriptTemplates/strategy/` |
| Manifest | `ScriptTemplates/research/manifest.json` | `ScriptTemplates/strategy/manifest.json` |
| Definition suffix | `_research.json` | `_strategy.json` |
| JSON `name` | kebab-case (`audnzd-macro-fair-value`) | Human-readable title (`Asset Class Trend-Following Strategy`) |
| `data.cache_dir` | Present (`<project>/market_data`) | Omitted |

## Workflow

### Step 1: Locate the EpochScript Source

Based on type, the source file lives at:
```
/home/adesola/EpochDev/ScriptTemplates/<type>/<script_name>.epochscript
```

Read the file. If it doesn't exist, report an error and stop.

### Step 2: Parse Arguments & Infer Metadata

From the arguments or by inspecting the EpochScript source:

- **`script_name`** (required): The base name without extension (e.g. `audnzd_macro_fair_value`)
- **`--type`**: `research` (default) or `strategy`. Auto-detected if omitted.
- **`--assets`**: Comma-separated asset list. If not provided, infer from `market_data_source()` context or comments in the script. Common patterns:
  - FX pairs: `AUDNZD-FX`, `EURUSD-FX`
  - Equities: `SPY-Stocks`, `AAPL-Stocks`
  - Futures: `ES-Futures`, `GC-Futures`
- **`--timeframe`**: `1D` (default) or `1Min`
- **`--project`**: Target project folder (default: `project`)

**Naming conventions:**
- **Research**: Definition name = kebab-case (`audnzd-macro-fair-value`), filename = `<name>_research.json`
- **Strategy**: Definition name = human-readable from script title comment, filename = `<name>_strategy.json`
- Manifest ID (both): `<script_name>` (underscore form)

### Step 3: Create JSON Definition

Write to: `<project>/definitions/test_runner/<script_name>_<type>.json`

**Research definition:**
```json
{
   "name": "<kebab-case-name>",
   "description": "<extracted from script header comments>",
   "data": {
      "assets": ["<ASSET-TICKER>"],
      "source": "polygon",
      "cache_dir": "/home/adesola/EpochDev/ClaudeCodeResearch/<project>/market_data"
   },
   "source": "<epochscript source>",
   "global_timeframe": "<1D or 1Min>"
}
```

**Strategy definition:**
```json
{
   "name": "<Human-Readable Strategy Name>",
   "description": "<extracted from script header comments>",
   "data": {
      "assets": ["<ASSET1>", "<ASSET2>"],
      "source": "polygon"
   },
   "source": "<epochscript source>",
   "global_timeframe": "<1D or 1Min>"
}
```

**How to build the `source` field:**
Read the raw EpochScript file content. Use Python to safely embed and serialize:

```bash
python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    source = f.read()
defn = {
    'name': sys.argv[2],
    'description': sys.argv[3],
    'data': {
        'assets': sys.argv[4].split(','),
        'source': 'polygon',
    },
    'source': source,
    'global_timeframe': sys.argv[5]
}
# Add cache_dir for research only
if sys.argv[6] == 'research':
    defn['data']['cache_dir'] = sys.argv[7]
with open(sys.argv[8], 'w') as f:
    json.dump(defn, f, indent=3, ensure_ascii=False)
    f.write('\n')
" <source_path> <name> <description> <assets> <timeframe> <type> <cache_dir> <output_path>
```

### Step 4: Add/Update Manifest Entry

Manifest file: `/home/adesola/EpochDev/ScriptTemplates/<type>/manifest.json`

Check if an entry with the same `id` already exists:
- **Exists**: Update name, description, and tags in place
- **New**: Append before the closing `]`

**Manifest entry structure:**
```json
{
  "id": "<script_name>",
  "name": "<Human-readable name>",
  "description": "<LOAD/COMPUTE/DASHBOARD style description from header>",
  "tags": {
    "asset_class": ["fx"|"equities"|"futures"|"crypto"|"multi_asset"],
    "data_source": ["<data sources used>"],
    "methodology": ["<techniques used>"],
    "intraday": false
  }
}
```

**Tag inference rules:**
- `asset_class`: From asset ticker suffix (`-FX` → fx, `-Stocks` → equities, `-Futures` → futures)
- `data_source`: From transforms used (`common_economic_indicators`, `economic_indicators`, `analyst_ratings`, `earnings`, `market_data_source`, `technicals`)
- `methodology`: From transforms used (`pca`, `rolling_regression`, `zscore`, `event_study`, `seasonal_analysis`, `fair_value_model`, `trend_following`, `momentum`, `mean_reversion`, etc.)
- `intraday`: `true` if timeframe is `1Min` or `5Min`, `false` otherwise

### Step 5: Verify

1. Validate the JSON definition is syntactically correct:
```bash
python3 -c "import json; json.load(open('<output_path>'))"
```

2. Validate manifest.json is still valid JSON:
```bash
python3 -c "import json; d=json.load(open('<manifest_path>')); print(f'{len(d)} entries')"
```

3. Report what was created/updated:
   - Type (research/strategy)
   - Definition path
   - Manifest entry ID
   - Assets and timeframe used

## Notes

- The EpochScript source is embedded directly in the JSON `source` field
- Always use `polygon` as the data source
- Research definitions include `cache_dir`, strategy definitions do not
- If the definition file already exists, overwrite it (the source may have been updated)
- Do NOT run the study — use `/run-job-data` for that
