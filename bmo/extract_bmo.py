#!/usr/bin/env python3
"""
Extract images and text context from BMO FICC Macro Strategy PDFs.

Phase 1: Extracts all content into a staging directory.
Phase 2: Classifies and organizes into Exhibit-A-style folders.

Usage:
    python extract_bmo.py                      # Extract all PDFs to staging/
    python extract_bmo.py "BMO FX macro report 3-9-26.pdf"  # Extract single PDF
"""

import fitz  # PyMuPDF
import os
import sys
import json
import csv
import re
from pathlib import Path

BMO_DIR = Path(__file__).parent
STAGING_DIR = BMO_DIR / "staging"

# Minimum image dimensions to consider as content
MIN_WIDTH = 250
MIN_HEIGHT = 250

# BMO logos/banners to skip (exact dimensions)
LOGO_DIMS = {(1918, 312), (800, 281)}


def parse_pdf_date(filename: str) -> str:
    """Extract date from BMO filename like 'BMO FX macro report 3-9-26.pdf' -> '2026-03-09'."""
    # Pattern: M-D-YY
    match = re.search(r'(\d{1,2})-(\d{1,2})-(\d{2})', filename)
    if match:
        month, day, year_short = match.groups()
        return f"20{year_short}-{int(month):02d}-{int(day):02d}"

    # Pattern: DDMMMYY
    match = re.search(r'(\d{2})([A-Z]{3})(\d{2})', filename)
    if match:
        day, mon_str, year_short = match.groups()
        months = {
            'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
            'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
            'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
        }
        mon = months.get(mon_str, '00')
        return f"20{year_short}-{mon}-{day}"

    return "unknown"


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
                    "bbox": block["bbox"],
                    "y_center": (block["bbox"][1] + block["bbox"][3]) / 2
                })
    return text_blocks


def find_context_for_image(image_bbox, text_blocks, page_text: str) -> dict:
    """Find the text context surrounding an image based on position."""
    above = [b for b in text_blocks if b["y_center"] < image_bbox[1]]
    below = [b for b in text_blocks if b["y_center"] > image_bbox[3]]

    above.sort(key=lambda b: image_bbox[1] - b["y_center"])
    below.sort(key=lambda b: b["y_center"] - image_bbox[3])

    context = {
        "text_above": above[0]["text"] if above else "",
        "text_below": below[0]["text"] if below else "",
    }

    if above:
        context["nearest_heading"] = above[0]["text"].split("\n")[0]

    return context


def extract_pdf(pdf_path: Path, staging_base: Path) -> list[dict]:
    """Extract all content images and text from a single PDF."""
    doc = fitz.open(str(pdf_path))
    pdf_date = parse_pdf_date(pdf_path.name)
    slug = re.sub(r'[^a-z0-9]+', '_', pdf_path.stem.lower()).strip('_')

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
        mat = fitz.Matrix(2.0, 2.0)
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

            # Get image position on page
            img_rects = page.get_image_rects(xref)
            bbox = img_rects[0] if img_rects else fitz.Rect(0, 0, w, h)

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
                "classified": "",
                "title": "",
                "slug": "",
            }
            extracted.append(entry)
            img_idx += 1

    doc.close()
    return extracted


def run_extraction(pdf_filter: str = None):
    """Phase 1: Extract all PDFs into staging directory."""
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    all_entries = []
    pdf_files = sorted(BMO_DIR.glob("*.pdf"))

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

    csv_path = STAGING_DIR / "staging_manifest.csv"
    if all_entries:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_entries[0].keys())
            writer.writeheader()
            writer.writerows(all_entries)

    print(f"\nDone! {len(all_entries)} images extracted to {STAGING_DIR}/")
    print(f"Manifest: {manifest_path}")
    return all_entries


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_extraction(pdf_filter=sys.argv[1])
    else:
        run_extraction()
