#!/usr/bin/env python3
"""
Extract and download images from crawled markdown content.

Usage:
    python scripts/extract_images.py <topic_slug> <source_file.md>
    python scripts/extract_images.py <topic_slug> --all  # Process all sources
"""

import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urljoin, urlparse


def extract_image_urls(content: str, base_url: str = None) -> list:
    """Extract image URLs from markdown content."""
    patterns = [
        r'!\[([^\]]*)\]\(([^)]+)\)',  # ![alt](url)
        r'<img[^>]+src=["\']([^"\']+)["\']',  # <img src="url">
        r'(https?://[^\s<>"]+\.(?:png|jpg|jpeg|gif|webp|svg))',  # Direct URLs
    ]

    urls = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                # For markdown pattern, URL is second group
                url = match[1] if len(match) > 1 else match[0]
            else:
                url = match

            # Make absolute URL if base provided
            if base_url and not url.startswith('http'):
                url = urljoin(base_url, url)

            if url.startswith('http'):
                urls.append(url)

    return list(set(urls))  # Deduplicate


def download_image(url: str, dest_path: Path, timeout: int = 30) -> bool:
    """Download image using wget."""
    try:
        result = subprocess.run(
            ['wget', '-q', '-O', str(dest_path), '--timeout', str(timeout), url],
            capture_output=True,
            timeout=timeout + 5
        )
        return result.returncode == 0 and dest_path.exists() and dest_path.stat().st_size > 0
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False


def process_source(source_path: Path, topic_dir: Path) -> list:
    """Extract and download images from a source file."""
    with open(source_path) as f:
        content = f.read()

    # Get base URL from frontmatter
    base_url = None
    url_match = re.search(r'^url:\s*(.+)$', content, re.MULTILINE)
    if url_match:
        base_url = url_match.group(1).strip()

    image_urls = extract_image_urls(content, base_url)

    if not image_urls:
        return []

    # Create images folder for this source
    source_name = source_path.stem
    images_dir = source_path.parent / source_name / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    downloaded = []
    for i, url in enumerate(image_urls, 1):
        # Determine extension
        parsed = urlparse(url)
        ext = Path(parsed.path).suffix.lower() or '.png'
        if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
            ext = '.png'

        dest = images_dir / f"img_{i:03d}{ext}"
        print(f"  Downloading: {url[:60]}...")

        if download_image(url, dest):
            downloaded.append({
                "url": url,
                "file": str(dest.relative_to(topic_dir)),
                "source": str(source_path.relative_to(topic_dir))
            })
            print(f"    -> {dest.name}")
        else:
            print(f"    -> FAILED")

    return downloaded


def process_topic(topic_slug: str, source_file: str = None, base_dir: Path = None):
    """Process sources in a topic to extract images."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    topic_dir = base_dir / topic_slug
    manifest_path = topic_dir / "manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Topic not found: {topic_slug}")

    # Find source files
    if source_file:
        sources = [topic_dir / source_file]
    else:
        sources = list(topic_dir.glob("sources/**/*.md"))

    all_images = []
    for source_path in sources:
        if not source_path.exists():
            continue
        print(f"\nProcessing: {source_path.name}")
        images = process_source(source_path, topic_dir)
        all_images.extend(images)

    # Update manifest
    with open(manifest_path) as f:
        manifest = json.load(f)

    manifest["stats"]["total_images"] = len(all_images)

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    # Save image index
    image_index_path = topic_dir / "images" / "extracted_index.json"
    with open(image_index_path, 'w') as f:
        json.dump({"images": all_images}, f, indent=2)

    print(f"\nTotal images downloaded: {len(all_images)}")
    return all_images


def main():
    parser = argparse.ArgumentParser(description="Extract images from crawled content")
    parser.add_argument("topic_slug", help="Topic folder slug")
    parser.add_argument("source_file", nargs="?", help="Specific source file, or --all")
    parser.add_argument("--all", action="store_true", help="Process all sources")

    args = parser.parse_args()

    if args.all or not args.source_file:
        process_topic(args.topic_slug)
    else:
        process_topic(args.topic_slug, args.source_file)


if __name__ == "__main__":
    main()
