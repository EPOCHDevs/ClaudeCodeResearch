# Builtin/Macro Coverage Test Plan

## Goal
100% coverage of every Layer 1/2 function in the EBNF grammar — verify each compiles with both positional and kwargs forms, and resolves to a valid registered transform.

## Test Layers

### Layer A: Registry Coverage (`builtin_coverage_test.cpp`)
For every entry in `BuiltinRegistry`:
1. `Lower()`/`Expand()` succeeds with synthetic args matching `ArgSpec`
2. `impl_node_id` exists in `ITransformRegistry`
3. Every option set by the lowering exists in the transform's metadata
4. Both positional AND kwargs forms work

### Layer B: EBNF Grammar Coverage (`ebnf_coverage_test.cpp`)
Parse the generated EBNF, extract every function signature, compile a minimal script for each:
1. Every Layer 1 function listed in the EBNF compiles
2. Every Layer 2 macro listed in the EBNF compiles
3. Every Layer 3 registered transform listed in the EBNF compiles
4. Every enum value referenced in the EBNF is valid
5. Every data source function compiles with its documented options

### Layer C: Syntax Variants
For each function, test all call forms:
- Positional: `sma(close, 20)`
- Kwargs: `sma(close, period=20)`
- Pipeline: `close | sma(20)`
- Default args: `sma(close)` (if period has default)

## What This Catches
- Stale `impl_node_id` (transform renamed/removed)
- `ArgSpec` mismatch (min/max wrong)
- Kwargs ignored (corr, day_of_week bugs)
- Option name mismatch between builtin and transform metadata
- EBNF documents a function that doesn't compile
- Enum names in EBNF don't match registered enums
- Missing builtins (in registry but not EBNF, or vice versa)

## Implementation
- `builtin_coverage_test.cpp` — registry-level, no compilation, fast
- `ebnf_coverage_test.cpp` — parses EBNF, compiles snippets, slower but comprehensive
- Both in `epoch_script_test` target with `[builtin_coverage]` tag
- No data needed, no E2E, pure compiler validation
