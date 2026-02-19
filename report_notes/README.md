# Report Notes

Research crawler for collecting financial resources. See `CLAUDE.md` for full documentation.

## Quick Start

```bash
/research-topic "seasonality in financial assets"
```

## Structure

```
report_notes/
├── CLAUDE.md           # Full documentation
├── scripts/
│   ├── init_topic.py   # Initialize topic folder
│   ├── add_source.py   # Add crawled source
│   ├── add_chart.py    # Register chart metadata
│   ├── status.py       # Show topic status
│   └── quantpedia_login.py
└── <topic_slug>/       # Research topics
    ├── manifest.json
    ├── sources/
    ├── images/
    └── tables/
```
