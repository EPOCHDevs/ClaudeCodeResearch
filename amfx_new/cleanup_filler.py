#!/usr/bin/env python3
"""
Remove non-quantitative (DISCARD) images from amFX folders.
Keeps only images referenced by KEEP items in analysis.md.
Also keeps page_XX.png renders and page_XX_text.txt files.
"""

import re
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

def extract_keep_images(analysis_path: Path) -> set:
    """Parse analysis.md and return set of image filenames that are KEEP."""
    text = analysis_path.read_text()
    keep_images = set()
    
    # Pattern 1: From inventory tables - find KEEP rows with image files
    # Match rows like: | 6 | 2 | USDCAD chart | **KEEP** | page_02_img_00.jpeg | reason |
    for match in re.finditer(r'\*\*KEEP\*\*\s*\|\s*(page_\d+_img_\d+\.\w+)', text):
        keep_images.add(match.group(1))
    
    # Pattern 2: From detailed analysis - image_file: lines
    # Match lines like: - **image_file:** page_02_img_00.jpeg
    for match in re.finditer(r'\*\*image_file:\*\*\s*(page_\d+_img_\d+\.\w+)', text):
        keep_images.add(match.group(1))
    
    # Pattern 3: Some have composite references like "page_01_img_02.png (top half)"
    for match in re.finditer(r'(page_\d+_img_\d+\.\w+)\s*\((?:top|bottom)\s+half\)', text):
        keep_images.add(match.group(1))
    
    # Pattern 4: Comma-separated lists like "page_05_img_01.png, page_05_img_02.png"
    for match in re.finditer(r'\*\*image_file:\*\*\s*(.+)', text):
        line = match.group(1)
        for img_match in re.finditer(r'(page_\d+_img_\d+\.\w+)', line):
            keep_images.add(img_match.group(1))
    
    return keep_images


def cleanup_folder(folder: Path) -> dict:
    """Remove DISCARD images from a single folder."""
    analysis = folder / "analysis.md"
    if not analysis.exists():
        return {"folder": folder.name, "error": "no analysis.md"}
    
    keep_images = extract_keep_images(analysis)
    
    # Find all extracted image files (page_XX_img_YY.ext)
    all_img_files = sorted(folder.glob("page_*_img_*.*"))
    
    removed = []
    kept = []
    
    for img in all_img_files:
        if img.name in keep_images:
            kept.append(img.name)
        else:
            removed.append(img.name)
            img.unlink()
    
    return {
        "folder": folder.name,
        "keep_count": len(kept),
        "removed_count": len(removed),
        "kept": kept,
        "removed": removed,
    }


def main():
    folders = sorted(OUTPUT_DIR.glob("AMFX_*"))
    
    total_removed = 0
    total_kept = 0
    
    for folder in folders:
        if not folder.is_dir():
            continue
        result = cleanup_folder(folder)
        
        if "error" in result:
            print(f"  SKIP {result['folder']}: {result['error']}")
            continue
        
        total_removed += result["removed_count"]
        total_kept += result["keep_count"]
        
        print(f"{result['folder']}:")
        print(f"  KEPT ({result['keep_count']}): {', '.join(result['kept']) if result['kept'] else '(none)'}")
        if result["removed"]:
            print(f"  REMOVED ({result['removed_count']}): {', '.join(result['removed'])}")
        else:
            print(f"  REMOVED: (none)")
        print()
    
    print(f"{'='*60}")
    print(f"TOTAL: Kept {total_kept} images, removed {total_removed} filler images")


if __name__ == "__main__":
    main()
