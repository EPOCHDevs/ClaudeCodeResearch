"""
Python reference implementation of futures continuation adjustment.

Mirrors the exact math from our C++ code in:
  - backward.h  (BackwardAdjustmentDirection)
  - forward.h   (ForwardAdjustmentDirection)
  - adjustment_style.h  (PanamaCanal + Ratio)

Used to cross-validate against open-source libraries and compute
correct expected values for C++ unit tests.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple


# ============================================================================
# Adjustment Styles (mirrors adjustment_style.h)
# ============================================================================

class PanamaCanal:
    """Additive adjustment: factor = back - front, accumulated via sum."""

    def __init__(self):
        self.adjustment_factor = 0.0
        self.accumulated = 0.0

    def compute_factor(self, front_close: float, back_close: float):
        self.adjustment_factor = back_close - front_close
        self.accumulated += self.adjustment_factor

    def apply_cumulative(self, value: float) -> float:
        return value + self.accumulated


class Ratio:
    """Multiplicative adjustment: factor = back / front, accumulated via product."""

    def __init__(self):
        self.adjustment_factor = 1.0
        self.accumulated = 1.0

    def compute_factor(self, front_close: float, back_close: float):
        self.adjustment_factor = back_close / front_close
        self.accumulated *= self.adjustment_factor

    def apply_cumulative(self, value: float) -> float:
        return value * self.accumulated


# ============================================================================
# Data Model
# ============================================================================

@dataclass
class BuiltBars:
    """Result of BuildBars phase (FirstOfMonth rollover)."""
    dates: list
    contracts: list          # active contract symbol per output bar
    opens: list
    highs: list
    lows: list
    closes: list
    volumes: list
    ois: list
    roll_ranges: List[Tuple[int, int]]  # (start, length) per contract segment

    # Parallel arrays for the BACK (deferred) contract at each output position
    back_opens: list = field(default_factory=list)
    back_highs: list = field(default_factory=list)
    back_lows: list = field(default_factory=list)
    back_closes: list = field(default_factory=list)


def build_bars(contracts, dates, opens, highs, lows, closes, volumes, ois):
    """
    Simulate BuildBars with FirstOfMonth rollover.

    Input: multi-contract DataFrame (multiple contracts on overlap days).
    Output: single-contract per day, with rollRange segments.

    Logic: group by date, for each date keep the FIRST contract (front by sort order).
    On overlap days, the earlier-expiry contract is kept until its last trading day.
    """
    df = pd.DataFrame({
        'contract': contracts,
        'date': pd.to_datetime(dates),
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volumes,
        'oi': ois,
    })

    # Get unique contracts in order of first appearance
    contract_order = list(dict.fromkeys(contracts))

    # For each date, pick front contract (earliest in contract_order that has data)
    out_dates = []
    out_contracts = []
    out_opens = []
    out_highs = []
    out_lows = []
    out_closes = []
    out_volumes = []
    out_ois = []
    # Back contract data (for adjustment factor computation)
    out_back_closes = []
    out_back_opens = []
    out_back_highs = []
    out_back_lows = []

    for date, group in df.groupby('date', sort=True):
        available = group.set_index('contract')
        # Pick front contract: earliest in contract_order
        front = None
        back = None
        for i, c in enumerate(contract_order):
            if c in available.index:
                if front is None:
                    front = c
                elif back is None:
                    back = c
                    break

        row = available.loc[front]
        out_dates.append(date)
        out_contracts.append(front)
        out_opens.append(row['open'])
        out_highs.append(row['high'])
        out_lows.append(row['low'])
        out_closes.append(row['close'])
        out_volumes.append(row['volume'])
        out_ois.append(row['oi'])

        # Back contract data
        if back and back in available.index:
            back_row = available.loc[back]
            out_back_closes.append(back_row['close'])
            out_back_opens.append(back_row['open'])
            out_back_highs.append(back_row['high'])
            out_back_lows.append(back_row['low'])
        else:
            out_back_closes.append(np.nan)
            out_back_opens.append(np.nan)
            out_back_highs.append(np.nan)
            out_back_lows.append(np.nan)

    # Compute roll ranges (segments of same contract)
    roll_ranges = []
    if out_contracts:
        seg_start = 0
        seg_contract = out_contracts[0]
        for i in range(1, len(out_contracts)):
            if out_contracts[i] != seg_contract:
                roll_ranges.append((seg_start, i - seg_start))
                seg_start = i
                seg_contract = out_contracts[i]
        roll_ranges.append((seg_start, len(out_contracts) - seg_start))

    return BuiltBars(
        dates=out_dates,
        contracts=out_contracts,
        opens=out_opens,
        highs=out_highs,
        lows=out_lows,
        closes=out_closes,
        volumes=out_volumes,
        ois=out_ois,
        roll_ranges=roll_ranges,
        back_opens=out_back_opens,
        back_highs=out_back_highs,
        back_lows=out_back_lows,
        back_closes=out_back_closes,
    )


def build_bars_intraday(contracts, dates, opens, highs, lows, closes, volumes, ois):
    """
    BuildBars for intraday data. Same logic but preserves intraday bars.

    For overlap days, pick front contract and keep all its intraday bars.
    Back contract data is populated at all intraday positions.
    """
    df = pd.DataFrame({
        'contract': contracts,
        'date': pd.to_datetime(dates),
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volumes,
        'oi': ois,
    })

    contract_order = list(dict.fromkeys(contracts))
    df['day'] = df['date'].dt.date

    out_dates = []
    out_contracts = []
    out_opens = []
    out_highs = []
    out_lows = []
    out_closes = []
    out_volumes = []
    out_ois = []
    out_back_closes = []
    out_back_opens = []
    out_back_highs = []
    out_back_lows = []

    for day, day_group in df.groupby('day', sort=True):
        available_contracts = day_group['contract'].unique()
        # Pick front contract
        front = None
        back = None
        for c in contract_order:
            if c in available_contracts:
                if front is None:
                    front = c
                elif back is None:
                    back = c
                    break

        front_bars = day_group[day_group['contract'] == front].sort_values('date')
        back_bars = None
        if back:
            back_bars = day_group[day_group['contract'] == back].sort_values('date')

        for _, row in front_bars.iterrows():
            out_dates.append(row['date'])
            out_contracts.append(front)
            out_opens.append(row['open'])
            out_highs.append(row['high'])
            out_lows.append(row['low'])
            out_closes.append(row['close'])
            out_volumes.append(row['volume'])
            out_ois.append(row['oi'])

            # Find matching back bar (same timestamp or last bar of day)
            if back_bars is not None and len(back_bars) > 0:
                # Match by timestamp
                matching = back_bars[back_bars['date'] == row['date']]
                if len(matching) > 0:
                    br = matching.iloc[0]
                    out_back_closes.append(br['close'])
                    out_back_opens.append(br['open'])
                    out_back_highs.append(br['high'])
                    out_back_lows.append(br['low'])
                else:
                    out_back_closes.append(np.nan)
                    out_back_opens.append(np.nan)
                    out_back_highs.append(np.nan)
                    out_back_lows.append(np.nan)
            else:
                out_back_closes.append(np.nan)
                out_back_opens.append(np.nan)
                out_back_highs.append(np.nan)
                out_back_lows.append(np.nan)

    # Compute roll ranges
    roll_ranges = []
    if out_contracts:
        seg_start = 0
        seg_contract = out_contracts[0]
        for i in range(1, len(out_contracts)):
            if out_contracts[i] != seg_contract:
                roll_ranges.append((seg_start, i - seg_start))
                seg_start = i
                seg_contract = out_contracts[i]
        roll_ranges.append((seg_start, len(out_contracts) - seg_start))

    return BuiltBars(
        dates=out_dates,
        contracts=out_contracts,
        opens=out_opens,
        highs=out_highs,
        lows=out_lows,
        closes=out_closes,
        volumes=out_volumes,
        ois=out_ois,
        roll_ranges=roll_ranges,
        back_opens=out_back_opens,
        back_highs=out_back_highs,
        back_lows=out_back_lows,
        back_closes=out_back_closes,
    )


# ============================================================================
# Adjustment Directions (mirrors backward.h / forward.h)
# ============================================================================

def backward_adjust(bars: BuiltBars, StyleClass):
    """
    Backward adjustment: most recent segment unchanged, iterate backward.

    Mirrors backward.h:
      - Copy last segment as-is
      - For each segment from rbegin+1 to rend:
        - boundary = end - 1 (last bar of current segment)
        - Compute factor from closeFront[end-1] and closeBack[end-1]
        - Apply cumulative factor to all OHLC columns of current segment
    """
    n = len(bars.closes)
    adj_closes = list(bars.closes)
    adj_opens = list(bars.opens)
    adj_highs = list(bars.highs)
    adj_lows = list(bars.lows)

    roll_ranges = bars.roll_ranges
    close_front = bars.closes       # front contract close at each position
    close_back = bars.back_closes   # back contract close at each position

    # Copy last segment as-is (already in adj_* from initialization)
    # ... nothing to do, adj_* starts as copy of raw front data

    style = StyleClass()

    # Iterate segments in reverse, skip last
    for seg_idx in range(len(roll_ranges) - 2, -1, -1):
        start, length = roll_ranges[seg_idx]
        end = start + length

        # Boundary = last bar of this segment
        boundary = end - 1

        # Compute factor from close at boundary
        style.compute_factor(close_front[boundary], close_back[boundary])

        # Apply cumulative to this segment
        for i in range(start, end):
            adj_closes[i] = style.apply_cumulative(bars.closes[i])
            adj_opens[i] = style.apply_cumulative(bars.opens[i])
            adj_highs[i] = style.apply_cumulative(bars.highs[i])
            adj_lows[i] = style.apply_cumulative(bars.lows[i])

    return adj_opens, adj_highs, adj_lows, adj_closes


def forward_adjust(bars: BuiltBars, StyleClass):
    """
    Forward adjustment: first segment unchanged, iterate forward.

    Mirrors forward.h:
      - Copy first segment as-is
      - For each segment from begin+1 to end:
        - boundary = start - 1 (last bar of previous segment)
        - Compute factor from closeFront[start-1] and closeBack[start-1]
        - Apply cumulative factor to all OHLC columns of current segment
    """
    n = len(bars.closes)
    adj_closes = list(bars.closes)
    adj_opens = list(bars.opens)
    adj_highs = list(bars.highs)
    adj_lows = list(bars.lows)

    roll_ranges = bars.roll_ranges
    close_front = bars.closes
    close_back = bars.back_closes

    style = StyleClass()

    # First segment as-is, iterate from second onward
    for seg_idx in range(1, len(roll_ranges)):
        start, length = roll_ranges[seg_idx]

        # Boundary = last bar of PREVIOUS segment
        boundary = start - 1

        style.compute_factor(close_front[boundary], close_back[boundary])

        for i in range(start, start + length):
            adj_closes[i] = style.apply_cumulative(bars.closes[i])
            adj_opens[i] = style.apply_cumulative(bars.opens[i])
            adj_highs[i] = style.apply_cumulative(bars.highs[i])
            adj_lows[i] = style.apply_cumulative(bars.lows[i])

    return adj_opens, adj_highs, adj_lows, adj_closes


# ============================================================================
# Convenience: run all 4 methods
# ============================================================================

def adjust_all(bars: BuiltBars):
    """Run all 4 adjustment methods and return dict of results."""
    results = {}

    for direction_name, direction_fn in [('Backward', backward_adjust),
                                          ('Forward', forward_adjust)]:
        for style_name, style_class in [('Panama', PanamaCanal),
                                         ('Ratio', Ratio)]:
            key = f"{direction_name}{style_name}"
            adj_o, adj_h, adj_l, adj_c = direction_fn(bars, style_class)
            results[key] = {
                'opens': adj_o,
                'highs': adj_h,
                'lows': adj_l,
                'closes': adj_c,
            }

    return results


# ============================================================================
# Test Data (matches C++ test helpers exactly)
# ============================================================================

def make_three_contract_daily():
    """Matches make_three_contract_daily_df() in C++ test."""
    return dict(
        contracts=["ESU23", "ESU23", "ESZ23", "ESZ23", "ESH24", "ESH24"],
        dates=["2023-11-01", "2023-11-02", "2023-11-02", "2023-11-03",
               "2023-11-03", "2023-11-04"],
        opens=[4500, 4510, 4515, 4525, 4530, 4540],
        highs=[4520, 4530, 4535, 4545, 4550, 4560],
        lows=[4490, 4500, 4505, 4515, 4520, 4530],
        closes=[4510, 4520, 4525, 4535, 4530, 4540],
        volumes=[1000, 1100, 800, 900, 700, 800],
        ois=[500, 510, 400, 410, 300, 310],
    )


def make_three_contract_5min():
    """Matches make_three_contract_intraday_df() in C++ test."""
    return dict(
        contracts=[
            "ESU23", "ESU23",   # Nov 1
            "ESU23", "ESU23",   # Nov 2
            "ESZ23", "ESZ23",   # Nov 2
            "ESZ23", "ESZ23",   # Nov 3
            "ESH24", "ESH24",   # Nov 3
            "ESH24", "ESH24",   # Nov 4
        ],
        dates=[
            "2023-11-01 09:30:00", "2023-11-01 09:35:00",
            "2023-11-02 09:30:00", "2023-11-02 09:35:00",
            "2023-11-02 09:30:00", "2023-11-02 09:35:00",
            "2023-11-03 09:30:00", "2023-11-03 09:35:00",
            "2023-11-03 09:30:00", "2023-11-03 09:35:00",
            "2023-11-04 09:30:00", "2023-11-04 09:35:00",
        ],
        opens=[4500, 4505, 4510, 4515, 4515, 4522, 4525, 4532, 4530, 4527, 4540, 4537],
        highs=[4510, 4515, 4520, 4525, 4525, 4530, 4535, 4540, 4540, 4535, 4550, 4545],
        lows=[4495, 4500, 4505, 4510, 4510, 4518, 4520, 4528, 4525, 4523, 4535, 4533],
        closes=[4505, 4510, 4515, 4520, 4522, 4525, 4532, 4535, 4527, 4530, 4537, 4540],
        volumes=[100, 200, 110, 210, 90, 180, 95, 190, 80, 170, 100, 200],
        ois=[50, 55, 56, 60, 40, 44, 41, 45, 30, 34, 31, 35],
    )


def make_three_contract_1min():
    """Matches make_three_contract_1min_df() in C++ test."""
    return dict(
        contracts=[
            "ESU23", "ESU23", "ESU23",   # Nov 1
            "ESU23", "ESU23", "ESU23",   # Nov 2
            "ESZ23", "ESZ23", "ESZ23",   # Nov 2
            "ESZ23", "ESZ23", "ESZ23",   # Nov 3
            "ESH24", "ESH24", "ESH24",   # Nov 3
            "ESH24", "ESH24", "ESH24",   # Nov 4
        ],
        dates=[
            "2023-11-01 09:30:00", "2023-11-01 09:31:00", "2023-11-01 09:32:00",
            "2023-11-02 09:30:00", "2023-11-02 09:31:00", "2023-11-02 09:32:00",
            "2023-11-02 09:30:00", "2023-11-02 09:31:00", "2023-11-02 09:32:00",
            "2023-11-03 09:30:00", "2023-11-03 09:31:00", "2023-11-03 09:32:00",
            "2023-11-03 09:30:00", "2023-11-03 09:31:00", "2023-11-03 09:32:00",
            "2023-11-04 09:30:00", "2023-11-04 09:31:00", "2023-11-04 09:32:00",
        ],
        opens=[4500, 4503, 4506, 4510, 4513, 4516, 4515, 4519, 4522, 4525, 4529, 4532, 4530, 4526, 4528, 4540, 4535, 4537],
        highs=[4505, 4508, 4512, 4515, 4518, 4522, 4520, 4524, 4528, 4530, 4534, 4538, 4535, 4531, 4533, 4545, 4540, 4542],
        lows=[4498, 4501, 4504, 4508, 4511, 4514, 4513, 4517, 4520, 4523, 4527, 4530, 4528, 4524, 4526, 4538, 4533, 4535],
        closes=[4503, 4506, 4510, 4513, 4516, 4520, 4519, 4522, 4525, 4529, 4532, 4535, 4526, 4528, 4530, 4535, 4537, 4540],
        volumes=[50, 60, 70, 55, 65, 75, 40, 50, 60, 45, 55, 65, 35, 45, 55, 50, 60, 70],
        ois=[50, 52, 55, 56, 58, 60, 40, 42, 44, 41, 43, 45, 30, 32, 34, 31, 33, 35],
    )


if __name__ == '__main__':
    # Quick smoke test with daily data
    data = make_three_contract_daily()
    bars = build_bars(**data)

    print("=== Built Bars (Daily) ===")
    print(f"Dates:     {bars.dates}")
    print(f"Contracts: {bars.contracts}")
    print(f"Closes:    {bars.closes}")
    print(f"BackClose: {bars.back_closes}")
    print(f"RollRange: {bars.roll_ranges}")
    print()

    results = adjust_all(bars)
    for method, vals in results.items():
        print(f"--- {method} ---")
        print(f"  Close: {[round(v, 6) for v in vals['closes']]}")
        print(f"  Open:  {[round(v, 6) for v in vals['opens']]}")
    print()

    # Quick smoke test with 5Min data
    data5 = make_three_contract_5min()
    bars5 = build_bars_intraday(**data5)

    print("=== Built Bars (5Min) ===")
    print(f"Dates:     {bars5.dates}")
    print(f"Contracts: {bars5.contracts}")
    print(f"Closes:    {bars5.closes}")
    print(f"BackClose: {bars5.back_closes}")
    print(f"RollRange: {bars5.roll_ranges}")
    print()

    results5 = adjust_all(bars5)
    for method, vals in results5.items():
        print(f"--- {method} ---")
        print(f"  Close: {[round(v, 6) for v in vals['closes']]}")
        print(f"  Open:  {[round(v, 6) for v in vals['opens']]}")
