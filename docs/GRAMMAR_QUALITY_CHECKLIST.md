# EBNF Grammar Quality Checklist

Every edit to the grammar (Layer 1/2 signatures, Layer 3 listing) must pass ALL of these before commit.

---

## Line Rules

- [ ] **No line > 100 chars.** If columns overflow, split into multiple lines with same indent
- [ ] **No empty args.** `fn(, N)` is wrong. If the input has no name, fix the abbreviation or use `src`
- [ ] **No duplicate patterns.** If `fn(h, l)` appears twice, merge the names onto one line
- [ ] **No orphan names.** Every function listed must show how to call it. `ipos` alone is useless — show `ipos()` with columns

## Signature Rules

- [ ] **Every builtin shows inputs.** `rsi` alone is wrong. Must be `rsi(src, N)` or grouped under `fn(src, N): rsi ...`
- [ ] **Single option = positional.** `rsi(src, 14)` not `rsi(src, period=14)`. The option name is noise when there's only one
- [ ] **Multiple options = kwargs.** `adosc(h, l, c, v, short_period=3, long_period=10)`. Positional numbers are ambiguous
- [ ] **Return type only when non-Decimal.** `→ Bool`, `→ Int`, `→ Timestamp`. Decimal is default, never shown
- [ ] **Type prefix only when mixed.** `Decimal: .x .y  String: .z` — but if ALL outputs are Decimal, no prefix

## Data Source Rules

- [ ] **Every data source shows output columns.** No `fn() — no options: ipos splits ...` without columns
- [ ] **Group by ACTUAL shared schema, not convenience.** cash_flow and income_statement have different columns — don't say "same"
- [ ] **Show variable assignment.** `earn = earnings()` not just `earnings()` — agent needs to know how to access `.eps_surprise`
- [ ] **OHLCV is always `.o .h .l .c .v`** — stated once, not repeated per source

## Macro Rules

- [ ] **Every macro shows full example with output tuple.** `ml, sl, hist = macd(src.c)` — agent needs the variable names
- [ ] **All kwargs shown with defaults.** `macd(src.c, short_period=12, long_period=26, signal_period=9)`
- [ ] **Variadic macros show list syntax.** `patterns=[CandlestickPattern.doji, CandlestickPattern.hammer]`

## Layer 3 Rules

- [ ] **No builtins/macros in Layer 3.** If it has a single-stage form, it belongs in Layer 1/2 only
- [ ] **No internal transforms.** `downsample`, `upsample`, `ma`, `event_marker`, `is_asset_ref` — hidden
- [ ] **No infrastructure.** `asset_spec`, `index`, `group_by`, `pivot_wider` — agent never calls these directly

## Token Efficiency

- [ ] **Group same-signature functions on one line.** `fn(src, N): rsi trix cmo fosc ...` saves N-1 newlines
- [ ] **No redundant descriptions.** The signature IS the doc. Don't repeat what the name already says
- [ ] **No formal grammar rules.** LLMs know Python syntax. `integer = "0" | [1-9][0-9]*` is waste
- [ ] **Enum values inline when < 10.** `@Quarter: Q1 Q2 Q3 Q4`. If > 20, say "use find_enum()"

## Edge Case Accuracy

- [ ] **`where` 2-arg vs 3-arg documented.** 2 args = null on false
- [ ] **`coalesce` order matters, min 2 args.** Left-to-right, first non-null
- [ ] **`conditional_select` is case-when.** Alternating cond/value pairs, NOT same as where
- [ ] **`switch` is 0-indexed.** `switch(0, a, b, c)` returns `a`
- [ ] **`is_study_asset` takes 0 args.** Not `ticker="SPY"`
- [ ] **Lag/lead supports 0 and negative.** `>> 0` is identity, `<< 1` is look-ahead
- [ ] **Pipeline passes left as first arg.** `src.c | sma(20)` = `sma(src.c, 20)`

## Pre-Commit Verification

```bash
# 1. Build and generate
cd EpochBackend && ./scripts/generate_sdk.sh --lezer

# 2. Check no line > 100 chars
awk 'length > 100 {print NR": "length" chars: "$0}' packages/epoch-script/docs/epochscript.ebnf

# 3. Check no empty args fn(, )
grep 'fn(,' packages/epoch-script/docs/epochscript.ebnf

# 4. Run compiler tests
./cpp_tools/run_target.sh -j64 --run epoch_script_test -- "[compiler]"

# 5. Read the output as an agent would — can you write code from every line?
head -120 packages/epoch-script/docs/epochscript.ebnf
```
