#!/usr/bin/env python3
"""
PCA + Rolling OLS Validation Script (ENG-674)

Loads macro factor data from a study's Arrow output, runs sklearn PCA and
statsmodels OLS as ground truth, and compares against the EpochScript PCA
transform output.

Usage:
    python validate_pca.py <job_folder>
    python validate_pca.py <job_folder> --plot        # Show matplotlib charts
    python validate_pca.py <job_folder> --dump-csv    # Export comparison CSV

Requires: pandas, pyarrow, numpy, scikit-learn, statsmodels, scipy
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.ipc as ipc
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats
import statsmodels.api as sm


def load_arrow_table(job_folder: str, asset: str = "^audnzd_fx") -> pd.DataFrame:
    """Load the Arrow IPC market data table for the given asset."""
    base = Path(job_folder)
    # Find the arrow file
    pattern = f"market_data_1d_{asset}*"
    candidates = list(base.rglob("*.arrow")) + list(base.rglob("*.ipc"))
    if not candidates:
        # Try reading from dataframes subfolder
        df_dir = base / "dataframes"
        if df_dir.exists():
            candidates = list(df_dir.glob(f"*{asset}*"))

    for c in candidates:
        if asset.replace("^", "").replace("-", "_") in c.stem.lower().replace("-", "_"):
            with open(c, "rb") as f:
                reader = ipc.open_file(f)
                return reader.read_pandas()

    # Fallback: try query_study_dataframes approach
    raise FileNotFoundError(
        f"Could not find Arrow file for {asset} in {job_folder}. "
        f"Candidates: {[c.name for c in candidates]}"
    )


def extract_factors(df: pd.DataFrame) -> pd.DataFrame:
    """Extract the macro factor columns from the study dataframe.

    Maps internal column names to human-readable factor names.
    """
    # Map from EpochScript internal names to factor labels
    # Arrow files use '#' separator; query_study uses '_'
    # These are the ffill'd values that were fed into the PCA/regression
    col_map = {}
    candidates = {
        "US_2Y": ["t2y#result", "t2y_result"],
        "US_10Y": ["t10y#result", "t10y_result"],
        "BE_5Y": ["be5y#result", "be5y_result"],
        "VIX": ["vix#result", "vix_result"],
        "Oil": ["oil#result", "oil_result"],
        "AU_NZ_Rate_Diff": ["sub_0#result", "sub_0_result", "rate_diff#result", "rate_diff_result"],
        "Iron_Ore": ["iron#result", "iron_result"],
    }
    # Also handle term_spread if present (older versions)
    candidates["Term_Spread"] = ["term_spread#result", "term_spread_result"]
    for name, possible_cols in candidates.items():
        for c in possible_cols:
            if c in df.columns:
                col_map[c] = name
                break

    available = {}
    for col, name in col_map.items():
        if col in df.columns:
            available[name] = df[col].values

    if not available:
        # Try alternative column names
        print("WARNING: Could not find expected factor columns.")
        print(f"Available columns: {sorted(df.columns.tolist())}")
        return pd.DataFrame()

    factors = pd.DataFrame(available, index=df.index if "index" not in df.columns else df["index"])
    return factors


def extract_epoch_pca(df: pd.DataFrame) -> dict:
    """Extract EpochScript PCA outputs for comparison."""
    result = {}

    # Component columns from tuple_index accessor (try both # and _ separator)
    for i in range(4):
        for sep in ["#", "_"]:
            col = f"tuple_index_{i}{sep}result"
            if col in df.columns:
                result[f"PC{i+1}"] = df[col].values
                break

    # Explained variance
    for col in ["pca_out#explained_variance_ratio", "pca_out_explained_variance_ratio"]:
        if col in df.columns:
            result["explained_var"] = df[col].values
            break

    # Regression outputs (try both # and _ separator)
    for base, name in [
        ("reg", "r_squared"),
        ("reg", "residual"),
        ("reg", "intercept"),
    ]:
        for sep in ["#", "_"]:
            col = f"{base}{sep}{name}"
            if col in df.columns:
                result[name] = df[col].values
                break

    return result


def apply_expanding_zscore(factors: pd.DataFrame, min_samples: int = 252) -> pd.DataFrame:
    """Apply expanding z-score to each factor, matching EpochScript ml_zscore.

    Each row is standardized using mean/std from all prior data (expanding window).
    Returns NaN for rows with insufficient data.
    """
    result = pd.DataFrame(np.nan, index=factors.index, columns=factors.columns)

    for i in range(len(factors)):
        if i + 1 < min_samples:
            continue
        window = factors.iloc[:i+1]
        valid = window.dropna()
        if len(valid) < min_samples:
            continue

        row = factors.iloc[i]
        if row.isna().any():
            continue

        means = valid.mean()
        stds = valid.std(ddof=1)  # arma::stddev uses ddof=1

        for col in factors.columns:
            if stds[col] > 1e-10:
                result.loc[result.index[i], col] = (row[col] - means[col]) / stds[col]
            else:
                result.loc[result.index[i], col] = row[col] - means[col]

    return result


def run_rolling_pca(factors: pd.DataFrame, n_components: int = 4,
                    window_size: int = 252, step: int = 21,
                    min_samples: int = 200,
                    pre_scaled: pd.DataFrame = None) -> pd.DataFrame:
    """Run sklearn PCA with rolling window, matching EpochScript behavior.

    If pre_scaled is provided, uses those values (matching ml_zscore → pca pipeline).
    Otherwise uses StandardScaler within each PCA window (old behavior).

    Returns DataFrame with PC1-PC4 columns + explained_variance_ratio.
    """
    n = len(factors)
    data = pre_scaled if pre_scaled is not None else factors

    # Output arrays
    components = np.full((n, n_components), np.nan)
    explained_var = np.full(n, np.nan)

    # Track last training step
    last_train_idx = -step  # Force training on first valid window
    pca_model = None
    scaler = None  # Only used when no pre_scaled

    for i in range(n):
        # Check if we have enough non-NaN data
        window_start = max(0, i - window_size + 1)
        window_data = data.iloc[window_start:i+1]
        valid = window_data.dropna()

        if len(valid) < min_samples:
            continue

        # Retrain PCA every `step` bars
        if pca_model is None or (i - last_train_idx) >= step:
            if pre_scaled is not None:
                # Data is already z-scored; PCA only mean-centers (like epoch)
                pca_model = PCA(n_components=min(n_components, valid.shape[1]))
                pca_model.fit(valid.values)
            else:
                # Old behavior: StandardScaler + PCA coupled
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(valid.values)
                pca_model = PCA(n_components=min(n_components, X_scaled.shape[1]))
                pca_model.fit(X_scaled)
            last_train_idx = i

        # Transform current observation
        row = data.iloc[i:i+1]
        if row.isna().any(axis=1).iloc[0]:
            continue

        if pre_scaled is not None:
            pc_values = pca_model.transform(row.values)[0]
        else:
            X_current = scaler.transform(row.values)
            pc_values = pca_model.transform(X_current)[0]

        components[i, :len(pc_values)] = pc_values
        explained_var[i] = pca_model.explained_variance_ratio_.sum()

    result = pd.DataFrame(index=factors.index)
    for j in range(n_components):
        result[f"PC{j+1}"] = components[:, j]
    result["explained_var"] = explained_var

    return result


def run_rolling_pca_expanding(factors: pd.DataFrame, n_components: int = 4,
                              step: int = 21, min_samples: int = 252,
                              pre_scaled: pd.DataFrame = None) -> pd.DataFrame:
    """Run sklearn PCA with expanding window.

    If pre_scaled is provided, uses those values (matching ml_zscore → pca pipeline).
    """
    n = len(factors)
    data = pre_scaled if pre_scaled is not None else factors
    components = np.full((n, n_components), np.nan)
    explained_var = np.full(n, np.nan)

    last_train_idx = -step
    pca_model = None
    scaler = None

    for i in range(n):
        # Expanding: use all data from start to current
        window_data = data.iloc[:i+1]
        valid = window_data.dropna()

        if len(valid) < min_samples:
            continue

        if pca_model is None or (i - last_train_idx) >= step:
            if pre_scaled is not None:
                pca_model = PCA(n_components=min(n_components, valid.shape[1]))
                pca_model.fit(valid.values)
            else:
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(valid.values)
                pca_model = PCA(n_components=min(n_components, X_scaled.shape[1]))
                pca_model.fit(X_scaled)
            last_train_idx = i

        row = data.iloc[i:i+1]
        if row.isna().any(axis=1).iloc[0]:
            continue

        if pre_scaled is not None:
            pc_values = pca_model.transform(row.values)[0]
        else:
            X_current = scaler.transform(row.values)
            pc_values = pca_model.transform(X_current)[0]

        components[i, :len(pc_values)] = pc_values
        explained_var[i] = pca_model.explained_variance_ratio_.sum()

    result = pd.DataFrame(index=factors.index)
    for j in range(n_components):
        result[f"PC{j+1}"] = components[:, j]
    result["explained_var"] = explained_var
    return result


def run_rolling_ols(y: np.ndarray, X: np.ndarray, window: int = 252) -> dict:
    """Run rolling OLS regression: y = X @ beta + intercept.

    Returns dict with r_squared, residual, intercept, coefficients arrays.
    """
    n = len(y)
    r_squared = np.full(n, np.nan)
    residual = np.full(n, np.nan)
    intercept = np.full(n, np.nan)
    coefficients = np.full((n, X.shape[1]), np.nan)

    for i in range(window - 1, n):
        start = i - window + 1
        y_win = y[start:i+1]
        X_win = X[start:i+1]

        # Skip if any NaN
        mask = ~(np.isnan(y_win) | np.isnan(X_win).any(axis=1))
        if mask.sum() < X.shape[1] + 2:
            continue

        y_clean = y_win[mask]
        X_clean = X_win[mask]

        # Add constant for intercept
        X_const = sm.add_constant(X_clean)

        try:
            model = sm.OLS(y_clean, X_const).fit()
            r_squared[i] = model.rsquared
            intercept[i] = model.params[0]
            coefficients[i] = model.params[1:]

            # Predict for current observation
            x_current = np.concatenate([[1.0], X[i]])
            if not np.isnan(x_current).any():
                pred = x_current @ model.params
                residual[i] = y[i] - pred
        except Exception:
            continue

    return {
        "r_squared": r_squared,
        "residual": residual,
        "intercept": intercept,
        "coefficients": coefficients,
    }


def compare_components(epoch_pca: dict, sklearn_pca: pd.DataFrame) -> dict:
    """Compare EpochScript PCA output vs sklearn PCA.

    Handles sign ambiguity by checking both +/- correlation.
    Returns comparison metrics.
    """
    results = {}

    for i in range(4):
        epoch_key = f"PC{i+1}"
        if epoch_key not in epoch_pca or epoch_key not in sklearn_pca.columns:
            continue

        ep = epoch_pca[epoch_key]
        sk = sklearn_pca[epoch_key].values

        # Find valid overlap
        mask = ~(np.isnan(ep) | np.isnan(sk))
        if mask.sum() < 10:
            results[epoch_key] = {"status": "insufficient_data", "valid_count": int(mask.sum())}
            continue

        ep_valid = ep[mask]
        sk_valid = sk[mask]

        # Correlation (handle sign ambiguity)
        corr_pos = np.corrcoef(ep_valid, sk_valid)[0, 1]
        corr_neg = np.corrcoef(ep_valid, -sk_valid)[0, 1]

        if abs(corr_neg) > abs(corr_pos):
            best_corr = corr_neg
            sign_flip = True
        else:
            best_corr = corr_pos
            sign_flip = False

        # Check for discontinuities (sign flips within series)
        ep_diff = np.diff(ep_valid)
        large_jumps = np.sum(np.abs(ep_diff) > 3 * np.nanstd(ep_diff))

        sk_diff = np.diff(sk_valid)
        sk_large_jumps = np.sum(np.abs(sk_diff) > 3 * np.nanstd(sk_diff))

        results[epoch_key] = {
            "correlation": round(best_corr, 4),
            "sign_flipped": sign_flip,
            "valid_count": int(mask.sum()),
            "epoch_jumps_3sigma": int(large_jumps),
            "sklearn_jumps_3sigma": int(sk_large_jumps),
            "epoch_std": round(np.nanstd(ep_valid), 4),
            "sklearn_std": round(np.nanstd(sk_valid), 4),
        }

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate PCA transform against sklearn (ENG-674)")
    parser.add_argument("job_folder", help="Path to research study output folder")
    parser.add_argument("--plot", action="store_true", help="Show matplotlib charts")
    parser.add_argument("--dump-csv", action="store_true", help="Export comparison CSV")
    parser.add_argument("--window-type", choices=["rolling", "expanding"], default="rolling",
                        help="PCA window type (default: rolling)")
    parser.add_argument("--window-size", type=int, default=252, help="PCA window size")
    parser.add_argument("--ols-window", type=int, default=252, help="OLS regression window")
    parser.add_argument("--step", type=int, default=21, help="PCA retrain step (bars)")
    args = parser.parse_args()

    print(f"=" * 70)
    print(f"PCA VALIDATION (ENG-674)")
    print(f"=" * 70)
    print(f"Study: {args.job_folder}")
    print(f"PCA: {args.window_type}, window={args.window_size}, step={args.step}")
    print(f"OLS: rolling, window={args.ols_window}")
    print()

    # ── 1. Load study data ──────────────────────────────────────────────
    print("Loading study data...")
    try:
        df = load_arrow_table(args.job_folder)
    except FileNotFoundError:
        # Fallback: use query_study_dataframes
        import subprocess
        result = subprocess.run(
            ["python3", str(Path(__file__).parent / "query_study_dataframes.py"),
             args.job_folder, "-q",
             'SELECT * FROM "market_data_1d_^audnzd_fx"'],
            capture_output=True, text=True
        )
        print("Arrow load failed. Use --dump-csv with query_study_dataframes instead.")
        sys.exit(1)

    print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")

    # ── 2. Extract factors ──────────────────────────────────────────────
    factors = extract_factors(df)
    if factors.empty:
        print("ERROR: Could not extract factor data from study output.")
        sys.exit(1)

    print(f"  Factors: {factors.columns.tolist()}")
    print(f"  Valid rows per factor:")
    for col in factors.columns:
        valid = factors[col].notna().sum()
        print(f"    {col:20s}: {valid:5d} / {len(factors)} ({valid/len(factors)*100:.1f}%)")
    print()

    # ── 3. Extract EpochScript PCA outputs ──────────────────────────────
    epoch_pca = extract_epoch_pca(df)
    epoch_pc_count = sum(1 for k in epoch_pca if k.startswith("PC"))
    print(f"  EpochScript PCA components found: {epoch_pc_count}")
    if "explained_var" in epoch_pca:
        valid_ev = np.sum(~np.isnan(epoch_pca["explained_var"]))
        print(f"  EpochScript explained_var valid: {valid_ev}")
    print()

    # ── 4. Apply expanding z-score (matching epoch ml_zscore) ───────────
    print("Applying expanding z-score (matching epoch ml_zscore pipeline)...")
    factors_zscored = apply_expanding_zscore(factors, min_samples=args.window_size)
    valid_zscored = factors_zscored.dropna().shape[0]
    print(f"  Z-scored valid rows: {valid_zscored} / {len(factors_zscored)}")

    # ── 5. Run sklearn PCA on z-scored data ───────────────────────────
    print("Running sklearn PCA (on pre-z-scored data, matching epoch pipeline)...")
    if args.window_type == "rolling":
        sklearn_pca = run_rolling_pca(
            factors, n_components=4,
            window_size=args.window_size,
            step=args.step,
            min_samples=200,
            pre_scaled=factors_zscored
        )
    else:
        sklearn_pca = run_rolling_pca_expanding(
            factors, n_components=4,
            step=args.step,
            min_samples=args.window_size,
            pre_scaled=factors_zscored
        )

    valid_pcs = sklearn_pca["PC1"].notna().sum()
    print(f"  sklearn PCA valid rows: {valid_pcs} / {len(sklearn_pca)}")
    print()

    # ── 6. Compare PCA outputs ──────────────────────────────────────────
    print("=" * 70)
    print("PCA COMPONENT COMPARISON: EpochScript vs sklearn")
    print("=" * 70)

    comparison = compare_components(epoch_pca, sklearn_pca)
    for pc, metrics in comparison.items():
        if metrics.get("status") == "insufficient_data":
            print(f"  {pc}: insufficient data ({metrics['valid_count']} valid)")
            continue

        corr = metrics["correlation"]
        flip = "YES" if metrics["sign_flipped"] else "no"
        ej = metrics["epoch_jumps_3sigma"]
        sj = metrics["sklearn_jumps_3sigma"]

        status = "OK" if abs(corr) > 0.9 and ej < sj * 3 else "WARN" if abs(corr) > 0.7 else "FAIL"

        print(f"  {pc}: corr={corr:+.4f}  sign_flip={flip:3s}  "
              f"epoch_jumps={ej:3d}  sklearn_jumps={sj:3d}  [{status}]")
    print()

    # ── 7. Run sklearn OLS for comparison ───────────────────────────────
    print("Running sklearn rolling OLS...")

    audnzd = None
    for col in ["src#c", "src_c"]:
        if col in df.columns:
            audnzd = df[col].values
            break
    if audnzd is None:
        print("  WARNING: Could not find AUDNZD spot price column")
    else:
        # Use sklearn PCA components as regressors
        X_sklearn = sklearn_pca[["PC1", "PC2", "PC3", "PC4"]].values
        ols_sklearn = run_rolling_ols(audnzd, X_sklearn, window=args.ols_window)

        # Also run OLS on EpochScript PCA components
        if epoch_pc_count == 4:
            X_epoch = np.column_stack([epoch_pca[f"PC{i+1}"] for i in range(4)])
            ols_epoch_pca = run_rolling_ols(audnzd, X_epoch, window=args.ols_window)
        else:
            ols_epoch_pca = None

        print()
        print("=" * 70)
        print("ROLLING OLS R² COMPARISON BY YEAR")
        print("=" * 70)

        # Build comparison dataframe
        dates = df["index"] if "index" in df.columns else df.index
        if hasattr(dates, "dt"):
            years = dates.dt.year
        else:
            years = pd.to_datetime(dates).year

        print(f"  {'Year':>6s}  {'sklearn_PCA→OLS':>15s}  ", end="")
        if ols_epoch_pca:
            print(f"{'epoch_PCA→pyOLS':>15s}  ", end="")
        if "r_squared" in epoch_pca:
            print(f"{'epoch_full':>15s}", end="")
        print()
        print(f"  {'':>6s}  {'avg R²':>15s}  ", end="")
        if ols_epoch_pca:
            print(f"{'avg R²':>15s}  ", end="")
        if "r_squared" in epoch_pca:
            print(f"{'avg R²':>15s}", end="")
        print()
        print("  " + "-" * 60)

        for year in sorted(years.unique()):
            mask = years == year

            sk_r2 = ols_sklearn["r_squared"][mask]
            sk_valid = sk_r2[~np.isnan(sk_r2)]
            sk_avg = np.mean(sk_valid) if len(sk_valid) > 0 else np.nan

            print(f"  {year:>6.0f}  {sk_avg:>15.3f}  ", end="")

            if ols_epoch_pca:
                ep_r2 = ols_epoch_pca["r_squared"][mask]
                ep_valid = ep_r2[~np.isnan(ep_r2)]
                ep_avg = np.mean(ep_valid) if len(ep_valid) > 0 else np.nan
                flag = " ⚠" if ep_avg < -1 else ""
                print(f"{ep_avg:>15.3f}{flag}  ", end="")

            if "r_squared" in epoch_pca:
                full_r2 = epoch_pca["r_squared"][mask]
                full_valid = full_r2[~np.isnan(full_r2)]
                full_avg = np.mean(full_valid) if len(full_valid) > 0 else np.nan
                flag = " ⚠" if full_avg < -1 else ""
                print(f"{full_avg:>15.3f}{flag}", end="")

            print()

        # Summary stats
        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)

        sk_all = ols_sklearn["r_squared"]
        sk_valid_all = sk_all[~np.isnan(sk_all)]
        print(f"  sklearn PCA → sklearn OLS:")
        print(f"    Mean R²:     {np.mean(sk_valid_all):.4f}")
        print(f"    Median R²:   {np.median(sk_valid_all):.4f}")
        print(f"    Min R²:      {np.min(sk_valid_all):.4f}")
        print(f"    Max R²:      {np.max(sk_valid_all):.4f}")
        print(f"    R² < 0:      {np.sum(sk_valid_all < 0)} / {len(sk_valid_all)}")
        print(f"    R² < -1:     {np.sum(sk_valid_all < -1)} / {len(sk_valid_all)}")

        if "r_squared" in epoch_pca:
            ep_all = epoch_pca["r_squared"]
            ep_valid_all = ep_all[~np.isnan(ep_all)]
            print(f"\n  EpochScript PCA → EpochScript OLS:")
            print(f"    Mean R²:     {np.mean(ep_valid_all):.4f}")
            print(f"    Median R²:   {np.median(ep_valid_all):.4f}")
            print(f"    Min R²:      {np.min(ep_valid_all):.6e}")
            print(f"    Max R²:      {np.max(ep_valid_all):.4f}")
            print(f"    R² < 0:      {np.sum(ep_valid_all < 0)} / {len(ep_valid_all)}")
            print(f"    R² < -1:     {np.sum(ep_valid_all < -1)} / {len(ep_valid_all)}")

    # ── 8. Optional: dump CSV ───────────────────────────────────────────
    if args.dump_csv:
        out_path = Path(args.job_folder) / "pca_validation.csv"
        export = pd.DataFrame(index=range(len(df)))
        export["date"] = dates.values if hasattr(dates, "values") else dates
        export["audnzd"] = audnzd

        for col in factors.columns:
            export[f"factor_{col}"] = factors[col].values

        for i in range(4):
            export[f"sklearn_PC{i+1}"] = sklearn_pca[f"PC{i+1}"].values
            if f"PC{i+1}" in epoch_pca:
                export[f"epoch_PC{i+1}"] = epoch_pca[f"PC{i+1}"]

        export["sklearn_r2"] = ols_sklearn["r_squared"]
        export["sklearn_residual"] = ols_sklearn["residual"]
        if "r_squared" in epoch_pca:
            export["epoch_r2"] = epoch_pca["r_squared"]
        if "residual" in epoch_pca:
            export["epoch_residual"] = epoch_pca["residual"]

        export.to_csv(out_path, index=False)
        print(f"\n  Exported: {out_path}")

    # ── 9. Optional: plot ───────────────────────────────────────────────
    if args.plot:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt

            fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
            dates_plot = pd.to_datetime(dates)

            # Chart 1: R² comparison
            ax = axes[0]
            sk_r2_clipped = np.clip(ols_sklearn["r_squared"], -2, 1)
            ax.plot(dates_plot, sk_r2_clipped, label="sklearn", alpha=0.7, linewidth=0.8)
            if "r_squared" in epoch_pca:
                ep_r2_clipped = np.clip(epoch_pca["r_squared"], -2, 1)
                ax.plot(dates_plot, ep_r2_clipped, label="EpochScript", alpha=0.7, linewidth=0.8)
            ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
            ax.set_ylabel("R² (clipped to [-2, 1])")
            ax.set_title("Rolling OLS R²: sklearn vs EpochScript")
            ax.legend()

            # Chart 2: PC1 comparison
            ax = axes[1]
            ax.plot(dates_plot, sklearn_pca["PC1"].values, label="sklearn PC1", alpha=0.7)
            if "PC1" in epoch_pca:
                ax.plot(dates_plot, epoch_pca["PC1"], label="EpochScript PC1", alpha=0.7)
            ax.set_ylabel("PC1 value")
            ax.set_title("PC1: sklearn vs EpochScript")
            ax.legend()

            # Chart 3: Spot vs Fair Value (sklearn)
            ax = axes[2]
            ax.plot(dates_plot, audnzd, label="AUDNZD Spot", color="black", linewidth=0.8)
            fair_sklearn = audnzd - ols_sklearn["residual"]
            ax.plot(dates_plot, fair_sklearn, label="sklearn Fair Value", color="blue", alpha=0.7)
            ax.set_ylabel("AUDNZD")
            ax.set_title("AUDNZD: Spot vs sklearn Fair Value")
            ax.legend()

            plt.tight_layout()
            out_png = Path(args.job_folder) / "pca_validation.png"
            plt.savefig(out_png, dpi=150)
            print(f"\n  Plot saved: {out_png}")
        except ImportError:
            print("\n  matplotlib not available, skipping plots")


if __name__ == "__main__":
    main()
