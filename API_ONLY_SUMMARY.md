# API-Only System Summary

## ✅ Migration Complete: CSV → API-Based

The system has been fully migrated to use **only APIs** (Yahoo Finance + FRED). No CSV files needed!

## What Changed

### ❌ Removed
- **Mode 1** (CSV-based agent analysis) - DELETED
- `perform_indicator_analysis()` method - DELETED
- `run_interactive_analysis()` method - DELETED
- `main()` function - DELETED
- All CSV file upload prompts
- Indicator forecaster CSV workflow
- Macro VAR CSV workflow

### ✅ Updated System

Now **2 modes** instead of 3:

#### **Mode 1: Portfolio Backtesting with VECM** (was Mode 2)
**What it does:**
1. User inputs tickers (e.g., `AAPL,MSFT,GOOGL,AMZN`)
2. Yahoo Finance fetches daily price data
3. FRED automatically fetches default macro series:
   - `CPIAUCSL` - CPI
   - `UNRATE` - Unemployment
   - `DGS10` - 10Y Treasury
   - `FEDFUNDS` - Fed Funds Rate
   - `INDPRO` - Industrial Production
4. Portfolio construction (equal-weight or inverse-vol)
5. VECM analysis on portfolio returns + macro variables
6. Backtest with performance metrics

**VECM Variables:**
- `Portfolio_Return` (from equity curve)
- `CPIAUCSL`, `UNRATE`, `DGS10`, `FEDFUNDS`, `INDPRO`
- **Total: 6 variables**

#### **Mode 2: Sector Portfolio Analysis** (was Mode 3)
**What it does:**
1. User inputs 10 sector stocks
2. Yahoo Finance fetches:
   - Daily prices
   - Fundamentals (PBR, ROE, ROA, PE, etc.)
3. Sector comparison analysis (percentiles, z-scores, rankings)
4. ARIMA regime-switching forecasts
5. Wassim + Yugo debate (3 rounds each)
6. Consensus mechanism
7. Portfolio construction from top-ranked stocks
8. Backtest with performance metrics

**No VECM in Mode 2** (focuses on sector comparison + ARIMA regimes instead)

## Data Flow

### Mode 1: Portfolio + VECM
```
User Input: AAPL,MSFT,GOOGL,AMZN
    ↓
Yahoo Finance API → Daily prices (2000-01-01 to today)
    ↓
FRED API → Macro series (CPIAUCSL, UNRATE, DGS10, FEDFUNDS, INDPRO)
    ↓
Portfolio Construction → Equal-weight or Inverse-Vol
    ↓
Backtest → Daily returns, monthly rebalancing
    ↓
VECM Analysis → Cointegration test (Portfolio_Return + 5 macro vars)
    ↓
Output: CAGR, Sharpe, MaxDD, Beta/Alpha coefficients, equity curve PNG
```

### Mode 2: Sector Analysis
```
User Input: 10 sector tickers
    ↓
Yahoo Finance API → Prices + Fundamentals
    ↓
Sector Comparison → Percentiles, Z-scores, Composite Scores
    ↓
ARIMA Regime-Switching → Volatility regime detection
    ↓
Wassim + Yugo Debate → 6 turns total
    ↓
Consensus → BUY/SELL/HOLD
    ↓
Portfolio Construction → Top N stocks
    ↓
Backtest → Performance metrics
    ↓
Output: CAGR, Sharpe, MaxDD, equity curve PNG
```

## VECM Details

### Default FRED Series (Mode 1)
| Series ID | Name | Frequency |
|-----------|------|-----------|
| `CPIAUCSL` | Consumer Price Index | Monthly |
| `UNRATE` | Unemployment Rate | Monthly |
| `DGS10` | 10-Year Treasury Yield | Daily |
| `FEDFUNDS` | Federal Funds Rate | Monthly |
| `INDPRO` | Industrial Production Index | Monthly |

### VECM Output Example
```
VECM Analysis Results
Cointegration Rank: 1
Series: Portfolio_Return, CPIAUCSL, UNRATE, DGS10, FEDFUNDS, INDPRO

Beta (Long-run equilibrium):
                      CV1
Portfolio_Return   1.0000
CPIAUCSL          -0.0234
UNRATE             0.2346
DGS10             -0.1235
FEDFUNDS          -0.0456
INDPRO             0.0678

Alpha (Adjustment speeds):
                      CV1
Portfolio_Return  -0.0457
CPIAUCSL           0.0012
UNRATE            -0.0123
DGS10              0.0234
FEDFUNDS           0.0089
INDPRO            -0.0034
```

**Interpretation:**
- **Beta**: How variables move together in long-run equilibrium
- **Alpha**: Speed of mean-reversion after shocks
- Negative alpha on `Portfolio_Return` suggests portfolio corrects toward equilibrium

## Usage Examples

### Mode 1: Portfolio Backtest
```bash
$ python interactive_cli.py

Select mode:
1) Portfolio backtesting with VECM (Yahoo Finance + FRED)
2) Sector portfolio analysis with agent debate (Yahoo Finance + optional FRED)
Enter 1 or 2: 1

Enter comma-separated tickers: AAPL,MSFT,GOOGL,AMZN
Start date: 2020-01-01
End date: [Enter]
Strategy: invvol
Rebalance frequency: M
Trading cost (bps): 5
Use custom FRED series IDs? [y/N]: [Enter for default]

# System fetches Yahoo + FRED data...
# Constructs portfolio...
# Runs backtest...
# Performs VECM analysis...

CAGR: 0.2345
Sharpe: 1.23
MaxDD: -0.18

VECM Cointegration Rank: 1
[Beta/Alpha tables...]

Saved: portfolio_equity_20251022_143022.png
```

### Mode 2: Sector Analysis
```bash
$ python interactive_cli.py

Select mode: 2

Enter 10 tickers: AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM
Start date: 2020-01-01
End date: [Enter]

# System fetches fundamentals...
# Computes sector comparison...
# Runs ARIMA regimes...
# Agents debate...
# Reaches consensus...

Construct portfolio? y
Top stocks: 5
Strategy: invvol

CAGR: 0.28
Sharpe: 1.34

Saved: sector_portfolio_Technology_20251022_143022.png
```

## Benefits of API-Only Approach

1. **No manual data prep**: No need to find/download CSVs
2. **Always fresh data**: Yahoo + FRED update automatically
3. **Standardized format**: APIs return consistent data structures
4. **Scalable**: Easy to analyze 10, 20, or 100 stocks
5. **Reproducible**: Same tickers + dates = same results
6. **Lower barrier**: Just install packages and run

## Required Setup

### One-time: Install Dependencies
```bash
pip install -r requirements.txt
```

### One-time: Set FRED API Key
```bash
source set_fred_key.sh
```

### Ready to Run
```bash
python interactive_cli.py
```

## Files Removed/Deprecated

- No longer need CSV files
- `indicator_forecaster.py` - Still exists but not used in main workflow
- `macro_var_analyzer.py` - Still exists but not used in main workflow

These modules are kept for reference but main system uses APIs directly.

## Summary

**Before:** 3 modes (1 CSV-based, 2 API-based)
**After:** 2 modes (both 100% API-based)

**Data sources:**
- Yahoo Finance: Prices + Fundamentals
- FRED: Macro indicators

**No CSV files needed anywhere!** 🎉

