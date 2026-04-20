# Auto-Upsample: Cascade Through Tuple Packing

**Status:** Open
**Priority:** High
**Component:** TimeframeResolver (epoch-script compiler)
**Affects:** `qqq_ib_low_reversal_timing_research` and similar multi-timeframe intraday studies

## Summary

The inline auto-upsample in `TimeframeResolver::ResolveAll` does not fully cascade through deep node chains involving `logical_and`, `boolean_select`, and `tuple_pack`. When a 5Min series is mixed with a 1Min series 4+ nodes upstream of a `tuple_pack`, the intermediate nodes don't all get corrected, leaving `tuple_pack` at 5Min. The upsample runtime then fails because `fill_null_forward` doesn't support StructArrays.

## Reproduction

```
src = study_assets(target_timeframe="5Min")
ib_sw = session_window(...)(src.o, src.h, src.l, src.c)   # 5Min
eod_sw = session_window(...)(src.o, src.h, src.l, src.c)   # 5Min
is_eod = eod_sw.closed                                     # 5Min (from session_window)

# Chain: is_eod(5Min) → is_triggered → is_win → ifexp → mul → win_count → tuple_pack
# BUT: dow comes from datetime_extract(index()) which is 1Min
# tuple_pack(win_count[5Min], loss_count[5Min], dow[1Min]) → mismatch
```

## Root Cause

The inline auto-upsample inserts `upsample + tuple_index[0]` when it detects a mismatch. But the cascade needs to propagate through many intermediate nodes (`logical_and`, `boolean_select`, `mul`). Each node along the chain may have BOTH inputs at 5Min (no mismatch), so no auto-upsample fires. Only at the `tuple_pack` does the mismatch appear (5Min inputs + 1Min `dow`).

The fix needs to either:
1. Re-run timeframe resolution after each insertion (multi-pass)
2. Or detect that `tuple_pack` inputs should inherit from the finest timeframe in the full dependency tree, not just immediate inputs

## Error

```
Pipeline error in Upsample strategy, transform 'upsample' (__auto_upsample_tuple_pack_0_to_1Min):
  fill_null_forward has no kernel matching input types (struct<...>)
```

## Workaround

In the definition, explicitly use `resample()` to align timeframes before mixing:
```python
dow_5min = resample(dow, target_timeframe="5Min")
```

## Files

- `packages/epoch-script/src/transforms/compiler/timeframe_resolver.cpp`
- `packages/epoch-script/src/transforms/runtime/execution/strategies/upsample_strategy.cpp`
