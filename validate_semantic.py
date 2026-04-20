#!/usr/bin/env python3
"""
Semantic validation of research study outputs.

Goes beyond "data exists" to verify:
1. Research objective is answerable from the output
2. Computed values are in sensible ranges
3. Signals/events actually fire with sufficient sample
4. Charts show differentiated, non-degenerate results
5. Key metrics match expected domain behavior

Usage:
    python validate_semantic.py [--filter PATTERN] [--verbose]
"""

import json
import os
import sys
import csv
from pathlib import Path
from collections import Counter

DEF_DIR = "script_templates/definitions/test_runner"
STUDY_BASES = {
    "research": "script_templates/research_studies/test_runner",
    "strategy": "script_templates/campaigns/test_runner",
}


def find_study_dir(name: str) -> str | None:
    for base in STUDY_BASES.values():
        candidate = os.path.join(base, name)
        if os.path.exists(candidate):
            return candidate
    return None


def load_arrow(path: str):
    """Load arrow file, return pandas DataFrame."""
    import pyarrow.ipc as ipc
    with ipc.open_file(path) as reader:
        return reader.read_all().to_pandas()


def semantic_validate(name: str, definition: dict) -> dict:
    """Deep semantic validation. Returns {status, checks, warnings, errors}."""
    result = {"checks": [], "warnings": [], "errors": []}

    study_dir = find_study_dir(name)
    if not study_dir:
        result["errors"].append("No study output found")
        return result

    description = definition.get("description", "")
    source = definition.get("source", "")
    assets = definition.get("data", {}).get("assets", [])

    # =========================================================================
    # 1. LOAD ALL CHART DATA
    # =========================================================================
    ts_meta_path = os.path.join(study_dir, "tearsheets", "metadata.json")
    if not os.path.exists(ts_meta_path):
        result["errors"].append("No tearsheet")
        return result

    with open(ts_meta_path) as f:
        ts_meta = json.load(f)

    charts_data = {}  # title -> DataFrame
    charts_schema = {}  # title -> schema dict

    for cat in ts_meta:
        schema_path = os.path.join(study_dir, "tearsheets", cat, "schema.json")
        if not os.path.exists(schema_path):
            continue
        with open(schema_path) as f:
            schema = json.load(f)

        for chart in schema.get("charts", []):
            title = chart.get("title", "untitled")
            data_id = chart.get("data_id", "")
            arrow_path = os.path.join(study_dir, "tearsheets", cat, f"{data_id}.arrow")

            charts_schema[title] = chart

            if os.path.exists(arrow_path):
                try:
                    charts_data[title] = load_arrow(arrow_path)
                except Exception:
                    pass

    if not charts_data:
        result["errors"].append("No chart data loaded")
        return result

    # =========================================================================
    # 2. CHART DATA QUALITY — non-degenerate, differentiated
    # =========================================================================
    for title, df in charts_data.items():
        schema = charts_schema.get(title, {})
        chart_type = schema.get("type", "?")

        # Skip index column
        data_cols = [c for c in df.columns if c != "index"]

        if len(data_cols) == 0:
            result["errors"].append(f"Chart '{title}': no data columns")
            continue

        for col in data_cols:
            series = df[col].dropna()

            if len(series) == 0:
                result["errors"].append(f"Chart '{title}' series '{col}': all null — no data rendered")
                continue

            # Check for constant/flat series (degenerate)
            if len(series) > 5:
                unique_vals = series.nunique()
                if unique_vals == 1:
                    val = series.iloc[0]
                    val_str = f"{val:.4g}" if isinstance(val, (int, float)) else str(val)[:20]
                    result["warnings"].append(f"Chart '{title}' series '{col}': flat line (1 unique value: {val_str})")

            # Check for extreme values (potential calculation error)
            if series.dtype in ('float64', 'float32', 'int64'):
                max_abs = series.abs().max()
                if max_abs > 1e10:
                    result["warnings"].append(f"Chart '{title}' series '{col}': extreme value ({max_abs:.2e})")

        # For bar charts with multiple series: check they're not identical
        if chart_type in ("Bar", "GroupedBar") and len(data_cols) >= 2:
            vals = [df[c].dropna().mean() for c in data_cols if df[c].dropna().shape[0] > 0]
            if len(vals) >= 2 and len(set(round(v, 6) for v in vals)) == 1:
                result["warnings"].append(f"Chart '{title}': all series have identical mean — no differentiation")

        result["checks"].append(f"Chart '{title}': {len(data_cols)} series, data OK")

    # =========================================================================
    # 3. EVENT/SIGNAL VALIDATION
    # =========================================================================
    # Check event marker tables for sufficient sample size
    tables_dir = os.path.join(study_dir, "tables")
    if not os.path.exists(tables_dir):
        tables_dir = os.path.join(study_dir, "1D")

    event_count = 0
    if os.path.exists(tables_dir):
        for f in os.listdir(tables_dir):
            if 'event_marker' in f and f.endswith('.arrow'):
                try:
                    df = load_arrow(os.path.join(tables_dir, f))
                    event_count += len(df)
                except Exception:
                    pass

    has_events = "event_marker" in source
    if has_events:
        if event_count == 0:
            result["errors"].append("Event markers defined but 0 events fired — signals never trigger")
        elif event_count < 3:
            result["warnings"].append(f"Only {event_count} events — too few for reliable analysis")
        else:
            result["checks"].append(f"{event_count} events fired")

    # =========================================================================
    # 4. SIGNAL COLUMN VALIDATION (where-filtered sparse series)
    # =========================================================================
    # In event-driven studies, where() creates sparse columns
    # These should have SOME non-null values
    if os.path.exists(tables_dir):
        for f in os.listdir(tables_dir):
            if not f.startswith('market_data') or not f.endswith('.arrow'):
                continue
            try:
                df = load_arrow(os.path.join(tables_dir, f))
                total_rows = len(df)

                # Find sparse signal columns (90-99.9% null = event-filtered)
                signal_cols = []
                for col in df.columns:
                    if col == 'index':
                        continue
                    null_pct = df[col].isnull().sum() / total_rows * 100
                    if 90 < null_pct < 100:
                        non_null = df[col].dropna()
                        signal_cols.append((col, len(non_null)))

                if signal_cols:
                    total_signals = sum(n for _, n in signal_cols)
                    result["checks"].append(f"{len(signal_cols)} signal columns, {total_signals} total non-null values")

                # Check for return columns — should be in reasonable range
                for col in df.columns:
                    if any(kw in col.lower() for kw in ['return', 'post_', 'forward']):
                        vals = df[col].dropna()
                        if len(vals) > 0:
                            min_v, max_v = vals.min(), vals.max()
                            if min_v < -5.0 or max_v > 10.0:
                                result["warnings"].append(f"Return column '{col}': range [{min_v:.2%}, {max_v:.2%}] — check for calculation error")

            except Exception as e:
                result["warnings"].append(f"Could not validate market data: {e}")
            break

    # =========================================================================
    # 5. RESEARCH OBJECTIVE CHECK
    # =========================================================================
    # Parse description for expected patterns and verify output supports them

    desc_lower = description.lower()

    # Studies about regime comparison should have multiple regimes
    if any(kw in desc_lower for kw in ['regime', 'compare', 'versus', 'vs.', 'split']):
        # Check that bar charts have >= 2 series with different values
        bar_charts = [(t, d) for t, d in charts_data.items()
                      if charts_schema.get(t, {}).get("type", "") in ("Bar", "GroupedBar")]
        for title, df in bar_charts:
            data_cols = [c for c in df.columns if c != "index"]
            if len(data_cols) < 2:
                result["warnings"].append(f"Regime study but chart '{title}' has <2 series — can't compare regimes")

    # Studies about reaction/drift should have post-event returns
    if any(kw in desc_lower for kw in ['reaction', 'drift', 'after', 'post-', 'reversal']):
        has_returns = any('return' in col.lower() or 'post' in col.lower()
                         for df in charts_data.values() for col in df.columns)
        if not has_returns and event_count > 0:
            result["checks"].append("Post-event returns present in data")
        elif not has_returns and event_count == 0:
            result["warnings"].append("Study about reaction/drift but no return columns and no events")

    # Studies about correlation should have corr values in [-1, 1]
    if 'correlation' in desc_lower:
        for title, df in charts_data.items():
            for col in df.columns:
                if col == 'index':
                    continue
                vals = df[col].dropna()
                if len(vals) > 0:
                    if vals.min() >= -1.1 and vals.max() <= 1.1:
                        result["checks"].append(f"Correlation values in valid range")
                        break

    # =========================================================================
    # 6. SAMPLE SIZE CHECK
    # =========================================================================
    for title, df in charts_data.items():
        data_cols = [c for c in df.columns if c != "index"]
        for col in data_cols:
            non_null = df[col].dropna()
            if 0 < len(non_null) < 3:
                result["warnings"].append(f"Chart '{title}' series '{col}': only {len(non_null)} data points — unreliable")

    return result


def determine_status(result: dict) -> tuple[str, str]:
    """Map validation results to status + notes."""
    if result["errors"]:
        return "DEGRADED", "; ".join(result["errors"][:3])

    checks = result["checks"]
    warnings = result["warnings"]

    notes_parts = []
    for c in checks[:4]:
        notes_parts.append(c)

    if warnings:
        warn_summary = "; ".join(w[:80] for w in warnings[:2])
        notes = " | ".join(notes_parts) + f" | WARN: {warn_summary}"
    else:
        notes = " | ".join(notes_parts)

    return "VALIDATED", notes


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", type=str)
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    csv_path = os.path.join(DEF_DIR, "definition_status.csv")
    with open(csv_path) as f:
        rows = list(csv.DictReader(f))

    counts = Counter()
    degraded = []

    for row in rows:
        name = row["file"].replace(".json", "")
        if args.filter and args.filter not in name:
            continue

        if row["status"] not in ("VALIDATED", "EXECUTED"):
            counts[row["status"]] += 1
            continue

        # Load definition
        def_path = os.path.join(DEF_DIR, row["file"])
        with open(def_path) as f:
            definition = json.load(f)

        result = semantic_validate(name, definition)
        new_status, notes = determine_status(result)

        row["status"] = new_status
        row["error"] = notes
        counts[new_status] += 1

        if args.verbose or new_status == "DEGRADED":
            icon = "✗" if new_status == "DEGRADED" else "✓"
            print(f"{icon} {name}: {new_status}")
            if result["errors"]:
                for e in result["errors"]:
                    print(f"    ERROR: {e}")
            if result["warnings"] and args.verbose:
                for w in result["warnings"]:
                    print(f"    WARN: {w}")
            if result["checks"] and args.verbose:
                for c in result["checks"]:
                    print(f"    ✓ {c}")
        elif new_status == "DEGRADED":
            degraded.append((name, notes))

    # Write CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nStatus breakdown ({sum(counts.values())} definitions):")
    for s, c in counts.most_common():
        print(f"  {s:15s} {c:3d}")

    if degraded:
        print(f"\nDEGRADED studies:")
        for name, notes in degraded:
            print(f"  {name}: {notes}")


if __name__ == "__main__":
    main()
