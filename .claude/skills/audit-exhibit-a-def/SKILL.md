---
name: audit-exhibit-a-def
description: |
  Audit an Exhibit A study definition by comparing it against the original reference image and transcript.
  Use when the user wants to review, audit, or fix a definition to match the Exhibit A source material.
  Checks for: visual match, data-driven approach (no hardcoded values), correct data source/range, chart type accuracy, and proper labeling.
allowed-tools: Bash, Read, Glob, Grep, Edit, Write, Agent
argument-hint: "<definition-name>"
---

# Exhibit A Definition Auditor

Audit an Exhibit A study definition against its reference image and transcript. Produce a structured audit report with issues and recommended fixes.

## Usage

```
/audit-exhibit-a-def time-between-all-time-highs
/audit-exhibit-a-def ea_sp500_showing_all_time_highs_research
```

## Paths

- **Definitions:** `/home/adesola/EpochDev/ClaudeCodeResearch/project/definitions/test_runner/`
- **Exhibit A images & transcripts:** `/home/adesola/EpochDev/ClaudeCodeResearch/exhibit_a_research/exhibita_organized/`
- **Manifest:** `/home/adesola/EpochDev/ClaudeCodeResearch/exhibit_a_research/manifest.csv`
- **Study outputs:** `/home/adesola/EpochDev/ClaudeCodeResearch/project/research_studies/test_runner/`

## Workflow

### Step 1: Resolve the Definition

Given the argument, find the matching definition JSON and Exhibit A reference materials.

```bash
# Strip ea_ prefix and _research suffix to get the study slug
# e.g. "ea_sp500_showing_all_time_highs_research" -> "sp500-showing-all-time-highs"
# or user may pass the slug directly: "time-between-all-time-highs"
```

1. Find the definition JSON in `project/definitions/test_runner/`
2. Find the Exhibit A directory in `exhibit_a_research/exhibita_organized/<slug>/`
3. If no match, search the manifest.csv for the closest match

### Step 2: Load All Reference Materials

Read these files:

1. **Definition JSON** - the EpochScript source and configuration
2. **Exhibit A image** (`.png`) - the reference chart/visual the definition should replicate
3. **Exhibit A transcript** (`transcript.txt`) - title, topic, question, key takeaways, source

### Step 3: Audit Against Checklist

Compare the definition against the Exhibit A reference using this checklist:

#### A. Data Coverage & Source
- Does the date range match the Exhibit A? (e.g., "Since 1950" requires `common_indices(ticker=SPX)`, not SPY which starts 2003)
- Are the correct assets/data sources used?
- Is the data source capable of providing the full history shown in the Exhibit A image?

#### B. Chart Type & Visual Match
- Does the chart type match? (lines, bars, area, histogram, scatter, etc.)
- Does the number of series match?
- Are colors consistent with the Exhibit A?
- Is the area fill used when the Exhibit A shows it?

#### C. Labeling & Metadata
- Does the chart title match the Exhibit A title?
- Are axis labels correct? (Y-axis label, format, decimal places)
- Is the category/section naming appropriate?

#### D. Data-Driven Approach (CRITICAL)
- **NO hardcoded values** - All thresholds, averages, reference lines must be computed from data
- **NO hardcoded date ranges** - Use dynamic detection (e.g., `hold_until`, `crossunder`, `crossover`) instead of year filters
- **NO hardcoded period labels** - Derive from data where possible
- Reference lines should use computed aggregations (e.g., `cumulative(agg=AggregationType.Mean)`)
- If the Exhibit A shows summary statistics, compute them dynamically

#### E. Completeness
- Does the definition capture all charts/tables shown in the Exhibit A?
- Are key takeaways from the transcript reflected in the data presentation?
- Are event markers used where appropriate?

#### F. EpochScript Correctness
- Are transforms used correctly? (check known bugs: `Timestamp()` returns NaT, `valuewhen(occurrence=0)` returns current bar)
- Are enum values fully qualified? (e.g., `AggregationType.Max` not bare `Max`)
- Is the null handling correct? (consider `nullPolicy: DropNulls` in reporters)

### Step 4: Generate Audit Report

Output a structured report:

```
## Audit: <definition-name>

### Reference
- **Exhibit A Title:** <title from transcript>
- **Exhibit A Date Range:** <date range visible in image>
- **Transcript Key Points:** <bullet points>

### Issues Found

| # | Severity | Category | Issue | Fix |
|---|----------|----------|-------|-----|
| 1 | CRITICAL | Data Coverage | SPY only goes to 2003, Exhibit A shows 1950+ | Use common_indices(ticker=SPX) |
| 2 | HIGH     | Hardcoded    | Reference line uses hardcoded -35% | Compute from cumulative mean |
| 3 | MEDIUM   | Labeling     | Y-axis label doesn't match | Change to "..." |
| 4 | LOW      | Style        | Color doesn't match Exhibit A | Change to Color.X |

### Recommended Definition

[Updated EpochScript source with all fixes applied]
```

### Step 5: Apply Fixes (if user confirms)

If the user wants to apply fixes, update the definition JSON with the corrected EpochScript.

ARGUMENTS: $ARGUMENTS
