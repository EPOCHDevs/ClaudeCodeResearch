#!/bin/bash
#
# Build generate_job_data target via run_target.sh (shared build lock)
#
# Usage:
#   ./build_generate_job_data.sh                  # Release build (default)
#   ./build_generate_job_data.sh --asan           # Debug build with AddressSanitizer
#   ./build_generate_job_data.sh -j4              # Limit to 4 parallel jobs
#   ./build_generate_job_data.sh --asan -j8       # ASAN build with 8 jobs
#
# Delegates to run_target.sh to ensure a single build lock across all agents.
# Never runs cmake/ninja directly.
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/run_target.sh" "$@" generate_job_data
