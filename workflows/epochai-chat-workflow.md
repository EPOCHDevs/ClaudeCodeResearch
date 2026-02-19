# EpochAI Chat Workflow

This document describes the workflow for having Claude Code assist with EpochAI conversations.

## Overview

The `/epochai-chat` skill enables a collaborative workflow where:
1. You select a definition (strategy/research) you've created
2. Claude Code loads the definition and its reference notes
3. Claude Code drafts messages for you to send to EpochAI
4. You copy/paste responses back to Claude Code
5. Claude Code helps you navigate the conversation

## Why This Workflow?

- **Context Preservation**: Claude Code has full context of the definition and reference materials
- **Advisory Mode**: You control what gets sent; Claude Code suggests
- **Documentation**: Conversations are logged for future reference
- **Expertise**: Claude Code can help interpret EpochAI responses and suggest optimal paths

## Quick Start

```bash
# Start a chat using a definition
/epochai-chat project/definitions/test_runner/momentum_asset_allocation_research.json

# Or with a strategy
/epochai-chat project/definitions/test_runner/asset_class_trend_following_strategy.json
```

## Workflow Steps

### 1. Select Definition

Choose a definition file you want to discuss with EpochAI:
- Research definitions: `*_research.json`
- Strategy definitions: `*_strategy.json`

### 2. Claude Code Loads Context

Claude Code will:
- Read the definition JSON
- Find matching reference notes in `reference_notes/`
- Create a session file in `workflows/`

### 3. Draft Initial Message

Claude Code drafts a conversational message for EpochAI. Example:

```
SUGGESTED MESSAGE FOR EPOCHAI:
─────────────────────────────────
Hey, I'm working on a momentum asset allocation strategy. I've got a basic
implementation using SPY, EFA, BND, VNQ, and GSG with a 12-month lookback.

Can you help me validate if the IC analysis looks reasonable? I'm seeing
positive ICs for the longer lookbacks but want to make sure I'm interpreting
the results correctly.
─────────────────────────────────
```

### 4. Execute Commands

Run the suggested command to send the message:

```bash
python /home/adesola/EpochDev/EpochAI/tools/thread_chat.py chat "message here"
```

### 5. Share Responses

When EpochAI responds:
- Copy/paste the response back to Claude Code
- Or share a screenshot if the response is complex

### 6. Handle Interrupts

EpochAI may ask questions (ask_user) or present plans (approve_plan).

Claude Code will analyze and suggest responses:

```
INTERRUPT ANALYSIS:
- Type: approve_plan
- The plan proposes running a 10-year backtest with monthly rebalancing

SUGGESTED RESPONSE:
'{"action": "approve"}'

REASONING: Plan matches our definition parameters. Time period is appropriate
for momentum strategies.
```

### 7. Iterate & Document

Continue until the conversation reaches its goal. Claude Code will update the session file with findings.

## Session Files

Each conversation creates a session file:

```
workflows/epochai_2024-01-30_153045.md
```

Contents:
- Definition and reference notes used
- Thread ID
- Full conversation log
- Session summary and findings

## Tips

### Being Authoritative

Don't just approve everything EpochAI proposes. Use `edit` to:
- Specify exact outputs you want
- Add research-specific analysis
- Correct misunderstandings

### Reference Notes Are Key

The reference notes contain:
- Expected performance metrics
- Implementation details from source papers
- Known limitations

Use this to validate what EpochAI produces.

### Screenshot Handling

For complex EpochAI responses (charts, tables):
1. Take a screenshot
2. Share the path with Claude Code
3. Claude Code will analyze the visual

## File Locations

| Resource | Path |
|----------|------|
| Definitions | `project/definitions/test_runner/` |
| Reference Notes | `reference_notes/` |
| Session Files | `workflows/` |
| Thread Chat Tool | `/home/adesola/EpochDev/EpochAI/tools/thread_chat.py` |

## Related Skills

- `/run-job-data` - Execute definitions locally
- `/study-reports` - Analyze executed studies
- `/query-study` - SQL queries on study data
