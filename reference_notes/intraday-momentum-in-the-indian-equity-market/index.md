# Intraday Momentum in the Indian Equity Market

**Quantpedia ID**: #0431
**URL**: https://quantpedia.com/strategies/intraday-momentum-in-the-indian-equity-market
**Status**: INELIGIBLE
**Linear Issue**: [ENG-274](https://linear.app/epoch-inc/issue/ENG-274/feature-request-indian-single-stock-futures-and-intraday-data-for-0431)

## Overview
This strategy exploits intraday momentum in Indian single-stock futures. Using a 3-day lookback with 60-minute rebalancing, it goes long futures with positive momentum and shorts those with negative momentum. The strategy uses risk-budgeting for portfolio construction.

## Trading Rules
**Universe**: Futures on stocks in the Nifty 50 Index (50 stocks)

**Signal**: Intraday momentum
1. Lookback period: 3 days
2. Rebalancing period: 60 minutes
3. Long futures with positive momentum
4. Short futures with negative momentum

**Portfolio Construction**:
- Risk budgets proportional to absolute normalized indicator values
- Total allocation risk target: 15% annualized
- Target risk: 10%
- Weights scaled so risk is 15%, sum of exposure ~100%

**Weighting**: Risk-budgeted
**Rebalancing**: Intraday (every 60 minutes)

## Fundamental Reason
- Momentum anomalies driven by behavioral biases (herding, confirmation bias, under-reaction)
- Efficacy of momentum strategies increases as lookback and rebalancing frequencies decrease
- Very short-term momentum with frequent rebalancing can be profitable
- Trading costs are the limiting factor for rebalancing frequency
- Uses liquid futures to manage transaction costs

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 2010-2019 |
| Return | 12.36% p.a. |
| Volatility | 12.81% |
| Max Drawdown | Not stated |
| Sharpe Ratio | 0.96 |

Note: Data from Figure 7, 3 days/60 mins configuration.

**Note**: No OOS data available. Unknown if strategy works in US market.

## Source Paper
Srivastava, Sonam and Chakravorty, Gaurav and Singhal, Mansi: Momentum in the Indian Equity Markets: Positive Convexity and Positive Alpha
- SSRN: https://ssrn.com/abstract=3345280

## QuantConnect Reference Code
Not available (no QC code for this strategy)

## Eligibility Check
### Available
- **Transforms**:
  - `roc` - Momentum calculation
  - Standard momentum transforms
- **Assets**:
  - INDA-Stocks (India ETF) - broad India exposure only

### Missing
- **Indian Single-Stock Futures** - NOT AVAILABLE
  - Requires futures on 50 individual stocks in Nifty 50 Index
  - We only have INDA/INDY ETFs for India exposure
  - No individual Indian stock data or futures
- **Intraday Data** - PARTIAL
  - Strategy requires 60-minute bar data
  - Intraday rebalancing infrastructure needed
  - Current focus is primarily on daily data
- **Risk-Budgeting Framework** - COMPLEX
  - Specialized portfolio construction approach
  - Would need custom implementation

## Implementation Notes
- Strategy is marked INELIGIBLE due to:
  1. Missing Indian single-stock futures data
  2. Intraday data requirements (60-minute bars)
  3. Complex risk-budgeting portfolio construction
- Confidence rating: Strong
- Complexity: Complex
- Good Sharpe ratio (0.96) but requires significant infrastructure
- Unknown if transferable to US market
- No OOS validation data available

