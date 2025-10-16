"""
Demo script for the Financial Analysis Multi-Agent System
Simplified version for testing and demonstration
"""

import asyncio
import random
from autogen_ext.models.ollama import OllamaChatCompletionClient


class SimpleFinancialAgent:
    """Simplified financial agent for demo purposes"""
    
    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
    
    async def analyze_stock(self, stock_symbol: str) -> dict:
        """Analyze a stock and return recommendation"""
        # Randomly choose BUY or SELL
        recommendation = random.choice(["BUY", "SELL"])
        
        # Generate reasoning based on specialty
        reasoning = self._generate_reasoning(recommendation, stock_symbol)
        
        return {
            'agent': self.name,
            'specialty': self.specialty,
            'recommendation': recommendation,
            'reasoning': reasoning
        }
    
    def _generate_reasoning(self, recommendation: str, stock_symbol: str) -> str:
        """Generate reasoning based on agent specialty"""
        if self.specialty == "Fundamental":
            if recommendation == "BUY":
                reasons = [
                    "Strong revenue growth of 15% YoY",
                    "Healthy P/E ratio of 18x vs industry 22x",
                    "Low debt-to-equity ratio of 0.3x",
                    "Consistent cash flow generation"
                ]
            else:
                reasons = [
                    "Declining revenue growth to 5% YoY",
                    "High P/E ratio of 28x vs industry 22x",
                    "Increasing debt-to-equity ratio to 0.8x",
                    "Negative free cash flow trends"
                ]
        elif self.specialty == "Sentiment":
            if recommendation == "BUY":
                reasons = [
                    "Positive news sentiment with 70% bullish coverage",
                    "Analyst upgrades from 3 major firms",
                    "Strong social media sentiment trending positive",
                    "Institutional buying pressure increasing"
                ]
            else:
                reasons = [
                    "Negative news sentiment with 65% bearish coverage",
                    "Recent analyst downgrades and price target cuts",
                    "Deteriorating social media sentiment",
                    "Institutional selling pressure building"
                ]
        else:  # Valuation
            if recommendation == "BUY":
                reasons = [
                    "DCF model shows 25% upside to current price",
                    "Trading at 15% discount to peer multiples",
                    "Conservative scenarios still attractive",
                    "Strong margin of safety at current levels"
                ]
            else:
                reasons = [
                    "DCF model indicates 20% downside risk",
                    "Trading at 20% premium to historical multiples",
                    "Optimistic assumptions required for current price",
                    "Limited upside potential from current levels"
                ]
        
        return " • " + "\n • ".join(random.sample(reasons, 3))


async def run_demo():
    """Run a simple demo of the financial analysis system"""
    
    print("🤖 Financial Analysis Multi-Agent Demo")
    print("=" * 50)
    
    # Create agents
    agents = [
        SimpleFinancialAgent("Dr. Smith", "Fundamental"),
        SimpleFinancialAgent("Dr. Johnson", "Sentiment"),
        SimpleFinancialAgent("Dr. Williams", "Valuation")
    ]
    
    # Demo stocks
    demo_stocks = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN"]
    
    for stock in demo_stocks:
        print(f"\n📊 Analyzing {stock}")
        print("-" * 30)
        
        # Get analyses from all agents
        analyses = []
        for agent in agents:
            analysis = await agent.analyze_stock(stock)
            analyses.append(analysis)
            
            print(f"\n{analysis['agent']} ({analysis['specialty']} Analyst):")
            print(f"Recommendation: {analysis['recommendation']}")
            print(f"Reasoning:\n{analysis['reasoning']}")
        
        # Check for consensus
        recommendations = [a['recommendation'] for a in analyses]
        unique_recommendations = set(recommendations)
        
        print(f"\n📋 Summary for {stock}:")
        if len(unique_recommendations) == 1:
            print(f"✅ CONSENSUS: All agents recommend {unique_recommendations.pop()}")
        else:
            print(f"⚠️  DISAGREEMENT: {len(unique_recommendations)} different recommendations")
            print("Recommendations:", recommendations)
            
            # Simulate a quick debate
            print("\n🗣️  Quick Debate:")
            buy_count = recommendations.count("BUY")
            sell_count = recommendations.count("SELL")
            
            if buy_count > sell_count:
                final_rec = "BUY"
            else:
                final_rec = "SELL"
            
            print(f"Final Recommendation: {final_rec} (Majority: {buy_count} BUY, {sell_count} SELL)")
        
        print("\n" + "=" * 50)
    
    print("\n🎉 Demo completed!")


async def test_ollama_connection():
    """Test if Ollama is working properly"""
    print("🔄 Testing Ollama connection...")
    
    try:
        model_client = OllamaChatCompletionClient(model="llama3.2")
        
        # Test a simple query
        response = await model_client.create([{
            "role": "user", 
            "content": "Say 'Hello, Ollama is working!'"
        }])
        
        print("✅ Ollama connection successful!")
        print(f"Test response: {response.choices[0].message.content}")
        
        await model_client.close()
        return True
        
    except Exception as e:
        print(f"❌ Ollama connection failed: {str(e)}")
        print("Make sure Ollama is running: brew services start ollama")
        print("And the model is available: ollama list")
        return False


if __name__ == "__main__":
    print("Running demo automatically...")
    print("This demo shows the financial analysis system without requiring Ollama.")
    print("-" * 60)
    
    # Run the demo
    asyncio.run(run_demo())
