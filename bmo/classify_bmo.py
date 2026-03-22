#!/usr/bin/env python3
"""
Phase 2: Classify BMO extracted images using Claude Vision API.

Usage:
    python classify_bmo.py                # Classify all + organize
    python classify_bmo.py --dry-run      # Preview without API calls
    python classify_bmo.py --organize     # Skip classification, just organize
    python classify_bmo.py --stats        # Show classification stats
"""

import anthropic
import base64
import json
import os
import re
import shutil
import sys
import csv
import time
from pathlib import Path

BMO_DIR = Path(__file__).parent
STAGING_DIR = BMO_DIR / "staging"
ORGANIZED_DIR = BMO_DIR / "bmo_organized"
MANIFEST_PATH = STAGING_DIR / "staging_manifest.json"

API_KEY = "REDACTED"

CLASSIFY_PROMPT = """You are classifying images extracted from BMO Capital Markets FICC Macro Strategy reports ("Making Sense of Macro" by Mark McCormick).

Given an image and its surrounding text context, classify it and provide metadata.

## Classification Rules

**chart** — Financial chart: price charts, line charts, scatter plots, bar charts, area charts, stacked bar charts, any data visualization showing FX, rates, macro, or positioning data. This includes BMO proprietary indicators (MOOD, GPS, MAPS).

**table** — Data table: performance tables, comparison tables, positioning summaries, economic calendars, any structured tabular data.

**decorative** — Non-analytical images: logos, banners, author photos, decorative elements.

**skip** — Corrupted, too small, duplicates, or disclosure/legal page content.

## Text Context
- Text above image: {text_above}
- Text below image: {text_below}
- Nearest heading: {nearest_heading}
- Source: {source_pdf} (page {page})

## Response Format
Respond with ONLY a JSON object (no markdown, no backticks):
{{"classified": "chart|table|decorative|skip", "title": "Descriptive title for the chart/table", "slug": "kebab-case-slug-name", "insight": "One sentence describing what this image shows or why it matters"}}

Rules for title/slug:
- For chart/table: Use the chart title if visible in the image, otherwise derive from context
- Slug must be lowercase kebab-case, no special characters
- Include date context in slug if helpful for uniqueness
"""


def load_manifest() -> list[dict]:
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def save_manifest(entries: list[dict]):
    with open(MANIFEST_PATH, "w") as f:
        json.dump(entries, f, indent=2)

    csv_path = STAGING_DIR / "staging_manifest.csv"
    if entries:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=entries[0].keys())
            writer.writeheader()
            writer.writerows(entries)


def classify_image(client: anthropic.Anthropic, entry: dict) -> dict:
    """Send an image to Claude for classification."""
    img_path = STAGING_DIR / entry["staging_path"]
    if not img_path.exists():
        return {"classified": "skip", "title": "Missing image", "slug": "missing", "insight": "Image file not found"}

    img_data = img_path.read_bytes()
    img_b64 = base64.standard_b64encode(img_data).decode("utf-8")

    ext = entry["format"].lower()
    media_type_map = {"png": "image/png", "jpeg": "image/jpeg", "jpg": "image/jpeg"}
    media_type = media_type_map.get(ext, "image/png")

    prompt = CLASSIFY_PROMPT.format(
        text_above=entry.get("text_above", "N/A"),
        text_below=entry.get("text_below", "N/A"),
        nearest_heading=entry.get("nearest_heading", "N/A"),
        source_pdf=entry.get("source_pdf", "N/A"),
        page=entry.get("page", "N/A"),
    )

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": img_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
    )

    text = response.content[0].text.strip()
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    return {"classified": "skip", "title": "Parse error", "slug": "parse-error", "insight": text[:100]}


def ensure_unique_slugs(entries: list[dict]):
    """Ensure all slugs are unique by appending date suffix if needed."""
    slug_counts = {}
    for entry in entries:
        if entry.get("classified") in ("chart", "table"):
            slug = entry.get("slug", "")
            if slug:
                slug_counts[slug] = slug_counts.get(slug, 0) + 1

    slug_seen = {}
    for entry in entries:
        if entry.get("classified") in ("chart", "table"):
            slug = entry.get("slug", "")
            if slug and slug_counts.get(slug, 0) > 1:
                date_suffix = entry.get("pdf_date", "unknown").replace("-", "")
                if slug in slug_seen:
                    slug_seen[slug] += 1
                    entry["slug"] = f"{slug}-{date_suffix}-{slug_seen[slug]}"
                else:
                    slug_seen[slug] = 1
                    entry["slug"] = f"{slug}-{date_suffix}"


def run_classification(dry_run: bool = False):
    """Classify all unclassified images."""
    entries = load_manifest()

    unclassified = [e for e in entries if not e.get("classified")]
    print(f"Total images: {len(entries)}")
    print(f"Unclassified: {len(unclassified)}")
    print(f"Already classified: {len(entries) - len(unclassified)}")

    if not unclassified:
        print("All images already classified!")
        return entries

    if dry_run:
        print("\n[DRY RUN] Would classify these images:")
        for e in unclassified:
            print(f"  {e['staging_path']} — heading: {e.get('nearest_heading', 'N/A')[:60]}")
        return entries

    client = anthropic.Anthropic(api_key=API_KEY)

    classified_count = 0
    for i, entry in enumerate(entries):
        if entry.get("classified"):
            continue

        print(f"[{i+1}/{len(entries)}] Classifying: {entry['staging_path']}", end=" ... ", flush=True)

        try:
            result = classify_image(client, entry)
            entry["classified"] = result.get("classified", "skip")
            entry["title"] = result.get("title", "")
            entry["slug"] = result.get("slug", "")
            entry["insight"] = result.get("insight", "")
            print(f"{entry['classified']} — {entry['title'][:50]}")
            classified_count += 1
            time.sleep(0.5)

        except Exception as e:
            print(f"ERROR: {e}")
            entry["classified"] = "skip"
            entry["title"] = f"Error: {str(e)[:80]}"
            entry["slug"] = "error"

    ensure_unique_slugs(entries)
    save_manifest(entries)
    print(f"\nClassified {classified_count} images. Manifest updated.")
    return entries


def organize(entries: list[dict] = None):
    """Create Exhibit-A-style organized folders."""
    if entries is None:
        entries = load_manifest()

    keep = [e for e in entries if e.get("classified") in ("chart", "table")]

    if not keep:
        print("No chart/table entries found. Run classification first.")
        return

    if ORGANIZED_DIR.exists():
        shutil.rmtree(ORGANIZED_DIR)
    ORGANIZED_DIR.mkdir(parents=True)

    organized = []
    for entry in keep:
        slug = entry.get("slug", "").strip()
        if not slug or slug in ("error", "parse-error", "missing"):
            continue

        folder = ORGANIZED_DIR / slug
        folder.mkdir(parents=True, exist_ok=True)

        # Copy image
        src_img = STAGING_DIR / entry["staging_path"]
        ext = entry["format"]
        dst_img = folder / f"{slug}.{ext}"
        if src_img.exists():
            shutil.copy2(str(src_img), str(dst_img))

        # Write notes.txt
        title = entry.get("title", "Untitled")
        insight = entry.get("insight", "")
        text_above = entry.get("text_above", "").strip()
        text_below = entry.get("text_below", "").strip()

        notes = f"Title: {title}\n"
        notes += f"Source: {entry['source_pdf']} (page {entry['page']})\n"
        notes += f"Date: {entry['pdf_date']}\n"
        notes += f"Type: {entry['classified']}\n"

        if insight:
            notes += f"\nInsight: {insight}\n"
        if text_above:
            notes += f"\nContext (above):\n{text_above}\n"
        if text_below:
            notes += f"\nContext (below):\n{text_below}\n"

        (folder / "notes.txt").write_text(notes)

        organized.append({
            "slug": slug,
            "title": title,
            "source_pdf": entry["source_pdf"],
            "date": entry["pdf_date"],
            "page": entry["page"],
            "type": entry["classified"],
            "image_file": f"{slug}.{ext}",
            "insight": insight,
        })

    if organized:
        csv_path = ORGANIZED_DIR / "manifest.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=organized[0].keys())
            writer.writeheader()
            writer.writerows(organized)

    charts = sum(1 for o in organized if o["type"] == "chart")
    tables = sum(1 for o in organized if o["type"] == "table")
    print(f"\nOrganized {len(organized)} items into {ORGANIZED_DIR}/")
    print(f"  Charts: {charts}")
    print(f"  Tables: {tables}")


def show_stats():
    entries = load_manifest()
    total = len(entries)
    by_class = {}
    for e in entries:
        c = e.get("classified", "(unclassified)")
        by_class[c] = by_class.get(c, 0) + 1
    print(f"Total images: {total}")
    for cls, count in sorted(by_class.items()):
        print(f"  {cls:15s}: {count:3d} ({count/total*100:.0f}%)")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--stats" in args:
        show_stats()
    elif "--organize" in args:
        organize()
    elif "--dry-run" in args:
        run_classification(dry_run=True)
    else:
        entries = run_classification()
        print("\nNow organizing...")
        organize(entries)
