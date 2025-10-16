"""
Demo script showing the user interface capabilities
"""

import asyncio
import time
import random


class MockFinancialAgent:
    """Mock financial agent for demo purposes"""
    
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty
    
    def get_analysis(self, stock_symbol):
        """Get mock analysis"""
        recommendation = random.choice(["BUY", "SELL"])
        
        if self.specialty == "Fundamental":
            reasoning = [
                f"Strong revenue growth of {random.randint(8, 25)}% YoY",
                f"P/E ratio of {random.randint(15, 35)}x vs industry {random.randint(18, 28)}x",
                f"Debt-to-equity ratio of {random.uniform(0.1, 1.0):.1f}x"
            ]
        elif self.specialty == "Sentiment":
            reasoning = [
                f"News sentiment: {random.randint(40, 80)}% positive",
                f"Analyst upgrades: {random.randint(0, 5)} recent",
                f"Social media buzz: {random.choice(['High', 'Medium', 'Low'])}"
            ]
        else:  # Valuation
            reasoning = [
                f"DCF shows {random.randint(10, 40)}% upside/downside",
                f"Trading at {random.randint(5, 25)}% premium/discount to peers",
                f"Intrinsic value: ${random.randint(100, 300)}"
            ]
        
        return {
            'recommendation': recommendation,
            'reasoning': reasoning,
            'confidence': random.randint(60, 95)
        }


def demo_streamlit_interface():
    """Demo the Streamlit interface concept"""
    
    print("🌐 STREAMLIT WEB INTERFACE DEMO")
    print("=" * 50)
    print()
    print("📱 What the user would see:")
    print()
    print("┌─────────────────────────────────────────────────────────┐")
    print("│  🤖 Financial Analysis Multi-Agent System              │")
    print("│  Three AI experts debate and reach consensus            │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│                                                         │")
    print("│  Stock Symbol: [AAPL     ]                              │")
    print("│                                                         │")
    print("│  Analysis Prompt:                                       │")
    print("│  ┌─────────────────────────────────────────────────┐   │")
    print("│  │ Provide analysis and recommendation whether a   │   │")
    print("│  │ risk neutral investor should BUY or SELL...     │   │")
    print("│  └─────────────────────────────────────────────────┘   │")
    print("│                                                         │")
    print("│  [🚀 Start Analysis]                                   │")
    print("│                                                         │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│  🤖 Agents are now analyzing and debating...           │")
    print("│                                                         │")
    print("│  🧮 Dr. Sarah Chen (Fundamental Analyst):              │")
    print("│  Initial Recommendation: BUY                           │")
    print("│  Analysis:                                             │")
    print("│  • Strong revenue growth of 18% YoY demonstrates...    │")
    print("│  • Healthy P/E ratio of 22x vs industry average...     │")
    print("│  • Low debt-to-equity ratio of 0.3x shows...           │")
    print("│  -----------------------------------------------------  │")
    print("│                                                         │")
    print("│  📊 Dr. Marcus Rodriguez (Sentiment Analyst):          │")
    print("│  Initial Recommendation: SELL                          │")
    print("│  Analysis:                                             │")
    print("│  • Negative news sentiment with 70% bearish coverage   │")
    print("│  • Recent analyst downgrades and 12% price target...   │")
    print("│  • Institutional selling pressure building...          │")
    print("│  -----------------------------------------------------  │")
    print("│                                                         │")
    print("│  🗣️ Agent Debate:                                      │")
    print("│  Dr. Sarah Chen: I maintain my position based on...    │")
    print("│  Dr. Marcus Rodriguez: Market sentiment is powerful... │")
    print("│  Dr. Priya Patel: From a valuation standpoint...       │")
    print("│                                                         │")
    print("│  🎉 Analysis Complete!                                 │")
    print("│  Final Recommendation: BUY (Majority: 2 BUY, 1 SELL)   │")
    print("└─────────────────────────────────────────────────────────┘")
    print()


def demo_cli_interface():
    """Demo the CLI interface"""
    
    print("💻 COMMAND-LINE INTERFACE DEMO")
    print("=" * 50)
    print()
    print("$ python interactive_cli.py")
    print()
    print("🤖 Financial Analysis Multi-Agent System")
    print("=" * 60)
    print()
    print("Enter stock symbol (e.g., AAPL, TSLA, MSFT): AAPL")
    print()
    print("Enter analysis prompt (or press Enter for default): ")
    print()
    print("📊 Analyzing: AAPL")
    print("Prompt: Provide analysis and recommendation whether a risk neutral investor should BUY or SELL this stock.")
    print("=" * 60)
    print()
    print("🔄 Initializing AI agents...")
    print("✅ Agents initialized successfully!")
    print()
    print("🤖 Agents are now analyzing and debating...")
    print("=" * 60)
    print()
    print("🧮 Dr. Sarah Chen (Fundamental Analyst):")
    print("Based on my fundamental analysis of AAPL, I recommend BUY...")
    print("-" * 60)
    print()
    print("📊 Dr. Marcus Rodriguez (Sentiment Analyst):")
    print("From a sentiment perspective, I see some concerns...")
    print("-" * 60)
    print()
    print("📈 Dr. Priya Patel (Valuation Analyst):")
    print("My DCF model suggests the stock is undervalued...")
    print("-" * 60)
    print()
    print("🧮 Dr. Sarah Chen:")
    print("I understand your concerns, Marcus, but the fundamentals...")
    print("-" * 60)
    print()
    print("🎉 ANALYSIS COMPLETE!")
    print("=" * 60)
    print("📊 Final Recommendation: BUY")
    print("✅ Consensus Reached: Yes")
    print("💬 Conversation Length: 8 messages")
    print()
    print("📈 Recommendation Breakdown:")
    print("  BUY: 2")
    print("  SELL: 1")
    print()
    print("👥 Individual Agent Positions:")
    print("  Dr. Sarah Chen: BUY")
    print("  Dr. Marcus Rodriguez: SELL")
    print("  Dr. Priya Patel: BUY")
    print()


def demo_agent_conversations():
    """Demo the agent conversation flow"""
    
    print("🗣️ AGENT CONVERSATION DEMO")
    print("=" * 50)
    print()
    
    agents = [
        MockFinancialAgent("Dr. Sarah Chen", "Fundamental"),
        MockFinancialAgent("Dr. Marcus Rodriguez", "Sentiment"),
        MockFinancialAgent("Dr. Priya Patel", "Valuation")
    ]
    
    stock = "AAPL"
    
    print(f"📊 Analyzing {stock}...")
    print()
    
    # Initial analyses
    print("🔄 Step 1: Initial Analysis")
    print("-" * 30)
    
    initial_recommendations = []
    for agent in agents:
        analysis = agent.get_analysis(stock)
        initial_recommendations.append(analysis['recommendation'])
        
        specialty_icon = {"Fundamental": "🧮", "Sentiment": "📊", "Valuation": "📈"}
        print(f"{specialty_icon[agent.specialty]} {agent.name} ({agent.specialty} Analyst):")
        print(f"Recommendation: {analysis['recommendation']}")
        print(f"Confidence: {analysis['confidence']}%")
        print(f"Reasoning: {', '.join(analysis['reasoning'][:2])}")
        print()
    
    # Check consensus
    unique_recs = set(initial_recommendations)
    if len(unique_recs) == 1:
        print("✅ CONSENSUS REACHED! All agents agree.")
        return
    
    print("⚠️ DISAGREEMENT DETECTED - Starting debate...")
    print()
    
    # Simulate debate
    print("🗣️ Step 2: Agent Debate")
    print("-" * 30)
    
    debate_responses = [
        "I maintain my position based on solid financial metrics.",
        "Market sentiment is a powerful driver of price movements.",
        "From a pure valuation standpoint, the math doesn't support current price.",
        "I respect your analysis, but sentiment can override fundamentals.",
        "My models suggest we need more realistic assumptions.",
        "After considering your arguments, I'm reconsidering my position."
    ]
    
    for round_num in range(2):
        print(f"Round {round_num + 1}:")
        for agent in agents:
            response = random.choice(debate_responses)
            specialty_icon = {"Fundamental": "🧮", "Sentiment": "📊", "Valuation": "📈"}
            print(f"{specialty_icon[agent.specialty]} {agent.name}: {response}")
        print()
    
    # Final recommendation
    print("🎯 Step 3: Final Consensus")
    print("-" * 30)
    
    buy_count = initial_recommendations.count("BUY")
    sell_count = initial_recommendations.count("SELL")
    final_rec = "BUY" if buy_count > sell_count else "SELL"
    
    print(f"Final Recommendation: {final_rec}")
    print(f"Vote: {buy_count} BUY, {sell_count} SELL")
    print(f"Consensus: {'Yes' if buy_count != sell_count else 'No'}")


def main():
    """Run all demos"""
    
    print("🎪 FINANCIAL ANALYSIS MULTI-AGENT INTERFACE DEMOS")
    print("=" * 60)
    print()
    
    # Demo 1: Streamlit Interface
    demo_streamlit_interface()
    
    print("\n" + "=" * 60 + "\n")
    
    # Demo 2: CLI Interface
    demo_cli_interface()
    
    print("\n" + "=" * 60 + "\n")
    
    # Demo 3: Agent Conversations
    demo_agent_conversations()
    
    print("\n" + "=" * 60)
    print("🎉 DEMO COMPLETE!")
    print()
    print("🚀 To run the actual interfaces:")
    print("   Web Interface: streamlit run simple_streamlit_app.py")
    print("   CLI Interface: python interactive_cli.py")
    print("   Full System:   python final_demo.py")
    print()


if __name__ == "__main__":
    main()


