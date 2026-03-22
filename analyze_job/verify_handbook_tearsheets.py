"""
Verify handbook tearsheets — dump EXACTLY what the agent sees.

For each handbook, loads the tearsheet proto via LocalDataProvider and calls:
1. format_tearsheet_summary() — the text injected into <dashboard_data> for key_takeaways
2. cards_to_compact_list() — the card metrics the agent reads
3. chart_to_dataframe() — the DataFrames available for SQL querying

Outputs one .txt file per handbook with the FULL agent-visible content.
"""
import sys
import os
import json
import traceback
from pathlib import Path

# Add EpochAI to path for imports
sys.path.insert(0, "/home/adesola/EpochDev/EpochAI")
sys.path.insert(0, "/home/adesola/EpochDev/EpochAI/packages/epoch-protos")

from epoch_protos import tearsheet_pb2, table_def_pb2, common_pb2
from epoch_protos.summary import format_tearsheet_summary
from epoch_protos.converters import cards_to_compact_list


def load_tearsheet_from_local(job_folder: str):
    """Load tearsheet data from local job data using LocalDataProvider.
    Returns (categories, tearsheets_dict) where tearsheets_dict maps category -> TearSheet proto.
    """
    sys.path.insert(0, "/home/adesola/EpochDev/ClaudeCodeResearch")
    from analyze_job.get_study_reports import _load_provider_data
    provider, cats, tearsheets = _load_provider_data(job_folder)
    return cats, tearsheets


def format_cards_verbose(tearsheet):
    """Extract ALL card data with raw values — exactly what the agent sees."""
    lines = []
    card_tables = []
    if tearsheet.tables and tearsheet.tables.tables:
        card_tables = [
            t for t in tearsheet.tables.tables
            if t.flavor == table_def_pb2.TABLE_FLAVOR_CARDS
        ]

    if not card_tables:
        lines.append("  (no cards)")
        return "\n".join(lines)

    for table in card_tables:
        if table.category:
            lines.append(f"  [Category: {table.category}]")
        if not table.cards_data:
            continue
        for cell in table.cards_data.cells:
            raw_val = _extract_raw(cell.value)
            formatted = _format_card_value(cell.value)
            lines.append(f"    {cell.title}: {formatted}  (raw={raw_val})")
    return "\n".join(lines)


def format_tables_verbose(tearsheet):
    """Extract ALL table data — rows, columns, values."""
    lines = []
    if not tearsheet.tables or not tearsheet.tables.tables:
        lines.append("  (no tables)")
        return "\n".join(lines)

    regular_tables = [
        t for t in tearsheet.tables.tables
        if t.flavor != table_def_pb2.TABLE_FLAVOR_CARDS
    ]

    if not regular_tables:
        lines.append("  (no regular tables)")
        return "\n".join(lines)

    for table in regular_tables:
        flavor_name = "Summary" if table.flavor == table_def_pb2.TABLE_FLAVOR_SUMMARY else "Detailed"
        title = getattr(table, 'title', '(untitled)')
        category = getattr(table, 'category', '-') or '-'
        lines.append(f"  TABLE: {title} [{flavor_name}] (category={category})")

        # Column headers
        col_headers = []
        for i, col in enumerate(table.columns):
            name = None
            for attr in ('title', 'name', 'header'):
                try:
                    name = getattr(col, attr, None)
                    if name:
                        break
                except:
                    pass
            col_headers.append(name or f"Col{i}")
        if col_headers:
            lines.append(f"    Columns: {' | '.join(col_headers)}")

        # Layout info
        if table.HasField('layout'):
            lines.append(f"    Layout: {table.layout.row_size}x{table.layout.col_size}")

        # Row data (detailed tables)
        has_data = False
        try:
            if table.HasField('data') and table.data.rows:
                has_data = True
                for row_idx, row in enumerate(table.data.rows):
                    cells = []
                    # Try cells first, then values
                    row_cells = list(row.cells) if row.cells else []
                    row_values = list(row.values) if hasattr(row, 'values') and row.values else []
                    for cell in (row_cells or row_values):
                        cells.append(_extract_raw(cell))
                    row_label = f"    Row {row_idx}"
                    if hasattr(row, 'header') and row.header:
                        row_label = f"    {row.header}"
                    lines.append(f"{row_label}: {' | '.join(str(c) for c in cells)}")
        except:
            pass

        # Summary data (summary tables)
        try:
            if not has_data and table.HasField('summary_data') and table.summary_data.cells:
                has_data = True
                for cell in table.summary_data.cells:
                    val = _extract_raw(cell.value) if hasattr(cell, 'value') else _extract_raw(cell)
                    title_str = getattr(cell, 'title', None) or getattr(cell, 'label', None) or '?'
                    lines.append(f"    {title_str}: {val}")
        except:
            pass

        # Cards data fallback
        try:
            if not has_data and table.HasField('cards_data') and table.cards_data.cells:
                has_data = True
                for cell in table.cards_data.cells:
                    val = _extract_raw(cell.value)
                    lines.append(f"    {cell.title}: {val}")
        except:
            pass

        if not has_data:
            # Last resort — dump MessageToDict
            try:
                from google.protobuf.json_format import MessageToDict
                d = MessageToDict(table, preserving_proto_field_name=True)
                # Remove bulky fields, show what data fields exist
                data_keys = [k for k in d.keys() if k not in ('chart_def', 'columns')]
                lines.append(f"    Data fields: {data_keys}")
                # Show summary_data or data if present
                for key in ('summary_data', 'data', 'cards_data'):
                    if key in d:
                        import json
                        dump = json.dumps(d[key], indent=2, default=str)[:500]
                        lines.append(f"    {key}: {dump}")
            except Exception as e:
                lines.append(f"    (no row data, fallback error: {e})")

        lines.append("")
    return "\n".join(lines)


def format_charts_verbose(tearsheet):
    """Extract ALL chart data — every series, every point, every slice."""
    lines = []
    if not tearsheet.charts or not tearsheet.charts.charts:
        lines.append("  (no charts)")
        return "\n".join(lines)

    for chart in tearsheet.charts.charts:
        chart_type = chart.WhichOneof("chart_type")
        if not chart_type:
            continue

        chart_data = getattr(chart, chart_type)
        chart_def = chart_data.chart_def
        title = chart_def.title or chart_def.id or "(untitled)"
        category = chart_def.category or "-"
        type_display = chart_type.replace("_def", "")

        lines.append(f"  CHART: {title} [type={type_display}] (category={category})")

        try:
            if chart_type == "lines_def":
                _dump_lines(lines, chart_data)
            elif chart_type == "numeric_lines_def":
                _dump_numeric_lines(lines, chart_data)
            elif chart_type == "bar_def":
                _dump_bars(lines, chart_data)
            elif chart_type == "pie_def":
                _dump_pie(lines, chart_data)
            elif chart_type == "scatter_def":
                _dump_scatter(lines, chart_data)
            elif chart_type == "bubble_def":
                _dump_bubble(lines, chart_data)
            elif chart_type == "heat_map_def":
                _dump_heatmap(lines, chart_data)
            elif chart_type == "histogram_def":
                _dump_histogram(lines, chart_data)
            elif chart_type == "box_plot_def":
                _dump_boxplot(lines, chart_data)
            elif chart_type == "gauge_def":
                _dump_gauge(lines, chart_data)
            elif chart_type == "x_range_def":
                _dump_xrange(lines, chart_data)
            elif chart_type == "area_def":
                _dump_area(lines, chart_data)
            else:
                lines.append(f"    (unhandled chart type: {chart_type})")
        except Exception as e:
            lines.append(f"    ERROR parsing {chart_type}: {e}")
            lines.append(f"    {traceback.format_exc()}")

        lines.append("")
    return "\n".join(lines)


# ─── Chart data dumpers ───

def _dump_lines(lines, data):
    """Dump timeseries lines — head/tail + stats."""
    for line in data.lines:
        pts = list(line.data)
        lines.append(f"    Series: {line.name or '(unnamed)'} ({len(pts)} points)")
        if pts:
            head = pts[:5]
            tail = pts[-3:] if len(pts) > 5 else []
            for pt in head:
                lines.append(f"      x={_ts_to_date(pt.x)}, y={pt.y:.6f}")
            if tail:
                lines.append(f"      ... ({len(pts) - 8} more) ...")
                for pt in tail:
                    lines.append(f"      x={_ts_to_date(pt.x)}, y={pt.y:.6f}")
    # Reference lines
    if hasattr(data, 'straight_lines') and data.straight_lines:
        for sl in data.straight_lines:
            lines.append(f"    RefLine: {sl.title}={sl.value}")


def _dump_numeric_lines(lines, data):
    """Dump numeric-x lines."""
    x_cats = None
    if data.chart_def.HasField("x_axis") and data.chart_def.x_axis.categories:
        x_cats = list(data.chart_def.x_axis.categories)
        lines.append(f"    X-Categories: {x_cats}")
    for line in data.lines:
        pts = list(line.data)
        lines.append(f"    Series: {line.name or '(unnamed)'} ({len(pts)} points)")
        if pts:
            for pt in pts[:10]:
                x_label = x_cats[int(pt.x)] if x_cats and 0 <= int(pt.x) < len(x_cats) else pt.x
                lines.append(f"      x={x_label}, y={pt.y:.6f}")
            if len(pts) > 10:
                lines.append(f"      ... ({len(pts) - 10} more)")
    if hasattr(data, 'straight_lines') and data.straight_lines:
        for sl in data.straight_lines:
            lines.append(f"    RefLine: {sl.title}={sl.value}")


def _dump_bars(lines, data):
    """Dump bar chart data — categories + values."""
    categories = []
    if data.chart_def.HasField("x_axis") and data.chart_def.x_axis.categories:
        categories = list(data.chart_def.x_axis.categories)
        lines.append(f"    X-Categories: {categories}")
    for bar_series in data.data:
        name = bar_series.name or "Values"
        vals = list(bar_series.values)
        lines.append(f"    Series: {name} ({len(vals)} bars)")
        for i, val in enumerate(vals):
            cat = categories[i] if i < len(categories) else str(i)
            lines.append(f"      {cat}: {val:.6f}")
    # Overlay lines
    if data.overlay_lines:
        for overlay in data.overlay_lines:
            lines.append(f"    Overlay: {overlay.name or '(unnamed)'} ({len(overlay.data)} points)")
            for pt in overlay.data[:10]:
                lines.append(f"      x={pt.x}, y={pt.y:.6f}")
    if hasattr(data, 'straight_lines') and data.straight_lines:
        for sl in data.straight_lines:
            lines.append(f"    RefLine: {sl.title}={sl.value}")


def _dump_pie(lines, data):
    """Dump pie chart — every slice with name, value, percentage."""
    for ring_idx, ring in enumerate(data.data):
        pts = list(ring.points)
        name = ring.name or f"Ring {ring_idx}"
        inner = ring.inner_size or "0%"
        size = ring.size or "75%"
        lines.append(f"    Ring: {name} (size={size}, innerSize={inner}, {len(pts)} slices)")
        total = sum(pt.y for pt in pts)
        for pt in pts:
            pct = (pt.y / total * 100) if total > 0 else 0
            color_str = ""
            try:
                if pt.HasField("color"):
                    color_str = f" color=({pt.color.r},{pt.color.g},{pt.color.b})"
            except (ValueError, AttributeError):
                pass
            lines.append(f"      {pt.name}: y={pt.y:.4f} ({pct:.1f}%){color_str}")
    # Colors at chart level
    try:
        if hasattr(data, 'colors') and data.colors:
            color_strs = [f"({c.r},{c.g},{c.b})" for c in data.colors]
            lines.append(f"    Chart Colors: {color_strs}")
    except (AttributeError, TypeError):
        pass


def _dump_scatter(lines, data):
    """Dump scatter chart data."""
    for s in data.series:
        pts = list(s.data)
        lines.append(f"    Series: {s.name or '(unnamed)'} ({len(pts)} points)")
        for pt in pts[:15]:
            name_str = f" name={pt.name}" if pt.name else ""
            lines.append(f"      x={pt.x:.6f}, y={pt.y:.6f}{name_str}")
        if len(pts) > 15:
            lines.append(f"      ... ({len(pts) - 15} more)")
    if hasattr(data, 'straight_lines') and data.straight_lines:
        for sl in data.straight_lines:
            lines.append(f"    RefLine: {sl.title}={sl.value} vertical={sl.vertical}")


def _dump_bubble(lines, data):
    """Dump bubble chart data."""
    for s in data.series:
        pts = list(s.data)
        lines.append(f"    Series: {s.name or '(unnamed)'} ({len(pts)} bubbles)")
        for pt in pts[:15]:
            name_str = f" name={pt.name}" if pt.name else ""
            desc_str = f" desc={pt.description}" if pt.description else ""
            lines.append(f"      x={pt.x:.6f}, y={pt.y:.6f}, z={pt.z:.6f}{name_str}{desc_str}")
        if len(pts) > 15:
            lines.append(f"      ... ({len(pts) - 15} more)")
    if hasattr(data, 'straight_lines') and data.straight_lines:
        for sl in data.straight_lines:
            lines.append(f"    RefLine: {sl.title}={sl.value} vertical={sl.vertical}")


def _dump_heatmap(lines, data):
    """Dump heatmap — all points with x/y labels."""
    x_cats = []
    y_cats = []
    if data.chart_def.HasField("x_axis") and data.chart_def.x_axis.categories:
        x_cats = list(data.chart_def.x_axis.categories)
    if data.chart_def.HasField("y_axis") and data.chart_def.y_axis.categories:
        y_cats = list(data.chart_def.y_axis.categories)
    if x_cats:
        lines.append(f"    X-Categories: {x_cats}")
    if y_cats:
        lines.append(f"    Y-Categories: {y_cats}")
    pts = list(data.points)
    lines.append(f"    Points: {len(pts)} cells")
    for pt in pts[:50]:
        x_label = x_cats[pt.x] if pt.x < len(x_cats) else str(pt.x)
        y_label = y_cats[pt.y] if pt.y < len(y_cats) else str(pt.y)
        label_str = f" label={pt.label}" if pt.label else ""
        empty_str = " EMPTY" if pt.is_empty else ""
        lines.append(f"      [{y_label}, {x_label}]: {pt.value:.6f}{label_str}{empty_str}")
    if len(pts) > 50:
        lines.append(f"      ... ({len(pts) - 50} more)")


def _dump_histogram(lines, data):
    """Dump histogram — bins and analytics."""
    if data.series:
        for s in data.series:
            lines.append(f"    Series: {s.name or '(unnamed)'} ({len(s.bins)} bins)")
            for b in s.bins:
                lines.append(f"      [{b.bin_start:.6f}, {b.bin_end:.6f}): count={b.count}")
    if data.HasField('analytics'):
        a = data.analytics
        lines.append(f"    Analytics: mean={a.mean:.6f}, std={a.std_dev:.6f}, n={a.sample_count}")
        try:
            if a.HasField('skewness'):
                lines.append(f"      skewness={a.skewness:.6f}, kurtosis={a.kurtosis:.6f}")
        except ValueError:
            # proto3 scalar fields don't support HasField
            if a.skewness != 0:
                lines.append(f"      skewness={a.skewness:.6f}, kurtosis={a.kurtosis:.6f}")
        try:
            if a.HasField('mode'):
                lines.append(f"      mode={a.mode:.6f}")
        except ValueError:
            if a.mode != 0:
                lines.append(f"      mode={a.mode:.6f}")


def _dump_boxplot(lines, data):
    """Dump box plot data. BoxPlotDef.data is a BoxPlotDataPointDef with .points and .outliers."""
    box_data = data.data  # BoxPlotDataPointDef (not iterable — single message)
    pts = list(box_data.points)  # BoxPlotDataPoint[] — each has low, q1, median, q3, high
    x_cats = []
    if data.chart_def.HasField("x_axis") and data.chart_def.x_axis.categories:
        x_cats = list(data.chart_def.x_axis.categories)
    lines.append(f"    Boxes: {len(pts)}")
    for i, pt in enumerate(pts):
        label = x_cats[i] if i < len(x_cats) else f"Box {i}"
        lines.append(f"      {label}: low={pt.low:.6f}, q1={pt.q1:.6f}, median={pt.median:.6f}, q3={pt.q3:.6f}, high={pt.high:.6f}")
    # Outliers
    outliers = list(box_data.outliers) if box_data.outliers else []
    if outliers:
        lines.append(f"    Outliers: {len(outliers)}")
        for o in outliers[:20]:
            cat_label = x_cats[o.category_index] if o.category_index < len(x_cats) else str(o.category_index)
            lines.append(f"      [{cat_label}]: {o.value:.6f}")


def _dump_gauge(lines, data):
    """Dump gauge data. GaugeDef has .stops (GaugeStop[]) not .zones."""
    lines.append(f"    Value: {data.value:.6f}")
    lines.append(f"    Min: {data.min}, Max: {data.max}")
    try:
        if data.stops:
            stops = [(f"pos={s.position:.2f}", f"color=({s.color.r},{s.color.g},{s.color.b})") for s in data.stops]
            lines.append(f"    Stops: {stops}")
    except (AttributeError, TypeError):
        pass
    try:
        lines.append(f"    Solid: {data.solid}")
    except AttributeError:
        pass


def _dump_xrange(lines, data):
    """Dump x-range (gantt) data."""
    pts = list(data.data)
    lines.append(f"    Ranges: {len(pts)}")
    for pt in pts[:20]:
        lines.append(f"      {pt.label}: x={pt.x}, x2={pt.x2}, y={pt.y}")


def _dump_area(lines, data):
    """Dump area chart."""
    for area in data.areas:
        pts = list(area.data)
        lines.append(f"    Area: {area.name or '(unnamed)'} ({len(pts)} points)")
        for pt in pts[:5]:
            lines.append(f"      x={_ts_to_date(pt.x)}, y={pt.y:.6f}")
        if len(pts) > 5:
            lines.append(f"      ... ({len(pts) - 5} more)")


# ─── Helpers ───

def _ts_to_date(ms):
    from datetime import datetime, timezone
    try:
        return datetime.fromtimestamp(float(ms) / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    except (OSError, ValueError):
        return str(ms)


def _extract_raw(scalar):
    """Get raw value from Scalar proto."""
    for field in ('percent_value', 'decimal_value', 'integer_value',
                  'timestamp_ms', 'string_value', 'boolean_value',
                  'date_value', 'day_duration', 'monetary_value', 'duration_ms'):
        try:
            if scalar.HasField(field):
                return getattr(scalar, field)
        except:
            pass
    return None


def _format_card_value(scalar):
    """Format card value with type info."""
    for field in ('percent_value', 'decimal_value', 'integer_value',
                  'timestamp_ms', 'string_value', 'boolean_value',
                  'date_value', 'day_duration', 'monetary_value', 'duration_ms'):
        try:
            if scalar.HasField(field):
                val = getattr(scalar, field)
                if field == 'percent_value':
                    return f"{val:.2f}%"
                elif field == 'decimal_value':
                    return f"{val:.4f}"
                elif field == 'integer_value':
                    return f"{val:,}"
                elif field == 'monetary_value':
                    return f"${val:,.2f}"
                elif field == 'timestamp_ms' or field == 'date_value':
                    return _ts_to_date(val)
                elif field == 'boolean_value':
                    return "Yes" if val else "No"
                elif field == 'day_duration':
                    return f"{val} days"
                else:
                    return str(val)
        except:
            pass
    return "N/A"


def verify_handbook(job_folder: str, output_path: str):
    """Run full verification on a handbook's job output."""
    handbook_name = Path(job_folder).name
    lines = [f"{'='*80}", f"HANDBOOK: {handbook_name}", f"{'='*80}", ""]

    try:
        categories, tearsheets = load_tearsheet_from_local(job_folder)
    except Exception as e:
        lines.append(f"FATAL: Failed to load tearsheet: {e}")
        lines.append(traceback.format_exc())
        with open(output_path, 'w') as f:
            f.write("\n".join(lines))
        return False

    lines.append(f"Categories found: {categories}")
    lines.append("")

    errors = []

    for cat_name in categories:
        try:
            tearsheet = tearsheets[cat_name]
        except (KeyError, AttributeError) as e:
            lines.append(f"ERROR: Cannot access category '{cat_name}': {e}")
            errors.append(f"Category access: {cat_name}")
            continue

        lines.append(f"\n{'─'*70}")
        lines.append(f"CATEGORY: {cat_name}")
        lines.append(f"{'─'*70}")

        # 1. format_tearsheet_summary — what key_takeaways agent sees in <dashboard_data>
        lines.append("\n┌─ format_tearsheet_summary() output (agent sees this) ─┐")
        try:
            summary = format_tearsheet_summary(tearsheet, cat_name)
            lines.append(summary)
        except Exception as e:
            lines.append(f"ERROR: {e}")
            lines.append(traceback.format_exc())
            errors.append(f"format_tearsheet_summary({cat_name}): {e}")
        lines.append("└────────────────────────────────────────────────────────┘")

        # 2. Cards — verbose dump
        lines.append("\n┌─ Cards (verbose with raw values) ─┐")
        try:
            cards_output = format_cards_verbose(tearsheet)
            lines.append(cards_output)
        except Exception as e:
            lines.append(f"ERROR: {e}")
            errors.append(f"cards({cat_name}): {e}")
        lines.append("└───────────────────────────────────┘")

        # 3. Tables — verbose dump
        lines.append("\n┌─ Tables (verbose) ─┐")
        try:
            tables_output = format_tables_verbose(tearsheet)
            lines.append(tables_output)
        except Exception as e:
            lines.append(f"ERROR: {e}")
            errors.append(f"tables({cat_name}): {e}")
        lines.append("└────────────────────┘")

        # 4. Charts — verbose dump with ALL data
        lines.append("\n┌─ Charts (full data dump) ─┐")
        try:
            charts_output = format_charts_verbose(tearsheet)
            lines.append(charts_output)
        except Exception as e:
            lines.append(f"ERROR: {e}")
            lines.append(traceback.format_exc())
            errors.append(f"charts({cat_name}): {e}")
        lines.append("└───────────────────────────┘")

    # Summary
    lines.append(f"\n{'='*80}")
    lines.append(f"SUMMARY: {handbook_name}")
    lines.append(f"  Categories: {len(categories)}")
    lines.append(f"  Errors: {len(errors)}")
    if errors:
        for err in errors:
            lines.append(f"    - {err}")
    lines.append(f"{'='*80}")

    with open(output_path, 'w') as f:
        f.write("\n".join(lines))

    return len(errors) == 0


if __name__ == "__main__":
    handbooks = [
        "bars_handbook", "boxplot_handbook", "bubble_handbook",
        "gauge_handbook", "heatmap_handbook", "histogram_handbook",
        "lines_handbook", "pie_handbook", "scatter_handbook", "tables_handbook",
    ]

    output_dir = Path("project/verification/handbook_reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for hb in handbooks:
        job_folder = f"project/research_studies/test_runner/{hb}"
        output_path = str(output_dir / f"{hb}_FULL.txt")
        print(f"Verifying {hb}...", end=" ", flush=True)
        try:
            ok = verify_handbook(job_folder, output_path)
            results[hb] = "OK" if ok else "ERRORS"
            print(results[hb])
        except Exception as e:
            results[hb] = f"FATAL: {e}"
            print(results[hb])

    print(f"\n{'='*50}")
    print("RESULTS:")
    for hb, status in results.items():
        print(f"  {hb}: {status}")
