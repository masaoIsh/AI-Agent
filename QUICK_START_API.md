# Quick Start Guide - API-Only System

## ⚡ 30-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run!
python interactive_cli.py
```

## 🏢 Sector Analysis + AI Debate + Consensus Filter

**What:** Sector comparison with agent debate and consensus-driven portfolio construction

**Input:**
```
Tickers: AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM
Start: 2020-01-01
End: [Enter for today]
```

**Output:**
- Sector comparison (PBR/ROE/ROA rankings)
- ARIMA regime forecast
- Agent debate transcript
- Consensus filter (BUY/HOLD/SELL recommendation)
- Portfolio backtest with 3 visualizations
- Equity curves PNG

---

## 🌐 Data Sources

### Yahoo Finance (Automatic)
- **Daily prices**: Open, High, Low, Close, Volume, Adj Close
- **Fundamentals**: PBR, ROE, ROA, PE ratio, profit margin, debt/equity

---

## 📝 Example Session

### Sector Analysis with Consensus Filter
```
python interactive_cli.py

AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM
2020-01-01
[Enter]

→ Sector comparison: NVDA #1 (composite 2.35)
→ ARIMA regime: medium_vol
→ Wassim: BUY (conf 0.85, reliability 0.90)
→ Yugo: BUY (conf 0.75, reliability 0.85)
→ Consensus: BUY (strength 0.72)
→ 🟢 GREEN LIGHT for portfolio construction

y [construct portfolio]
5 [top stocks]
invvol

→ CAGR: 0.28, Sharpe: 1.34, MaxDD: -0.15
→ 3 charts saved:
  - sector_portfolio_Technology.png
  - cumulative_return_Technology.png
  - rolling_sharpe_Technology.png
```

---

## 💡 Tips

1. **Stock picking**: Enter 5-10 stocks from the same sector for best comparison
2. **Time period**: Use 2+ years of data for reliable results
3. **Consensus filter**: Trust agent recommendations (override only if you disagree)
4. **Strategy**: Inverse-vol (invvol) = risk-based weighting, better than equal-weight
5. **Visualizations**: Review all 3 charts to understand portfolio behavior

---

## 📚 Full Documentation

- **API-Only Overview**: `API_ONLY_SUMMARY.md`
- **Sector Analysis Guide**: `SECTOR_ANALYSIS_GUIDE.md`
- **Portfolio System**: `PORTFOLIO_SYSTEM_SUMMARY.md`
- **Main README**: `README.md`

---

## ❓ Troubleshooting

**"yfinance not found"**
```bash
pip install -r requirements.txt
```

**"No data for ticker XXX"**
- Check ticker spelling
- Use uppercase
- Try different date range

**"Rate limit error"**
- System includes 0.5s delays between requests
- If persistent, wait a few minutes and retry

---

## 🎯 Quick Reference

**System Features:**
- 100% API-based (no CSVs!)
- Sector-based fundamental comparison
- ARIMA regime-switching forecasts
- AI agent debate with consensus filter
- Portfolio backtesting with 3 visualizations
- Daily price data from Yahoo Finance

