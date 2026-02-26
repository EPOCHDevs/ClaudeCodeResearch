#!/usr/bin/env python3
"""
AMZN Downside Scenario Analysis
Assumptions: +100bp real rate rise, flat forward earnings
Date: 2026-02-26
"""

import numpy as np

# =============================================================================
# CURRENT MARKET INPUTS
# =============================================================================
CURRENT_PRICE = 210.66
SHARES_OUT_B = 10.56  # ~10.56B diluted shares
CURRENT_EPS = 7.86    # 2026E consensus EPS
CONSENSUS_EPS_GROWTH = 0.20  # Street expects ~20% EPS growth

# Rate environment
REAL_RATE_CURRENT = 1.78    # 10Y TIPS yield, 2/24/2026
NOMINAL_10Y = 4.06          # 10Y UST nominal
EQUITY_RISK_PREMIUM = 5.5   # Standard ERP estimate
BETA = 1.15                 # AMZN beta vs SPX

# Derived
CURRENT_WACC = 0.10         # ~10% from multiple sources
CURRENT_FWD_PE = CURRENT_PRICE / CURRENT_EPS

# FCF inputs (TTM approx)
FCF_PER_SHARE_BASE = 6.50   # ~$68B FCF / 10.56B shares
CAPEX_INTENSITY = 0.55      # capex/revenue ratio (heavy AI/infra spend)

# =============================================================================
# SCENARIO DEFINITIONS
# =============================================================================
RATE_SHOCK_BP = 100  # +100bp real rate rise

scenarios = {
    "Base Case (Consensus)": {
        "eps_growth": 0.20,
        "wacc": CURRENT_WACC,
        "terminal_growth": 0.04,
        "description": "Street consensus: 20% EPS growth, current rates"
    },
    "Downside: Flat EPS + 100bp": {
        "eps_growth": 0.00,
        "wacc": CURRENT_WACC + 0.01,  # +100bp pass-through
        "terminal_growth": 0.03,       # Lower terminal growth with flat earnings
        "description": "Flat forward EPS, +100bp real rates, reduced terminal growth"
    },
    "Severe Downside: Flat EPS + 100bp + Multiple Compression": {
        "eps_growth": 0.00,
        "wacc": CURRENT_WACC + 0.01,
        "terminal_growth": 0.025,
        "description": "Flat EPS, +100bp rates, market derates to utility-like terminal"
    }
}

# =============================================================================
# 1. SCENARIO SUMMARY TABLE
# =============================================================================
print("=" * 80)
print("AMZN DOWNSIDE SCENARIO ANALYSIS")
print(f"Current Price: ${CURRENT_PRICE:.2f}  |  Date: 2026-02-26")
print(f"Current Fwd P/E: {CURRENT_FWD_PE:.1f}x  |  2026E EPS: ${CURRENT_EPS:.2f}")
print(f"10Y Real Rate: {REAL_RATE_CURRENT:.2f}%  |  Shocked: {REAL_RATE_CURRENT + 1.0:.2f}%")
print("=" * 80)

print("\n1. SCENARIO ASSUMPTIONS")
print("-" * 80)
print(f"{'Metric':<35} {'Base Case':<20} {'Downside':<20} {'Severe':<20}")
print("-" * 80)

rows = [
    ("EPS Growth (annual)", "20%", "0% (flat)", "0% (flat)"),
    ("WACC / Discount Rate", "10.0%", "11.0%", "11.0%"),
    ("Terminal Growth Rate", "4.0%", "3.0%", "2.5%"),
    ("Real Rate (10Y TIPS)", "1.78%", "2.78%", "2.78%"),
    ("Earnings Trajectory", "Accelerating", "Flat at $7.86", "Flat at $7.86"),
]
for label, base, down, severe in rows:
    print(f"{label:<35} {base:<20} {down:<20} {severe:<20}")

# =============================================================================
# 2. DCF VALUATION (5-Year + Terminal)
# =============================================================================
print("\n\n2. DCF VALUATION — 5-YEAR EXPLICIT + TERMINAL VALUE")
print("=" * 80)

def run_dcf(fcf_base, growth_rate, wacc, terminal_growth, years=5):
    """Simple 2-stage DCF: explicit period + terminal value."""
    fcfs = []
    for yr in range(1, years + 1):
        fcf = fcf_base * (1 + growth_rate) ** yr
        fcfs.append(fcf)

    # Terminal value (Gordon Growth)
    terminal_fcf = fcfs[-1] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (wacc - terminal_growth)

    # Discount everything back
    pv_fcfs = []
    for yr, fcf in enumerate(fcfs, 1):
        pv = fcf / (1 + wacc) ** yr
        pv_fcfs.append(pv)

    pv_terminal = terminal_value / (1 + wacc) ** years

    total_pv = sum(pv_fcfs) + pv_terminal

    return {
        "fcfs": fcfs,
        "pv_fcfs": pv_fcfs,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "total_pv": total_pv,
        "pv_fcf_sum": sum(pv_fcfs),
        "terminal_pct": pv_terminal / total_pv * 100
    }

for scenario_name, params in scenarios.items():
    print(f"\n--- {scenario_name} ---")
    print(f"  {params['description']}")

    result = run_dcf(
        fcf_base=FCF_PER_SHARE_BASE,
        growth_rate=params["eps_growth"],
        wacc=params["wacc"],
        terminal_growth=params["terminal_growth"]
    )

    implied_price = result["total_pv"]
    upside = (implied_price / CURRENT_PRICE - 1) * 100

    print(f"\n  {'Year':<8}", end="")
    for yr in range(1, 6):
        print(f"{'Y' + str(yr):>10}", end="")
    print(f"{'Terminal':>12}")

    print(f"  {'FCF/sh':<8}", end="")
    for fcf in result["fcfs"]:
        print(f"${fcf:>8.2f}", end="")
    print()

    print(f"  {'PV FCF':<8}", end="")
    for pv in result["pv_fcfs"]:
        print(f"${pv:>8.2f}", end="")
    print(f"${result['pv_terminal']:>10.2f}")

    print(f"\n  PV of Cash Flows:   ${result['pv_fcf_sum']:>8.2f}")
    print(f"  PV of Terminal:     ${result['pv_terminal']:>8.2f}  ({result['terminal_pct']:.0f}% of total)")
    print(f"  ----------------------------------------")
    print(f"  Implied Fair Value: ${implied_price:>8.2f}")
    print(f"  Current Price:      ${CURRENT_PRICE:>8.2f}")
    print(f"  Upside/Downside:    {upside:>+7.1f}%")

# =============================================================================
# 3. MULTIPLE-BASED VALUATION
# =============================================================================
print("\n\n3. MULTIPLE-BASED VALUATION")
print("=" * 80)

print("\nHistorical context — AMZN P/E in different rate regimes:")
print("-" * 60)
historical = [
    ("2021 (ZIRP, peak growth)", "60-80x", "Real rates: -1.0%"),
    ("2022 Q4 (rate shock trough)", "~50x (on depressed E)", "Real rates: +1.5%"),
    ("2023 (recovery)", "40-50x", "Real rates: +2.0%"),
    ("2024 (normalization)", "35-40x", "Real rates: +1.8%"),
    ("2025-26 (current)", "~27x", "Real rates: +1.8%"),
]
for period, pe, rates in historical:
    print(f"  {period:<35} P/E: {pe:<22} {rates}")

print("\nJustified P/E under downside scenario:")
print("-" * 60)

# Gordon Growth implied P/E = payout / (ke - g)
# For AMZN, use earnings yield framework
# P/E = 1 / (ke - g) when payout = 100% of earnings to equity
# More practically, justified P/E for zero-growth = 1/ke

ke_base = CURRENT_WACC  # cost of equity proxy
ke_shocked = CURRENT_WACC + 0.01

justified_pe_base_growth = 1 / (ke_base - 0.15)  # with 15% sustainable growth (conservative of 20%)
justified_pe_flat_base_rate = 1 / ke_base           # flat earnings, current rate
justified_pe_flat_shocked = 1 / ke_shocked          # flat earnings, shocked rate

# More realistic: use a 2-stage approach
# Stage 1: 5 years of growth, Stage 2: terminal at GDP
def justified_pe_2stage(g1, years, g2, ke):
    """2-stage justified P/E ratio."""
    pv = 0
    for yr in range(1, years + 1):
        pv += (1 + g1) ** yr / (1 + ke) ** yr
    terminal_pe = (1 + g1) ** years * (1 + g2) / (ke - g2)
    pv += terminal_pe / (1 + ke) ** years
    return pv

pe_scenarios = [
    ("Consensus (20% growth 5yr, 4% terminal, 10% WACC)",
     justified_pe_2stage(0.20, 5, 0.04, 0.10)),
    ("Flat EPS, current rates (0% growth, 3% terminal, 10% WACC)",
     justified_pe_2stage(0.00, 5, 0.03, 0.10)),
    ("Flat EPS, +100bp rates (0% growth, 3% terminal, 11% WACC)",
     justified_pe_2stage(0.00, 5, 0.03, 0.11)),
    ("Flat EPS, +100bp, low terminal (0%, 2.5% terminal, 11% WACC)",
     justified_pe_2stage(0.00, 5, 0.025, 0.11)),
]

print(f"\n  {'Scenario':<60} {'Justified P/E':>12} {'Implied Price':>14}")
print("  " + "-" * 88)
for desc, pe in pe_scenarios:
    price = pe * CURRENT_EPS
    delta = (price / CURRENT_PRICE - 1) * 100
    print(f"  {desc:<60} {pe:>10.1f}x    ${price:>8.2f} ({delta:>+.0f}%)")

# =============================================================================
# 4. SENSITIVITY MATRIX
# =============================================================================
print("\n\n4. SENSITIVITY MATRIX — IMPLIED SHARE PRICE")
print("=" * 80)

wacc_range = [0.085, 0.090, 0.095, 0.100, 0.105, 0.110, 0.115, 0.120]
growth_range = [0.00, 0.05, 0.10, 0.15, 0.20]

print(f"\n  FCF/share base: ${FCF_PER_SHARE_BASE:.2f} | 5-year explicit + terminal value")
print(f"  Terminal growth: 3.0% for all cells")
print(f"  Current price: ${CURRENT_PRICE:.2f}\n")

# Header
print(f"  {'WACC ↓ / Growth →':>20}", end="")
for g in growth_range:
    print(f"  {g*100:>6.0f}%  ", end="")
print()
print("  " + "-" * 72)

for w in wacc_range:
    marker = " ◄ current" if abs(w - 0.10) < 0.001 else ""
    marker_down = " ◄ +100bp" if abs(w - 0.11) < 0.001 else ""
    label = f"{w*100:.1f}%{marker}{marker_down}"
    print(f"  {label:>20}", end="")
    for g in growth_range:
        r = run_dcf(FCF_PER_SHARE_BASE, g, w, 0.03)
        price = r["total_pv"]
        # Color coding via markers
        if price < CURRENT_PRICE * 0.7:
            flag = "!!"  # severe downside
        elif price < CURRENT_PRICE * 0.9:
            flag = " !"  # meaningful downside
        elif price > CURRENT_PRICE * 1.1:
            flag = " +"
        else:
            flag = "  "
        print(f"  ${price:>6.0f}{flag}", end="")
    print()

print(f"\n  Legend: !! = >30% downside  |  ! = >10% downside  |  + = >10% upside")
print(f"  Downside scenario cell: WACC=11%, Growth=0% (flat EPS + 100bp shock)")

# =============================================================================
# 5. HISTORICAL ANALOG: 2022 RATE SHOCK
# =============================================================================
print("\n\n5. HISTORICAL ANALOG — 2022 RATE SHOCK")
print("=" * 80)

print("""
  The closest analog is the 2022 rate cycle:

  Period          Real Rate    AMZN Price    Fwd P/E    Drawdown
  ----------------------------------------------------------------
  Nov 2021        -1.04%       $188*         ~60x       (peak)
  Jun 2022        +0.53%       $106*         ~45x       -44%
  Oct 2022        +1.64%       $ 86*         ~50x**     -54%
  Dec 2023        +1.72%       $153          ~42x       -19%
  Today           +1.78%       $211          ~27x       ---

  * Split-adjusted prices (20:1 split Jun 2022)
  ** Depressed earnings inflated P/E

  Key takeaway: In 2022, a ~260bp real rate rise drove a 54% peak-to-trough
  drawdown. We're modeling a much smaller shock (+100bp), but starting from
  a higher rate base where marginal bp moves may matter more.

  Critical difference: In 2022, earnings were also falling (margin compression
  from over-hiring + logistics build-out). Today AMZN has higher margins and
  proven AWS/ads profitability. A flat-earnings scenario is conservative but
  not catastrophic — it assumes growth stalls, not that margins collapse.
""")

# =============================================================================
# 6. KEY RISK METRICS & CONCLUSIONS
# =============================================================================
print("\n6. KEY RISK METRICS")
print("=" * 80)

# Downside scenario implied price
downside_dcf = run_dcf(FCF_PER_SHARE_BASE, 0.00, 0.11, 0.03)
severe_dcf = run_dcf(FCF_PER_SHARE_BASE, 0.00, 0.11, 0.025)

downside_price = downside_dcf["total_pv"]
severe_price = severe_dcf["total_pv"]
downside_pe = downside_price / CURRENT_EPS
severe_pe = severe_price / CURRENT_EPS

# Breakeven growth rate at shocked WACC
# Find growth rate where DCF = current price
from scipy.optimize import brentq

def price_minus_current(g):
    r = run_dcf(FCF_PER_SHARE_BASE, g, 0.11, 0.03)
    return r["total_pv"] - CURRENT_PRICE

try:
    breakeven_growth = brentq(price_minus_current, -0.10, 0.50)
except:
    breakeven_growth = None

print(f"""
  Metric                                    Value
  ----------------------------------------------------------
  Current Price                             ${CURRENT_PRICE:.2f}
  Current Forward P/E                       {CURRENT_FWD_PE:.1f}x

  DOWNSIDE SCENARIO (flat EPS + 100bp):
    Implied Fair Value (DCF)                ${downside_price:.2f}
    Implied Forward P/E                     {downside_pe:.1f}x
    Drawdown from Current                   {(downside_price/CURRENT_PRICE - 1)*100:+.1f}%

  SEVERE DOWNSIDE (flat EPS + 100bp + low terminal):
    Implied Fair Value (DCF)                ${severe_price:.2f}
    Implied Forward P/E                     {severe_pe:.1f}x
    Drawdown from Current                   {(severe_price/CURRENT_PRICE - 1)*100:+.1f}%
""")

if breakeven_growth is not None:
    print(f"""  BREAKEVEN ANALYSIS:
    At WACC = 11.0% (post-shock), AMZN needs {breakeven_growth*100:.1f}% annual
    FCF growth over the next 5 years just to justify today's price.
    Consensus expects ~20%. The margin of safety is {0.20 - breakeven_growth:.0%} of
    growth expectation.
""")

print(f"""  SCENARIO PRICE MAP:

    Bull (consensus):     ${run_dcf(FCF_PER_SHARE_BASE, 0.20, 0.10, 0.04)['total_pv']:.0f}   (upside from growth + current rates)
    Current price:        ${CURRENT_PRICE:.0f}   (where the market is today)
    Downside:             ${downside_price:.0f}   (flat earnings + 100bp rate shock)
    Severe:               ${severe_price:.0f}   (flat + 100bp + terminal compression)

    ├─────────────────────────────────────────────────────────┤
    ${severe_price:.0f}          ${downside_price:.0f}        ${CURRENT_PRICE:.0f}               ${run_dcf(FCF_PER_SHARE_BASE, 0.20, 0.10, 0.04)['total_pv']:.0f}
    Severe       Downside     Current              Bull
""")

print("=" * 80)
print("END OF REPORT")
print("=" * 80)
