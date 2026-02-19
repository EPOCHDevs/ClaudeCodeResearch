#!/usr/bin/env python3
"""
Add chart metadata to a topic's chart index.

Usage:
    python scripts/add_chart.py <topic_slug> <source_url> <chart_file> [--title "Chart Title"]
"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path


def add_chart(
    topic_slug: str,
    source_url: str,
    chart_file: str,
    title: str = None,
    chart_type: str = None,
    x_axis: str = None,
    y_axis: str = None,
    metrics: list = None,
    element_selector: str = None,
    base_dir: Path = None
) -> dict:
    """Add chart to index and copy to all_charts folder."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    topic_dir = base_dir / topic_slug
    chart_index_path = topic_dir / "images" / "chart_index.json"
    all_charts_dir = topic_dir / "images" / "all_charts"

    if not chart_index_path.exists():
        raise FileNotFoundError(f"Topic not initialized: {topic_slug}")

    # Load chart index
    with open(chart_index_path) as f:
        chart_index = json.load(chart_index_path)

    chart_path = Path(chart_file)
    if not chart_path.exists():
        raise FileNotFoundError(f"Chart file not found: {chart_file}")

    # Determine chart number
    chart_num = len(chart_index["charts"]) + 1
    new_filename = f"chart_{chart_num:03d}{chart_path.suffix}"

    # Copy to all_charts
    dest_path = all_charts_dir / new_filename
    shutil.copy(chart_path, dest_path)

    # Create chart entry
    chart_entry = {
        "id": chart_num,
        "source_url": source_url,
        "original_file": str(chart_path),
        "indexed_file": f"images/all_charts/{new_filename}",
        "title": title or f"Chart {chart_num}",
        "chart_type": chart_type,
        "x_axis": x_axis,
        "y_axis": y_axis,
        "metrics_shown": metrics or [],
        "element_selector": element_selector,
        "captured_at": datetime.utcnow().isoformat() + "Z"
    }

    # Save chart metadata alongside original
    metadata_path = chart_path.with_suffix('.json')
    with open(metadata_path, 'w') as f:
        json.dump(chart_entry, f, indent=2)

    # Update chart index
    chart_index["charts"].append(chart_entry)

    with open(chart_index_path, 'w') as f:
        json.dump(chart_index, f, indent=2)

    # Update manifest stats
    manifest_path = topic_dir / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    manifest["stats"]["total_charts"] = len(chart_index["charts"])

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"Added chart: {dest_path}")
    return chart_entry


def main():
    parser = argparse.ArgumentParser(description="Add chart to topic index")
    parser.add_argument("topic_slug", help="Topic folder slug")
    parser.add_argument("source_url", help="URL where chart was found")
    parser.add_argument("chart_file", help="Path to chart image file")
    parser.add_argument("--title", help="Chart title")
    parser.add_argument("--type", dest="chart_type", help="Chart type (line, bar, etc.)")
    parser.add_argument("--x-axis", help="X-axis label")
    parser.add_argument("--y-axis", help="Y-axis label")
    parser.add_argument("--metrics", nargs="+", help="Metrics shown in chart")
    parser.add_argument("--selector", help="CSS selector used to capture")

    args = parser.parse_args()

    add_chart(
        topic_slug=args.topic_slug,
        source_url=args.source_url,
        chart_file=args.chart_file,
        title=args.title,
        chart_type=args.chart_type,
        x_axis=args.x_axis,
        y_axis=args.y_axis,
        metrics=args.metrics,
        element_selector=args.selector
    )


if __name__ == "__main__":
    main()
