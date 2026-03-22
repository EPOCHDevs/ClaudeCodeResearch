# Claude Code Research Workspace

Quantitative research and strategy development workspace for Epoch.

---

## Exhibit A Quality Standard

All research definitions must follow the Exhibit A (EA) chart quality standard. Before writing or reviewing any definition, consult these references:

| Document | Path | Purpose |
|----------|------|---------|
| **Style Guide** | `exhibit_a_research/EXHIBIT_A_STYLE_GUIDE.md` | Chart type vocabulary, color palette, EpochScript patterns, design principles |
| **Antipatterns** | `exhibit_a_research/ANTIPATTERNS.md` | 11 documented mistakes with BAD/GOOD examples and EA fixes |

### Core Principles (from EA)

1. **One chart, one insight** — every definition answers ONE question
2. **Blue monochromatic palette** — `Color.Blue` primary, `Color.Gray` secondary, 3 colors max
3. **Annotation-driven** — `data_labels=True` on all bar charts, reference lines for context
4. **Question-framed titles** — titles answer "so what?", not describe the data type
5. **2-3 charts max per definition** — bar (snapshot) + line (timing) is the ideal pair
6. **Cards must earn their space** — only add cards that show information no chart already displays

### EA Quality Checklist

Before submitting any definition:

- [ ] Can you state the ONE question this answers?
- [ ] 3 charts or fewer?
- [ ] `Color.Blue` is primary on every chart?
- [ ] `data_labels=True` on every bar chart?
- [ ] Reference lines on every chart (zero line, average, median)?
- [ ] Title hints at the answer, not the data type?
- [ ] No redundancy between charts/cards?
- [ ] 3 series max per chart?
- [ ] Cards show something charts don't already display?

---

## Research Workflow

Research sources are cataloged in `research.csv` and stored in `report_notes/`. Two skills handle the workflow:

| Phase | Skill | Purpose |
|-------|-------|---------|
| **1. Collect** | `/research-topic` | Crawl sources for a topic using Exa |
| **2. Evaluate** | `/research-evaluate` | Analyze source, create Linear issue |
| **3. Implement** | `/research-implement` | Build definition, run study |

### research.csv Columns

| Column | Description |
|--------|-------------|
| `id` | Unique ID (RS-001, RS-002, ...) |
| `topic` | Topic folder name |
| `name` | Source title |
| `url` | Original source URL |
| `domain` | Source category (academic, quantpedia, etc.) |
| `file_path` | Path to markdown file |
| `status` | PENDING → TODO → IN_PROGRESS → COMPLETED |
| `linear_issue` | Linked Linear issue |
| `charts` | Number of charts |
| `tables` | Number of tables |
| `hypothesis` | Key research question |
| `keywords` | Search keywords |

### Quick Commands

```bash
# Collect sources for a new topic
/research-topic "momentum factor investing"

# Evaluate a specific source and create issue
/research-evaluate RS-006
/research-evaluate "mean reversion currencies"

# Implement research study from issue
/research-implement ENG-XXX
```

---

## Quantpedia Strategy Implementation

The Quantpedia workflow is focused **solely on strategy building and backtesting**. Research and idea discovery are handled separately.

### Workflow Overview

| Phase | Tool/Skill | Purpose |
|-------|------------|---------|
| **1. Evaluate** | `/quantpedia-evaluate` | Assess strategy eligibility, create Linear issue |
| **2. Implement** | `/quantpedia-implement` | Build strategy definition, run backtest |
| **3. Review** | `/review` | Address review comments, iterate |
| **4. Approve** | `/approve` | Move to DONE/TESTED status |

### What Quantpedia Tools Do

- Parse strategy rules from Quantpedia pages
- Build EpochScript definitions (triggers, positions, exits)
- Configure backtests with appropriate parameters
- Run `/run-job-data` to execute studies
- Analyze tearsheet results via `/study-reports`
- Track progress through Linear issue lifecycle

### What Quantpedia Tools Do NOT Do

- **No research** - Strategy ideas come from external sources (Quantpedia site, papers, etc.)
- **No data exploration** - Use `/query-study` for SQL queries on study data
- **No arbitrary browsing** - Only fetch specific strategy pages when implementing

### Strategy Lifecycle (Linear States)

```
ELIGIBLE → Todo → In Progress → In Review → Done/Tested
    ↑                              ↓
    └──────── (if rejected) ───────┘
```

### Quick Commands

```bash
# Evaluate a new strategy for eligibility
/quantpedia-evaluate <quantpedia-url>

# Implement an eligible strategy (provide Linear issue ID)
/quantpedia-implement ENG-XXX

# Review implementation based on comments
/review ENG-XXX

# Approve and close the issue
/approve ENG-XXX
```

---

## Python Environment Setup

```bash
cd /home/adesola/EpochDev/ClaudeCodeResearch
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Dependencies:**
- `pyarrow` - Read Arrow IPC files
- `pandas` - DataFrame operations
- `duckdb` - SQL queries on DataFrames
- `protobuf` - Parse tearsheet.pb files

**Optional (for pyfolio comparison):**
```bash
pip install pyfolio-reloaded empyrical-reloaded
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/dump-metadata` | Refresh all docs (schemas, transforms, grammars) |
| `/build-job-data [--asan]` | Build generate_job_data binary |
| `/run-job-data <def.json> [options]` | Execute a study definition |
| `/epochai-chat <def.json>` | Start EpochAI conversation with definition context |
| `/research-topic <topic>` | Crawl sources for a research topic |
| `/research-evaluate <id/query>` | Evaluate research source, create Linear issue |
| `/research-implement <issue>` | Build definition and run research study |
| `/publish-research <name>` | Publish EpochScript template to definition + manifest |
| `/quantpedia-evaluate <url>` | Evaluate Quantpedia strategy for eligibility |
| `/quantpedia-implement <issue>` | Implement strategy from ELIGIBLE to IN_REVIEW |
| `/review <issue>` | Review Linear issue, address comments |
| `/approve <issue>` | Approve issue and move to DONE |
| `/query-study <job> [sql]` | Query study dataframes with SQL |
| `/study-reports <job>` | Get tearsheets, cards, charts from executed studies |

### /dump-metadata

Rebuilds server, generates grammars, fetches all documentation to `docs/`:
- `schemas.json`, `transform_metadata.json`, `assets.json`, `index_constituents.json`
- `epochscript.ebnf`, `script_grammar.txt`
- `overview.md`, `execution_guide.md`, `timeframe_guide.md`

### /build-job-data

```bash
/build-job-data              # Release build
/build-job-data --asan       # Debug with AddressSanitizer
/build-job-data -j4          # Limit to 4 parallel jobs
/build-job-data --asan -j8   # ASAN build with 8 jobs
```

---

## C++ Testing

Run Catch3 unit tests using `cpp_tools/run_tests.sh`. Builds with **ASAN by default**.

### Quick Usage

```bash
# Run single test (builds with ASAN)
./cpp_tools/run_tests.sh epoch_frame_test

# Run multiple tests
./cpp_tools/run_tests.sh epoch_frame_test epoch_script_test

# Use release build instead of ASAN
./cpp_tools/run_tests.sh --release epoch_trading_test

# Limit parallel build jobs
./cpp_tools/run_tests.sh -j4 epoch_frame_test

# Skip build, just run existing executable
./cpp_tools/run_tests.sh --no-build epoch_empyrical_test

# List available test targets
./cpp_tools/run_tests.sh --list
```

### Passing Catch3 Arguments

Use `--` to pass arguments to the Catch3 test executable:

```bash
# List all test cases
./cpp_tools/run_tests.sh epoch_frame_test -- --list-tests

# Run tests with specific tag
./cpp_tools/run_tests.sh epoch_frame_test -- "[datetime]"

# Show successful tests
./cpp_tools/run_tests.sh epoch_frame_test -- -s

# Run specific test by name
./cpp_tools/run_tests.sh epoch_frame_test -- "Test Max Drawdown"
```

### Available Test Targets

| Target | Description |
|--------|-------------|
| `epoch_frame_test` | DataFrame, index, date/time tests |
| `epoch_frame_cal_test` | Calendar tests |
| `epoch_script_test` | EpochScript parser/compiler tests |
| `epoch_script_test_runtime` | Script runtime tests |
| `epoch_script_test_metadata` | Script metadata tests |
| `epoch_script_test_ml` | Machine learning script tests |
| `epoch_trading_test` | Trading engine tests |
| `epoch_stratifyx_test` | Strategy execution tests |
| `epoch_stratifyx_integration_test` | Integration tests |
| `epoch_stratifyx_pipeline_integration_test` | Pipeline integration tests |
| `epoch_stratifyx_service_test` | Service layer tests |
| `epoch_empyrical_test` | Performance metrics tests |
| `epoch_folio_test` | Portfolio analytics tests |
| `epoch_dashboard_test` | Dashboard tests |
| `epoch_data_sdk_test` | Data SDK tests |
| `epoch_events_test` | Event system tests |

### Build Locking

The script uses file locking to prevent concurrent builds. If another build is running, it will wait automatically.

---

### /run-job-data

```bash
# Research study
/run-job-data "path/to/definition.json" --start 2023-01-01 --end 2023-12-31

# Trading campaign
/run-job-data "path/to/definition.json" --cash 100000

# Debug mode
/run-job-data --asan "path/to/definition.json" --cash 100000
```

### /epochai-chat

Start an EpochAI conversation using a definition as the foundation. Claude Code acts as your research assistant, drafting messages for you to copy/paste to EpochAI.

```bash
# Start chat with a research definition
/epochai-chat project/definitions/test_runner/momentum_asset_allocation_research.json

# Start chat with a strategy definition
/epochai-chat project/definitions/test_runner/asset_class_trend_following_strategy.json
```

**Workflow:**
1. Claude Code loads the definition and finds matching reference notes
2. Creates a session file in `workflows/` to track the conversation
3. Drafts conversational messages for you to send to EpochAI
4. You copy/paste responses back (or share screenshots)
5. Claude Code analyzes responses and suggests next actions

**Session Files:** Saved to `workflows/epochai_YYYY-MM-DD_HHMMSS.md`

See `workflows/epochai-chat-workflow.md` for full documentation.

---

## Analysis Scripts

Located in `analyze_job/`. Requires Python venv (see setup above).

**Preferred:** Use slash commands instead of running scripts directly:
- `/query-study` - SQL queries on study data
- `/study-reports` - Tearsheet analysis

### query_study_dataframes.py

**Purpose:** Query Arrow data from executed studies using SQL (DuckDB).

**Slash command:** `/query-study <job_folder> [sql_query]`

**When to use:**
- Inspect market data, orders, positions, account tables
- Analyze null values in computed columns
- Run custom SQL queries for debugging
- Interactive exploration of study data

```bash
# List all available tables
python analyze_job/query_study_dataframes.py <job_folder> --tables

# Show table schema
python analyze_job/query_study_dataframes.py <job_folder> --schema <table_name>

# Analyze null values across all tables
python analyze_job/query_study_dataframes.py <job_folder> --nulls

# Execute SQL query
python analyze_job/query_study_dataframes.py <job_folder> -q "SELECT * FROM orders LIMIT 10"

# Interactive SQL mode
python analyze_job/query_study_dataframes.py <job_folder> -i
```

**Available tables:**
- `market_data_1d_<asset>` - OHLCV + computed transforms
- `event_marker_<asset>_N` - Event markers (round trips, signals)
- `orders` - Order history (campaigns only)
- `positions` - Position snapshots (campaigns only)
- `account` - Account equity/cash (campaigns only)

### get_study_reports.py

**Purpose:** Parse and display tearsheet protobuf reports.

**Slash command:** `/study-reports <job_folder>`

**When to use:**
- View card metrics (Sharpe, Max Drawdown, Win Rate, etc.)
- List available charts and their configurations
- Inspect table data from reports
- Validate tearsheet generation

```bash
# Full summary of all tearsheets
python analyze_job/get_study_reports.py <job_folder>

# Cards only (key metrics)
python analyze_job/get_study_reports.py <job_folder> --cards

# Charts only
python analyze_job/get_study_reports.py <job_folder> --charts

# Tables only
python analyze_job/get_study_reports.py <job_folder> --tables

# Filter by category (asset)
python analyze_job/get_study_reports.py <job_folder> -c SPY-Stocks

# Verbose output
python analyze_job/get_study_reports.py <job_folder> --verbose
```

### compare_with_pyfolio.py

**Purpose:** Validate epoch-folio metrics against pyfolio/empyrical.

**When to use:**
- Verify Sharpe ratio, Sortino, Max Drawdown calculations
- Cross-validate tearsheet metrics with industry-standard library
- Debug discrepancies in performance metrics

**Requires:** `pip install pyfolio-reloaded empyrical-reloaded`

```bash
python analyze_job/compare_with_pyfolio.py <job_name>
```

**Compares:**
- Annual/cumulative returns
- Sharpe ratio
- Sortino ratio
- Max drawdown
- Calmar ratio
- Win rate

---

## Linear Issue Tracking

All issues are tracked in Linear using the MCP integration.

### IMPORTANT: One Issue Per Work Item

**NEVER create separate issues for the same work item.** Use a single issue to track the entire lifecycle:

- **Wrong:** ENG-10 "Implement Strategy X" + ENG-12 "Strategy X Ready for Review"
- **Correct:** Single issue "Implement Strategy X" → update status from Todo → In Progress → In Review → Done

**Why this matters:**
- Keeps all context, comments, and history in one place
- Easier to track progress and find information
- Avoids confusion about which issue to update
- Prevents orphaned/duplicate issues

**When working on existing issues:**
1. Search Linear first to find related issues before creating new ones
2. Update the existing issue's status and add comments for progress
3. Only create a new issue if it's genuinely different work

### Quick Reference IDs

| Resource | ID |
|----------|-----|
| **Team: Engineering** | `53f03fc6-d769-481a-b0f6-f7d6f8ab8085` |
| **Project: Platform Development** | `101a9b28-b0f7-4b8f-b703-b50a62fd383a` |
| **Project: Quantitative Research** | `aedc87b9-3cee-4bdb-95ef-ac3d49e1218f` |

### Labels

| Label | ID | Use For |
|-------|-----|---------|
| **Bug** | `908a7dc7-f075-4c89-b637-ae3b14e39566` | Something broken, errors, crashes |
| **Feature** | `e742d72c-2d58-4bbf-aa84-3165dd17dc4e` | New functionality |
| **Improvement** | `10d99707-964a-4112-bac2-ed87d8866118` | Enhancements to existing features |
| **UI component development** | `d6ec6631-0d00-46f4-9d0b-579419925673` | Frontend/UI work |

### Priority Levels

| Priority | Value | Use For |
|----------|-------|---------|
| Urgent | `1` | Blocking issues, production down |
| High | `2` | Important bugs, critical features |
| Normal | `3` | Standard work items |
| Low | `4` | Nice to have, backlog items |

### Workflow States

| State | ID | Type |
|-------|-----|------|
| Backlog | `243bc62f-21be-46a3-a0ed-86f8535c6b88` | backlog |
| Todo | `6727aad3-ba80-47b3-b578-e530fc896081` | unstarted |
| In Progress | `49c7285c-33c4-443c-a0af-49b51b8e1739` | started |
| In Review | `e93bf93b-77e3-41bb-afbd-5b76f8194653` | started |
| Done | `52ea8ebd-76aa-4b55-b049-70bd327c89db` | completed |
| Canceled | `35205496-6697-4f15-b81f-1db572aa7211` | canceled |
| Duplicate | `4200d518-da49-4464-8ec9-85338100c563` | canceled |

---

## Creating Issues

### Report a Bug

```
mcp__linear__linear_createIssue

teamId: "53f03fc6-d769-481a-b0f6-f7d6f8ab8085"
projectId: "101a9b28-b0f7-4b8f-b703-b50a62fd383a"
labelIds: ["908a7dc7-f075-4c89-b637-ae3b14e39566"]
priority: 2
title: "Brief description of the bug"
description: |
  ## Summary
  What's broken and what's the impact.

  ## Steps to Reproduce
  1. Step one
  2. Step two
  3. Step three

  ## Expected Behavior
  What should happen.

  ## Actual Behavior
  What happens instead.

  ## Environment
  - Files affected: `path/to/file.cpp`
  - Build: release / asan
  - Date first noticed: YYYY-MM-DD

  ## Workaround
  Any temporary fix (if known).
```

### Request a Feature

```
mcp__linear__linear_createIssue

teamId: "53f03fc6-d769-481a-b0f6-f7d6f8ab8085"
projectId: "101a9b28-b0f7-4b8f-b703-b50a62fd383a"
labelIds: ["e742d72c-2d58-4bbf-aa84-3165dd17dc4e"]
priority: 3
title: "Brief description of the feature"
description: |
  ## Summary
  What feature is needed and why.

  ## Use Case
  Describe the problem this solves.

  ## Proposed Solution
  How it could work (API, behavior, etc.)

  ## Alternatives Considered
  Other approaches and why they're less ideal.

  ## Acceptance Criteria
  - [ ] Criterion 1
  - [ ] Criterion 2
```

### Request an Improvement

```
mcp__linear__linear_createIssue

teamId: "53f03fc6-d769-481a-b0f6-f7d6f8ab8085"
projectId: "101a9b28-b0f7-4b8f-b703-b50a62fd383a"
labelIds: ["10d99707-964a-4112-bac2-ed87d8866118"]
priority: 3
title: "Brief description of the improvement"
description: |
  ## Summary
  What existing feature needs improvement.

  ## Current Behavior
  How it works now.

  ## Proposed Improvement
  How it should work better.

  ## Benefits
  Why this matters.
```

### Create Research Task

For quantitative research tasks, use the Quantitative Research project:

```
mcp__linear__linear_createIssue

teamId: "53f03fc6-d769-481a-b0f6-f7d6f8ab8085"
projectId: "aedc87b9-3cee-4bdb-95ef-ac3d49e1218f"
priority: 3
title: "Research: [Strategy/Analysis Name]"
description: |
  ## Hypothesis
  What we expect to find.

  ## Approach
  - Data sources
  - Methodology
  - Time period

  ## Success Criteria
  How we'll know if the research is valid.

  ## References
  - Papers, Quantpedia links, etc.
```

---

## Updating Issues

### Change Status

```
mcp__linear__linear_updateIssue

id: "ISSUE-ID"
stateId: "49c7285c-33c4-443c-a0af-49b51b8e1739"  # In Progress
```

### Add Comment

```
mcp__linear__linear_createComment

issueId: "ISSUE-ID"
body: "Update on progress..."
```

### Set Priority

```
mcp__linear__linear_setIssuePriority

issueId: "ISSUE-ID"
priority: 2  # High
```

---

## Playwright Browser Handling

Use the Playwright MCP for web browsing (Quantpedia, documentation, etc.).

### Quantpedia Access Policy

**Strategy Implementation Only:** Only access Quantpedia to fetch specific strategy pages during `/quantpedia-implement`. Do not use for:
- Research or idea discovery
- Browsing strategy lists
- Exploring unrelated content

For research, use the `/research-topic` skill which uses Exa for web crawling.

### Credentials

Quantpedia login credentials are stored in `.env`:
```
QUANTPEDIA_EMAIL=epochfinllc@gmail.com
QUANTPEDIA_PASSWORD=FREEword123@
```

### Browser Session Management

**IMPORTANT: Use tabs, don't kill Chrome!**

If a Playwright session is already active, use tabs instead of killing the browser:

```python
# List open tabs
mcp__playwright__browser_tabs(action="list")

# Open new tab
mcp__playwright__browser_tabs(action="new")

# Switch to tab by index
mcp__playwright__browser_tabs(action="select", index=0)

# Close current tab
mcp__playwright__browser_tabs(action="close")

# Navigate in current tab
mcp__playwright__browser_navigate(url="https://quantpedia.com/...")
```

**Only kill Chrome when:**
- Browser was opened manually by user (separate process)
- Playwright session was lost/expired
- Error: "Opening in existing browser session"

```bash
# Last resort - kill and restart
pkill -9 chrome; sleep 2
```

### Common Operations

```python
# Take snapshot (better than screenshot for interactions)
mcp__playwright__browser_snapshot()

# Click element
mcp__playwright__browser_click(ref="e123", element="Button name")

# Fill form
mcp__playwright__browser_type(ref="e456", text="input text")

# Select dropdown
mcp__playwright__browser_select_option(ref="e789", values=["option"])
```

STUDY GENERATION INSTURCTION+GRAMAMR
in STUDY_GEN_PROMPT.md