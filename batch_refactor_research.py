#!/usr/bin/env python3
"""
Batch refactor research definitions to new grammar, run studies, and validate.

Usage:
    python batch_refactor_research.py [--dry-run] [--skip-run] [--filter PATTERN]
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

DIR = "script_templates/definitions/test_runner"
RUN_SCRIPT = "cpp_tools/run_generate_job_data.sh"
STUDY_DIR = "script_templates/research_studies/test_runner"
QUERY_SCRIPT = "analyze_job/query_study_dataframes.py"
REPORT_SCRIPT = "analyze_job/get_study_reports.py"


def refactor_source(src: str) -> tuple[str, list[str]]:
    """Apply grammar refactoring to EpochScript source. Returns (new_src, changes)."""
    changes = []
    original = src

    # 1. market_data_source(timeframe=1D)() → study_assets()
    #    market_data_source()() → study_assets()
    #    market_data_source(timeframe=5Min)() etc — keep timeframe via study_assets target_timeframe
    for pat in re.findall(r'market_data_source\(timeframe=(\w+)\)\(\)', src):
        old = f'market_data_source(timeframe={pat})()'
        if pat == '1D':
            new = 'study_assets()'
        else:
            # For non-1D, use study_assets with target_timeframe
            new = f'study_assets(target_timeframe="{pat}")'
        src = src.replace(old, new)
        changes.append(f'{old} → {new}')

    if 'market_data_source()()' in src:
        src = src.replace('market_data_source()()', 'study_assets()')
        changes.append('market_data_source()() → study_assets()')

    # 2. Layer 1 data sources: remove trailing ()
    # economic_indicators(series_id='X')() → economic_indicators(series_id="X")
    for m in re.finditer(r"economic_indicators\(series_id='([^']*)'\)\(\)", src):
        old = m.group(0)
        sid = m.group(1)
        new = f'economic_indicators(series_id="{sid}")'
        src = src.replace(old, new)
        changes.append(f'economic_indicators(...{sid}...)() → single-stage')

    # Also handle double-quoted version
    for m in re.finditer(r'economic_indicators\(series_id="([^"]*)"\)\(\)', src):
        old = m.group(0)
        sid = m.group(1)
        new = f'economic_indicators(series_id="{sid}")'
        src = src.replace(old, new)
        changes.append(f'economic_indicators(...{sid}...)() → single-stage')

    # economic_calendar(...)() → economic_calendar(...)
    for m in re.finditer(r"(economic_calendar\([^)]*\))\(\)", src):
        old = m.group(0)
        new = m.group(1)
        src = src.replace(old, new)
        changes.append(f'economic_calendar(...)() → single-stage')

    # economic_revisions(...)() → economic_revisions(...)
    for m in re.finditer(r"(economic_revisions\([^)]*\))\(\)", src):
        old = m.group(0)
        new = m.group(1)
        src = src.replace(old, new)
        changes.append(f'economic_revisions(...)() → single-stage')

    # Simple data sources: earnings()(), short_volume()(), etc.
    for ds in ['earnings', 'analyst_ratings', 'short_volume', 'short_interest',
               'ipos', 'splits', 'ticker_events']:
        old = f'{ds}()()'
        if old in src:
            src = src.replace(old, f'{ds}()')
            changes.append(f'{ds}()() → {ds}()')

    # Data sources with options: income_statement(period=...)(), balance_sheet(period=...)()
    for ds in ['income_statement', 'balance_sheet', 'cash_flow', 'dividends']:
        for m in re.finditer(rf"({ds}\([^)]*\))\(\)", src):
            old = m.group(0)
            new = m.group(1)
            src = src.replace(old, new)
            changes.append(f'{ds}(...)() → single-stage')

    # 3. Layer 1 moving averages: fn(period=N)(expr) → fn(expr, N)
    for fn in ['sma', 'ema', 'wma', 'hma', 'dema', 'tema', 'kama', 'trima', 'wilders', 'zlema']:
        for m in re.finditer(rf'{fn}\(period=(\d+)\)\(([^)]+)\)', src):
            old = m.group(0)
            period = m.group(1)
            expr = m.group(2)
            new = f'{fn}({expr}, {period})'
            src = src.replace(old, new)
            changes.append(f'{fn}(period={period})(x) → {fn}(x, {period})')

    # 4. Layer 1 indicators: fn(period=N)(expr) → fn(expr, N)
    for fn in ['rsi', 'roc', 'rocr', 'stochrsi', 'cmo', 'fosc', 'trix', 'dpo',
               'vhf', 'md', 'percentrank', 'decay', 'edecay', 'apo', 'ppo',
               'ulcer_index', 'forward_returns', 'nlargest', 'nsmallest']:
        for m in re.finditer(rf'{fn}\(period=(\d+)\)\(([^)]+)\)', src):
            old = m.group(0)
            period = m.group(1)
            expr = m.group(2)
            new = f'{fn}({expr}, {period})'
            src = src.replace(old, new)
            changes.append(f'{fn}(period={period})(x) → {fn}(x, {period})')

    # 5. Multi-input indicators: atr(period=N)(h, l, c) → atr(h, l, c, N)
    for fn in ['atr', 'natr', 'cci', 'willr', 'adx', 'adxr', 'dx', 'mfi']:
        for m in re.finditer(rf'{fn}\(period=(\d+)\)\(([^)]+)\)', src):
            old = m.group(0)
            period = m.group(1)
            inputs = m.group(2)
            new = f'{fn}({inputs}, {period})'
            src = src.replace(old, new)
            changes.append(f'{fn}(period={period})(inputs) → {fn}(inputs, {period})')

    # 6. Layer 1 pair stats: corr(window=N)(a, b) → corr(a, b, window=N)
    for fn in ['corr', 'cov', 'beta']:
        for m in re.finditer(rf'{fn}\(window=(\d+)\)\(([^)]+)\)', src):
            old = m.group(0)
            window = m.group(1)
            inputs = m.group(2)
            new = f'{fn}({inputs}, window={window})'
            src = src.replace(old, new)
            changes.append(f'{fn}(window={window})(inputs) → {fn}(inputs, window={window})')

    # 7. Layer 2 macros: bbands(period=N, stddev=S)(expr) → upper, mid, lower = bbands(expr, period=N, stddev=S)
    # These are trickier — the macro call itself changes, but the assignment pattern stays
    for fn in ['volatility']:
        for m in re.finditer(rf'{fn}\(([^)]+)\)\(([^)]+)\)', src):
            old = m.group(0)
            opts = m.group(1)
            inputs = m.group(2)
            new = f'{fn}({inputs}, {opts})'
            src = src.replace(old, new)
            changes.append(f'{fn}(opts)(inputs) → {fn}(inputs, opts)')

    # donchian_channel(window=N)(h, l) → donchian_channel(h, l, window=N)
    for fn in ['donchian_channel']:
        for m in re.finditer(rf'{fn}\(([^)]+)\)\(([^)]+)\)', src):
            old = m.group(0)
            opts = m.group(1)
            inputs = m.group(2)
            new = f'{fn}({inputs}, {opts})'
            src = src.replace(old, new)
            changes.append(f'{fn}(opts)(inputs) → {fn}(inputs, opts)')

    # 8. Single-quote string options → double quotes (normalize)
    # Only in function args, not in comments
    # economic_indicators already handled above; catch remaining single-quoted strings in function calls
    # This is cosmetic but aligns with EBNF convention

    return src, changes


def refactor_definition(path: str, dry_run: bool = False) -> tuple[bool, list[str]]:
    """Refactor a single definition file. Returns (changed, changes)."""
    with open(path) as f:
        data = json.load(f)

    changes = []

    # Refactor source
    src = data.get("source", "")
    new_src, src_changes = refactor_source(src)
    changes.extend(src_changes)

    if new_src != src:
        data["source"] = new_src

    # Remove global_timeframe
    if "global_timeframe" in data:
        data.pop("global_timeframe")
        changes.append("Removed global_timeframe")

    if changes and not dry_run:
        with open(path, 'w') as f:
            json.dump(data, f, separators=(',', ':'))
            f.write('\n')

    return bool(changes), changes


def run_study(def_path: str, timeout: int = 120) -> tuple[bool, str]:
    """Run generate_job_data on a definition. Returns (success, output)."""
    cmd = [RUN_SCRIPT, def_path, "--start", "2020-01-01", "--end", "2024-12-31"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = result.stdout + result.stderr
        success = "Study completed successfully" in output
        return success, output
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)


def validate_study(study_name: str) -> dict:
    """Run validation queries on study output. Returns validation dict."""
    study_dir = os.path.join(STUDY_DIR, study_name)
    if not os.path.exists(study_dir):
        return {"error": "Study dir not found"}

    validation = {}

    # 1. Get tables
    try:
        result = subprocess.run(
            [sys.executable, QUERY_SCRIPT, study_dir, "--tables"],
            capture_output=True, text=True, timeout=30
        )
        validation["tables"] = result.stdout.strip()
    except Exception as e:
        validation["tables_error"] = str(e)

    # 2. Get reports
    try:
        result = subprocess.run(
            [sys.executable, REPORT_SCRIPT, study_dir],
            capture_output=True, text=True, timeout=30
        )
        validation["reports"] = result.stdout.strip()
    except Exception as e:
        validation["reports_error"] = str(e)

    # 3. Null analysis
    try:
        result = subprocess.run(
            [sys.executable, QUERY_SCRIPT, study_dir, "--nulls"],
            capture_output=True, text=True, timeout=30
        )
        # Count high-null columns (>95% null, excluding expected sparse data)
        lines = result.stdout.strip().split('\n')
        high_null = [l for l in lines if 'nulls' in l and '100.0%' in l]
        validation["null_summary"] = f"{len(high_null)} columns with 100% nulls"
    except Exception as e:
        validation["nulls_error"] = str(e)

    # 4. Row count check
    try:
        result = subprocess.run(
            [sys.executable, QUERY_SCRIPT, study_dir, "--tables"],
            capture_output=True, text=True, timeout=30
        )
        for line in result.stdout.strip().split('\n'):
            if 'market_data' in line:
                validation["market_data_rows"] = line.strip()
                break
    except Exception:
        pass

    # 5. Check tearsheet exists and has content
    ts_dir = os.path.join(study_dir, "tearsheets")
    if os.path.exists(ts_dir):
        ts_meta = os.path.join(ts_dir, "metadata.json")
        if os.path.exists(ts_meta):
            with open(ts_meta) as f:
                meta = json.load(f)
            total_charts = sum(v.get("charts", 0) for v in meta.values())
            total_tables = sum(v.get("tables", 0) for v in meta.values() if isinstance(v, dict))
            validation["tearsheet"] = f"{len(meta)} categories, {total_charts} charts"

    return validation


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    parser.add_argument("--skip-run", action="store_true", help="Only refactor, don't run studies")
    parser.add_argument("--filter", type=str, help="Only process files matching pattern")
    parser.add_argument("--skip-existing", action="store_true", help="Skip if study output exists")
    args = parser.parse_args()

    files = sorted(f for f in os.listdir(DIR) if f.endswith('_research.json'))
    if args.filter:
        files = [f for f in files if args.filter in f]

    print(f"Processing {len(files)} research definitions")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"{'='*80}\n")

    results = {"refactored": 0, "unchanged": 0, "run_ok": 0, "run_fail": 0, "skipped": 0}
    failures = []

    for i, fname in enumerate(files):
        path = os.path.join(DIR, fname)
        study_name = fname.replace('.json', '')
        print(f"[{i+1}/{len(files)}] {study_name}")

        # Refactor
        changed, changes = refactor_definition(path, dry_run=args.dry_run)
        if changed:
            results["refactored"] += 1
            for c in changes:
                print(f"  ✓ {c}")
        else:
            results["unchanged"] += 1
            print(f"  (no changes needed)")

        if args.dry_run or args.skip_run:
            continue

        # Check if study already exists
        study_dir = os.path.join(STUDY_DIR, study_name)
        if args.skip_existing and os.path.exists(study_dir):
            results["skipped"] += 1
            print(f"  → Skipped (output exists)")
            continue

        # Run study
        print(f"  → Running study...", end="", flush=True)
        t0 = time.time()
        success, output = run_study(path)
        elapsed = time.time() - t0

        if success:
            results["run_ok"] += 1
            print(f" OK ({elapsed:.1f}s)")

            # Validate
            val = validate_study(study_name)
            if val.get("market_data_rows"):
                print(f"    Data: {val['market_data_rows']}")
            if val.get("tearsheet"):
                print(f"    Tearsheet: {val['tearsheet']}")
            if val.get("null_summary"):
                print(f"    Nulls: {val['null_summary']}")
        else:
            results["run_fail"] += 1
            # Extract error
            error_lines = [l for l in output.split('\n') if 'error' in l.lower() or 'Error' in l]
            error_msg = error_lines[-1] if error_lines else "Unknown error"
            print(f" FAILED ({elapsed:.1f}s)")
            print(f"    ERROR: {error_msg[:120]}")
            failures.append((study_name, error_msg[:200]))

    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"  Refactored: {results['refactored']}")
    print(f"  Unchanged:  {results['unchanged']}")
    if not args.dry_run and not args.skip_run:
        print(f"  Run OK:     {results['run_ok']}")
        print(f"  Run FAIL:   {results['run_fail']}")
        print(f"  Skipped:    {results['skipped']}")

    if failures:
        print(f"\nFAILURES:")
        for name, err in failures:
            print(f"  {name}: {err}")


if __name__ == "__main__":
    main()
