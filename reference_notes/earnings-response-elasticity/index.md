# Earnings Response Elasticity

**Quantpedia ID**: #0421
**URL**: https://quantpedia.com/strategies/earnings-response-elasticity
**Status**: INELIGIBLE
**Linear Issue**: [ENG-264](https://linear.app/epoch-inc/issue/ENG-264/feature-request-event-study-methodology-eaar-calculation-for-0421)

## Overview
This strategy exploits the post-earnings-announcement drift by using a novel measure - the Earnings Response Elasticity (ERE). ERE directly captures the degree of initial market reaction to earnings surprises. Firms with lower ERE (more muted initial reaction) experience larger subsequent price drifts, creating a profitable trading opportunity.

## Trading Rules
**Universe**: NYSE stocks

**Signal**: Earnings Response Elasticity (ERE)
1. Calculate ERE = |EAAR| / |Earnings Surprise|
   - EAAR = Earnings Announcement Abnormal Return (3-day window centered on announcement)
   - Earnings Surprise = Actual EPS - Estimated EPS
2. Sort stocks into quintiles by ERE
3. Long: Bottom ERE quintile when both earnings surprises AND EAARs are positive
4. Short: Bottom ERE quintile when both earnings surprises AND EAARs are negative
5. Hold to next quarter

**Selection**:
- Long bottom ERE quintile (positive surprise + positive EAAR)
- Short bottom ERE quintile (negative surprise + negative EAAR)

**Weighting**: Not specified (likely equal-weighted)
**Rebalancing**: Daily (as earnings announcements occur)

## Fundamental Reason
Returns can be attributed to initial underreaction to earnings information. Firms in the lowest ERE quintile are typically:
1. Smaller companies with less media/investor attention
2. Higher book-to-market ratios (less "glamorous")
3. Followed by fewer analysts

This limited attention causes investors to ignore useful information, leading to stock price underreaction. The information is incorporated into prices with a delay, creating the drift.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1985-2008 |
| Return | 8.5% p.a. |
| Volatility | 17.15% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.26 |

Note: Data from Table 5, spread between ERE1 panels. Quarterly alpha of 5.11%.

**WARNING**: Quantpedia rates confidence as "Moderate" - OOS backtest shows slightly negative performance. Alpha appears to be deteriorating.

## Source Paper
Yan, Zhipeng and Zhao, Yan and Wei, Xu and Cheng, Lee-Young: Earnings Response Elasticity and Post-Earnings-Announcement Drift
- SSRN: https://ssrn.com/abstract=3309788

## QuantConnect Reference Code
Available on Quantpedia (requires Pro subscription)
Clone URL: https://www.quantconnect.com/terminal/clone/23810878/

## Eligibility Check
### Available
- **Transforms**:
  - `earnings` - Earnings announcements with EPS surprise data
  - `eps_surprise` / `eps_surprise_percent` - Earnings surprise calculation
  - `cs_rank` - Cross-sectional ranking for quintile sorting
  - `roc` - Return calculation
- **Assets**: US Stocks available (NYSE)

### Missing
- **Event-Study Methodology** - NOT AVAILABLE
  - Computing 3-day abnormal returns around earnings announcement dates
  - Requires aligning returns to specific event dates (EAAR calculation)
  - Framework for event-window return computation
- **Abnormal Return Calculation** - NOT AVAILABLE
  - Market-adjusted or model-based expected returns
  - Stock return minus expected return for abnormal return
- **ERE Computation** - REQUIRES ABOVE
  - ERE = |EAAR| / |Earnings Surprise|
  - Cannot compute without EAAR

## Implementation Notes
- Strategy is marked INELIGIBLE due to missing event-study methodology
- Confidence rating: Moderate (OOS shows slightly negative performance)
- Complexity: Complex
- We have earnings surprise data but lack event-study framework
- Would require implementing:
  1. Event-window return calculation (returns around earnings dates)
  2. Abnormal return computation (market-adjusted returns)
  3. ERE signal construction
- Low Sharpe (0.26) and deteriorating alpha reduce priority

