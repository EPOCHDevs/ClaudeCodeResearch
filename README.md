# Claude Code Research Workspace

Quantitative research and strategy development workspace for Epoch.

---

## Quantpedia Research Workflow

### Strategy Index

All Quantpedia strategies are tracked in `quantpedia_strategies.csv` (1276 strategies).

### Status Flow

```
OPENED → ELIGIBLE/INELIGIBLE → IN_PROGRESS → TESTED
            ↓           ↓
    [Linear Issue]  [Feature Request]
```

| Status | Meaning | Linear State | Action |
|--------|---------|--------------|--------|
| `OPENED` | Quantpedia researched, reference notes created | - | - |
| `ELIGIBLE` | Epoch can implement (transforms, assets, data available) | Todo | Create Linear issue |
| `INELIGIBLE` | Missing capability | Backlog | Create Linear feature request |
| `IN_PROGRESS` | Actively implementing | In Progress | Link definitions to issue |
| `TESTED` | Backtested & validated | Done | Close issue |

### Research Process

1. **Select Strategy** - Pick from `quantpedia_strategies.csv`
2. **Open & Study** - Navigate to Quantpedia page (use Playwright MCP for logged-in access)
3. **Extract & Save** - Create `reference_notes/{slug}/index.md` with:
   - Trading rules
   - Source paper (SSRN link)
   - QuantConnect code
   - Performance benchmarks
4. **Eligibility Check** - Verify against:
   - `docs/transform_metadata.json` - Required transforms available?
   - `docs/assets.json` - Required tickers available?
   - Data sources & timeframes
5. **Update Status** - Set ELIGIBLE or INELIGIBLE in CSV
6. **Create Linear Issue** - Document implementation plan or feature request

---

## EpochScript Best Practices

### Monthly Rebalancing

**Problem**: Ensuring trades only execute on the first trading day of each month.

**Solution**: Use `datetime_extract` + `rebalance_on` parameter.

```epochscript
# Detect first trading day of month
current_month = datetime_extract(component=DatetimeExtractionType.month)(index())
is_new_month = current_month != (current_month >> 1)

# Signals only trigger on month boundary
enter_long = is_new_month and <your_condition>
exit_long = is_new_month and not <your_condition>

# Hold position between rebalances
held_signal = hold_until()(enter=enter_long, exit=exit_long)

# CRITICAL: Restrict position changes to month start only
position_size(type="percent")(size=weights * 100, rebalance_on=is_new_month)
```

### Long-Short Strategies

**Key Constraint:** `position_size` only accepts positive values. Direction (long/short) is handled by `long_and_short_zone`.

```epochscript
# Cross-sectional selection
is_top_3 = cs_select(direction=CSSelectDirection.top, mode=CSSelectMode.count, k=3)(momentum)
is_bottom_3 = cs_select(direction=CSSelectDirection.bottom, mode=CSSelectMode.count, k=3)(momentum)

# Monthly rebalance signals for LONG positions
enter_long = is_new_month and is_top_3
exit_long = is_new_month and not is_top_3
held_long = hold_until()(enter=enter_long, exit=exit_long)

# Monthly rebalance signals for SHORT positions
enter_short = is_new_month and is_bottom_3
exit_short = is_new_month and not is_bottom_3
held_short = hold_until()(enter=enter_short, exit=exit_short)

# long_and_short_zone handles direction: +1 (long), -1 (short), 0 (flat)
long_and_short_zone()(long_entry=held_long, short_entry=held_short)

# Equal weight across ALL active positions (both long and short)
# position_size only takes magnitude; direction comes from long_and_short_zone
is_active = held_long or held_short
weights = equal_weight()(is_active)

# Size is always positive
position_size(type="percent")(size=weights * 100, rebalance_on=is_new_month)
```

**Common Mistake:** Using negative weights for shorts:
```epochscript
# WRONG - position_size rejects negative values
weights = long_weight - short_weight  # Creates negative weights for shorts
position_size(type="percent")(size=weights * 100)  # Fails!
```

### Key Patterns

| Pattern | Purpose |
|---------|---------|
| `>> 1` | Shift series by 1 bar (previous value) |
| `month != (month >> 1)` | Detect period boundary |
| `hold_until()(enter, exit)` | Maintain state between signals |
| `rebalance_on=` | Restrict when trades execute |
| `long_and_short_zone()` | Handle long/short direction |
| `is_active = long or short` | Combine masks for sizing |

### Rebalancing Periods

| Period | Component | Pattern |
|--------|-----------|---------|
| Weekly | `week` | `week != (week >> 1)` |
| Monthly | `month` | `month != (month >> 1)` |
| Quarterly | `quarter` | `quarter != (quarter >> 1)` |
| Yearly | `year` | `year != (year >> 1)` |

### Asset Naming Convention

Assets use format: `{TICKER}-{AssetClass}`

- `SPY-Stocks`
- `EFA-Stocks`
- `BTC-Crypto`
- `EURUSD-FX`

### Asset Universe Expansion

Use index IDs or exchange codes directly in the `assets` array - the system automatically expands them to constituent stocks.

#### Index Constituents

Curated lists of index members (see `docs/index_constituents.json`):

| Index ID | Constituents |
|----------|--------------|
| `SP500` | ~503 S&P 500 stocks |
| `RUSSELL1000` | ~1002 stocks |
| `RUSSELL2000` | ~1962 stocks |
| `NASDAQ100` | ~101 stocks |
| `DJIA30` | 30 Dow Jones stocks |

#### Exchange Universe

For academic research-style universe construction (Fama-French, etc.), use exchange codes to get all stocks on an exchange:

| Exchange | Stocks | Description |
|----------|--------|-------------|
| `NASDAQ` | 4,866 | NASDAQ Stock Market |
| `AMEX` | 3,401 | NYSE American (formerly AMEX) |
| `NYSE` | 2,935 | New York Stock Exchange |
| `XNAS` | 847 | NASDAQ (alternate code) |
| `XNYS` | 522 | NYSE (alternate code) |
| `ARCX` | 302 | NYSE Arca |
| `BATS` | 214 | BATS Global Markets |
| `XASE` | 58 | NYSE American (alternate code) |

#### Expansion Priority

```
Input: ["NYSE", "DJIA30", "AAPL-Stocks"]
         │         │           │
         ▼         ▼           ▼
   1. Check IndexConstituentsDatabase
      - "NYSE" not found → continue
      - "DJIA30" found → expand to 30 stocks
         │
         ▼
   2. Check ExchangeUniverseDatabase
      - "NYSE" found → expand to 2,935 stocks
         │
         ▼
   3. Treat as single asset
      - "AAPL-Stocks" → validate and add
         │
         ▼
   Output: 2,935 + 30 + 1 = 2,966 unique assets
```

#### Example: Index-Based Strategy

```json
{
   "data": {
      "assets": ["SP500"],
      "source": "polygon"
   }
}
```

#### Example: Exchange-Based (Fama-French Style)

```json
{
   "data": {
      "assets": ["NYSE", "AMEX", "NASDAQ"],
      "source": "polygon"
   }
}
```

This expands to ~11,200 stocks across all major US exchanges - useful for academic research requiring the full US equity universe.

### Example: Faber Asset Class Trend-Following

```epochscript
# Data source
src = market_data_source(timeframe=1D)()
close = src.c

# 210-day SMA (10 months * 21 trading days)
sma_210 = ma(period=210, type=MAType.sma)(close)
trend_up = close > sma_210

# Monthly rebalance detection
current_month = datetime_extract(component=DatetimeExtractionType.month)(index())
is_new_month = current_month != (current_month >> 1)

# Monthly signals with hold
enter_long = is_new_month and trend_up
exit_long = is_new_month and not trend_up
held_signal = hold_until()(enter=enter_long, exit=exit_long)

# Zones and weights
long_and_short_zone()(long_entry=held_signal, short_entry=False)
weights = equal_weight()(held_signal)

# Execute only on month start
position_size(type="percent")(size=weights * 100, rebalance_on=is_new_month)
```

---

## Directory Structure

```
ClaudeCodeResearch/
├── README.md                    # This file
├── CLAUDE.md                    # Claude instructions
├── quantpedia_strategies.csv    # Master strategy index (1276 strategies)
├── docs/
│   ├── transform_metadata.json  # Available transforms
│   ├── assets.json              # Available assets
│   ├── schemas.json             # Data schemas
│   └── best_practices.md        # EpochScript patterns
├── reference_notes/
│   └── {strategy_slug}/
│       └── index.md             # Per-strategy research notes
├── project/
│   ├── definitions/             # Study definitions
│   └── market_data/             # Cached market data
└── analyze_job/
    ├── query_study_dataframes.py
    └── get_study_reports.py
```

---

## Python Environment Setup

```bash
cd /home/adesola/EpochDev/ClaudeCodeResearch
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Dependencies:** pyarrow, pandas, duckdb, protobuf

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/dump-metadata` | Refresh docs (schemas, transforms, grammars) |
| `/build-job-data [--asan]` | Build generate_job_data binary |
| `/run-job-data <def.json> [options]` | Execute a study definition |
| `/query-study <job_folder> [options]` | SQL queries on study data |
| `/study-reports <job_folder> [options]` | View tearsheet metrics |

---

## Linear Issue Tracking

### Quick Reference IDs

| Resource | ID |
|----------|-----|
| **Team: Engineering** | `53f03fc6-d769-481a-b0f6-f7d6f8ab8085` |
| **Project: Platform Development** | `101a9b28-b0f7-4b8f-b703-b50a62fd383a` |
| **Project: Quantitative Research** | `aedc87b9-3cee-4bdb-95ef-ac3d49e1218f` |

### Labels

| Label | ID |
|-------|-----|
| Bug | `908a7dc7-f075-4c89-b637-ae3b14e39566` |
| Feature | `e742d72c-2d58-4bbf-aa84-3165dd17dc4e` |
| Improvement | `10d99707-964a-4112-bac2-ed87d8866118` |

### Strategy Implementation Issue Template

```markdown
## Quantpedia Reference
- ID: #XXXX
- URL: https://quantpedia.com/strategies/...
- Paper: SSRN XXXXXXX

## Implementation Plan
1. Research Study - Validate signal/hypothesis
2. Trading Strategy - Implement with backtest

## Eligibility Check
- [ ] Transforms available
- [ ] Assets available
- [ ] Data sources available

## Definitions
- [ ] {strategy}_research.json
- [ ] {strategy}_strategy.json
```

### Feature Request Template (INELIGIBLE)

```markdown
## Context
Trying to implement [Strategy Name] (#XXXX) but missing capability.

## Quantpedia Reference
- URL: https://quantpedia.com/strategies/...

## Required Feature
[Description of what's needed]

## Use Case
[How it would be used in the strategy]
```
