"""
Compute correct expected values for all C++ unit tests.

Runs the reference implementation on all test datasets (daily, 5Min, 1Min)
for all 4 adjustment methods and prints values in C++ paste-ready format.
"""

from continuation import (
    make_three_contract_daily,
    make_three_contract_5min,
    make_three_contract_1min,
    build_bars,
    build_bars_intraday,
    backward_adjust,
    forward_adjust,
    PanamaCanal,
    Ratio,
)


def fmt(v, decimals=2):
    """Format a value for C++ output."""
    return f"{v:.{decimals}f}"


def print_cpp_checks(prefix, values, var="c", tolerance="0.01", decimals=2):
    """Print CHECK_THAT lines for C++ test."""
    for i, v in enumerate(values):
        print(f'    CHECK_THAT(result["cont1#{var}"].iloc({i}).as_double(), '
              f'WithinAbs({fmt(v, decimals)}, {tolerance}));')


def print_cpp_ratio_checks(prefix, raw_values, accumulated_ratio, var="c", tolerance="0.1"):
    """Print CHECK_THAT lines for ratio-adjusted values."""
    for i, raw in enumerate(raw_values):
        adjusted = raw * accumulated_ratio
        print(f'    CHECK_THAT(result["cont1#{var}"].iloc({i}).as_double(),')
        print(f'               WithinAbs({raw:.1f} * ratioFactor, {tolerance}));')


def section(title):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def subsection(title):
    print(f"\n  --- {title} ---")


def main():
    # ====================================================================
    # Daily 3-contract
    # ====================================================================
    section("DAILY 3-CONTRACT")

    data = make_three_contract_daily()
    bars = build_bars(**data)

    print(f"\n  Built bars: {len(bars.closes)} rows")
    print(f"  Contracts:  {bars.contracts}")
    print(f"  Segments:   {bars.roll_ranges}")
    print(f"  Raw closes: {bars.closes}")
    print(f"  Raw opens:  {bars.opens}")
    print(f"  Back close: {bars.back_closes}")

    # BackwardPanama
    bwp_o, bwp_h, bwp_l, bwp_c = backward_adjust(bars, PanamaCanal)
    subsection("BackwardPanama")
    print(f"  Close: {[round(v, 2) for v in bwp_c]}")
    print(f"  Open:  {[round(v, 2) for v in bwp_o]}")
    print(f"  High:  {[round(v, 2) for v in bwp_h]}")
    print(f"  Low:   {[round(v, 2) for v in bwp_l]}")

    # Trace the factors
    print(f"\n  Factor computation (backward, PanamaCanal):")
    print(f"    Segment 2 [3,1): ESH24 — UNCHANGED (last segment)")
    print(f"    Segment 1 [2,1): boundary=end-1=2")
    print(f"      closeFront[2]={bars.closes[2]}, closeBack[2]={bars.back_closes[2]}")
    print(f"      factor = {bars.back_closes[2]} - {bars.closes[2]} = {bars.back_closes[2] - bars.closes[2]}")
    print(f"      accumulated = {bars.back_closes[2] - bars.closes[2]}")
    print(f"    Segment 0 [0,2): boundary=end-1=1")
    print(f"      closeFront[1]={bars.closes[1]}, closeBack[1]={bars.back_closes[1]}")
    print(f"      factor = {bars.back_closes[1]} - {bars.closes[1]} = {bars.back_closes[1] - bars.closes[1]}")
    acc = (bars.back_closes[2] - bars.closes[2]) + (bars.back_closes[1] - bars.closes[1])
    print(f"      accumulated = {acc}")

    print("\n  C++ expected values:")
    print('  SECTION("Adjusted close values") {')
    print_cpp_checks("    ", bwp_c, "c")
    print("  }")
    print('  SECTION("Adjusted open values") {')
    print_cpp_checks("    ", bwp_o, "o")
    print("  }")

    # BackwardRatio
    bwr_o, bwr_h, bwr_l, bwr_c = backward_adjust(bars, Ratio)
    subsection("BackwardRatio")

    # Compute the cumulative ratio factors
    # Segment 1: ratio = back[2]/front[2] = 4530/4535
    ratio1 = bars.back_closes[2] / bars.closes[2]
    # Segment 0: ratio = back[1]/front[1] = 4525/4520, cumulative = ratio1 * ratio0
    ratio0 = bars.back_closes[1] / bars.closes[1]
    cum_ratio_seg0 = ratio1 * ratio0
    cum_ratio_seg1 = ratio1

    print(f"  Ratio at seg1 boundary: {bars.back_closes[2]}/{bars.closes[2]} = {ratio1:.9f}")
    print(f"  Ratio at seg0 boundary: {bars.back_closes[1]}/{bars.closes[1]} = {ratio0:.9f}")
    print(f"  Cumulative for seg0: {cum_ratio_seg0:.9f}")
    print(f"  Cumulative for seg1: {cum_ratio_seg1:.9f}")
    print(f"  Close: {[round(v, 6) for v in bwr_c]}")
    print(f"  Open:  {[round(v, 6) for v in bwr_o]}")

    # ForwardPanama
    fwp_o, fwp_h, fwp_l, fwp_c = forward_adjust(bars, PanamaCanal)
    subsection("ForwardPanama")
    print(f"  Close: {[round(v, 2) for v in fwp_c]}")
    print(f"  Open:  {[round(v, 2) for v in fwp_o]}")

    print(f"\n  Factor computation (forward, PanamaCanal):")
    print(f"    Segment 0 [0,2): ESU23 — UNCHANGED (first segment)")
    print(f"    Segment 1 [2,1): boundary=start-1=1")
    print(f"      closeFront[1]={bars.closes[1]}, closeBack[1]={bars.back_closes[1]}")
    fwd_f1 = bars.back_closes[1] - bars.closes[1]
    print(f"      factor = {fwd_f1}, accumulated = {fwd_f1}")
    print(f"    Segment 2 [3,1): boundary=start-1=2")
    print(f"      closeFront[2]={bars.closes[2]}, closeBack[2]={bars.back_closes[2]}")
    fwd_f2 = bars.back_closes[2] - bars.closes[2]
    fwd_acc2 = fwd_f1 + fwd_f2
    print(f"      factor = {fwd_f2}, accumulated = {fwd_acc2}")

    print("\n  C++ expected values:")
    print('  SECTION("Adjusted close values") {')
    print_cpp_checks("    ", fwp_c, "c")
    print("  }")
    print('  SECTION("Adjusted open values") {')
    print_cpp_checks("    ", fwp_o, "o")
    print("  }")

    # ForwardRatio
    fwr_o, fwr_h, fwr_l, fwr_c = forward_adjust(bars, Ratio)
    subsection("ForwardRatio")
    fwd_r1 = bars.back_closes[1] / bars.closes[1]
    fwd_r2 = bars.back_closes[2] / bars.closes[2]
    print(f"  Ratio at seg1 boundary: {fwd_r1:.9f}")
    print(f"  Ratio at seg2 boundary: {fwd_r2:.9f}")
    print(f"  Cumulative for seg1: {fwd_r1:.9f}")
    print(f"  Cumulative for seg2: {fwd_r1 * fwd_r2:.9f}")
    print(f"  Close: {[round(v, 6) for v in fwr_c]}")
    print(f"  Open:  {[round(v, 6) for v in fwr_o]}")

    print("\n  C++ expected values:")
    print('  SECTION("Adjusted close values") {')
    print_cpp_checks("    ", fwr_c, "c", "0.1", 6)
    print("  }")
    print('  SECTION("Adjusted open values") {')
    print_cpp_checks("    ", fwr_o, "o", "0.1", 6)
    print("  }")

    # ====================================================================
    # 5Min 3-contract
    # ====================================================================
    section("5Min 3-CONTRACT")

    data5 = make_three_contract_5min()
    bars5 = build_bars_intraday(**data5)

    print(f"\n  Built bars: {len(bars5.closes)} rows")
    print(f"  Contracts:  {bars5.contracts}")
    print(f"  Segments:   {bars5.roll_ranges}")
    print(f"  Raw closes: {bars5.closes}")
    print(f"  Back close: {bars5.back_closes}")

    # 5Min BackwardPanama
    bwp5_o, bwp5_h, bwp5_l, bwp5_c = backward_adjust(bars5, PanamaCanal)
    subsection("5Min BackwardPanama")
    print(f"  Close: {[round(v, 2) for v in bwp5_c]}")
    print(f"  Open:  {[round(v, 2) for v in bwp5_o]}")

    # Trace factors
    seg1_start, seg1_len = bars5.roll_ranges[1]
    seg1_end = seg1_start + seg1_len
    seg0_start, seg0_len = bars5.roll_ranges[0]
    seg0_end = seg0_start + seg0_len
    print(f"\n  Factors:")
    print(f"    Seg1 boundary={seg1_end-1}: front={bars5.closes[seg1_end-1]}, back={bars5.back_closes[seg1_end-1]}")
    print(f"    Seg0 boundary={seg0_end-1}: front={bars5.closes[seg0_end-1]}, back={bars5.back_closes[seg0_end-1]}")

    print("\n  C++ expected values (close):")
    print('  SECTION("5Min BackwardPanama adjusted close values") {')
    print_cpp_checks("    ", bwp5_c, "c")
    print("  }")
    print('  SECTION("5Min BackwardPanama adjusted open values") {')
    # Only first 6 opens tested in current C++ test
    print_cpp_checks("    ", bwp5_o[:6], "o")
    print("  }")

    # 5Min BackwardRatio
    bwr5_o, bwr5_h, bwr5_l, bwr5_c = backward_adjust(bars5, Ratio)
    subsection("5Min BackwardRatio")

    r5_seg1 = bars5.back_closes[seg1_end-1] / bars5.closes[seg1_end-1]
    r5_seg0 = bars5.back_closes[seg0_end-1] / bars5.closes[seg0_end-1]
    cum_r5_seg1 = r5_seg1
    cum_r5_seg0 = r5_seg1 * r5_seg0

    print(f"  Ratio seg1: {bars5.back_closes[seg1_end-1]}/{bars5.closes[seg1_end-1]} = {r5_seg1:.9f}")
    print(f"  Ratio seg0: {bars5.back_closes[seg0_end-1]}/{bars5.closes[seg0_end-1]} = {r5_seg0:.9f}")
    print(f"  Cumulative seg0: {cum_r5_seg0:.9f}")
    print(f"  Cumulative seg1: {cum_r5_seg1:.9f}")
    print(f"  Close: {[round(v, 6) for v in bwr5_c]}")

    print("\n  C++ expected values:")
    print(f"    const double ratioFactor = {bars5.back_closes[seg1_end-1]:.1f} / {bars5.closes[seg1_end-1]:.1f};")
    print(f"    // BUT segment 0 has DIFFERENT cumulative ratio!")
    print(f"    const double ratioSeg0 = ({bars5.back_closes[seg1_end-1]:.1f} / {bars5.closes[seg1_end-1]:.1f}) * ({bars5.back_closes[seg0_end-1]:.1f} / {bars5.closes[seg0_end-1]:.1f});")
    print(f"    // ratioFactor (seg1) = {cum_r5_seg1:.9f}")
    print(f"    // ratioSeg0          = {cum_r5_seg0:.9f}")

    # 5Min ForwardPanama
    fwp5_o, fwp5_h, fwp5_l, fwp5_c = forward_adjust(bars5, PanamaCanal)
    subsection("5Min ForwardPanama")
    print(f"  Close: {[round(v, 2) for v in fwp5_c]}")
    print(f"  Open:  {[round(v, 2) for v in fwp5_o]}")
    print("\n  C++ expected values:")
    print('  SECTION("5Min ForwardPanama adjusted close values") {')
    print_cpp_checks("    ", fwp5_c, "c")
    print("  }")

    # 5Min ForwardRatio
    fwr5_o, fwr5_h, fwr5_l, fwr5_c = forward_adjust(bars5, Ratio)
    subsection("5Min ForwardRatio")
    print(f"  Close: {[round(v, 6) for v in fwr5_c]}")
    print("\n  C++ expected values:")
    print('  SECTION("5Min ForwardRatio adjusted close values") {')
    print_cpp_checks("    ", fwr5_c, "c", "0.1", 6)
    print("  }")

    # ====================================================================
    # 1Min 3-contract
    # ====================================================================
    section("1Min 3-CONTRACT")

    data1 = make_three_contract_1min()
    bars1 = build_bars_intraday(**data1)

    print(f"\n  Built bars: {len(bars1.closes)} rows")
    print(f"  Contracts:  {bars1.contracts}")
    print(f"  Segments:   {bars1.roll_ranges}")
    print(f"  Raw closes: {bars1.closes}")
    print(f"  Back close: {bars1.back_closes}")

    # 1Min BackwardPanama
    bwp1_o, bwp1_h, bwp1_l, bwp1_c = backward_adjust(bars1, PanamaCanal)
    subsection("1Min BackwardPanama")
    print(f"  Close: {[round(v, 2) for v in bwp1_c]}")

    seg1_start_1m, seg1_len_1m = bars1.roll_ranges[1]
    seg1_end_1m = seg1_start_1m + seg1_len_1m
    seg0_start_1m, seg0_len_1m = bars1.roll_ranges[0]
    seg0_end_1m = seg0_start_1m + seg0_len_1m
    print(f"\n  Factors:")
    print(f"    Seg1 boundary={seg1_end_1m-1}: front={bars1.closes[seg1_end_1m-1]}, back={bars1.back_closes[seg1_end_1m-1]}")
    print(f"    Seg0 boundary={seg0_end_1m-1}: front={bars1.closes[seg0_end_1m-1]}, back={bars1.back_closes[seg0_end_1m-1]}")

    print("\n  C++ expected values:")
    print('  SECTION("1Min BackwardPanama adjusted close values") {')
    print_cpp_checks("    ", bwp1_c, "c")
    print("  }")

    # 1Min BackwardRatio
    bwr1_o, bwr1_h, bwr1_l, bwr1_c = backward_adjust(bars1, Ratio)
    subsection("1Min BackwardRatio")

    r1_seg1 = bars1.back_closes[seg1_end_1m-1] / bars1.closes[seg1_end_1m-1]
    r1_seg0 = bars1.back_closes[seg0_end_1m-1] / bars1.closes[seg0_end_1m-1]
    cum_r1_seg0 = r1_seg1 * r1_seg0

    print(f"  Ratio seg1: {r1_seg1:.9f}")
    print(f"  Ratio seg0: {cum_r1_seg0:.9f}")
    print(f"  Close: {[round(v, 6) for v in bwr1_c]}")

    print("\n  C++ expected values:")
    print(f"    const double ratioSeg1 = {bars1.back_closes[seg1_end_1m-1]:.1f} / {bars1.closes[seg1_end_1m-1]:.1f};")
    print(f"    const double ratioSeg0 = ratioSeg1 * ({bars1.back_closes[seg0_end_1m-1]:.1f} / {bars1.closes[seg0_end_1m-1]:.1f});")

    # 1Min ForwardPanama
    fwp1_o, fwp1_h, fwp1_l, fwp1_c = forward_adjust(bars1, PanamaCanal)
    subsection("1Min ForwardPanama")
    print(f"  Close: {[round(v, 2) for v in fwp1_c]}")

    # 1Min ForwardRatio
    fwr1_o, fwr1_h, fwr1_l, fwr1_c = forward_adjust(bars1, Ratio)
    subsection("1Min ForwardRatio")
    print(f"  Close: {[round(v, 6) for v in fwr1_c]}")

    # ====================================================================
    # Summary of what changed vs old test expectations
    # ====================================================================
    section("SUMMARY: Old vs New Expected Values")
    print("""
  Daily BackwardPanama:
    OLD test: close = [4505, 4515, 4535, 4540]  (seg0 adj by -5, seg1 unchanged)
    NEW corr: close = [4510, 4520, 4530, 4540]  (seg0 unchanged, seg1 adj by -5)
    OLD test: open  = [4495, 4505, 4525, 4540]
    NEW corr: open  = [4500, 4510, 4520, 4540]

  5Min BackwardPanama:
    OLD test: close = [4500, 4505, 4510, 4515, 4532, 4535, 4537, 4540]
    NEW corr: close = [4505, 4510, 4515, 4520, 4527, 4530, 4537, 4540]
    OLD test: open  = [4495, 4500, 4505, 4510, 4525, 4532]
    NEW corr: open  = [4500, 4505, 4510, 4515, 4520, 4527]

  5Min BackwardRatio:
    OLD test: ratioFactor = 4530/4535 applied to seg0
    NEW corr: seg1 ratio = 4530/4535, seg0 ratio = (4530/4535)*(4525/4520)

  1Min BackwardPanama:
    OLD test: close = [4498, 4501, 4505, 4508, 4511, 4515, 4529, 4532, 4535, ...]
    NEW corr: close = [4503, 4506, 4510, 4513, 4516, 4520, 4524, 4527, 4530, ...]

  1Min BackwardRatio:
    OLD test: ratioFactor = 4530/4535 applied to seg0
    NEW corr: seg1 ratio = 4530/4535, seg0 ratio = (4530/4535)*(4525/4520)

  Root cause: Off-by-one in boundary bar selection (now fixed in backward.h/forward.h).
  The old code used 'end' (first bar of NEXT segment) instead of 'end-1' (last bar
  of CURRENT segment). This read the wrong contracts at the boundary.
""")


if __name__ == '__main__':
    main()
