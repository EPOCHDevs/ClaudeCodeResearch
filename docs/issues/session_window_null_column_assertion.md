# Session Window: Null column assertion failure on ES-Futures

**Status:** Open
**Priority:** Medium
**Component:** Session window transform runtime (epoch-script)
**Affects:** `ct_es_volume_range_distributions_research`

## Summary

The `session_window` transform hits an assertion failure `column != nullptr` when processing ES-Futures data. This suggests a null/missing column in the input DataFrame that session_window doesn't handle gracefully.

## Error

```
Pipeline error in Default strategy, transform 'session_window' (eth_sw), asset 'ES-Futures':
  Assertion failed: column != nullptr
```

## Root Cause

Likely a missing OHLCV column in the ES-Futures data for the requested session range, or the ETH (Extended Trading Hours) session produces a DataFrame with null columns that session_window doesn't guard against.

## Reproduction

```bash
./cpp_tools/run_generate_job_data.sh script_templates/definitions/test_runner/ct_es_volume_range_distributions_research.json --start 2023-01-01 --end 2024-06-30
```

## Files

- `packages/epoch-script/src/transforms/packages/sessions/impl/session_window.h`
