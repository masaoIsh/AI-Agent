# Getting Started Guide

This guide will help you quickly set up and run the AI Financial Analysis Multi-Agent System.

## 🚀 Quick Setup (5 minutes)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/Ai-Agent.git
cd Ai-Agent
```

### Step 2: Run the Setup Script
```bash
python setup.py
```

This script will:
- ✅ Check your Python version (3.10+ required)
- ✅ Verify Ollama installation
- ✅ Install Python dependencies
- ✅ Download the Llama3.2 AI model
- ✅ Test the installation

### Step 3: Run the System
```bash
python interactive_cli.py
```

## 🎯 First Run Example

When you run `python interactive_cli.py`, you'll see:

```
🤖 Financial Analysis Multi-Agent System
============================================================
Enter stock symbol (e.g., AAPL, TSLA, MSFT): AAPL

Enter analysis prompt (or press Enter for default): 

📊 Analyzing: AAPL
Prompt: Provide analysis and recommendation whether a risk neutral investor should BUY or SELL this stock.
============================================================

Initializing AI agents...
✅ Agents initialized successfully!

🤖 Agents are now analyzing and debating...
============================================================

🧮 Wassim (Fundamental Agent) - Round 1, Turn 1:
[Fundamental analysis appears here...]

📊 Khizar (Sentiment Agent) - Round 1, Turn 1:
[Sentiment analysis appears here...]

📈 Yugo (Valuation Agent) - Round 1, Turn 1:
[Valuation analysis appears here...]

🎉 ANALYSIS COMPLETE!
============================================================
Final Recommendation: BUY
Consensus Reached: Yes
```

## 🔧 Manual Setup (if needed)

If the automated setup doesn't work, follow these steps:

### 1. Install Ollama

**macOS:**
```bash
brew install ollama
brew services start ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

**Windows:**
- Download from [ollama.ai](https://ollama.ai/download)

### 2. Download AI Model
```bash
ollama pull llama3.2
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test Installation
```bash
python test_setup.py
```

## 🆘 Troubleshooting

### "Ollama not found"
- Make sure Ollama is installed and running
- Check: `ollama list` should show available models

### "Model not found"
- Download the model: `ollama pull llama3.2`
- Verify: `ollama list | grep llama3.2`

### "Import errors"
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.10+)

### "Connection refused"
- Start Ollama service: `brew services start ollama` (macOS)
- Or run: `ollama serve` (Linux/Windows)

## 📚 What's Next?

1. **Try different stocks**: Run the system with various stock symbols
2. **Custom prompts**: Provide your own analysis questions
3. **Read the full README**: Check `README.md` for advanced features
4. **Customize agents**: Modify agent personalities in `interactive_cli.py`

## 🎉 You're Ready!

The system is now ready to provide AI-powered financial analysis through multi-agent debates. Enjoy exploring different stocks and investment scenarios!



