#!/bin/bash
#
# Build and optionally run any CMake/ninja target
# Supports building libraries, executables, and test targets
#
# Usage:
#   ./run_target.sh <target1> [target2] [...]              # Build targets (release, nproc jobs)
#   ./run_target.sh --asan <target1> [target2] [...]       # Build with ASAN (nproc/2 jobs)
#   ./run_target.sh --coverage <target1> [target2] [...]   # Build with coverage (nproc/2 jobs)
#   ./run_target.sh --debug <target1> [target2] [...]      # Build with debug (nproc/2 jobs)
#   ./run_target.sh --run <target> [-- catch3_args]        # Build + run executable
#   ./run_target.sh -j64 epoch_script                      # Build with 64 jobs (override)
#   ./run_target.sh --list-tests                           # List known test targets
#
# Examples:
#   ./run_target.sh epoch_script                           # Build library only
#   ./run_target.sh epoch_script_test                      # Build test binary only
#   ./run_target.sh --run epoch_script_test                # Build + run all tests
#   ./run_target.sh --run epoch_script_test -- "[compiler]" # Build + run tagged tests
#   ./run_target.sh epoch_script epoch_trading -j64        # Build multiple targets
#   ./run_target.sh --asan --run epoch_script_test         # ASAN build + run
#   ./run_target.sh --no-build --run epoch_script_test     # Just run (skip build)
#

set -e

SCRIPT_NAME="run_target"
BACKEND_DIR="$HOME/EpochDev/EpochBackend"
NUM_JOBS=""  # set after parsing based on build mode

# Known test targets (for --list-tests and auto-detection)
KNOWN_TESTS=(
    "epoch_dashboard_test"
    "epoch_data_sdk_test"
    "epoch_empyrical_test"
    "epoch_events_test"
    "epoch_folio_test"
    "epoch_frame_cal_test"
    "epoch_frame_test"
    "epoch_script_test"
    "epoch_script_test_metadata"
    "epoch_script_test_ml"
    "epoch_script_test_runtime"
    "epoch_stratifyx_integration_test"
    "epoch_stratifyx_pipeline_integration_test"
    "epoch_stratifyx_arrow_query_test"
    "epoch_stratifyx_service_test"
    "epoch_stratifyx_test"
    "epoch_trading_test"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

is_test_target() {
    local target="$1"
    for t in "${KNOWN_TESTS[@]}"; do
        if [[ "$target" == "$t" ]]; then
            return 0
        fi
    done
    return 1
}

print_usage() {
    echo "Usage: $0 [options] <target1> [target2] [...] [-- run_args]"
    echo ""
    echo "Options:"
    echo "  --asan       Use ASAN build (build-asan, nproc/2 jobs)"
    echo "  --coverage   Use coverage build (build-coverage, nproc/2 jobs)"
    echo "  --debug      Use debug build (cmake-build-debug, nproc/2 jobs)"
    echo "  --run        Run executable after building (for test/binary targets)"
    echo "  --no-build   Skip building, just run existing executables"
    echo "  -j, --jobs N Limit parallel build jobs (default: nproc)"
    echo "  --list-tests List known test targets"
    echo "  -h, --help   Show this help message"
    echo ""
    echo "Arguments after -- are passed to the executable (e.g., Catch3 args)"
    echo ""
    echo "Examples:"
    echo "  $0 epoch_script                           # Build library"
    echo "  $0 --run epoch_script_test                # Build + run tests"
    echo "  $0 --run epoch_script_test -- \"[compiler]\" # Run tagged tests"
    echo "  $0 -j64 epoch_script epoch_trading        # Parallel build"
    echo "  $0 --asan --run epoch_frame_test          # ASAN build + run"
}

list_tests() {
    echo -e "${BLUE}Known test targets:${NC}"
    for target in "${KNOWN_TESTS[@]}"; do
        if [[ -x "${BACKEND_DIR}/build/bin/${target}" ]] || [[ -x "${BACKEND_DIR}/build-asan/bin/${target}" ]]; then
            echo -e "  ${GREEN}●${NC} $target"
        else
            echo -e "  ${YELLOW}○${NC} $target (not built)"
        fi
    done
}

# Parse arguments
BUILD_MODE="release"
BUILD_DIR="${BACKEND_DIR}/build"
SKIP_BUILD=false
RUN_AFTER=false
TARGETS=()
RUN_ARGS=()
PARSING_RUN_ARGS=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --asan)
            BUILD_MODE="asan"
            BUILD_DIR="${BACKEND_DIR}/build-asan"
            shift
            ;;
        --coverage)
            BUILD_MODE="coverage"
            BUILD_DIR="${BACKEND_DIR}/build-coverage"
            shift
            ;;
        --debug)
            BUILD_MODE="debug"
            BUILD_DIR="${BACKEND_DIR}/cmake-build-debug"
            shift
            ;;
        --run)
            RUN_AFTER=true
            shift
            ;;
        --no-build)
            SKIP_BUILD=true
            shift
            ;;
        -j|--jobs)
            if [[ -n "$2" && "$2" =~ ^[0-9]+$ ]]; then
                NUM_JOBS="$2"
                shift 2
            else
                echo -e "${RED}Error: -j/--jobs requires a numeric argument${NC}"
                exit 1
            fi
            ;;
        -j*)
            NUM_JOBS="${1#-j}"
            if [[ ! "$NUM_JOBS" =~ ^[0-9]+$ ]]; then
                echo -e "${RED}Error: Invalid job count: $NUM_JOBS${NC}"
                exit 1
            fi
            shift
            ;;
        --list-tests)
            list_tests
            exit 0
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        --)
            PARSING_RUN_ARGS=true
            shift
            ;;
        *)
            if $PARSING_RUN_ARGS; then
                RUN_ARGS+=("$1")
            else
                TARGETS+=("$1")
            fi
            shift
            ;;
    esac
done

# Set default job count based on build mode if not overridden by -j
if [[ -z "$NUM_JOBS" ]]; then
    if [[ "$BUILD_MODE" == "release" ]]; then
        NUM_JOBS=$(nproc)
    else
        # coverage, debug, asan: half cores to avoid OOM from instrumentation overhead
        NUM_JOBS=$(( $(nproc) / 2 ))
        [[ "$NUM_JOBS" -lt 1 ]] && NUM_JOBS=1
    fi
fi

# Validate we have at least one target
if [[ ${#TARGETS[@]} -eq 0 ]]; then
    echo -e "${RED}Error: No targets specified${NC}"
    echo ""
    print_usage
    exit 1
fi

# Check build directory exists
if [[ ! -d "$BUILD_DIR" ]]; then
    echo -e "${RED}Error: Build directory does not exist: $BUILD_DIR${NC}"
    if [[ "$BUILD_MODE" == "asan" ]]; then
        echo "Hint: You may need to configure the ASAN build first"
    fi
    exit 1
fi

# Build targets if not skipping
if ! $SKIP_BUILD; then
    LOCKFILE="/tmp/${SCRIPT_NAME}_${BUILD_MODE}.lock"

    # Acquire exclusive lock
    exec 200>"$LOCKFILE"
    if ! flock -n 200; then
        echo -e "${YELLOW}[$SCRIPT_NAME] Another $BUILD_MODE build is running. Waiting...${NC}"
        flock 200
    fi

    echo -e "${BLUE}[$SCRIPT_NAME] Building...${NC}"
    echo "  Mode: $BUILD_MODE"
    echo "  Jobs: $NUM_JOBS"
    echo "  Targets: ${TARGETS[*]}"
    echo ""

    cd "$BUILD_DIR"

    if ! ninja -j"$NUM_JOBS" "${TARGETS[@]}"; then
        echo -e "${RED}[$SCRIPT_NAME] Build failed${NC}"
        exit 1
    fi

    echo -e "${GREEN}[$SCRIPT_NAME] Build complete${NC}"
    echo ""
fi

# Run targets if --run specified
if $RUN_AFTER; then
    FAILED=()
    PASSED=()

    for target in "${TARGETS[@]}"; do
        EXECUTABLE="${BUILD_DIR}/bin/${target}"

        if [[ ! -x "$EXECUTABLE" ]]; then
            echo -e "${YELLOW}[$SCRIPT_NAME] No executable for '$target' — skipping run${NC}"
            continue
        fi

        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BLUE}Running: $target${NC}"
        if [[ ${#RUN_ARGS[@]} -gt 0 ]]; then
            echo -e "${YELLOW}  Args: ${RUN_ARGS[*]}${NC}"
        fi
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""

        if "$EXECUTABLE" "${RUN_ARGS[@]}"; then
            PASSED+=("$target")
            echo -e "${GREEN}✓ $target passed${NC}"
        else
            FAILED+=("$target")
            echo -e "${RED}✗ $target failed${NC}"
        fi
        echo ""
    done

    # Summary (only if multiple targets)
    if [[ $(( ${#PASSED[@]} + ${#FAILED[@]} )) -gt 1 ]]; then
        echo -e "${BLUE}━━━ Summary ━━━${NC}"
        for t in "${PASSED[@]}"; do echo -e "  ${GREEN}✓${NC} $t"; done
        for t in "${FAILED[@]}"; do echo -e "  ${RED}✗${NC} $t"; done
    fi

    if [[ ${#FAILED[@]} -gt 0 ]]; then
        exit 1
    fi
fi
