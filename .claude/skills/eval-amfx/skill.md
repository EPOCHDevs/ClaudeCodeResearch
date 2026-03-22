---
name: eval-amfx
description: Evaluate an amFX folder - visually inspect all kept charts, assess discretionary value, and create a tasks.md tracking file for reproduction.
user_invocable: true
arg: folder path or folder name under amfx_new/ (e.g. "AMFX_02AUG23" or full path)
---

# Evaluate amFX Charts for Reproduction

## Context

These are charts from Brent Donnelly's amFX (Spectra Markets) newsletters. Donnelly is a **discretionary macro FX trader** — NOT a quant. The value is in how he visualizes markets to build conviction, not just backtestable signals.

## What to evaluate

When given a folder under `/home/adesola/EpochDev/ClaudeCodeResearch/amfx_new/`, do the following:

### Step 1: Read analysis.md
Read the `analysis.md` in the folder to understand what charts exist and their context.

### Step 2: Visually inspect every KEPT image
Use the Read tool to view each image file referenced in analysis.md. Look at the actual chart.

### Step 3: Evaluate each chart with a DISCRETIONARY eye

**This is NOT about backtestable strategies.** Evaluate from these angles:

1. **Is the data interesting?** Does it show something surprising, extreme, or regime-changing?
2. **Is the chart design interesting?** Good use of overlays, color coding, annotations, dual axes, scatter vs line choice?
3. **Does it tell a story?** Would a macro trader look at this and form conviction?
4. **How do charts relate to each other?** Do they build a narrative together (zoom in/out, different angles on same thesis)?
5. **Can we reproduce it?** What data sources (FRED, Yahoo Finance, CFTC, BIS, etc.) and what chart type (scatter, bar, line, dual-axis overlay, heatmap)?

**Keep charts that are visually interesting, show interesting data, or demonstrate good chart craft — even if they're not "backtestable."**

Only discard charts that are truly uninteresting (generic price chart with no insight, stale point-in-time levels with no lasting value).

### Step 4: Create tasks.md

Create a `tasks.md` file in the folder with this format:

```markdown
# AMFX_XXXX — Chart Reproduction Tasks

Source: AMFX DDMMMYY newsletter by Brent Donnelly (Spectra Markets)
Theme: [1-line summary of the newsletter's thesis]
Date: [newsletter date]

## Charts to Reproduce

### Task 1: [Chart Title]
- **status:** TODO
- **image_ref:** [image filename]
- **chart_type:** [scatter, bar, line, dual-axis overlay, candlestick, heatmap, table]
- **data_sources:** [FRED series IDs, Yahoo tickers, etc.]
- **what_makes_it_interesting:** [1-2 lines on why this chart matters from a discretionary perspective]
- **reproduction_notes:** [any specific details needed — annotations, color coding, reference lines, etc.]

### Task 2: [Chart Title]
...

## Discarded Charts
| Chart | Reason |
|-------|--------|
| [name] | [why it's not worth reproducing] |
```

Status values: `TODO` → `IN_PROGRESS` → `DONE` → `PUBLISHED`

### Step 5: Summary
Print a brief summary: how many charts to reproduce, what the narrative thread is, any charts discarded and why.
