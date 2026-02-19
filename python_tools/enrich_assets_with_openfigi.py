#!/usr/bin/env python3
"""
Enrich asset metadata with sector/industry data using Polygon + OpenFIGI.

Flow:
1. Load existing assets from docs/assets.json
2. For stocks missing sector/industry, fetch composite_figi from Polygon
3. Query OpenFIGI with those FIGIs to get classification data
4. Update assets and save to new file

Usage:
    python scripts/enrich_assets_with_openfigi.py --polygon-key YOUR_KEY --openfigi-key YOUR_KEY

Note: OpenFIGI free tier allows 25 req/min without key, higher with key.
      Polygon allows 5 req/min on free tier.
"""

import argparse
import json
import time
import os
from pathlib import Path

try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    exit(1)


POLYGON_BASE_URL = "https://api.polygon.io"
OPENFIGI_BASE_URL = "https://api.openfigi.com/v3"

# Rate limiting
POLYGON_DELAY = 0.25  # 4 req/sec with buffer
OPENFIGI_BATCH_SIZE = 100  # OpenFIGI allows 100 items per batch request
OPENFIGI_DELAY = 0.5  # Delay between batches


def fetch_polygon_ticker_details(ticker: str, api_key: str) -> dict:
    """Fetch ticker details from Polygon to get composite_figi and SIC code."""
    url = f"{POLYGON_BASE_URL}/v3/reference/tickers/{ticker}"
    params = {"apiKey": api_key}

    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("results", {})
        elif resp.status_code == 429:
            print(f"  Rate limited on {ticker}, waiting...")
            time.sleep(60)
            return fetch_polygon_ticker_details(ticker, api_key)
        else:
            return {}
    except Exception as e:
        print(f"  Error fetching {ticker}: {e}")
        return {}


def batch_query_openfigi(figis: list, api_key: str = None) -> dict:
    """
    Query OpenFIGI for a batch of FIGIs.
    Returns dict mapping FIGI -> result data.
    """
    url = f"{OPENFIGI_BASE_URL}/mapping"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-OPENFIGI-APIKEY"] = api_key

    # Build request body - query by ID_BB_GLOBAL (composite FIGI)
    jobs = [{"idType": "ID_BB_GLOBAL", "idValue": figi} for figi in figis]

    try:
        resp = requests.post(url, headers=headers, json=jobs, timeout=30)
        if resp.status_code == 200:
            results = resp.json()
            figi_to_data = {}
            for i, result in enumerate(results):
                if "data" in result and result["data"]:
                    figi_to_data[figis[i]] = result["data"][0]
            return figi_to_data
        elif resp.status_code == 429:
            print("  OpenFIGI rate limited, waiting 60s...")
            time.sleep(60)
            return batch_query_openfigi(figis, api_key)
        else:
            print(f"  OpenFIGI error: {resp.status_code} - {resp.text[:200]}")
            return {}
    except Exception as e:
        print(f"  OpenFIGI request error: {e}")
        return {}


def map_sic_to_sector(sic_code: str) -> tuple:
    """
    Map SIC code to GICS-style sector and industry.
    Returns (sector, industry) tuple.
    """
    if not sic_code:
        return None, None

    try:
        sic = int(sic_code)
    except:
        return None, None

    # SIC to Sector mapping (simplified GICS-style)
    if 100 <= sic <= 999:
        return "Materials", "Agriculture"
    elif 1000 <= sic <= 1499:
        return "Energy", "Mining & Extraction"
    elif 1500 <= sic <= 1799:
        return "Industrials", "Construction"
    elif 2000 <= sic <= 2099:
        return "Consumer Staples", "Food Products"
    elif 2100 <= sic <= 2199:
        return "Consumer Staples", "Tobacco"
    elif 2200 <= sic <= 2399:
        return "Consumer Discretionary", "Textiles & Apparel"
    elif 2400 <= sic <= 2599:
        return "Materials", "Wood & Paper Products"
    elif 2600 <= sic <= 2799:
        return "Materials", "Paper & Publishing"
    elif 2800 <= sic <= 2899:
        return "Materials", "Chemicals"
    elif 2900 <= sic <= 2999:
        return "Energy", "Oil & Gas Refining"
    elif 3000 <= sic <= 3099:
        return "Consumer Discretionary", "Rubber & Plastics"
    elif 3100 <= sic <= 3199:
        return "Consumer Discretionary", "Leather Products"
    elif 3200 <= sic <= 3299:
        return "Materials", "Glass & Concrete"
    elif 3300 <= sic <= 3399:
        return "Materials", "Primary Metals"
    elif 3400 <= sic <= 3499:
        return "Industrials", "Fabricated Metal Products"
    elif 3500 <= sic <= 3599:
        return "Industrials", "Industrial Machinery"
    elif 3600 <= sic <= 3699:
        return "Technology", "Electronic Equipment"
    elif 3700 <= sic <= 3799:
        return "Consumer Discretionary", "Transportation Equipment"
    elif 3800 <= sic <= 3899:
        return "Healthcare", "Medical Instruments"
    elif 3900 <= sic <= 3999:
        return "Consumer Discretionary", "Miscellaneous Manufacturing"
    elif 4000 <= sic <= 4799:
        return "Industrials", "Transportation"
    elif 4800 <= sic <= 4899:
        return "Communication Services", "Telecommunications"
    elif 4900 <= sic <= 4999:
        return "Utilities", "Electric & Gas Utilities"
    elif 5000 <= sic <= 5199:
        return "Consumer Discretionary", "Wholesale Trade"
    elif 5200 <= sic <= 5999:
        return "Consumer Discretionary", "Retail Trade"
    elif 6000 <= sic <= 6199:
        return "Financials", "Banking"
    elif 6200 <= sic <= 6299:
        return "Financials", "Securities & Investments"
    elif 6300 <= sic <= 6499:
        return "Financials", "Insurance"
    elif 6500 <= sic <= 6599:
        return "Real Estate", "Real Estate"
    elif 6700 <= sic <= 6799:
        return "Financials", "Investment Offices"
    elif 7000 <= sic <= 7099:
        return "Consumer Discretionary", "Hotels & Lodging"
    elif 7200 <= sic <= 7299:
        return "Consumer Discretionary", "Personal Services"
    elif 7300 <= sic <= 7399:
        return "Industrials", "Business Services"
    elif 7370 <= sic <= 7379:
        return "Technology", "Software & IT Services"
    elif 7500 <= sic <= 7599:
        return "Consumer Discretionary", "Auto Services"
    elif 7800 <= sic <= 7899:
        return "Communication Services", "Entertainment"
    elif 7900 <= sic <= 7999:
        return "Consumer Discretionary", "Recreation Services"
    elif 8000 <= sic <= 8099:
        return "Healthcare", "Healthcare Services"
    elif 8100 <= sic <= 8199:
        return "Industrials", "Legal Services"
    elif 8200 <= sic <= 8299:
        return "Consumer Discretionary", "Education Services"
    elif 8300 <= sic <= 8399:
        return "Healthcare", "Social Services"
    elif 8700 <= sic <= 8799:
        return "Industrials", "Engineering & Accounting"
    elif 8900 <= sic <= 8999:
        return "Industrials", "Miscellaneous Services"
    else:
        return None, None


def main():
    parser = argparse.ArgumentParser(description="Enrich assets with OpenFIGI data")
    parser.add_argument("--polygon-key", required=True, help="Polygon API key")
    parser.add_argument("--openfigi-key", help="OpenFIGI API key (optional, increases rate limits)")
    parser.add_argument("--input", default="docs/assets.json", help="Input assets file")
    parser.add_argument("--output", default="docs/assets_enriched.json", help="Output assets file")
    parser.add_argument("--limit", type=int, help="Limit number of assets to process (for testing)")
    parser.add_argument("--only-missing", action="store_true", help="Only process assets with 'Others' or empty sector")
    args = parser.parse_args()

    # Load existing assets
    print(f"Loading assets from {args.input}...")
    with open(args.input) as f:
        data = json.load(f)

    assets = data["items"]
    total_items = data["total_items"]

    # Filter to stocks
    stocks = [a for a in assets if a.get("asset_class") == "Stocks"]
    print(f"Found {len(stocks)} stocks out of {total_items} total assets")

    # Filter to only missing if requested
    if args.only_missing:
        stocks = [a for a in stocks if a.get("sector") in ["Others", "", None] or a.get("industry") in ["Others", "", None]]
        print(f"Filtered to {len(stocks)} stocks with missing sector/industry")

    # Apply limit if specified
    if args.limit:
        stocks = stocks[:args.limit]
        print(f"Limited to {len(stocks)} stocks for processing")

    # Build lookup for updating
    asset_lookup = {a["id"]: a for a in assets}

    # Step 1: Fetch composite_figi from Polygon for each stock
    print("\n--- Step 1: Fetching FIGIs from Polygon ---")
    ticker_to_figi = {}
    ticker_to_sic = {}

    for i, stock in enumerate(stocks):
        ticker = stock.get("ticker")
        if not ticker:
            continue

        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{len(stocks)}")

        details = fetch_polygon_ticker_details(ticker, args.polygon_key)
        if details:
            figi = details.get("composite_figi")
            sic = details.get("sic_code")
            if figi:
                ticker_to_figi[ticker] = figi
            if sic:
                ticker_to_sic[ticker] = sic

        time.sleep(POLYGON_DELAY)

    print(f"\nCollected {len(ticker_to_figi)} FIGIs and {len(ticker_to_sic)} SIC codes from Polygon")

    # Step 2: Query OpenFIGI in batches
    print("\n--- Step 2: Querying OpenFIGI ---")
    figi_list = list(ticker_to_figi.values())
    figi_to_data = {}

    for i in range(0, len(figi_list), OPENFIGI_BATCH_SIZE):
        batch = figi_list[i:i + OPENFIGI_BATCH_SIZE]
        print(f"  Batch {i//OPENFIGI_BATCH_SIZE + 1}: querying {len(batch)} FIGIs...")

        batch_results = batch_query_openfigi(batch, args.openfigi_key)
        figi_to_data.update(batch_results)

        time.sleep(OPENFIGI_DELAY)

    print(f"\nReceived data for {len(figi_to_data)} FIGIs from OpenFIGI")

    # Step 3: Update assets
    print("\n--- Step 3: Updating assets ---")
    updated_count = 0

    # Reverse lookup: FIGI -> ticker
    figi_to_ticker = {v: k for k, v in ticker_to_figi.items()}

    for stock in stocks:
        ticker = stock.get("ticker")
        asset_id = stock.get("id")

        if not ticker or asset_id not in asset_lookup:
            continue

        asset = asset_lookup[asset_id]
        updated = False

        # Try SIC code mapping first (more reliable for sector)
        sic = ticker_to_sic.get(ticker)
        if sic:
            sector, industry = map_sic_to_sector(sic)
            if sector and asset.get("sector") in ["Others", "", None]:
                asset["sector"] = sector
                updated = True
            if industry and asset.get("industry") in ["Others", "", None]:
                asset["industry"] = industry
                updated = True
            # Store SIC code
            asset["sic_code"] = sic

        # Store FIGI if we have it
        figi = ticker_to_figi.get(ticker)
        if figi:
            asset["composite_figi"] = figi

            # Check OpenFIGI data (for any additional fields)
            openfigi_data = figi_to_data.get(figi, {})
            if openfigi_data:
                # OpenFIGI marketSector is security type, not business sector
                # But we can store it for reference
                if openfigi_data.get("marketSector"):
                    asset["openfigi_market_sector"] = openfigi_data["marketSector"]
                if openfigi_data.get("securityType"):
                    asset["security_type"] = openfigi_data["securityType"]

        if updated:
            updated_count += 1

    print(f"Updated {updated_count} assets with new sector/industry data")

    # Step 4: Save enriched assets
    print(f"\n--- Step 4: Saving to {args.output} ---")
    output_data = {
        "items": assets,
        "total_items": total_items
    }

    with open(args.output, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"Done! Enriched assets saved to {args.output}")

    # Summary stats
    print("\n--- Summary ---")
    stocks_after = [a for a in assets if a.get("asset_class") == "Stocks"]
    sectors_after = {}
    for s in stocks_after:
        sec = s.get("sector", "Unknown")
        sectors_after[sec] = sectors_after.get(sec, 0) + 1

    print("Sector distribution after enrichment:")
    for sec, count in sorted(sectors_after.items(), key=lambda x: -x[1])[:15]:
        print(f"  {sec}: {count}")


if __name__ == "__main__":
    main()
