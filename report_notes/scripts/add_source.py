#!/usr/bin/env python3
"""
Add a crawled source to a topic's manifest and save content.

Usage:
    python scripts/add_source.py <topic_slug> <url> <title> <content_file>
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


DOMAIN_MAPPING = {
    "quantpedia.com": "quantpedia",
    "www.quantpedia.com": "quantpedia",
    "ssrn.com": "ssrn",
    "papers.ssrn.com": "ssrn",
    "barchart.com": "barchart",
    "www.barchart.com": "barchart",
    "stockcharts.com": "stockcharts",
    "www.stockcharts.com": "stockcharts",
    "tradingview.com": "tradingview",
    "www.tradingview.com": "tradingview",
    "investopedia.com": "investopedia",
    "www.investopedia.com": "investopedia",
    "seekingalpha.com": "misc",
    "arxiv.org": "academic",
    "nber.org": "academic",
    "jstor.org": "academic",
}


def get_domain_folder(url: str) -> str:
    """Determine which source folder a URL belongs to."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    return DOMAIN_MAPPING.get(domain, "misc")


def slugify_title(title: str) -> str:
    """Convert title to filename-safe slug."""
    title = title.lower()
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'[\s_]+', '_', title)
    title = title.strip('_')
    return title[:60]


def add_source(topic_slug: str, url: str, title: str, content: str, base_dir: Path = None) -> dict:
    """Add a source to the topic manifest and save content."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    topic_dir = base_dir / topic_slug
    manifest_path = topic_dir / "manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Topic not initialized: {topic_slug}")

    # Load manifest
    with open(manifest_path) as f:
        manifest = json.load(f)

    # Determine folder and filename
    domain_folder = get_domain_folder(url)
    source_count = len([s for s in manifest["sources"] if s["domain"] == domain_folder])
    file_slug = slugify_title(title)
    filename = f"{source_count + 1:03d}_{file_slug}.md"

    # Create source entry
    source_entry = {
        "url": url,
        "domain": domain_folder,
        "title": title,
        "crawled_at": datetime.utcnow().isoformat() + "Z",
        "file": f"sources/{domain_folder}/{filename}",
        "charts": [],
        "tables": 0
    }

    # Save content as markdown with frontmatter
    source_dir = topic_dir / "sources" / domain_folder
    source_dir.mkdir(parents=True, exist_ok=True)

    content_path = source_dir / filename
    frontmatter = f"""---
url: {url}
title: {title}
domain: {domain_folder}
crawled_at: {source_entry['crawled_at']}
---

"""
    with open(content_path, 'w') as f:
        f.write(frontmatter + content)

    # Create charts subfolder for this source
    charts_dir = source_dir / filename.replace('.md', '') / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    # Update manifest
    manifest["sources"].append(source_entry)
    manifest["stats"]["total_sources"] = len(manifest["sources"])

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"Added source: {content_path}")
    return source_entry


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python add_source.py <topic_slug> <url> <title> <content_file>")
        sys.exit(1)

    topic_slug = sys.argv[1]
    url = sys.argv[2]
    title = sys.argv[3]
    content_file = sys.argv[4]

    with open(content_file) as f:
        content = f.read()

    add_source(topic_slug, url, title, content)
