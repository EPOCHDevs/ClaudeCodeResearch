#!/bin/bash
#
# Build generate_job_data target with single-instance lock
# Only one agent/process can run this at a time
#
# Usage:
#   ./build_generate_job_data.sh                  # Release build (default)
#   ./build_generate_job_data.sh --asan           # Debug build with AddressSanitizer
#   ./build_generate_job_data.sh -j4              # Limit to 4 parallel jobs
#   ./build_generate_job_data.sh --asan -j8       # ASAN build with 8 jobs
#

set -e

SCRIPT_NAME="build_generate_job_data"
TARGET="generate_job_data"

# Defaults
BUILD_MODE="release"
BACKEND_DIR="$HOME/EpochDev/EpochBackend"
BUILD_DIR="$BACKEND_DIR/build"
NUM_JOBS=$(( $(nproc) > 8 ? 8 : $(nproc) ))

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --asan)
            BUILD_MODE="asan"
            BUILD_DIR="$BACKEND_DIR/build-asan"
            shift
            ;;
        --coverage)
            BUILD_MODE="coverage"
            BUILD_DIR="$BACKEND_DIR/build-coverage"
            shift
            ;;
        -j|--jobs)
            if [[ -n "$2" && "$2" =~ ^[0-9]+$ ]]; then
                NUM_JOBS="$2"
                shift 2
            else
                echo "[$SCRIPT_NAME] ERROR: -j/--jobs requires a numeric argument"
                exit 1
            fi
            ;;
        -j*)
            NUM_JOBS="${1#-j}"
            if [[ ! "$NUM_JOBS" =~ ^[0-9]+$ ]]; then
                echo "[$SCRIPT_NAME] ERROR: Invalid job count: $NUM_JOBS"
                exit 1
            fi
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--asan|--coverage] [-j N]"
            echo ""
            echo "Options:"
            echo "  --asan       Debug build with AddressSanitizer"
            echo "  --coverage   Coverage build (debug, no sanitizers)"
            echo "  -j, --jobs N Limit parallel build jobs (default: $(nproc))"
            echo "  -h, --help   Show this help message"
            exit 0
            ;;
        *)
            echo "[$SCRIPT_NAME] ERROR: Unknown argument: $1"
            exit 1
            ;;
    esac
done

LOCKFILE="/tmp/${SCRIPT_NAME}_${BUILD_MODE}.lock"

# Acquire exclusive lock (non-blocking)
exec 200>"$LOCKFILE"
if ! flock -n 200; then
    echo "[$SCRIPT_NAME] Another $BUILD_MODE build is already running. Waiting..."
    flock 200  # Block until lock is available
fi

echo "[$SCRIPT_NAME] Lock acquired. Starting build..."
echo "[$SCRIPT_NAME] Mode: $BUILD_MODE"
echo "[$SCRIPT_NAME] Build dir: $BUILD_DIR"
echo "[$SCRIPT_NAME] Target: $TARGET"
echo "[$SCRIPT_NAME] Jobs: $NUM_JOBS"

# Verify build directory exists
if [[ ! -d "$BUILD_DIR" ]]; then
    echo "[$SCRIPT_NAME] ERROR: Build directory does not exist: $BUILD_DIR"
    exit 1
fi

# Run the build
cd "$BUILD_DIR"
ninja -j"$NUM_JOBS" "$TARGET"

echo "[$SCRIPT_NAME] Build complete."
