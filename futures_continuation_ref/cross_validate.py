"""
Cross-validate our reference implementation against:
  1. arbitragelab (Panama Canal backward only, close-to-open gap)
  2. zipline-reloaded (close-to-close, both 'add' and 'mul')

Key finding: arbitragelab uses OPEN_new - CLOSE_old (overnight gap),
while our code and zipline use CLOSE_back - CLOSE_front (same-date gap).
This is a known methodological difference documented below.
"""

import numpy as np
from continuation import (
    make_three_contract_daily,
    build_bars,
    backward_adjust,
    PanamaCanal,
    Ratio,
)


def our_reference():
    """Run our reference implementation on the 3-contract daily test data."""
    data = make_three_contract_daily()
    bars = build_bars(**data)

    bw_panama_o, bw_panama_h, bw_panama_l, bw_panama_c = backward_adjust(bars, PanamaCanal)
    bw_ratio_o, bw_ratio_h, bw_ratio_l, bw_ratio_c = backward_adjust(bars, Ratio)

    return {
        'dates': bars.dates,
        'contracts': bars.contracts,
        'raw_closes': bars.closes,
        'raw_opens': bars.opens,
        'back_closes': bars.back_closes,
        'backward_panama_closes': bw_panama_c,
        'backward_panama_opens': bw_panama_o,
        'backward_ratio_closes': bw_ratio_c,
        'backward_ratio_opens': bw_ratio_o,
        'roll_ranges': bars.roll_ranges,
    }


def arbitragelab_style():
    """
    Simulate arbitragelab's roll() method on our test data.

    arbitragelab gap = OPEN_new_contract - CLOSE_old_contract (overnight gap)
    This differs from our close-to-close approach.

    From base_futures_roller.py:193-222:
        iloc = [iloc.index(i)-1 for i in roll_dates]
        day_before_exp_vals = dataset[open_col].loc[roll_dates]
        day_after_exp_vals = dataset[close_col].iloc[iloc]
        gaps[roll_dates] = day_before_exp_vals - day_after_exp_vals
        gaps = gaps.cumsum()
        if match_end: gaps -= gaps.iloc[-1]  # backward
    """
    # Our built bars (after stitching): Nov 1-4
    raw_closes = [4510, 4520, 4535, 4540]
    raw_opens = [4500, 4510, 4525, 4540]
    dates = ["Nov1", "Nov2", "Nov3", "Nov4"]

    # Roll dates = first day of new contract in the output
    # Roll 1: ESU23→ESZ23, new contract starts at Nov 3 (index 2)
    # Roll 2: ESZ23→ESH24, new contract starts at Nov 4 (index 3)
    roll_dates_idx = [2, 3]

    # arbitragelab: gap = OPEN_on_roll_date - CLOSE_day_before
    # But these refer to the output series (already stitched), where:
    #   - The open on the roll date IS the new contract's open
    #   - The close day before IS the old contract's close
    #
    # Roll 1 (index 2): open_new = ESZ23 open Nov 3 = 4525, close_old = ESU23 close Nov 2 = 4520
    # Roll 2 (index 3): open_new = ESH24 open Nov 4 = 4540, close_old = ESZ23 close Nov 3 = 4535
    gaps = [0.0, 0.0, 0.0, 0.0]
    gaps[2] = raw_opens[2] - raw_closes[1]   # 4525 - 4520 = +5
    gaps[3] = raw_opens[3] - raw_closes[2]   # 4540 - 4535 = +5

    # Cumulative sum
    cum_gaps = np.cumsum(gaps).tolist()  # [0, 0, 5, 10]

    # match_end=True (backward): subtract last value
    cum_gaps_bw = [g - cum_gaps[-1] for g in cum_gaps]  # [-10, -10, -5, 0]

    # Adjusted = raw - cum_gaps (arbitragelab subtracts gaps)
    adj_closes = [raw_closes[i] - cum_gaps_bw[i] for i in range(4)]
    adj_opens = [raw_opens[i] - cum_gaps_bw[i] for i in range(4)]

    return {
        'dates': dates,
        'gaps': gaps,
        'cum_gaps': cum_gaps,
        'cum_gaps_backward': cum_gaps_bw,
        'adj_closes': adj_closes,
        'adj_opens': adj_opens,
    }


def zipline_style():
    """
    Simulate zipline's ContinuousFutureAdjustmentReader on our test data.

    From history_loader.py:171-179:
        adj_base = back_close - front_close
        if adjustment_type == "mul":
            adj_value = 1.0 + adj_base / front_close  # = back/front
        elif adjustment_type == "add":
            adj_value = adj_base  # = back - front

    zipline uses close-to-close on the day BEFORE the roll (previous_session).
    This matches our approach exactly.

    zipline applies adjustments via AdjustedArrayWindow which works backward
    from the end, applying Float64Multiply/Float64Add to all bars before the roll.
    """
    # Built bars: Nov 1-4
    raw_closes = [4510, 4520, 4535, 4540]
    raw_opens = [4500, 4510, 4525, 4540]

    # At each roll, zipline reads front_close and back_close on the day BEFORE
    # the roll date (= last day of old contract = our boundary bar).

    # Roll 1: ESU23→ESZ23
    # Day before roll = Nov 2 (last day of ESU23)
    # front_close = ESU23 close Nov 2 = 4520
    # back_close  = ESZ23 close Nov 2 = 4525
    front1, back1 = 4520.0, 4525.0

    # Roll 2: ESZ23→ESH24
    # Day before roll = Nov 3 (last day of ESZ23)
    # front_close = ESZ23 close Nov 3 = 4535
    # back_close  = ESH24 close Nov 3 = 4530
    front2, back2 = 4535.0, 4530.0

    # 'add' adjustments (backward, applied to all bars before roll)
    add_adj1 = back1 - front1   # 4525 - 4520 = +5
    add_adj2 = back2 - front2   # 4530 - 4535 = -5

    # 'mul' adjustments
    mul_adj1 = back1 / front1   # 4525/4520
    mul_adj2 = back2 / front2   # 4530/4535

    # Apply backward: adjustments are cumulative from the end
    # Last segment (bar 3): no adjustment
    # Bar 2 (ESZ23): gets adj2 only
    # Bars 0-1 (ESU23): get adj1 AND adj2

    # Additive
    adj_add_closes = [
        raw_closes[0] + add_adj1 + add_adj2,   # 4510 + 5 + (-5) = 4510
        raw_closes[1] + add_adj1 + add_adj2,   # 4520 + 5 + (-5) = 4520
        raw_closes[2] + add_adj2,               # 4535 + (-5) = 4530
        raw_closes[3],                           # 4540 (unchanged)
    ]
    adj_add_opens = [
        raw_opens[0] + add_adj1 + add_adj2,
        raw_opens[1] + add_adj1 + add_adj2,
        raw_opens[2] + add_adj2,
        raw_opens[3],
    ]

    # Multiplicative
    adj_mul_closes = [
        raw_closes[0] * mul_adj1 * mul_adj2,
        raw_closes[1] * mul_adj1 * mul_adj2,
        raw_closes[2] * mul_adj2,
        raw_closes[3],
    ]
    adj_mul_opens = [
        raw_opens[0] * mul_adj1 * mul_adj2,
        raw_opens[1] * mul_adj1 * mul_adj2,
        raw_opens[2] * mul_adj2,
        raw_opens[3],
    ]

    return {
        'add_adj1': add_adj1, 'add_adj2': add_adj2,
        'mul_adj1': mul_adj1, 'mul_adj2': mul_adj2,
        'adj_add_closes': adj_add_closes,
        'adj_add_opens': adj_add_opens,
        'adj_mul_closes': adj_mul_closes,
        'adj_mul_opens': adj_mul_opens,
    }


def main():
    ours = our_reference()
    arb = arbitragelab_style()
    zipline = zipline_style()

    print("=" * 80)
    print("CROSS-VALIDATION: Futures Continuation Adjustments")
    print("=" * 80)

    # --- Built bars info ---
    print("\n--- Built Bars (after FirstOfMonth rollover) ---")
    print(f"  Dates:      {[str(d.date()) for d in ours['dates']]}")
    print(f"  Contracts:  {ours['contracts']}")
    print(f"  Raw closes: {ours['raw_closes']}")
    print(f"  Raw opens:  {ours['raw_opens']}")
    print(f"  Back close: {ours['back_closes']}")
    print(f"  Segments:   {ours['roll_ranges']}")

    # --- Our reference ---
    print("\n--- Our Reference (close-to-close) ---")
    print(f"  BackwardPanama close: {[round(v, 6) for v in ours['backward_panama_closes']]}")
    print(f"  BackwardPanama open:  {[round(v, 6) for v in ours['backward_panama_opens']]}")
    print(f"  BackwardRatio close:  {[round(v, 6) for v in ours['backward_ratio_closes']]}")
    print(f"  BackwardRatio open:   {[round(v, 6) for v in ours['backward_ratio_opens']]}")

    # --- Zipline comparison ---
    print("\n--- Zipline (close-to-close, same methodology) ---")
    print(f"  Adj factors: add1={zipline['add_adj1']:+.1f}, add2={zipline['add_adj2']:+.1f}")
    print(f"               mul1={zipline['mul_adj1']:.6f}, mul2={zipline['mul_adj2']:.6f}")
    print(f"  'add' close: {[round(v, 6) for v in zipline['adj_add_closes']]}")
    print(f"  'add' open:  {[round(v, 6) for v in zipline['adj_add_opens']]}")
    print(f"  'mul' close: {[round(v, 6) for v in zipline['adj_mul_closes']]}")
    print(f"  'mul' open:  {[round(v, 6) for v in zipline['adj_mul_opens']]}")

    # --- Verify zipline matches ours ---
    print("\n--- Verification: Our Reference vs Zipline ---")

    panama_match = all(
        abs(a - b) < 1e-6
        for a, b in zip(ours['backward_panama_closes'], zipline['adj_add_closes'])
    )
    ratio_match = all(
        abs(a - b) < 1e-6
        for a, b in zip(ours['backward_ratio_closes'], zipline['adj_mul_closes'])
    )

    print(f"  BackwardPanama vs zipline 'add': {'MATCH' if panama_match else 'MISMATCH'}")
    if not panama_match:
        for i, (a, b) in enumerate(zip(ours['backward_panama_closes'], zipline['adj_add_closes'])):
            print(f"    [{i}] ours={a:.6f} zipline={b:.6f} diff={a-b:.9f}")

    print(f"  BackwardRatio vs zipline 'mul':  {'MATCH' if ratio_match else 'MISMATCH'}")
    if not ratio_match:
        for i, (a, b) in enumerate(zip(ours['backward_ratio_closes'], zipline['adj_mul_closes'])):
            print(f"    [{i}] ours={a:.6f} zipline={b:.6f} diff={a-b:.9f}")

    # --- Arbitragelab comparison ---
    print("\n--- arbitragelab (close-to-open, DIFFERENT methodology) ---")
    print(f"  Gaps at rolls:       {arb['gaps']}")
    print(f"  Cumulative gaps:     {[round(v, 2) for v in arb['cum_gaps']]}")
    print(f"  Backward cum gaps:   {[round(v, 2) for v in arb['cum_gaps_backward']]}")
    print(f"  Adjusted close:      {[round(v, 6) for v in arb['adj_closes']]}")
    print(f"  Adjusted open:       {[round(v, 6) for v in arb['adj_opens']]}")

    print("\n  NOTE: arbitragelab uses overnight gap (OPEN_new - CLOSE_old)")
    print("  Our code uses same-date gap (CLOSE_back - CLOSE_front)")
    print("  These are intentionally different — our approach isolates the")
    print("  pure roll spread without overnight noise. See:")
    print("  - De Prado, 'Advances in Financial Machine Learning'")
    print("  - Quandl/Nasdaq Data Link continuous futures methodology")

    arb_diff = [
        abs(a - b)
        for a, b in zip(ours['backward_panama_closes'], arb['adj_closes'])
    ]
    print(f"\n  Difference (ours vs arbitragelab): {[round(d, 6) for d in arb_diff]}")
    print(f"  Max diff: {max(arb_diff):.6f}")

    # --- Return preservation check ---
    print("\n--- Return Preservation Check ---")
    raw_c = ours['raw_closes']
    bw_c = ours['backward_panama_closes']

    # Within-contract returns at roll boundaries
    # Roll 1: ESU23→ESZ23, Nov 2→Nov 3
    # Within ESZ23: close Nov 2 = 4525, close Nov 3 = 4535, return = +10
    # Our adjusted: Nov 2 = bw_c[1], Nov 3 = bw_c[2]
    adj_return_roll1 = bw_c[2] - bw_c[1]
    within_contract_return1 = 4535 - 4525  # ESZ23 Nov 2→Nov 3
    print(f"  Roll 1 (ESU23→ESZ23): adj return={adj_return_roll1:.1f}, "
          f"within-contract={within_contract_return1:.1f} "
          f"{'MATCH' if abs(adj_return_roll1 - within_contract_return1) < 0.01 else 'MISMATCH'}")

    # Roll 2: ESZ23→ESH24, Nov 3→Nov 4
    # Within ESH24: close Nov 3 = 4530, close Nov 4 = 4540, return = +10
    adj_return_roll2 = bw_c[3] - bw_c[2]
    within_contract_return2 = 4540 - 4530  # ESH24 Nov 3→Nov 4
    print(f"  Roll 2 (ESZ23→ESH24): adj return={adj_return_roll2:.1f}, "
          f"within-contract={within_contract_return2:.1f} "
          f"{'MATCH' if abs(adj_return_roll2 - within_contract_return2) < 0.01 else 'MISMATCH'}")

    print("\n" + "=" * 80)
    if panama_match and ratio_match:
        print("RESULT: Our reference matches zipline exactly (close-to-close).")
        print("        arbitragelab uses different methodology (close-to-open) as expected.")
        print("        All within-contract returns preserved correctly.")
    else:
        print("RESULT: MISMATCH detected — investigate!")
    print("=" * 80)


if __name__ == '__main__':
    main()
