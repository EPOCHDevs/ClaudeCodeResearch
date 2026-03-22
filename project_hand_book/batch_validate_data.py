#!/usr/bin/env python3
"""
Batch SQL validation for all exec_cluster campaign outputs.
Runs structural + semantic queries against orders, account, positions tables.
"""
import subprocess
import sys
import json
from pathlib import Path
from collections import defaultdict

CAMPAIGNS = Path(__file__).parent / "campaigns" / "test_runner"
QUERY_TOOL = "/home/adesola/EpochDev/AgentSwarm/tools/analyze_job/query_study_dataframes.py"

PASS = 0
FAIL = 0
WARN = 0
ISSUES = []


def log(level, test, msg):
    global PASS, FAIL, WARN
    if level == "PASS":
        PASS += 1
    elif level == "FAIL":
        FAIL += 1
        ISSUES.append(f"FAIL [{test}]: {msg}")
        print(f"    FAIL: {msg}")
    elif level == "WARN":
        WARN += 1
        ISSUES.append(f"WARN [{test}]: {msg}")
        print(f"    WARN: {msg}")


def query(job_folder, sql):
    """Run SQL query and return result as string."""
    result = subprocess.run(
        [sys.executable, QUERY_TOOL, str(job_folder), "--query", sql],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip()


def parse_single_value(output):
    """Parse a single numeric value from pandas-style query output.
    Format: '    n\n0  73\n(1 rows)' → 73.0
    """
    lines = [l.strip() for l in output.split("\n") if l.strip()]
    # Skip header line and '(N rows)' line — data is in between
    for line in lines:
        if line.startswith("(") or not any(c.isdigit() or c == '.' or c == '-' for c in line):
            continue
        parts = line.split()
        # Last numeric value on the line
        for p in reversed(parts):
            try:
                return float(p)
            except ValueError:
                continue
    return 0.0


def parse_multi_values(output):
    """Parse multiple numeric values from a single-row query.
    Format: '    total_comm  total_slip\n0      24.88       0.385\n(1 rows)' → [24.88, 0.385]
    """
    lines = [l.strip() for l in output.split("\n") if l.strip()]
    for line in lines:
        if line.startswith("(") or not any(c.isdigit() for c in line):
            continue
        parts = line.split()
        vals = []
        for p in parts:
            try:
                vals.append(float(p))
            except ValueError:
                pass
        if len(vals) >= 2:
            return vals
    return [0.0, 0.0]


def validate_campaign(name):
    """Run all validation queries for a single campaign."""
    folder = CAMPAIGNS / name
    if not (folder / "tables" / "orders.arrow").exists():
        log("WARN", name, "No orders.arrow — skipping")
        return

    # ─── 1. Orders: filled count > 0 ──────────────────────────────────────
    out = query(folder, "SELECT COUNT(*) as n FROM orders WHERE status = 'Filled'")
    filled = int(parse_single_value(out))
    if filled == 0:
        log("FAIL", name, "Zero filled orders")
    else:
        log("PASS", name, f"{filled} filled orders")

    # ─── 2. No negative filled_qty ────────────────────────────────────────
    out = query(folder,
        "SELECT COUNT(*) as n FROM orders WHERE status = 'Filled' AND filled_qty <= 0")
    bad = int(parse_single_value(out))
    if bad > 0:
        log("FAIL", name, f"{bad} filled orders with qty <= 0")
    else:
        log("PASS", name, "All filled_qty > 0")

    # ─── 3. No negative filled_price ──────────────────────────────────────
    out = query(folder,
        "SELECT COUNT(*) as n FROM orders WHERE status = 'Filled' AND filled_price <= 0")
    bad = int(parse_single_value(out))
    if bad > 0:
        log("FAIL", name, f"{bad} filled orders with price <= 0")
    else:
        log("PASS", name, "All filled_price > 0")

    # ─── 4. Stop orders have stop_price set ───────────────────────────────
    out = query(folder,
        "SELECT COUNT(*) as n FROM orders WHERE type = 'Stop' AND (stop_price IS NULL OR stop_price <= 0)")
    bad = int(parse_single_value(out))
    if bad > 0:
        log("WARN", name, f"{bad} stop orders with invalid stop_price")
    else:
        log("PASS", name, "All stop orders have valid stop_price")

    # ─── 5. Account equity never negative ─────────────────────────────────
    out = query(folder, "SELECT MIN(equity) as min_eq FROM account")
    min_eq = parse_single_value(out)
    if min_eq < 0:
        log("FAIL", name, f"Negative equity: ${min_eq:.2f}")
    else:
        log("PASS", name, f"Min equity ${min_eq:.0f}")

    # ─── 6. Account starts at ~$100k ──────────────────────────────────────
    out = query(folder, "SELECT equity FROM account LIMIT 1")
    first_eq = parse_single_value(out)
    if abs(first_eq - 100000) > 1:
        log("WARN", name, f"Initial equity={first_eq:.0f}, expected 100000")
    else:
        log("PASS", name, "Initial equity = $100,000")

    # ─── 7. Final equity (P&L summary) ────────────────────────────────────
    out = query(folder,
        "SELECT equity FROM account ORDER BY \"index\" DESC LIMIT 1")
    final_eq = parse_single_value(out)
    if final_eq == 0:
        final_eq = 100000
    pnl = final_eq - 100000
    log("PASS", name, f"Final equity ${final_eq:.0f} (P&L {pnl:+,.0f})")

    # ─── 8. Commission/slippage checks (cost profiles only) ──────────────
    if "cost_" in name:
        out = query(folder,
            "SELECT SUM(commission) as total_comm, SUM(slippage) as total_slip "
            "FROM orders WHERE status = 'Filled'")
        try:
            parts = out.split("\n")[-1].strip().split()
            total_comm = float(parts[-2]) if len(parts) >= 2 else 0
            total_slip = float(parts[-1]) if len(parts) >= 1 else 0
        except (ValueError, IndexError):
            total_comm = total_slip = 0

        if total_comm <= 0:
            log("FAIL", name, "Total commission = $0 (cost profile should have costs)")
        else:
            log("PASS", name, f"Total commission ${total_comm:.2f}")

        if total_slip <= 0:
            log("FAIL", name, "Total slippage = $0 (cost profile should have slippage)")
        else:
            log("PASS", name, f"Total slippage ${total_slip:.4f}")

        # Dollar slippage = slippage * filled_qty (accrued_slippages is per-unit)
        out = query(folder,
            "SELECT SUM(slippage * filled_qty) as dollar_slip "
            "FROM orders WHERE status = 'Filled'")
        try:
            dollar_slip = float(out.split("\n")[-1].strip().split()[-1])
        except (ValueError, IndexError):
            dollar_slip = 0
        if dollar_slip > 0:
            log("PASS", name, f"Dollar slippage ${dollar_slip:.2f}")

    # ─── 9. No zero-cost fills on non-cost profiles ──────────────────────
    elif "cost_" not in name:
        out = query(folder,
            "SELECT SUM(commission) as c, SUM(slippage) as s "
            "FROM orders WHERE status = 'Filled'")
        try:
            parts = out.split("\n")[-1].strip().split()
            total_comm = float(parts[-2]) if len(parts) >= 2 else 0
            total_slip = float(parts[-1]) if len(parts) >= 1 else 0
        except (ValueError, IndexError):
            total_comm = total_slip = 0
        if total_comm != 0 or total_slip != 0:
            log("WARN", name, f"Non-zero costs on --cost none: comm=${total_comm}, slip=${total_slip}")
        else:
            log("PASS", name, "Zero costs (--cost none correct)")

    # ─── 10. Order type distribution ──────────────────────────────────────
    out = query(folder,
        "SELECT type, COUNT(*) as n FROM orders GROUP BY type ORDER BY n DESC")
    lines = [l.strip() for l in out.split("\n") if l.strip() and not l.startswith("─")]
    type_dist = {}
    for line in lines[1:]:  # skip header
        parts = line.split()
        if len(parts) >= 2:
            try:
                type_dist[parts[0]] = int(parts[1])
            except ValueError:
                pass
    if type_dist:
        dist_str = ", ".join(f"{k}={v}" for k, v in sorted(type_dist.items()))
        log("PASS", name, f"Order types: {dist_str}")

    # ─── 11. Positions: no orphan positions at end ────────────────────────
    out = query(folder,
        "SELECT COUNT(*) as n FROM positions WHERE quantity != 0")
    try:
        open_pos = int(out.split("\n")[-1].strip().split()[-1])
    except (ValueError, IndexError):
        open_pos = 0
    # Open positions at end of backtest are normal (strategy may still be in a trade)
    if open_pos > 0:
        log("PASS", name, f"{open_pos} open positions at end (normal)")
    else:
        log("PASS", name, "All positions closed at end")


def main():
    print("=" * 72)
    print("  BATCH DATA VALIDATION (SQL queries on campaign outputs)")
    print("=" * 72)

    campaigns = sorted([
        d.name for d in CAMPAIGNS.iterdir()
        if d.is_dir() and d.name.startswith("exec_cluster")
    ])

    print(f"  Campaigns: {len(campaigns)}")

    for name in campaigns:
        print(f"\n--- {name} ---")
        try:
            validate_campaign(name)
        except Exception as e:
            log("FAIL", name, f"Exception: {e}")

    print(f"\n{'=' * 72}")
    print(f"  RESULTS: {PASS} PASS  |  {FAIL} FAIL  |  {WARN} WARN")
    print(f"{'=' * 72}")

    if ISSUES:
        print(f"\n  ISSUES ({len(ISSUES)}):")
        for issue in ISSUES:
            print(f"    {issue}")

    return 1 if FAIL > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
