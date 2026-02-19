# Job Registry

Auto-discovers study definitions and manages run configurations. No manual scanning or syncing required — drop a definition JSON into the definitions folder and it appears automatically.

## Quick Start

```bash
# See everything
python scripts/job_registry.py list

# Run one study (partial match works)
python scripts/job_registry.py run fed_model

# Run all
python scripts/job_registry.py run-all

# Preview without executing
python scripts/job_registry.py run-all --dry-run
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List all definitions with run parameters |
| `show <id>` | Show full details and run command for a definition |
| `run <id>` | Execute a single definition |
| `run-all` | Execute all definitions |
| `validate` | Check definitions and config for issues |
| `clean` | Remove output folders |

## list

```bash
python scripts/job_registry.py list                  # All 36 definitions
python scripts/job_registry.py list --type campaign   # Strategies only (15)
python scripts/job_registry.py list --type research   # Research only (21)
```

## show

```bash
python scripts/job_registry.py show fed_model_strategy
python scripts/job_registry.py show fed_model          # Partial match works
```

## run

```bash
python scripts/job_registry.py run fed_model_strategy
python scripts/job_registry.py run fed_model --dry-run   # Preview only
python scripts/job_registry.py run fed_model --asan      # ASAN build
```

## run-all

```bash
python scripts/job_registry.py run-all                           # Everything
python scripts/job_registry.py run-all --type campaign            # All strategies
python scripts/job_registry.py run-all --type research            # All research
python scripts/job_registry.py run-all --dry-run                  # Preview commands
python scripts/job_registry.py run-all --asan                     # ASAN build
python scripts/job_registry.py run-all --stop-on-error            # Halt on first failure
python scripts/job_registry.py run-all --exclude id1 id2          # Skip specific definitions
```

## clean

```bash
python scripts/job_registry.py clean --dry-run            # Preview what would be deleted
python scripts/job_registry.py clean                      # Remove all output folders
python scripts/job_registry.py clean --orphans             # Only remove orphaned folders (no matching definition)
python scripts/job_registry.py clean --type research       # Only clean research output
python scripts/job_registry.py clean donchian              # Clean specific definition
```

## Run Configuration

Run parameters live in `scripts/run_config.json`:

```json
{
  "defaults": {
    "research": {
      "1D":   {"start": "2020-01-01", "end": "2024-12-31"},
      "1W":   {"start": "2010-01-01", "end": "2024-12-31"},
      "5Min": {"start": "2024-01-01", "end": "2025-01-01"},
      "1Min": {"start": "2024-06-01", "end": "2025-01-01"}
    },
    "campaign": {
      "cash": 100000
    }
  },
  "overrides": {
    "rs007_fx_monthly_seasonality_research": {"start": "2005-01-01", "end": "2024-12-31"}
  }
}
```

- **Research defaults** are grouped by timeframe — intraday studies get shorter windows automatically
- **Campaign default** is `$100,000` starting cash
- **Overrides** let you customize any definition by ID (start/end dates, cash amount)

## How It Works

- Definitions folder: `project/definitions/test_runner/*.json`
- Job type detected from filename: `*_strategy.json` = campaign, `*_research.json` = research
- Timeframe read from the definition's `global_timeframe` field
- Adding a new definition file = it auto-appears in the registry with sensible defaults
- No registry file to maintain — everything is live from the definitions folder
