---
name: fred-search
description: Search FRED (Federal Reserve Economic Data) for series by keyword, tag, or category. Returns series IDs, titles, date ranges, and frequencies.
allowed-tools: WebFetch, Bash, Read
argument-hint: "<search query>"
---

# FRED Search

Search the FRED API for economic data series. Use this when you need to find FRED series IDs for use in `economic_indicators(series_id='...')` transforms.

## API Key

The FRED API requires a free API key. Set it in `.env`:

```
FRED_API_KEY=your_key_here
```

Get one at: https://fred.stlouisfed.org/docs/api/api_key.html

## How to Search

Given the user's query (e.g., "central bank rate australia", "GDP growth mexico quarterly"), perform the search using the FRED API.

### Step 1: Load API Key

```bash
source /home/adesola/EpochDev/ClaudeCodeResearch/.env 2>/dev/null
echo $FRED_API_KEY
```

If no key is set, use the default demo key: `DEMO_KEY` (rate-limited but functional).

### Step 2: Search FRED

Use WebFetch to call the FRED API. The main endpoints:

#### Series Search (primary)
```
https://api.stlouisfed.org/fred/series/search?search_text=<QUERY>&api_key=<KEY>&file_type=json&limit=20&order_by=popularity
```

#### Series Search by Tags
```
https://api.stlouisfed.org/fred/tags/series?tag_names=<TAG1>;<TAG2>&api_key=<KEY>&file_type=json&limit=20
```

#### Get Series Details (when you have a series ID)
```
https://api.stlouisfed.org/fred/series?series_id=<ID>&api_key=<KEY>&file_type=json
```

#### Get Series Observations (to check date range and values)
```
https://api.stlouisfed.org/fred/series/observations?series_id=<ID>&api_key=<KEY>&file_type=json&sort_order=desc&limit=5
```

### Step 3: Present Results

For each matching series, show:

| Field | Description |
|-------|-------------|
| **Series ID** | The FRED identifier (e.g., `ECBDFR`) |
| **Title** | Full series name |
| **Frequency** | Monthly, Quarterly, Daily, etc. |
| **Date Range** | First observation to last observation |
| **Units** | Percent, Index, Billions, etc. |
| **Source** | Data provider (ECB, OECD, BLS, etc.) |
| **Popularity** | FRED popularity score |

### Step 4: Recommend Best Match

Based on the user's needs, recommend the best series considering:
- **Frequency**: Monthly preferred for `economic_indicators()` (aligns with daily market data via ffill)
- **Date range**: Must cover the study period (typically 2020-2026)
- **Recency**: Prefer actively updated series
- **Source quality**: OECD, central banks, BLS preferred

## Common Search Patterns

| Need | Search Query | Example Series |
|------|-------------|----------------|
| Central bank rate | `"central bank rate <country>"` | IRSTCB01xxM156N |
| Overnight rate | `"overnight interbank rate <country>"` | IRSTCI01xxM156N |
| GDP growth | `"GDP growth <country> quarterly"` | xxxGDPRQPSMEI |
| Inflation CPI | `"consumer price index <country>"` | CPIAUCSL |
| Unemployment | `"unemployment rate <country>"` | UNRATE |
| Interest rate spread | `"yield spread <country>"` | T10Y2Y |

## Usage in EpochScript

Once you find the right series ID, use it as:
```
date, value, revision = economic_indicators(series_id='SERIES_ID')()
filled = ffill(value)
```

## Notes

- FRED has 800,000+ series — search is the fastest way to find what you need
- Series ending in `M156N` are monthly, `Q156N` quarterly
- OECD series (IRSTCB01, IR3TIB01, etc.) have consistent naming across countries
- `order_by=popularity` surfaces the most-used series first
