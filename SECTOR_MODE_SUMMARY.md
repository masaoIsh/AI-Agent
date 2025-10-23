# Sector Portfolio Analysis - Implementation Summary

## ✅ All Requirements Fulfilled

Your request was to:
1. ✅ Pick 10 stocks in the same sector (comparable)
2. ✅ Wassim uses PBR/ROE/ROA to compare equities within sector
3. ✅ Yugo does forecasting using ARIMA regime-switching
4. ✅ Agents debate using current consensus mechanism
5. ✅ Construct portfolio and perform backtesting

## New Components Created

### 1. `data_fetchers.py` - Extended
**Added `fetch_fundamentals(symbols)`**
- Fetches PBR, ROE, ROA, PE ratio, profit margin, debt-to-equity
- Gets sector and industry classifications
- Returns comprehensive DataFrame for all stocks

### 2. `sector_comparator.py` - NEW
**SectorComparator class for relative valuation:**
- `compute_sector_comparison()`: Calculates percentile rankings and z-scores
- `format_comparison_report()`: Generates readable reports for Wassim
- `get_sector_rankings()`: Composite score ranking (ROE + ROA - PBR z-scores)

**Key outputs:**
- Percentile ranks (0-100): Where each stock stands in the sector
- Z-scores: Standard deviations from sector average
- Composite scores: Combined quality + valuation metric

### 3. `arima_regime_switching.py` - NEW
**ARIMARegimeSwitching class for Yugo:**
- `detect_regimes()`: Classifies periods into low/medium/high volatility
- `fit_regime_models()`: Fits separate ARIMA models per regime
- `forecast()`: Generates forecasts using appropriate regime model
- `format_report()`: Creates reports showing regime distribution, current regime, forecasts

**Regime detection:**
- Rolling volatility calculation (20-day window)
- Percentile-based thresholds (33rd, 67th percentiles)
- Separate ARIMA(2,1,2) models for each regime

### 4. `interactive_cli.py` - Enhanced
**Updated agent prompts:**
- **Wassim**: Now specializes in PBR/ROE/ROA sector comparison
  - Interprets percentile rankings
  - Analyzes z-scores for premium/discount identification
  - Uses composite scores to find value opportunities
  
- **Yugo**: Now specializes in ARIMA regime-switching
  - Identifies current volatility regime
  - Explains regime implications for forecast reliability
  - Compares AIC/BIC across regime models
  - Uses regime-specific forecasts for price targets

**New workflow: `run_sector_portfolio_analysis()`**
1. Collect 10 sector stocks from user
2. Fetch fundamentals via yfinance
3. Run sector comparison analysis
4. Fetch price data
5. Run ARIMA regime-switching on representative stock
6. Initialize agents with enhanced prompts
7. Agents debate with full sector + regime data
8. Consensus mechanism produces recommendation
9. Optional: construct portfolio from top-ranked stocks
10. Backtest with chosen strategy

**Updated main menu:**
- Option 1: CSV-based agent analysis (original + VECM)
- Option 2: Portfolio backtesting (Yahoo)
- Option 3: Sector portfolio analysis ⭐ **NEW**

## How It Works

### Agent Specialization

#### Wassim's Fundamental Analysis
**Receives:**
```
Sector Comparison Analysis: Technology
Number of stocks in sector: 10

Sector Averages:
  PB_RATIO: Mean=23.45, Median=18.23
  ROE: Mean=0.45, Median=0.39
  ROA: Mean=0.17, Median=0.15

Stock Analysis: NVDA
  ROE: 1.2301 (Percentile: 95.0, Z-score: 2.45) Above average
  ROA: 0.4512 (Percentile: 92.0, Z-score: 2.12) Above average
  PB_RATIO: 55.23 (Percentile: 88.0, Z-score: 1.87) Premium valuation
  
Composite Score: 2.35 (Rank #1)
```

**Wassim's analysis:**
- "NVDA shows exceptional profitability (ROE at 95th percentile)"
- "Despite high PBR, the premium is justified by superior fundamentals"
- "Composite score of 2.35 ranks #1, indicating best risk-adjusted value"
- "RECOMMENDATION: BUY with high conviction"

#### Yugo's Regime-Switching Forecasts
**Receives:**
```
ARIMA Regime-Switching Analysis (AAPL)
Regime Distribution:
  low_vol: 523 periods (41.6%)
  medium_vol: 412 periods (32.7%)
  high_vol: 323 periods (25.7%)

Current Regime: medium_vol

Fitted Models:
  low_vol: AIC=5234.56
  medium_vol: AIC=4123.45 ← Best fit
  high_vol: AIC=6789.01

Forecast (medium_vol regime):
  Step 1: 175.45 (95% CI: [170.23, 180.67])
  Step 2: 176.89 (95% CI: [168.56, 185.22])
```

**Yugo's analysis:**
- "Currently in medium_vol regime (moderate uncertainty)"
- "Forecast shows +2.3% uptrend over 5 days"
- "Confidence intervals are reasonable, not too wide"
- "Medium_vol model has best AIC, suggesting good fit"
- "Technical momentum confirms uptrend"
- "RECOMMENDATION: BUY with medium confidence due to regime"

### Debate Integration
Agents receive **combined data**:
- Sector comparison table (all 10 stocks)
- Rankings by composite score
- ARIMA regime analysis for representative stock
- Historical price data

They debate for **3 rounds each** (6 total turns):
- Round 1: Initial analysis
- Round 2: Respond to each other, refine views
- Round 3: Final consensus with direction/confidence/reliability

### Consensus Mechanism
Same 7-step protocol as before:
1. Collect agent data (direction, confidence, reliability)
2. Check unanimous high-confidence HOLD
3. Minimum confidence threshold (≥0.5)
4. Conflict detection (opposite directions with high reliability)
5. Vibe check (normalized directional coherence |V| ≥ 0.5)
6. Value computation & t-test
7. Summary and final recommendation

### Portfolio Construction
After consensus:
- User chooses top N stocks (default 5)
- Filters by composite score rankings
- Equal-weight or inverse-volatility strategy
- Monthly rebalancing (configurable)
- 5 bps trading costs

### Backtesting Output
```
📊 Portfolio Performance Metrics
CAGR: 0.2845
Vol: 0.2123
Sharpe: 1.3401
MaxDD: -0.1834

🖼️  Saved: sector_portfolio_Technology_20251022_143022.png
```

## Usage Example

```bash
python interactive_cli.py
```

**Session:**
```
Select mode:
1) Agent analysis (CSV-based with VECM)
2) Portfolio backtesting (Yahoo Finance)
3) Sector portfolio analysis with agent debate (NEW!)
Enter 1, 2, or 3: 3

Enter 10 stock tickers in the same sector: 
AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM

Start date: 2020-01-01
End date: 2024-12-31

[... fundamentals fetched ...]
[... sector comparison computed ...]
[... ARIMA regime-switching run ...]
[... agents debate ...]
[... consensus reached: BUY ...]

Construct portfolio? y
How many top stocks? 5
Strategy: invvol
Rebalance: M

[... portfolio backtested ...]
CAGR: 0.28, Sharpe: 1.34
```

## Key Advantages

1. **Sector-Pure Comparison**: All metrics normalized within sector
2. **Regime Awareness**: Forecasts adapt to market volatility
3. **Agent Specialization**: 
   - Wassim = "Which stocks?" (fundamentals)
   - Yugo = "When/How confident?" (regime timing)
4. **Automated Ranking**: Composite score identifies best opportunities
5. **End-to-End**: From stock selection to backtest in one workflow
6. **Consensus-Driven**: Not just analysis, but actionable BUY/SELL/HOLD

## Sector Examples

**Technology:**
```
AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM
```

**Financials:**
```
JPM,BAC,WFC,C,GS,MS,BLK,SCHW,AXP,USB
```

**Healthcare:**
```
JNJ,UNH,PFE,ABBV,TMO,MRK,ABT,DHR,LLY,AMGN
```

**Energy:**
```
XOM,CVX,COP,SLB,EOG,MPC,PSX,VLO,OXY,HAL
```

**Consumer Discretionary:**
```
AMZN,TSLA,HD,NKE,MCD,SBUX,TGT,LOW,BKNG,CMG
```

## Documentation

- **README.md**: Updated with Mode 3 overview
- **SECTOR_ANALYSIS_GUIDE.md**: Comprehensive usage guide with examples
- **SECTOR_MODE_SUMMARY.md**: This file (implementation summary)

## Files Modified/Created

### Modified
- `data_fetchers.py`: Added `fetch_fundamentals()`
- `interactive_cli.py`: 
  - Updated Wassim/Yugo prompts
  - Added `run_sector_portfolio_analysis()`
  - Updated main menu

### Created
- `sector_comparator.py`: Sector relative valuation
- `arima_regime_switching.py`: Regime-aware ARIMA forecasting
- `SECTOR_ANALYSIS_GUIDE.md`: User documentation
- `SECTOR_MODE_SUMMARY.md`: This implementation summary

## Next Steps

You can now:
1. Run sector analysis on any 10 stocks
2. Let Wassim and Yugo debate using their specialized methodologies
3. Get consensus-driven recommendations
4. Construct and backtest portfolios from top-ranked stocks
5. Save equity curves and performance metrics

**All your requirements have been implemented!** 🎉

