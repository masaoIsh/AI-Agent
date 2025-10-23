# Sector Portfolio Analysis Guide

## Overview

**Mode 3: Sector Portfolio Analysis with Agent Debate** is a comprehensive workflow that combines:
1. Fundamental ratio analysis (PBR, ROE, ROA)
2. Sector-relative valuation comparison
3. ARIMA regime-switching forecasts
4. AI agent debate with consensus mechanism
5. Portfolio construction and backtesting

This fulfills your requirements for analyzing 10 stocks in the same sector with Wassim and Yugo using their specialized methodologies.

## Quick Start

```bash
python interactive_cli.py
# Select option 3
```

## Example Technology Sector Analysis

### Input Example

```
Select mode:
1) Agent analysis (CSV-based with VECM)
2) Portfolio backtesting (Yahoo Finance)
3) Sector portfolio analysis with agent debate (NEW!)
Enter 1, 2, or 3 (default 1): 3

🏢 Sector Portfolio Analysis & Agent Debate
================================================================================
Enter 10 stock tickers in the same sector (comma-separated): 
AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM

Start date [YYYY-MM-DD, default 2020-01-01]: 2020-01-01
End date [YYYY-MM-DD, default today]: 2024-12-31
```

### What Happens Next

#### Step 1: Fundamentals Fetching
```
⬇️  Fetching fundamentals for 10 stocks...
✅ Fundamentals fetched:
symbol sector           pb_ratio    roe      roa
AAPL   Technology       45.23      1.4701   0.2234
MSFT   Technology       12.34      0.4312   0.1823
GOOGL  Technology       6.78       0.2891   0.1456
...
```

#### Step 2: Sector Comparison Analysis
Wassim receives detailed sector comparison including:
- **Percentile Rankings**: Where each stock ranks within the sector
- **Z-Scores**: How many standard deviations from sector average
- **Composite Scores**: Combined valuation + quality metric

```
📊 Running sector comparison analysis...
Sector Comparison Analysis: Technology
================================================================================
Number of stocks in sector: 10

Sector Averages:
  PB_RATIO: Mean=23.4567, Median=18.2345
  ROE: Mean=0.4523, Median=0.3891
  ROA: Mean=0.1734, Median=0.1523

🏆 Sector Rankings (by composite score):
symbol  composite_score  pb_ratio    roe      roa
NVDA    2.3456          55.23       1.2301   0.4512
MSFT    1.8923          12.34       0.4312   0.1823
AAPL    1.4567          45.23       1.4701   0.2234
...
```

**Interpretation for Wassim:**
- High composite score = Better fundamentals relative to valuation
- NVDA example: High ROE/ROA despite high PBR (growth premium justified)
- Negative composite = Expensive relative to fundamentals (potential SELL)

#### Step 3: Price Data & ARIMA Regime-Switching

```
⬇️  Fetching price data from 2020-01-01 to 2024-12-31...
✅ Price data fetched: 1258 days, 10 stocks

🔮 Running ARIMA regime-switching forecast for AAPL...
ARIMA Regime-Switching Analysis
================================================================================
Regime Distribution:
  low_vol: 523 periods (41.6%)
  medium_vol: 412 periods (32.7%)
  high_vol: 323 periods (25.7%)

Current Regime: medium_vol

Fitted ARIMA Models by Regime:
  low_vol: AIC=5234.56, BIC=5256.78
  medium_vol: AIC=4123.45, BIC=4145.67
  high_vol: AIC=6789.01, BIC=6811.23

Forecast Results:
  Regime: medium_vol
  Step 1: 175.4523 (95% CI: [170.2345, 180.6701])
  Step 2: 176.8912 (95% CI: [168.5623, 185.2201])
  Step 3: 178.2301 (95% CI: [165.8912, 190.5690])
  ...
```

**Interpretation for Yugo:**
- **Current regime** determines forecast reliability
- **Low vol regime**: Tight confidence intervals, more reliable forecasts
- **High vol regime**: Wide CIs, less predictable, higher risk
- **AIC/BIC**: Lower = better fit for that regime

#### Step 4: Agent Debate

Wassim and Yugo receive the comprehensive data and debate:

```
🤖 Agents are now analyzing and debating...
============================================================

🧮 Wassim (Fundamental Agent) - Round 1, Turn 1:
Looking at the sector comparison, I see NVDA and MSFT as standout opportunities.

NVDA Analysis:
- ROE of 1.23 is at the 95th percentile - exceptional profitability
- ROA of 0.45 is top-tier efficiency
- PBR of 55 seems high, but Z-score of +1.8 indicates this is a growth premium
- Composite score of 2.35 ranks #1 in the sector

MSFT Analysis:
- ROE at 85th percentile (0.43) with PBR at 45th percentile (12.34)
- This is a value opportunity: high quality at reasonable valuation
- Z-score of -0.3 on PBR means trading below sector average

I recommend BUY on NVDA and MSFT for the portfolio.

CONSENSUS: direction=1 confidence=0.85 reliability=0.90

📈 Yugo (Valuation Agent) - Round 1, Turn 1:
Based on ARIMA regime-switching analysis for AAPL:

Current Regime: medium_vol
- Forecast shows upward trend: +2.3% over 5 days
- Confidence intervals are moderate width (medium volatility)
- AIC suggests medium_vol model fits better than high_vol

Technical Indicators:
- RSI at 58 (neutral, not overbought)
- MACD histogram positive (bullish momentum)

I agree with Wassim's NVDA recommendation but would add AAPL due to:
- Positive forecast trajectory in stable regime
- Technical momentum confirming uptrend

CONSENSUS: direction=1 confidence=0.75 reliability=0.85

[... 4 more turns of debate ...]

🧮 Applying Sophisticated Consensus Protocol...
============================================================
[Step 1] Collecting agent inputs
  Wassim        d=+1, c=0.85, r=0.90
  Yugo          d=+1, c=0.75, r=0.85
[Step 6] Value Computation and Statistical Test
🟢 Significant positive value → BUY.

🎉 ANALYSIS COMPLETE!
Final Recommendation: BUY
```

#### Step 5: Portfolio Construction & Backtesting

```
Construct and backtest a portfolio from top-ranked stocks? [y/N]: y
How many top stocks to include? (default 5): 5

🧮 Constructing portfolio from: NVDA, MSFT, AAPL, GOOGL, META

Strategy [equal|invvol] (default equal): invvol
Rebalance frequency [D/W/M/Q] (default M): M

📊 Portfolio weights:
NVDA     0.1523
MSFT     0.2341
AAPL     0.2012
GOOGL    0.2134
META     0.1990

📊 Portfolio Performance Metrics
================================================================================
CAGR: 0.2845
Vol: 0.2123
Sharpe: 1.3401
MaxDD: -0.1834

🖼️  Saved: sector_portfolio_Technology_20251022_143022.png
```

## Sector Examples

### Technology Sector (10 stocks)
```
AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM
```

### Financial Sector (10 stocks)
```
JPM,BAC,WFC,C,GS,MS,BLK,SCHW,AXP,USB
```

### Healthcare Sector (10 stocks)
```
JNJ,UNH,PFE,ABBV,TMO,MRK,ABT,DHR,LLY,AMGN
```

### Consumer Discretionary (10 stocks)
```
AMZN,TSLA,HD,NKE,MCD,SBUX,TGT,LOW,BKNG,CMG
```

### Energy Sector (10 stocks)
```
XOM,CVX,COP,SLB,EOG,MPC,PSX,VLO,OXY,HAL
```

## Key Metrics Explained

### Wassim's Fundamental Ratios

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **PBR (Price-to-Book)** | Market Cap / Book Value | Lower = cheaper valuation. High PBR may indicate growth premium or overvaluation. |
| **ROE (Return on Equity)** | Net Income / Shareholder Equity | Higher = better returns to shareholders. >20% is excellent. |
| **ROA (Return on Assets)** | Net Income / Total Assets | Higher = more efficient use of assets. >5% is good. |
| **Composite Score** | ROE z-score + ROA z-score - PBR z-score | Higher = better quality + cheaper valuation |

### Percentile Rankings
- **>75th percentile**: Top quartile, excellent
- **50-75th percentile**: Above average
- **25-50th percentile**: Below average
- **<25th percentile**: Bottom quartile, weak

### Z-Scores
- **>+2**: Extremely high (potentially overheated or exceptional)
- **+1 to +2**: High (premium)
- **-1 to +1**: Normal range
- **-1 to -2**: Low (discount)
- **<-2**: Extremely low (deep value or distressed)

### Yugo's ARIMA Regime-Switching

| Regime | Characteristics | Forecast Reliability | Investment Implication |
|--------|----------------|----------------------|------------------------|
| **Low Vol** | Stable, predictable | High (tight CIs) | Good for momentum strategies |
| **Medium Vol** | Moderate fluctuations | Moderate | Balanced risk/reward |
| **High Vol** | Large swings | Low (wide CIs) | Higher risk, higher uncertainty |

**Regime Transitions:**
- Low → Medium: Increasing uncertainty, reduce position size
- Medium → High: Risk-off signal, consider defensive positioning
- High → Medium: Stabilizing, opportunities emerging
- Medium → Low: Confidence building, good entry point

## Analysis Workflow Summary

```
┌──────────────────────────────────────────────────────────────┐
│ 1. Input: 10 sector stocks + date range                     │
└───────────────────┬──────────────────────────────────────────┘
                    │
    ┌───────────────▼───────────────┐
    │ 2. Fetch Fundamentals (Yahoo) │
    │    - PBR, ROE, ROA            │
    │    - Sector, Industry         │
    └───────────────┬───────────────┘
                    │
    ┌───────────────▼───────────────────────┐
    │ 3. Sector Comparison Analysis         │
    │    - Percentile ranks                 │
    │    - Z-scores                         │
    │    - Composite scores                 │
    │    - Rankings                         │
    └───────────────┬───────────────────────┘
                    │
    ┌───────────────▼───────────────┐
    │ 4. Fetch Price Data (Yahoo)   │
    └───────────────┬───────────────┘
                    │
    ┌───────────────▼──────────────────────┐
    │ 5. ARIMA Regime-Switching Forecast  │
    │    - Detect vol regimes              │
    │    - Fit regime models               │
    │    - Generate forecasts              │
    └───────────────┬──────────────────────┘
                    │
    ┌───────────────▼──────────────────────┐
    │ 6. Agent Debate                      │
    │    Wassim: Fundamental analysis      │
    │    Yugo: Regime-switching forecasts  │
    │    3 rounds each (6 total turns)     │
    └───────────────┬──────────────────────┘
                    │
    ┌───────────────▼──────────────────────┐
    │ 7. Consensus Mechanism               │
    │    - Collect direction/conf/rel      │
    │    - Apply 7-step protocol           │
    │    - Final recommendation            │
    └───────────────┬──────────────────────┘
                    │
    ┌───────────────▼──────────────────────┐
    │ 8. Portfolio Construction            │
    │    - Top N stocks (user choice)      │
    │    - Equal-weight or inverse-vol     │
    └───────────────┬──────────────────────┘
                    │
    ┌───────────────▼──────────────────────┐
    │ 9. Backtesting                       │
    │    - Daily returns                   │
    │    - Periodic rebalancing            │
    │    - CAGR, Sharpe, MaxDD             │
    │    - Equity curve plot               │
    └──────────────────────────────────────┘
```

## Tips for Best Results

1. **Sector Selection**: Ensure all 10 stocks are truly in the same sector for meaningful comparison
2. **Time Period**: Use at least 2-3 years of data for reliable regime detection
3. **Portfolio Size**: 5-7 stocks typically provides good diversification without dilution
4. **Rebalancing**: Monthly is a good balance between turnover costs and maintaining target weights
5. **Interpretation**: 
   - Wassim identifies *which* stocks to buy (fundamentals)
   - Yugo identifies *when* (regime timing)
   - Together they determine portfolio composition

## Output Files

- `sector_portfolio_{Sector}_{timestamp}.png` - Equity curve chart
- Agent debate logs in console
- Performance metrics printed

## Common Issues

**Different Sectors Warning:**
```
⚠️  Warning: Multiple sectors detected: {'Technology': 8, 'Communication': 2}
```
- Some stocks may be classified differently
- Analysis proceeds using the most common sector
- Consider replacing outliers for purer sector exposure

**Insufficient Regime Data:**
```
⚠️ Insufficient data for regime 'high_vol' (12 obs), skipping.
```
- Short time periods may not have enough data for all regimes
- Extend date range or accept limited regime coverage

**ARIMA Fitting Issues:**
```
⚠️ Could not fit ARIMA for regime 'low_vol': ...
```
- Some regimes may have non-stationary data
- The system will use the best available model
- Consider different ARIMA order parameters if persistent

