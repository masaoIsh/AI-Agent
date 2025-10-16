# AI Financial Analysis Multi-Agent System

A sophisticated multi-agent system that combines technical indicator-based forecasting with macro VAR/Granger causality analysis. Two specialized AI agents (Fundamental and Valuation analysts) provide BUY/SELL recommendations based on comprehensive quantitative analysis and engage in interactive debates to reach consensus.

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (recommended: Python 3.11 or 3.12)
- **Ollama** (for local AI models)
- **Git** (for cloning the repository)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Ai-Agent.git
   cd Ai-Agent
   ```

2. **Install Ollama** (macOS):
   ```bash
   brew install ollama
   brew services start ollama
   ```

   **Install Ollama** (Linux):
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama serve
   ```

   **Install Ollama** (Windows):
   - Download from [ollama.ai](https://ollama.ai/download)

3. **Download the AI model**:
   ```bash
   ollama pull llama3.2
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the interactive system**:
   ```bash
   python interactive_cli.py
   ```

## 🎯 Features

### Two Specialized AI Agents

- **🧮 Wassim (Fundamental Agent)**: Analysis using macro VAR/Granger causality analysis
- **📈 Yugo (Valuation Agent)**: Technical indicator-based forecasting

### Interactive Debate System

- **Structured 3-Round Debates**: Each agent speaks exactly 3 times maximum (6 total turns for 2 agents)
- **Sophisticated Consensus Protocol**: 7-step statistical validation with confidence/reliability weighting
- **Automatic Termination**: System automatically stops after each agent completes 3 turns
- **Statistical Validation**: t-test and weighted scoring for investment decisions
- **Real-time Analysis**: Watch agents debate and build consensus in real-time
- **Comprehensive Reports**: Get detailed breakdowns of individual agent positions with consensus method

### Local AI Processing

- **No API Keys Required**: Uses Ollama with local models for complete privacy
- **Offline Capable**: Works without internet connection once set up
- **Customizable Models**: Use any Ollama-compatible model

### Advanced Quantitative Analysis

#### Technical Indicator Forecasting
- **RandomForest Model**: Machine learning approach using technical indicators as features
- **RSI (Relative Strength Index)**: Momentum oscillator measuring overbought/oversold conditions (14-period)
- **Bollinger Bands**: Price volatility bands with moving average and standard deviation (20-period, 2σ)
- **MACD (Moving Average Convergence Divergence)**: Trend-following momentum indicator (12,26,9 periods)
- **Realized Volatility**: Annualized volatility from 20-day rolling log returns
- **Walk-Forward Validation**: Robust out-of-sample testing with MSE/MAE metrics
- **1-Day & 1-Week Forecasts**: Multi-horizon predictions with performance metrics

#### Macro VAR Analysis & Granger Causality
- **VAR Model**: Vector Autoregression analyzing relationships between macro variables and asset returns
- **Granger Causality Testing**: Statistical test to determine if macro variables predict asset returns
- **Economic Indicators**: CPI, Unemployment, 10Y Treasury, Fed Funds Rate, Industrial Production Index
- **Statistical Significance**: p-values indicate strength of causal relationships
- **Direction & Strength**: Positive/negative correlations with magnitude measurements
- **Dual CSV Input**: Separate macro economic data and price data for comprehensive analysis

#### Visualization & Output
- **Forecast Plots**: Price charts with technical indicators overlaid
- **Indicator Panels**: Separate RSI and MACD visualization panels
- **Performance Metrics**: MSE/MAE for 1-day and 1-week ahead forecasts
- **Causality Tables**: Structured output showing which macro variables drive returns

### Sophisticated Consensus Protocol

- **7-Step Decision Process**: Structured validation with statistical rigor
- **Rule-Based Validation**: 4 rules for conflict detection and confidence thresholds
- **Statistical Testing**: t-test validation with p-value < 0.05 significance
- **Weighted Scoring**: Combines direction, confidence, and reliability metrics
- **Transparent Process**: Detailed logging of each consensus step
- **Fallback Mechanism**: Graceful degradation to simple counting if needed

**Consensus Rules:**
1. **Minimum Confidence**: All agents must have confidence ≥ 0.5
2. **Conflict Detection**: Identifies reliable agents with opposing views
3. **Vibe Check**: Normalized directional coherence (|V| ≥ 0.5)
4. **Unanimous Hold**: Shortcut for confident neutral positions

## 📖 Usage Examples

### Basic Stock Analysis with Dual CSV Input

```bash
python interactive_cli.py
```

**Example Session**:
```
🤖 Financial Analysis Multi-Agent System
======================================================================
Enter CSV file path with historical data (or press Enter to skip): stock_data.csv

Which equity/stock does this CSV data represent? (e.g., AAPL, TSLA, MSFT): AAPL

Enter analysis prompt (or press Enter for default): 

📊 Analyzing: AAPL
Prompt: Analyze AAPL using the provided historical data and ARIMA forecasting analysis to determine whether a risk neutral investor should BUY or SELL this stock. Base your analysis on the time series data and forecasting results.
📈 CSV Data: stock_data.csv
======================================================================

Initializing AI agents...
✅ Agents initialized successfully!

🤖 Agents are now analyzing and debating...
============================================================

🧮 Wassim (Fundamental Agent) - Round 1, Turn 1:
Based on the macro VAR analysis, CPI shows strong positive Granger causality...

📈 Yugo (Valuation Agent) - Round 1, Turn 1:
Based on the indicator-based forecasting, 1D MSE of 0.0234 suggests strong predictive power...

🧮 Wassim (Fundamental Agent) - Round 3, Turn 3:
[Final analysis with consensus statement]
CONSENSUS: direction=1 confidence=0.8 reliability=0.9

📈 Yugo (Valuation Agent) - Round 3, Turn 3:
[Final analysis with consensus statement]
CONSENSUS: direction=1 confidence=0.7 reliability=0.8

🧮 Applying Sophisticated Consensus Protocol...
============================================================
[Step 1] Collecting agent inputs
  Wassim        d=+1, c=0.80, r=0.90
  Yugo          d=+1, c=0.70, r=0.80
[Step 3] Rule 1 — Minimum Confidence Threshold
✅ Confidence threshold satisfied.
[Step 4] Rule 2 — Directional Conflict Check
✅ No critical directional conflict detected.
[Step 5] Rule 3 — Normalized Total Vibe Check
✅ |V| = 0.75 ≥ 0.5 → Directional coherence reached.
[Step 6] Value Computation and Statistical Test
🟢 Significant positive value → BUY.

🎉 ANALYSIS COMPLETE!
============================================================
Final Recommendation: BUY
Consensus Reached: Yes
Consensus Method: Sophisticated Protocol
Conversation Length: 6 messages

📈 Recommendation Breakdown:
  BUY: 2

👥 Individual Agent Positions:
  Wassim (Fundamental Agent): BUY
  Yugo (Valuation Agent): BUY

Would you like to analyze another stock? (y/n):
```

### Custom Analysis Prompts

You can provide custom analysis prompts for specific scenarios:

- "Should a growth investor BUY or SELL this stock for a 5-year horizon?"
- "Analyze this stock for a value investor focused on dividend yield"
- "Provide analysis for a day trader considering this position"

### CSV-First Workflow

The system now uses a CSV-first approach where historical data drives the analysis:

```bash
python interactive_cli.py
```

**New Workflow**:
```
🤖 Financial Analysis Multi-Agent System with Indicator-Based Forecasting + Macro VAR
======================================================================
Enter MACRO CSV path ['CPI','Unemployment','10Y_Treasury','FedFundsRate','IP_Index']: macro_data.csv
Enter PRICE CSV path with historical price data: stock_data.csv

Which equity/stock does this CSV data represent? (e.g., AAPL, TSLA, MSFT): AAPL

📈 Conducting Indicator-Based Forecasting on: stock_data.csv
======================================================================
✅ Successfully loaded 1000 data points
📅 Date range: 2020-01-01 to 2023-12-31
📊 Value column: close
📊 Technical Indicators: RSI(14), Bollinger Bands(20,2σ), MACD(12,26,9), Realized Vol(20)
1D-ahead -> MSE: 0.0234, MAE: 0.1234
1W-ahead -> MSE: 0.0456, MAE: 0.2345
... walk-forward progress: 50/200 steps
... walk-forward progress: 100/200 steps
... walk-forward progress: 150/200 steps
... walk-forward progress: 200/200 steps
✅ Forecast plot saved as: indicator_forecast_20241208_143022_price.png

📑 Macro VAR/Granger Causality Analysis Results:
variable       p_value  direction  strength  interpretation
CPI            0.0234   pos        0.3456   Strong predictor (p<0.05)
10Y_Treasury   0.0456   neg        0.2345   Significant predictor
Unemployment   0.1234   pos        0.1234   Moderate predictor
FedFundsRate   0.2345   neg        0.0987   Weak predictor
IP_Index       0.4567   pos        0.0678   Not significant

🤖 Agents are now analyzing and debating...
======================================================================
```

**Required CSV Formats**:

**Macro CSV** (required columns):
```csv
Date,CPI,Unemployment,10Y_Treasury,FedFundsRate,IP_Index
2020-01-01,2.1,3.5,1.8,1.5,100.0
2020-02-01,2.2,3.4,1.9,1.6,101.2
...
```

**Price CSV** (flexible format):
```csv
Date,Close_Price,Volume
2020-01-01,100.50,1500000
2020-01-02,101.25,1600000
...
```

## 📊 Technical Analysis Details

### Technical Indicators Explained

**RSI (Relative Strength Index)**:
- **Formula**: 100 - (100 / (1 + RS)) where RS = Average Gain / Average Loss
- **Period**: 14-day exponential moving average of gains/losses
- **Interpretation**: >70 overbought, <30 oversold, 50 neutral
- **Usage**: Identifies momentum shifts and potential reversal points

**Bollinger Bands**:
- **Components**: Middle band (20-period SMA), Upper band (+2σ), Lower band (-2σ)
- **Width**: Measures volatility (Upper - Lower = 4σ)
- **Interpretation**: Price near bands suggests overbought/oversold conditions
- **Usage**: Volatility-based support/resistance levels

**MACD (Moving Average Convergence Divergence)**:
- **Components**: MACD line (12-EMA - 26-EMA), Signal line (9-EMA of MACD), Histogram (MACD - Signal)
- **Interpretation**: MACD above Signal = bullish, below = bearish
- **Usage**: Trend changes and momentum confirmation

**Realized Volatility**:
- **Calculation**: 20-day rolling standard deviation of log returns × √252
- **Interpretation**: Annualized volatility measure
- **Usage**: Risk assessment and volatility regime identification

### Macro VAR Analysis Details

**Vector Autoregression (VAR)**:
- **Purpose**: Models dynamic relationships between multiple time series
- **Method**: Each variable regressed on lagged values of all variables
- **Lag Selection**: Automatic selection based on AIC/BIC criteria (max 6 lags)

**Granger Causality**:
- **Definition**: Variable X Granger-causes Y if X helps predict Y beyond Y's own history
- **Test**: F-test comparing restricted vs unrestricted VAR models
- **Interpretation**: p-value < 0.05 indicates significant causality

**Economic Indicators**:
- **CPI**: Consumer Price Index (inflation measure)
- **Unemployment**: Unemployment rate (economic health indicator)
- **10Y Treasury**: 10-year Treasury yield (interest rate proxy)
- **Fed Funds Rate**: Federal funds rate (monetary policy indicator)
- **IP Index**: Industrial Production Index (economic activity measure)

## 🛠️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Interactive CLI (interactive_cli.py)       │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│            RoundRobinGroupChat Team                     │
│  • Manages 3-round debate structure                     │
│  • Coordinates agent interactions                       │
│  • Streams real-time conversations                     │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌───▼──────┐ ┌────▼──────┐
│ Fundamental  │ │Sentiment │ │ Valuation │
│   Agent      │ │ Agent    │ │   Agent   │
│              │ │          │ │           │
│ • Financial  │ │ • News   │ │ • DCF     │
│   statements │ │   sentiment│ │   models │
│ • Ratios     │ │ • Social │ │ • Comps   │
│ • Growth     │ │   media  │ │ • Risk    │
└──────────────┘ └──────────┘ └───────────┘
```

## 🔧 Configuration

### Using Different Models

You can use any Ollama-compatible model by modifying the model name in `interactive_cli.py`:

```python
# Line 26 in interactive_cli.py
self.ollama_client = OllamaChatCompletionClient(model="llama3.2")
```

**Available Models**:
```bash
# List available models
ollama list

# Pull different models
ollama pull mistral
ollama pull codellama
ollama pull llama3.1
```

### Customizing Agent Personalities

Edit the system messages in `interactive_cli.py` (lines 33-101) to customize agent personalities and expertise areas.

## 📁 Project Structure

```
Ai-Agent/
├── README.md                 # This file
├── interactive_cli.py        # Main interactive CLI application
├── indicator_forecaster.py   # Technical indicator forecasting module
├── macro_var_analyzer.py     # Macro VAR/Granger causality analysis
├── consensus_mechanism.py    # Sophisticated consensus protocol
├── arima_forecaster.py       # Legacy ARIMA forecasting module
├── requirements.txt          # Python dependencies
├── setup.py                  # Quick setup script
├── test_arima.py            # Legacy ARIMA tests
├── .gitignore               # Git ignore file
└── autogen/                 # AutoGen framework (submodule)
```

## 🚨 Troubleshooting

### Common Issues

**1. Ollama Connection Error**
```
❌ Error: Connection refused
```
**Solution**:
```bash
# Start Ollama service
brew services start ollama  # macOS
# or
ollama serve               # Linux/Windows
```

**2. Model Not Found**
```
❌ Error: model 'llama3.2' not found
```
**Solution**:
```bash
ollama pull llama3.2
```

**3. Import Errors**
```
ModuleNotFoundError: No module named 'autogen_agentchat'
```
**Solution**:
```bash
pip install -r requirements.txt
```

**4. Python Version Issues**
```
Python 3.10+ required
```
**Solution**: Install Python 3.10 or higher

**5. ARIMA Dependencies Missing**
```
ModuleNotFoundError: No module named 'statsmodels'
```
**Solution**: Install ARIMA dependencies:
```bash
pip install pandas numpy matplotlib statsmodels seaborn
```

**6. CSV File Not Found**
```
❌ CSV file not found: /path/to/file.csv
```
**Solution**: 
- Check the file path is correct
- Ensure the file exists and is readable
- Use absolute path if needed: `/Users/username/Downloads/data.csv`

**7. CSV Format Issues**
```
❌ Failed to load CSV data
```
**Solution**: Ensure your CSV has:
- Proper date column (e.g., Date, timeOpen, timestamp)
- Numeric value column (e.g., close, price, value)
- Valid CSV format

### Getting Help

1. **Check Ollama Status**:
   ```bash
   brew services list | grep ollama  # macOS
   ollama list                       # Check models
   ```

2. **Verify Python Installation**:
   ```bash
   python --version
   pip list | grep autogen
   ```

3. **Test Ollama Connection**:
   ```bash
   ollama run llama3.2 "Hello, how are you?"
   ```

## 🎨 Customization

### Adding New Agent Types

To add a new agent (e.g., Technical Analysis):

1. Add agent definition in `initialize_agents()` method
2. Update the agent list in `RoundRobinGroupChat`
3. Add display formatting in message handlers

### Modifying Debate Structure

- Change `max_turns=9` to adjust debate length
- Modify consensus detection logic in `analyze_consensus()` and `consensus_mechanism.py`
- Customize message formatting and display
- Adjust consensus protocol rules in `consensus_mechanism.py`

### Integration with Real Data

The system is designed to work with real financial data. You can:

- Connect to financial APIs (Alpha Vantage, Yahoo Finance)
- Add real-time stock data fetching
- Integrate with portfolio management systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational and demonstration purposes. Please ensure compliance with any applicable financial regulations when using for actual investment decisions.

## 🙏 Acknowledgments

- Built with [AutoGen](https://github.com/microsoft/autogen) framework
- Uses [Ollama](https://ollama.ai/) for local AI inference
- Inspired by collaborative AI research and multi-agent systems

---

**⚠️ Disclaimer**: This tool is for educational purposes only. Do not use for actual investment decisions without proper financial analysis and professional advice.