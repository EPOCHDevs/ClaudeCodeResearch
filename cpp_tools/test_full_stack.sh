#!/bin/bash
#
# Full-stack test for tearsheet migration + AI agents
#
# Prerequisites:
#   1. Backend server running: ./run_server.sh
#   2. Portal running: cd EpochPortal && npm run dev
#   3. LangGraph dev server: cd EpochAI && langgraph dev
#   4. Postgres running (for LangGraph checkpoints)
#
# Usage:
#   ./test_full_stack.sh [--token TOKEN]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_URL="http://localhost:9000"
PORTAL_URL="http://localhost:3001"
AI_URL="http://localhost:8123"
HANDBOOK="$HOME/EpochDev/ClaudeCodeResearch/project_hand_book/definitions/test_runner"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get token
TOKEN="${1:-}"
if [[ "$TOKEN" == "--token" ]]; then TOKEN="${2:-}"; fi
if [[ -z "$TOKEN" ]]; then
    TOKEN=$(python3 "$HOME/EpochDev/EpochAI/tools/cognito_auth.py" token 2>/dev/null) || true
fi
if [[ -z "$TOKEN" ]]; then
    echo -e "${RED}No auth token. Run: python3 ~/EpochDev/EpochAI/tools/cognito_auth.py login${NC}"
    exit 1
fi

PASS=0; FAIL=0

check() {
    local name="$1" result="$2"
    if [[ "$result" == "PASS" ]]; then
        echo -e "  ${GREEN}✓${NC} $name"
        PASS=$((PASS+1))
    else
        echo -e "  ${RED}✗${NC} $name — $result"
        FAIL=$((FAIL+1))
    fi
}

# ============================================================================
echo -e "${BLUE}=== 1. Backend Health ===${NC}"
# ============================================================================

r=$(curl -s "$BACKEND_URL/api/v1/health" 2>/dev/null)
[[ "$r" == *"ok"* ]] && check "Server health" "PASS" || check "Server health" "Server not responding"

# ============================================================================
echo -e "${BLUE}=== 2. Execute Study ===${NC}"
# ============================================================================

DEF=$(cat "$HANDBOOK/reporter_cluster_lines_handbook.json" | python3 -c "import sys,json; d=json.load(sys.stdin); d['data']['cache_dir']='$HOME/EpochDev/ClaudeCodeResearch/project/market_data'; print(json.dumps(d))" 2>/dev/null)
DEF_ID=$(curl -s -X POST "$BACKEND_URL/api/v1/studies/definitions" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "$DEF" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
EXEC_ID=$(curl -s -X POST "$BACKEND_URL/api/v1/studies/executions" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"id\": \"$DEF_ID\", \"period\": {\"start\": \"2020-01-01\", \"end\": \"2025-12-31\"}}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('execution_id',d.get('id','')))" 2>/dev/null)
sleep 3

[[ -n "$EXEC_ID" ]] && check "Study execution" "PASS" || check "Study execution" "No execution ID"
echo "  Execution ID: $EXEC_ID"

# ============================================================================
echo -e "${BLUE}=== 3. Dashboard Schema Endpoint ===${NC}"
# ============================================================================

SCHEMA=$(curl -s "$BACKEND_URL/api/v1/studies/executions/$EXEC_ID/dashboard/schema?category=SPY-Stocks" -H "Authorization: Bearer $TOKEN")
CHARTS=$(echo "$SCHEMA" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('charts',[])))" 2>/dev/null)
[[ "$CHARTS" -gt 0 ]] && check "Schema endpoint ($CHARTS charts)" "PASS" || check "Schema endpoint" "No charts"

# ============================================================================
echo -e "${BLUE}=== 4. Arrow Data Endpoint ===${NC}"
# ============================================================================

ARROW_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/v1/studies/executions/$EXEC_ID/dashboard/data/chart_0?category=SPY-Stocks" -H "Authorization: Bearer $TOKEN")
[[ "$ARROW_STATUS" == "200" ]] && check "Arrow data endpoint" "PASS" || check "Arrow data endpoint" "HTTP $ARROW_STATUS"

# ============================================================================
echo -e "${BLUE}=== 5. DuckDB Query on Chart Tables ===${NC}"
# ============================================================================

QUERY_RESULT=$(curl -s -X POST "$BACKEND_URL/api/v1/studies/executions/$EXEC_ID/query" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"queries": [{"name": "test", "sql": "SELECT COUNT(*) as cnt FROM chart_spy_stocks_chart_0"}]}' -o /tmp/test_query.bin -w "%{http_code}")
if [[ "$QUERY_RESULT" == "200" ]]; then
    CNT=$(python3 -c "import pyarrow.ipc as ipc; r=ipc.open_stream('/tmp/test_query.bin').read_all(); print(r.to_pandas().iloc[0,0])" 2>/dev/null)
    [[ "$CNT" -gt 0 ]] && check "DuckDB chart query ($CNT rows)" "PASS" || check "DuckDB chart query" "0 rows"
else
    check "DuckDB chart query" "HTTP $QUERY_RESULT"
fi

# ============================================================================
echo -e "${BLUE}=== 6. AI Notes Endpoint ===${NC}"
# ============================================================================

NOTES_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BACKEND_URL/api/v1/studies/executions/$EXEC_ID/dashboard/ai-notes?category=SPY-Stocks" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"chart_notes": {"0": "Test note for chart 0"}, "table_notes": {}, "event_summary": "Test event summary"}')
[[ "$NOTES_STATUS" == "200" ]] && check "AI Notes POST endpoint" "PASS" || check "AI Notes POST endpoint" "HTTP $NOTES_STATUS"

# Verify note was saved in schema
SAVED_NOTE=$(curl -s "$BACKEND_URL/api/v1/studies/executions/$EXEC_ID/dashboard/schema?category=SPY-Stocks" -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['charts'][0].get('ai_note',''))" 2>/dev/null)
[[ "$SAVED_NOTE" == "Test note for chart 0" ]] && check "AI Note persisted in schema" "PASS" || check "AI Note persisted" "Note not found"

SAVED_SUMMARY=$(curl -s "$BACKEND_URL/api/v1/studies/executions/$EXEC_ID/dashboard/schema?category=SPY-Stocks" -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('event_summary',''))" 2>/dev/null)
[[ "$SAVED_SUMMARY" == "Test event summary" ]] && check "Event summary persisted" "PASS" || check "Event summary persisted" "Not found"

# ============================================================================
echo -e "${BLUE}=== 7. Portal (manual) ===${NC}"
# ============================================================================

echo -e "  ${YELLOW}→${NC} Open ${PORTAL_URL}/playground/studies"
echo -e "  ${YELLOW}→${NC} Click execution: $EXEC_ID"
echo -e "  ${YELLOW}→${NC} Verify: charts render, AI Insight shows on chart 0"
echo -e "  ${YELLOW}→${NC} Verify: 'AI Notes' button on categories without notes"

# ============================================================================
echo -e "${BLUE}=== 8. AI Notes Agent (manual) ===${NC}"
# ============================================================================

echo -e "  ${YELLOW}→${NC} Run in Python:"
echo "    from agent_src.agents.ai_notes import generate_ai_notes"
echo "    notes = await generate_ai_notes('$EXEC_ID', 'SPY-Stocks', '$TOKEN')"

# ============================================================================
echo -e "${BLUE}=== 9. Query Dashboard Agent (manual) ===${NC}"
# ============================================================================

echo -e "  ${YELLOW}→${NC} Run in Python:"
echo "    from agent_src.agents.query_dashboard import query_dashboard, DashboardQuestion"
echo "    answers = await query_dashboard('$EXEC_ID', ["
echo "        DashboardQuestion(component_id=0, question='what is the trend?'),"
echo "    ], category='SPY-Stocks', authorization='$TOKEN')"

# ============================================================================
echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo -e "  ${GREEN}Pass: $PASS${NC}"
echo -e "  ${RED}Fail: $FAIL${NC}"
echo ""
echo "  Execution ID: $EXEC_ID"
[[ $FAIL -eq 0 ]] && echo -e "  ${GREEN}All automated checks passed!${NC}" || echo -e "  ${RED}Some checks failed${NC}"
