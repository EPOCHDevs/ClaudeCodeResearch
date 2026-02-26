# QuantPedia #0022: Term Structure Effect in Commodities
# Full source code from Quantpedia's QuantConnect implementation
# Saved from: https://quantpedia.com/strategies/term-structure-effect-in-commodities/
#
# See: quantpedia_022_main.py and quantpedia_022_data_tools.py for full code.
#
# =============================================================================
# KEY IMPLEMENTATION DETAILS (from actual Quantpedia code)
# =============================================================================
#
# 1. UNIVERSE: 20 commodity futures
#    symbols = {
#        'CME_S1': Soybeans,    'CME_W1': Wheat,      'CME_SM1': SoybeanMeal,
#        'CME_C1': Corn,        'CME_O1': Oats,       'CME_LC1': LiveCattle,
#        'CME_FC1': FeederCattle, 'CME_LN1': LeanHogs, 'CME_GC1': Gold,
#        'CME_SI1': Silver,     'CME_PL1': Platinum,   'CME_HG1': Copper,
#        'CME_LB1': Lumber,     'CME_NG1': NaturalGas, 'CME_PA1': Palladium,
#        'CME_RB1': Gasoline,   'ICE_WT1': CrudeOilWTI, 'ICE_CC1': Cocoa,
#        'ICE_O1': HeatingOil,  'ICE_SB1': Sugar11CME
#    }
#    NOTE: ClassIIIMilk (CME_DA1) is commented out
#    NOTE: Missing vs original 22: Cotton (CT), Orange Juice (OJ), Soybean Oil (ZL)
#    NOTE: Added vs original 22: Copper (HG), Lumber (LB)
#
# 2. ROLL RETURN FORMULA:
#    roll_return = raw_price_near / raw_price_distant - 1
#
#    THIS IS IDENTICAL TO OUR CARRY FORMULA!
#    carry = frontClose / backClose - 1
#
#    The QuantConnect research page showed a log-based annualized formula,
#    but the ACTUAL Quantpedia implementation uses the simple ratio.
#
# 3. CONTRACT SELECTION:
#    near_contract = contracts[0]   (front month, sorted by expiry ascending)
#    dist_contract = contracts[1]   (SECOND contract, NOT furthest!)
#
#    THIS IS IDENTICAL TO OUR IMPLEMENTATION!
#    We use front (index 0) and back (index currentFrontContractIndex + 1)
#
# 4. QUINTILE SELECTION:
#    quantile = len(sorted_by_roll) / 5    # top/bottom 20%
#    long = sorted_by_roll[:quantile]       # highest roll return (backwardation)
#    short = sorted_by_roll[-quantile:]     # lowest roll return (contango)
#
#    NOTE: They sort ALL commodities together and take top/bottom quintile.
#    This is DIFFERENT from the QuantConnect research page which splits
#    positive/negative first. The Quantpedia code does a simple top/bottom sort.
#
# 5. SIZING:
#    SetHoldings(symbol, +1/len(portfolio))  for longs
#    SetHoldings(symbol, -1/len(portfolio))  for shorts
#
#    100% long / 100% short exposure total (NOT 50%/50% like QC research page)
#
# 6. REBALANCING: Monthly (first trading day of new month)
#    if self.Time.month != self.recent_month
#
# =============================================================================
# COMPARISON WITH OUR IMPLEMENTATION
# =============================================================================
#
# CARRY FORMULA:  IDENTICAL  (front/back - 1)
# CONTRACT PAIR:  IDENTICAL  (front month vs second contract)
# SELECTION:      SIMILAR    (top/bottom 20% of all, simple sort)
# SIZING:         DIFFERENT  (they do 100%/100%, we need to match)
# REBALANCE:      IDENTICAL  (monthly, first trading day)
# UNIVERSE:       SIMILAR    (20 vs our 22, minor differences)
#
# Our implementation should match closely. The main issue is likely SIZING -
# SetHoldings(1/N) means each position is 1/N of portfolio value, so with
# ~4 longs and ~4 shorts, that's 25% per position = 100% long + 100% short.
# This is very leveraged for futures.
