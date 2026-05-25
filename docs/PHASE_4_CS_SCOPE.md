# Phase 4 — Cross-Sectional Scope Flag

**Status:** Not started
**Depends on:** Phases 0–3 complete (or can run in parallel — metadata-only changes)
**Goal:** Add `cross_sectional=True` flag to base transforms (`zscore`, `winsorize`) so `cs_*` variants become unnecessary. Purely C++ metadata struct changes — no new impl nodes, no parser changes.
**Touches:** C++ registered transform metadata structs (wherever each transform registers its options — `transform_metadata.json` is generated output from these structs via `/dump-metadata`, not edited directly)

---

## Background

`cs_zscore`, `cs_winsorize`, `cs_rank`, `cs_quantile`, `cs_weighted_mean` exist as separate
transforms because the cs_ prefix was the original way to select cross-sectional scope.
The refactor adds `cross_sectional: Boolean` as an option on the base transform, making the
cs_ variants redundant.

The `agg` builtin (Phase 2) already absorbs `cs_agg`. This phase handles the remaining
cs_* statistical transforms.

**Reporter cs_* (do NOT touch):** `cs_bars`, `cs_lines`, `cs_scatter`, `cs_histogram`,
`cs_boxplot`, `cs_pie`, `cs_gauge`, `cs_heatmap`, `cs_bubble`, `cs_summary_table`,
`cs_labeled_*`, `cs_news` — these are genuinely different chart/report types, not
scope variants. Leave them as-is.

---

## 4a — `zscore` + `cs_zscore`

### Current state

```
zscore(period=60, window_type="rolling")(signal)          — time-series zscore
cs_zscore(group_by=GroupBy.sector)(signal)                — cross-sectional zscore
```

Two separate transforms, different option sets.

### New state

```
zscore(period=60)(signal)                                          — time-series (unchanged)
zscore(cross_sectional=True)(signal)                              — cross-sectional, no group
zscore(cross_sectional=True, group_by=GroupBy.sector)(signal)     — cross-sectional grouped
```

### Metadata change

Add to `zscore` transform options:

```json
{
  "id": "cross_sectional",
  "name": "Cross-Sectional",
  "type": "Boolean",
  "required": false,
  "default": false,
  "description": "If true, compute z-score across all assets at each timestamp instead of rolling window over time."
},
{
  "id": "group_by",
  "name": "Group By",
  "type": "Select",
  "required": false,
  "default": "none",
  "enumType": "GroupBy",
  "condition": "cross_sectional == true",
  "description": "Grouping dimension for cross-sectional z-score. Only valid when cross_sectional=True."
}
```

### Impl node routing

When `cross_sectional=True`, the compiler routes to the `cs_zscore` impl node internally.
This is a metadata-driven routing decision — no new runtime node needed.

```
zscore(cross_sectional=False, period=60)(signal)  →  zscore impl node (existing)
zscore(cross_sectional=True)(signal)              →  cs_zscore impl node (existing)
zscore(cross_sectional=True, group_by=...)(signal) →  cs_zscore impl node with group_by
```

### `cs_zscore` deprecation

Mark `cs_zscore` → `internalUse=true` after this ships. Old form continues to compile but
is hidden from search results and docs.

### Validation

- `group_by` option present + `cross_sectional=False` → COMPILE WARNING: "group_by has no effect when cross_sectional=False"
- `period` option present + `cross_sectional=True` → COMPILE WARNING: "period has no effect when cross_sectional=True"

---

## 4b — `winsorize` + `cs_winsorize`

### Same pattern as zscore

```
winsorize(lower=0.05, upper=0.95, period=60)(signal)                       — time-series
winsorize(lower=0.05, upper=0.95, cross_sectional=True)(signal)            — cross-sectional
winsorize(lower=0.05, upper=0.95, cross_sectional=True, group_by=...)(s)   — grouped
```

Add `cross_sectional: Boolean = false` and conditional `group_by` option.
Mark `cs_winsorize` → `internalUse=true`.

---

## 4c — `rank` (from `cs_rank`)

`cs_rank` has no time-series counterpart, so we're not adding a flag to an existing base —
we're introducing `rank` as the new canonical name.

```
# Old:
cs_rank(group_by=GroupBy.sector)(signal)

# New:
rank(cross_sectional=True)(signal)
rank(cross_sectional=True, group_by=GroupBy.sector)(signal)
```

`cross_sectional` defaults to `True` here (rank only makes sense cross-sectionally).
Mark `cs_rank` → `internalUse=true`.

---

## 4d — `quantile` (from `cs_quantile`)

```
# Old:
cs_quantile(q=0.5, group_by=GroupBy.sector)(signal)

# New:
quantile(q=0.5, cross_sectional=True)(signal)
quantile(q=0.5, cross_sectional=True, group_by=GroupBy.sector)(signal)
```

Mark `cs_quantile` → `internalUse=true`.

---

## 4e — `weighted_mean` (from `cs_weighted_mean`)

```
# Old:
cs_weighted_mean()(signal, weights)

# New:
weighted_mean(cross_sectional=True)(signal, weights)
```

Mark `cs_weighted_mean` → `internalUse=true`.

---

## Summary table

| New form | Old form (internalUse) | cross_sectional default | Notes |
|---|---|---|---|
| `zscore(cross_sectional=True)` | `cs_zscore` | `false` | period option still valid when false |
| `winsorize(cross_sectional=True)` | `cs_winsorize` | `false` | lower/upper bounds still valid |
| `rank(cross_sectional=True)` | `cs_rank` | `true` | cs-only for now |
| `quantile(q=, cross_sectional=True)` | `cs_quantile` | `true` | cs-only for now |
| `weighted_mean(cross_sectional=True)` | `cs_weighted_mean` | `true` | cs-only for now |

---

## Implementation notes

All changes are metadata JSON updates. No C++ changes needed. The routing logic
(`cross_sectional=True` → cs_* impl node) is handled by the existing option-based routing
that already exists in the registered transform infrastructure.

Each transform's C++ metadata registration gets:
1. `cross_sectional: Boolean` option added
2. `group_by` option added (conditional on `cross_sectional=True`)
3. `internalUse=true` on the old `cs_*` registration
4. Routing annotation: `"when": {"cross_sectional": true}, "impl_node": "cs_zscore"`

Run `/dump-metadata` after changes to regenerate `transform_metadata.json` and verify the new options appear.

---

## Acceptance criteria

- [ ] `zscore(cross_sectional=True)(signal)` compiles and produces same output as `cs_zscore()(signal)`
- [ ] `zscore(cross_sectional=True, group_by=GroupBy.sector)(signal)` correct
- [ ] `zscore(period=60)(signal)` unchanged (no regression)
- [ ] `winsorize(cross_sectional=True)` works
- [ ] `rank(cross_sectional=True)` works
- [ ] `quantile(q=0.5, cross_sectional=True)` works
- [ ] `weighted_mean(cross_sectional=True)` works
- [ ] All 5 `cs_*` transforms marked `internalUse=true`
- [ ] COMPILE WARNING for `group_by` with `cross_sectional=False`
- [ ] All existing `cs_*` usage in test studies still compiles (backwards compat until deprecation)
- [ ] `/dump-metadata` regenerates `transform_metadata.json` with new options visible on all 5 base transforms
