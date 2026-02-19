# Low Volatility Factor Effect in Stocks

**Quantpedia ID**: #0007
**URL**: https://quantpedia.com/strategies/low-volatility-factor-effect-in-stocks
**Status**: IN_REVIEW

## Definitions
- Strategy: `project/definitions/test_runner/low_volatility_factor_strategy.json`
**Linear Issue**: [ENG-564](https://linear.app/epoch-inc/issue/ENG-564/implement-low-volatility-factor-effect-0007)

## Overview

Low-risk stocks exhibit significantly higher risk-adjusted returns than the market portfolio, while high-risk stocks significantly underperform on a risk-adjusted basis. This strategy exploits the low volatility anomaly by going long stocks with the lowest historical volatility.

## Trading Rules

**Universe**: S&P 500 constituents (use `SP500` as asset ID - system expands automatically)

**Signal**: 3-year volatility of returns
- Original paper uses weekly returns over 3 years (156 weeks)
- For daily data: 756 trading days (~3 years)

**Selection**:
- Rank stocks by historical volatility
- Long: Bottom decile (lowest 10% volatility) = ~50 stocks

**Weighting**: Equal weight within portfolio

**Rebalancing**: Monthly

## Fundamental Reason

1. **Leverage constraints**: Many investors cannot or will not apply leverage needed to exploit low-risk stocks, so the opportunity cannot be easily arbitraged away
2. **Benchmark-driven investing**: Asset managers tilt towards high beta/volatility stocks to beat benchmarks, leading to overpriced high-risk stocks and underpriced low-risk stocks
3. **Behavioral biases**: Private investors overpay for risky "lottery ticket" stocks seeking high returns quickly
4. **Market mispricing**: Low-volatility stock returns attributed to mispricing rather than compensation for systematic risk

## Performance (Source Paper)

| Metric | Value |
|--------|-------|
| Period | 1986-2006 |
| Annual Return | 11.3% |
| Volatility | 10.1% |
| Max Drawdown | -45.92% |
| Sharpe Ratio | 0.72 |

Note: Results for D1 (lowest volatility decile) long-only portfolio.

## Source Paper

**Blitz, Vliet: "The Volatility Effect: Lower Risk Without Lower Return"**
- URL: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=980865

> Abstract: We present empirical evidence that stocks with low volatility earn high risk-adjusted returns. The annual alpha spread of global low versus high volatility decile portfolios amounts to 12% over the 1986-2006 period. We also observe this volatility effect within the US, European and Japanese markets in isolation. Furthermore, we find that the volatility effect cannot be explained by other well-known effects such as value and size.

## Related Papers

1. Baker, Bradley, Wurgler: "Benchmarks as Limits to Arbitrage" - SSRN 1585031
2. Sullivan, Li: "Why Low-Volatility Stocks Outperform" - SSRN 1739227
3. Baker, Haugen: "Low Risk Stocks Outperform within All Observable Markets" - SSRN 2055431
4. Blitz, van Vliet, Baltussen: "The Volatility Effect Revisited" - SSRN 3442749

## Keywords

stock picking, volatility effect, factor investing, smart beta

## Implementation Notes

- Use `SP500` as asset ID - system expands to current constituents
- 3-year volatility = 756 trading days for daily data
- Bottom decile selection = ~50 stocks (10% of 500)
- `cs_select(direction=CSSelectDirection.bottom, mode=CSSelectMode.percent, k=10)` for bottom 10%

## Epoch Implementation

**Period**: 2007-01-01 to 2025-12-31

**Asset ID**: SP500 (expands to ~500 constituents)

### Backtest Results (2007-2025)

| Metric | Value |
|--------|-------|
| Annual Return | 19.74% |
| Cumulative Returns | 2946.11% |
| Annual Volatility | 23.76% |
| Max Drawdown | -45.65% |
| Sharpe Ratio | 0.87 |
| Round Trips | 727 |

**Comparison with Source Paper (1986-2006):**
- Our results show higher returns (19.74% vs 11.3%) with higher Sharpe (0.87 vs 0.72)
- Volatility is higher (23.76% vs 10.1%) likely due to different time period (includes 2008 crisis, COVID)
- Max drawdown nearly identical (-45.65% vs -45.92%)
- Results confirm the low volatility anomaly persists in out-of-sample period
