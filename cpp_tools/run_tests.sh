#!/bin/bash
#
# Run Catch3 tests by target name
# Builds with release by default, then runs the specified test targets
#
# Usage:
#   ./run_tests.sh <target1> [target2] [...]              # Run specific tests (release)
#   ./run_tests.sh --asan <target1> [target2] [...]       # Run with ASAN build
#   ./run_tests.sh -j4 <target1> [target2] [...]          # Limit to 4 build jobs
#   ./run_tests.sh --list                                 # List available test targets
#   ./run_tests.sh <target> -- [catch3 args]              # Pass args to Catch3
#
# Examples:
#   ./run_tests.sh epoch_frame_test
#   ./run_tests.sh epoch_frame_test epoch_script_test
#   ./run_tests.sh epoch_frame_test -- --list-tests
#   ./run_tests.sh epoch_frame_test -- "[datetime]"       # Run tests with tag
#   ./run_tests.sh epoch_frame_test -- -s                 # Show successful tests
#   ./run_tests.sh --asan epoch_trading_test
#   ./run_tests.sh -j4 epoch_frame_test                   # Use 4 parallel jobs
#

set -e

SCRIPT_NAME="run_tests"
BACKEND_DIR="$HOME/EpochDev/EpochBackend"
NUM_JOBS=$(( $(nproc) > 16 ? 16 : $(nproc) ))

# Available test targets
AVAILABLE_TESTS=(
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

print_usage() {
    echo "Usage: $0 [options] <target1> [target2] [...] [-- catch3_args]"
    echo ""
    echo "Options:"
    echo "  --asan       Use ASAN build instead of release (default: release)"
    echo "  --no-build   Skip building, just run existing executables"
    echo "  -j, --jobs N Limit parallel build jobs (default: $(nproc))"
    echo "  --list       List available test targets"
    echo "  -h, --help   Show this help message"
    echo ""
    echo "Available test targets:"
    for target in "${AVAILABLE_TESTS[@]}"; do
        echo "  - $target"
    done
    echo ""
    echo "Examples:"
    echo "  $0 epoch_frame_test                    # Build and run with release"
    echo "  $0 --asan epoch_trading_test           # Build and run with ASAN"
    echo "  $0 epoch_frame_test -- --list-tests    # List all test cases"
    echo "  $0 epoch_frame_test -- \"[datetime]\"    # Run tests with [datetime] tag"
    echo "  $0 epoch_frame_test -- -s              # Show successful tests"
    echo "  $0 epoch_frame_test epoch_script_test  # Run multiple test targets"
}

list_targets() {
    echo -e "${BLUE}Available test targets:${NC}"
    for target in "${AVAILABLE_TESTS[@]}"; do
        # Check if executable exists in either build directory
        if [[ -x "${BACKEND_DIR}/build/bin/${target}" ]] || [[ -x "${BACKEND_DIR}/build-asan/bin/${target}" ]]; then
            echo -e "  ${GREEN}●${NC} $target"
        else
            echo -e "  ${YELLOW}○${NC} $target (not built)"
        fi
    done
}

validate_target() {
    local target="$1"
    for valid in "${AVAILABLE_TESTS[@]}"; do
        if [[ "$target" == "$valid" ]]; then
            return 0
        fi
    done
    return 1
}

# Parse arguments
BUILD_MODE="release"
BUILD_DIR="${BACKEND_DIR}/build"
SKIP_BUILD=false
TARGETS=()
CATCH_ARGS=()
PARSING_CATCH_ARGS=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --asan)
            BUILD_MODE="asan"
            BUILD_DIR="${BACKEND_DIR}/build-asan"
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
            # Handle -jN format (no space)
            NUM_JOBS="${1#-j}"
            if [[ ! "$NUM_JOBS" =~ ^[0-9]+$ ]]; then
                echo -e "${RED}Error: Invalid job count: $NUM_JOBS${NC}"
                exit 1
            fi
            shift
            ;;
        --list)
            list_targets
            exit 0
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        --)
            PARSING_CATCH_ARGS=true
            shift
            ;;
        *)
            if $PARSING_CATCH_ARGS; then
                CATCH_ARGS+=("$1")
            else
                TARGETS+=("$1")
            fi
            shift
            ;;
    esac
done

# Validate we have at least one target
if [[ ${#TARGETS[@]} -eq 0 ]]; then
    echo -e "${RED}Error: No test targets specified${NC}"
    echo ""
    print_usage
    exit 1
fi

# Validate all targets
for target in "${TARGETS[@]}"; do
    if ! validate_target "$target"; then
        echo -e "${RED}Error: Unknown test target: $target${NC}"
        echo ""
        echo "Run '$0 --list' to see available targets"
        exit 1
    fi
done

# Check build directory exists
if [[ ! -d "$BUILD_DIR" ]]; then
    echo -e "${RED}Error: Build directory does not exist: $BUILD_DIR${NC}"
    if [[ "$BUILD_MODE" == "asan" ]]; then
        echo "Hint: You may need to configure the ASAN build first (cmake preset)"
    fi
    exit 1
fi

# Build targets if not skipping
if ! $SKIP_BUILD; then
    LOCKFILE="/tmp/${SCRIPT_NAME}_${BUILD_MODE}.lock"

    # Acquire exclusive lock (non-blocking first, then wait)
    exec 200>"$LOCKFILE"
    if ! flock -n 200; then
        echo -e "${YELLOW}[$SCRIPT_NAME] Another $BUILD_MODE build is already running. Waiting...${NC}"
        flock 200  # Block until lock is available
    fi

    echo -e "${BLUE}[$SCRIPT_NAME] Lock acquired. Building targets...${NC}"
    echo "  Mode: $BUILD_MODE"
    echo "  Build dir: $BUILD_DIR"
    echo "  Jobs: $NUM_JOBS"
    echo "  Targets: ${TARGETS[*]}"
    echo ""

    cd "$BUILD_DIR"

    # Build all targets together for efficiency
    if ! ninja -j"$NUM_JOBS" "${TARGETS[@]}"; then
        echo -e "${RED}[$SCRIPT_NAME] Build failed${NC}"
        exit 1
    fi

    echo -e "${GREEN}[$SCRIPT_NAME] Build complete${NC}"
    echo ""
fi

# Run each test target
FAILED_TESTS=()
PASSED_TESTS=()

for target in "${TARGETS[@]}"; do
    EXECUTABLE="${BUILD_DIR}/bin/${target}"

    if [[ ! -x "$EXECUTABLE" ]]; then
        echo -e "${RED}Error: Executable not found: $EXECUTABLE${NC}"
        FAILED_TESTS+=("$target")
        continue
    fi

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Running: $target${NC}"
    if [[ ${#CATCH_ARGS[@]} -gt 0 ]]; then
        echo -e "${YELLOW}  Args: ${CATCH_ARGS[*]}${NC}"
    fi
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    if "$EXECUTABLE" "${CATCH_ARGS[@]}"; then
        PASSED_TESTS+=("$target")
        echo ""
        echo -e "${GREEN}✓ $target passed${NC}"
    else
        FAILED_TESTS+=("$target")
        echo ""
        echo -e "${RED}✗ $target failed${NC}"
    fi
    echo ""
done

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [[ ${#PASSED_TESTS[@]} -gt 0 ]]; then
    echo -e "${GREEN}Passed (${#PASSED_TESTS[@]}):${NC}"
    for t in "${PASSED_TESTS[@]}"; do
        echo -e "  ${GREEN}✓${NC} $t"
    done
fi

if [[ ${#FAILED_TESTS[@]} -gt 0 ]]; then
    echo -e "${RED}Failed (${#FAILED_TESTS[@]}):${NC}"
    for t in "${FAILED_TESTS[@]}"; do
        echo -e "  ${RED}✗${NC} $t"
    done
    exit 1
fi

echo ""
echo -e "${GREEN}All tests passed!${NC}"
