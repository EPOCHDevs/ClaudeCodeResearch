#!/usr/bin/env python3
"""
Initialize a topic folder for research crawling.

Usage:
    python scripts/init_topic.py "seasonality in financial assets"
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '_', text)
    text = text.strip('_')
    return text[:50]  # Limit length


def init_topic(topic: str, base_dir: Path = None) -> Path:
    """Initialize folder structure for a research topic."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    slug = slugify(topic)
    topic_dir = base_dir / slug

    # Create directory structure
    dirs = [
        topic_dir / "sources" / "quantpedia",
        topic_dir / "sources" / "ssrn",
        topic_dir / "sources" / "barchart",
        topic_dir / "sources" / "stockcharts",
        topic_dir / "sources" / "tradingview",
        topic_dir / "sources" / "investopedia",
        topic_dir / "sources" / "academic",
        topic_dir / "sources" / "misc",
        topic_dir / "images" / "all_charts",
        topic_dir / "tables",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Initialize manifest
    manifest = {
        "topic": topic,
        "slug": slug,
        "created": datetime.utcnow().isoformat() + "Z",
        "sources": [],
        "stats": {
            "total_sources": 0,
            "total_charts": 0,
            "total_tables": 0
        }
    }

    manifest_path = topic_dir / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    # Initialize chart index
    chart_index = {
        "topic": topic,
        "charts": []
    }

    chart_index_path = topic_dir / "images" / "chart_index.json"
    with open(chart_index_path, 'w') as f:
        json.dump(chart_index, f, indent=2)

    print(f"Initialized topic folder: {topic_dir}")
    print(f"Manifest: {manifest_path}")

    return topic_dir


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python init_topic.py '<topic>'")
        sys.exit(1)

    topic = sys.argv[1]
    init_topic(topic)
