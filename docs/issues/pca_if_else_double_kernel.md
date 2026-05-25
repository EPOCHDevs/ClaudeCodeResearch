# PCA Transform: if_else kernel missing for (double, double, double)

**Status:** Open
**Priority:** Medium
**Component:** PCA transform runtime (epoch-script)
**Affects:** `audnzd_macro_fair_value_research`

## Summary

The PCA transform internally calls Arrow's `if_else` function with three `double` arguments. Arrow's `if_else` expects `(bool, T, T)` — the first argument must be a boolean condition. The PCA implementation is passing a double as the condition.

## Error

```
Pipeline error in Default strategy, transform 'pca' (pca_out), asset '^NZDUSD-FX':
  NotImplemented: Function 'if_else' has no kernel matching input types (double, double, double)
```

## Root Cause

The PCA transform's internal logic uses `if_else` for conditional value selection but passes a numeric value where a boolean is expected. This is a type error in the PCA implementation, not a compiler issue.

## Files

- `packages/epoch-script/src/transforms/packages/machine_learning/impl/rolling_pca.h` (likely)
