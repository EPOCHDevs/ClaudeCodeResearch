# Exhibit A Chart Style Guide

How Exhibit A uses specific chart types to convey specific financial insights. This guide is derived from analysis of all 99 Exhibit A reference images and 53 implemented EpochScript definitions.

---

## Design Philosophy

Exhibit A charts follow six core principles:

1. **One chart, one insight** -- Every chart tells exactly one story. No chart combines multiple chart types or tries to show more than 3 series.
2. **Monochromatic blue palette** -- All data uses blue tones (dark navy primary, medium/light blue secondary, gray tertiary). No reds, greens, or rainbow palettes in data series.
3. **Annotation-driven storytelling** -- The most important number is always labeled directly on the chart (endpoint values, bar labels). Readers get the takeaway without reading axes.
4. **Long time horizons** -- Most charts span decades (1950s-present), emphasizing long-term perspective central to advisor communication.
5. **Minimal clutter** -- No gridlines, no dual axes, no complex legends. Clean white background with subtle axis lines.
6. **Paired narrative** -- Every chart has a companion "Key Takeaways" panel with 3 bullet points, making each chart self-contained for client communication.
7. **Summary tables over cards** -- Use `summary_table` for multiple metrics (90% of the time). Cards are reserved for hero metrics or verdicts — maximum 3 per definition.

---

## Dashboard Structure

Each definition produces a single-category dashboard by default. On the UI, each category renders as an accordion of components.

### Component Order (within a category)

1. **Cards** (0-3 max) — hero metric or verdict only
2. **Tables** — `summary_table` for detailed metrics
3. **Charts** — visual evidence (1-3 charts)

### Category Rules

- **Default: 1 category** — keeps everything in a single scroll
- **2 categories only** when there's a genuine narrative split (e.g., "Current State" vs "Historical Context")
- **Never 3+ categories** — consolidate by story, not data type

### Cards vs Summary Tables

| Scenario | Use |
|----------|-----|
| 1 hero number or verdict | Card |
| 2-3 standalone metrics not in any chart | Cards (max 3) |
| 4+ related metrics | `summary_table` |
| Before/after comparison | `summary_table` |
| Multi-asset metric snapshot | `summary_table` |
| Distribution stats (median, p25, p75) | `summary_table` or reference lines |

---

## Chart Type Vocabulary

Exhibit A uses only 5 chart types. No scatter plots, heatmaps, candlesticks, pie charts (one exception), or stacked areas appear in the collection.

| Chart Type | Frequency | Primary Use |
|------------|-----------|-------------|
| **Bar chart** (`xy_bars`) | ~50% | Cross-sectional comparisons, distributions, event counts |
| **Line chart** (`xy_lines`) | ~40% | Time series trends, growth paths, economic indicators |
| **Area chart** (`xy_lines` + `area=True`) | ~7% | Spread visualization, magnitude/streak charts |
| **Labeled lines** (`labeled_lines`) | ~2% | Term structure (yield curve) |
| **Event markers** (`event_marker`) | ~1% | Highlighting specific days on a price chart |

---

## Pattern 1: Cross-Sectional Bar Comparison

**When to use:** Comparing a metric across discrete categories at a point in time.

**Exhibit A examples:**
- YTD asset class returns (11 asset classes ranked by return)
- Country equity performance (10 countries by YTD return)
- Major US index performance (SPY, DIA, QQQ side by side)
- Portfolio stock/bond split metrics (11 allocations from 100/0 to 0/100)

**Visual conventions:**
- Bars sorted by value (highest to lowest) or by natural category order
- `data_labels=True` -- every bar shows its value
- `color_by_value=True` for return charts (green positive, red negative)
- `reference_lines` at 0% for return charts
- `y_axis_format=PercentFormat` for returns, `IntegerFormat` for counts

**EpochScript pattern:** Named series bars (no `label=` parameter). Each `BarSeriesSpec` is a distinct category. Single scalar per series aggregated across the full time range.

```
xy_bars(
    agg=AggregationType.Last,     # Point-in-time snapshot
    data_labels=True,
    color_by_value=True,
    y_axis_format=AxisValueFormat.PercentFormat,
    reference_lines=ReferenceLineSchema(lines=[
        ReferenceLine(value=0.0, color=Color.Gray, dash_style=DashStyle.Dash)
    ]),
    series=BarSeriesSchema(series=[
        BarSeriesSpec(name='S&P 500', color=Color.Blue),
        BarSeriesSpec(name='Dow', color=Color.Gray),
        BarSeriesSpec(name='NASDAQ', color=Color.Cyan)
    ])
)(spy_ytd, dia_ytd, qqq_ytd)
```

**Aggregation choice by information type:**

| Information | Aggregation | Example |
|-------------|-------------|---------|
| Current/latest value | `agg=Last` | YTD returns, current yield |
| Historical average | `agg=Mean` | Average return by month, avg holding period return |
| Event count | `agg=Sum` | Number of pullbacks, ATH count |
| Worst case | `agg=Min` | Bear market max drawdown |
| Best case | `agg=Max` | Bull market max return |

---

## Pattern 2: Labeled Bar Chart (Time-Bucketed)

**When to use:** Aggregating a metric by time period (month, quarter, year, decade).

**Exhibit A examples:**
- Average return by month (12 bars, one per calendar month)
- ATH count by year (one bar per year)
- 1%+ days by decade (one bar per decade)
- Nonfarm payrolls by month (monthly bars with moving average overlay)
- GDP growth by quarter (quarterly bars)

**Visual conventions:**
- X-axis driven by a computed label column
- `x_category_type` matches the time bucket: `Month`, `QuarterYear`, `Exact` (for years/decades)
- `color_by_value=True` common for positive/negative bars
- Reference line at 0% or at the historical average

**EpochScript pattern:** Uses `label=` parameter. The label column must have NaN for non-boundary bars to avoid duplicate entries.

```
# NaN propagation pattern for month-end-only values
nan_flag = monthly_ret / monthly_ret          # 1.0 when valid, NaN when NaN
month_label = month_num * nan_flag            # NaN for non-month-end bars

xy_bars(
    agg=AggregationType.Mean,
    x_category_type=CategoryAxisType.Month,
    color_by_value=True,
    data_labels=True,
    reference_lines=ReferenceLineSchema(lines=[
        ReferenceLine(value=0.0, color=Color.Gray, dash_style=DashStyle.Dash)
    ])
)(monthly_ret, label=month_label)
```

---

## Pattern 3: Bar Chart with Overlay (Return + Drawdown)

**When to use:** Showing two related metrics for the same categories -- typically annual return bars with intra-year drawdown diamond markers.

**Exhibit A examples:**
- 60/40 annual returns with intra-year drawdowns
- Bond annual returns with intra-year declines
- Bitcoin vs asset classes (return bars + drawdown diamonds)
- Nonfarm payrolls (monthly bars + 3-month moving average line)

**Visual conventions:**
- Primary bars for the main metric (returns)
- Diamond markers (`DiamondMarker`) for the secondary metric (drawdowns)
- Overlay series uses `agg=Min` for drawdowns, `agg=Last` for moving averages
- Two-color scheme: blue bars + gray/red diamonds

**EpochScript pattern:**

```
xy_bars(
    agg=AggregationType.Last,
    data_labels=True,
    color_by_value=True,
    series=BarSeriesSchema(series=[
        BarSeriesSpec(name='Annual Return', color=Color.Blue)
    ]),
    overlay_series=OverlaySeriesSchema(series=[
        OverlaySeriesSpec(
            name='Max Intra-Year Drawdown',
            color=Color.Gray,
            agg=AggregationType.Min,
            marker=MarkerSymbol.DiamondMarker
        )
    ])
)(annual_ret, year_label, overlay_values=max_dd)
```

---

## Pattern 4: Time Series Line Chart

**When to use:** Showing how a metric evolves over time. The most common pattern for economic indicators and price levels.

**Exhibit A examples:**
- Treasury yields 2Y/10Y (dual line, short-term and long-term views)
- Consumer sentiment, continued claims, initial claims (single economic line)
- PCE headline vs core, PPI headline vs core (dual line comparison)
- Quits vs hires rate (dual line)
- S&P 500 index level short-term (single price line)
- Major index YTD paths (3 cumulative return lines)

**Visual conventions:**
- Dark blue for primary series, gray/lighter blue for secondary
- Final/current value annotated on the chart
- 1-3 series maximum per chart
- `y_axis_format` matches the data: `PercentFormat` for rates, `DecimalFormat` for levels

**EpochScript pattern:**

```
xy_lines(
    title='Treasury Yields: 2-Year vs 10-Year',
    series=LineSeriesSchema(series=[
        LineSeriesSpec(name='10-Year Yield', color=Color.Blue),
        LineSeriesSpec(name='2-Year Yield', color=Color.Green)
    ])
)(bar_ts, y10_filled, y2_filled)
```

**Sub-variants:**

| Variant | When | Options | Examples |
|---------|------|---------|----------|
| Log scale | Long-term price levels (50+ years) | `log_scale=True` | S&P 500 since 1950, growth of $1 |
| Dashed projection | Actual + forecast | `dash_style=DashStyle.Dash` on forecast series | Fed funds rate + FOMC projection |
| Smooth seasonal | Calendar-year path overlays | `smooth=True`, `x_category_type=DayOfYear` | Average calendar year path |
| Marker dots | Highlighting specific events on price | `marker=MarkerSymbol.CircleMarker` | ATH days, best/worst days |

---

## Pattern 5: Area Fill (Spread / Magnitude)

**When to use:** Emphasizing the magnitude or sign of a spread, or visualizing streaks/gaps.

**Exhibit A examples:**
- Yield curve spread (10Y-2Y): positive blue area, negative red area
- S&P 500 vs international rolling spread: blue area (intl outperforms), gray area (US outperforms)
- Gold vs S&P 500 rolling 3Y spread: single-color filled area
- Days since last 5% pullback: filled area showing gap duration
- Days within 3% of ATH: filled area showing streak duration
- Real GDP level: filled area showing economic size

**Visual conventions:**
- Dual-color area for sign-split spreads (blue positive, red/gray negative)
- Single-color area for magnitude visualization (streaks, levels)
- Reference line at 0% for spread charts

**EpochScript technique -- Dual-color area split:**

```
# Split spread into positive and negative components
spread_pos = spread if spread > 0 else 0.0 / 0.0
spread_neg = spread if spread < 0 else 0.0 / 0.0

xy_lines(
    area=True,
    series=LineSeriesSchema(series=[
        LineSeriesSpec(name='Uninverted', color=Color.Blue),
        LineSeriesSpec(name='Inverted', color=Color.Red)
    ])
)(bar_ts, spread_pos, spread_neg)
```

---

## Pattern 6: Growth-of-$1 Comparison

**When to use:** Comparing cumulative wealth paths under different scenarios or strategies.

**Exhibit A examples:**
- Time in the market: invested all days vs missing best 50/100 days
- Tactical approach: invested all days vs missing worst 50/100 days
- S&P 500 with vs without dividends reinvested
- Impact of bad investing behavior: buy-and-hold vs sell-at-5%-pullback

**Visual conventions:**
- Log scale Y-axis (essential for 50+ year compounding charts)
- 2-3 lines diverging dramatically
- Endpoint values prominently annotated ($413 vs $29 vs $3.5)
- Dark blue for "stay invested" (always the winning strategy)

**EpochScript pattern:**

```
growth_all = cumulative(agg=AggregationType.Product)(1 + daily_ret)

# Zero out worst N days
is_worst50 = nsmallest(n=50)(daily_ret)
ret_skip_worst50 = boolean_select_number(is_worst50, 0, daily_ret)
growth_skip50 = cumulative(agg=AggregationType.Product)(1 + ret_skip_worst50)

xy_lines(
    log_scale=True,
    y_axis_format=AxisValueFormat.MonetaryFormat,
    series=LineSeriesSchema(series=[
        LineSeriesSpec(name='Invested All Days', color=Color.Blue),
        LineSeriesSpec(name='Missed Worst 50 Days', color=Color.Gray)
    ])
)(bar_ts, growth_all, growth_skip50)
```

---

## Pattern 7: Recession/Event Band Shading

**When to use:** Overlaying gray bands on a price or economic chart to show recession periods.

**Exhibit A examples:**
- S&P 500 with recession periods
- Real GDP with recessions
- U.S. recessions since 1854

**Visual conventions:**
- Light gray vertical bands for recession periods
- Primary data line in dark blue overlaid on top
- Log scale for long-term price charts

**EpochScript technique:**

```
# Use RecessionProb > 0.5 as recession indicator
rec_obs, rec_val, rec_rev = common_economic_indicators(
    category=MacroEconomicsIndicator.RecessionProb
)()
rec_filled = ffill(rec_val)
is_recession = rec_filled > 0.5
recession_band = 1000000.0 if is_recession else 0.0 / 0.0

xy_lines(
    log_scale=True,
    series=LineSeriesSchema(series=[
        LineSeriesSpec(name='S&P 500', color=Color.Blue),
        LineSeriesSpec(
            name='Recession',
            color=Color.LightGray,
            is_band=True        # renders as shaded background band
        )
    ])
)(bar_ts, spy_c, recession_band)
```

---

## Pattern 8: Presidential/Political Coloring

**When to use:** Showing market performance segmented by political party or administration.

**Exhibit A examples:**
- S&P 500 price during presidential terms (blue Democrats, red Republicans)
- S&P 500 annualized by presidential term

**Visual conventions:**
- Dark blue for Democratic administrations
- Red/gray for Republican administrations
- Log scale for long-term price
- Both parties show strong growth (the point: politics doesn't matter)

**EpochScript technique:**

```
# Alternate party-colored area segments using NaN masking
dem_price = spy_c if is_democrat else 0.0 / 0.0
rep_price = spy_c if is_republican else 0.0 / 0.0

xy_lines(
    log_scale=True, area=True,
    series=LineSeriesSchema(series=[
        LineSeriesSpec(name='Democrat', color=Color.Blue),
        LineSeriesSpec(name='Republican', color=Color.Red)
    ])
)(bar_ts, dem_price, rep_price)
```

---

## Pattern 9: Bear/Bull Market Comparison

**When to use:** Showing returns or duration across distinct market cycles.

**Exhibit A examples:**
- Returns during bear markets (negative bars + average reference line)
- Returns during bull markets (positive bars + average reference line)
- Length of bull markets (duration bars + average reference line)
- Length of bear markets (duration bars + average reference line)
- Historic bull and bear markets (alternating positive/negative bars)

**Visual conventions:**
- One bar per market cycle
- Dashed horizontal reference line at the historical average
- Current/ongoing cycle highlighted in a different shade
- Data labels on every bar

**EpochScript technique -- Dynamic cycle detection:**

```
running_max = cumulative(agg=AggregationType.Max)(spy_c)
drawdown = (spy_c - running_max) / running_max

# Bear market: enter at -20% drawdown, exit at +20% rally from trough
bear_entry = crossunder(drawdown, -0.20)
trough = cumulative(agg=AggregationType.Min)(spy_c, bear_entry)
rally = (spy_c - trough) / trough
bear_exit = crossover(rally, 0.20)
in_bear = hold_until(bear_entry, bear_exit)
```

---

## Pattern 10: Pullback Counting / Debounce

**When to use:** Counting discrete episodes (pullbacks, corrections) per year or across portfolio variants.

**Exhibit A examples:**
- 5% pullbacks annually (bar per year, count of episodes)
- 5% / 10% pullbacks by stock/bond splits (bar per allocation)

**EpochScript technique -- Rising-edge debounce:**

```
crossed_5 = crossunder(drawdown, -0.05)
recovered = crossover(drawdown, -0.01)
in_pullback = hold_until(crossed_5, recovered)
in_pullback_num = 1.0 if in_pullback else 0.0
pullback_entry = crossover(in_pullback_num, 0.5)    # rising edge = new episode
pullback_flag = 1.0 if pullback_entry else 0.0
```

---

## Color Palette Reference

| Color | EpochScript | Usage Convention |
|-------|-------------|-----------------|
| Dark blue | `Color.Blue` | Primary series (ALWAYS) |
| Gray | `Color.Gray` | Secondary series, reference lines, historical averages |
| Red | `Color.Red` | Negative/bearish: inverted yield curve, worst days, Republican |
| Green | `Color.Green` | Positive/bullish (rare): short-term yields |
| Orange | `Color.Orange` | Tertiary: commodities, Bitcoin, Core PCE |
| Cyan | `Color.Cyan` | NASDAQ, Growth ETFs |
| Sky | `Color.Sky` | Bonds, projections |
| Purple | `Color.Purple` | Mid Cap, Core PPI |
| Yellow | `Color.Yellow` | Gold |
| Silver | `Color.Silver` | T-Bills, current period highlight |

**Rule:** Blue is always first. Never use red/green for primary data. Reserve red for explicitly negative data (inversions, losses, bear markets).

---

## Common Options Reference

| Option | Value | When to Use |
|--------|-------|-------------|
| `data_labels` | `True` | Bar charts (always), line chart endpoints |
| `color_by_value` | `True` | Return bars where sign matters |
| `log_scale` | `True` | Price levels spanning 50+ years, growth-of-$1 |
| `area` | `True` | Spread visualization, magnitude/streak charts |
| `smooth` | `True` | Calendar year path overlays (DayOfYear x-axis) |
| `reference_lines` | `value=0.0` | Any chart with positive/negative values |
| `reference_lines` | `value=avg` | Bar charts comparing to historical average |

---

## Axis Format Reference

| Format | When |
|--------|------|
| `PercentFormat` | Returns, rates, spreads, YoY changes |
| `DecimalFormat` | Yields, index levels, ratios |
| `IntegerFormat` | Event counts, pullback counts, ATH counts |
| `MonetaryFormat` | Growth of $1, GDP in trillions, dollar values |

---

## Data Source Decision Tree

```
What are you charting?
├── Stock/ETF prices or returns
│   ├── SPY, AGG, GLD, DIA, QQQ, IWM → common_reference_stocks()
│   ├── Country/sector ETFs (EWZ, EFA, etc.) → reference_stocks()
│   ├── Primary asset with full OHLCV → market_data_source()
│   └── Bitcoin → common_crypto_pairs()
│
├── Economic indicators
│   ├── Common curated series (CPI, PCE, GDP, yields) → common_economic_indicators()
│   └── Any FRED series by ID → economic_indicators(series_id='XXXX')
│
├── Corporate data
│   └── Dividends → dividends()
│
└── Derived/computed
    └── Portfolio blends, spreads, rankings → computed from above sources
```

---

## Narrative Themes

Every Exhibit A chart serves one of these advisor-communication themes:

| Theme | Message | Chart Patterns Used |
|-------|---------|-------------------|
| **Stay invested** | Markets recover; don't panic sell | Growth-of-$1, bear/bull comparison, missed-best-days |
| **Volatility is normal** | Drawdowns happen every year | Return+drawdown overlay, pullback counts, annual distribution |
| **Time beats timing** | Long holding periods win | Holding period returns, growth-of-$1, ATH frequency |
| **Diversification** | Don't concentrate risk | Stock/bond splits, US vs international, asset class returns |
| **Economic context** | Macro data informs but doesn't predict | Economic indicator time series, yield curves, GDP |
| **Historical perspective** | Today is not unique | Decade comparisons, presidential terms, recession history |

---

## Unimplemented Chart Types

The following Exhibit A visual patterns do NOT yet have EpochScript definitions:

| Pattern | Examples | Implementation Challenge |
|---------|----------|------------------------|
| **Pie chart** | Mag 7 market cap concentration | No `pie` chart type in EpochScript |
| **Scatter plot with trend line** | Forward P/E vs 10-year forward returns | `xy_scatter` exists but not used yet |
| **Ranked waterfall bars** | Annual returns highest to lowest (96 bars) | Feasible with labeled bars + sorting |
| **Mathematical function** | Rule of 72 (72/x curve) | No market data; needs creative workaround |
| **Grouped paired bars** | CapEx 2024 vs 2025 by company | Feasible with stacked/grouped `xy_bars` |
| **Earnings/fundamental data** | Forward profit margins, trailing P/E | Requires corporate earnings data source |
| **Sentiment data** | Bull/bear spread (AAII) | Requires sentiment data source |
