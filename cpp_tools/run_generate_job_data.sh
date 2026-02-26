#!/bin/bash
#
# Run generate_job_data binary
#
# Usage:
#   ./run_generate_job_data.sh <args>              # Release build (default)
#   ./run_generate_job_data.sh --asan <args>       # Debug build with AddressSanitizer
#   ./run_generate_job_data.sh --coverage <args>   # Coverage build (debug, no sanitizers)
#
# Examples:
#   ./run_generate_job_data.sh "path/to/definition.json" --start 2023-01-01 --end 2023-12-31
#   ./run_generate_job_data.sh --asan "path/to/definition.json" --cash 100000
#

set -e

SCRIPT_NAME="run_generate_job_data"
BIN_NAME="generate_job_data"

# Default to release build
BACKEND_DIR="$HOME/EpochDev/EpochBackend"
BUILD_DIR="$BACKEND_DIR/build"
BUILD_MODE="release"

# Check for build mode flag (must be first argument)
if [[ "$1" == "--asan" ]]; then
    BUILD_MODE="asan"
    BUILD_DIR="$BACKEND_DIR/build-asan"
    shift  # Remove flag from arguments
elif [[ "$1" == "--coverage" ]]; then
    BUILD_MODE="coverage"
    BUILD_DIR="$BACKEND_DIR/build-coverage"
    shift  # Remove flag from arguments
fi

BIN_PATH="$BUILD_DIR/bin/$BIN_NAME"

# Verify binary exists
if [[ ! -x "$BIN_PATH" ]]; then
    echo "[$SCRIPT_NAME] ERROR: Binary not found or not executable: $BIN_PATH"
    echo "[$SCRIPT_NAME] Run build_generate_job_data.sh $([ "$BUILD_MODE" == "asan" ] && echo "--asan") first"
    exit 1
fi

echo "[$SCRIPT_NAME] Mode: $BUILD_MODE"
echo "[$SCRIPT_NAME] Binary: $BIN_PATH"
echo "[$SCRIPT_NAME] Args: $@"
echo ""

# Run the binary with remaining arguments
exec "$BIN_PATH" "$@"
