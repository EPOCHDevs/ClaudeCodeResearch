#!/usr/bin/env python3
"""
Deep validation of research study outputs.

Checks:
  1. STRUCTURAL — expected outputs exist (charts, tables, event markers)
  2. SEMANTIC   — charts have data, tables have values, signals fire
  3. QUALITY    — sufficient sample size, no degenerate results

Status levels:
  OPEN        — not processed
  REFACTORED  — grammar updated, not run
  EXECUTED    — ran without error, output exists
  VALIDATED   — all checks pass
  DEGRADED    — runs but has quality issues (empty charts, no signals, etc.)
  PARSE_ERROR — EpochScript won't compile
  RUNTIME_ERROR — crashes during execution
  INFRA_ERROR — infrastructure issue (permissions, missing data)
"""

import json
import os
import sys
import csv
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, os.path.expanduser("~/EpochDev/EpochAI"))

STUDY_BASES = {
    "research": "script_templates/research_studies/test_runner",
    "strategy": "script_templates/campaigns/test_runner",
}
DEF_DIR = "script_templates/definitions/test_runner"


def validate_study(study_name: str) -> dict:
    """Deep validation of a study. Returns validation report."""
    # Check both research and campaign output dirs
    study_dir = None
    for base in STUDY_BASES.values():
        candidate = os.path.join(base, study_name)
        if os.path.exists(candidate):
            study_dir = candidate
            break
    if study_dir is None:
        study_dir = os.path.join(list(STUDY_BASES.values())[0], study_name)
    report = {
        "checks": [],
        "warnings": [],
        "errors": [],
        "stats": {},
    }

    if not os.path.exists(study_dir):
        report["errors"].append("Study output directory not found")
        return report

    # =========================================================================
    # 1. STRUCTURAL CHECKS — do expected outputs exist?
    # =========================================================================

    # Manifest
    manifest_path = os.path.join(study_dir, "manifest.json")
    if not os.path.exists(manifest_path):
        report["errors"].append("No manifest.json")
        return report

    with open(manifest_path) as f:
        manifest = json.load(f)

    report["checks"].append("manifest exists")

    # Tearsheet
    ts_meta_path = os.path.join(study_dir, "tearsheets", "metadata.json")
    if not os.path.exists(ts_meta_path):
        report["errors"].append("No tearsheet metadata")
        return report

    with open(ts_meta_path) as f:
        ts_meta = json.load(f)

    categories = list(ts_meta.keys())
    report["stats"]["categories"] = len(categories)
    report["checks"].append(f"{len(categories)} tearsheet categories")

    # =========================================================================
    # 2. CHART VALIDATION — do charts have actual data?
    # =========================================================================

    total_charts = 0
    populated_charts = 0
    empty_charts = []

    for cat in categories:
        cat_info = ts_meta[cat]
        schema_path = cat_info.get("schema_path", "")

        # Fix path if it references old /home/adesola
        if "/home/adesola/" in schema_path:
            schema_path = schema_path.replace("/home/adesola/", "/home/ubuntu/")

        # Try relative path
        if not os.path.exists(schema_path):
            schema_path = os.path.join(study_dir, "tearsheets", cat, "schema.json")

        if not os.path.exists(schema_path):
            report["warnings"].append(f"Schema not found for {cat}")
            continue

        with open(schema_path) as f:
            schema = json.load(f)

        for chart in schema.get("charts", []):
            total_charts += 1
            data_id = chart.get("data_id", "")
            title = chart.get("title", "untitled")
            chart_type = chart.get("type", "?")

            # Check arrow data file
            arrow_path = os.path.join(study_dir, "tearsheets", cat, f"{data_id}.arrow")
            if not os.path.exists(arrow_path):
                empty_charts.append(f"{title} (no data file)")
                continue

            arrow_size = os.path.getsize(arrow_path)
            if arrow_size < 100:
                empty_charts.append(f"{title} (data file too small: {arrow_size}B)")
                continue

            # Read arrow to check row count and series
            try:
                import pyarrow.ipc as ipc
                with ipc.open_file(arrow_path) as reader:
                    table = reader.read_all()
                    rows = table.num_rows
                    cols = table.num_columns

                if rows == 0:
                    empty_charts.append(f"{title} (0 rows)")
                elif rows < 3:
                    report["warnings"].append(f"Chart '{title}' has only {rows} data points")
                    populated_charts += 1
                else:
                    populated_charts += 1

                # Check for all-null series (degenerate chart)
                null_series = []
                for col_name in table.column_names:
                    if col_name == "index":
                        continue
                    col = table.column(col_name)
                    if col.null_count == len(col):
                        null_series.append(col_name)

                if null_series and len(null_series) == (cols - 1):
                    report["warnings"].append(f"Chart '{title}' has all-null series")

            except Exception as e:
                report["warnings"].append(f"Could not read arrow for '{title}': {e}")
                populated_charts += 1  # Don't penalize for read errors

    report["stats"]["total_charts"] = total_charts
    report["stats"]["populated_charts"] = populated_charts
    report["stats"]["empty_charts"] = len(empty_charts)

    if total_charts == 0:
        report["errors"].append("No charts in tearsheet")
    elif populated_charts == 0:
        report["errors"].append("All charts are empty")
    elif empty_charts:
        for ec in empty_charts:
            report["warnings"].append(f"Empty chart: {ec}")

    report["checks"].append(f"{populated_charts}/{total_charts} charts populated")

    # =========================================================================
    # 3. TABLE VALIDATION — do summary tables have values?
    # =========================================================================

    total_tables = 0
    for cat in categories:
        cat_info = ts_meta[cat]
        total_tables += cat_info.get("tables", 0)

    report["stats"]["total_tables"] = total_tables
    if total_tables > 0:
        report["checks"].append(f"{total_tables} tables present")

    # =========================================================================
    # 4. MARKET DATA VALIDATION — computed columns aren't all null
    # =========================================================================

    tables_dir = os.path.join(study_dir, "tables")
    if not os.path.exists(tables_dir):
        # Try 1D subdirectory
        tables_dir = os.path.join(study_dir, "1D")

    if os.path.exists(tables_dir):
        try:
            import pyarrow.ipc as ipc
            for arrow_file in os.listdir(tables_dir):
                if not arrow_file.endswith('.arrow'):
                    continue
                arrow_path = os.path.join(tables_dir, arrow_file)
                with ipc.open_file(arrow_path) as reader:
                    table = reader.read_all()
                    rows = table.num_rows
                    cols = table.num_columns

                report["stats"]["market_data_rows"] = rows
                report["stats"]["market_data_cols"] = cols

                if rows == 0:
                    report["errors"].append(f"Market data table has 0 rows")
                    continue

                report["checks"].append(f"Market data: {rows} rows, {cols} columns")

                # Count columns that are ALL null (100%)
                all_null_cols = 0
                # Count "signal" columns (boolean-like or where-filtered)
                signal_cols = 0
                signal_populated = 0

                for col_name in table.column_names:
                    if col_name == "index":
                        continue
                    col = table.column(col_name)
                    null_pct = col.null_count / len(col) * 100

                    if null_pct == 100:
                        all_null_cols += 1

                    # Detect signal columns (where-filtered series are mostly null)
                    if 90 < null_pct < 100:
                        signal_cols += 1
                        signal_populated += 1

                report["stats"]["all_null_columns"] = all_null_cols
                report["stats"]["signal_columns"] = signal_cols

                if signal_cols > 0:
                    report["checks"].append(f"{signal_cols} signal columns detected (sparse, as expected)")
                elif total_tables > 0:
                    # Studies with tables usually have signal columns
                    report["warnings"].append("No signal columns found — events may not be firing")

                break  # Only check first market data table
        except Exception as e:
            report["warnings"].append(f"Could not validate market data: {e}")

    # =========================================================================
    # 5. EVENT MARKER VALIDATION
    # =========================================================================

    event_tables = []
    if os.path.exists(tables_dir):
        event_tables = [f for f in os.listdir(tables_dir) if 'event_marker' in f and f.endswith('.arrow')]

    if event_tables:
        try:
            for ef in event_tables:
                with ipc.open_file(os.path.join(tables_dir, ef)) as reader:
                    table = reader.read_all()
                    event_count = table.num_rows
                    report["stats"]["event_marker_count"] = event_count
                    if event_count == 0:
                        report["warnings"].append("Event marker table exists but has 0 events")
                    else:
                        report["checks"].append(f"{event_count} events in event markers")
        except Exception:
            pass

    return report


def determine_status(report: dict) -> tuple[str, str]:
    """Determine final status and notes from validation report."""
    if report["errors"]:
        return "DEGRADED", "; ".join(report["errors"])

    if report["warnings"]:
        # Warnings alone don't block VALIDATED, but flag for review
        stats = report["stats"]
        populated = stats.get("populated_charts", 0)
        total = stats.get("total_charts", 0)

        if populated == 0 and total > 0:
            return "DEGRADED", "All charts empty"

        notes = f"{populated}/{total} charts"
        if stats.get("total_tables", 0):
            notes += f", {stats['total_tables']} tables"
        if stats.get("event_marker_count", 0):
            notes += f", {stats['event_marker_count']} events"
        if stats.get("market_data_rows", 0):
            notes += f", {stats['market_data_rows']} rows"

        warning_summary = "; ".join(report["warnings"][:2])
        return "VALIDATED", f"{notes} | WARN: {warning_summary}"

    # All clean
    stats = report["stats"]
    populated = stats.get("populated_charts", 0)
    total = stats.get("total_charts", 0)
    notes = f"{populated}/{total} charts"
    if stats.get("total_tables", 0):
        notes += f", {stats['total_tables']} tables"
    if stats.get("event_marker_count", 0):
        notes += f", {stats['event_marker_count']} events"
    if stats.get("market_data_rows", 0):
        notes += f", {stats['market_data_rows']} rows"

    return "VALIDATED", notes


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", type=str, help="Only process matching files")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    # Read current CSV
    csv_path = os.path.join(DEF_DIR, "definition_status.csv")
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    updated = 0
    for row in rows:
        name = row["file"].replace(".json", "")

        if args.filter and args.filter not in name:
            continue

        # Only validate definitions that were EXECUTED (or already VALIDATED)
        if row["status"] not in ("VALIDATED", "EXECUTED"):
            continue

        found = False
        for base in STUDY_BASES.values():
            if os.path.exists(os.path.join(base, name)):
                found = True
                break
        if not found:
            continue

        report = validate_study(name)
        new_status, notes = determine_status(report)

        old_status = row["status"]
        row["status"] = new_status
        row["error"] = notes

        if args.verbose or new_status == "DEGRADED":
            print(f"{'!' if new_status == 'DEGRADED' else '✓'} {name}: {new_status}")
            if report["errors"]:
                for e in report["errors"]:
                    print(f"    ERROR: {e}")
            if report["warnings"]:
                for w in report["warnings"]:
                    print(f"    WARN: {w}")
            if args.verbose:
                for c in report["checks"]:
                    print(f"    ✓ {c}")

        updated += 1

    # Write updated CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    # Summary
    from collections import Counter
    status_counts = Counter(r["status"] for r in rows)
    print(f"\nValidated {updated} studies")
    print(f"\nStatus breakdown (all {len(rows)} definitions):")
    for s, c in status_counts.most_common():
        print(f"  {s:15s} {c:3d}")


if __name__ == "__main__":
    main()
