#!/usr/bin/env python3
"""
Extract images and text context from AMFX PDF newsletters.

Phase 1: Extracts all content into a staging directory.
Phase 2: Classifies and organizes into Exhibit-A-style folders.

Usage:
    python extract_amfx.py                    # Extract all PDFs to staging/
    python extract_amfx.py --organize         # Organize staging/ into amfx_organized/
    python extract_amfx.py "AMFX 12DEC25.pdf" # Extract single PDF
"""

import fitz  # PyMuPDF
import os
import sys
import json
import csv
import re
from pathlib import Path
from datetime import datetime

AMFX_DIR = Path(__file__).parent
STAGING_DIR = AMFX_DIR / "staging"
ORGANIZED_DIR = AMFX_DIR / "amfx_organized"

# Minimum image dimensions to consider as content (skip logos, icons)
MIN_WIDTH = 250
MIN_HEIGHT = 200

# Spectra logo dimensions (382x110) - skip exact matches
LOGO_DIMS = {(382, 110), (412, 66)}  # header logo + footer logo


def parse_pdf_date(filename: str) -> str:
    """Extract date from AMFX filename like 'AMFX 12DEC25.pdf' -> '2025-12-12'."""
    match = re.search(r'(\d{2})([A-Z]{3})(\d{2})', filename)
    if not match:
        return "unknown"
    day, mon_str, year_short = match.groups()
    months = {
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
        'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
        'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
    }
    mon = months.get(mon_str, '00')
    year = f"20{year_short}"
    return f"{year}-{mon}-{day}"


def is_logo_or_icon(width: int, height: int) -> bool:
    """Check if image dimensions match known logos/icons."""
    if (width, height) in LOGO_DIMS:
        return True
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        return True
    return False


def extract_text_blocks(page) -> list[dict]:
    """Extract text blocks with position info from a page."""
    blocks = page.get_text("dict")["blocks"]
    text_blocks = []
    for block in blocks:
        if block["type"] == 0:  # text block
            text = ""
            for line in block["lines"]:
                for span in line["spans"]:
                    text += span["text"]
                text += "\n"
            text = text.strip()
            if text:
                text_blocks.append({
                    "text": text,
                    "bbox": block["bbox"],  # (x0, y0, x1, y1)
                    "y_center": (block["bbox"][1] + block["bbox"][3]) / 2
                })
    return text_blocks


def find_context_for_image(image_bbox, text_blocks, page_text: str) -> dict:
    """Find the text context surrounding an image based on position."""
    img_y_center = (image_bbox[1] + image_bbox[3]) / 2

    # Find text blocks above and below the image
    above = [b for b in text_blocks if b["y_center"] < image_bbox[1]]
    below = [b for b in text_blocks if b["y_center"] > image_bbox[3]]

    # Sort by proximity
    above.sort(key=lambda b: image_bbox[1] - b["y_center"])
    below.sort(key=lambda b: b["y_center"] - image_bbox[3])

    context = {
        "text_above": above[0]["text"] if above else "",
        "text_below": below[0]["text"] if below else "",
    }

    # Try to identify a title (bold/large text above)
    if above:
        context["nearest_heading"] = above[0]["text"].split("\n")[0]

    return context


def extract_pdf(pdf_path: Path, staging_base: Path) -> list[dict]:
    """Extract all content images and text from a single PDF."""
    doc = fitz.open(str(pdf_path))
    pdf_date = parse_pdf_date(pdf_path.name)
    slug = pdf_path.stem.lower().replace(" ", "_").replace("(", "").replace(")", "").strip("_")

    pdf_staging = staging_base / slug
    pdf_staging.mkdir(parents=True, exist_ok=True)

    extracted = []
    seen_xrefs = set()

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text_blocks = extract_text_blocks(page)
        page_text = page.get_text().strip()

        # Save full page text
        text_path = pdf_staging / f"page_{page_num + 1:02d}_text.txt"
        text_path.write_text(page_text)

        # Render full page as image for visual reference
        mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for quality
        pix = page.get_pixmap(matrix=mat)
        page_img_path = pdf_staging / f"page_{page_num + 1:02d}.png"
        pix.save(str(page_img_path))

        # Extract individual embedded images
        images = page.get_images(full=True)
        img_idx = 0
        for img_info in images:
            xref = img_info[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)

            base_image = doc.extract_image(xref)
            w, h = base_image["width"], base_image["height"]

            if is_logo_or_icon(w, h):
                continue

            ext = base_image["ext"]
            img_data = base_image["image"]

            # Get image position on page for context matching
            img_rects = page.get_image_rects(xref)
            bbox = img_rects[0] if img_rects else fitz.Rect(0, 0, w, h)

            # Find surrounding text context
            context = find_context_for_image(bbox, text_blocks, page_text)

            # Save image
            img_filename = f"page_{page_num + 1:02d}_img_{img_idx:02d}.{ext}"
            img_path = pdf_staging / img_filename
            img_path.write_bytes(img_data)

            entry = {
                "source_pdf": pdf_path.name,
                "pdf_date": pdf_date,
                "page": page_num + 1,
                "image_file": img_filename,
                "width": w,
                "height": h,
                "format": ext,
                "text_above": context.get("text_above", ""),
                "text_below": context.get("text_below", ""),
                "nearest_heading": context.get("nearest_heading", ""),
                "staging_path": str(img_path.relative_to(staging_base)),
                "page_image": str(page_img_path.relative_to(staging_base)),
                "classified": "",  # To be filled in Phase 2: chart|table|decorative|skip
                "title": "",       # To be filled in Phase 2
                "slug": "",        # To be filled in Phase 2
            }
            extracted.append(entry)
            img_idx += 1

    doc.close()
    return extracted


def run_extraction(pdf_filter: str = None):
    """Phase 1: Extract all PDFs into staging directory."""
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    all_entries = []
    pdf_files = sorted(AMFX_DIR.glob("*.pdf"))

    if pdf_filter:
        pdf_files = [p for p in pdf_files if pdf_filter in p.name]

    for pdf_path in pdf_files:
        print(f"Extracting: {pdf_path.name}")
        entries = extract_pdf(pdf_path, STAGING_DIR)
        all_entries.extend(entries)
        print(f"  -> {len(entries)} content images extracted")

    # Write staging manifest
    manifest_path = STAGING_DIR / "staging_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(all_entries, f, indent=2)

    # Also write CSV for easy review
    csv_path = STAGING_DIR / "staging_manifest.csv"
    if all_entries:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_entries[0].keys())
            writer.writeheader()
            writer.writerows(all_entries)

    print(f"\nDone! {len(all_entries)} images extracted to {STAGING_DIR}/")
    print(f"Manifest: {manifest_path}")
    print(f"CSV:      {csv_path}")
    print(f"\nNext step: Review staging_manifest.csv and classify each image,")
    print(f"then run: python extract_amfx.py --organize")

    return all_entries


def organize_staging():
    """Phase 2: Read classified staging manifest and create organized folders."""
    manifest_path = STAGING_DIR / "staging_manifest.json"
    if not manifest_path.exists():
        print("No staging manifest found. Run extraction first.")
        return

    with open(manifest_path) as f:
        entries = json.load(f)

    ORGANIZED_DIR.mkdir(parents=True, exist_ok=True)
    organized = []

    for entry in entries:
        if entry.get("classified") not in ("chart", "table"):
            continue
        if not entry.get("slug"):
            continue

        slug = entry["slug"]
        folder = ORGANIZED_DIR / slug
        folder.mkdir(parents=True, exist_ok=True)

        # Copy image
        src_img = STAGING_DIR / entry["staging_path"]
        ext = entry["format"]
        dst_img = folder / f"{slug}.{ext}"
        if src_img.exists():
            dst_img.write_bytes(src_img.read_bytes())

        # Write notes.txt
        notes_path = folder / "notes.txt"
        title = entry.get("title", entry.get("nearest_heading", "Untitled"))
        notes_content = f"""Title: {title}
Source: {entry['source_pdf']} (page {entry['page']})
Date: {entry['pdf_date']}
Type: {entry['classified']}

Context Above:
{entry.get('text_above', '')}

Context Below:
{entry.get('text_below', '')}
"""
        notes_path.write_text(notes_content.strip() + "\n")

        organized.append({
            "slug": slug,
            "title": title,
            "source_pdf": entry["source_pdf"],
            "date": entry["pdf_date"],
            "page": entry["page"],
            "type": entry["classified"],
            "image_file": f"{slug}.{ext}",
        })

    # Write organized manifest
    if organized:
        csv_path = ORGANIZED_DIR / "manifest.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=organized[0].keys())
            writer.writeheader()
            writer.writerows(organized)
        print(f"Organized {len(organized)} items into {ORGANIZED_DIR}/")
        print(f"Manifest: {csv_path}")
    else:
        print("No classified entries found. Edit staging_manifest.json first:")
        print('  Set "classified" to "chart" or "table"')
        print('  Set "slug" to a kebab-case name')
        print('  Set "title" to the chart/table title')


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--organize":
        organize_staging()
    elif len(sys.argv) > 1:
        run_extraction(pdf_filter=sys.argv[1])
    else:
        run_extraction()
