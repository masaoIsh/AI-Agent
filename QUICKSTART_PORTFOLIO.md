# Portfolio Backtesting Quick Start Guide

## Installation

1. **Install new dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up FRED API key** (your key is already configured):
```bash
source set_fred_key.sh
```

Or for permanent setup:
```bash
echo 'export FRED_API_KEY="9d0f00f8cad2d867849f09410fb483a0"' >> ~/.zshrc
source ~/.zshrc
```

## Running Portfolio Backtest

```bash
python interactive_cli.py
```

**Select option 2** when prompted.

### Example Session

```
Select mode:
1) Agent analysis (CSV-based)
2) Portfolio backtesting (Yahoo Finance)
Enter 1 or 2 (default 1): 2

📦 Portfolio Backtesting Mode
============================================================
Enter comma-separated tickers (e.g., AAPL,MSFT,GOOG): AAPL,MSFT,GOOGL,AMZN

Start date [YYYY-MM-DD, default 2000-01-01]: 2015-01-01
End date [YYYY-MM-DD, default today]: 2024-12-31
Strategy [equal|invvol] (default equal): invvol
Rebalance frequency [D/W/M/Q] (default M): M
Trading cost (bps per turnover, default 0): 5

⬇️  Fetching Yahoo Finance data...

🧮 Using strategy: invvol → weights:
AAPL     0.2341
MSFT     0.2876
GOOGL    0.2512
AMZN     0.2271

📊 Performance Metrics
============================================================
CAGR: 0.1834
Vol: 0.1923
Sharpe: 0.9543
MaxDD: -0.2145

🖼️  Saved equity curve: portfolio_equity_20251022_143022.png

Fetch FRED macro series and run VECM? [y/N]: y
Enter comma-separated FRED series IDs (e.g., CPIAUCSL,UNRATE,DGS10,FEDFUNDS,INDPRO): CPIAUCSL,UNRATE,DGS10

✅ FRED series fetched:
            CPIAUCSL    UNRATE    DGS10
2024-11-01   315.620     3.7      4.28
2024-12-01   316.123     3.8      4.35

🔬 Running VECM Cointegration Analysis...
Johansen Cointegration Test
============================================================
Series: Portfolio_Return, CPIAUCSL, UNRATE, DGS10
Detected Cointegration Rank: 1

Trace Statistics vs 95% Critical Values:
  r ≤ 0: Trace=45.23, Crit=40.17 ***
  r ≤ 1: Trace=25.67, Crit=24.28

VECM Analysis Results
============================================================
Cointegration Rank: 1
Series: Portfolio_Return, CPIAUCSL, UNRATE, DGS10

Cointegration Vectors (Beta - Long-run relationships):
                       CV1
Portfolio_Return  1.000000
CPIAUCSL         -0.023456
UNRATE            0.234567
DGS10            -0.123456

Adjustment Coefficients (Alpha - Speed of adjustment to equilibrium):
                       CV1
Portfolio_Return -0.045678
CPIAUCSL          0.001234
UNRATE           -0.012345
DGS10             0.023456
```

## Common FRED Series IDs

| Series ID | Description |
|-----------|-------------|
| `CPIAUCSL` | Consumer Price Index (CPI) |
| `UNRATE` | Unemployment Rate |
| `DGS10` | 10-Year Treasury Constant Maturity Rate |
| `FEDFUNDS` | Federal Funds Effective Rate |
| `INDPRO` | Industrial Production Index |
| `GDP` | Gross Domestic Product |
| `DEXUSEU` | USD/EUR Exchange Rate |
| `VIXCLS` | VIX Volatility Index |

Browse more at: https://fred.stlouisfed.org/

## Strategy Options

### Equal-Weight (`equal`)
- Simple 1/N allocation
- Rebalances to equal weights at each rebalance date
- Good baseline strategy

### Inverse-Volatility (`invvol`)
- Weights inversely proportional to rolling volatility (63-day lookback)
- Lower volatility assets get higher weights
- Risk-based allocation

## Rebalancing Frequencies

- `D` - Daily (high turnover, expensive)
- `W` - Weekly
- `M` - Monthly (recommended)
- `Q` - Quarterly (lower turnover)

## Output Files

- `portfolio_equity_YYYYMMDD_HHMMSS.png` - Equity curve chart

## Tips

1. **Start with monthly rebalancing** to reduce trading costs
2. **Use inverse-vol for risk management** in volatile markets
3. **VECM analysis helps identify** when portfolio returns deviate from macro equilibrium
4. **Negative alpha on returns** suggests mean-reversion (opportunity)
5. **Compare Sharpe ratios** across different strategies

## Troubleshooting

**FRED API Error**:
```
EnvironmentError: Set FRED_API_KEY environment variable
```
Solution: Run `source set_fred_key.sh` before starting Python

**Yahoo Download Issues**:
- Check tickers are valid (uppercase)
- Ensure date range has data available
- Some tickers may not have full history

**VECM No Cointegration**:
- Try different FRED series
- Ensure sufficient data (>50 observations after alignment)
- Short time periods may not show long-run relationships

