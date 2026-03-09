# Research Definition Antipatterns

Common mistakes found in pre-Exhibit A research definitions, documented during the rubric review process. Each antipattern includes what's wrong, why it matters, and the Exhibit A fix.

---

## Antipattern 1: Dashboard Dump

**What it looks like:** A single definition produces 10-20+ charts covering every angle of a topic — summary tables, bar charts, line charts, z-scores, margins, event markers — all in one file.

**Why it's wrong:** No single chart tells a clear story. The reader drowns in data and has to figure out the insight themselves. Exhibit A's core principle is *one chart, one insight*.

**Example:** `aapl_valuation_multiples_peer_comparison` — 17 charts (2 summary tables, 8 bar charts, 6 line charts, 1 card, 1 event marker) answering no specific question.

**EA fix:** Pick the ONE question you're answering. Produce 1-3 charts max. If you need a deep-dive dashboard, that's a separate definition from the presentation chart.

```
BAD:  "Here are all the valuation metrics for 6 companies"
GOOD: "Is AAPL expensive relative to mega-cap tech peers?"
```

---

## Antipattern 2: Rainbow Palette

**What it looks like:** Each chart uses a different color — Blue for P/E, Purple for P/S, Teal for EV/EBITDA, Indigo for Adj P/E, Green for Op Margin, Emerald for Net Margin.

**Why it's wrong:** Color variety fights for attention instead of letting the data speak. It creates visual noise and looks unprofessional. Exhibit A uses a monochromatic blue palette for everything.

**Example:** `aapl_valuation_multiples_peer_comparison` — 6 different colors across 8 bar charts.

**EA fix:** Use `Color.Blue` as primary for all data. Use `Color.Gray` for secondary/comparison series. Reserve `Color.Red` only for explicitly negative data (inversions, losses). Never use more than 3 colors in a single definition.

```
BAD:  colors=['Blue'], colors=['Purple'], colors=['Teal'], colors=['Indigo']
GOOD: Color.Blue for all primary bars, Color.Gray for reference/comparison
```

---

## Antipattern 3: Missing Data Labels

**What it looks like:** Bar charts render without numeric labels on the bars. The reader has to trace bars back to the y-axis to read values.

**Why it's wrong:** Exhibit A's annotation-driven storytelling means the key number is always visible on the chart itself. Every bar chart should show its value.

**EA fix:** Always set `data_labels=True` on bar charts.

```
BAD:  cs_bars(title='P/E Ratio by Asset', agg=Last)(pe)
GOOD: cs_bars(title='P/E Ratio by Asset', agg=Last, data_labels=True)(pe)
```

---

## Antipattern 4: No Framing Question

**What it looks like:** The definition description lists what data is computed but never states what question the chart answers or what insight the reader should take away.

**Why it's wrong:** Without a question, the chart is just data visualization, not communication. Exhibit A charts always answer a specific question that an advisor would ask or a client would care about.

**Example:** `"Cross-sectional comparison of AAPL valuation multiples (P/E, P/S, EV/EBITDA, P/B) against large-cap tech peers"` — this describes the computation, not the insight.

**EA fix:** Every definition should start from a question. The `name` field should hint at the answer, and the `description` field should state the question explicitly.

```
BAD:  name: "AAPL Valuation Multiples: 5Y History & Large-Cap Tech Peer Comparison"
GOOD: name: "Is AAPL Expensive Relative to Mega-Cap Tech Peers?"
```

---

## Antipattern 5: No Reference Lines

**What it looks like:** Bar charts or line charts with no contextual anchors — no zero line, no average, no median, no historical norm.

**Why it's wrong:** Without a reference point, the reader can't judge "is this high or low?" Exhibit A uses reference lines on 55% of charts. A zero line on return charts and an average line on comparison charts are essential.

**EA fix:** Add reference lines for context:

```
BAD:  xy_bars(agg=Last)(pe_by_company)
GOOD: xy_bars(
    agg=Last,
    reference_lines=ReferenceLineSchema(lines=[
        ReferenceLine(value=25.0, color=Color.Gray, dash_style=DashStyle.Dash, title='Peer Median')
    ])
)(pe_by_company)
```

| Chart Type | Reference Line |
|-----------|----------------|
| Return bars (pos/neg) | `value=0.0` zero line |
| Cross-sectional comparison | Peer median or historical average |
| Z-score charts | `value=0.0` and optionally +1/-1 bounds |
| Spread/area charts | `value=0.0` zero line |

---

## Antipattern 6: Too Many Series

**What it looks like:** A single chart with 6+ overlaid lines or 6+ bar groups. Labels overlap, colors blur together, the chart becomes unreadable.

**Why it's wrong:** Exhibit A never shows more than 3 series per chart. When comparing 6+ entities, use a bar chart (one bar per entity) rather than 6 overlaid lines.

**EA fix:**
- **1-3 entities:** Use `xy_lines` with distinct series
- **4+ entities:** Use `xy_bars` (cross-sectional snapshot) or `cs_bars` (one bar per asset)
- **If you need all entities over time:** Split into 2 charts (e.g., AAPL+MSFT+GOOGL in one, AMZN+META+NVDA in another)

---

## Antipattern 7: Redundant Charts

**What it looks like:** The same metric shown as both a bar chart AND a line chart AND a table. P/E appears as `cs_bars(P/E)`, `cs_lines(P/E over time)`, and `cs_summary_table(P/E column)`.

**Why it's wrong:** Each chart should add unique information. Showing the same number three ways wastes the reader's attention. Pick the best visualization for the insight.

**EA fix:** Choose ONE format per metric based on what you're communicating:

| What You're Showing | Best Format |
|---------------------|-------------|
| Current snapshot comparison | `cs_bars` or `xy_bars` |
| How it changed over time | `xy_lines` or `cs_lines` |
| Exact numbers for reference | `summary_table` (use sparingly) |

Don't use all three for the same metric.

---

## Antipattern 8: Generic Titles

**What it looks like:** Titles that describe the data type rather than the insight: "P/E Ratio (TTM) by Asset", "Operating Margin Over Time", "Z-Score History".

**Why it's wrong:** Exhibit A titles hint at the takeaway. They're written for someone who wants to understand, not someone who already knows what P/E is.

**EA fix:** Write titles that answer "so what?":

```
BAD:  "P/E Ratio (TTM) by Asset"
GOOD: "NVDA Commands the Highest Valuation Among Mega-Cap Tech"

BAD:  "Operating Margin Over Time"
GOOD: "AAPL's Margins Have Remained Remarkably Stable"

BAD:  "P/E Z-Score by Asset"
GOOD: "Most Mega-Cap Tech Trades Near Historical Averages"
```

---

## Antipattern 9: Unstructured Category Sprawl

**What it looks like:** Charts spread across 7+ categories with generic names: "1. Cross-Sectional Snapshot", "2. Valuation Bars", "3. Profitability", "4. Relative Value", "5. Valuation History", "6. Margin History", "7. Z-Score History".

**Why it's wrong:** This mirrors an analyst's mental model, not a reader's journey. Exhibit A presents information in narrative order — setup, evidence, conclusion — not by data type.

**EA fix:** Organize by the story arc, using 1-3 categories max:

```
BAD:  7 categories organized by data type
GOOD:
  Category 1: "Valuation Snapshot" (the current comparison — 1-2 charts)
  Category 2: "Historical Context" (how we got here — 1 chart)
```

---

## Antipattern 10: Technical Jargon Titles

**What it looks like:** Chart titles use the statistical method or computation as the title: "P/E Z-Score Over Time", "Rolling 5Y Standard Deviation", "Cross-Sectional Correlation Matrix".

**Why it's wrong:** The z-score is the *tool*, not the *insight*. Advisors and clients don't think in z-scores — they think in questions like "Is this stock expensive compared to its own history?" The title should name the domain implication, not the statistical technique used to measure it.

Agents are especially prone to this — they default to describing the computation they performed rather than the question it answers. Every technical metric maps to a plain-language domain question:

| Technical Title (BAD) | Domain Question (GOOD) |
|----------------------|----------------------|
| P/E Z-Score Over Time | Is AAPL's Valuation Stretched vs Its Own History? |
| Rolling 5Y Standard Deviation | How Volatile Has This Asset Been? |
| EV/EBITDA Z-Score by Asset | Which Mega-Cap Tech Is Cheapest Relative to History? |
| Cross-Sectional Correlation | Do These Assets Move Together or Diversify? |
| Drawdown Duration Analysis | How Long Do Recoveries Take? |
| Sharpe Ratio Comparison | Which Strategy Delivers the Best Risk-Adjusted Returns? |
| Bollinger Band Width Over Time | Is Volatility Expanding or Contracting? |
| Beta Rolling 60-Day | Is This Stock Becoming More or Less Sensitive to the Market? |

**EA fix:** Ask yourself: *"If I showed this to someone who doesn't know what a z-score is, what would the title say?"* That's your title.

```
BAD:  "P/E Z-Score Over Time"
GOOD: "Is AAPL's Valuation Stretched vs Its Own History?"

BAD:  "Volatility Z-Score by Asset"
GOOD: "Which Assets Are Experiencing Unusual Volatility?"

BAD:  "Return Distribution Histogram"
GOOD: "Most Years the S&P 500 Gains Between 10-20%"
```

The rule: **Name the insight, not the instrument.**

---

## Antipattern 11: Reflexive Card Dumps

**What it looks like:** Cards that echo the same values already shown in the chart — e.g., a return attribution definition with cards showing "Earnings Contribution: +3.1%", "Sentiment Shift: +53.1%" alongside a bar chart that already displays those exact numbers with `data_labels=True`.

**Why it's wrong:** Cards occupy prime dashboard real estate. When they duplicate what the charts already communicate, they waste space and add no new information. Models default to adding cards because they *can*, not because they *should*. The instinct is "more context = better" — but on a dashboard, redundancy = noise.

**How we caught this:** During the MSFT return drivers redesign, we had three cards (Earnings Contribution, Sentiment Shift, P/E Ratio) alongside a bar chart showing the same three values with labeled bars. When we asked "what is the card showing that the bar chart is not?" — the answer was nothing. The bar chart with `data_labels=True` and `color_by_value=True` already IS the card, but with visual context (reference line, relative sizing, color encoding).

**When cards ARE useful:**
- **Standalone metrics** that don't appear in any chart (e.g., current P/E on a price chart definition)
- **Cross-definition context** — a metric from a different domain that frames the chart (e.g., "10Y Yield: 4.5%" on an equity valuation chart)
- **Status/verdict indicators** — binary or categorical outcomes (e.g., "Signal: Overvalued")

**When cards are NOT useful:**
- Restating what a labeled bar chart already shows
- Showing the "last" value of a line chart (the endpoint is visible)
- Summary statistics (mean, median) that could be a reference line instead

**EA fix:** Before adding a card, ask: *"If I removed this card, would the reader miss any information?"* If the answer is no — delete the card. Use reference lines, data labels, and chart annotations instead.

```
BAD:  cards(Earnings: +3.1%, Sentiment: +53.1%) + xy_bars(Earnings: +3.1%, Sentiment: +53.1%)
GOOD: xy_bars with data_labels=True — the chart IS the summary

BAD:  cards(Current P/E: 43.5) + xy_lines(P/E over time ending at 43.5)
GOOD: xy_lines alone — the endpoint value is the "card"

GOOD USE: cards(10Y Yield: 4.5%) on a definition about equity valuation
           — the yield doesn't appear in any chart but frames the story
```

---

## Antipattern 12: Unqualified Card Metrics

**What it looks like:** A card that says "P/E Ratio: 43.5" or "EPS Growth: 0.4%" with no indication of *when*, *what period*, or *what context* the number refers to.

**Why it's wrong:** The reader sees a random number with no anchor. Is it current? Last quarter? 5-year average? Study-window end? Cards with `card_agg=AggregationType.Last` show the last value in the study period — not a live/current figure. If the study ran 2021-2024, "P/E Ratio: 43.5" is the Dec 2024 value, not today. Without qualification, the reader assumes it's current and may act on stale data.

**How we caught this:** During the MSFT earnings trajectory redesign, a card showed "P/E Ratio: 43.5" alongside YoY growth bars. Two problems: (1) it was redundant — the dashboard already shows the actual current P/E, and (2) it was unqualified — "43.5" could be anything without a date or label context. The reader sees a random number.

**The rule:** Every card metric must be **self-qualifying** — the title alone must tell the reader what the number is, when it's from, or what it means.

```
BAD:  "P/E Ratio: 43.5"         — when? current? historical? which period?
BAD:  "EPS Growth: 0.4%"        — YoY? QoQ? this quarter? trailing?
GOOD: "P/E (TTM, Dec '24): 43.5" — qualified with period and date
GOOD: "EPS Growth YoY (Q4 '24): 0.4%" — qualified with method and quarter
GOOD: "Signal: Overvalued"       — self-qualifying (status/verdict)
```

**But the deeper question remains:** Even a properly qualified card must still pass the Antipattern #11 test — *"If I removed this card, would the reader miss any information?"* A qualified card that duplicates the chart is still redundant. Qualification is necessary but not sufficient.

---

## Antipattern 13: Distribution Without Summary Stats

**What it looks like:** A histogram or distribution chart that shows the *shape* of the data but never states the actual numbers — no median, no percentiles, no "current vs typical" anchor.

**Why it's wrong:** The reader can see the distribution shape but can't answer the question without eyeballing. "What P/E has AMZN typically traded at?" requires a number — the histogram alone forces the reader to estimate from bar heights. A summary table or card with median, 25th/75th percentile, and the current value turns visual impression into actionable knowledge.

**How we caught this:** An AMZN P/E histogram showed a wide distribution (27x–473x) with hardcoded scenario lines that didn't match reality. When asked "what does AMZN typically trade at?", we had to query the raw data to compute median=126x, IQR=53x–154x, current=29x. None of those numbers appeared anywhere in the definition.

**The rule:** Every distribution chart needs a companion summary — either a `summary_table` with key percentiles or `cards` with the headline stats. The chart shows *shape*, the summary shows *numbers*.

```
BAD:  histogram(title='P/E Distribution')(pe)
      — reader sees a shape, can't quote a number

GOOD: histogram(title='P/E Distribution',
        reference_lines=[median, p25, p75])(pe)
      + summary_table(Median, 25th, 75th, Current)(pe_median, pe_p25, pe_p75, pe_current)
      — reader sees shape AND can quote "median 126x, currently 29x"
```

**When the summary IS the chart:** If the question is "what's the typical value?" rather than "what's the distribution shape?", consider whether you even need the histogram. A bar chart of percentile ranges or a single card might answer the question more directly.

---

## Antipattern 14: NaN-Poisoned Conditionals

EpochScript's ternary `X if cond else Y` returns **NaN when `cond` is NaN** — not `Y`. Guard sparse conditionals with `is_valid()`:

```
BAD:  event_ret = nfp_day if is_strong else 0.0       # NaN when is_strong is NaN
GOOD: raw = nfp_day if is_strong else 0.0
      event_ret = raw if is_valid(raw) else 0.0        # guaranteed dense
```

---

## Quick Reference: EA Quality Checklist

Before submitting a definition, verify:

- [ ] **Question stated** — Can you articulate the ONE question this answers?
- [ ] **3 charts or fewer** — Can the story be told in 1-3 visualizations?
- [ ] **Blue palette** — Is `Color.Blue` the primary color on every chart?
- [ ] **Data labels on bars** — Does every bar chart have `data_labels=True`?
- [ ] **Reference lines** — Does every chart have contextual anchors (zero line, average, median)?
- [ ] **Insightful title** — Does the title hint at the answer, not describe the data?
- [ ] **No redundancy** — Is every chart showing something the others don't?
- [ ] **3 series max** — No chart has more than 3 overlaid series?
- [ ] **2 categories max** — Are charts organized by narrative, not data type?
- [ ] **Cards earn their space** — Does every card show something the charts don't already display?
- [ ] **Cards are qualified** — Does every card title specify what, when, and how (e.g., "P/E (TTM, Dec '24)")?
- [ ] **Distributions have stats** — Does every histogram/distribution chart have companion summary stats (median, percentiles, current)?
- [ ] **Dense cumulative series** — Does every `cumulative()` feeding a line chart have an `is_valid()` guard to fill NaN gaps?
