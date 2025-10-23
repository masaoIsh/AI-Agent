# AI Financial Analysis Multi-Agent System

A sophisticated multi-agent system that combines sector-based fundamental analysis, ARIMA regime-switching forecasts, and consensus-driven investing. Two specialized AI agents (Wassim: Fundamental Analyst & Yugo: Valuation Analyst) engage in interactive debates to reach consensus on portfolio construction, using a sophisticated filter to validate investment decisions.

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

All data fetched automatically from:
- **Yahoo Finance**: Stock prices, fundamentals (PBR/ROE/ROA)

**Run it:**
```bash
python interactive_cli.py
# Enter sector tickers: AAPL,MSFT,GOOGL,AMZN,META,NVDA,TSLA,AMD,INTC,CRM
# Start date: 2020-01-01
# Construct portfolio: y

## Acknowledgments

- Built with [AutoGen](https://github.com/microsoft/autogen) framework
- Uses [Ollama](https://ollama.ai/) for local AI inference
- Inspired by collaborative AI research and multi-agent systems
