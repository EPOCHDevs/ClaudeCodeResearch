# Report Notes - Research Crawler

Raw resource collection tool for financial research topics. Crawls articles, captures charts, extracts tables - no summarization.

---

## Quick Start

```bash
# Activate environment
cd /home/adesola/EpochDev/ClaudeCodeResearch
source .venv/bin/activate
```

**To research a topic:**
```
/research-topic "FX macro correlations commodity currencies"
```

---

## Exa Crawler Script (Primary Tool)

**Location:** `report_notes/scripts/exa_crawler.py`

Uses optimized Exa API parameters for maximum content extraction:

```json
{
  "text": {
    "maxCharacters": 50000,
    "includeHtmlTags": true
  },
  "extras": {
    "imageLinks": 30,
    "links": 20
  },
  "livecrawl": "preferred"
}
```

### Commands

```bash
# Search and crawl with full content + images
python report_notes/scripts/exa_crawler.py search "USDCAD oil correlation" --num 15 -o results.json

# Crawl single URL
python report_notes/scripts/exa_crawler.py crawl "https://example.com/article" --json

# Crawl URLs into topic folder
python report_notes/scripts/exa_crawler.py topic <topic_slug> <url1> <url2> ...
```

### What Gets Extracted

| Field | Description |
|-------|-------------|
| `text` | Full HTML content with `<h2>`, `<p>`, `<table>`, `<a>` tags |
| `imageLinks` | All image URLs (charts, figures, diagrams) |
| `links` | Outbound URLs for follow-up research |
| `image` | Main page image |
| `author` | Article author |

### Automatic Chart Download

The script automatically:
1. Extracts all image URLs from crawled content
2. Filters out logos, icons, banners (keeps charts)
3. Downloads images to `sources/<domain>/<source>/charts/`
4. Records image URLs in frontmatter (even if download fails)

---

## How It Works

### 1. Search Phase
Uses Exa search API with full content retrieval:
- **Tier 1 (quant sources):** quantpedia.com, ssrn.com, nber.org, arxiv.org
- **Tier 2 (market data):** barchart.com, macrotrends.net, tradingview.com
- **Tier 3 (broker research):** forex.com, oanda.com, acy.com
- **Tier 4 (educational):** investopedia.com, babypips.com

### 2. Crawl Phase
For each URL:
- Full page content with HTML tags preserved
- Image URLs extracted via `extras.imageLinks`
- Outbound links captured for follow-up

### 3. Download Phase
Charts are automatically downloaded:
- Filters logos/icons from real charts
- Saves to organized folder structure
- Records in manifest.json

### 4. Organize Phase
Categorize by source domain into structured folders.

---

## Output Structure

```
report_notes/
├── <topic_slug>/
│   ├── manifest.json
│   ├── sources/
│   │   ├── quantpedia/
│   │   │   ├── 001_<title>.md
│   │   │   └── 001_<title>/
│   │   │       └── charts/
│   │   │           ├── chart_01.png
│   │   │           └── chart_02.jpg
│   │   ├── academic/
│   │   ├── broker_research/
│   │   ├── market_data/
│   │   └── misc/
│   └── images/
│       └── chart_index.json
```

---

## Source Markdown Format

Each source saved with comprehensive frontmatter:

```yaml
---
url: https://forex.com/analysis/usdcad-oil
title: USDCAD Oil Correlation Analysis
domain: broker_research
crawled_at: 2026-02-04T01:00:00+00:00
source: exa_search
author: Market Analyst
main_image: https://forex.com/images/main.jpg
chart_count: 5
image_links:
  - https://forex.com/charts/usdcad_vs_wti.png
  - https://forex.com/charts/correlation_heatmap.png
outbound_links:
  - https://forex.com/related-article
---

<h2>USDCAD and Oil Price Correlation</h2>
<p>The correlation between USD/CAD and crude oil...</p>
<table>
  <tr><td>Correlation</td><td>0.75-0.80</td></tr>
</table>
```

---

## Manifest Format

```json
{
  "topic": "FX macro correlations",
  "slug": "fx_macro_correlations_commodity_currencies",
  "created": "2026-02-04T00:51:48Z",
  "sources": [
    {
      "url": "https://...",
      "domain": "broker_research",
      "title": "USDCAD Oil Correlation",
      "crawled_at": "2026-02-04T01:09:10+00:00",
      "file": "sources/broker_research/001_usdcad_oil.md",
      "charts": [
        "sources/broker_research/001_usdcad_oil/charts/chart_01.png",
        "sources/broker_research/001_usdcad_oil/charts/chart_02.png"
      ],
      "tables": 0
    }
  ],
  "stats": {
    "total_sources": 15,
    "total_charts": 62
  }
}
```

---

## Domain Categories

| Domain | Folder | Content Type |
|--------|--------|--------------|
| quantpedia.com | `quantpedia/` | Strategy papers, backtests |
| ssrn.com, nber.org, arxiv.org | `academic/` | Academic papers |
| forex.com, oanda.com | `broker_research/` | Broker analysis |
| barchart.com, tradingview.com | `market_data/` | Charts, data |
| investopedia.com, babypips.com | `educational/` | Tutorials |
| Other | `misc/` | Everything else |

---

## Exa API Reference

### Direct API (Used by exa_crawler.py)

```python
# Optimal crawl parameters
payload = {
    "urls": ["https://example.com"],
    "text": {
        "maxCharacters": 50000,
        "includeHtmlTags": True,  # Preserves HTML structure
    },
    "extras": {
        "imageLinks": 30,  # Extracts chart/image URLs
        "links": 20,       # Extracts outbound links
    },
    "livecrawl": "preferred",
    "livecrawlTimeout": 15000,
}
```

### MCP Tools (Fallback)

```python
# Basic search (limited parameters)
mcp__exa__web_search_exa(
    query="seasonality financial assets",
    numResults=10
)

# Crawl (no imageLinks/includeHtmlTags exposed)
mcp__exa__crawling_exa(
    url="https://...",
    maxCharacters=50000
)
```

**Note:** The MCP tools don't expose `includeHtmlTags` or `extras.imageLinks`. Use `exa_crawler.py` for full extraction.

---

## Python Usage

```python
import sys
sys.path.insert(0, 'report_notes/scripts')
from exa_crawler import crawl_url, search_and_crawl, save_source_to_topic
from pathlib import Path

# Crawl single URL
result = crawl_url("https://example.com/article")
print(f"Images: {len(result['imageLinks'])}")
print(f"Content: {result['text'][:500]}")

# Search and crawl
results = search_and_crawl(
    "USDCAD oil correlation",
    num_results=10,
    include_domains=["forex.com", "investopedia.com"]
)

# Save to topic
topic_dir = Path("report_notes/fx_correlations")
for r in results:
    save_source_to_topic(topic_dir, r, download_images=True)
```

---

## Manual Commands

### List Topic Folders
```bash
ls -la report_notes/*/manifest.json
```

### View Topic Stats
```bash
python -c "
import json
m = json.load(open('report_notes/<topic>/manifest.json'))
print(f'Sources: {m[\"stats\"][\"total_sources\"]}')
print(f'Charts: {m[\"stats\"][\"total_charts\"]}')
"
```

### List Downloaded Charts
```bash
find report_notes/<topic> -name "chart_*.png" -o -name "chart_*.jpg"
```

### Open Charts Folder
```bash
xdg-open report_notes/<topic>/sources/
```

---

## Tips

1. **Use exa_crawler.py** - Not the MCP tools - for full HTML + image extraction
2. **Charts download automatically** - Script filters logos from real charts
3. **Image URLs always saved** - In frontmatter even if download fails
4. **HTML preserved** - Tables, links, formatting all retained
5. **Check manifest.json** - Track progress and chart counts
6. **Search broadly first** - Then narrow with domain-specific queries
