#!/bin/bash
#
# Run Catch3 tests by target name (wrapper for run_target.sh --run)
#
# Usage:
#   ./run_tests.sh <target1> [target2] [...]              # Run specific tests (release)
#   ./run_tests.sh --asan <target1> [target2] [...]       # Run with ASAN build
#   ./run_tests.sh -j4 <target1> [target2] [...]          # Limit to 4 build jobs
#   ./run_tests.sh --list                                 # List available test targets
#   ./run_tests.sh <target> -- [catch3 args]              # Pass args to Catch3
#
# This is a compatibility wrapper. Use run_target.sh directly for more options.
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Translate --list to --list-tests for run_target.sh
ARGS=()
for arg in "$@"; do
    if [[ "$arg" == "--list" ]]; then
        ARGS+=("--list-tests")
    else
        ARGS+=("$arg")
    fi
done

exec "$SCRIPT_DIR/run_target.sh" --run "${ARGS[@]}"
