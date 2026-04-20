#!/bin/bash
#
# (Re)configure CMake build directories using presets
#
# Usage:
#   ./configure.sh              # Configure all presets
#   ./configure.sh release      # Configure release only
#   ./configure.sh asan coverage # Configure specific presets
#   ./configure.sh --list       # List available presets
#   ./configure.sh --clean release # Wipe + reconfigure release
#
# Presets: release, asan, tsan, coverage
#

set -e

BACKEND_DIR="$HOME/EpochDev/EpochBackend"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ALL_PRESETS=(release asan tsan coverage)

preset_build_dir() {
    case "$1" in
        release)  echo "${BACKEND_DIR}/build" ;;
        asan)     echo "${BACKEND_DIR}/build-asan" ;;
        tsan)     echo "${BACKEND_DIR}/build-tsan" ;;
        coverage) echo "${BACKEND_DIR}/build-coverage" ;;
        *)        echo "" ;;
    esac
}

list_presets() {
    echo -e "${BLUE}Available CMake presets:${NC}"
    for preset in "${ALL_PRESETS[@]}"; do
        local dir
        dir=$(preset_build_dir "$preset")
        if [[ -f "${dir}/build.ninja" ]]; then
            echo -e "  ${GREEN}●${NC} ${preset}  (${dir})"
        elif [[ -d "${dir}" ]]; then
            echo -e "  ${YELLOW}○${NC} ${preset}  (${dir} — needs configure)"
        else
            echo -e "  ${RED}○${NC} ${preset}  (not created)"
        fi
    done
}

configure_preset() {
    local preset="$1"
    local clean="$2"
    local dir
    dir=$(preset_build_dir "$preset")

    if [[ -z "$dir" ]]; then
        echo -e "${RED}Error: Unknown preset '$preset'${NC}"
        echo "Valid presets: ${ALL_PRESETS[*]}"
        return 1
    fi

    if [[ "$clean" == "clean" && -d "$dir" ]]; then
        echo -e "${YELLOW}[configure] Cleaning ${dir}${NC}"
        # Preserve bin/ if it has built executables (avoid re-linking everything)
        rm -rf "${dir}/CMakeCache.txt" "${dir}/CMakeFiles" "${dir}/build.ninja" \
               "${dir}/.cmake" "${dir}/cmake_install.cmake" "${dir}/.ninja_deps" \
               "${dir}/.ninja_log"
    fi

    echo -e "${BLUE}[configure] Configuring preset: ${preset}${NC}"
    echo "  Directory: ${dir}"
    echo ""

    cd "$BACKEND_DIR"
    if cmake --preset "$preset"; then
        echo ""
        echo -e "${GREEN}[configure] ${preset} configured successfully${NC}"
    else
        echo ""
        echo -e "${RED}[configure] ${preset} configuration failed${NC}"
        return 1
    fi
}

# Parse arguments
CLEAN=false
PRESETS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --list|-l)
            list_presets
            exit 0
            ;;
        --clean|-c)
            CLEAN=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options] [preset1] [preset2] ..."
            echo ""
            echo "Options:"
            echo "  --list, -l    List available presets and their status"
            echo "  --clean, -c   Wipe CMake cache before reconfiguring"
            echo "  -h, --help    Show this help message"
            echo ""
            echo "Presets: ${ALL_PRESETS[*]}"
            echo ""
            echo "If no presets are specified, all presets are configured."
            exit 0
            ;;
        *)
            PRESETS+=("$1")
            shift
            ;;
    esac
done

# Default: all presets
if [[ ${#PRESETS[@]} -eq 0 ]]; then
    PRESETS=("${ALL_PRESETS[@]}")
fi

FAILED=()
PASSED=()

for preset in "${PRESETS[@]}"; do
    clean_arg=""
    $CLEAN && clean_arg="clean"

    if configure_preset "$preset" "$clean_arg"; then
        PASSED+=("$preset")
    else
        FAILED+=("$preset")
    fi
    echo ""
done

# Summary
if [[ $(( ${#PASSED[@]} + ${#FAILED[@]} )) -gt 1 ]]; then
    echo -e "${BLUE}━━━ Summary ━━━${NC}"
    for p in "${PASSED[@]}"; do echo -e "  ${GREEN}✓${NC} $p"; done
    for p in "${FAILED[@]}"; do echo -e "  ${RED}✗${NC} $p"; done
fi

if [[ ${#FAILED[@]} -gt 0 ]]; then
    exit 1
fi
