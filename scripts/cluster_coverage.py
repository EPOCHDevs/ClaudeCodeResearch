#!/usr/bin/env python3
"""
Cluster Coverage Analyzer

Measures test coverage of transform clusters by matching definitions against
the full transform metadata inventory.

CONCEPT:
  Each transform × code-flow-enum-value = 1 coverage unit.
  - Code-flow enums: route to different implementations (ma-sma vs ma-ema)
  - Parametric enums: same code path, different value (weekday=Friday) — NOT separate units
  - Cosmetic enums: Color, Icon, DashStyle — always excluded

WORKFLOW (for any cluster):
  1. Write SKILLS first (EpochAI/agent_src/prompts/skills/) — what the agent learns
  2. Write DEFINITIONS (project_hand_book/definitions/test_runner/) — validate skill syntax
  3. Run definitions: /build-job-data && /run-job-data <definition.json>
  4. Check coverage: python scripts/cluster_coverage.py --cluster <Category> --all
  5. Validate data: python tools/analyze_job/query_study_dataframes.py <study_dir> --tables

AVAILABLE CLUSTERS (categories):
  ControlFlow, Trend, Momentum, Volatility, Volume, PriceAction,
  Statistical, Factor, Utility, Reporter, Executor, ML, Portfolio,
  DataSource, DataPrep, Math, Indicator, Scalar, EventMarker, Aggregate

DEFINITION NAMING:
  Prefix with cluster name: signal_cluster_S16_crossover.json
                            trend_cluster_T01_sma_ema.json
                            exec_cluster_E01_zone_basic.json

Usage:
    python scripts/cluster_coverage.py                     # signal_cluster defs only
    python scripts/cluster_coverage.py --all               # all definitions
    python scripts/cluster_coverage.py --cluster Trend     # Trend cluster
    python scripts/cluster_coverage.py --cluster Executor  # Executor cluster
    python scripts/cluster_coverage.py "exec_cluster_*"    # custom glob pattern

ADDING NEW ENUMS:
  If a new enum type is added to transforms, classify it in this file:
  - CODE_FLOW_ENUM_TYPES: each value = different algorithm (add here)
  - PARAMETRIC_ENUM_TYPES: same code, different constant (add here)
  - COSMETIC_ENUM_TYPES: display-only, never affects computation (add here)
  Unknown enums default to code-flow (conservative — will show as uncovered until classified).
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Paths
METADATA_PATH = Path("/home/adesola/EpochDev/ClaudeCodeResearch/docs/transform_metadata.json")
DEFINITIONS_DIR = Path("/home/adesola/EpochDev/ClaudeCodeResearch/project_hand_book/definitions/test_runner")
RESEARCH_DIR = Path("/home/adesola/EpochDev/ClaudeCodeResearch/project_hand_book/research_studies/test_runner")
CAMPAIGNS_DIR = Path("/home/adesola/EpochDev/ClaudeCodeResearch/project_hand_book/campaigns/test_runner")

# ─── Cluster → Category mapping (from EpochAI attachment.py) ─────────────
# 5 functional clusters that the agent actually uses, NOT the 19 backend categories.
# Source: EpochAI/agent_src/subgraphs/build_study/context/attachment.py
CATEGORY_TO_CLUSTER = {
    "Reporter": "Reporter",
    "Executor": "Execution",
    "EventMarker": "Signal",
    "PriceAction": "Signal",
    "ControlFlow": "Signal",
    "DataSource": "DataLoading",
    "DataPrep": "DataLoading",
    "ML": "Compute",
    "Portfolio": "Compute",
    "Volume": "Compute",
    "Volatility": "Compute",
    "Momentum": "Compute",
    "Scalar": "Compute",
    "Aggregate": "Compute",
    # Unmapped → Compute (default)
    "Trend": "Compute",
    "Statistical": "Compute",
    "Utility": "Compute",
    "Math": "Compute",
    "Indicator": "Compute",
    "Factor": "Compute",
}

# Reverse: cluster → [categories]
CLUSTER_TO_CATEGORIES = defaultdict(list)
for cat, cluster in CATEGORY_TO_CLUSTER.items():
    CLUSTER_TO_CATEGORIES[cluster].append(cat)

# ─── Enum classification ────────────────────────────────────────────────────
# Code-flow enums: each value routes to a DIFFERENT implementation or algorithm.
# Example: MAType.sma calls Tulip SMA, MAType.ema calls Tulip EMA — different code.
CODE_FLOW_ENUM_TYPES = {
    "MAType",                   # sma/ema/dema/tema/wma — different Tulip indicators
    "ReturnType", "ReturnsType",  # simple/log/monetary — different formulas
    "BasicVolatilityType",      # parkinson/garman_klass/etc — different estimators
    "VolatilityEstimatorType",  # different vol models
    "PeriodType",               # month/quarter/week/year — different temporal logic
    "BoundaryType",             # start/end — different look-ahead behavior
    "OrdinalType",              # first/second/third/fourth/last — different occurrence matching
    "DayAnchorType",            # monday..friday — different day anchor
    "StringCheckOperation",     # is_alnum/is_alpha/etc — different Arrow compute functions
    "ContainsOperation",        # contains/ends_with/starts_with — different search
    "StringCaseOperation",      # lower/upper/title — different case transform
    "TrimOperation",            # leading/trailing/both — different trim mode
    "StreakDirection",          # up/down/bidirectional — different counting logic
    "AggregationType",         # first/last/min/max/sum/mean/count — different agg
    "NumericDownsampleAgg",    # different downsample aggregation
    "SizeType",                # percent/unit/notional — different position sizing
    "StopUnit",                # percent/atr/price — different stop calculation
    "RiskMeasure",             # std/cvar/etc — different risk computation
    "RiskMode",                # different risk targeting
    "LinkageMethod",           # different clustering linkage
    "KalmanModelType",         # different Kalman filter models
    "CSSelectMode",            # different cross-sectional selection
    "CSSelectDirection",       # top/bottom — different selection direction
    "CorrelationMethod",       # pearson/spearman/kendall — different correlation
    "FillDirection",           # forward/backward — different fill direction
    "FillMethod",              # different fill interpolation
    "RolloverType",            # different futures rollover
    "DistributionType",        # different distribution fit
    "ProfileType",             # different profile calculation
    "DatetimeExtractionType",  # year/month/day/hour — different temporal component
    "FinanceRatioType",        # different financial ratio
    "BoostingType",            # gbdt/dart/goss — different ML boosting
    "ReportingPeriod",         # annual/quarterly/ttm — different fundamental period
}

# Parametric enums: same code path, different target value. NOT separate coverage units.
# Example: Weekday.Friday vs Weekday.Monday — same comparison logic, different constant.
PARAMETRIC_ENUM_TYPES = {
    "Weekday",              # day_of_week just compares to target value
    "Month",                # month_of_year just compares to target value
    "Quarter",              # quarter just compares to target value
    "WeekOfMonth",          # week_of_month just compares to target value
    "HolidayCalendar",      # same algorithm, different calendar data
    "AssetClassUI",         # same filter logic, different field value
    "StockSector",          # same filter logic
    "AssetCategory",        # same filter logic (100+ values)
    "StockExchange",        # same filter logic
    "ReferenceFXPair",      # just selects a ticker
    "ReferenceCryptoPair",  # just selects a ticker
    "ReferenceFutures",     # just selects a ticker
    "ReferenceIndex",       # just selects a ticker
    "ReferenceStock",       # just selects a ticker
    "TreasuryAuctionType",  # just selects auction type
    "TreasurySecurityType",
    "TreasuryTerm",
    "MacroEconomicsIndicator",
    "CalendarSource",
    "EiaFrequency",
    "DividendType",
}

# Cosmetic enums: never affect computation. Always excluded.
COSMETIC_ENUM_TYPES = {
    "Color",
    "DashStyle",
    "AxisValueFormat",
    "CategoryAxisType",
    "SortByValue",
    "StackType",
    "BarMode",
    "CSBarMode",
    "BoxplotMode",
    "CSBoxplotMode",
    "HeatmapMode",
    "TableMode",
    "SizeBy",
    "SessionTimeframe",     # cosmetic for reporters
    "WindowType",           # display window type
    "MLWindowType",
    "ArrayMatchMode",
    "StepType",
}


def is_code_flow_enum(enum_type: str) -> bool:
    """True if this enum type routes to different code paths."""
    if enum_type in CODE_FLOW_ENUM_TYPES:
        return True
    if enum_type in PARAMETRIC_ENUM_TYPES:
        return False
    if enum_type in COSMETIC_ENUM_TYPES:
        return False
    # Unknown — default to code-flow (conservative: assume it matters)
    return True


def load_cluster_units(cluster: str = "Signal") -> dict:
    """
    Load all coverage units for a cluster.
    Each unit = transform_id or transform_id:option=value for code-flow enums.
    Accepts cluster name (Signal, Compute, etc.) or raw category (ControlFlow).
    """
    meta = json.loads(METADATA_PATH.read_text())
    units = {}  # unit_key -> {name, transform_id, option, value, ...}

    # Resolve cluster → categories
    if cluster not in CLUSTER_TO_CATEGORIES:
        valid = ", ".join(sorted(CLUSTER_TO_CATEGORIES.keys()))
        raise ValueError(f"Unknown cluster '{cluster}'. Valid clusters: {valid}")
    target_categories = set(CLUSTER_TO_CATEGORIES[cluster])

    for t in meta:
        if t.get("category") not in target_categories:
            continue
        # Skip generic aliases that resolve to typed variants (e.g., where → where_decimal).
        # These have hasNullTransform=true AND internalUse=true (hidden from agent).
        # Options-only transforms (cppi, kelly, etc.) also have hasNullTransform=true
        # but are NOT aliases — they're real transforms that must be covered.
        if t.get("hasNullTransform", False) and t.get("internalUse", False):
            continue
        # Skip empty-id metadata artifacts
        if not t.get("id", "").strip():
            continue

        tid = t["id"]
        has_code_flow_enum = False

        for opt in t.get("options", []):
            if opt.get("type") != "Select":
                continue
            so = opt.get("selectOption", {})
            enum_type = so.get("enumType", "")
            vals = so.get("enumValues", [])

            if not vals or not is_code_flow_enum(enum_type):
                continue

            has_code_flow_enum = True
            for val in vals:
                key = f"{tid}:{opt['id']}={val}"
                units[key] = {
                    "transform_id": tid,
                    "name": t.get("name", tid),
                    "option": opt["id"],
                    "value": val,
                    "enum_type": enum_type,
                    "internal": t.get("internalUse", False),
                }

        # If no code-flow enums, the transform itself is one unit
        if not has_code_flow_enum:
            units[tid] = {
                "transform_id": tid,
                "name": t.get("name", tid),
                "option": None,
                "value": None,
                "enum_type": None,
                "internal": t.get("internalUse", False),
            }

    return units


def load_definition_coverage(def_path: Path) -> set:
    """Return set of covered unit keys from a study output + source parsing."""
    name = def_path.stem
    covered = set()

    # === Method 1: transforms.json (compiled nodes) ===
    for base in [RESEARCH_DIR, CAMPAIGNS_DIR]:
        transforms_file = base / name / "transforms.json"
        if not transforms_file.exists():
            continue

        nodes = json.loads(transforms_file.read_text())
        for node in nodes:
            ntype = node.get("type", "unknown")
            opts = node.get("options", {})

            for opt_id, opt_val in opts.items():
                val_str = None
                if isinstance(opt_val, str):
                    val_str = opt_val
                elif isinstance(opt_val, dict):
                    val_str = opt_val.get("value") or opt_val.get("id")
                elif isinstance(opt_val, bool):
                    val_str = str(opt_val)

                if val_str:
                    covered.add(f"{ntype}:{opt_id}={val_str}")

            covered.add(ntype)
        break  # found transforms.json, don't check other base

    # === Method 2: Source parsing (catches transforms compiled away) ===
    try:
        defn = json.loads(def_path.read_text())
        source = defn.get("source", "")

        # Extract transform calls: transform_name(...)
        calls = set(re.findall(r'\b([a-z_][a-z0-9_]*)\s*\(', source))
        # Note: min, max, sum are real EpochScript transforms (rolling window aggs).
        # They share names with Python builtins but EpochScript source won't have
        # Python builtins, so it's safe to NOT skip them.
        skip = {"print", "abs", "int", "float", "str", "len", "range", "list",
                "dict", "set", "tuple", "type", "format", "open", "close",
                "any", "all", "map", "filter", "sorted",
                "index", "not", "and", "or", "if", "else", "for", "in", "where"}
        for c in calls:
            if c not in skip:
                covered.add(c)

        # Extract option=EnumType.Value patterns per transform call
        # Pattern: transform_name(..., option=EnumType.Value, ...)
        # Find each transform call block and extract its enum options
        for match in re.finditer(r'(\b[a-z_][a-z0-9_]*)\s*\(([^)]*)\)', source):
            transform_name = match.group(1)
            args_str = match.group(2)
            if transform_name in skip:
                continue

            # Find option=EnumType.Value within this call's args
            for opt_match in re.finditer(r'(\w+)\s*=\s*(\w+)\.(\w+)', args_str):
                opt_name = opt_match.group(1)
                val = opt_match.group(3)
                covered.add(f"{transform_name}:{opt_name}={val}")

            # Also handle option="string_value" patterns
            for opt_match in re.finditer(r'(\w+)\s*=\s*["\'](\w+)["\']', args_str):
                opt_name = opt_match.group(1)
                val = opt_match.group(2)
                covered.add(f"{transform_name}:{opt_name}={val}")

    except Exception:
        pass

    return covered


def find_definitions(pattern: str = "signal_cluster_*", all_defs: bool = False) -> list:
    if all_defs:
        return sorted(DEFINITIONS_DIR.glob("*.json"))
    return sorted(DEFINITIONS_DIR.glob(f"{pattern}.json"))


def analyze_coverage(units: dict, definitions: list):
    """Analyze coverage of all units across definitions."""

    # Gather coverage from all definitions
    all_covered = set()
    def_coverage = {}  # def_name -> covered_keys

    for def_path in definitions:
        cov = load_definition_coverage(def_path)
        def_coverage[def_path.stem] = cov
        all_covered.update(cov)

    # Match units to coverage
    covered_units = {}
    uncovered_units = {}

    for key, unit in units.items():
        tid = unit["transform_id"]

        # Check exact key match (transform:option=value)
        if key in all_covered:
            covered_units[key] = unit
            continue

        # For base units (no enum), check transform presence
        if unit["option"] is None and tid in all_covered:
            covered_units[key] = unit
            continue

        uncovered_units[key] = unit

    # Report
    total = len(units)
    covered = len(covered_units)

    print(f"\n{'='*72}")
    print(f"  CLUSTER COVERAGE REPORT (transform x code-flow-enum = 1 unit)")
    print(f"{'='*72}")
    print(f"  Definitions scanned: {len(definitions)}")
    print(f"  Coverage units:      {total}")
    print(f"  Covered:             {covered} ({100*covered//max(total,1)}%)")
    print(f"  Uncovered:           {total - covered}")

    # Group by transform
    by_transform = defaultdict(lambda: {"covered": [], "uncovered": []})
    for key, unit in covered_units.items():
        by_transform[unit["transform_id"]]["covered"].append(key)
    for key, unit in uncovered_units.items():
        by_transform[unit["transform_id"]]["uncovered"].append(key)

    print(f"\n  {'TRANSFORM':<25s} {'COVERED':>8s} {'MISSING':>8s}  DETAIL")
    print(f"  {'─'*25} {'─'*8} {'─'*8}  {'─'*30}")

    for tid in sorted(by_transform.keys()):
        info = by_transform[tid]
        nc = len(info["covered"])
        nu = len(info["uncovered"])
        total_t = nc + nu
        mark = "✓" if nu == 0 else "✗"

        if total_t == 1:
            # Base transform (no code-flow enums)
            status = "✓" if nc > 0 else "✗"
            print(f"  {status} {tid:<23s} {nc:>8d} {nu:>8d}")
        else:
            # Has code-flow enum variants
            print(f"  {mark} {tid:<23s} {nc:>8d} {nu:>8d}")
            if nu > 0:
                for key in sorted(info["uncovered"]):
                    # Extract option=value from key
                    _, ov = key.split(":", 1) if ":" in key else (key, "")
                    print(f"    ✗ {ov}")

    if uncovered_units:
        print(f"\n  UNCOVERED UNITS ({len(uncovered_units)}):")
        for key in sorted(uncovered_units.keys()):
            u = uncovered_units[key]
            internal = " [internal]" if u["internal"] else ""
            print(f"    {key}{internal}")

    return covered, total


# ─── Cluster → Skills directory mapping ────────────────────────────────────
SKILLS_DIR = Path("/home/adesola/EpochDev/EpochAI/agent_src/prompts/skills")
CLUSTER_TO_SKILLS_DIR = {
    "Execution": "execution",
    "Signal": "signal",
    "Compute": "compute",
    "DataLoading": "data_source",
    "Reporter": "reporting",
}


def analyze_skill_coverage(cluster: str, units: dict):
    """Check that every transform in the cluster is mentioned in at least one skill."""
    skills_subdir = CLUSTER_TO_SKILLS_DIR.get(cluster)
    if not skills_subdir:
        return

    skills_path = SKILLS_DIR / skills_subdir
    if not skills_path.exists():
        print(f"\n  Skills directory not found: {skills_path}")
        return

    # Read all skill files
    skill_contents = {}  # filename -> content
    for md_file in sorted(skills_path.glob("*.md")):
        skill_contents[md_file.stem] = md_file.read_text()

    # Get ALL transform IDs in this cluster (including hasNullTransform=true)
    meta = json.loads(METADATA_PATH.read_text())
    target_categories = set(CLUSTER_TO_CATEGORIES.get(cluster, []))
    transform_ids = sorted(set(
        t["id"] for t in meta
        if t.get("category") in target_categories and t.get("id", "").strip()
    ))

    # Count mentions per transform across all skills
    transform_mentions = {}  # transform_id -> {skill_id: count}
    for tid in transform_ids:
        mentions = {}
        # Match transform_id as a word boundary (avoid partial matches)
        pattern = re.compile(rf'\b{re.escape(tid)}\b')
        for skill_id, content in skill_contents.items():
            count = len(pattern.findall(content))
            if count > 0:
                mentions[skill_id] = count
        transform_mentions[tid] = mentions

    # Report
    total = len(transform_ids)
    covered = sum(1 for m in transform_mentions.values() if m)
    uncovered = total - covered
    total_mentions = sum(sum(m.values()) for m in transform_mentions.values())

    print(f"\n{'='*72}")
    print(f"  SKILL COVERAGE ({skills_subdir}/ — {len(skill_contents)} skill files)")
    print(f"{'='*72}")
    print(f"  Transforms in cluster: {total}")
    print(f"  Mentioned in skills:   {covered} ({100*covered//max(total,1)}%)")
    print(f"  Missing from skills:   {uncovered}")
    print(f"  Total mentions:        {total_mentions}")

    print(f"\n  {'TRANSFORM':<25s} {'MENTIONS':>9s}  SKILLS")
    print(f"  {'─'*25} {'─'*9}  {'─'*40}")

    for tid in transform_ids:
        mentions = transform_mentions[tid]
        total_count = sum(mentions.values())
        mark = "✓" if mentions else "✗"

        if mentions:
            skill_list = ", ".join(f"{sid}({n})" for sid, n in sorted(mentions.items()))
            print(f"  {mark} {tid:<23s} {total_count:>9d}  {skill_list}")
        else:
            print(f"  {mark} {tid:<23s} {total_count:>9d}")

    if uncovered > 0:
        missing = [tid for tid in transform_ids if not transform_mentions[tid]]
        print(f"\n  TRANSFORMS MISSING FROM SKILLS ({uncovered}):")
        for tid in missing:
            print(f"    {tid}")

    return covered, total


def list_clusters():
    """Show all functional clusters with transform/unit counts and categories."""
    meta = json.loads(METADATA_PATH.read_text())

    # Count transforms per cluster
    cluster_transforms = defaultdict(list)
    for t in meta:
        cat = t.get("category", "Unknown")
        cluster = CATEGORY_TO_CLUSTER.get(cat, "Compute")
        cluster_transforms[cluster].append(t["id"])

    print(f"\n{'CLUSTER':<14s} {'TRANSFORMS':>11s}  {'COVERAGE UNITS':>15s}  CATEGORIES")
    print(f"{'─'*14} {'─'*11}  {'─'*15}  {'─'*40}")

    for cluster in sorted(CLUSTER_TO_CATEGORIES.keys()):
        units = load_cluster_units(cluster)
        cats = sorted(CLUSTER_TO_CATEGORIES[cluster])
        print(f"  {cluster:<12s} {len(cluster_transforms[cluster]):>11d}  {len(units):>15d}  {', '.join(cats)}")

    print(f"\n  Total: {len(meta)} transforms")
    print(f"\n  Usage: python scripts/cluster_coverage.py --cluster Signal --all")
    print(f"         python scripts/cluster_coverage.py --cluster Compute --all")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Cluster Coverage Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python scripts/cluster_coverage.py --list-clusters\n"
               "  python scripts/cluster_coverage.py --cluster Trend --all\n"
               "  python scripts/cluster_coverage.py \"exec_cluster_*\"\n"
    )
    parser.add_argument("pattern", nargs="?", default="signal_cluster_*",
                        help="Glob pattern for definition files")
    parser.add_argument("--cluster", default="Signal",
                        help="Functional cluster: Signal, Compute, DataLoading, Reporter, Execution")
    parser.add_argument("--all", action="store_true",
                        help="Scan all definitions")
    parser.add_argument("--list-clusters", action="store_true",
                        help="List all available clusters with transform counts")
    args = parser.parse_args()

    if args.list_clusters:
        list_clusters()
        sys.exit(0)

    units = load_cluster_units(args.cluster)
    definitions = find_definitions(args.pattern, args.all)

    if not definitions:
        print(f"No definitions found matching '{args.pattern}' in {DEFINITIONS_DIR}")
        sys.exit(1)

    if not units:
        print(f"No coverage units for cluster '{args.cluster}'. Run --list-clusters.")
        sys.exit(1)

    covered, total = analyze_coverage(units, definitions)

    # Skill coverage: verify every transform appears in skills
    analyze_skill_coverage(args.cluster, units)

    if covered < total:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
