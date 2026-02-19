#!/usr/bin/env python3
"""
Job Registry - Auto-discovers study definitions and manages run configurations.

Source of truth: Definition JSON files in project/definitions/test_runner/
Run parameters: scripts/run_config.json (defaults + per-definition overrides)

Usage:
    python scripts/job_registry.py list                     # List all definitions
    python scripts/job_registry.py list --type research      # Filter by type
    python scripts/job_registry.py show <definition_id>      # Show run details
    python scripts/job_registry.py run <definition_id>       # Run single definition
    python scripts/job_registry.py run-all                   # Run everything
    python scripts/job_registry.py run-all --type campaign   # Run all campaigns
    python scripts/job_registry.py run-all --exclude id1 id2 # Skip specific definitions
    python scripts/job_registry.py validate                  # Check definitions + config
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ─── Paths ───────────────────────────────────────────────────────────────────

WORKSPACE_ROOT = Path(__file__).parent.parent
DEFINITIONS_DIR = WORKSPACE_ROOT / "project" / "definitions" / "test_runner"
RUN_CONFIG_FILE = WORKSPACE_ROOT / "scripts" / "run_config.json"
RUN_SCRIPT = WORKSPACE_ROOT / "cpp_tools" / "run_generate_job_data.sh"

# Output folders where job results are written
OUTPUT_DIRS = {
    "research": WORKSPACE_ROOT / "project" / "research_studies" / "test_runner",
    "campaign": WORKSPACE_ROOT / "project" / "campaigns" / "test_runner",
}


# ─── Core ────────────────────────────────────────────────────────────────────

def load_run_config() -> dict:
    """Load run configuration with defaults and overrides."""
    if RUN_CONFIG_FILE.exists():
        with open(RUN_CONFIG_FILE) as f:
            return json.load(f)
    return {
        "defaults": {
            "research": {"1D": {"start": "2020-01-01", "end": "2024-12-31"}},
            "campaign": {"cash": 100000},
        },
        "overrides": {},
    }


def discover_definitions() -> list:
    """Auto-discover all definition JSON files from the definitions folder."""
    definitions = []
    for f in sorted(DEFINITIONS_DIR.glob("*.json")):
        def_id = f.stem
        try:
            with open(f) as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, FileNotFoundError):
            continue

        job_type = "campaign" if def_id.endswith("_strategy") else "research"

        definitions.append({
            "id": def_id,
            "name": data.get("name", def_id),
            "job_type": job_type,
            "assets": data.get("data", {}).get("assets", []),
            "source": data.get("data", {}).get("source", "polygon"),
            "timeframe": data.get("global_timeframe", "1D"),
            "path": str(f.relative_to(WORKSPACE_ROOT)),
        })

    return definitions


def get_run_params(definition: dict, config: dict) -> dict:
    """Get run parameters for a definition (merging defaults + overrides)."""
    def_id = definition["id"]
    job_type = definition["job_type"]
    timeframe = definition["timeframe"]

    if job_type == "campaign":
        params = {"cash": config.get("defaults", {}).get("campaign", {}).get("cash", 100000)}
    else:
        tf_defaults = config.get("defaults", {}).get("research", {})
        fallback = {"start": "2020-01-01", "end": "2024-12-31"}
        params = dict(tf_defaults.get(timeframe, tf_defaults.get("1D", fallback)))

    overrides = config.get("overrides", {}).get(def_id, {})
    params.update(overrides)

    return params


def build_command(definition: dict, params: dict) -> str:
    """Build the /run-job-data slash command string."""
    path = definition["path"]
    if definition["job_type"] == "campaign":
        return f'/run-job-data "{path}" --cash {params.get("cash", 100000)}'
    else:
        return f'/run-job-data "{path}" --start {params["start"]} --end {params["end"]}'


def build_shell_command(definition: dict, params: dict, asan: bool = False) -> list:
    """Build the actual shell command list for subprocess execution."""
    cmd = [str(RUN_SCRIPT)]
    if asan:
        cmd.append("--asan")

    def_path = str(WORKSPACE_ROOT / definition["path"])

    if definition["job_type"] == "campaign":
        cmd.extend([def_path, "--cash", str(params.get("cash", 100000))])
    else:
        cmd.extend([def_path, "--start", params["start"], "--end", params["end"]])

    return cmd


def find_definition(definitions: list, search: str) -> Optional[dict]:
    """Find a definition by exact ID or partial match. Returns None if ambiguous."""
    # Exact match
    for d in definitions:
        if d["id"] == search:
            return d

    # Partial match
    matches = [d for d in definitions if search in d["id"]]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"Ambiguous '{search}'. Matches:")
        for m in matches:
            print(f"  {m['id']}")
        return None
    else:
        print(f"Definition '{search}' not found.")
        return None


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_list(args):
    """List all definitions with their run parameters."""
    config = load_run_config()
    definitions = discover_definitions()

    if args.type:
        definitions = [d for d in definitions if d["job_type"] == args.type]

    research = [d for d in definitions if d["job_type"] == "research"]
    campaigns = [d for d in definitions if d["job_type"] == "campaign"]

    print(f"\n{'=' * 95}")
    print("DEFINITION REGISTRY")
    print(f"{'=' * 95}")

    if campaigns:
        print(f"\nCAMPAIGNS ({len(campaigns)})")
        print(f"{'─' * 95}")
        print(f"{'#':<4} {'Definition ID':<52} {'TF':<6} {'Assets':<15} {'Cash':>10}")
        print(f"{'─' * 95}")
        for i, d in enumerate(campaigns, 1):
            params = get_run_params(d, config)
            assets = _format_assets(d["assets"])
            print(f"{i:<4} {d['id']:<52} {d['timeframe']:<6} {assets:<15} ${params.get('cash', 100000):>9,}")

    if research:
        print(f"\nRESEARCH ({len(research)})")
        print(f"{'─' * 95}")
        print(f"{'#':<4} {'Definition ID':<52} {'TF':<6} {'Assets':<15} {'Period'}")
        print(f"{'─' * 95}")
        for i, d in enumerate(research, 1):
            params = get_run_params(d, config)
            assets = _format_assets(d["assets"])
            period = f"{params.get('start', '?')} to {params.get('end', '?')}"
            print(f"{i:<4} {d['id']:<52} {d['timeframe']:<6} {assets:<15} {period}")

    print(f"\n{'=' * 95}")
    print(f"Total: {len(definitions)} definitions ({len(campaigns)} campaigns, {len(research)} research)")
    print(f"Config: {RUN_CONFIG_FILE.relative_to(WORKSPACE_ROOT)}")
    print(f"{'=' * 95}\n")


def cmd_show(args):
    """Show details and run command for a specific definition."""
    config = load_run_config()
    definitions = discover_definitions()

    match = find_definition(definitions, args.definition_id)
    if not match:
        return

    params = get_run_params(match, config)
    command = build_command(match, params)

    print(f"\n{'=' * 70}")
    print(f"  {match['name']}")
    print(f"{'=' * 70}")
    print(f"  ID:        {match['id']}")
    print(f"  Type:      {match['job_type']}")
    print(f"  Timeframe: {match['timeframe']}")
    print(f"  Assets:    {', '.join(match['assets']) or '(none)'}")
    print(f"  Source:    {match['source']}")
    print(f"  File:      {match['path']}")
    print(f"{'─' * 70}")
    if match["job_type"] == "campaign":
        print(f"  Cash:      ${params.get('cash', 100000):,}")
    else:
        print(f"  Period:    {params.get('start')} to {params.get('end')}")
    print(f"{'─' * 70}")
    print(f"  Run:       {command}")
    print(f"{'=' * 70}\n")


def cmd_run(args):
    """Run a single definition."""
    config = load_run_config()
    definitions = discover_definitions()

    match = find_definition(definitions, args.definition_id)
    if not match:
        sys.exit(1)

    params = get_run_params(match, config)
    cmd = build_shell_command(match, params, asan=args.asan)

    mode = "[ASAN] " if args.asan else ""
    print(f"\n{mode}Running: {match['id']} ({match['job_type']})")
    print(f"Command: {' '.join(cmd)}")

    if args.dry_run:
        print("[DRY RUN] Skipping execution.\n")
        return

    print(f"{'─' * 60}")
    result = subprocess.run(cmd, cwd=WORKSPACE_ROOT)

    if result.returncode != 0:
        print(f"\nFailed: {match['id']} (exit code {result.returncode})")
        sys.exit(result.returncode)
    print(f"\nDone: {match['id']}")


def cmd_run_all(args):
    """Run all definitions (or filtered subset)."""
    config = load_run_config()
    definitions = discover_definitions()

    if args.type:
        definitions = [d for d in definitions if d["job_type"] == args.type]

    if args.exclude:
        excludes = set(args.exclude)
        definitions = [d for d in definitions if d["id"] not in excludes]

    total = len(definitions)
    if total == 0:
        print("No definitions to run.")
        return

    mode = "[ASAN] " if args.asan else ""
    dry = " [DRY RUN]" if args.dry_run else ""
    print(f"\n{mode}Running {total} definitions{dry}...")
    print(f"{'=' * 70}")

    success = 0
    failed = 0
    failures = []

    for i, d in enumerate(definitions, 1):
        params = get_run_params(d, config)
        cmd = build_shell_command(d, params, asan=args.asan)

        print(f"\n[{i}/{total}] {d['id']} ({d['job_type']})")
        print(f"  {' '.join(cmd)}")

        if args.dry_run:
            success += 1
            continue

        result = subprocess.run(cmd, cwd=WORKSPACE_ROOT)
        if result.returncode == 0:
            success += 1
        else:
            failed += 1
            failures.append(d["id"])
            if args.stop_on_error:
                print(f"\nStopping after failure: {d['id']}")
                break

    print(f"\n{'=' * 70}")
    print(f"Results: {success} succeeded, {failed} failed (of {total})")
    if failures:
        print(f"Failed:  {', '.join(failures)}")
    print(f"{'=' * 70}\n")


def cmd_validate(args):
    """Validate all definitions exist and config is consistent."""
    definitions = discover_definitions()
    config = load_run_config()

    errors = []
    warnings = []

    for d in definitions:
        path = WORKSPACE_ROOT / d["path"]
        if not path.exists():
            errors.append(f"  MISSING: {d['id']} -> {d['path']}")
            continue

        if not d["assets"]:
            warnings.append(f"  NO ASSETS: {d['id']}")

        params = get_run_params(d, config)
        if d["job_type"] == "research" and ("start" not in params or "end" not in params):
            errors.append(f"  NO DATES: {d['id']} (timeframe={d['timeframe']})")

    # Check for stale overrides
    def_ids = {d["id"] for d in definitions}
    for override_id in config.get("overrides", {}):
        if override_id not in def_ids:
            warnings.append(f"  STALE OVERRIDE: '{override_id}' has no matching definition")

    print(f"\nValidated {len(definitions)} definitions")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(e)

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(w)

    if not errors and not warnings:
        print("  All OK\n")
    else:
        print()


def cmd_clean(args):
    """Clean output folders for definitions."""
    definitions = discover_definitions()
    def_ids = {d["id"] for d in definitions}

    to_remove = []

    if args.definition_id:
        # Clean specific definition
        match = find_definition(definitions, args.definition_id)
        if not match:
            sys.exit(1)
        for output_dir in OUTPUT_DIRS.values():
            folder = output_dir / match["id"]
            if folder.exists():
                to_remove.append(folder)
    else:
        # Clean all
        for job_type, output_dir in OUTPUT_DIRS.items():
            if not output_dir.exists():
                continue
            if args.type and args.type != job_type:
                continue
            for folder in sorted(output_dir.iterdir()):
                if not folder.is_dir():
                    continue
                if args.orphans:
                    # Only remove folders that DON'T match any current definition
                    if folder.name not in def_ids:
                        to_remove.append(folder)
                else:
                    to_remove.append(folder)

    if not to_remove:
        print("Nothing to clean.")
        return

    # Calculate sizes
    total_size = 0
    print(f"\n{'Will delete' if not args.dry_run else '[DRY RUN] Would delete'}:")
    for folder in to_remove:
        size = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file())
        total_size += size
        size_mb = size / (1024 * 1024)
        orphan_tag = " (orphan)" if folder.name not in def_ids else ""
        print(f"  {folder.relative_to(WORKSPACE_ROOT)}  ({size_mb:.1f} MB){orphan_tag}")

    total_mb = total_size / (1024 * 1024)
    print(f"\n  {len(to_remove)} folders, {total_mb:.1f} MB total")

    if args.dry_run:
        print("[DRY RUN] No files removed.\n")
        return

    for folder in to_remove:
        shutil.rmtree(folder)
    print(f"Cleaned {len(to_remove)} folders.\n")


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _format_assets(assets: list) -> str:
    """Format assets list for display."""
    if not assets:
        return "(none)"
    if len(assets) == 1:
        a = assets[0]
        return a if len(a) <= 14 else a[:11] + "..."
    return f"{len(assets)} assets"


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Job Registry - Auto-discovers definitions and manages run configs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    sub = parser.add_subparsers(dest="action")

    # list
    p = sub.add_parser("list", help="List all definitions")
    p.add_argument("--type", choices=["research", "campaign"], help="Filter by type")

    # show
    p = sub.add_parser("show", help="Show definition details")
    p.add_argument("definition_id", help="Definition ID (supports partial match)")

    # run
    p = sub.add_parser("run", help="Run a single definition")
    p.add_argument("definition_id", help="Definition ID to run")
    p.add_argument("--dry-run", action="store_true", help="Show command only")
    p.add_argument("--asan", action="store_true", help="Use ASAN build")

    # run-all
    p = sub.add_parser("run-all", help="Run all definitions")
    p.add_argument("--type", choices=["research", "campaign"], help="Filter by type")
    p.add_argument("--dry-run", action="store_true", help="Show commands only")
    p.add_argument("--asan", action="store_true", help="Use ASAN build")
    p.add_argument("--stop-on-error", action="store_true", help="Stop on first failure")
    p.add_argument("--exclude", nargs="*", metavar="ID", help="Definition IDs to skip")

    # validate
    sub.add_parser("validate", help="Validate definitions and config")

    # clean
    p = sub.add_parser("clean", help="Remove output folders")
    p.add_argument("definition_id", nargs="?", help="Clean specific definition (partial match)")
    p.add_argument("--type", choices=["research", "campaign"], help="Filter by type")
    p.add_argument("--orphans", action="store_true", help="Only remove orphaned folders (no matching definition)")
    p.add_argument("--dry-run", action="store_true", help="Show what would be deleted")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        return

    {
        "list": cmd_list,
        "show": cmd_show,
        "run": cmd_run,
        "run-all": cmd_run_all,
        "validate": cmd_validate,
        "clean": cmd_clean,
    }[args.action](args)


if __name__ == "__main__":
    main()
