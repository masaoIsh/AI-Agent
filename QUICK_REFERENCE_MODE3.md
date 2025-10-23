# Mode 3 Quick Reference Card

## Launch

```bash
python interactive_cli.py
# Select: 3
```

## Inputs Required

| Input | Example | Notes |
|-------|---------|-------|
| **Tickers** | `AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM` | 10 stocks, same sector |
| **Start Date** | `2020-01-01` | YYYY-MM-DD, default 2020-01-01 |
| **End Date** | `2024-12-31` | YYYY-MM-DD, default today |

## What You Get

### 1. Sector Fundamentals
- PBR, ROE, ROA for each stock
- Percentile rankings (0-100)
- Z-scores (standard deviations)
- Composite score rankings

### 2. ARIMA Regime Analysis
- Current volatility regime (low/med/high)
- 5-step forecast with confidence intervals
- Model quality metrics (AIC/BIC)

### 3. Agent Debate
- Wassim: Fundamental comparison
- Yugo: Regime-switching forecasts
- 6 turns total (3 each)
- Consensus: BUY/SELL/HOLD

### 4. Portfolio Backtest
- Top N stocks (you choose, default 5)
- Equal-weight or inverse-vol
- Monthly rebalancing (configurable)
- CAGR, Sharpe, MaxDD metrics

## Quick Sector Lists

**Tech:** `AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM`

**Finance:** `JPM,BAC,WFC,C,GS,MS,BLK,SCHW,AXP,USB`

**Health:** `JNJ,UNH,PFE,ABBV,TMO,MRK,ABT,DHR,LLY,AMGN`

**Energy:** `XOM,CVX,COP,SLB,EOG,MPC,PSX,VLO,OXY,HAL`

**Consumer:** `AMZN,TSLA,HD,NKE,MCD,SBUX,TGT,LOW,BKNG,CMG`

## Interpreting Output

### Composite Score
```
Higher = Better fundamentals + Cheaper valuation
```
- Score > 2.0: Exceptional opportunity
- Score 1.0-2.0: Good value
- Score 0.0-1.0: Fair
- Score < 0.0: Overvalued or weak fundamentals

### Percentile Rankings
```
>75%: Top quartile, excellent
50-75%: Above average
25-50%: Below average
<25%: Bottom quartile, weak
```

### Z-Scores
```
>+2: Extreme high
+1 to +2: High (premium)
-1 to +1: Normal
-1 to -2: Low (discount)
<-2: Extreme low
```

### ARIMA Regimes
```
Low Vol: Stable, tight CIs, reliable forecasts
Medium Vol: Moderate, balanced risk/reward
High Vol: Unstable, wide CIs, high uncertainty
```

## Workflow Summary

```
Input 10 stocks
    ↓
Fetch fundamentals
    ↓
Sector comparison (Wassim's domain)
    ↓
Fetch prices
    ↓
ARIMA regimes (Yugo's domain)
    ↓
Agent debate (6 turns)
    ↓
Consensus mechanism
    ↓
Portfolio construction (top 5)
    ↓
Backtest
    ↓
Results: CAGR, Sharpe, MaxDD, equity curve
```

## Example Session (2 min)

```bash
$ python interactive_cli.py
Select mode: 3

Enter 10 tickers: AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM
Start: 2020-01-01
End: [Enter for today]

# System fetches fundamentals...
# Computes sector comparison...
# Runs ARIMA regime-switching...
# Agents debate...
# Consensus: BUY

Construct portfolio? y
Top stocks: 5
Strategy: invvol
Rebalance: M

# Backtest runs...
CAGR: 0.28, Sharpe: 1.34, MaxDD: -0.18
Saved: sector_portfolio_Technology_20251022_143022.png
```

## Tips

1. **Sector purity**: Ensure all 10 stocks truly in same sector
2. **Time period**: 2+ years for good regime detection
3. **Portfolio size**: 5-7 stocks optimal for diversification
4. **Rebalancing**: Monthly = good balance
5. **Trust the process**: Agents will debate and reach consensus

## Output Files

- `sector_portfolio_{Sector}_{timestamp}.png` - Equity curve
- Console logs show full agent debate

## Documentation

- Full guide: `SECTOR_ANALYSIS_GUIDE.md`
- Implementation: `SECTOR_MODE_SUMMARY.md`
- Main README: `README.md`

