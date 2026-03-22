#!/usr/bin/env python3
"""
Query study dataframes using SQL.

Usage:
    python query_study_dataframes.py <job_folder> --tables
    python query_study_dataframes.py <job_folder> --schema <table>
    python query_study_dataframes.py <job_folder> --query "SELECT * FROM ..."
    python query_study_dataframes.py <job_folder> --nulls
    python query_study_dataframes.py <job_folder> --interactive

Examples:
    python query_study_dataframes.py job_data/research_studies/test_runner/my_study --tables
    python query_study_dataframes.py job_data/research_studies/test_runner/my_study --nulls
    python query_study_dataframes.py job_data/research_studies/test_runner/my_study -q "SELECT COUNT(*) FROM market_data"
"""

import sys
import os
import asyncio
import argparse
from pathlib import Path
from typing import Dict

import pandas as pd

# Add EpochAI to path for provider imports
sys.path.insert(0, os.path.expanduser("~/EpochDev/EpochAI"))

from agent_src.providers import LocalDataProvider, sanitize_name

try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False


def load_dataframes(job_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load all data from a job directory into DataFrames via LocalDataProvider."""
    provider = LocalDataProvider(job_dir)

    async def _load():
        # Market data + orders + positions + account
        dfs = await provider.get_raw_dataframes("")

        # Event markers as DataFrames (provider returns row dicts)
        _, cached_markers = await provider.get_all_event_markers("")
        for key, items in cached_markers.items():
            if items:
                dfs[f"event_marker_{sanitize_name(key)}"] = pd.DataFrame(items)

        return dfs

    return asyncio.run(_load())


def create_connection(dataframes: Dict[str, pd.DataFrame]) -> "duckdb.DuckDBPyConnection":
    """Create DuckDB connection with all DataFrames registered."""
    if not HAS_DUCKDB:
        raise ImportError("duckdb not installed. Run: pip install duckdb")

    conn = duckdb.connect(":memory:")

    for table_name, df in dataframes.items():
        # Sanitize column names
        df_copy = df.copy()
        df_copy.columns = [sanitize_name(c) if isinstance(c, str) else f"col_{c}" for c in df_copy.columns]
        conn.register(table_name, df_copy)

    return conn


def list_tables(dataframes: Dict[str, pd.DataFrame]) -> None:
    """Print available tables."""
    print("Tables:")
    for name, df in dataframes.items():
        print(f"  {name} ({len(df)} rows, {len(df.columns)} cols)")


def show_schema(dataframes: Dict[str, pd.DataFrame], table_name: str) -> None:
    """Print schema for a table."""
    if table_name not in dataframes:
        print(f"Table not found: {table_name}")
        print(f"Available: {list(dataframes.keys())}")
        return

    df = dataframes[table_name]
    print(f"Schema for {table_name}:")
    for col in df.columns:
        dtype = df[col].dtype
        null_count = df[col].isna().sum()
        null_pct = 100 * null_count / len(df) if len(df) > 0 else 0
        sanitized = sanitize_name(col) if isinstance(col, str) else f"col_{col}"
        print(f"  {sanitized}: {dtype} (nulls: {null_count}/{len(df)}, {null_pct:.1f}%)")


def analyze_nulls(dataframes: Dict[str, pd.DataFrame]) -> None:
    """Analyze null values across all tables."""
    print("Null Analysis:")
    print("=" * 70)

    for table_name, df in dataframes.items():
        if len(df) == 0:
            continue

        null_cols = []
        for col in df.columns:
            null_count = df[col].isna().sum()
            if null_count > 0:
                null_pct = 100 * null_count / len(df)
                sanitized = sanitize_name(col) if isinstance(col, str) else f"col_{col}"
                null_cols.append((sanitized, null_count, null_pct))

        if null_cols:
            print(f"\n{table_name} ({len(df)} rows):")
            # Sort by null percentage descending
            null_cols.sort(key=lambda x: x[2], reverse=True)
            for col, count, pct in null_cols:
                print(f"  {col}: {count} nulls ({pct:.1f}%)")


def execute_query(conn: "duckdb.DuckDBPyConnection", sql: str, limit: int = 1000) -> pd.DataFrame:
    """Execute SQL query."""
    sql_upper = sql.upper()
    if "LIMIT" not in sql_upper and not sql_upper.startswith("SHOW") and not sql_upper.startswith("DESCRIBE"):
        sql = f"SELECT * FROM ({sql}) AS _q LIMIT {limit}"
    return conn.execute(sql).df()


def interactive_mode(dataframes: Dict[str, pd.DataFrame]) -> None:
    """Interactive SQL REPL."""
    conn = create_connection(dataframes)

    print("\nInteractive SQL Mode")
    print("Commands: .tables, .schema <table>, .nulls, .quit")
    print("")

    try:
        while True:
            try:
                query = input("sql> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break

            if not query:
                continue

            if query == ".quit":
                break
            elif query == ".tables":
                list_tables(dataframes)
            elif query.startswith(".schema"):
                parts = query.split()
                if len(parts) > 1:
                    show_schema(dataframes, parts[1])
                else:
                    print("Usage: .schema <table>")
            elif query == ".nulls":
                analyze_nulls(dataframes)
            else:
                try:
                    result = execute_query(conn, query)
                    print(result.to_string())
                    print(f"({len(result)} rows)")
                except Exception as e:
                    print(f"Error: {e}")
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("job_folder", type=Path, help="Job folder path")
    parser.add_argument("--tables", action="store_true", help="List available tables")
    parser.add_argument("--schema", type=str, metavar="TABLE", help="Show schema for table")
    parser.add_argument("--query", "-q", type=str, help="Execute SQL query")
    parser.add_argument("--nulls", action="store_true", help="Analyze null values")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive SQL mode")
    args = parser.parse_args()

    if not args.job_folder.exists():
        print(f"Error: Directory not found: {args.job_folder}")
        sys.exit(1)

    dataframes = load_dataframes(args.job_folder)

    if not dataframes:
        print(f"No data found in {args.job_folder}")
        sys.exit(1)

    if args.tables:
        list_tables(dataframes)
    elif args.schema:
        show_schema(dataframes, args.schema)
    elif args.nulls:
        analyze_nulls(dataframes)
    elif args.query:
        conn = create_connection(dataframes)
        try:
            result = execute_query(conn, args.query)
            print(result.to_string())
            print(f"({len(result)} rows)")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            conn.close()
    elif args.interactive:
        interactive_mode(dataframes)
    else:
        # Default: show tables
        list_tables(dataframes)


if __name__ == "__main__":
    main()
