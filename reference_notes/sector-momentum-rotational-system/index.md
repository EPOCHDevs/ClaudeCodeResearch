# Sector Momentum - Rotational System

**Quantpedia ID**: #0003
**URL**: https://quantpedia.com/strategies/sector-momentum-rotational-system
**Status**: ELIGIBLE
**Linear Issue**: [ENG-13](https://linear.app/epoch-inc/issue/ENG-13/implement-sector-momentum-rotational-system-0003)

## Overview
This approach combines momentum and sector rotation principles to select outperforming equity sectors. Investors identify sectors with the strongest recent performance and overweight them in their portfolio, rotating monthly to maintain exposure to current winners while avoiding laggards.

## Trading Rules
**Universe**: 10 U.S. sector ETFs (XLK, XLP, XLF, XLB, XLV, XLE, XLI, XLY, XLRE, XLC, XLU)
**Signal**: Rank sectors by 12-month price momentum (ROC)
**Selection**: Top 3 sectors with highest momentum
**Weighting**: Equal weight (33.3% each)
**Rebalancing**: Monthly

## Fundamental Reason
The strategy exploits behavioral finance mechanisms. Moskowitz and Grinblatt documented that "momentum investment strategies, which buy past winning stocks and sell past losing stocks, are significantly less profitable once we control for industry momentum." Industry-level momentum appears to drive much of the individual stock momentum effect.

Additionally, sectors exhibit differential sensitivity to business cycles. Chen, Jiang, and Zhu demonstrated that "sector indexes exhibit both price momentum and earnings momentum," with profitability persisting even after transaction cost adjustments.

## Performance (Source Paper)
| Metric | Value |
|--------|-------|
| Period | 1928-2009 |
| Return | 13.94% p.a. |
| Volatility | 18.38% |
| Max Drawdown | -46.29% |
| Sharpe Ratio | 0.54 |

## Out-of-Sample Performance (Quantpedia)
| Metric | Value |
|--------|-------|
| Period | 2004-2025 |
| Return | 9.4% p.a. |
| Volatility | 18.51% |
| Max Drawdown | -46.32% |
| Sharpe Ratio | 0.51 |

## Source Paper
**Relative Strength Strategies for Investing**
- Author: Mebane Faber
- SSRN: http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1585517
- Key Finding: The relative strength model applied to U.S. equity sectors from the 1920s onward produces increased absolute returns with equity-equivalent risk.

## QuantConnect Reference Code
Strategy has QuantConnect code available on Quantpedia (subscription: Free).

## Eligibility Check
### Available
**Transforms:**
- `roc(close, period=12)` - Rate of Change for 12-month momentum calculation
- `cs_momentum` - Cross-Sectional Momentum for relative performance ranking
- `cs_select(direction=top, mode=count, k=3)` - Select top 3 sectors by momentum

**Assets (11 Sector ETFs):**
- XLK-Stocks (Technology)
- XLP-Stocks (Consumer Staples)
- XLF-Stocks (Financials)
- XLB-Stocks (Materials)
- XLV-Stocks (Healthcare)
- XLE-Stocks (Energy)
- XLI-Stocks (Industrials)
- XLY-Stocks (Consumer Discretionary)
- XLRE-Stocks (Real Estate)
- XLC-Stocks (Communication Services)
- XLU-Stocks (Utilities)

### Missing
None - all required components available.

## Implementation Notes
1. **Timeframe**: Use monthly bars for 12-period ROC calculation
2. **Signal Logic**:
   - Calculate `roc(close, 12)` for each sector
   - Apply `cs_select(roc_value, direction=top, mode=count, k=3)` to get boolean mask
   - Allocate equal weight to selected sectors
3. **Position Management**: Equal weight (1/3) across top 3 sectors
4. **Rebalance Trigger**: Monthly at month-end
5. **Full reconstitution**: Liquidate and rebuild portfolio each month

## Related Research
- Moskowitz and Grinblatt - Industry momentum driving stock momentum
- Chen, Jiang, and Zhu - Sector price and earnings momentum
- Andreu et al. - Momentum effects exploitable through ETFs despite costs
