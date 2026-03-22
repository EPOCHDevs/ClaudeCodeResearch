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
import os
import asyncio
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add EpochAI to path for provider imports
sys.path.insert(0, os.path.expanduser("~/EpochDev/EpochAI"))
# Add proto path for tearsheet parsing helpers
sys.path.insert(0, os.path.expanduser("~/EpochDev/EpochBackend/packages/epoch-protos/python"))

from agent_src.providers import LocalDataProvider

try:
    from epoch_protos import table_def_pb2
    from epoch_protos.summary import format_tearsheet_summary
    from epoch_protos.converters import cards_to_compact_list
    HAS_PROTOS = True
except ImportError:
    HAS_PROTOS = False


def _load_provider_data(job_dir: Path, category: Optional[str] = None):
    """Load tearsheet data via LocalDataProvider.

    Returns (provider, categories, tearsheets) where tearsheets maps
    category -> proto object.
    """
    provider = LocalDataProvider(job_dir)

    async def _load():
        cats = await provider.list_tearsheet_categories("")
        if category:
            cats = [c for c in cats if c == category]
        tearsheets = {}
        for cat in cats:
            try:
                tearsheets[cat] = await provider.get_tearsheet_proto("", cat)
            except FileNotFoundError:
                pass
        return cats, tearsheets

    cats, tearsheets = asyncio.run(_load())
    return provider, cats, tearsheets


def get_cards(tearsheets: Dict) -> Dict[str, Any]:
    """Get card metrics from tearsheets."""
    result = {}
    for cat, ts in tearsheets.items():
        cards = cards_to_compact_list(ts)
        result[cat] = {title: {"value": value, "type": vtype} for title, value, vtype in cards}
    return result


def get_charts(tearsheets: Dict) -> Dict[str, List[Dict]]:
    """Get chart info from tearsheets."""
    result = {}
    for cat, ts in tearsheets.items():
        charts = []
        for chart in ts.charts.charts:
            chart_type_name = chart.WhichOneof('chart_type') if hasattr(chart, 'WhichOneof') else None
            if not chart_type_name:
                continue
            defn = getattr(chart, chart_type_name, None)
            if defn is None:
                continue
            chart_def = getattr(defn, 'chart_def', None)
            chart_info = {
                "title": chart_def.title if chart_def else "?",
                "type": chart_type_name.replace('_def', ''),
                "category": chart_def.category if chart_def else "?",
            }
            if chart_type_name in ('numeric_lines_def', 'lines_def'):
                chart_info["series_count"] = len(defn.lines)
            elif chart_type_name == 'pie_def':
                slices = []
                for ring in defn.data:
                    for pt in ring.points:
                        slices.append({"name": pt.name, "value": pt.y})
                chart_info["slice_count"] = len(slices)
                chart_info["slices"] = slices
            elif chart_type_name == 'histogram_def':
                if defn.series:
                    chart_info["series_count"] = len(defn.series)
                    chart_info["bin_count"] = sum(len(s.bins) for s in defn.series)
                    bins_data = []
                    for s in defn.series:
                        series_bins = [{"start": b.bin_start, "end": b.bin_end, "count": b.count} for b in s.bins]
                        bins_data.append({"name": s.name, "bins": series_bins})
                    chart_info["histogram_series"] = bins_data
                    if defn.HasField('analytics'):
                        chart_info["analytics"] = {
                            "mean": defn.analytics.mean,
                            "std_dev": defn.analytics.std_dev,
                            "sample_count": defn.analytics.sample_count,
                        }
                else:
                    chart_info["bin_count"] = defn.bins_count
            elif chart_type_name == 'box_plot_def':
                chart_info["type"] = "box"
            charts.append(chart_info)
        result[cat] = charts
    return result


def get_tables(tearsheets: Dict) -> Dict[str, List[Dict]]:
    """Get table info from tearsheets."""
    result = {}
    for cat, ts in tearsheets.items():
        tables = []
        for table in ts.tables.tables:
            row_count = 0
            col_count = len(table.columns)

            if table.flavor == table_def_pb2.TABLE_FLAVOR_DETAILED:
                if table.HasField('data') and table.data.rows:
                    row_count = len(table.data.rows)
            elif table.flavor == table_def_pb2.TABLE_FLAVOR_SUMMARY:
                if table.HasField('layout'):
                    row_count = table.layout.row_size
                    col_count = table.layout.col_size
                elif table.HasField('summary_data'):
                    row_count = len(table.summary_data.cells)
            elif table.flavor == table_def_pb2.TABLE_FLAVOR_CARDS:
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


def print_summary(tearsheets: Dict, verbose: bool = False) -> None:
    """Print full tearsheet summary."""
    for cat, ts in tearsheets.items():
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


def print_cards(tearsheets: Dict) -> None:
    """Print card metrics."""
    cards = get_cards(tearsheets)
    for cat, metrics in cards.items():
        print(f"\n{cat}:")
        for name, info in metrics.items():
            print(f"  {name}: {info['value']} ({info['type']})")


def print_charts(tearsheets: Dict) -> None:
    """Print chart info."""
    charts = get_charts(tearsheets)
    for cat, chart_list in charts.items():
        print(f"\n{cat} Charts:")
        for chart in chart_list:
            extra = ""
            if "slice_count" in chart:
                total = sum(s["value"] for s in chart["slices"])
                if total > 0:
                    parts = [f"{s['name']}={s['value']/total*100:.1f}%" for s in chart["slices"]]
                else:
                    parts = [f"{s['name']}={s['value']:.2f}" for s in chart["slices"]]
                extra = f" ({chart['slice_count']} slices: {', '.join(parts)})"
            elif "series_count" in chart and "histogram_series" in chart:
                extra = f" ({chart['bin_count']} bins, {chart['series_count']} series)"
                if "analytics" in chart:
                    a = chart["analytics"]
                    extra += f" [mean={a['mean']:.4f}, std={a['std_dev']:.4f}, n={a['sample_count']}]"
            elif "series_count" in chart:
                extra = f" ({chart['series_count']} series)"
            elif "bin_count" in chart:
                extra = f" ({chart['bin_count']} bins)"
            elif "box_count" in chart:
                extra = f" ({chart['box_count']} boxes)"
            print(f"  {chart['title']}: {chart['type']}{extra} [{chart['category']}]")


def print_tables(tearsheets: Dict) -> None:
    """Print table info."""
    tables = get_tables(tearsheets)
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

    _, cats, tearsheets = _load_provider_data(args.job_folder, args.category)

    if not tearsheets:
        print(f"No tearsheets found in {args.job_folder}")
        sys.exit(1)

    if args.cards:
        print_cards(tearsheets)
    elif args.charts:
        print_charts(tearsheets)
    elif args.tables:
        print_tables(tearsheets)
    else:
        print_summary(tearsheets, args.verbose)


if __name__ == "__main__":
    main()
