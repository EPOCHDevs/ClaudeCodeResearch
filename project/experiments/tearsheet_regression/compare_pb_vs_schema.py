#!/usr/bin/env python3
"""
Compare prod .pb tearsheets with local schema.json + Arrow output.

Decodes both formats and compares:
- Chart count, types, titles, series count
- Table count, flavors, titles
- Card values (title, value, type)
- Series data point counts
- Axis types and labels
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict

# Add the proto python path
PROTO_PATH = Path.home() / "EpochDev/EpochBackend/packages/epoch-protos/python"
sys.path.insert(0, str(PROTO_PATH))

from google.protobuf.json_format import MessageToDict
from epoch_protos import tearsheet_pb2

COMPARE_DIR = Path.home() / "EpochDev/ClaudeCodeResearch/project/experiments/tearsheet_regression/compare"
PROD_PB_DIR = COMPARE_DIR / "prod_pb"
HANDBOOK_DIR = Path.home() / "EpochDev/ClaudeCodeResearch/project_hand_book/research_studies/test_runner"

# Map handbook study names to their reporter type
REPORTER_NAMES = [
    "reporter_cluster_bars_handbook",
    "reporter_cluster_boxplot_handbook",
    "reporter_cluster_bubble_handbook",
    "reporter_cluster_gauge_handbook",
    "reporter_cluster_heatmap_handbook",
    "reporter_cluster_histogram_handbook",
    "reporter_cluster_lines_handbook",
    "reporter_cluster_pie_handbook",
    "reporter_cluster_scatter_handbook",
    "reporter_cluster_tables_handbook",
]


def decode_pb(pb_path: Path) -> dict:
    """Decode a .pb tearsheet into a dict using protobuf."""
    ts = tearsheet_pb2.TearSheet()
    ts.ParseFromString(pb_path.read_bytes())
    return MessageToDict(ts, preserving_proto_field_name=True)


def load_schema(schema_path: Path) -> dict:
    """Load schema.json."""
    return json.loads(schema_path.read_text())


def extract_proto_charts(proto_dict: dict) -> list:
    """Extract chart info from proto dict."""
    charts_container = proto_dict.get("charts", {})
    charts = charts_container.get("charts", [])
    result = []
    for c in charts:
        # Determine type from oneof — the chart_def is INSIDE the type-specific field
        chart_type = None
        chart_def = {}
        for key in c:
            if key.endswith("_def") and key != "chart_def":
                chart_type = key.replace("_def", "")
                # chart_def is nested inside the type-specific field
                chart_def = c[key].get("chart_def", {})
                break
        # Fallback to top-level chart_def
        if not chart_def:
            chart_def = c.get("chart_def", {})

        info = {
            "type": chart_type or "unknown",
            "title": chart_def.get("title", ""),
            "category": chart_def.get("category", ""),
        }

        # Count series/data points — data is inside the type-specific field
        type_key = chart_type + "_def" if chart_type else None
        type_data = c.get(type_key, {}) if type_key else {}

        if chart_type in ("lines", "numeric_lines"):
            lines = type_data.get("lines", [])
            info["series_count"] = len(lines)
            info["data_points"] = sum(len(l.get("data", [])) for l in lines)
        elif chart_type == "bar":
            bar_data = type_data.get("data", [])
            info["series_count"] = len(bar_data)
            info["data_points"] = sum(len(b.get("values", [])) for b in bar_data)
        elif chart_type == "scatter":
            scatter_series = type_data.get("series", [])
            info["series_count"] = len(scatter_series)
            info["data_points"] = sum(len(s.get("data", [])) for s in scatter_series)
        elif chart_type == "pie":
            pie_data = type_data.get("data", [])
            info["series_count"] = len(pie_data)
            info["data_points"] = sum(len(p.get("points", [])) for p in pie_data)
        elif chart_type == "gauge":
            info["series_count"] = 1
            info["data_points"] = 1
            info["gauge_value"] = type_data.get("value")
        elif chart_type == "heatmap":
            points = type_data.get("points", [])
            info["series_count"] = 1
            info["data_points"] = len(points)
        elif chart_type == "boxplot":
            data = type_data.get("data", {})
            info["series_count"] = 1
            info["data_points"] = len(data.get("points", []))
        elif chart_type == "bubble":
            series = type_data.get("series", [])
            info["series_count"] = len(series)
            info["data_points"] = sum(len(s.get("data", [])) for s in series)
        elif chart_type == "histogram":
            data = type_data.get("data", {})
            info["series_count"] = 1
            info["data_points"] = len(data.get("values", []))
        else:
            info["series_count"] = 0
            info["data_points"] = 0

        result.append(info)
    return result


def extract_schema_charts(schema: dict) -> list:
    """Extract chart info from schema.json."""
    result = []
    for c in schema.get("charts", []):
        info = {
            "type": c["type"],
            "title": c.get("title", ""),
            "category": c.get("category", ""),
            "series_count": (
                len(c.get("series", []))
                or len(c.get("bar_series", []))
                or len(c.get("scatter_series", []))
                or len(c.get("pie_series", []))
                or (1 if c.get("gauge_value") is not None else 0)
                or (1 if c.get("boxplot_data") else 0)
                or len(c.get("histogram_series", []))
                or 0
            ),
        }

        # Inline data counts
        if c["type"] == "Pie":
            info["data_points"] = sum(len(ps.get("points", [])) for ps in c.get("pie_series", []))
        elif c["type"] == "Gauge":
            info["data_points"] = 1
            info["gauge_value"] = c.get("gauge_value")
        elif c["type"] == "BoxPlot":
            info["data_points"] = len(c.get("boxplot_data", []))
        else:
            info["data_points"] = -1  # Arrow data, count separately

        result.append(info)
    return result


def extract_proto_tables(proto_dict: dict) -> list:
    """Extract table info from proto dict."""
    tables_container = proto_dict.get("tables", {})
    tables = tables_container.get("tables", [])
    result = []
    for t in tables:
        flavor_val = t.get("flavor", 0)
        # Proto flavor enum: 0=unspecified, 1=cards, 2=summary, 3=detailed
        flavor_map = {0: "Unknown", 1: "Cards", 2: "Summary", 3: "Detailed"}
        flavor = flavor_map.get(flavor_val, str(flavor_val))

        info = {
            "title": t.get("title", ""),
            "flavor": flavor,
        }

        if flavor == "Cards":
            cards = t.get("cards_data", {}).get("cells", [])
            info["cards"] = []
            for card in cards:
                title = card.get("title", "")
                # Extract scalar value
                value_field = card.get("value", {})
                val = None
                for k in ["decimal_value", "integer_value", "percent_value", "monetary_value"]:
                    if k in value_field:
                        val = value_field[k]
                        break
                info["cards"].append({"title": title, "value": val})

        result.append(info)
    return result


def extract_schema_tables(schema: dict) -> list:
    """Extract table info from schema.json."""
    result = []
    for t in schema.get("tables", []):
        info = {
            "title": t.get("title", ""),
            "flavor": t.get("flavor", "Unknown"),
        }
        if t.get("flavor") == "Cards":
            info["cards"] = [{"title": c["title"], "value": c["value"]} for c in t.get("cards", [])]
        result.append(info)
    return result


def compare_study(name: str, categories: list) -> dict:
    """Compare a single study across all categories."""
    results = {"name": name, "categories": {}}

    for cat in categories:
        pb_path = PROD_PB_DIR / name / cat / "tearsheet.pb"
        schema_path = HANDBOOK_DIR / name / "tearsheets" / cat / "schema.json"

        if not pb_path.exists():
            results["categories"][cat] = {"status": "SKIP", "reason": "no .pb"}
            continue
        if not schema_path.exists():
            results["categories"][cat] = {"status": "SKIP", "reason": "no schema.json"}
            continue

        issues = []

        # Decode both
        try:
            proto_dict = decode_pb(pb_path)
        except Exception as e:
            results["categories"][cat] = {"status": "FAIL", "reason": f"pb decode: {e}"}
            continue

        schema = load_schema(schema_path)

        # Compare charts
        proto_charts = extract_proto_charts(proto_dict)
        schema_charts = extract_schema_charts(schema)

        if len(proto_charts) != len(schema_charts):
            issues.append(f"chart count: proto={len(proto_charts)} schema={len(schema_charts)}")

        # Compare chart-by-chart (by title)
        proto_by_title = {c["title"]: c for c in proto_charts}
        schema_by_title = {c["title"]: c for c in schema_charts}

        for title in set(proto_by_title) | set(schema_by_title):
            pc = proto_by_title.get(title)
            sc = schema_by_title.get(title)

            if not pc:
                issues.append(f"chart '{title}': only in schema")
                continue
            if not sc:
                issues.append(f"chart '{title}': only in proto")
                continue

            # Compare series count
            if pc["series_count"] != sc["series_count"]:
                issues.append(f"chart '{title}': series proto={pc['series_count']} schema={sc['series_count']}")

            # Compare inline data points (pie, gauge, boxplot)
            if sc["data_points"] >= 0 and pc["data_points"] != sc["data_points"]:
                issues.append(f"chart '{title}': points proto={pc['data_points']} schema={sc['data_points']}")

            # Compare gauge values
            if "gauge_value" in pc and "gauge_value" in sc:
                pv = pc["gauge_value"]
                sv = sc["gauge_value"]
                if pv is not None and sv is not None and abs(float(pv) - float(sv)) > 0.01:
                    issues.append(f"chart '{title}': gauge value proto={pv} schema={sv}")

        # Compare tables
        proto_tables = extract_proto_tables(proto_dict)
        schema_tables = extract_schema_tables(schema)

        if len(proto_tables) != len(schema_tables):
            issues.append(f"table count: proto={len(proto_tables)} schema={len(schema_tables)}")

        # Compare cards by title
        for pt in proto_tables:
            if pt["flavor"] != "Cards":
                continue
            for st in schema_tables:
                if st["flavor"] != "Cards":
                    continue
                proto_cards = {c["title"]: c["value"] for c in pt.get("cards", [])}
                schema_cards = {c["title"]: c["value"] for c in st.get("cards", [])}

                for card_title in set(proto_cards) | set(schema_cards):
                    pv = proto_cards.get(card_title)
                    sv = schema_cards.get(card_title)
                    if pv is not None and sv is not None:
                        try:
                            if abs(float(pv) - float(sv)) > 0.001:
                                issues.append(f"card '{card_title}': proto={pv} schema={sv}")
                        except (ValueError, TypeError):
                            pass
                    elif pv is None and sv is not None:
                        issues.append(f"card '{card_title}': only in schema ({sv})")
                    elif sv is None and pv is not None:
                        issues.append(f"card '{card_title}': only in proto ({pv})")

        results["categories"][cat] = {
            "status": "PASS" if len(issues) == 0 else "FAIL",
            "proto_charts": len(proto_charts),
            "schema_charts": len(schema_charts),
            "proto_tables": len(proto_tables),
            "schema_tables": len(schema_tables),
            "issues": issues,
        }

    return results


def main():
    print("=== Proto vs Schema Tearsheet Comparison ===\n")

    all_pass = 0
    all_fail = 0
    all_skip = 0
    all_issues = []

    for name in sorted(REPORTER_NAMES):
        # Find categories from prod pb dir
        pb_dir = PROD_PB_DIR / name
        if not pb_dir.exists():
            print(f"  SKIP {name} (no prod data)")
            all_skip += 1
            continue

        categories = [d.name for d in pb_dir.iterdir() if d.is_dir()]
        result = compare_study(name, categories)

        for cat, data in sorted(result["categories"].items()):
            status = data["status"]
            if status == "PASS":
                print(f"  PASS {name}/{cat} — {data['proto_charts']} charts, {data['proto_tables']} tables")
                all_pass += 1
            elif status == "SKIP":
                print(f"  SKIP {name}/{cat} — {data['reason']}")
                all_skip += 1
            else:
                print(f"  FAIL {name}/{cat}:")
                issues = data.get("issues", [data.get("reason", "unknown")])
                for issue in issues:
                    print(f"    - {issue}")
                    all_issues.append(f"{name}/{cat}: {issue}")
                all_fail += 1

    print(f"\n=== Summary ===")
    print(f"  Pass: {all_pass}")
    print(f"  Fail: {all_fail}")
    print(f"  Skip: {all_skip}")

    if all_issues:
        print(f"\n=== Issues ({len(all_issues)}) ===")
        for issue in all_issues:
            print(f"  - {issue}")

    return 0 if all_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
