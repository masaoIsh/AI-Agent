# Portfolio Construction & VECM System Summary

## Overview

The system has been extended from a single-stock CSV analysis tool to a comprehensive portfolio construction and backtesting platform with VECM cointegration analysis.

## New Capabilities

### 1. **Data Fetching** (`data_fetchers.py`)
- **Yahoo Finance Integration**: Fetches OHLCV data for multiple equities via `yfinance`
- **FRED Integration**: Fetches macroeconomic time series from Federal Reserve Economic Data
- Environment-based API key management for FRED

### 2. **Portfolio Construction** (`portfolio_constructor.py`)
- **Equal-Weight Strategy**: Simple 1/N allocation across assets
- **Inverse-Volatility Strategy**: Risk-based weighting using rolling volatility lookback

### 3. **Backtesting Engine** (`backtester.py`)
- Daily returns computation from price series
- Configurable rebalancing frequency (Daily/Weekly/Monthly/Quarterly)
- Transaction cost modeling (basis points per turnover)
- Performance metrics:
  - CAGR (Compounded Annual Growth Rate)
  - Volatility (annualized)
  - Sharpe Ratio
  - Maximum Drawdown
- Equity curve generation and visualization

### 4. **VECM Cointegration Analysis** (`vecm_analyzer.py`)
- **Johansen Cointegration Test**: Detects long-run equilibrium relationships
- **Cointegration Rank Detection**: Automatic rank selection via trace statistics
- **Beta Coefficients**: Long-run equilibrium vectors showing how variables move together
- **Alpha Coefficients**: Adjustment speeds back to equilibrium after shocks
- Formatted reports for AI agent consumption

### 5. **Enhanced Agent Workflow**

#### Mode 1: CSV-based Agent Analysis (Enhanced)
- Now includes VECM analysis alongside VAR/Granger causality
- Wassim receives VECM cointegration reports showing:
  - Long-run equilibrium relationships between returns and macro variables
  - Adjustment speeds (alpha coefficients)
  - Cointegration vectors (beta coefficients)
- Agents use VECM insights to assess fundamental equilibrium vs short-term deviations

#### Mode 2: Portfolio Backtesting (New)
- Interactive workflow:
  1. Enter tickers (e.g., AAPL,MSFT,GOOG)
  2. Select date range
  3. Choose strategy (equal-weight or inverse-vol)
  4. Set rebalancing frequency
  5. Optional: trading costs
  6. Optional: FRED macro series + VECM analysis on portfolio returns
- Output:
  - Performance metrics printed to console
  - Equity curve saved as PNG
  - VECM cointegration analysis if FRED data requested

## Setup Requirements

### Dependencies Added
```bash
yfinance>=0.2.40
fredapi>=0.5.2
```

### FRED API Key Setup
```bash
# One-time setup (for current session):
source set_fred_key.sh

# Permanent setup (add to ~/.zshrc):
export FRED_API_KEY="9d0f00f8cad2d867849f09410fb483a0"
```

## Usage Examples

### Portfolio Backtesting
```bash
python interactive_cli.py
# Select option 2

# Enter tickers: AAPL,MSFT,GOOG
# Start date: 2015-01-01
# End date: 2023-12-31
# Strategy: invvol
# Rebalance frequency: M
# Trading cost: 5
# FRED analysis: y
# FRED series: CPIAUCSL,UNRATE,DGS10
```

Output:
```
📊 Performance Metrics
============================================================
CAGR: 0.1523
Vol: 0.1834
Sharpe: 0.8301
MaxDD: -0.2345

🖼️  Saved equity curve: portfolio_equity_20251022_143022.png

🔬 Running VECM Cointegration Analysis...
Johansen Cointegration Test
============================================================
Series: Portfolio_Return, CPIAUCSL, UNRATE, DGS10
Detected Cointegration Rank: 1

VECM Analysis Results
============================================================
Cointegration Rank: 1
...
```

### CSV Agent Analysis with VECM
```bash
python interactive_cli.py
# Select option 1

# Enter MACRO CSV: macro_data.csv
# Enter PRICE CSV: stock_data.csv
# Stock symbol: AAPL
```

Agents receive:
1. Indicator forecasting results (1D/1W MSE/MAE)
2. Macro VAR/Granger causality table
3. **NEW**: VECM cointegration analysis showing long-run equilibrium relationships

## Key Files

| File | Purpose |
|------|---------|
| `data_fetchers.py` | Yahoo Finance & FRED API wrappers |
| `portfolio_constructor.py` | Equal-weight & inverse-vol strategies |
| `backtester.py` | Backtest engine with metrics |
| `vecm_analyzer.py` | VECM cointegration analysis |
| `interactive_cli.py` | Enhanced CLI with 2 modes |
| `set_fred_key.sh` | FRED API key helper script |

## Wassim's Enhanced Capabilities

Wassim now receives and interprets:

1. **VAR/Granger Causality**: Which macro variables predict returns
2. **VECM Cointegration**: Long-run equilibrium relationships
   - Beta vectors: How variables are bound together in equilibrium
   - Alpha coefficients: How fast deviations correct
3. **Interpretation**: Assess if current prices deviate from fundamental equilibrium (mean-reversion opportunity) or if relationships have broken down

## Future Extensions

Potential additions:
- Mean-variance optimization (Markowitz)
- Risk-parity weighting
- Momentum overlays
- Constraint-based optimization (sector caps, max weight)
- Multi-factor models (Fama-French)
- Rolling walk-forward strategy optimization

