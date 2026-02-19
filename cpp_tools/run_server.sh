#!/bin/bash
#
# Build (if stale) and run epoch_stratifyx_server
#
# Usage:
#   ./run_server.sh          # Release build, default port
#   ./run_server.sh --asan   # Debug build with AddressSanitizer
#
# The server runs on port 8080 by default.
# Press Ctrl+C to stop.
#

set -e

SCRIPT_NAME="run_server"
TARGET="epoch_stratifyx_server"
DEFAULT_PORT=8080

# Default to release build
BUILD_MODE="release"
BUILD_DIR="/home/adesola/EpochDev/EpochBackend/build"

# Check for --asan flag
if [[ "$1" == "--asan" ]]; then
    BUILD_MODE="asan"
    BUILD_DIR="/home/adesola/EpochDev/EpochBackend/build-asan"
    shift
fi

BIN_PATH="$BUILD_DIR/bin/$TARGET"

echo "[$SCRIPT_NAME] Mode: $BUILD_MODE"
echo "[$SCRIPT_NAME] Build dir: $BUILD_DIR"

# Verify build directory exists
if [[ ! -d "$BUILD_DIR" ]]; then
    echo "[$SCRIPT_NAME] ERROR: Build directory does not exist: $BUILD_DIR"
    exit 1
fi

# Build if stale (ninja handles staleness check automatically)
echo "[$SCRIPT_NAME] Building $TARGET (if stale)..."
ninja -C "$BUILD_DIR" -j$(( $(nproc) > 16 ? 16 : $(nproc) )) "$TARGET"

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
