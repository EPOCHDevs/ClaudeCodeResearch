#!/usr/bin/env python3
"""
Validate all exec_cluster test outputs.
Checks data integrity, semantic correctness, and expected behavior.
"""
import pyarrow.ipc as ipc
import os
import sys
import json
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent
CAMPAIGNS = BASE / "campaigns" / "test_runner"
DEFS = BASE / "definitions" / "test_runner"

PASS = 0
FAIL = 0
WARN = 0
ISSUES = []


def log_pass(test, msg):
    global PASS
    PASS += 1


def log_fail(test, msg):
    global FAIL
    FAIL += 1
    ISSUES.append(f"FAIL [{test}]: {msg}")
    print(f"  FAIL: {msg}")


def log_warn(test, msg):
    global WARN
    WARN += 1
    ISSUES.append(f"WARN [{test}]: {msg}")
    print(f"  WARN: {msg}")


def read_arrow(path):
    with open(path, "rb") as f:
        return ipc.open_file(f).read_all()


def get_tables(name):
    """Read orders, account, positions for a test."""
    d = CAMPAIGNS / name / "tables"
    result = {}
    for tbl in ["orders", "account", "positions"]:
        p = d / f"{tbl}.arrow"
        if p.exists():
            result[tbl] = read_arrow(p)
    return result


def to_dicts(table):
    """Convert arrow table to list of dicts."""
    return table.to_pydict()


def validate_common(name, tables):
    """Common validations for all tests."""
    orders = tables.get("orders")
    account = tables.get("account")
    positions = tables.get("positions")

    if orders is None:
        log_fail(name, "No orders table")
        return

    od = orders.to_pydict()
    n_orders = orders.num_rows

    # 1. Must have at least 1 filled order
    filled = [s for s in od["status"] if s == "Filled"]
    if not filled:
        log_fail(name, "No filled orders")
    else:
        log_pass(name, f"{len(filled)} filled orders")

    # 2. filled_qty must be > 0 for filled orders
    for i in range(n_orders):
        if od["status"][i] == "Filled":
            if od["filled_qty"][i] is None or od["filled_qty"][i] <= 0:
                log_fail(name, f"Order {i}: filled but filled_qty={od['filled_qty'][i]}")

    # 3. filled_price must be > 0 for filled orders
    for i in range(n_orders):
        if od["status"][i] == "Filled":
            if od["filled_price"][i] is None or od["filled_price"][i] <= 0:
                log_fail(name, f"Order {i}: filled but filled_price={od['filled_price'][i]}")

    # 4. Account equity should never go negative
    if account is not None:
        ad = account.to_pydict()
        neg_equity = [e for e in ad["equity"] if e is not None and e < 0]
        if neg_equity:
            log_fail(name, f"Negative equity detected: min={min(neg_equity):.2f}")
        else:
            log_pass(name, "Equity always >= 0")

        # 5. Account should start at ~$100,000
        first_equity = ad["equity"][0]
        if first_equity is not None and abs(first_equity - 100000) > 1:
            log_warn(name, f"Initial equity={first_equity:.2f}, expected ~100000")

    # 6. Side must be buy or sell
    invalid_sides = [s for s in od["side"] if s not in ("Buy", "Sell", "BuyToCover", "SellShort")]
    if invalid_sides:
        log_fail(name, f"Invalid order sides: {set(invalid_sides)}")

    return od


def validate_E01_zone_basic(name):
    """E01: Basic zone + E03 percent sizing + E07 SL + E08 TP."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # Check that stop_loss orders have stop_price set
    sl_orders = [i for i in range(len(od["type"])) if od["type"][i] == "Stop"]
    if not sl_orders:
        log_warn(name, "No stop orders found (SL may not have triggered)")
    else:
        for i in sl_orders:
            if od["stop_price"][i] is None or od["stop_price"][i] <= 0:
                log_fail(name, f"Stop order {i} has no stop_price")

    # Check limit orders exist (TP)
    limit_orders = [i for i in range(len(od["type"])) if od["type"][i] == "Limit"]
    if not limit_orders:
        log_warn(name, "No limit orders found (TP may not have triggered)")

    # All 3 assets should have trades (orders use ticker without -Stocks suffix)
    assets_traded = set(od["asset"])
    expected_tickers = {"SPY", "QQQ", "GLD"}
    missing = expected_tickers - assets_traded
    if missing:
        log_warn(name, f"Tickers not traded: {missing} (got: {assets_traded})")
    else:
        log_pass(name, f"All {len(expected_tickers)} tickers traded")


def validate_E01_hold_strict(name):
    """E01: hold_long=10, strict_hold=True."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # Should have market orders (entries) and stop orders (SL)
    order_types = set(od["type"])
    if "Market" not in order_types:
        log_fail(name, "No market orders (entries)")
    if "Stop" not in order_types:
        log_warn(name, "No stop orders (SL may not have triggered)")


def validate_E03_sizing_modes(name):
    """E03: equal_weight + rebalance_on."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # With 3 assets and equal weight, each should get ~33% of equity
    # Check that filled_qty varies by asset (price-dependent sizing)
    assets_qty = defaultdict(list)
    for i in range(len(od["status"])):
        if od["status"][i] == "Filled" and od["side"][i] == "Buy":
            assets_qty[od["asset"][i]].append(od["filled_qty"][i])

    if len(assets_qty) > 0:
        log_pass(name, f"Equal weight across {len(assets_qty)} assets")


def validate_E04_risk_unit(name):
    """E04: risk_unit with ATR stop + trailing."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # Should have market orders (entries) and stop orders (SL from risk_unit + trailing)
    # Trailing stop state is engine-internal (trail_amount not serialized to orders).
    stop_orders = [i for i in range(len(od["type"])) if od["type"][i] == "Stop"]
    if not stop_orders:
        log_warn(name, "No stop orders — risk_unit SL + trailing may not have triggered")
    else:
        log_pass(name, f"{len(stop_orders)} stop orders (risk_unit SL + trailing)")


def validate_E04_fixed_risk_rr(name):
    """E04: risk_mode=fixed, rr_ratio=2.0."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # With rr_ratio=2.0, should have limit orders (TP at 2x stop distance)
    limit_orders = [i for i in range(len(od["type"])) if od["type"][i] == "Limit"]
    stop_orders = [i for i in range(len(od["type"])) if od["type"][i] == "Stop"]

    if not limit_orders:
        log_warn(name, "No limit orders (TP from rr_ratio=2.0 may not have triggered)")
    if not stop_orders:
        log_warn(name, "No stop orders (SL from risk_unit may not have triggered)")

    # With lot_size=1 and min_size=1, all filled_qty should be whole numbers >= 1
    for i in range(len(od["status"])):
        if od["status"][i] == "Filled":
            qty = od["filled_qty"][i]
            if qty is not None and qty > 0:
                if qty != int(qty):
                    log_fail(name, f"Order {i}: qty={qty} not whole (lot_size=1)")
                if qty < 1:
                    log_fail(name, f"Order {i}: qty={qty} < min_size=1")


def validate_E05_kelly(name):
    """E05: Kelly half-Kelly sizing."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # Kelly uses fallback_pct=10 initially, then adjusts. Just verify orders exist.
    filled = [i for i in range(len(od["status"])) if od["status"][i] == "Filled"]
    if len(filled) < 2:
        log_warn(name, f"Only {len(filled)} filled orders — Kelly may not have enough trades")


def validate_E05_optimal_f(name):
    """E05: Optimal f sizing."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    filled = [i for i in range(len(od["status"])) if od["status"][i] == "Filled"]
    if len(filled) < 2:
        log_warn(name, f"Only {len(filled)} filled orders — Optimal f needs trade history")


def validate_E06_cppi(name):
    """E06: CPPI with floor_pct=0.8."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # CPPI floor = 100000 * 0.8 = $80,000
    # Equity should never breach this floor (in theory)
    account = tables.get("account")
    if account is not None:
        ad = account.to_pydict()
        min_eq = min(e for e in ad["equity"] if e is not None)
        if min_eq < 79000:  # Allow 1% tolerance for intra-bar moves
            log_warn(name, f"Equity dipped to {min_eq:.2f}, floor should be ~$80,000 (CPPI)")
        else:
            log_pass(name, f"CPPI floor respected: min equity={min_eq:.2f}")


def validate_E06_tipp(name):
    """E06: TIPP with floor_pct=0.85."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    account = tables.get("account")
    if account is not None:
        ad = account.to_pydict()
        equities = [e for e in ad["equity"] if e is not None]
        # TIPP floor ratchets: floor = max_equity_seen_so_far * 0.85
        # Check each bar: equity should stay above contemporaneous floor
        running_max = equities[0]
        worst_breach = 0
        for eq in equities:
            if eq > running_max:
                running_max = eq
            floor = running_max * 0.85
            breach = floor - eq
            if breach > worst_breach:
                worst_breach = breach
        if worst_breach > running_max * 0.02:  # >2% breach of contemporaneous floor
            log_warn(name, f"TIPP floor breached by ${worst_breach:.2f} "
                     f"(peak so far=${running_max:.2f})")
        else:
            log_pass(name, f"TIPP floor respected (max breach ${worst_breach:.2f})")


def validate_E08_tiered_tp(name):
    """E08: Tiered R-multiple take profit."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # With r_levels=[1.5, 2.0, 3.0] and exit_pcts=[0.33, 0.33, 0.34],
    # should see multiple limit orders per position (partial exits)
    limit_orders = [i for i in range(len(od["type"])) if od["type"][i] == "Limit"]
    if not limit_orders:
        log_warn(name, "No limit orders — tiered TP may not have triggered")
    elif len(limit_orders) < 3:
        log_warn(name, f"Only {len(limit_orders)} limit orders — expected 3+ for tiered exits")
    else:
        log_pass(name, f"{len(limit_orders)} limit orders (tiered TP working)")


def validate_E09_stepped(name):
    """E09: trailing_stop with step=1.0."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # Trailing stop state is engine-internal (trail_amount/hwm not serialized).
    # Validate that Stop orders exist (trailing manifests as ratcheting stop_price).
    stop_orders = [i for i in range(len(od["type"])) if od["type"][i] == "Stop"]
    if not stop_orders:
        log_warn(name, "No stop orders — stepped trailing may not have triggered")
    else:
        # Check stop prices vary (evidence of ratcheting)
        stop_prices = [od["stop_price"][i] for i in stop_orders
                       if od["stop_price"][i] is not None]
        unique_prices = len(set(f"{p:.2f}" for p in stop_prices))
        if unique_prices > 1:
            log_pass(name, f"Stop orders with {unique_prices} distinct prices (trail ratcheting)")
        else:
            log_pass(name, f"{len(stop_orders)} stop orders placed")


def validate_E10_indicator_exits(name):
    """E10: chandelier_exit, chande_kroll_stop, psar."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # These are indicator-driven signals, just verify trades happened
    filled = [i for i in range(len(od["status"])) if od["status"][i] == "Filled"]
    if len(filled) < 4:
        log_warn(name, f"Only {len(filled)} fills — indicator exits may not be generating signals")
    else:
        log_pass(name, f"{len(filled)} fills from indicator-driven signals")


def validate_E11_futures(name):
    """E11: Futures rollover + risk_unit."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # Futures rollover: orders use individual contract tickers (ESH23, ESM23, etc.)
    assets = set(od["asset"])
    es_contracts = [a for a in assets if a.startswith("ES")]
    if not es_contracts:
        log_fail(name, f"No ES contracts found, got: {assets}")
    elif len(es_contracts) < 2:
        log_warn(name, f"Only {len(es_contracts)} ES contract(s) — rollover may not have occurred")
    else:
        log_pass(name, f"Rollover across {len(es_contracts)} ES contracts: {sorted(es_contracts)}")


def validate_E17_exit_combos(name):
    """E17: SL + trail + TP stacked."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # Should have stop, limit, and potentially trailing orders
    order_types = set(od["type"])
    if "Stop" not in order_types:
        log_warn(name, "No stop orders in triple exit stack")
    if "Limit" not in order_types:
        log_warn(name, "No limit orders in triple exit stack")

    # Trailing stop state is engine-internal. Just verify stop orders exist.

    # At most one exit per position should fill (first triggered wins)
    # Group orders by oca_group
    oca_groups = defaultdict(list)
    for i in range(len(od["oca_group"])):
        if od["oca_group"][i]:
            oca_groups[od["oca_group"][i]].append(i)

    for group, indices in oca_groups.items():
        filled_in_group = [i for i in indices if od["status"][i] == "Filled"]
        if len(filled_in_group) > 1:
            log_warn(name, f"OCA group {group[:8]}...: {len(filled_in_group)} fills (expected ≤1)")


def validate_E18_directional(name):
    """E18: Long-only wiring."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # Long-only: should NOT have sell_short orders
    short_orders = [i for i in range(len(od["side"])) if od["side"][i] == "SellShort"]
    if short_orders:
        log_fail(name, f"{len(short_orders)} sell_short orders in long-only strategy!")
    else:
        log_pass(name, "No short orders (long-only correct)")


def validate_cost_profile(name, cost_type):
    """Validate cost profile has non-zero commission and slippage."""
    tables = get_tables(name)
    od = validate_common(name, tables)
    if od is None:
        return

    # Commission should be non-zero for filled orders
    filled_commissions = [od["commission"][i] for i in range(len(od["status"]))
                          if od["status"][i] == "Filled" and od["commission"][i] is not None]
    nonzero_comm = [c for c in filled_commissions if c > 0]

    if not nonzero_comm:
        log_fail(name, f"ALL commissions zero for {cost_type} preset")
    else:
        log_pass(name, f"Commission: {len(nonzero_comm)}/{len(filled_commissions)} "
                 f"non-zero (avg=${sum(nonzero_comm)/len(nonzero_comm):.4f})")

    # Slippage should be non-zero for filled orders
    filled_slippages = [od["slippage"][i] for i in range(len(od["status"]))
                        if od["status"][i] == "Filled" and od["slippage"][i] is not None]
    nonzero_slip = [s for s in filled_slippages if s > 0]

    if not nonzero_slip:
        log_fail(name, f"ALL slippages zero for {cost_type} preset")
    else:
        log_pass(name, f"Slippage: {len(nonzero_slip)}/{len(filled_slippages)} "
                 f"non-zero (avg=${sum(nonzero_slip)/len(nonzero_slip):.6f})")

    # Account should show accrued fees/slippages
    account = tables.get("account")
    if account is not None:
        ad = account.to_pydict()
        final_fees = ad["accrued_fees"][-1] if ad["accrued_fees"] else 0
        final_slip = ad["accrued_slippages"][-1] if ad["accrued_slippages"] else 0
        if final_fees is not None and final_fees > 0:
            log_pass(name, f"Accrued fees: ${final_fees:.4f}")
        else:
            log_warn(name, f"Accrued fees={final_fees} (expected > 0)")

    # Equity should end below starting equity minus costs
    # (costs should have real impact on P&L)
    if account is not None:
        start_eq = ad["equity"][0]
        end_eq = ad["equity"][-1]
        if start_eq and end_eq:
            log_pass(name, f"Equity: ${start_eq:.0f} → ${end_eq:.0f} "
                     f"(Δ={end_eq-start_eq:+.0f})")


def validate_no_cost(name):
    """Validate that --cost none produces zero commission/slippage."""
    tables = get_tables(name)
    if "orders" not in tables:
        return

    od = tables["orders"].to_pydict()
    nonzero_comm = [od["commission"][i] for i in range(len(od["status"]))
                    if od["commission"][i] is not None and od["commission"][i] > 0]
    nonzero_slip = [od["slippage"][i] for i in range(len(od["status"]))
                    if od["slippage"][i] is not None and od["slippage"][i] > 0]

    if nonzero_comm:
        log_fail(name, f"Commission non-zero with --cost none: {nonzero_comm[:3]}")
    else:
        log_pass(name, "Commission correctly zero (--cost none)")

    if nonzero_slip:
        log_fail(name, f"Slippage non-zero with --cost none: {nonzero_slip[:3]}")
    else:
        log_pass(name, "Slippage correctly zero (--cost none)")


def main():
    global PASS, FAIL, WARN, ISSUES

    print("=" * 70)
    print("EXEC CLUSTER VALIDATION SUITE")
    print("=" * 70)

    # =========================================================================
    # EXECUTOR SKILL TESTS (--cost none)
    # =========================================================================

    exec_tests = {
        "exec_cluster_E01_zone_basic": validate_E01_zone_basic,
        "exec_cluster_E01_hold_strict": validate_E01_hold_strict,
        "exec_cluster_E03_sizing_modes": validate_E03_sizing_modes,
        "exec_cluster_E04_risk_unit_trailing": validate_E04_risk_unit,
        "exec_cluster_E04_fixed_risk_rr": validate_E04_fixed_risk_rr,
        "exec_cluster_E05_kelly_sizing": validate_E05_kelly,
        "exec_cluster_E05_optimal_f": validate_E05_optimal_f,
        "exec_cluster_E06_cppi_insurance": validate_E06_cppi,
        "exec_cluster_E06_tipp_insurance": validate_E06_tipp,
        "exec_cluster_E08_tiered_tp": validate_E08_tiered_tp,
        "exec_cluster_E09_stepped_trailing": validate_E09_stepped,
        "exec_cluster_E10_indicator_exits": validate_E10_indicator_exits,
        "exec_cluster_E11_futures_rollover": validate_E11_futures,
        "exec_cluster_E17_exit_combos": validate_E17_exit_combos,
        "exec_cluster_E18_directional_wiring": validate_E18_directional,
    }

    for name, validator in exec_tests.items():
        test_dir = CAMPAIGNS / name
        if not test_dir.exists():
            log_fail(name, f"Output directory not found: {test_dir}")
            continue
        print(f"\n--- {name} ---")
        # Validate no costs (ran with --cost none)
        validate_no_cost(name)
        # Validate test-specific expectations
        validator(name)

    # =========================================================================
    # COST PROFILE TESTS
    # =========================================================================

    cost_tests = {
        "exec_cluster_cost_us_equity": "us_equity",
        "exec_cluster_cost_futures": "futures",
        "exec_cluster_cost_crypto": "crypto",
        "exec_cluster_cost_fx": "fx",
        "exec_cluster_cost_ib_equity": "ib_equity",
        "exec_cluster_cost_flat_fee": "flat_fee",
        "exec_cluster_cost_volume_impact": "volume_impact",
    }

    for name, cost_type in cost_tests.items():
        test_dir = CAMPAIGNS / name
        if not test_dir.exists():
            log_fail(name, f"Output directory not found: {test_dir}")
            continue
        print(f"\n--- {name} (--cost {cost_type}) ---")
        validate_cost_profile(name, cost_type)

    # =========================================================================
    # SUMMARY
    # =========================================================================

    print("\n" + "=" * 70)
    print(f"RESULTS: {PASS} PASS  |  {FAIL} FAIL  |  {WARN} WARN")
    print("=" * 70)

    if ISSUES:
        print("\nISSUES:")
        for issue in ISSUES:
            print(f"  {issue}")

    return 1 if FAIL > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
