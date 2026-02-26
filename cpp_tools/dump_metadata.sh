#!/bin/bash
#
# Fetch documentation from stratifyx server
#
# Workflow:
#   1. Build epoch_stratifyx_server and generate_grammars
#   2. Generate EpochScript EBNF grammar
#   3. Start server on port 9002
#   4. Fetch schemas, transforms, enums, and metadata
#   5. Stop server
#
# Outputs:
#   docs/epochscript.ebnf         - Generated grammar
#   docs/schemas.json             - /api/v1/schemas (raw=false)
#   docs/transform_metadata.json  - /api/v1/metadata/transforms
#   docs/enums.json               - /api/v1/enums
#   docs/assets.json              - /api/v1/metadata/assets
#   docs/index_constituents.json  - /api/v1/metadata/index_constituents
#   docs/fred_series.json         - /api/v1/metadata/fred_series
#

set -e

SCRIPT_NAME="dump_metadata"
DOCS_DIR="$HOME/EpochDev/ClaudeCodeResearch/docs"
BUILD_DIR="$HOME/EpochDev/EpochBackend/build"
SERVER_BIN="$BUILD_DIR/bin/epoch_stratifyx_server"
SERVER_PORT=9002
SERVER_URL="http://localhost:$SERVER_PORT"
SERVER_PID=""
LOCKFILE="/tmp/${SCRIPT_NAME}.lock"

# Acquire exclusive lock
exec 200>"$LOCKFILE"
if ! flock -n 200; then
    echo "[$SCRIPT_NAME] Another instance is already running. Waiting..."
    flock 200
fi
echo "[$SCRIPT_NAME] Lock acquired."

# Cleanup function
cleanup() {
    if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "[$SCRIPT_NAME] Stopping server (PID $SERVER_PID)..."
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
    # Clean up temp server directory
    if [[ -n "$SERVER_WORKDIR" ]] && [[ -d "$SERVER_WORKDIR" ]]; then
        rm -rf "$SERVER_WORKDIR"
    fi
}
trap cleanup EXIT

# Build targets
echo "[$SCRIPT_NAME] Building epoch_stratifyx_server and generate_grammars..."
ninja -C "$BUILD_DIR" -j$(( $(nproc) > 16 ? 16 : $(nproc) )) epoch_stratifyx_server generate_grammars

# Verify binary exists
if [[ ! -x "$SERVER_BIN" ]]; then
    echo "[$SCRIPT_NAME] ERROR: Server binary not found: $SERVER_BIN"
    exit 1
fi

# Ensure docs directory exists
mkdir -p "$DOCS_DIR"

# Generate grammar and copy EBNF
GRAMMAR_BIN="$BUILD_DIR/bin/generate_grammars"
RUNTIME_DIR="$HOME/EpochDev/EpochBackend/services/stratifyx/test/integration/test_runner"
echo "[$SCRIPT_NAME] Generating grammars..."
(cd "$RUNTIME_DIR" && "$GRAMMAR_BIN" .) > /dev/null 2>&1
cp "$RUNTIME_DIR/docs/epochscript.ebnf" "$DOCS_DIR/"
echo "[$SCRIPT_NAME] Copied epochscript.ebnf"

# Start server from temp directory to avoid polluting cpp_tools
SERVER_WORKDIR=$(mktemp -d)
echo ""
echo "[$SCRIPT_NAME] Starting server on port $SERVER_PORT..."
(cd "$SERVER_WORKDIR" && "$SERVER_BIN" --port "$SERVER_PORT") &
SERVER_PID=$!

# Wait for server to be ready
echo "[$SCRIPT_NAME] Waiting for server to start..."
for i in {1..30}; do
    if curl -sf "$SERVER_URL/health" > /dev/null 2>&1; then
        echo "[$SCRIPT_NAME] Server ready!"
        break
    fi
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "[$SCRIPT_NAME] ERROR: Server failed to start"
        exit 1
    fi
    sleep 1
done

echo ""

# Fetch and format JSON
fetch_json() {
    local endpoint=$1
    local output=$2
    echo "[$SCRIPT_NAME] Fetching $output..."
    curl -sf "$SERVER_URL$endpoint" | python3 -m json.tool > "$output"
}

# Fetch raw text (non-JSON responses)
fetch_text() {
    local endpoint=$1
    local output=$2
    echo "[$SCRIPT_NAME] Fetching $output..."
    curl -sf "$SERVER_URL$endpoint" > "$output"
}

# Schemas (raw=false returns Python-like representations)
fetch_text "/api/v1/schemas?raw=false" "$DOCS_DIR/schemas.txt"

# Transforms
fetch_json "/api/v1/metadata/transforms" "$DOCS_DIR/transform_metadata.json"

# Enums
fetch_json "/api/v1/enums" "$DOCS_DIR/enums.json"

# Assets & index constituents
fetch_json "/api/v1/metadata/assets" "$DOCS_DIR/assets.json"
fetch_json "/api/v1/metadata/index_constituents" "$DOCS_DIR/index_constituents.json"

# FRED series
fetch_json "/api/v1/metadata/fred_series?page_size=10000" "$DOCS_DIR/fred_series.json"

echo ""
echo "[$SCRIPT_NAME] Done. Files:"
ls -la "$DOCS_DIR"/ 2>/dev/null || true
