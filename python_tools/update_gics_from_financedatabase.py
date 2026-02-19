#!/usr/bin/env python3
"""
Update asset specifications with proper GICS sector/industry from FinanceDatabase.

FinanceDatabase (https://github.com/JerBouma/FinanceDatabase) provides GICS-like
classifications for 300K+ symbols, community-curated to match official GICS standards.

Usage:
    python python_tools/update_gics_from_financedatabase.py --input <parquet> --output <parquet>
    python python_tools/update_gics_from_financedatabase.py --compare-only  # Just show comparison

Requirements:
    pip install financedatabase pandas pyarrow
"""

import argparse
import sys
from pathlib import Path

try:
    import financedatabase as fd
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install financedatabase pandas pyarrow")
    sys.exit(1)


def load_financedatabase_gics(country: str = "United States") -> pd.DataFrame:
    """Load GICS data from FinanceDatabase."""
    print(f"Loading FinanceDatabase equities for {country}...")
    equities = fd.Equities()
    data = equities.search(country=country)

    # The index is the ticker symbol - reset to make it a column
    data = data.reset_index(names='ticker')

    # Keep only relevant columns
    cols = ['ticker', 'name', 'sector', 'industry', 'industry_group', 'exchange',
            'isin', 'cusip', 'figi', 'composite_figi']
    available_cols = [c for c in cols if c in data.columns]

    print(f"  Loaded {len(data)} equities")
    print(f"  Sectors: {data['sector'].nunique()}")
    print(f"  Industries: {data['industry'].nunique()}")

    return data[available_cols]


def load_current_assets(parquet_path: str) -> pd.DataFrame:
    """Load current asset specifications from parquet."""
    print(f"Loading current assets from {parquet_path}...")
    df = pd.read_parquet(parquet_path)
    print(f"  Loaded {len(df)} assets")
    return df


def compare_classifications(current_df: pd.DataFrame, gics_df: pd.DataFrame):
    """Compare current classifications with GICS data."""

    # Filter to stocks only
    stocks = current_df[current_df['asset_class'] == 'Stocks'].copy()

    print("\n" + "=" * 70)
    print("COMPARISON: Current vs FinanceDatabase GICS")
    print("=" * 70)

    # Merge on ticker
    merged = stocks.merge(
        gics_df[['ticker', 'sector', 'industry']],
        on='ticker',
        how='left',
        suffixes=('_current', '_gics')
    )

    # Stats
    has_gics = merged['sector_gics'].notna().sum()
    total = len(merged)

    print(f"\nMatch rate: {has_gics}/{total} ({100*has_gics/total:.1f}%)")

    # Sector comparison
    print("\n--- SECTOR CHANGES ---")
    sector_changes = merged[
        (merged['sector_current'] != merged['sector_gics']) &
        merged['sector_gics'].notna()
    ]

    if len(sector_changes) > 0:
        print(f"Stocks needing sector update: {len(sector_changes)}")

        # Show summary of changes
        change_summary = sector_changes.groupby(['sector_current', 'sector_gics']).size()
        print("\nTop sector migrations:")
        for (old, new), count in change_summary.nlargest(15).items():
            print(f"  {old or 'Empty'} -> {new}: {count} stocks")
    else:
        print("No sector changes needed")

    # Industry comparison
    print("\n--- INDUSTRY CHANGES ---")
    industry_changes = merged[
        (merged['industry_current'] != merged['industry_gics']) &
        merged['industry_gics'].notna()
    ]

    if len(industry_changes) > 0:
        print(f"Stocks needing industry update: {len(industry_changes)}")

        # Show current vs GICS industries
        print("\nCurrent unique industries:", merged['industry_current'].nunique())
        print("GICS unique industries:", merged['industry_gics'].nunique())

    # Missing GICS data
    missing = merged[merged['sector_gics'].isna()]
    if len(missing) > 0:
        print(f"\n--- MISSING FROM FINANCEDATABASE ({len(missing)} stocks) ---")
        print("Sample tickers without GICS data:")
        for ticker in missing['ticker'].head(20).tolist():
            print(f"  {ticker}")

    return merged


def update_assets(current_df: pd.DataFrame, gics_df: pd.DataFrame) -> pd.DataFrame:
    """Update asset dataframe with GICS classifications."""

    # Create ticker lookup from GICS data
    gics_lookup = gics_df.set_index('ticker')[['sector', 'industry']].to_dict('index')

    updated = current_df.copy()
    updates = {'sector': 0, 'industry': 0}

    for idx, row in updated.iterrows():
        if row.get('asset_class') != 'Stocks':
            continue

        ticker = row.get('ticker')
        if ticker not in gics_lookup:
            continue

        gics_data = gics_lookup[ticker]

        # Update sector if GICS has data
        if pd.notna(gics_data.get('sector')):
            old_sector = row.get('sector', '')
            new_sector = gics_data['sector']
            if old_sector != new_sector:
                updated.at[idx, 'sector'] = new_sector
                updates['sector'] += 1

        # Update industry if GICS has data
        if pd.notna(gics_data.get('industry')):
            old_industry = row.get('industry', '')
            new_industry = gics_data['industry']
            if old_industry != new_industry:
                updated.at[idx, 'industry'] = new_industry
                updates['industry'] += 1

    print(f"\nUpdated {updates['sector']} sector values")
    print(f"Updated {updates['industry']} industry values")

    return updated


def main():
    parser = argparse.ArgumentParser(
        description="Update asset GICS classifications from FinanceDatabase"
    )
    parser.add_argument(
        "--input",
        default="/home/adesola/EpochDev/EpochBackend/files/asset_specs.parquet.gzip",
        help="Input parquet file"
    )
    parser.add_argument(
        "--output",
        help="Output parquet file (default: overwrite input)"
    )
    parser.add_argument(
        "--compare-only",
        action="store_true",
        help="Only show comparison, don't update"
    )
    parser.add_argument(
        "--country",
        default="United States",
        help="Country filter for FinanceDatabase"
    )

    args = parser.parse_args()

    # Load GICS data
    gics_df = load_financedatabase_gics(args.country)

    # Load current assets
    current_df = load_current_assets(args.input)

    # Compare
    merged = compare_classifications(current_df, gics_df)

    if args.compare_only:
        print("\n[Compare only mode - no changes written]")
        return

    # Update
    print("\n" + "=" * 70)
    print("UPDATING CLASSIFICATIONS")
    print("=" * 70)

    updated_df = update_assets(current_df, gics_df)

    # Save
    output_path = args.output or args.input
    print(f"\nSaving to {output_path}...")

    # Write as gzip-compressed parquet
    updated_df.to_parquet(output_path, compression='gzip', index=False)
    print("Done!")

    # Show final stats
    stocks = updated_df[updated_df['asset_class'] == 'Stocks']
    print(f"\nFinal sector distribution:")
    for sector, count in stocks['sector'].value_counts().head(15).items():
        print(f"  {sector}: {count}")


if __name__ == "__main__":
    main()
