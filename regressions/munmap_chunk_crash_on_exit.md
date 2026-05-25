# Regression: munmap_chunk(): invalid pointer on all jobs

**Observed:** 2026-03-28
**Affects:** ALL definitions (campaign and research)
**Severity:** High — all jobs crash after completing

## Symptom

Every `generate_job_data` invocation ends with:
```
Study completed successfully
[job_persister] Wrote manifest to .../manifest.json
munmap_chunk(): invalid pointer
```
Exit code: **-6 (SIGABRT)** — aborted by glibc heap integrity check.

Data is fully written (all `.arrow` files, `config.json`, `manifest.json`, `metadata.json`), but the process crashes during **destructor/cleanup** after the job completes.

## Confirmed on

- `exec_cluster_E01_hold_strict` (campaign, SPY/QQQ/GLD, 2020-2024)
- `exec_cluster_E01_zone_basic` (campaign, 3 assets, 2020-2024)

## Diagnosis

`munmap_chunk(): invalid pointer` is a glibc heap corruption detection error. It indicates:
- A double-free in a destructor, OR
- A use-after-free / corrupted chunk header being unmapped

The crash consistently occurs **after** `job_persister.cpp:356` (manifest write) and **before** normal process exit. This means it's in the destruction path of some long-lived object (study runner, data loader, or similar).

## Likely Cause

Phase 5 refactor (varargs NumericTuple downsample/upsample) or Phase 4/3 (timeframe resolver rewrite). The changes to `DownsampleTransform` / `UpsampleTransform` replaced 4 typed specializations with a single class. If the new class has incorrect ownership semantics (double ownership of Arrow arrays or metadata objects), this would manifest as a heap corruption on destruction.

## What to investigate

1. Run with ASAN build: `python3 scripts/job_registry.py run exec_cluster_E01_hold_strict --asan`
2. Check if crash existed before Phase 5: `git bisect` between the Phase 4 and Phase 5 commits
3. Check `DownsampleTransform` destructor / ownership of `NumericTuple` data

## Impact on this regression test

- Study data is **intact** — all Arrow files and metadata written before crash
- Data quality analysis **can proceed** despite exit code -6
- Treating all exit code -6 failures as "data ok, destruction crash" for now
