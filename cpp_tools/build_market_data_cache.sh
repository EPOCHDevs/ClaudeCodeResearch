#!/bin/bash
set -e

BUILD_DIR="$HOME/EpochDev/EpochBackend/build"
TARGET="build_market_data_cache"
BIN="$BUILD_DIR/bin/$TARGET"

# Build the binary
echo "Building $TARGET..."
cd "$BUILD_DIR"
ninja -j$(nproc) "$TARGET"
echo "Build complete."

"$BIN"

echo "Syncing to S3..."
aws s3 sync $HOME/EpochDev/ClaudeCodeResearch/project/market_data \
    s3://epoch-db/market_data --exclude "*.lock"
echo "Done."
