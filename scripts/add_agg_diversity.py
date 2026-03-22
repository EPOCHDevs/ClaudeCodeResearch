#!/usr/bin/env python3
"""Add AggregationType diversity sections to all reporter cluster handbooks.

Fills all uncovered reporter × agg enum coverage units by appending compact
invocations to existing handbook definition files.
"""

import json
import os

HANDBOOK_DIR = "/home/adesola/EpochDev/ClaudeCodeResearch/project_hand_book/definitions/test_runner"

ALL_AGGS = [
    "Mean", "Sum", "Last", "Min", "Max", "Median", "Std", "Count",
    "First", "All", "Any", "CountDistinct", "Kurtosis", "Mode",
    "Product", "Quantile", "Skew", "Var"
]

# (handbook_file, reporter_name, covered_aggs, template_with_{agg}_placeholder)
CONFIGS = [
    # === bars_handbook (xy_bars: 15 missing, cs_bars: 16 missing) ===
    ("reporter_cluster_bars_handbook.json", "xy_bars",
     ["Mean", "Sum", "Last"],
     "xy_bars(\n"
     "    mode=BarMode.labeled,\n"
     "    agg=AggregationType.{agg},\n"
     "    x_category_type=CategoryAxisType.DayOfWeek,\n"
     "    category='AD xy_bars agg={agg}'\n"
     ")(daily_ret, label=day_of_week)"),

    ("reporter_cluster_bars_handbook.json", "cs_bars",
     ["Mean", "Last"],
     "cs_bars(\n"
     "    mode=CSBarMode.simple,\n"
     "    agg=AggregationType.{agg},\n"
     "    category='AD cs_bars agg={agg}'\n"
     ")(values=daily_ret)"),

    # === gauge_handbook (gauge: 17 missing, cs_gauge: 17 missing) ===
    ("reporter_cluster_gauge_handbook.json", "gauge",
     ["Last"],
     "gauge(\n"
     "    agg=AggregationType.{agg},\n"
     "    min=0, max=100,\n"
     "    category='AD gauge agg={agg}'\n"
     ")(value=rsi_14)"),

    ("reporter_cluster_gauge_handbook.json", "cs_gauge",
     ["Mean"],
     "cs_gauge(\n"
     "    agg=AggregationType.{agg},\n"
     "    min=0, max=100,\n"
     "    category='AD cs_gauge agg={agg}'\n"
     ")(value=rsi_14)"),

    # === heatmap_handbook (heatmap: 15 missing, cs_heatmap: 13 missing) ===
    ("reporter_cluster_heatmap_handbook.json", "heatmap",
     ["Mean", "Count", "Last"],
     "heatmap(\n"
     "    agg=AggregationType.{agg},\n"
     "    x_category_type=CategoryAxisType.Month,\n"
     "    category='AD heatmap agg={agg}'\n"
     ")(x=month_num, y=year_num, value=daily_ret)"),

    ("reporter_cluster_heatmap_handbook.json", "cs_heatmap",
     ["Last", "Mean", "Std", "Min", "Median"],
     "cs_heatmap(\n"
     "    mode=HeatmapMode.values,\n"
     "    agg=AggregationType.{agg},\n"
     "    category='AD cs_heatmap agg={agg}'\n"
     ")(daily_ret)"),

    # === lines_handbook (cs_lines: 16 missing, cs_labeled_lines: 16 missing) ===
    ("reporter_cluster_lines_handbook.json", "cs_lines",
     ["Mean", "Median"],
     "cs_lines(\n"
     "    agg=AggregationType.{agg},\n"
     "    category='AD cs_lines agg={agg}'\n"
     ")(x_values=ts, y_values=daily_ret)"),

    ("reporter_cluster_lines_handbook.json", "cs_labeled_lines",
     ["Last", "Mean"],
     "cs_labeled_lines(\n"
     "    agg=AggregationType.{agg},\n"
     "    x_labels=['5D', '10D', '20D', '60D', '120D'],\n"
     "    category='AD cs_labeled_lines agg={agg}'\n"
     ")(sma_5, sma_10, sma_20, sma_60, sma_120)"),

    # === pie_handbook (cs_pie: 13 missing) ===
    ("reporter_cluster_pie_handbook.json", "cs_pie",
     ["Last", "Sum", "Std", "Mean", "Min"],
     "cs_pie(\n"
     "    agg=AggregationType.{agg},\n"
     "    category='AD cs_pie agg={agg}'\n"
     ")(close)"),

    # === scatter_handbook (cs_scatter: 17 missing, cs_labeled_scatter: 17 missing) ===
    ("reporter_cluster_scatter_handbook.json", "cs_scatter",
     ["Mean"],
     "cs_scatter(\n"
     "    agg=AggregationType.{agg},\n"
     "    category='AD cs_scatter agg={agg}'\n"
     ")(x=rolling_var, y=daily_ret)"),

    ("reporter_cluster_scatter_handbook.json", "cs_labeled_scatter",
     ["Mean"],
     "cs_labeled_scatter(\n"
     "    agg=AggregationType.{agg},\n"
     "    category='AD cs_labeled_scatter agg={agg}'\n"
     ")(x=rolling_var, y=daily_ret)"),

    # === bubble_handbook (cs_labeled_bubble: 17 missing) ===
    ("reporter_cluster_bubble_handbook.json", "cs_labeled_bubble",
     ["Mean"],
     "cs_labeled_bubble(\n"
     "    agg=AggregationType.{agg},\n"
     "    category='AD cs_labeled_bubble agg={agg}'\n"
     ")(x=vol_20, y=daily_ret, z=volume)"),

    # === tables_handbook (cs_summary_table: 16 missing) ===
    ("reporter_cluster_tables_handbook.json", "cs_summary_table",
     ["Last", "Mean"],
     "cs_summary_table(\n"
     "    agg=AggregationType.{agg},\n"
     "    schema=TableReportSchema(\n"
     "      columns=[\n"
     "        ColumnSpec(title='Close', type=CardRenderType.DecimalFormat, dp=2),\n"
     "        ColumnSpec(title='RSI', type=CardRenderType.DecimalFormat, dp=1)\n"
     "      ]),\n"
     "    category='AD cs_summary_table agg={agg}'\n"
     ")(close, rsi_14)"),
]


def main():
    # Group by handbook file
    by_file = {}
    for handbook_file, reporter, covered, template in CONFIGS:
        if handbook_file not in by_file:
            by_file[handbook_file] = []
        missing = [a for a in ALL_AGGS if a not in covered]
        by_file[handbook_file].append((reporter, missing, template))

    total_added = 0
    for handbook_file, reporters in by_file.items():
        filepath = os.path.join(HANDBOOK_DIR, handbook_file)
        with open(filepath, 'r') as f:
            data = json.load(f)

        source = data['source']
        file_added = 0

        for reporter, missing_aggs, template in reporters:
            header = (
                f"\n# ========================================================================\n"
                f"# {reporter.upper()} — AGG DIVERSITY ({len(missing_aggs)} values)\n"
                f"# ========================================================================\n"
            )
            source += header

            for agg in missing_aggs:
                invocation = template.format(agg=agg)
                source += f"\n{invocation}\n"
                file_added += 1

        data['source'] = source

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=3)

        total_added += file_added
        print(f"  {handbook_file}: +{file_added} invocations")

    print(f"\nTotal: {total_added} agg diversity invocations added")


if __name__ == "__main__":
    main()
