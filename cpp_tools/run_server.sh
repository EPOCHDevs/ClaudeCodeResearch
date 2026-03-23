#!/bin/bash
#
# Build (if stale) and run epoch_stratifyx_server
#
# Usage:
#   ./run_server.sh              # Release build, default port
#   ./run_server.sh --no-build   # Skip build, run existing binary
#   ./run_server.sh --asan       # Debug build with AddressSanitizer
#   ./run_server.sh -j4          # Limit to 4 parallel build jobs
#   ./run_server.sh --asan -j4   # ASAN build with 4 jobs
#
# The server runs on port 8080 by default.
# Press Ctrl+C to stop.
#

set -e

SCRIPT_NAME="run_server"
TARGET="epoch_stratifyx_server"
DEFAULT_PORT=9000
NUM_JOBS=$(( $(nproc) > 8 ? 8 : $(nproc) ))

# Default to release build
BUILD_MODE="release"
BUILD_DIR="../../EpochBackend/build"
SKIP_BUILD=false

# Parse flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-build)
            SKIP_BUILD=true
            shift
            ;;
        --asan)
            BUILD_MODE="asan"
            BUILD_DIR="../../EpochBackend/build-asan"
            shift
            ;;
        -j|--jobs)
            if [[ -n "$2" && "$2" =~ ^[0-9]+$ ]]; then
                NUM_JOBS="$2"
                shift 2
            else
                echo "[$SCRIPT_NAME] Error: -j requires a numeric argument"
                exit 1
            fi
            ;;
        -j*)
            # Handle -jN format (no space)
            NUM_JOBS="${1#-j}"
            if [[ ! "$NUM_JOBS" =~ ^[0-9]+$ ]]; then
                echo "[$SCRIPT_NAME] Error: Invalid job count: $NUM_JOBS"
                exit 1
            fi
            shift
            ;;
        *)
            echo "[$SCRIPT_NAME] Unknown option: $1"
            exit 1
            ;;
    esac
done

BIN_PATH="$BUILD_DIR/bin/$TARGET"

echo "[$SCRIPT_NAME] Mode: $BUILD_MODE"
echo "[$SCRIPT_NAME] Build dir: $BUILD_DIR"
echo "[$SCRIPT_NAME] Jobs: $NUM_JOBS"

# Verify build directory exists
if [[ ! -d "$BUILD_DIR" ]]; then
    echo "[$SCRIPT_NAME] ERROR: Build directory does not exist: $BUILD_DIR"
    exit 1
fi

# Build if stale (ninja handles staleness check automatically)
if [[ "$SKIP_BUILD" == true ]]; then
    echo "[$SCRIPT_NAME] Skipping build (--no-build)"
else
    echo "[$SCRIPT_NAME] Building $TARGET (if stale)..."
    ninja -C "$BUILD_DIR" -j"$NUM_JOBS" "$TARGET"
fi

# Verify binary exists
if [[ ! -x "$BIN_PATH" ]]; then
    echo "[$SCRIPT_NAME] ERROR: Binary not found: $BIN_PATH"
    exit 1
fi

echo ""
echo "[$SCRIPT_NAME] Starting server on port $DEFAULT_PORT..."
echo "[$SCRIPT_NAME] Binary: $BIN_PATH"
echo "[$SCRIPT_NAME] Workdir: $BUILD_DIR/bin (contains .env.local)"
echo "[$SCRIPT_NAME] Press Ctrl+C to stop"
echo ""

# Run from bin directory where .env.local is located
cd "$BUILD_DIR/bin"
exec "./$TARGET" --port "$DEFAULT_PORT"
