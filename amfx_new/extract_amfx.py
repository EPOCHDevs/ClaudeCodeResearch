#!/usr/bin/env python3
"""
Extract images from amFX Friday Speedrun PDFs into per-PDF folders.

Extracts all content images (charts, tables, plots) while filtering out
logos, tiny icons, and known branding elements. Also renders full pages
as PNG for visual reference.

Usage:
    python extract_amfx.py                    # Extract all PDFs
    python extract_amfx.py "AMFX 12DEC25"     # Extract single PDF (partial match)
"""

import fitz  # PyMuPDF
import os
import sys
import json
import csv
import re
from pathlib import Path

SOURCE_DIR = Path("/home/adesola/Downloads/amFX _ Friday Speedrun (1)/amFX : Friday Speedrun")
OUTPUT_DIR = Path(__file__).parent

# Minimum image dimensions to consider as content (skip tiny icons/logos)
MIN_WIDTH = 150
MIN_HEIGHT = 150

# Known logo/banner dimensions to skip (Spectra Markets header, amFX logo, etc.)
LOGO_DIMS = set()

# Skip images that are very wide but short (banners/headers)
BANNER_ASPECT_MIN = 4.0  # width/height > 4 = likely a banner


def parse_pdf_date(filename: str) -> str:
    """Extract date from AMFX filename like 'AMFX 12DEC25.pdf' -> '2025-12-12'."""
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


def make_folder_name(filename: str) -> str:
    """Convert 'AMFX 12DEC25.pdf' -> 'AMFX_12DEC25'."""
    return filename.replace('.pdf', '').replace(' ', '_')


def is_logo_or_icon(width: int, height: int) -> bool:
    """Check if image dimensions match known logos/icons."""
    if (width, height) in LOGO_DIMS:
        return True
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        return True
    # Banner detection: very wide and short
    if height > 0 and width / height > BANNER_ASPECT_MIN:
        return True
    return False


def extract_text_blocks(page) -> list:
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


def find_context_for_image(image_bbox, text_blocks) -> dict:
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


def extract_pdf(pdf_path: Path, output_base: Path) -> list:
    """Extract all content images and page renders from a single PDF."""
    doc = fitz.open(str(pdf_path))
    pdf_date = parse_pdf_date(pdf_path.name)
    folder_name = make_folder_name(pdf_path.name)

    pdf_output = output_base / folder_name
    pdf_output.mkdir(parents=True, exist_ok=True)

    extracted = []
    seen_xrefs = set()

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text_blocks = extract_text_blocks(page)
        page_text = page.get_text().strip()

        # Save full page text
        text_path = pdf_output / f"page_{page_num + 1:02d}_text.txt"
        text_path.write_text(page_text)

        # Render full page as PNG (2x zoom for readability)
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat)
        page_img_path = pdf_output / f"page_{page_num + 1:02d}.png"
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

            context = find_context_for_image(bbox, text_blocks)

            # Save image
            img_filename = f"page_{page_num + 1:02d}_img_{img_idx:02d}.{ext}"
            img_path = pdf_output / img_filename
            img_path.write_bytes(img_data)

            entry = {
                "source_pdf": pdf_path.name,
                "pdf_date": pdf_date,
                "folder": folder_name,
                "page": page_num + 1,
                "image_file": img_filename,
                "width": w,
                "height": h,
                "format": ext,
                "text_above": context.get("text_above", ""),
                "text_below": context.get("text_below", ""),
                "nearest_heading": context.get("nearest_heading", ""),
                "image_path": str(img_path.relative_to(output_base)),
                "page_image": str(page_img_path.relative_to(output_base)),
            }
            extracted.append(entry)
            img_idx += 1

    doc.close()
    return extracted


def run_extraction(pdf_filter: str = None):
    """Extract all PDFs (or filtered subset) into output folders."""
    all_entries = []
    pdf_files = sorted(SOURCE_DIR.glob("*.pdf"))

    if pdf_filter:
        pdf_files = [p for p in pdf_files if pdf_filter in p.name]

    if not pdf_files:
        print(f"No PDFs found matching filter '{pdf_filter}' in {SOURCE_DIR}")
        return []

    for pdf_path in pdf_files:
        print(f"Extracting: {pdf_path.name}")
        entries = extract_pdf(pdf_path, OUTPUT_DIR)
        all_entries.extend(entries)
        print(f"  -> {len(entries)} content images extracted")

    # Write master manifest
    manifest_json = OUTPUT_DIR / "extraction_manifest.json"
    with open(manifest_json, "w") as f:
        json.dump(all_entries, f, indent=2)

    manifest_csv = OUTPUT_DIR / "extraction_manifest.csv"
    if all_entries:
        with open(manifest_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_entries[0].keys())
            writer.writeheader()
            writer.writerows(all_entries)

    print(f"\nDone! {len(all_entries)} content images extracted across {len(pdf_files)} PDFs")
    print(f"Manifest: {manifest_json}")
    return all_entries


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_extraction(pdf_filter=sys.argv[1])
    else:
        run_extraction()
