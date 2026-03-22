---
name: audit-code
description: |
  Deep code audit across the Epoch stack: code smell detection, systematic fix application, and cross-stack connectivity verification.
  Use when you want to audit a feature or component for bugs, dead code, silent failures, missing tests, or broken field wiring across layers.
  Covers: metadata → transform impl → proto → frontend connectivity.
allowed-tools: Bash, Read, Glob, Grep, Edit, Write, Agent
argument-hint: "<component-or-feature> [--phase 2|3|4|all] [--layer metadata|impl|proto|frontend]"
---

# Code Audit Skill

Deep audit of Epoch stack components across 3 phases: code smell detection, fix application, and cross-stack connectivity verification.

## Usage

```
/audit-code xy_bars
/audit-code bar_chart --phase 2
/audit-code histogram --phase 4
/audit-code lines_chart --phase all
```

## Phases

| Phase | Name | Purpose |
|-------|------|---------|
| **2** | Code Smell Audit | Single-file deep read, systematic questions per code block |
| **3** | Fix Pattern | One fix at a time, test-first, build+verify each |
| **4** | Cross-Stack Connectivity | Trace every field through all 4 layers, find broken wires |

Default: runs all phases sequentially (2 → 3 → 4).

## Stack Layers

| Layer | Location Pattern | Purpose |
|-------|-----------------|---------|
| **Metadata** | `epoch-script/src/transforms/metadata/*.cpp` | Declares options, inputs, outputs for transforms |
| **Implementation** | `epoch-script/src/transforms/components/reports/*.cpp` | Reads options, processes data, calls builders |
| **Proto** | `epoch-protos/proto/*.proto` | Defines the wire format (BarDef, LinesDef, etc.) |
| **Builder** | `epoch-dashboard/include/epoch_dashboard/tearsheet/*.h` | C++ builder that populates proto messages |
| **Frontend Types** | `EpochPortal/src/types/dashboard/protos.d.ts` | TypeScript proto type definitions |
| **Frontend Component** | `EpochPortal/src/components/dashboard/charts/*.tsx` | React component that reads proto → Highcharts config |

## Key Paths

```
BACKEND=/home/adesola/EpochDev/EpochBackend
PORTAL=/home/adesola/EpochDev/EpochPortal

# Metadata
$BACKEND/packages/epoch-script/src/transforms/metadata/

# Implementation
$BACKEND/packages/epoch-script/src/transforms/components/reports/

# Tests
$BACKEND/packages/epoch-script/test/unit/transforms/reports/
$BACKEND/packages/epoch-dashboard/tests/

# Proto definitions
$BACKEND/packages/epoch-protos/proto/

# Builders
$BACKEND/packages/epoch-dashboard/include/epoch_dashboard/tearsheet/
$BACKEND/packages/epoch-dashboard/src/tearsheet/

# Frontend types (package copy — authoritative)
$PORTAL/packages/epoch-protos/src/protos.d.ts

# Frontend types (local copy — may be stale)
$PORTAL/src/types/dashboard/protos.d.ts

# Frontend components
$PORTAL/src/components/dashboard/charts/
$PORTAL/src/utils/dashboard/protoToHighcharts.ts
```

---

## Phase 2: Code Smell Audit

### Scope: Per-File

Phase 2 operates on **one file at a time**. Each file gets its own complete deep read and independent audit report. If the argument names a component (e.g., `xy_bars`), resolve it to specific files and audit each separately:

```
/audit-code xy_bars
  → File 1: epoch-script/src/transforms/components/reports/bars.cpp
  → File 2: epoch-script/test/unit/transforms/reports/.../bars_test.cpp
  → File 3: epoch-dashboard/src/tearsheet/bar_chart_builder.cpp
  → File 4: EpochPortal/src/components/dashboard/charts/BarChart.tsx
  (each gets its own Phase 2 audit)

/audit-code bars.cpp
  → Single file audit

/audit-code BarChart.tsx
  → Single file audit
```

### Method

For **each file**, read it completely and evaluate **every code block** against these 5 questions:

| # | Question | What to look for |
|---|----------|-----------------|
| 1 | **Is it reachable?** | Dead code behind impossible conditions, unreachable branches, options never set by metadata |
| 2 | **Is it correct for ALL inputs?** | Edge cases: empty arrays, NaN values, single element, negative numbers, zero division, all-same values |
| 3 | **Does it fail explicitly or silently?** | Silent 0 or empty string on error vs. throwing/logging. NaN→0 conversions hiding data issues |
| 4 | **Is it tested?** | Find the test file. Is every branch/option covered? Are edge cases tested? |
| 5 | **Is it consistent?** | Same pattern used differently in two places? Copy-paste with subtle divergence? |

### Procedure (repeat for each file)

1. **Read the file** completely (not skimming — every line)
2. **Identify the corresponding test file** (if auditing an impl, find its tests; if auditing a test, find its impl)
3. **For each logical block** (function, branch, loop), answer all 5 questions
4. **Catalog findings** for this file in a numbered list with severity:

```markdown
## Code Smell Audit: <file_path>

| # | Severity | Question | Location | Finding | Impact |
|---|----------|----------|----------|---------|--------|
| 1 | CRITICAL | Correct for all inputs? | line 305 | Empty values → NaN but caller expects 0 | Silent data corruption |
| 2 | HIGH | Fails explicitly? | line 370 | Infinite aggregation silently becomes 0 | Misleading chart values |
| 3 | MEDIUM | Is it tested? | line 145 | groupPadding option not tested | Regression risk |
| 4 | LOW | Is it consistent? | lines 120,180 | Same pattern but different default | Confusing maintenance |
```

5. **Move to the next file** — do NOT bundle findings across files

### Severity Definitions

| Severity | Meaning |
|----------|---------|
| **CRITICAL** | Produces wrong results silently. User sees incorrect data with no warning. |
| **HIGH** | Loses information or masks errors. Recoverable but misleading. |
| **MEDIUM** | Missing test coverage or inconsistency. Not wrong today, but fragile. |
| **LOW** | Style, naming, minor inconsistency. No functional impact. |

### Code Smell Patterns to Watch For

- **NaN→0 conversions**: Arrow C++ `sum([NaN,...])` returns 0, not NaN. Any aggregation of NaN-heavy data silently zeroes out.
- **Empty container assumptions**: `.front()` / `.back()` on empty vector. `values[0]` without size check.
- **Option declared but never read**: Metadata declares an option, implementation never calls `getOption()`.
- **Test that can never fail**: Assertion checks condition that code guarantees (e.g., testing NaN throws when code explicitly allows NaN).
- **Copy-paste divergence**: Two similar code paths (e.g., labeled mode vs series mode) where one has a fix the other doesn't.
- **Silent fallback**: Catch-all `else` or `default:` that returns a plausible value instead of erroring.
- **Unreachable validation**: Validation that runs after the value is already coerced (e.g., checking for negative after `abs()`).

---

## Phase 3: Fix Pattern

### Method

For each issue found in Phase 2, fix **one at a time** in this order:

1. **Write/update the test first** — the test should fail (or be missing) before the fix
2. **Apply the minimal code fix** — smallest change that resolves the issue
3. **Build and run tests** — verify the fix passes and nothing regresses
4. **Move to the next issue**

### Procedure

```
For each issue (ordered CRITICAL → HIGH → MEDIUM → LOW):

  1. ASSESS: Is this truly a bug, or a design choice? If design choice, document and skip.

  2. TEST FIRST:
     - Find the test file for this component
     - Add a test case that exercises the exact bug condition
     - Build and confirm the NEW test fails (or add it alongside the fix if it's a missing-coverage issue)

  3. FIX:
     - Make the minimal code change
     - Do NOT refactor surrounding code
     - Do NOT add features
     - Do NOT fix other issues in the same edit

  4. VERIFY:
     - Build the test target:
       ./cpp_tools/run_tests.sh <test_target>
     - ALL existing tests must still pass
     - The new test must pass
     - If build fails, fix the build error before moving on

  5. REPORT:
     Issue #N: <title>
     - Test: <test file>:<line> — <test name>
     - Fix: <impl file>:<line> — <description>
     - Result: ✅ All tests pass (X assertions)
```

### Fix Anti-patterns (DO NOT)

- Do NOT bundle multiple fixes in one edit
- Do NOT "improve" code that isn't broken
- Do NOT add defensive checks for impossible states
- Do NOT change function signatures unless the bug requires it
- Do NOT skip the test step ("it's obvious this works")

---

## Phase 4: Cross-Stack Connectivity

### Method

For every field in the target proto message, trace the **full path** through all layers and verify it's connected end-to-end.

### Procedure

#### Step 1: Enumerate all proto fields

Read the `.proto` file for the target component. List every field with its type and number.

```
Example for BarDef:
  1. chart_def (ChartDef)
  2. data (repeated BarData)
  3. vertical (bool)
  4. stack_type (StackType)
  5. overlay_lines (repeated NumericLine)
  ...
```

#### Step 2: Trace each field through all layers

For each field, check:

| Layer | Check | How |
|-------|-------|-----|
| **Metadata** | Is there an option/input that feeds this field? | Grep for the option name in metadata `.cpp` |
| **Implementation** | Does the impl read the option and pass it to the builder? | Search for `getOption("field_name")` or equivalent in impl `.cpp` |
| **Builder** | Does the builder have a setter for this field? | Check the builder `.h` for `setFieldName()` method |
| **Builder impl** | Does the setter actually write to the proto? | Check builder `.cpp` for `set_field_name()` or `mutable_field_name()` |
| **Proto** | Is the field defined? | Already enumerated in Step 1 |
| **Frontend types** | Is the field in the TypeScript interface? | Grep `protos.d.ts` for the camelCase field name |
| **Frontend component** | Does the React component read and use the field? | Grep the chart `.tsx` for `data.fieldName` |
| **Highcharts mapping** | Does it map to the correct Highcharts option? | Check the chart component or `protoToHighcharts.ts` |

#### Step 3: Build connectivity matrix

```markdown
## Connectivity Matrix: <Component>

| Field | Metadata | Impl | Builder | Proto | TS Types | Component | Highcharts | Status |
|-------|----------|------|---------|-------|----------|-----------|------------|--------|
| vertical | ✅ b_vertical | ✅ getOption | ✅ setVertical | ✅ field 3 | ✅ vertical | ✅ data.vertical | ✅ chart type | CONNECTED |
| stackLabels | ✅ b_stack_labels | ✅ getOption | ✅ setStackLabels | ✅ field 10 | ✅ stackLabels | ❌ not read | ❌ | BROKEN at Component |
| overlayLines | — (code-set) | ✅ addOverlayLine | ✅ addOverlayLine | ✅ field 5 | ❌ missing | ❌ | ❌ | BROKEN at TS Types |
```

#### Step 4: Diagnose disconnections

For each BROKEN field:

1. **Identify the break point** — which layer is the first ❌?
2. **Determine the fix** — is it missing code, wrong field name, stale generated types?
3. **Assess severity**:
   - User-facing field that doesn't work → CRITICAL
   - Internal optimization field → LOW
   - Field used by some chart types but not others → MEDIUM

#### Step 5: Fix disconnections

Apply Phase 3 fix pattern to each disconnection, working from the deepest layer outward:
1. Fix proto/types first (regenerate if needed)
2. Fix frontend component
3. Verify with build

### Common Disconnection Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Stale generated types** | Package proto has field, local copy doesn't | Regenerate or manually add to local `protos.d.ts` |
| **Builder has setter, impl doesn't call it** | Option declared in metadata but never wired | Add `getOption()` → `builder.setX()` in impl |
| **Frontend ignores field** | Proto has field, component never reads `data.fieldName` | Add Highcharts mapping in component |
| **Wrong Highcharts option** | Field is read but mapped to wrong HC property | Fix the mapping (e.g., `yAxis.stackLabels` not `plotOptions.stackLabels`) |
| **Hardcoded override** | Component reads field but then overwrites with hardcoded value | Remove hardcoded value, use proto value with fallback default |

---

## Output Format

After completing all requested phases, produce a final summary:

```markdown
## Audit Summary: <component>

### Phase 2: Code Smells
- **Found:** X issues (Y critical, Z high, ...)
- **Key findings:** [1-2 sentence summary]

### Phase 3: Fixes Applied
- **Fixed:** X of Y issues
- **Skipped:** Z issues (with reasons)
- **Tests:** All passing (N assertions)

### Phase 4: Connectivity
- **Fields traced:** X
- **Connected:** Y (Z%)
- **Disconnected:** W (list)
- **Fixed:** V disconnections

### Remaining Work
- [ ] Item 1
- [ ] Item 2
```

ARGUMENTS: $ARGUMENTS
