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

- **🧮 Wassim (Fundamental Agent)**: Analyzes financial statements, ratios, business fundamentals, and **macro VAR/Granger causality analysis**
- **📈 Yugo (Valuation Agent)**: Performs DCF modeling, quantitative valuation analysis, and **technical indicator-based forecasting**

### Interactive Debate System

- **Round-Robin Debates**: Agents engage in structured 3-round discussions when they disagree
- **Consensus Detection**: System automatically identifies when agents reach agreement
- **Real-time Analysis**: Watch agents debate and build consensus in real-time
- **Comprehensive Reports**: Get detailed breakdowns of individual agent positions

### Local AI Processing

- **No API Keys Required**: Uses Ollama with local models for complete privacy
- **Offline Capable**: Works without internet connection once set up
- **Customizable Models**: Use any Ollama-compatible model

### Advanced Quantitative Analysis

- **Technical Indicator Forecasting**: RandomForest-based model with RSI, Bollinger Bands, MACD, and realized volatility
- **Walk-Forward Validation**: Robust out-of-sample testing with MSE/MAE metrics
- **Macro VAR Analysis**: Granger causality testing of economic indicators on asset returns
- **Dual CSV Input**: Separate macro economic data and price data for comprehensive analysis
- **Visualization**: Generate forecast plots with technical indicators overlaid
- **1-Day & 1-Week Forecasts**: Multi-horizon predictions with performance metrics

## 📖 Usage Examples

### Basic Stock Analysis with Dual CSV Input

```bash
python interactive_cli.py
```

**Example Session**:
```
🤖 Financial Analysis Multi-Agent System with ARIMA Forecasting
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
Apple Inc. demonstrates strong fundamental metrics...

📊 Khizar (Sentiment Agent) - Round 1, Turn 1:
Market sentiment for Apple has been mixed recently...

📈 Yugo (Valuation Agent) - Round 1, Turn 1:
Based on my DCF analysis, Apple appears undervalued...

🎉 ANALYSIS COMPLETE!
============================================================
Final Recommendation: BUY
Consensus Reached: Yes
Conversation Length: 9 messages

📈 Recommendation Breakdown:
  BUY: 2
  SELL: 1

👥 Individual Agent Positions:
  Wassim (Fundamental Agent): BUY
  Khizar (Sentiment Agent): SELL
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
🤖 Financial Analysis Multi-Agent System with ARIMA Forecasting
======================================================================
Enter CSV file path with historical data (or press Enter to skip): stock_data.csv

Which equity/stock does this CSV data represent? (e.g., AAPL, TSLA, MSFT): AAPL

📈 Conducting ARIMA Analysis on: stock_data.csv
======================================================================
✅ Successfully loaded 1000 data points
📅 Date range: 2020-01-01 to 2023-12-31
📊 Value column: Close_Price
📊 Stationarity Test Results:
   ADF Statistic: -2.45
   p-value: 0.12
   Stationary: No
✅ Series made stationary with first difference
✅ Optimal ARIMA parameters: (2, 1, 1)
🔮 Generating 30-period forecast...
✅ Forecast generated for 30 periods

📈 CRITICAL: ARIMA Time Series Analysis Results for AAPL:
[Detailed forecasting report with confidence intervals, trends, and insights]

🤖 Agents are now analyzing and debating...
======================================================================
```

**CSV File Format**:
Your CSV should have columns like:
```csv
Date,Close_Price,Volume
2020-01-01,100.50,1500000
2020-01-02,101.25,1600000
...
```

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
- Modify consensus detection logic in `analyze_consensus()`
- Customize message formatting and display

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