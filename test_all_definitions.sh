#!/bin/bash

# Test all definition files
GENERATOR="/home/adesola/EpochDev/EpochBackend/build/release/bin/generate_job_data"
DEFS_DIR="/home/adesola/EpochDev/ClaudeCodeResearch/project/definitions/test_runner"
OUTPUT_DIR="/home/adesola/EpochDev/ClaudeCodeResearch/test_output"
RESULTS_FILE="/home/adesola/EpochDev/ClaudeCodeResearch/definition_test_results.txt"

# Short test range for validation
START_DATE="2024-01-02"
END_DATE="2024-01-15"

mkdir -p "$OUTPUT_DIR"
rm -f "$RESULTS_FILE"

echo "Testing all definitions..."
echo "=========================="
echo ""

passed=0
failed=0

for def in "$DEFS_DIR"/*.json; do
    name=$(basename "$def" .json)
    echo -n "Testing: $name ... "

    # Run with short date range, capture output
    output=$("$GENERATOR" "$def" --start "$START_DATE" --end "$END_DATE" --name "test_$name" 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "PASS"
        echo "PASS: $name" >> "$RESULTS_FILE"
        ((passed++))
    else
        echo "FAIL"
        echo "FAIL: $name" >> "$RESULTS_FILE"
        echo "  Error: $(echo "$output" | tail -3)" >> "$RESULTS_FILE"
        ((failed++))
    fi
done

echo ""
echo "=========================="
echo "Results: $passed passed, $failed failed"
echo ""
echo "Results saved to: $RESULTS_FILE"
