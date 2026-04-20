# Phase 1 — Foundation Macros

**Status:** Not started
**Depends on:** Phase 0 complete (COMPILER_MACROS array + grammar structure + `BuiltinRegistry` from 0e)
**Goal:** `resample` macro (core variadic expansion infrastructure) + `study_assets` trading_hours option + 14 DataSource builtins.
**Touches:** `grammar_generator.cpp`, new files: `resample_expander.h`, `datasource_lowering.h`, registration calls in `InitializeTransforms()`

### Architecture note

All dispatch uses Phase 0e strategy interfaces. No if/else chains in `constructor_parser.cpp`.

- **`resample`** — custom `ResampleExpander` class (direction inference + plurality validation)
- **`study_assets` trading_hours** — existing variadic DataSource path (option addition only)
- **14 DataSource builtins** — `DataSourceLowering` strategy (validates kwargs, forwards to impl node)

---

## 1a — `resample` macro

### Why first

`resample` exercises the full variadic expansion stack — option-driven plurality, input-driven plurality, direction inference, and compile-time error cases. Every other variadic macro in Phase 3 follows the same pattern. Getting this right first de-risks the rest.

`downsample` and `upsample` become `internalUse=true` after this ships.

### EBNF contract

```ebnf
resample_expr ::=
    "resample" "(" resample_inputs "," resample_opts ")"

resample_inputs ::= series_expr ("," series_expr)*

resample_opts ::=
    "target_timeframe" "=" (timeframe_literal | "[" timeframe_literal ("," timeframe_literal)* "]")
    ("," "agg"  "=" "[" agg_type ("," agg_type)* "]")?   (* one per input; implies downsample *)
    ("," "how"  "=" fill_method_ref)?                     (* single fill; implies upsample *)

fill_method_ref ::= "FillMethod" "." ("ffill" | "bfill" | "nearest" | "asfreq")

(* @FillMethod: ffill | bfill | nearest | asfreq  — registered enum, auto-inlines in grammar *)
```

### Plurality rule

Exactly one axis may be plural. The compiler checks both:

| Case | inputs | target_timeframe | Result |
|---|---|---|---|
| Option-driven (same direction) | 1 | list `["1D","1W"]` | N nodes, same input, direction inferred per element |
| Option-driven (mixed direction) | 1 | list `["1W","30m"]` | N nodes — each element inferred independently; some downsample, some upsample |
| Option-driven | many | list `["1D","1W"]` | **COMPILE ERROR: ambiguous** |
| Input-driven | many | scalar `"1D"` | N nodes, same TF |
| Neither plural | 1 | scalar `"1D"` | 1 node |
| Both plural | many | list | **COMPILE ERROR: ambiguous expansion** |

### Direction inference

Resolved at compile time from the source node's timeframe annotation in the AST:

```
source_tf < target_tf  →  downsample(target_timeframe=tf, agg=[...])(inputs)
source_tf > target_tf  →  upsample(target_timeframe=tf, how=fill)(inputs)
source_tf == target_tf →  COMPILE ERROR: "resample to same timeframe has no effect"
source_tf unknown      →  COMPILE ERROR: "cannot infer resample direction — source timeframe unknown; use downsample() or upsample() directly"
```

Conflict guards:
- `agg` present + direction would be upsample → COMPILE ERROR: "`agg` option implies downsample but target_timeframe is smaller than source"
- `how` present + direction would be downsample → COMPILE ERROR: "`how` option implies upsample but target_timeframe is larger than source"
- Both `agg` and `how` present → COMPILE ERROR: "cannot specify both `agg` and `how`"
- Mixed direction + `agg` present → COMPILE ERROR on any element that would upsample
- Mixed direction + `how` present → COMPILE ERROR on any element that would downsample
- Mixed direction with no `agg`/`how` → valid; each element uses its inferred direction with defaults

### constructor_parser.cpp changes

```cpp
// Pseudocode for resample single-stage parse
if (name == "resample") {
    auto inputs = parse_positional_series_args(call);   // all series exprs before first kwarg
    auto opts   = parse_kwargs(call);

    auto tf = get_required_kwarg(opts, "target_timeframe");  // string or list<string>
    auto agg_list = get_optional_kwarg(opts, "agg");         // list<AggType> or null
    auto how      = get_optional_kwarg(opts, "how");         // FillMethod enum or null

    validate_resample_conflict(agg_list, how);               // error if both present

    bool tf_plural    = is_list(tf);
    bool input_plural = inputs.size() > 1;

    if (tf_plural && input_plural) {
        compile_error("ambiguous expansion: both target_timeframe list and multiple inputs");
    }

    // Emit N nodes via variadic_expansion_option machinery
    emit_resample_nodes(inputs, tf, agg_list, how);
}
```

### node_builder.cpp changes

`resample` uses the existing `variadic_expansion_option` path. The metadata entry for `resample` sets `variadic_expansion_option` to drive expansion. Direction inference happens before node_builder sees it — constructor_parser resolves to `downsample` or `upsample` impl node names, then node_builder emits N copies.

### Grammar addition (`GenerateEBNF()` COMPILER MACROS section)

This block is appended to the COMPILER MACROS section of the generated grammar doc:

```
# ── resample ───────────────────────────────────────────────────────────────
# resample(inputs..., target_timeframe=TF_or_list, agg=[...], how=FillMethod.X)
#
# Direction inferred per target at compile time:
#   source_tf < target_tf  →  downsample
#   source_tf > target_tf  →  upsample
#   source_tf == target_tf →  COMPILE ERROR
#
# OPTION-DRIVEN same direction (list TF → N outputs, same input):
#   daily, weekly = resample(src.c, target_timeframe=["1D", "1W"])
#
# OPTION-DRIVEN mixed direction (list TF → N outputs, direction per element):
#   weekly, hourly = resample(daily_src, target_timeframe=["1W", "1H"])
#   → 1W: downsample,  1H: upsample  (inferred independently)
#
# INPUT-DRIVEN (scalar TF → N outputs, multiple inputs):
#   c_d, h_d = resample(src.c, src.h, target_timeframe="1D")
#
# BOTH PLURAL → COMPILE ERROR: ambiguous expansion
#
# Downsample options:
#   agg=[Agg.Last]                    — aggregation per input (list length = input count)
# Upsample options:
#   how=FillMethod.ffill              — @FillMethod: ffill | bfill | nearest | asfreq
#
# Deprecates: downsample(), upsample()
```

### Skill: `S_resample_plurality.md`

```markdown
# S_resample_plurality — Resample variadic expansion rules

RULE: Exactly one axis may be plural. Violating this is a COMPILE ERROR.

OPTION-DRIVEN (list timeframe, single input → N outputs):
  daily, weekly = resample(src.c, target_timeframe=["1D", "1W"])
  → 2 nodes, both use src.c

INPUT-DRIVEN (scalar timeframe, multiple inputs → N outputs):
  c_d, h_d = resample(src.c, src.h, target_timeframe="1D")
  → 2 nodes, both downsample to 1D

SINGLE (scalar timeframe, single input → 1 output):
  daily = resample(src.c, target_timeframe="1D")
  → 1 node

DIRECTION INFERENCE:
  target larger than source  → downsample (daily from hourly)
  target smaller than source → upsample   (hourly from daily)
  same timeframe             → COMPILE ERROR

DOWNSAMPLE OPTIONS (agg= kwarg):
  daily_close = resample(src.c, target_timeframe="1D", agg=[Agg.Last])
  daily_c_h   = resample(src.c, src.h, target_timeframe="1D", agg=[Agg.Last, Agg.Max])
  NOTE: agg list length must match input count

OPTION-DRIVEN MIXED DIRECTION (list TF, directions inferred per element):
  weekly, hourly = resample(daily_src, target_timeframe=["1W", "1H"])
  → 1W > 1D: downsample  |  1H < 1D: upsample
  NOTE: cannot use agg= or how= with mixed direction — they imply a single direction

UPSAMPLE OPTIONS (how= kwarg):
  hourly_from_daily = resample(daily_close, target_timeframe="1H", how=FillMethod.ffill)
```

### Test cases (extend `variadic_datasource_test.cpp`)

```cpp
TEST_CASE("resample option-driven expansion") {
    // daily, weekly = resample(src.c, target_timeframe=["1D","1W"])
    // → 2 downsample nodes
}
TEST_CASE("resample input-driven expansion") {
    // c_d, h_d = resample(src.c, src.h, target_timeframe="1D")
    // → 2 downsample nodes, same TF
}
TEST_CASE("resample upsample direction inference") {
    // hourly source, daily target → upsample
}
TEST_CASE("resample downsample direction inference") {
    // daily source, weekly target → downsample
}
TEST_CASE("resample same-TF compile error") {
    // source is 1D, target is 1D → COMPILE ERROR
}
TEST_CASE("resample both-plural compile error") {
    // multiple inputs + list TF → COMPILE ERROR
}
TEST_CASE("resample agg-how conflict error") {
    // agg= and how= both present → COMPILE ERROR
}
TEST_CASE("resample agg count mismatch error") {
    // 2 inputs, agg list has 3 entries → COMPILE ERROR
}
TEST_CASE("resample option-driven mixed direction") {
    // daily source, target_timeframe=["1W","1H"]
    // → downsample to 1W + upsample to 1H, no agg/how → inferred defaults
}
TEST_CASE("resample mixed direction with agg conflict") {
    // daily source, target_timeframe=["1W","1H"], agg=[Agg.Last]
    // → COMPILE ERROR: agg implies downsample but "1H" target is smaller than source
}
```

### Acceptance criteria

- [ ] `resample` added to `COMPILER_MACROS`
- [ ] All 8 test cases pass
- [ ] `downsample`, `upsample` marked `internalUse=true` in metadata
- [ ] Grammar COMPILER MACROS section includes `resample` production rule and usage examples
- [ ] `S_resample_plurality.md` skill file complete
- [ ] `/dump-metadata` regenerates grammar with `resample` in single-stage names list

---

## 1b — `study_assets` trading_hours option

### What it adds

`study_assets()` currently always loads RTH (regular trading hours) data. Adding a `trading_hours` option lets users request extended hours, pre-market, or post-market without knowing the underlying `extended_market_data_source` impl node.

### API

```python
src      = study_assets()                                    # default: RTH
src      = study_assets(trading_hours=TradingHours.RTH)      # explicit RTH
src_ext  = study_assets(trading_hours=TradingHours.Extended) # extended hours
src_pre  = study_assets(trading_hours=TradingHours.PreMarket)
src_post = study_assets(trading_hours=TradingHours.PostMarket)

# With timeframe (existing):
daily, hourly = study_assets(target_timeframe=["1D","1H"], trading_hours=TradingHours.Extended)
```

### New enum: `TradingHoursType`

```cpp
// Register in InitializeTransforms() or equivalent:
GrammarGenerator::RegisterEnumType("TradingHoursType", {
    "RTH", "Extended", "PreMarket", "PostMarket"
});
```

4 values → auto-inline in EBNF quick reference and bundled on `study_assets` fetch.

### Lowering rule

```
TradingHours.RTH        → market_data_source impl node (existing, unchanged)
TradingHours.Extended   → extended_market_data_source impl node
TradingHours.PreMarket  → extended_market_data_source(session=pre_market) impl node
TradingHours.PostMarket → extended_market_data_source(session=post_market) impl node
```

The `study_assets` metadata entry gains a `trading_hours` option:

```json
{
  "id": "trading_hours",
  "name": "Trading Hours",
  "type": "Select",
  "required": false,
  "default": "RTH",
  "enumType": "TradingHoursType"
}
```

### Metadata / constructor_parser update

`study_assets` is already a variadic macro. The `trading_hours` option is a new kwarg that the constructor_parser reads before routing to the impl node selection:

```cpp
auto hours = get_optional_kwarg(opts, "trading_hours", "RTH");
std::string impl_node = (hours == "RTH")
    ? "market_data_source"
    : "extended_market_data_source";
// pass session param for PreMarket/PostMarket
```

### Grammar addition (`GenerateEBNF()` — study_assets options)

The `TradingHoursType` enum is registered and auto-inlines in the EBNF enum reference
(4 values — small enough to inline):

```
# study_assets trading_hours option
# trading_hours=TradingHours.RTH (default) | Extended | PreMarket | PostMarket
#
#   src     = study_assets()                                        # RTH (default)
#   src_ext = study_assets(trading_hours=TradingHours.Extended)
#   daily, hourly = study_assets(target_timeframe=["1D","1H"], trading_hours=TradingHours.Extended)
#
# @TradingHoursType: RTH | Extended | PreMarket | PostMarket
```

### Acceptance criteria

- [ ] `TradingHoursType` enum registered → appears in Lezer grammar for IDE completion
- [ ] `study_assets(trading_hours=TradingHours.Extended)` compiles and routes to `extended_market_data_source`
- [ ] Default (no `trading_hours`) still routes to `market_data_source` (no regression)
- [ ] `TradingHoursType` values inline in generated grammar EBNF enum reference

---

## 1c — DataSource builtins

### What it does

Promotes 14 DataSource transforms to Layer 1 builtins with single-stage call shapes. These are data loaders with zero or trivial options — the grammar one-liner tells the agent everything it needs.

5 additional DataSource transforms (`reference_stocks`, `reference_futures`, `fx_pairs`, `crypto_pairs`, `indices`) become `internalUse=true` — replaced by the existing `reference_assets()` builtin from Phase 1.

3 DataSource transforms stay Layer 3 (query builders with List filters): `news`, `cs_news`, `economic_calendar`.

### Migration rationale

All 14 pass the migration criteria:
- Not subsystems — they're single-purpose data loaders
- Options are not "the research" — they're data format selectors (annual vs quarterly, dividend type, series ID)
- No docs needed to pick params — enum values are self-documenting
- `fn(options)` grammar one-liner is the complete contract

### Grammar addition (`GenerateEBNF()` — BUILTIN FUNCTIONS, Tier D: DataSources)

```
# Tier D: DataSource builtins — single-stage data loaders
#
# Event data (zero arguments, outputs aligned to study asset timeline):
#   earnings()                  — EPS, revenue, surprises per filing date
#                                  .actual_eps .estimated_eps .eps_surprise .eps_surprise_percent
#                                  .actual_revenue .estimated_revenue .revenue_surprise .revenue_surprise_percent
#                                  .fiscal_period .fiscal_year .importance .date_status .previous_eps .previous_revenue
#   analyst_ratings()           — upgrades/downgrades, price targets, firm ratings
#                                  .rating .previous_rating .rating_action .price_target .previous_price_target
#                                  .adjusted_price_target .previous_adjusted_price_target .price_target_action
#                                  .price_percent_change .firm .importance
#   ipos()                      — IPO events: issue price, offer size, exchange
#                                  .final_issue_price .total_offer_size .shares_outstanding
#                                  .primary_exchange .ipo_status
#   splits()                    — stock splits: ratio, adjustment factor
#                                  .split_from .split_to .split_ratio .historical_adjustment_factor .adjustment_type
#   ticker_events()             — symbol changes, rebrandings
#                                  .event_type .ticker
#   short_interest()            — bi-monthly FINRA short interest
#                                  .short_interest .avg_daily_volume .days_to_cover
#   short_volume()              — daily FINRA short sale volume
#                                  .short_volume .total_volume .short_volume_ratio
#                                  .exempt_volume .non_exempt_volume
#
# Fundamental data (required period param):
#   balance_sheet(period=BalanceSheetTimeframe.quarterly)
#                                  .total_assets .total_liabilities .total_equity .cash .lt_debt .receivables
#                                  .inventories .goodwill .ppe_net .retained_earnings .current_assets
#                                  .current_liabilities .common_stock .filing_date .period_end
#                                  .fiscal_year .fiscal_quarter  (+ 13 more fields)
#   cash_flow(period=ReportingPeriod.quarterly)
#                                  .cfo .ncf_operating .ncf_investing .ncf_financing .capex .net_income
#                                  .dda .dividends .change_cash .filing_date .period_end
#                                  .fiscal_year .fiscal_quarter  (+ 9 more fields)
#   income_statement(period=ReportingPeriod.quarterly)
#                                  .revenue .gross_profit .operating_income .net_income .basic_eps .diluted_eps
#                                  .ebitda .cogs .rd .sga .basic_shares .diluted_shares
#                                  .filing_date .period_end .fiscal_year .fiscal_quarter  (+ 15 more fields)
#   @BalanceSheetTimeframe: annual | quarterly
#   @ReportingPeriod: annual | quarterly | trailing_twelve_months
#
# Dividends (optional type filter):
#   dividends()                                          — cash dividends (default: CD)
#   dividends(dividend_type=DividendType.LT)             — long-term capital gains
#                                  .cash_amount .split_adjusted_cash_amount .frequency .distribution_type
#                                  .declaration_date .record_date .pay_date .historical_adjustment_factor
#   @DividendType: CD | LT | SC | ST
#
# Macro / economic data (no asset requirement — universe-independent):
#   economic_indicators()                                          — FRED series (default: CPIAUCSL)
#   economic_indicators(series_id="UNRATE")                        — any FRED series by ID
#   economic_indicators(eia_route="petroleum/stoc/wstk", series_id="WCESTUS1")  — EIA data
#   economic_indicators(eia_route="...", eia_data_frequency=EiaFrequency.Monthly)
#                                  .result
#   @EiaFrequency: Annual | Daily | Monthly | Weekly
#
#   economic_revisions()                                           — FRED revision analysis (default: PAYEMS)
#   economic_revisions(series_id="GDPC1")
#                                  .initial_value .latest_value .revision_count .revision_delta
#
# Treasury auctions (no asset requirement):
#   common_treasury_auctions()                                     — default: Note10Y
#   common_treasury_auctions(auction_type=TreasuryAuctionType.Bond30Y)
#                                  .high_yield .bid_to_cover .allocation_pct
#   @TreasuryAuctionType: Bill4W | Bill8W | Bill13W | Bill26W | Bill52W
#                          Note2Y | Note3Y | Note5Y | Note7Y | Note10Y
#                          Bond20Y | Bond30Y | TIPS5Y | TIPS10Y | TIPS30Y
#
# Output fields are DataSource-specific — use dot access (e.g., earnings.eps_surprise).
# All event/fundamental sources align to the study asset's timeline.
# Macro/treasury sources have no asset requirement — universe-independent.
#
# DO NOT use: reference_stocks, reference_futures, fx_pairs, crypto_pairs, indices
#   — these are internalUse only; reference_assets() is the public form
```

### grammar_generator.cpp additions

Add to `BUILTIN_FUNCTIONS`:

```cpp
// Phase 1c: DataSource builtins
"earnings", "analyst_ratings", "ipos", "splits", "ticker_events",
"short_interest", "short_volume",
"balance_sheet", "cash_flow", "income_statement",
"dividends",
"economic_indicators", "economic_revisions",
"common_treasury_auctions",
```

### New enums to register

```cpp
// Already exist as metadata enums — register for grammar inlining:
GrammarGenerator::RegisterEnumType("BalanceSheetTimeframe", {"annual", "quarterly"});
GrammarGenerator::RegisterEnumType("ReportingPeriod", {"annual", "quarterly", "trailing_twelve_months"});
GrammarGenerator::RegisterEnumType("DividendType", {"CD", "LT", "SC", "ST"});
GrammarGenerator::RegisterEnumType("EiaFrequency", {"Annual", "Daily", "Monthly", "Weekly"});
GrammarGenerator::RegisterEnumType("TreasuryAuctionType", {
    "Bill4W", "Bill8W", "Bill13W", "Bill26W", "Bill52W",
    "Note2Y", "Note3Y", "Note5Y", "Note7Y", "Note10Y",
    "Bond20Y", "Bond30Y", "TIPS5Y", "TIPS10Y", "TIPS30Y"
});
```

### constructor_parser.cpp lowering

Each DataSource builtin maps 1:1 to its existing registered transform impl node:

```cpp
// DataSource builtins — lower to existing impl nodes
static const std::unordered_map<std::string, std::string> DATASOURCE_BUILTINS = {
    {"earnings",                  "earnings"},
    {"analyst_ratings",           "analyst_ratings"},
    {"ipos",                      "ipos"},
    {"splits",                    "splits"},
    {"ticker_events",             "ticker_events"},
    {"short_interest",            "short_interest"},
    {"short_volume",              "short_volume"},
    {"balance_sheet",             "balance_sheet"},
    {"cash_flow",                 "cash_flow"},
    {"income_statement",          "income_statement"},
    {"dividends",                 "dividends"},
    {"economic_indicators",       "economic_indicators"},
    {"economic_revisions",        "economic_revisions"},
    {"common_treasury_auctions",  "common_treasury_auctions"},
};
```

No impl node changes needed — these builtins are pure syntactic sugar over the existing registered forms. The parser extracts kwargs, validates against the builtin's accepted options, and emits the same impl node the two-stage form would have.

### internalUse changes

**14 promoted DataSources** — registered form → `internalUse=true`:
`earnings`, `analyst_ratings`, `ipos`, `splits`, `ticker_events`, `short_interest`, `short_volume`, `balance_sheet`, `cash_flow`, `income_statement`, `dividends`, `economic_indicators`, `economic_revisions`, `common_treasury_auctions`

**5 reference DataSources** — replaced by `reference_assets()` → `internalUse=true`:
`reference_stocks`, `reference_futures`, `fx_pairs`, `crypto_pairs`, `indices`

### DSL examples

```python
# ── Event data ────────────────────────────────────────────────────────
earn = earnings()
surprise = earn.eps_surprise_percent
beat = surprise > 0

ratings = analyst_ratings()
upgrade = ratings.rating_action == "Upgrades"

si = short_interest()
squeeze_risk = si.days_to_cover > 10

# ── Fundamental data ──────────────────────────────────────────────────
bs = balance_sheet(period=BalanceSheetTimeframe.quarterly)
current_ratio = bs.current_assets / bs.current_liabilities

inc = income_statement(period=ReportingPeriod.quarterly)
margin = inc.gross_profit / inc.revenue

cf = cash_flow(period=ReportingPeriod.annual)
fcf = cf.ncf_operating - cf.capex

# ── Dividends ─────────────────────────────────────────────────────────
div = dividends()
yield_proxy = div.split_adjusted_cash_amount

# ── Macro data ────────────────────────────────────────────────────────
cpi = economic_indicators(series_id="CPIAUCSL")
unrate = economic_indicators(series_id="UNRATE")
crude = economic_indicators(eia_route="petroleum/pri/spt", series_id="RWTC")

nfp_revisions = economic_revisions(series_id="PAYEMS")
revision_size = nfp_revisions.revision_delta

# ── Treasury auctions ─────────────────────────────────────────────────
t10y = common_treasury_auctions(auction_type=TreasuryAuctionType.Note10Y)
demand = t10y.bid_to_cover
```

### Acceptance criteria

- [ ] All 14 DataSource names added to `BUILTIN_FUNCTIONS`
- [ ] All 5 enums registered → appear in Lezer grammar for IDE completion
- [ ] Zero-option sources compile with no args: `earnings()`, `splits()`, etc.
- [ ] Fundamental sources require `period`: `balance_sheet()` → COMPILE ERROR
- [ ] `economic_indicators(eia_route=...)` routes correctly to EIA path
- [ ] All 14 registered forms marked `internalUse=true`
- [ ] `reference_stocks`, `reference_futures`, `fx_pairs`, `crypto_pairs`, `indices` marked `internalUse=true`
- [ ] Output field dot-access works: `earnings.eps_surprise` compiles
- [ ] All existing DataSource tests still pass — no regressions
