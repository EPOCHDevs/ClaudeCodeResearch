#!/usr/bin/env python3
"""
Show status and stats for a research topic.

Usage:
    python scripts/status.py <topic_slug>
    python scripts/status.py --list  # List all topics
"""

import argparse
import json
from pathlib import Path


def list_topics(base_dir: Path = None) -> list:
    """List all research topics."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    topics = []
    for manifest in base_dir.glob("*/manifest.json"):
        with open(manifest) as f:
            data = json.load(f)
            topics.append({
                "slug": data["slug"],
                "topic": data["topic"],
                "created": data["created"],
                "sources": data["stats"]["total_sources"],
                "charts": data["stats"]["total_charts"]
            })

    return sorted(topics, key=lambda x: x["created"], reverse=True)


def show_status(topic_slug: str, base_dir: Path = None) -> dict:
    """Show detailed status for a topic."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    topic_dir = base_dir / topic_slug
    manifest_path = topic_dir / "manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Topic not found: {topic_slug}")

    with open(manifest_path) as f:
        manifest = json.load(f)

    # Count files by domain
    domain_counts = {}
    for source in manifest["sources"]:
        domain = source["domain"]
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

    # Count actual files
    actual_files = list(topic_dir.glob("sources/**/*.md"))
    actual_charts = list(topic_dir.glob("**/*.png")) + list(topic_dir.glob("**/*.jpg"))

    return {
        "manifest": manifest,
        "domain_counts": domain_counts,
        "actual_files": len(actual_files),
        "actual_charts": len(actual_charts)
    }


def print_status(topic_slug: str = None, list_all: bool = False):
    """Print formatted status."""
    base_dir = Path(__file__).parent.parent

    if list_all:
        topics = list_topics(base_dir)
        print(f"\n{'TOPIC':<40} {'SOURCES':>8} {'CHARTS':>8} {'CREATED':<20}")
        print("-" * 80)
        for t in topics:
            print(f"{t['topic'][:40]:<40} {t['sources']:>8} {t['charts']:>8} {t['created'][:19]}")
        print(f"\nTotal topics: {len(topics)}")
        return

    status = show_status(topic_slug, base_dir)
    manifest = status["manifest"]

    print(f"\n{'=' * 60}")
    print(f"TOPIC: {manifest['topic']}")
    print(f"{'=' * 60}")
    print(f"Slug: {manifest['slug']}")
    print(f"Created: {manifest['created']}")
    print()

    print("STATS:")
    print(f"  Total Sources: {manifest['stats']['total_sources']}")
    print(f"  Total Charts:  {manifest['stats']['total_charts']}")
    print(f"  Total Tables:  {manifest['stats']['total_tables']}")
    print()

    print("SOURCES BY DOMAIN:")
    for domain, count in sorted(status["domain_counts"].items()):
        print(f"  {domain:<20} {count:>5}")
    print()

    print("RECENT SOURCES:")
    for source in manifest["sources"][-5:]:
        print(f"  [{source['domain']}] {source['title'][:50]}")
    print()

    print("FILE VERIFICATION:")
    print(f"  Manifest sources: {len(manifest['sources'])}")
    print(f"  Actual .md files: {status['actual_files']}")
    print(f"  Actual images:    {status['actual_charts']}")


def main():
    parser = argparse.ArgumentParser(description="Show research topic status")
    parser.add_argument("topic_slug", nargs="?", help="Topic folder slug")
    parser.add_argument("--list", action="store_true", help="List all topics")

    args = parser.parse_args()

    if args.list:
        print_status(list_all=True)
    elif args.topic_slug:
        print_status(topic_slug=args.topic_slug)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
