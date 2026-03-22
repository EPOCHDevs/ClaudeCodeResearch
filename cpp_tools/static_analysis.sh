#!/bin/bash
#
# Run C++ static analysis on EpochBackend source code.
#
# Tools:
#   cppcheck    - general bug finder (installed)
#   clang-tidy  - clang-based linter/checker (install: sudo apt install clang-tidy)
#
# Usage:
#   ./static_analysis.sh                          # Analyze all packages + services
#   ./static_analysis.sh services/stratifyx       # Analyze specific directory
#   ./static_analysis.sh packages/epoch-frame     # Analyze a single package
#   ./static_analysis.sh --tool cppcheck          # Only run cppcheck
#   ./static_analysis.sh --tool clang-tidy        # Only run clang-tidy
#   ./static_analysis.sh -j4                      # Limit parallel jobs
#   ./static_analysis.sh --severity warning        # cppcheck min severity (error|warning|style|performance|portability)
#
# Output is written to /tmp/static_analysis/ with timestamped filenames.
#

set -e

SCRIPT_NAME="static_analysis"
REPO_ROOT="$(cd "$(dirname "$0")/../../EpochBackend" && pwd)"
BUILD_DIR="$REPO_ROOT/build"
COMPILE_DB="$BUILD_DIR/compile_commands.json"
OUTPUT_DIR="/tmp/static_analysis"
NUM_JOBS=$(nproc)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Defaults
TOOL="all"
TARGET_DIR=""
CPPCHECK_SEVERITY="warning"

# Parse flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        --tool)
            TOOL="$2"
            shift 2
            ;;
        --severity)
            CPPCHECK_SEVERITY="$2"
            shift 2
            ;;
        -j|--jobs)
            NUM_JOBS="$2"
            shift 2
            ;;
        -j*)
            NUM_JOBS="${1#-j}"
            shift
            ;;
        -h|--help)
            head -18 "$0" | tail -16
            exit 0
            ;;
        *)
            TARGET_DIR="$1"
            shift
            ;;
    esac
done

# Resolve target directory
if [[ -n "$TARGET_DIR" ]]; then
    SCAN_PATH="$REPO_ROOT/$TARGET_DIR"
    if [[ ! -d "$SCAN_PATH" ]]; then
        echo "[$SCRIPT_NAME] ERROR: Directory not found: $SCAN_PATH"
        exit 1
    fi
    LABEL="$TARGET_DIR"
else
    SCAN_PATH="$REPO_ROOT"
    LABEL="all"
fi

mkdir -p "$OUTPUT_DIR"

echo "[$SCRIPT_NAME] Repository: $REPO_ROOT"
echo "[$SCRIPT_NAME] Scanning:   $SCAN_PATH"
echo "[$SCRIPT_NAME] Jobs:       $NUM_JOBS"
echo "[$SCRIPT_NAME] Output dir: $OUTPUT_DIR"
echo ""

# ── cppcheck ────────────────────────────────────────────────────────────────
run_cppcheck() {
    if ! command -v cppcheck &>/dev/null; then
        echo "[$SCRIPT_NAME] cppcheck not found. Install: sudo apt install cppcheck"
        return 1
    fi

    local outfile="$OUTPUT_DIR/cppcheck_${LABEL//\//_}_${TIMESTAMP}.txt"
    local xmlfile="$OUTPUT_DIR/cppcheck_${LABEL//\//_}_${TIMESTAMP}.xml"

    echo "[$SCRIPT_NAME] ── Running cppcheck ──"
    echo "[$SCRIPT_NAME] Min severity: $CPPCHECK_SEVERITY"

    cppcheck \
        --project="$COMPILE_DB" \
        --enable="$CPPCHECK_SEVERITY",performance,portability \
        --std=c++23 \
        --suppress=missingIncludeSystem \
        --suppress=unmatchedSuppression \
        --suppress=unusedFunction \
        --suppress=duplInheritedMember \
        --inline-suppr \
        -j "$NUM_JOBS" \
        --file-filter="$SCAN_PATH/*" \
        --suppress="*:*/test/*" \
        --suppress="*:*/tests/*" \
        --suppress="*:*.pb.h" \
        --suppress="*:*.pb.cc" \
        --suppress="*:*/build/*" \
        --suppress="*:*/build-*/*" \
        --output-file="$outfile" \
        --xml --xml-version=2 2>"$xmlfile" || true

    local error_count
    error_count=$(grep -c '<error ' "$xmlfile" 2>/dev/null || echo "0")

    echo "[$SCRIPT_NAME] cppcheck found $error_count issue(s)"
    echo "[$SCRIPT_NAME] Text report: $outfile"
    echo "[$SCRIPT_NAME] XML report:  $xmlfile"

    if [[ -s "$outfile" ]]; then
        echo ""
        echo "[$SCRIPT_NAME] ── cppcheck summary (first 50 lines) ──"
        head -50 "$outfile"
    fi
    echo ""
}

# ── clang-tidy ──────────────────────────────────────────────────────────────
run_clang_tidy() {
    # Try versioned binary first, then plain
    local CLANG_TIDY=""
    for candidate in clang-tidy-{20,19,18,17,16,15,14} clang-tidy; do
        if command -v "$candidate" &>/dev/null; then
            CLANG_TIDY="$candidate"
            break
        fi
    done

    if [[ -z "$CLANG_TIDY" ]]; then
        echo "[$SCRIPT_NAME] clang-tidy not found. Install: sudo apt install clang-tidy"
        return 1
    fi

    local outfile="$OUTPUT_DIR/clang_tidy_${LABEL//\//_}_${TIMESTAMP}.txt"

    echo "[$SCRIPT_NAME] ── Running clang-tidy ($CLANG_TIDY) ──"

    # Collect source files from compile_commands.json that match scan path
    local src_files
    src_files=$(python3 -c "
import json, sys
with open('$COMPILE_DB') as f:
    db = json.load(f)
for entry in db:
    f = entry.get('file', '')
    if f.startswith('$SCAN_PATH') and '/build/' not in f and '/build-' not in f and '.pb.cc' not in f and '/test/' not in f and '/tests/' not in f:
        print(f)
" 2>/dev/null | sort -u)

    local file_count
    file_count=$(echo "$src_files" | grep -c . 2>/dev/null || echo "0")

    if [[ "$file_count" -eq 0 ]]; then
        echo "[$SCRIPT_NAME] No source files found in compile_commands.json for: $SCAN_PATH"
        return 0
    fi

    echo "[$SCRIPT_NAME] Analyzing $file_count source file(s)..."

    # Run clang-tidy (raw output, then filter)
    local rawfile="${outfile%.txt}_raw.txt"
    echo "$src_files" | xargs -P "$NUM_JOBS" -I{} \
        "$CLANG_TIDY" -p "$BUILD_DIR" \
        --checks="-*,bugprone-*,performance-*,portability-*,cert-*,clang-analyzer-*,-bugprone-easily-swappable-parameters,-bugprone-lambda-function-name" \
        --quiet \
        --extra-arg=-ferror-limit=0 \
        --extra-arg=-Wno-everything \
        {} 2>&1 > "$rawfile"

    # Filter out compiler diagnostic errors (clang vs gcc C++23 differences) and vcpkg/build headers
    grep -v '\[clang-diagnostic-error\]' "$rawfile" \
        | grep -v 'vcpkg_installed/' \
        | grep -v '/build/' \
        | grep -v '\.pb\.' \
        | grep -v 'expanded from macro' \
        > "$outfile" || true

    local issue_count
    issue_count=$(grep -c ': warning:' "$outfile" 2>/dev/null || echo "0")

    echo ""
    echo "[$SCRIPT_NAME] clang-tidy found $issue_count warning(s)"
    echo "[$SCRIPT_NAME] Full report: $outfile"
    [[ -s "$outfile" ]] && echo "" && echo "[$SCRIPT_NAME] ── clang-tidy summary (first 50 lines) ──" && head -50 "$outfile"
    echo ""
}

# ── Run selected tool(s) ───────────────────────────────────────────────────
case "$TOOL" in
    cppcheck)
        run_cppcheck
        ;;
    clang-tidy|clang_tidy)
        run_clang_tidy
        ;;
    all)
        run_cppcheck
        run_clang_tidy
        ;;
    *)
        echo "[$SCRIPT_NAME] Unknown tool: $TOOL (use: cppcheck, clang-tidy, all)"
        exit 1
        ;;
esac

echo "[$SCRIPT_NAME] Done. All reports in: $OUTPUT_DIR"
