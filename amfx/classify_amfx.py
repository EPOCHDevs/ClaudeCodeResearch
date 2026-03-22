#!/usr/bin/env python3
"""
Phase 2: Classify AMFX extracted images using Claude Vision API.

Reads staging_manifest.json, sends each image + text context to Claude,
gets back classification (chart/table/decorative/skip), title, and slug.
Updates the manifest, then organizes into Exhibit-A-style folders.

Usage:
    python classify_amfx.py                # Classify all unclassified images
    python classify_amfx.py --dry-run      # Preview without API calls
    python classify_amfx.py --organize     # Skip classification, just organize
    python classify_amfx.py --stats        # Show classification stats
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

AMFX_DIR = Path(__file__).parent
STAGING_DIR = AMFX_DIR / "staging"
ORGANIZED_DIR = AMFX_DIR / "amfx_organized"
MANIFEST_PATH = STAGING_DIR / "staging_manifest.json"

API_KEY = "REDACTED"

CLASSIFY_PROMPT = """You are classifying images extracted from financial newsletter PDFs (AMFX by Brent Donnelly / Spectra Markets).

Given an image and its surrounding text context, classify it and provide metadata.

## Classification Rules

**chart** — Financial chart: price charts, line charts, bar charts, candlestick charts, scatter plots, area charts, any data visualization showing market data, economic data, or analytical content.

**table** — Data table: performance tables, comparison tables, statistics tables, calendars with data, any structured tabular data with numbers.

**decorative** — Non-analytical images: magazine covers, memes, pop culture references, author photos, cartoons, logos, social media screenshots, book covers, screenshots of articles/tweets.

**skip** — Corrupted, too small to be useful, duplicate of another image, or completely irrelevant.

## Text Context
- Text above image: {text_above}
- Text below image: {text_below}
- Nearest heading: {nearest_heading}
- Source: {source_pdf} (page {page})

## Response Format
Respond with ONLY a JSON object (no markdown, no backticks):
{{"classified": "chart|table|decorative|skip", "title": "Descriptive title for the chart/table", "slug": "kebab-case-slug-name", "insight": "One sentence describing what this image shows or why it matters"}}

Rules for title/slug:
- For chart/table: Use the chart title if visible, otherwise derive from context
- For decorative/skip: Use a brief description, slug should still be descriptive
- Slug must be lowercase kebab-case, no special characters
- Include the date context in slug if it helps uniqueness (e.g., "sp500-weekly-2022-nov")
"""


def load_manifest() -> list[dict]:
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def save_manifest(entries: list[dict]):
    with open(MANIFEST_PATH, "w") as f:
        json.dump(entries, f, indent=2)

    # Also update CSV
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

    # Read and encode image
    img_data = img_path.read_bytes()
    img_b64 = base64.standard_b64encode(img_data).decode("utf-8")

    # Determine media type
    ext = entry["format"].lower()
    media_type_map = {"png": "image/png", "jpeg": "image/jpeg", "jpg": "image/jpeg"}
    media_type = media_type_map.get(ext, "image/png")

    # Build prompt with context
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

    # Parse response
    text = response.content[0].text.strip()

    # Try to extract JSON from response (handle markdown wrapping)
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            result = json.loads(json_match.group())
            return result
        except json.JSONDecodeError:
            pass

    # Fallback
    return {"classified": "skip", "title": "Parse error", "slug": "parse-error", "insight": text[:100]}


def ensure_unique_slugs(entries: list[dict]):
    """Ensure all slugs are unique by appending date suffix if needed."""
    slug_counts = {}
    for entry in entries:
        if entry.get("classified") in ("chart", "table"):
            slug = entry.get("slug", "")
            if slug:
                slug_counts[slug] = slug_counts.get(slug, 0) + 1

    # For duplicates, append date
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
    """Classify all unclassified images in the staging manifest."""
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
        for e in unclassified[:5]:
            print(f"  {e['staging_path']} — heading: {e.get('nearest_heading', 'N/A')[:60]}")
        if len(unclassified) > 5:
            print(f"  ... and {len(unclassified) - 5} more")
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

            # Save progress every 10 images
            if classified_count % 10 == 0:
                save_manifest(entries)
                print(f"  [saved progress: {classified_count} classified]")

            # Rate limiting: ~50 req/min for Haiku
            time.sleep(0.5)

        except Exception as e:
            print(f"ERROR: {e}")
            entry["classified"] = "skip"
            entry["title"] = f"Error: {str(e)[:80]}"
            entry["slug"] = "error"

    # Ensure unique slugs
    ensure_unique_slugs(entries)

    # Final save
    save_manifest(entries)
    print(f"\nClassified {classified_count} images. Manifest updated.")

    return entries


def organize(entries: list[dict] = None):
    """Create Exhibit-A-style organized folders from classified manifest."""
    if entries is None:
        entries = load_manifest()

    # Filter to chart and table only
    keep = [e for e in entries if e.get("classified") in ("chart", "table")]

    if not keep:
        print("No chart/table entries found. Run classification first.")
        return

    # Clean and recreate organized dir
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

        # Write notes.txt (Exhibit-A style)
        notes_path = folder / "notes.txt"
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

        notes_path.write_text(notes)

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

    # Write manifest CSV
    if organized:
        csv_path = ORGANIZED_DIR / "manifest.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=organized[0].keys())
            writer.writeheader()
            writer.writerows(organized)

    print(f"\nOrganized {len(organized)} charts/tables into {ORGANIZED_DIR}/")
    print(f"Manifest: {ORGANIZED_DIR / 'manifest.csv'}")

    # Print summary
    charts = sum(1 for o in organized if o["type"] == "chart")
    tables = sum(1 for o in organized if o["type"] == "table")
    print(f"  Charts: {charts}")
    print(f"  Tables: {tables}")


def show_stats():
    """Show classification statistics."""
    entries = load_manifest()
    total = len(entries)
    by_class = {}
    for e in entries:
        c = e.get("classified", "(unclassified)")
        by_class[c] = by_class.get(c, 0) + 1

    print(f"Total images: {total}")
    for cls, count in sorted(by_class.items()):
        pct = count / total * 100
        print(f"  {cls:15s}: {count:3d} ({pct:.0f}%)")


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
