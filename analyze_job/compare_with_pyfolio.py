#!/usr/bin/env python3
"""
Compare epoch-folio tearsheet metrics with pyfolio.

This script loads study data from epoch-folio and computes the same metrics
using pyfolio for validation.

Usage:
    python compare_with_pyfolio.py <job_name>

Example:
    python compare_with_pyfolio.py macd_15min
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np

try:
    import pyfolio as pf
    import pyfolio.timeseries as timeseries
    import pyfolio.txn as txn
    import pyfolio.pos as pos
    PYFOLIO_AVAILABLE = True
except ImportError:
    PYFOLIO_AVAILABLE = False
    print("Warning: pyfolio not installed. Install with: pip install pyfolio-reloaded")

try:
    from scipy import stats as scipy_stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    import empyrical as ep
    EMPYRICAL_AVAILABLE = True
except ImportError:
    EMPYRICAL_AVAILABLE = False
    print("Warning: empyrical not installed. Install with: pip install empyrical-reloaded")


def load_study_dataframes(job_name: str) -> dict:
    """Load study dataframes from arrow files."""
    # Try campaigns path first, then research_studies
    base_paths = [
        Path(__file__).parent.parent / "job_data" / "campaigns" / "test_runner" / job_name / "tables",
        Path(__file__).parent.parent / "job_data" / "research_studies" / "test_runner" / job_name / "tables",
    ]

    base_path = None
    for path in base_paths:
        if path.exists():
            base_path = path
            break

    if not base_path:
        print(f"Warning: No tables directory found for {job_name}")
        return {}

    dataframes = {}
    for name in ["account", "positions", "orders"]:
        arrow_path = base_path / f"{name}.arrow"
        if arrow_path.exists():
            import pyarrow as pa
            import pyarrow.ipc as ipc
            with pa.memory_map(str(arrow_path), 'r') as source:
                reader = ipc.open_file(source)
                table = reader.read_all()
                dataframes[name] = table.to_pandas()
            print(f"Loaded {name}: {len(dataframes[name])} rows")
        else:
            print(f"Warning: {arrow_path} not found")

    return dataframes


def load_tearsheet_metrics(job_name: str) -> dict:
    """Load epoch-folio tearsheet metrics from protobuf."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent.parent.parent / "build" / "packages" / "epoch-protos"))

    # Try campaigns path first, then research_studies
    base_paths = [
        Path(__file__).parent.parent / "job_data" / "campaigns" / "test_runner" / job_name / "tearsheets" / "ALL" / "tearsheet.pb",
        Path(__file__).parent.parent / "job_data" / "research_studies" / "test_runner" / job_name / "tearsheets" / "ALL" / "tearsheet.pb",
    ]

    tearsheet_path = None
    for path in base_paths:
        if path.exists():
            tearsheet_path = path
            break

    if not tearsheet_path:
        print(f"Warning: No tearsheet found for {job_name}")
        return {}

    try:
        from epoch_protos import tearsheet_pb2
        with open(tearsheet_path, 'rb') as f:
            ts = tearsheet_pb2.TearSheet()
            ts.ParseFromString(f.read())
        return ts
    except Exception as e:
        print(f"Warning: Could not load tearsheet: {e}")
        return {}


def prepare_pyfolio_data(dataframes: dict) -> tuple:
    """
    Convert epoch-folio dataframes to pyfolio format.

    Returns:
        (returns, positions, transactions)
    """
    account = dataframes.get("account")
    positions_df = dataframes.get("positions")
    orders = dataframes.get("orders")

    # Returns: Daily returns from equity curve
    returns = None
    if account is not None and "equity" in account.columns:
        # Use updated_at as index if available
        if "updated_at" in account.columns:
            equity = account.set_index(pd.to_datetime(account["updated_at"]))["equity"]
        else:
            equity = account["equity"]

        # Resample to daily if intraday
        try:
            equity_daily = equity.groupby(equity.index.date).last()
            equity_daily.index = pd.to_datetime(equity_daily.index)
        except:
            equity_daily = equity

        returns = equity_daily.pct_change().dropna()
        returns.name = None

    # Positions: Need to pivot from log format to wide format
    positions = None
    if positions_df is not None and "asset" in positions_df.columns and "market_value" in positions_df.columns:
        # Pivot positions from log format to wide format (asset as columns)
        if "updated_at" in positions_df.columns:
            positions_df = positions_df.copy()
            positions_df["timestamp"] = pd.to_datetime(positions_df["updated_at"])
            positions_df["date"] = positions_df["timestamp"].dt.date

        # Get last market_value per asset per day (end-of-day snapshot)
        # Use NaN for missing days (not 0) to match epoch-folio's behavior
        # epoch-folio's mean() skips NaN, so averaging only over position days
        try:
            # Group by date and asset, take last value (end-of-day)
            last_mv = positions_df.groupby(["date", "asset"])["market_value"].last().unstack()
            last_mv.index = pd.to_datetime(last_mv.index)

            # Reindex to all account dates, keeping NaN for missing days
            # This matches epoch-folio's behavior where mean() skips NaN
            if account is not None and "index" in account.columns:
                account_dates = pd.to_datetime(account["index"]).dt.tz_localize(None).dt.normalize()
                account_index = pd.DatetimeIndex(account_dates.unique())
                # Reindex without fill_value - missing days stay NaN
                last_mv = last_mv.reindex(account_index)

            # Add cash column from account
            if account is not None and "cash" in account.columns:
                account_indexed = account.set_index(pd.to_datetime(account["index"]).dt.tz_localize(None).dt.normalize())
                last_mv["cash"] = account_indexed["cash"]
            else:
                last_mv["cash"] = 0

            # Don't fill NaN - epoch-folio's mean() skips NaN values
            positions = last_mv
        except Exception as e:
            print(f"Warning: Could not pivot positions: {e}")
            import traceback
            traceback.print_exc()
            positions = None

    # Transactions: From filled orders (timezone-naive to match positions)
    transactions = None
    if orders is not None and "status" in orders.columns:
        filled = orders[orders["status"] == "Filled"].copy()
        if len(filled) > 0:
            transactions = pd.DataFrame({
                "amount": filled["filled_qty"].values,
                "price": filled["filled_price"].values,
                "symbol": filled["asset"].values,
            }, index=pd.to_datetime(filled["updated_at"]).dt.tz_localize(None))

    return returns, positions, transactions


def compute_pyfolio_metrics(returns: pd.Series, positions: pd.DataFrame,
                            transactions: pd.DataFrame, turnover_denom: str = "AGB") -> dict:
    """Compute performance metrics using pyfolio/empyrical."""
    metrics = {}

    if returns is None or len(returns) == 0:
        return metrics

    # Basic stats from empyrical
    if EMPYRICAL_AVAILABLE:
        metrics["Cumulative Returns"] = ep.cum_returns_final(returns)
        metrics["Annual Return"] = ep.annual_return(returns)
        metrics["Annual Volatility"] = ep.annual_volatility(returns)
        metrics["Sharpe Ratio"] = ep.sharpe_ratio(returns)
        metrics["Max Drawdown"] = ep.max_drawdown(returns)
        metrics["Calmar Ratio"] = ep.calmar_ratio(returns)
        metrics["Sortino Ratio"] = ep.sortino_ratio(returns)
        metrics["Omega Ratio"] = ep.omega_ratio(returns)
        metrics["Tail Ratio"] = ep.tail_ratio(returns)
        # Use pyfolio's VaR formula (mean - 2*std), not empyrical's quantile
        metrics["Daily Value at Risk"] = returns.mean() - 2.0 * returns.std()
        metrics["Stability"] = ep.stability_of_timeseries(returns)
        # Use scipy.stats like pyfolio does for skew/kurtosis
        if SCIPY_AVAILABLE:
            metrics["Skew"] = scipy_stats.skew(returns)
            metrics["Kurtosis"] = scipy_stats.kurtosis(returns)
        else:
            metrics["Skew"] = returns.skew()
            metrics["Kurtosis"] = returns.kurtosis()

    # Turnover from pyfolio
    if PYFOLIO_AVAILABLE and positions is not None and transactions is not None:
        try:
            turnover = txn.get_turnover(positions, transactions, denominator=turnover_denom)
            metrics["Daily Turnover"] = turnover.mean()
        except Exception as e:
            print(f"Warning: Could not compute turnover: {e}")

    # Gross leverage - use epoch's approach (average over all account days)
    # pyfolio's get_percent_alloc only works on days with position data
    if positions is not None:
        try:
            # Epoch's formula: abs(positions excluding cash) / total portfolio value
            pos_no_cash = positions.drop("cash", axis=1, errors="ignore")
            gross_exposure = pos_no_cash.abs().sum(axis=1)
            portfolio_value = positions.sum(axis=1)
            gross_lev = gross_exposure / portfolio_value
            gross_lev = gross_lev.replace([np.inf, -np.inf], 0).fillna(0)
            metrics["Gross Leverage"] = gross_lev.mean()
        except Exception as e:
            print(f"Warning: Could not compute gross leverage: {e}")

    return metrics


def extract_epoch_metrics(tearsheet) -> dict:
    """Extract metrics from epoch-folio tearsheet protobuf."""
    metrics = {}

    if not tearsheet:
        return metrics

    # Handle protobuf object
    try:
        # Extract from cards (Key Metrics table)
        for table in tearsheet.tables.tables:
            if table.title in ["Performance Stats", "Key Metrics"]:
                if table.HasField("cards_data"):
                    for cell in table.cards_data.cells:
                        title = cell.title
                        val = cell.value
                        field = val.WhichOneof('value')
                        if field:
                            metrics[title] = getattr(val, field)

            # Extract from summary table (Performance Summary)
            if table.title == "Performance Summary":
                if table.HasField("summary_data"):
                    row_headers = list(table.layout.row_headers)
                    for cell in table.summary_data.cells:
                        if cell.row < len(row_headers):
                            title = row_headers[cell.row]
                            val = cell.value
                            field = val.WhichOneof('value')
                            if field:
                                metrics[title] = getattr(val, field)
    except Exception as e:
        print(f"Warning: Error extracting metrics: {e}")

    return metrics


def compare_metrics(epoch_metrics: dict, pyfolio_metrics: dict) -> pd.DataFrame:
    """Create comparison table of metrics."""
    # Metrics that are stored as percentages in epoch-folio but decimals in pyfolio
    pct_metrics = {
        "Annual Return", "Cumulative Returns", "Annual Volatility",
        "Max Drawdown", "Daily Value at Risk"
    }

    all_keys = set(epoch_metrics.keys()) | set(pyfolio_metrics.keys())

    comparison = []
    for key in sorted(all_keys):
        epoch_val = epoch_metrics.get(key)
        pyfolio_val = pyfolio_metrics.get(key)

        # Normalize percentage metrics for comparison
        epoch_normalized = epoch_val
        pyfolio_normalized = pyfolio_val
        if key in pct_metrics:
            # epoch-folio stores as percentage (27.24), pyfolio as decimal (0.2724)
            if isinstance(pyfolio_val, (int, float)) and not np.isnan(pyfolio_val):
                pyfolio_normalized = pyfolio_val * 100  # Convert to percentage

        # Calculate difference if both are numeric
        diff = None
        pct_diff = None
        if isinstance(epoch_normalized, (int, float)) and isinstance(pyfolio_normalized, (int, float)):
            if not np.isnan(epoch_normalized) and not np.isnan(pyfolio_normalized):
                diff = epoch_normalized - pyfolio_normalized
                if abs(pyfolio_normalized) > 1e-10:
                    pct_diff = (diff / abs(pyfolio_normalized)) * 100

        comparison.append({
            "Metric": key,
            "Epoch-Folio": epoch_val,
            "PyFolio": pyfolio_val,
            "PyFolio (norm)": pyfolio_normalized,
            "Difference": diff,
            "Pct Diff (%)": pct_diff,
        })

    return pd.DataFrame(comparison)


def format_value(val):
    """Format value for display."""
    if val is None:
        return "N/A"
    if isinstance(val, float):
        if abs(val) < 0.01:
            return f"{val:.6f}"
        return f"{val:.4f}"
    return str(val)


def main():
    parser = argparse.ArgumentParser(description="Compare epoch-folio with pyfolio tearsheet")
    parser.add_argument("job_name", help="Name of the job to analyze")
    parser.add_argument("--turnover-denom", default="AGB", choices=["AGB", "portfolio_value"],
                       help="Turnover denominator (default: AGB)")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"Comparing tearsheets for: {args.job_name}")
    print(f"{'='*60}\n")

    # Load data
    dataframes = load_study_dataframes(args.job_name)
    if not dataframes:
        print("Error: No dataframes found")
        return 1

    # Load epoch-folio tearsheet
    tearsheet = load_tearsheet_metrics(args.job_name)
    epoch_metrics = extract_epoch_metrics(tearsheet) if tearsheet else {}

    # Prepare pyfolio data
    returns, positions, transactions = prepare_pyfolio_data(dataframes)

    print(f"\nData Summary:")
    print(f"  Returns: {len(returns) if returns is not None else 0} days")
    print(f"  Positions: {positions.shape if positions is not None else 'N/A'}")
    print(f"  Transactions: {len(transactions) if transactions is not None else 0} trades")

    # Compute pyfolio metrics
    print(f"\nComputing pyfolio metrics (turnover_denom={args.turnover_denom})...")
    pyfolio_metrics = compute_pyfolio_metrics(returns, positions, transactions, args.turnover_denom)

    # Compare
    print(f"\n{'='*60}")
    print("METRIC COMPARISON")
    print(f"{'='*60}\n")

    comparison = compare_metrics(epoch_metrics, pyfolio_metrics)

    # Print formatted table
    print(f"{'Metric':<25} {'Epoch-Folio':>12} {'PyFolio(norm)':>14} {'Diff':>12} {'Pct Diff':>10}")
    print("-" * 76)
    for _, row in comparison.iterrows():
        metric = row["Metric"][:24]
        epoch_val = format_value(row["Epoch-Folio"])
        pyfolio_val = format_value(row["PyFolio (norm)"])
        diff = format_value(row["Difference"])
        pct_diff = f"{row['Pct Diff (%)']:.2f}%" if pd.notna(row["Pct Diff (%)"]) else "N/A"
        print(f"{metric:<25} {epoch_val:>12} {pyfolio_val:>14} {diff:>12} {pct_diff:>10}")

    # Summary statistics
    numeric_diffs = comparison["Pct Diff (%)"].dropna()
    if len(numeric_diffs) > 0:
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"  Metrics compared: {len(numeric_diffs)}")
        print(f"  Mean absolute % difference: {numeric_diffs.abs().mean():.4f}%")
        print(f"  Max absolute % difference: {numeric_diffs.abs().max():.4f}%")

        # Flag significant differences (>1%)
        significant = comparison[comparison["Pct Diff (%)"].abs() > 1]
        if len(significant) > 0:
            print(f"\n  Metrics with >1% difference:")
            for _, row in significant.iterrows():
                print(f"    - {row['Metric']}: {row['Pct Diff (%)']:.2f}%")

    # Also print pyfolio's simple stats for reference
    if PYFOLIO_AVAILABLE and returns is not None:
        print(f"\n{'='*60}")
        print("PYFOLIO PERF STATS (for reference)")
        print(f"{'='*60}\n")
        try:
            perf_stats = pf.timeseries.perf_stats(returns)
            print(perf_stats.to_string())
        except Exception as e:
            print(f"Could not compute perf_stats: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
