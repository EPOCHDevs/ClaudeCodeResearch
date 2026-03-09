#!/usr/bin/env python3
"""
Validate all EpochScript sources using epoch_compile_check binary.
Checks both JSON definitions (ClaudeCodeResearch) and .epochscript files (ScriptTemplates).
"""

import json
import subprocess
import sys
from pathlib import Path

COMPILE_CHECK = "/home/adesola/EpochDev/EpochBackend/build/bin/epoch_compile_check"
TIMEOUT = 30

CLAUDE_RESEARCH_DEFS = Path("/home/adesola/EpochDev/ClaudeCodeResearch/project/definitions/test_runner")
SCRIPT_TEMPLATES = Path("/home/adesola/EpochDev/ScriptTemplates")


def validate_source(source: str) -> tuple:
    """Returns (is_valid, message)"""
    try:
        result = subprocess.run(
            [COMPILE_CHECK, source],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )

        # Extract JSON from stdout (may have AWS errors before it)
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    response = json.loads(line)
                    return response.get("status") == "ok", response.get("message", "")
                except json.JSONDecodeError:
                    continue

        # Check stderr for JSON
        for line in result.stderr.split('\n'):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    response = json.loads(line)
                    return response.get("status") == "ok", response.get("message", "")
                except json.JSONDecodeError:
                    continue

        return False, f"No JSON response. stdout={result.stdout[:200]}, stderr={result.stderr[:200]}"

    except subprocess.TimeoutExpired:
        return False, "Timeout (30s)"
    except Exception as e:
        return False, str(e)


def main():
    passed = []
    failed = []

    # ClaudeResearch JSON definitions
    print("=== Validating ClaudeCodeResearch definitions ===")
    for f in sorted(CLAUDE_RESEARCH_DEFS.glob("*.json")):
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            failed.append((f.name, f"Invalid JSON: {e}"))
            print(f"  FAIL {f.name}: Invalid JSON")
            continue

        source = data.get("source", data.get("script", ""))
        if not source:
            continue

        ok, msg = validate_source(source)
        if ok:
            passed.append(f.name)
            print(f"  OK   {f.name}")
        else:
            failed.append((f.name, msg))
            print(f"  FAIL {f.name}: {msg[:120]}")

    # ScriptTemplates .epochscript files
    print("\n=== Validating ScriptTemplates ===")
    for f in sorted(SCRIPT_TEMPLATES.rglob("*.epochscript")):
        source = f.read_text()
        if not source.strip():
            continue

        ok, msg = validate_source(source)
        rel = f.relative_to(SCRIPT_TEMPLATES)
        if ok:
            passed.append(str(rel))
            print(f"  OK   {rel}")
        else:
            failed.append((str(rel), msg))
            print(f"  FAIL {rel}: {msg[:120]}")

    print(f"\n=== Summary ===")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    if failed:
        print("\nFailed files:")
        for name, msg in failed:
            print(f"  {name}: {msg[:200]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
