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
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add EpochAI to path for provider imports
sys.path.insert(0, os.path.expanduser("~/EpochDev/EpochAI"))

from agent_src.providers import LocalDataProvider


def _load_provider_data(job_dir: Path, category: Optional[str] = None):
    """Load tearsheet data via LocalDataProvider.

    Returns (provider, categories, tearsheets) where tearsheets maps
    category -> dict.
    """
    provider = LocalDataProvider(job_dir)

    async def _load():
        cats = await provider.list_tearsheet_categories("")
        if category:
            cats = [c for c in cats if c == category]
        tearsheets = {}
        for cat in cats:
            try:
                tearsheets[cat] = await provider.get_tearsheet_dict("", cat)
            except FileNotFoundError:
                pass
        return cats, tearsheets

    cats, tearsheets = asyncio.run(_load())
    return provider, cats, tearsheets


def _load_dashboard_schemas(job_dir: Path, categories: List[str]):
    """Load dashboard schemas for all categories."""
    provider = LocalDataProvider(job_dir)

    async def _load():
        schemas = {}
        for cat in categories:
            try:
                schemas[cat] = await provider.get_dashboard_schema("", cat)
            except (FileNotFoundError, Exception):
                pass
        return schemas

    return asyncio.run(_load())


def print_cards(tearsheets: Dict) -> None:
    """Print card metrics from tearsheet dicts."""
    for cat, ts in tearsheets.items():
        cards = ts.get("cards", [])
        if not cards:
            continue
        print(f"\n{'='*60}")
        print(f"CARDS: {cat}")
        print(f"{'='*60}")
        for card in cards:
            title = card.get("title", "?")
            value = card.get("value", "?")
            vtype = card.get("type", "?")
            color = card.get("color", "")
            color_str = f" [{color}]" if color else ""
            print(f"  {title}: {value} ({vtype}){color_str}")


def print_charts(tearsheets: Dict, schemas: Dict, verbose: bool = False) -> None:
    """Print chart info from tearsheet dicts + dashboard schemas."""
    for cat, ts in tearsheets.items():
        schema = schemas.get(cat, {})
        charts = schema.get("charts", [])
        if not charts:
            continue
        print(f"\n{'='*60}")
        print(f"CHARTS: {cat}")
        print(f"{'='*60}")
        for i, chart in enumerate(charts):
            title = chart.get("title", "untitled")
            chart_type = chart.get("type", "?")
            category = chart.get("category", "?")
            data_id = chart.get("data_id", "")
            series = chart.get("series", [])
            bar_series = chart.get("bar_series", [])
            scatter_series = chart.get("scatter_series", [])

            all_series = series + bar_series + scatter_series
            series_names = [s.get("name", "?") for s in all_series]

            y_axis = chart.get("y_axis", {})
            x_axis = chart.get("x_axis", {})
            y_label = y_axis.get("label", "")
            y_type = y_axis.get("value_type", "")
            ref_lines = chart.get("reference_lines", [])

            print(f"\n  [{i}] {title}")
            print(f"      Type: {chart_type} | Category: {category}")
            if series_names:
                print(f"      Series ({len(all_series)}): {', '.join(series_names)}")
            if y_label:
                print(f"      Y-axis: {y_label} ({y_type})")
            if ref_lines:
                for rl in ref_lines:
                    print(f"      RefLine: value={rl.get('value')}, color={rl.get('color')}")
            if data_id:
                print(f"      Data: {data_id}")

            # If verbose, try to load the arrow data
            if verbose and data_id:
                _print_chart_data_summary(tearsheets, cat, data_id, all_series)


def _print_chart_data_summary(tearsheets: Dict, cat: str, data_id: str, series: List) -> None:
    """Load arrow data for a chart and print summary stats."""
    try:
        import pyarrow.ipc as ipc
        import pyarrow as pa

        # Find the arrow file - check tearsheet dir
        ts = tearsheets.get(cat, {})
        # The data is typically at tearsheets/<cat>/<data_id>.arrow
        # We need to find it from the job dir
    except ImportError:
        pass


def print_tables(tearsheets: Dict, schemas: Dict) -> None:
    """Print table info from tearsheet dicts + dashboard schemas."""
    for cat, ts in tearsheets.items():
        schema = schemas.get(cat, {})
        tables = schema.get("tables", []) if schema else []

        # Also check tearsheet dict for tables
        ts_tables = ts.get("tables", [])
        all_tables = tables or ts_tables

        if not all_tables:
            continue
        print(f"\n{'='*60}")
        print(f"TABLES: {cat}")
        print(f"{'='*60}")
        for i, table in enumerate(all_tables):
            title = table.get("title", "untitled")
            category = table.get("category", "?")
            rows = table.get("rows", "?")
            cols = table.get("cols", "?")

            # For summary tables with layout
            layout = table.get("layout", {})
            if layout:
                row_headers = layout.get("row_headers", [])
                col_headers = layout.get("col_headers", [])
                cells = layout.get("cells", [])
                print(f"\n  [{i}] {title} [{category}]")
                print(f"      Layout: {len(row_headers)}x{len(col_headers)}")
                if row_headers:
                    print(f"      Rows: {', '.join(row_headers)}")
                if col_headers:
                    print(f"      Cols: {', '.join(col_headers)}")
                if cells:
                    for cell in cells:
                        val = cell.get("value", cell.get("formatted_value", "?"))
                        cell_title = cell.get("title", "")
                        r, c = cell.get("grid_row", "?"), cell.get("grid_col", "?")
                        print(f"      [{r},{c}] {cell_title}: {val}")
            else:
                print(f"\n  [{i}] {title}: {rows}x{cols} [{category}]")


def print_full_summary(tearsheets: Dict, schemas: Dict, verbose: bool = False) -> None:
    """Print everything."""
    for cat in tearsheets:
        print(f"\n{'='*70}")
        print(f"TEARSHEET: {cat}")
        print(f"{'='*70}")

        ts = tearsheets[cat]
        schema = schemas.get(cat, {})

        # Cards
        cards = ts.get("cards", [])
        if cards:
            print(f"\n  --- Cards ({len(cards)}) ---")
            for card in cards:
                title = card.get("title", "?")
                value = card.get("value", "?")
                vtype = card.get("type", "")
                print(f"    {title}: {value} ({vtype})")

        # Charts
        charts = schema.get("charts", [])
        if charts:
            print(f"\n  --- Charts ({len(charts)}) ---")
            for chart in charts:
                title = chart.get("title", "untitled")
                ctype = chart.get("type", "?")
                all_series = chart.get("series", []) + chart.get("bar_series", []) + chart.get("scatter_series", [])
                names = [s.get("name", "?") for s in all_series]
                y_label = chart.get("y_axis", {}).get("label", "")
                data_id = chart.get("data_id", "")
                extra = f" | y={y_label}" if y_label else ""
                print(f"    {title}: {ctype} ({len(all_series)} series: {', '.join(names)}){extra}")
                if data_id:
                    print(f"      data_id={data_id}")

        # Tables
        tables = schema.get("tables", [])
        if tables:
            print(f"\n  --- Tables ({len(tables)}) ---")
            for table in tables:
                title = table.get("title", "untitled")
                print(f"    {title}")

        # Event markers
        event_markers = schema.get("event_marker_notes", ts.get("event_markers", {}))
        if event_markers:
            print(f"\n  --- Event Markers ---")
            for key, val in event_markers.items():
                print(f"    {key}: {val}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("job_folder", type=Path, help="Job folder path")
    parser.add_argument("--category", "-c", type=str, help="Filter to specific category")
    parser.add_argument("--cards", action="store_true", help="Show only cards")
    parser.add_argument("--charts", action="store_true", help="Show only charts")
    parser.add_argument("--tables", action="store_true", help="Show only tables")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show raw values")
    args = parser.parse_args()

    if not args.job_folder.exists():
        print(f"Error: Directory not found: {args.job_folder}")
        sys.exit(1)

    _, cats, tearsheets = _load_provider_data(args.job_folder, args.category)
    schemas = _load_dashboard_schemas(args.job_folder, cats)

    if not tearsheets:
        print(f"No tearsheets found in {args.job_folder}")
        sys.exit(1)

    if args.cards:
        print_cards(tearsheets)
    elif args.charts:
        print_charts(tearsheets, schemas, args.verbose)
    elif args.tables:
        print_tables(tearsheets, schemas)
    else:
        print_full_summary(tearsheets, schemas, args.verbose)


if __name__ == "__main__":
    main()
