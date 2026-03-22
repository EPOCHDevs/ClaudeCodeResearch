#!/usr/bin/env python3
"""
Validate lines_handbook tearsheet protobuf output against handbook specs.
Checks each of the 27 layouts for correct proto-level properties.
"""
import sys
sys.path.insert(0, '/home/adesola/EpochDev/EpochBackend/packages/epoch-protos/python')

from epoch_protos import tearsheet_pb2
from epoch_protos import chart_union_pb2
import epoch_protos.lines_chart_pb2 as lines_pb2
import epoch_protos.chart_base_pb2 as chart_base_pb2
from pathlib import Path

BASE = Path("project/research_studies/test_runner/lines_handbook/tearsheets")

def load_tearsheet(category):
    pb_path = BASE / category / "tearsheet.pb"
    ts = tearsheet_pb2.TearSheet()
    ts.ParseFromString(pb_path.read_bytes())
    return ts

def get_charts_by_category(ts):
    """Return dict: category_string -> (chart_def, numeric_lines_def)"""
    result = {}
    for chart in ts.charts.charts:
        if chart.HasField('numeric_lines_def'):
            nld = chart.numeric_lines_def
            cd = nld.chart_def
            result[cd.category] = (cd, nld)
    return result

def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    msg = f"  [{status}] {name}"
    if detail and not condition:
        msg += f" — {detail}"
    print(msg)
    return condition

def validate_all():
    """Validate cross-sectional charts (ALL tearsheet)."""
    ts = load_tearsheet("ALL")
    charts = get_charts_by_category(ts)
    passed = 0
    failed = 0

    # --- cs_lines L1: Per-Asset (3 series, no agg) ---
    print("\n=== cs_lines L1: Per-Asset ===")
    cat = "01 cs_lines L1: Per-Asset"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L1: Per-Asset Cumulative Return", f"got '{cd.title}'")
        r &= check("3 series (one per asset)", len(nld.lines) == 3, f"got {len(nld.lines)}")
        r &= check("no stack", nld.stack_type == 0, f"got {nld.stack_type}")
        r &= check("no area", nld.area == False)
        r &= check("no smooth", nld.smooth == False)
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- cs_lines L2: Aggregated (1 series) ---
    print("\n=== cs_lines L2: Aggregated ===")
    cat = "02 cs_lines L2: Aggregated"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L2: Mean Daily Return Across Assets", f"got '{cd.title}'")
        r &= check("1 series (aggregated)", len(nld.lines) == 1, f"got {len(nld.lines)}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- cs_lines L3: Filtered+Agg (1 series, median) ---
    print("\n=== cs_lines L3: Filtered+Agg ===")
    cat = "03 cs_lines L3: Filtered+Agg"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L3: Median (Max 2 Assets)", f"got '{cd.title}'")
        r &= check("1 series (aggregated)", len(nld.lines) == 1, f"got {len(nld.lines)}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- cs_lines L4: Colors (3 series) ---
    print("\n=== cs_lines L4: Colors ===")
    cat = "04 cs_lines L4: Colors"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L4: Per-Asset with Custom Colors", f"got '{cd.title}'")
        r &= check("3 series", len(nld.lines) == 3, f"got {len(nld.lines)}")
        # Check colors are set (non-default)
        colors_set = all(line.color != 0 for line in nld.lines)
        r &= check("colors assigned", colors_set)
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- cs_lines L5: Stacked Area (NormalStack) ---
    print("\n=== cs_lines L5: Stacked Area ===")
    cat = "05 cs_lines L5: Stacked Area"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L5: Stacked Area", f"got '{cd.title}'")
        r &= check("area=True", nld.area == True)
        # NormalStack = 1 in proto enum
        r &= check("stack_type=NormalStack", nld.stack_type == 1, f"got {nld.stack_type}")
        r &= check("3 series", len(nld.lines) == 3, f"got {len(nld.lines)}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- cs_lines L6: Percent Stack ---
    print("\n=== cs_lines L6: Percent Stack ===")
    cat = "06 cs_lines L6: Percent Stack"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L6: 100% Stacked Area", f"got '{cd.title}'")
        r &= check("area=True", nld.area == True)
        # PercentStack = 2 in proto enum
        r &= check("stack_type=PercentStack", nld.stack_type == 2, f"got {nld.stack_type}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- cs_lines L7: Reference Line ---
    print("\n=== cs_lines L7: Reference Line ===")
    cat = "07 cs_lines L7: Reference Line"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L7: Daily Return with Zero Reference", f"got '{cd.title}'")
        r &= check("has reference lines", len(nld.straight_lines) >= 1, f"got {len(nld.straight_lines)}")
        if nld.straight_lines:
            r &= check("ref line value=0", nld.straight_lines[0].value == 0.0, f"got {nld.straight_lines[0].value}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- cs_labeled_lines L1: Yield Curves ---
    print("\n=== cs_labeled_lines L1: Yield Curves ===")
    cat = "08 cs_labeled_lines L1: Yield Curves"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L1: SMA Profiles by Asset", f"got '{cd.title}'")
        r &= check("3 series (one per asset)", len(nld.lines) == 3, f"got {len(nld.lines)}")
        # Check data points exist
        if nld.lines:
            pts = len(nld.lines[0].data)
            r &= check("5 data points per series", pts == 5, f"got {pts}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- cs_labeled_lines L2: Factor Profiles ---
    print("\n=== cs_labeled_lines L2: Factor Profiles ===")
    cat = "09 cs_labeled_lines L2: Factor Profiles"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L2: Factor Profiles by Asset", f"got '{cd.title}'")
        r &= check("3 series", len(nld.lines) == 3, f"got {len(nld.lines)}")
        if nld.lines:
            pts = len(nld.lines[0].data)
            r &= check("4 data points per series", pts == 4, f"got {pts}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    return passed, failed


def validate_per_asset(asset="SPY-Stocks"):
    """Validate per-asset charts (xy_lines + labeled_lines)."""
    ts = load_tearsheet(asset)
    charts = get_charts_by_category(ts)
    passed = 0
    failed = 0

    # --- xy_lines L1: Numeric X ---
    print(f"\n=== xy_lines L1: Numeric X ({asset}) ===")
    cat = "10 xy_lines L1: Numeric X"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L1: Return vs Bar Index", f"got '{cd.title}'")
        r &= check("1 series", len(nld.lines) == 1, f"got {len(nld.lines)}")
        r &= check("has data points", len(nld.lines[0].data) > 0, f"got {len(nld.lines[0].data)}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L2: Multi-Series ---
    print(f"\n=== xy_lines L2: Multi-Series ({asset}) ===")
    cat = "11 xy_lines L2: Multi-Series"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L2: Close vs SMA 20", f"got '{cd.title}'")
        r &= check("2 series", len(nld.lines) == 2, f"got {len(nld.lines)}")
        names = [line.name for line in nld.lines]
        r &= check("series names", "Close" in names and "SMA 20" in names, f"got {names}")
        # Check dash_style on SMA 20
        for line in nld.lines:
            if line.name == "SMA 20":
                r &= check("SMA 20 has dash_style", line.dash_style != 0, f"got {line.dash_style}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L3: Area Fill ---
    print(f"\n=== xy_lines L3: Area Fill ({asset}) ===")
    cat = "12 xy_lines L3: Area Fill"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L3: Cumulative Return (Area)", f"got '{cd.title}'")
        r &= check("area=True", nld.area == True)
        r &= check("1 series", len(nld.lines) == 1, f"got {len(nld.lines)}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L4: Mixed Area ---
    print(f"\n=== xy_lines L4: Mixed Area ({asset}) ===")
    cat = "13 xy_lines L4: Mixed Area"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L4: Mixed Line + Area", f"got '{cd.title}'")
        r &= check("2 series", len(nld.lines) == 2, f"got {len(nld.lines)}")
        # Check per-series area override
        areas = {line.name: line.area for line in nld.lines}
        r &= check("Cum Return has area=True", areas.get("Cum Return", False) == True, f"got {areas}")
        r &= check("Daily Return has area=False", areas.get("Daily Return", True) == False, f"got {areas}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L5: Stacked Area ---
    print(f"\n=== xy_lines L5: Stacked Area ({asset}) ===")
    cat = "14 xy_lines L5: Stacked Area"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L5: Stacked SMA 20 + SMA 50", f"got '{cd.title}'")
        r &= check("area=True", nld.area == True)
        r &= check("stack_type=NormalStack", nld.stack_type == 1, f"got {nld.stack_type}")
        r &= check("2 series", len(nld.lines) == 2, f"got {len(nld.lines)}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L6: Step Function ---
    print(f"\n=== xy_lines L6: Step Function ({asset}) ===")
    cat = "15 xy_lines L6: Step Function"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L6: Position Flag (Step)", f"got '{cd.title}'")
        # StepLeft = 1 in proto enum
        r &= check("step=StepLeft", nld.step == 1, f"got {nld.step}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L7: Split By Label ---
    print(f"\n=== xy_lines L7: Split By Label ({asset}) ===")
    cat = "16 xy_lines L7: Split By Label"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L7: Cumulative Return by Year", f"got '{cd.title}'")
        # Split by label should produce multiple series (one per year) — count depends on date range
        n_series = len(nld.lines)
        r &= check(f"split_by_label produced {n_series} series (>=1)", n_series >= 1, f"got {n_series} series")
        if n_series == 1:
            print("  [WARN] Only 1 series — re-run with multi-year date range (e.g., 2020-2024) for full validation")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L8: Category Mode ---
    print(f"\n=== xy_lines L8: Category Mode ({asset}) ===")
    cat = "17 xy_lines L8: Category Mode"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L8: Average Return by Month", f"got '{cd.title}'")
        r &= check("1 series", len(nld.lines) == 1, f"got {len(nld.lines)}")
        # Category mode with Month should produce ~12 data points
        if nld.lines:
            pts = len(nld.lines[0].data)
            r &= check("~12 data points (months)", 10 <= pts <= 13, f"got {pts}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L9: Band Mode ---
    print(f"\n=== xy_lines L9: Band Mode ({asset}) ===")
    cat = "18 xy_lines L9: Band Mode"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L9: Close with Big-Down Bands", f"got '{cd.title}'")
        # Band mode: is_band series gets converted to x_plot_bands, leaving 1 visible series
        r &= check("1 visible series (Close)", len(nld.lines) == 1, f"got {len(nld.lines)}")
        r &= check("has x_plot_bands from is_band", len(nld.x_plot_bands) >= 1, f"got {len(nld.x_plot_bands)}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L10: Reference Lines ---
    print(f"\n=== xy_lines L10: Reference Lines ({asset}) ===")
    cat = "19 xy_lines L10: Reference Lines"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L10: Daily Return with +/-2% Reference", f"got '{cd.title}'")
        r &= check("3 reference lines", len(nld.straight_lines) == 3, f"got {len(nld.straight_lines)}")
        ref_values = sorted([sl.value for sl in nld.straight_lines])
        r &= check("ref values [-0.02, 0, 0.02]", ref_values == [-0.02, 0.0, 0.02], f"got {ref_values}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L11: Spline + Labels ---
    print(f"\n=== xy_lines L11: Spline+Labels ({asset}) ===")
    cat = "20 xy_lines L11: Spline+Labels"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L11: SMA 50 (Smooth + Labels)", f"got '{cd.title}'")
        r &= check("smooth=True", nld.smooth == True)
        r &= check("data_labels=True", nld.data_labels == True)
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L12: Log Scale ---
    print(f"\n=== xy_lines L12: Log Scale ({asset}) ===")
    cat = "21 xy_lines L12: Log Scale"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L12: Close (Log Scale)", f"got '{cd.title}'")
        # Log scale is on the y_axis of chart_def
        r &= check("y_axis log scale", cd.y_axis.type == 2, f"got AxisType={cd.y_axis.type} (expected 2=AxisLogarithmic)")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L13: Timestamp X ---
    print(f"\n=== xy_lines L13: Timestamp X ({asset}) ===")
    cat = "22 xy_lines L13: Timestamp X"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L13: Close on Timestamp X", f"got '{cd.title}'")
        r &= check("1 series", len(nld.lines) == 1, f"got {len(nld.lines)}")
        r &= check("has data", len(nld.lines[0].data) > 100, f"got {len(nld.lines[0].data)} points")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L14: Plot Bands ---
    print(f"\n=== xy_lines L14: Plot Bands ({asset}) ===")
    cat = "23 xy_lines L14: Plot Bands"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L14: RSI with Zones", f"got '{cd.title}'")
        r &= check("3 y_plot_bands", len(nld.y_plot_bands) == 3, f"got {len(nld.y_plot_bands)}")
        if len(nld.y_plot_bands) == 3:
            bands = sorted([(getattr(b, 'from').decimal_value, b.to.decimal_value) for b in nld.y_plot_bands])
            r &= check("band ranges [0-30, 30-70, 70-100]",
                       bands == [(0.0, 30.0), (30.0, 70.0), (70.0, 100.0)],
                       f"got {bands}")
            # Check opacity is set
            has_opacity = any(b.opacity > 0 for b in nld.y_plot_bands)
            r &= check("opacity set on bands", has_opacity)
            # Check labels
            labels = [b.label for b in nld.y_plot_bands if b.label]
            r &= check("labels set on bands", len(labels) >= 2, f"got {labels}")
        r &= check("1 series (RSI)", len(nld.lines) == 1, f"got {len(nld.lines)}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- xy_lines L15: Overlay Lines ---
    print(f"\n=== xy_lines L15: Overlay Lines ({asset}) ===")
    cat = "24 xy_lines L15: Overlay Lines"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L15: Close with SMA 50 Overlay", f"got '{cd.title}'")
        r &= check("1 main series", len(nld.lines) == 1, f"got {len(nld.lines)}")
        r &= check("1 overlay line", len(nld.overlay_lines) == 1, f"got {len(nld.overlay_lines)}")
        if nld.overlay_lines:
            r &= check("overlay name='SMA 50'", nld.overlay_lines[0].name == "SMA 50",
                       f"got '{nld.overlay_lines[0].name}'")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- labeled_lines L1: Single Series ---
    print(f"\n=== labeled_lines L1: Single Series ({asset}) ===")
    cat = "25 labeled_lines L1: Single Series"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L1: SMA Profile", f"got '{cd.title}'")
        r &= check("1 series", len(nld.lines) == 1, f"got {len(nld.lines)}")
        if nld.lines:
            pts = len(nld.lines[0].data)
            r &= check("5 data points", pts == 5, f"got {pts}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- labeled_lines L2: Multi-Series ---
    print(f"\n=== labeled_lines L2: Multi-Series ({asset}) ===")
    cat = "26 labeled_lines L2: Multi-Series"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L2: Current vs 1Y Ago SMA", f"got '{cd.title}'")
        r &= check("2 series", len(nld.lines) == 2, f"got {len(nld.lines)}")
        names = [line.name for line in nld.lines]
        r &= check("series names", "Current" in names and "1Y Ago" in names, f"got {names}")
        if nld.lines:
            pts = len(nld.lines[0].data)
            r &= check("5 data points per series", pts == 5, f"got {pts}")
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    # --- labeled_lines L3: Reference Line ---
    print(f"\n=== labeled_lines L3: Reference Line ({asset}) ===")
    cat = "27 labeled_lines L3: Reference Line"
    if cat in charts:
        cd, nld = charts[cat]
        r = check("title", cd.title == "L3: SMA Deviation with Zero Reference", f"got '{cd.title}'")
        r &= check("1 series", len(nld.lines) == 1, f"got {len(nld.lines)}")
        r &= check("has reference lines", len(nld.straight_lines) >= 1, f"got {len(nld.straight_lines)}")
        if nld.straight_lines:
            r &= check("ref line value=0", nld.straight_lines[0].value == 0.0)
        passed += r; failed += (not r)
    else:
        print(f"  [FAIL] category '{cat}' not found"); failed += 1

    return passed, failed


if __name__ == "__main__":
    total_passed = 0
    total_failed = 0

    print("=" * 60)
    print("LINES HANDBOOK TEARSHEET VALIDATION")
    print("=" * 60)

    print("\n" + "=" * 60)
    print("CROSS-SECTIONAL CHARTS (ALL tearsheet)")
    print("=" * 60)
    p, f = validate_all()
    total_passed += p
    total_failed += f

    print("\n" + "=" * 60)
    print("PER-ASSET CHARTS (SPY-Stocks tearsheet)")
    print("=" * 60)
    p, f = validate_per_asset("SPY-Stocks")
    total_passed += p
    total_failed += f

    print("\n" + "=" * 60)
    print(f"SUMMARY: {total_passed} passed, {total_failed} failed")
    print("=" * 60)

    sys.exit(1 if total_failed > 0 else 0)
