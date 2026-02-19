#!/usr/bin/env python3
"""
Exa Research Crawler - Optimal HTML + Image Extraction

Uses the Exa API directly with full parameters:
- includeHtmlTags: true - Preserves HTML structure
- extras.imageLinks: N - Extracts image URLs (including charts)
- extras.links: N - Extracts outbound links
- livecrawl: preferred - Fresh content with cache fallback

Usage:
    # Crawl single URL
    python exa_crawler.py crawl <url> [--output <file>]

    # Search and crawl
    python exa_crawler.py search "<query>" --domains quantpedia.com,ssrn.com

    # Crawl all URLs from a topic manifest
    python exa_crawler.py topic <topic_slug>
"""

import argparse
import json
import os
import re
import sys
import time
import hashlib
import requests
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urljoin
from typing import Optional

# API Configuration
EXA_API_KEY = os.environ.get("EXA_API_KEY", "0146aa92-0fc6-4614-920c-5927baa15ed4")
EXA_API_BASE = "https://api.exa.ai"

# Optimal crawl parameters
DEFAULT_CRAWL_PARAMS = {
    "text": {
        "maxCharacters": 50000,
        "includeHtmlTags": True,
    },
    "extras": {
        "imageLinks": 30,  # Extract up to 30 image URLs
        "links": 20,       # Extract up to 20 outbound links
    },
    "livecrawl": "preferred",
    "livecrawlTimeout": 15000,
}

# Domain categories for organizing sources
DOMAIN_CATEGORIES = {
    # Tier 1: Quantitative
    "quantpedia.com": "quantpedia",
    "www.quantpedia.com": "quantpedia",
    "ssrn.com": "academic",
    "papers.ssrn.com": "academic",
    "nber.org": "academic",
    "www.nber.org": "academic",
    "arxiv.org": "academic",
    # Tier 2: Market Data
    "barchart.com": "market_data",
    "www.barchart.com": "market_data",
    "macrotrends.net": "market_data",
    "www.macrotrends.net": "market_data",
    "tradingview.com": "market_data",
    "www.tradingview.com": "market_data",
    # Tier 3: Analysis
    "investopedia.com": "educational",
    "www.investopedia.com": "educational",
    "babypips.com": "educational",
    "www.babypips.com": "educational",
    "forex.com": "broker_research",
    "www.forex.com": "broker_research",
    # Research/Blogs
    "macrosynergy.com": "research",
    "je-suis-tm.github.io": "quant_blog",
}


def get_domain_category(url: str) -> str:
    """Get category for a URL based on domain."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    return DOMAIN_CATEGORIES.get(domain, "misc")


def exa_request(endpoint: str, payload: dict) -> dict:
    """Make authenticated request to Exa API."""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": EXA_API_KEY,
    }
    response = requests.post(
        f"{EXA_API_BASE}/{endpoint}",
        headers=headers,
        json=payload,
        timeout=60
    )
    response.raise_for_status()
    return response.json()


def crawl_url(url: str, max_chars: int = 50000) -> dict:
    """
    Crawl a URL with optimal parameters for research.

    Returns:
        {
            "url": str,
            "title": str,
            "text": str (with HTML tags),
            "image": str (main image),
            "favicon": str,
            "imageLinks": [str] (all extracted image URLs),
            "links": [str] (outbound links),
            "crawled_at": str,
            "source": "cached" | "livecrawl"
        }
    """
    params = {
        "urls": [url],
        **DEFAULT_CRAWL_PARAMS
    }
    params["text"]["maxCharacters"] = max_chars

    result = exa_request("contents", params)

    if not result.get("results"):
        raise ValueError(f"No results returned for {url}")

    r = result["results"][0]
    status = result.get("statuses", [{}])[0]

    return {
        "url": r.get("url", url),
        "title": r.get("title", ""),
        "author": r.get("author"),
        "text": r.get("text", ""),
        "image": r.get("image"),
        "favicon": r.get("favicon"),
        "imageLinks": r.get("extras", {}).get("imageLinks", []),
        "links": r.get("extras", {}).get("links", []),
        "crawled_at": datetime.now(timezone.utc).isoformat(),
        "source": status.get("source", "unknown"),
        "cost": result.get("costDollars", {}).get("total", 0),
    }


def search_and_crawl(
    query: str,
    num_results: int = 10,
    include_domains: list = None,
    exclude_domains: list = None,
    category: str = None,
    crawl_results: bool = True,
) -> list:
    """
    Search Exa and optionally crawl all results.

    Args:
        query: Search query
        num_results: Number of results (1-100)
        include_domains: Only include these domains
        exclude_domains: Exclude these domains
        category: Filter by category (news, research paper, company, etc.)
        crawl_results: Whether to crawl each result for full content

    Returns:
        List of search results with optional crawled content
    """
    payload = {
        "query": query,
        "numResults": num_results,
        "type": "auto",
    }

    if include_domains:
        payload["includeDomains"] = include_domains
    if exclude_domains:
        payload["excludeDomains"] = exclude_domains
    if category:
        payload["category"] = category

    # If crawling, include contents in search to save API calls
    if crawl_results:
        payload["contents"] = DEFAULT_CRAWL_PARAMS

    result = exa_request("search", payload)

    results = []
    for r in result.get("results", []):
        item = {
            "url": r.get("url"),
            "title": r.get("title"),
            "score": r.get("score"),
            "publishedDate": r.get("publishedDate"),
            "author": r.get("author"),
        }

        if crawl_results:
            item["text"] = r.get("text", "")
            item["image"] = r.get("image")
            item["imageLinks"] = r.get("extras", {}).get("imageLinks", [])
            item["links"] = r.get("extras", {}).get("links", [])

        results.append(item)

    return results


def filter_chart_images(image_links: list, url: str) -> list:
    """
    Filter image URLs to identify likely charts vs logos/icons.

    Prioritizes:
    - Images with 'chart', 'graph', 'plot' in URL/filename
    - Images from data visualization paths
    - Larger dimension indicators

    Deprioritizes:
    - Logos, icons, banners, avatars
    - Social media share images
    - Ad/tracking pixels
    """
    charts = []
    other = []

    skip_patterns = [
        r'logo', r'icon', r'favicon', r'avatar', r'banner',
        r'button', r'sprite', r'pixel', r'tracking', r'ad[_-]',
        r'share', r'social', r'twitter', r'facebook', r'linkedin',
        r'pinterest', r'email', r'print', r'\d+x\d+\.', r'thumb',
    ]

    chart_patterns = [
        r'chart', r'graph', r'plot', r'figure', r'fig[_-]?\d',
        r'performance', r'returns', r'equity', r'drawdown',
        r'correlation', r'backtest', r'strategy', r'seasonal',
        r'heatmap', r'histogram', r'scatter', r'line[_-]',
    ]

    for img_url in image_links:
        img_lower = img_url.lower()

        # Skip if matches skip patterns
        if any(re.search(p, img_lower) for p in skip_patterns):
            continue

        # Prioritize if matches chart patterns
        if any(re.search(p, img_lower) for p in chart_patterns):
            charts.append(img_url)
        else:
            other.append(img_url)

    return charts + other


def download_image(url: str, output_path: Path, timeout: int = 30) -> bool:
    """Download an image to local file."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"
        }
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"  Failed to download {url}: {e}", file=sys.stderr)
        return False


def save_source_to_topic(
    topic_dir: Path,
    crawl_result: dict,
    download_images: bool = True,
) -> dict:
    """
    Save a crawled source to a topic directory.

    Creates:
    - sources/<category>/NNN_<slug>.md (content with frontmatter)
    - sources/<category>/NNN_<slug>/charts/ (downloaded chart images)
    - Updates manifest.json
    """
    manifest_path = topic_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Topic not initialized: {topic_dir}")

    with open(manifest_path) as f:
        manifest = json.load(f)

    url = crawl_result["url"]
    title = crawl_result.get("title", "Untitled")
    category = get_domain_category(url)

    # Count existing sources in this category
    source_count = len([s for s in manifest["sources"] if s.get("domain") == category])

    # Create slug from title
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_]+', '_', slug).strip('_')[:50]

    filename = f"{source_count + 1:03d}_{slug}"

    # Create directories
    source_dir = topic_dir / "sources" / category
    source_dir.mkdir(parents=True, exist_ok=True)

    charts_dir = source_dir / filename / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    # Filter and download chart images
    chart_files = []
    if download_images and crawl_result.get("imageLinks"):
        filtered_images = filter_chart_images(crawl_result["imageLinks"], url)

        for i, img_url in enumerate(filtered_images[:15]):  # Max 15 images per source
            # Determine extension
            parsed = urlparse(img_url)
            ext = Path(parsed.path).suffix.lower() or ".png"
            if ext not in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]:
                ext = ".png"

            chart_path = charts_dir / f"chart_{i+1:02d}{ext}"

            if download_image(img_url, chart_path):
                chart_files.append({
                    "file": str(chart_path.relative_to(topic_dir)),
                    "source_url": img_url,
                    "index": i + 1,
                })
                print(f"  Downloaded: {chart_path.name}")

    # Save main content
    content_path = source_dir / f"{filename}.md"

    # Build frontmatter
    frontmatter = {
        "url": url,
        "title": title,
        "domain": category,
        "crawled_at": crawl_result["crawled_at"],
        "source": crawl_result.get("source", "unknown"),
        "author": crawl_result.get("author"),
        "main_image": crawl_result.get("image"),
        "chart_count": len(chart_files),
        "image_links": crawl_result.get("imageLinks", [])[:30],  # Store first 30
        "outbound_links": crawl_result.get("links", [])[:20],
    }

    # Write markdown file
    with open(content_path, 'w') as f:
        f.write("---\n")
        for key, value in frontmatter.items():
            if value is not None:
                if isinstance(value, list):
                    f.write(f"{key}:\n")
                    for item in value:
                        f.write(f"  - {item}\n")
                else:
                    f.write(f"{key}: {value}\n")
        f.write("---\n\n")
        f.write(crawl_result.get("text", ""))

    # Update manifest
    source_entry = {
        "url": url,
        "domain": category,
        "title": title,
        "crawled_at": crawl_result["crawled_at"],
        "file": str(content_path.relative_to(topic_dir)),
        "charts": [c["file"] for c in chart_files],
        "tables": 0,  # TODO: Extract tables from HTML
    }

    manifest["sources"].append(source_entry)
    manifest["stats"]["total_sources"] = len(manifest["sources"])
    manifest["stats"]["total_charts"] = sum(len(s.get("charts", [])) for s in manifest["sources"])

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"Saved: {content_path}")
    return source_entry


def crawl_topic_urls(topic_slug: str, urls: list, base_dir: Path = None):
    """Crawl multiple URLs and save to a topic."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    topic_dir = base_dir / topic_slug

    results = []
    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] Crawling: {url}")
        try:
            crawl_result = crawl_url(url)
            entry = save_source_to_topic(topic_dir, crawl_result)
            results.append(entry)

            # Rate limiting
            if i < len(urls) - 1:
                time.sleep(1)
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)

    return results


def main():
    parser = argparse.ArgumentParser(description="Exa Research Crawler")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Crawl a single URL")
    crawl_parser.add_argument("url", help="URL to crawl")
    crawl_parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    crawl_parser.add_argument("--max-chars", type=int, default=50000, help="Max characters")
    crawl_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search and crawl")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--num", "-n", type=int, default=10, help="Number of results")
    search_parser.add_argument("--domains", help="Comma-separated domains to include")
    search_parser.add_argument("--exclude", help="Comma-separated domains to exclude")
    search_parser.add_argument("--category", help="Filter by category")
    search_parser.add_argument("--no-crawl", action="store_true", help="Skip crawling")
    search_parser.add_argument("--output", "-o", help="Output file")

    # Topic command
    topic_parser = subparsers.add_parser("topic", help="Crawl URLs for a topic")
    topic_parser.add_argument("topic_slug", help="Topic slug/folder name")
    topic_parser.add_argument("urls", nargs="*", help="URLs to crawl (or reads from stdin)")

    args = parser.parse_args()

    if args.command == "crawl":
        result = crawl_url(args.url, args.max_chars)

        if args.json:
            output = json.dumps(result, indent=2)
        else:
            output = f"# {result['title']}\n\n"
            output += f"URL: {result['url']}\n"
            output += f"Crawled: {result['crawled_at']}\n"
            output += f"Source: {result['source']}\n"
            output += f"Images: {len(result['imageLinks'])}\n"
            output += f"Links: {len(result['links'])}\n\n"
            output += "## Image URLs\n"
            for img in result['imageLinks'][:20]:
                output += f"- {img}\n"
            output += f"\n## Content\n\n{result['text']}"

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
        else:
            print(output)

    elif args.command == "search":
        include = args.domains.split(",") if args.domains else None
        exclude = args.exclude.split(",") if args.exclude else None

        results = search_and_crawl(
            args.query,
            num_results=args.num,
            include_domains=include,
            exclude_domains=exclude,
            category=args.category,
            crawl_results=not args.no_crawl,
        )

        output = json.dumps(results, indent=2)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
        else:
            print(output)

    elif args.command == "topic":
        urls = args.urls
        if not urls:
            # Read from stdin
            urls = [line.strip() for line in sys.stdin if line.strip()]

        if not urls:
            print("No URLs provided", file=sys.stderr)
            sys.exit(1)

        crawl_topic_urls(args.topic_slug, urls)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
