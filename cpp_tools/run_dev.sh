#!/bin/bash
#
# Start both the Epoch server and LangGraph dev in parallel.
#
# Usage:
#   ./run_dev.sh              # Release build server + langgraph dev
#   ./run_dev.sh --no-build   # Skip server build
#   ./run_dev.sh --asan       # ASAN server build
#
# Press Ctrl+C to stop both processes.
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EPOCH_AI_DIR="$(cd "$SCRIPT_DIR/../../EpochAI" && pwd)"

cleanup() {
    echo ""
    echo "[run_dev] Stopping all processes..."
    kill 0 2>/dev/null
    wait 2>/dev/null
    echo "[run_dev] Done."
}
trap cleanup EXIT INT TERM

echo "[run_dev] Starting Epoch server..."
"$SCRIPT_DIR/run_server.sh" "$@" &
SERVER_PID=$!

echo "[run_dev] Starting LangGraph dev..."
(
    source "$EPOCH_AI_DIR/.venv/bin/activate"
    cd "$EPOCH_AI_DIR"
    exec langgraph dev
) &
LANGGRAPH_PID=$!

echo "[run_dev] Server PID: $SERVER_PID"
echo "[run_dev] LangGraph PID: $LANGGRAPH_PID"
echo "[run_dev] Press Ctrl+C to stop both"

wait
