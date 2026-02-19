#!/usr/bin/env python3
"""
Get study reports (tearsheets, cards, charts, tables).

Usage:
    python get_study_reports.py <job_folder>
    python get_study_reports.py <job_folder> --category <category>
    python get_study_reports.py <job_folder> --cards
    python get_study_reports.py <job_folder> --charts
    python get_study_reports.py <job_folder> --tables
    python get_study_reports.py <job_folder> --verbose

Examples:
    python get_study_reports.py job_data/research_studies/test_runner/my_study
    python get_study_reports.py job_data/research_studies/test_runner/my_study --cards
    python get_study_reports.py job_data/research_studies/test_runner/my_study --category SPY-Stocks
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

sys.path.insert(0, "/home/adesola/EpochDev/EpochBackend/packages/epoch-protos/python")

try:
    from epoch_protos import tearsheet_pb2, table_def_pb2
    from epoch_protos.summary import format_tearsheet_summary
    from epoch_protos.converters import cards_to_compact_list, tearsheet_to_dict
    HAS_PROTOS = True
except ImportError:
    HAS_PROTOS = False


def load_tearsheet(path: Path) -> Optional[tearsheet_pb2.TearSheet]:
    """Load a tearsheet protobuf file."""
    if not HAS_PROTOS:
        return None
    with open(path, 'rb') as f:
        ts = tearsheet_pb2.TearSheet()
        ts.ParseFromString(f.read())
        return ts


def list_categories(job_dir: Path) -> List[str]:
    """List available tearsheet categories."""
    tearsheets_dir = job_dir / "tearsheets"
    if not tearsheets_dir.exists():
        return []
    return [d.name for d in tearsheets_dir.iterdir() if d.is_dir() and (d / "tearsheet.pb").exists()]


def get_cards(job_dir: Path, category: Optional[str] = None) -> Dict[str, Any]:
    """Get card metrics from tearsheet."""
    categories = [category] if category else list_categories(job_dir)
    result = {}

    for cat in categories:
        ts_path = job_dir / "tearsheets" / cat / "tearsheet.pb"
        if not ts_path.exists():
            continue

        ts = load_tearsheet(ts_path)
        if ts is None:
            continue

        cards = cards_to_compact_list(ts)
        result[cat] = {title: {"value": value, "type": vtype} for title, value, vtype in cards}

    return result


def get_charts(job_dir: Path, category: Optional[str] = None) -> Dict[str, List[Dict]]:
    """Get chart info from tearsheet."""
    categories = [category] if category else list_categories(job_dir)
    result = {}

    for cat in categories:
        ts_path = job_dir / "tearsheets" / cat / "tearsheet.pb"
        if not ts_path.exists():
            continue

        ts = load_tearsheet(ts_path)
        if ts is None:
            continue

        charts = []
        for chart in ts.charts:
            chart_info = {
                "title": chart.title,
                "type": tearsheet_pb2.ChartType.Name(chart.type),
                "category": chart.category,
            }
            # Add series count for line charts
            if chart.type == tearsheet_pb2.ChartType.Lines:
                chart_info["series_count"] = len(chart.lines.series)
            elif chart.type == tearsheet_pb2.ChartType.Histogram:
                chart_info["bin_count"] = len(chart.histogram.bins)
            elif chart.type == tearsheet_pb2.ChartType.Box:
                chart_info["box_count"] = len(chart.box.boxes)
            charts.append(chart_info)

        result[cat] = charts

    return result


def get_tables(job_dir: Path, category: Optional[str] = None) -> Dict[str, List[Dict]]:
    """Get table info from tearsheet."""
    categories = [category] if category else list_categories(job_dir)
    result = {}

    for cat in categories:
        ts_path = job_dir / "tearsheets" / cat / "tearsheet.pb"
        if not ts_path.exists():
            continue

        ts = load_tearsheet(ts_path)
        if ts is None:
            continue

        tables = []
        for table in ts.tables.tables:
            # Get row/col counts based on flavor
            row_count = 0
            col_count = len(table.columns)

            if table.flavor == table_def_pb2.TABLE_FLAVOR_DETAILED:
                # Detailed tables use data.rows
                if table.HasField('data') and table.data.rows:
                    row_count = len(table.data.rows)
            elif table.flavor == table_def_pb2.TABLE_FLAVOR_SUMMARY:
                # Summary tables use layout dimensions and summary_data.cells
                if table.HasField('layout'):
                    row_count = table.layout.row_size
                    col_count = table.layout.col_size
                elif table.HasField('summary_data'):
                    row_count = len(table.summary_data.cells)
            elif table.flavor == table_def_pb2.TABLE_FLAVOR_CARDS:
                # Cards use cards_data.cells
                if table.HasField('cards_data'):
                    row_count = len(table.cards_data.cells)

            tables.append({
                "title": table.title,
                "rows": row_count,
                "cols": col_count,
                "category": table.category,
                "flavor": table_def_pb2.TableFlavor.Name(table.flavor) if table.flavor else "Unknown",
            })

        result[cat] = tables

    return result


def print_summary(job_dir: Path, category: Optional[str] = None, verbose: bool = False) -> None:
    """Print full tearsheet summary."""
    categories = [category] if category else list_categories(job_dir)

    for cat in categories:
        ts_path = job_dir / "tearsheets" / cat / "tearsheet.pb"
        if not ts_path.exists():
            continue

        ts = load_tearsheet(ts_path)
        if ts is None:
            continue

        print("=" * 70)
        print(f"TEARSHEET: {cat}")
        print("=" * 70)

        summary = format_tearsheet_summary(ts, cat, max_cards=50)
        print(summary)

        if verbose:
            print("\n--- Raw Card Values ---")
            cards = cards_to_compact_list(ts)
            for title, value, vtype in cards:
                print(f"  {title}: {value} ({vtype})")


def print_cards(job_dir: Path, category: Optional[str] = None) -> None:
    """Print card metrics."""
    cards = get_cards(job_dir, category)
    for cat, metrics in cards.items():
        print(f"\n{cat}:")
        for name, info in metrics.items():
            print(f"  {name}: {info['value']} ({info['type']})")


def print_charts(job_dir: Path, category: Optional[str] = None) -> None:
    """Print chart info."""
    charts = get_charts(job_dir, category)
    for cat, chart_list in charts.items():
        print(f"\n{cat} Charts:")
        for chart in chart_list:
            extra = ""
            if "series_count" in chart:
                extra = f" ({chart['series_count']} series)"
            elif "bin_count" in chart:
                extra = f" ({chart['bin_count']} bins)"
            elif "box_count" in chart:
                extra = f" ({chart['box_count']} boxes)"
            print(f"  {chart['title']}: {chart['type']}{extra} [{chart['category']}]")


def print_tables(job_dir: Path, category: Optional[str] = None) -> None:
    """Print table info."""
    tables = get_tables(job_dir, category)
    for cat, table_list in tables.items():
        print(f"\n{cat} Tables:")
        for table in table_list:
            print(f"  {table['title']}: {table['rows']}x{table['cols']} [{table['category']}] {table['flavor']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("job_folder", type=Path, help="Job folder path")
    parser.add_argument("--category", "-c", type=str, help="Filter to specific category")
    parser.add_argument("--cards", action="store_true", help="Show only cards")
    parser.add_argument("--charts", action="store_true", help="Show only charts")
    parser.add_argument("--tables", action="store_true", help="Show only tables")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show raw values")
    args = parser.parse_args()

    if not HAS_PROTOS:
        print("Error: epoch_protos not installed.")
        print("Run: pip install -e /home/adesola/EpochDev/EpochBackend/packages/epoch-protos/python")
        sys.exit(1)

    if not args.job_folder.exists():
        print(f"Error: Directory not found: {args.job_folder}")
        sys.exit(1)

    categories = list_categories(args.job_folder)
    if not categories:
        print(f"No tearsheets found in {args.job_folder}")
        sys.exit(1)

    if args.cards:
        print_cards(args.job_folder, args.category)
    elif args.charts:
        print_charts(args.job_folder, args.category)
    elif args.tables:
        print_tables(args.job_folder, args.category)
    else:
        print_summary(args.job_folder, args.category, args.verbose)


if __name__ == "__main__":
    main()
