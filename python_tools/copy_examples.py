#!/usr/bin/env python3
"""
Convert test_runner JSON definitions to flattened .txt examples.

Always overwrites existing files and removes stale .txt files
that no longer have a matching source definition.

Usage:
    python3 copy_examples.py [--dry-run] [--validate] [--validate-only]

Options:
    --dry-run       Preview what would be converted without writing files
    --validate      Validate EpochScript source before converting
    --validate-only Only validate definitions, don't convert to .txt
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# UUID pattern (8-4-4-4-12 hex)
UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.IGNORECASE)

# Executor keywords that indicate a strategy (not research)
STRATEGY_INDICATORS = [
    "position_size(", "long_and_short_zone(", "long_zone(", "short_zone(",
    "rollover_policy(",
]

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent / "project"
SOURCE_DIR = PROJECT_DIR / "definitions" / "test_runner"
DEST_DIR = Path("/home/adesola/EpochDev/EpochBackend/examples")

# epoch_compile_check binary - check multiple possible locations
COMPILE_CHECK_PATHS = [
    Path("/home/adesola/EpochDev/EpochBackend/build/bin/epoch_compile_check"),
    SCRIPT_DIR / "bin" / "epoch_compile_check",
]


def is_uuid_filename(name: str) -> bool:
    """Check if filename (without extension) looks like a UUID."""
    return bool(UUID_RE.match(name))


def detect_suffix(source_code: str) -> str:
    """Detect whether a definition is a strategy or research based on source."""
    for indicator in STRATEGY_INDICATORS:
        if indicator in source_code:
            return "_strategy"
    return "_research"


def ensure_suffix(stem: str, source_code: str) -> str:
    """Return stem with _research or _strategy suffix, adding if missing."""
    if stem.endswith("_strategy") or stem.endswith("_research"):
        return stem
    return stem + detect_suffix(source_code)


def find_compile_check() -> Path | None:
    """Find the epoch_compile_check binary."""
    for path in COMPILE_CHECK_PATHS:
        if path.exists():
            return path
    return None


def validate_source(source: str, compile_check: Path) -> tuple[bool, str]:
    """
    Validate EpochScript source code using epoch_compile_check.

    Returns (is_valid, message).
    """
    try:
        result = subprocess.run(
            [str(compile_check), source],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Parse JSON response - look for JSON in the output
        # (AWS credential errors may appear before the JSON)
        output = result.stdout.strip()

        # Find the JSON object in the output (last line with JSON)
        json_line = None
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                json_line = line

        if not json_line:
            # Check stderr too
            for line in result.stderr.strip().split('\n'):
                line = line.strip()
                if line.startswith('{') and line.endswith('}'):
                    json_line = line

        if not json_line:
            return False, f"No JSON response found in output"

        try:
            response = json.loads(json_line)
            status = response.get("status", "error")
            message = response.get("message", "Unknown error")
            return status == "ok", message
        except json.JSONDecodeError:
            return False, f"Invalid JSON response: {json_line}"

    except subprocess.TimeoutExpired:
        return False, "Compilation check timed out"
    except Exception as e:
        return False, f"Error running compile check: {e}"


def json_to_txt(json_data: dict) -> str:
    """Convert JSON definition to flattened .txt format."""
    name = json_data.get("name", "Untitled")
    description = json_data.get("description", "")

    # Handle assets - can be list or string
    data = json_data.get("data", {})
    assets = data.get("assets", [])
    if isinstance(assets, list):
        assets_str = ", ".join(assets)
    else:
        assets_str = str(assets)

    source_name = data.get("source", "polygon")
    timeframe = json_data.get("global_timeframe", "1D")
    source_code = json_data.get("source", "")

    # Build the flattened format
    lines = [
        f"Name: {name}",
        "",
        f"Description: {description}",
        "",
        f"Assets: {assets_str}",
        f"Data Source: {source_name}",
        f"Timeframe: {timeframe}",
        "",
        "=" * 80,
        "",
        source_code
    ]

    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    validate = "--validate" in sys.argv or "--validate-only" in sys.argv
    validate_only = "--validate-only" in sys.argv

    if not SOURCE_DIR.exists():
        print(f"ERROR: Source directory not found: {SOURCE_DIR}")
        return 1

    # Find compile check binary if validation requested
    compile_check = None
    if validate:
        compile_check = find_compile_check()
        if not compile_check:
            print("ERROR: epoch_compile_check not found. Build it first:")
            print("  ninja epoch_compile_check")
            print(f"\nSearched paths:")
            for p in COMPILE_CHECK_PATHS:
                print(f"  - {p}")
            return 1
        print(f"Using compile checker: {compile_check}")

    if not validate_only:
        if not DEST_DIR.exists():
            print(f"Creating destination directory: {DEST_DIR}")
            if not dry_run:
                DEST_DIR.mkdir(parents=True, exist_ok=True)

    # Get all JSON files
    json_files = sorted(SOURCE_DIR.glob("*.json"))

    if not json_files:
        print("No JSON files found in source directory")
        return 1

    print(f"Found {len(json_files)} definition files")
    print(f"Source: {SOURCE_DIR}")
    if not validate_only:
        print(f"Destination: {DEST_DIR}")
    print()

    if dry_run:
        print("DRY RUN - no files will be written\n")

    converted = 0
    errors = 0
    skipped = 0
    validation_passed = 0
    validation_failed = 0

    # Track which .txt files we write so we can remove stale ones
    written_txt = set()

    for src_file in json_files:
        # Skip UUID-named files
        if is_uuid_filename(src_file.stem):
            print(f"  SKIPPED (UUID): {src_file.name}")
            skipped += 1
            continue

        try:
            # Read and parse JSON
            with open(src_file, "r") as f:
                json_data = json.load(f)

            source_code = json_data.get("source", "")

            # Validate if requested
            if validate and source_code:
                is_valid, message = validate_source(source_code, compile_check)
                if is_valid:
                    print(f"  VALID: {src_file.name}")
                    validation_passed += 1
                else:
                    print(f"  INVALID: {src_file.name}")
                    print(f"    Error: {message}")
                    validation_failed += 1
                    errors += 1
                    continue  # Skip conversion for invalid definitions

            # Skip conversion if validate-only
            if validate_only:
                continue

            # Ensure output name has _research or _strategy suffix
            out_stem = ensure_suffix(src_file.stem, source_code)
            dest_file = DEST_DIR / f"{out_stem}.txt"

            # Convert to txt format
            txt_content = json_to_txt(json_data)

            if dry_run:
                print(f"  WOULD CONVERT: {src_file.name} -> {dest_file.name}")
            else:
                with open(dest_file, "w") as f:
                    f.write(txt_content)
                print(f"  CONVERTED: {src_file.name} -> {dest_file.name}")

            written_txt.add(dest_file.name)

            converted += 1

        except json.JSONDecodeError as e:
            print(f"  ERROR (invalid JSON): {src_file.name}: {e}")
            errors += 1
        except Exception as e:
            print(f"  ERROR: {src_file.name}: {e}")
            errors += 1

    # Remove stale .txt files that no longer have a matching source
    removed = 0
    if not validate_only and DEST_DIR.exists():
        for txt_file in sorted(DEST_DIR.glob("*.txt")):
            if txt_file.name not in written_txt:
                if dry_run:
                    print(f"  WOULD REMOVE (stale): {txt_file.name}")
                else:
                    txt_file.unlink()
                    print(f"  REMOVED (stale): {txt_file.name}")
                removed += 1

    print()

    # Summary
    if validate:
        print(f"Validation: {validation_passed} passed, {validation_failed} failed")

    if not validate_only:
        print(f"Conversion: {converted} converted, {skipped} skipped, {removed} stale removed, {errors} errors")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
