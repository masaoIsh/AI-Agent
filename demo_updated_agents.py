"""
Demo showing the updated agent names and 2-round consensus system
"""

import asyncio
import random
import time


class UpdatedAgentDemo:
    """Demo of the updated agent system"""
    
    def __init__(self):
        self.agents = {
            'fundamental': {'name': 'Wassim', 'specialty': 'Fundamental', 'icon': '🧮'},
            'sentiment': {'name': 'Khizar', 'specialty': 'Sentiment', 'icon': '📊'},
            'valuation': {'name': 'Yugo', 'specialty': 'Valuation', 'icon': '📈'}
        }
    
    def generate_analysis(self, agent_type, stock_symbol, round_num):
        """Generate analysis for each agent"""
        agent = self.agents[agent_type]
        recommendation = random.choice(["BUY", "SELL"])
        
        if round_num == 1:
            # First round - initial analysis
            if agent_type == 'fundamental':
                analysis = f"""**Initial Analysis for {stock_symbol}:**

Based on my fundamental analysis, I recommend **{recommendation}**.

**Key Factors:**
• Revenue growth: {random.randint(5, 25)}% YoY
• P/E ratio: {random.randint(15, 35)}x vs industry {random.randint(18, 30)}x
• Debt-to-equity: {random.uniform(0.2, 1.0):.1f}x
• Operating margin: {random.randint(8, 25)}%

The company shows {'strong' if recommendation == 'BUY' else 'concerning'} fundamentals that support my {recommendation} recommendation."""
            
            elif agent_type == 'sentiment':
                analysis = f"""**Initial Analysis for {stock_symbol}:**

From a sentiment perspective, I recommend **{recommendation}**.

**Sentiment Indicators:**
• News sentiment: {random.randint(40, 80)}% {'positive' if recommendation == 'BUY' else 'negative'}
• Analyst consensus: {random.choice(['Upgrades', 'Downgrades'])} from {random.randint(2, 5)} firms
• Social media buzz: {random.choice(['High', 'Medium', 'Low'])} and {'positive' if recommendation == 'BUY' else 'negative'}
• Institutional activity: {'Net buying' if recommendation == 'BUY' else 'Net selling'} pressure

Market sentiment {'supports' if recommendation == 'BUY' else 'weighs against'} a {recommendation} position."""
            
            else:  # valuation
                analysis = f"""**Initial Analysis for {stock_symbol}:**

My valuation analysis suggests **{recommendation}**.

**Valuation Metrics:**
• DCF intrinsic value: ${random.randint(100, 300)} per share
• Trading at {random.randint(5, 30)}% {'discount' if recommendation == 'BUY' else 'premium'} to intrinsic value
• P/E ratio: {random.randint(15, 40)}x vs peers {random.randint(18, 30)}x
• PEG ratio: {random.uniform(0.8, 2.5):.2f}

{'Current price presents value opportunity' if recommendation == 'BUY' else 'Valuation appears stretched'} supporting my {recommendation} recommendation."""
        
        elif round_num == 2:
            # Second round - consensus building
            if agent_type == 'fundamental':
                analysis = f"""**Consensus Building - Round 2:**

I appreciate the insights from Khizar and Yugo. After considering their perspectives on sentiment and valuation, I {'maintain' if random.random() > 0.3 else 'am reconsidering'} my **{recommendation}** recommendation.

While sentiment and valuation are important, the fundamental health of the business remains my primary focus. The {'strong' if recommendation == 'BUY' else 'concerning'} financial metrics I identified {'continue to support' if recommendation == 'BUY' else 'still raise concerns about'} this investment."""
            
            elif agent_type == 'sentiment':
                analysis = f"""**Consensus Building - Round 2:**

Thank you Wassim and Yugo for your detailed analysis. The combination of fundamental and valuation perspectives {'aligns with' if random.random() > 0.3 else 'contrasts with'} my sentiment-based **{recommendation}** recommendation.

Market psychology often {'reinforces' if recommendation == 'BUY' else 'contradicts'} fundamental trends, and the current sentiment landscape {'supports continued momentum' if recommendation == 'BUY' else 'suggests caution'} for this stock."""
            
            else:  # valuation
                analysis = f"""**Consensus Building - Round 2:**

After reviewing Wassim's fundamental analysis and Khizar's sentiment insights, I {'stand by' if random.random() > 0.3 else 'am adjusting'} my **{recommendation}** recommendation.

The mathematical reality of valuation {'supports' if recommendation == 'BUY' else 'challenges'} the current price level. While {'sentiment and fundamentals align favorably' if recommendation == 'BUY' else 'other factors may be more optimistic'}, my models suggest {'attractive risk-adjusted returns' if recommendation == 'BUY' else 'limited upside potential'}."""
        
        else:
            # Third round - final consensus
            if agent_type == 'fundamental':
                analysis = f"""**Final Consensus - Round 3:**

After three rounds of discussion with Khizar and Yugo, I {'maintain' if random.random() > 0.4 else 'have adjusted'} my position to **{recommendation}**. 

The comprehensive analysis across fundamental, sentiment, and valuation perspectives {'strongly supports' if recommendation == 'BUY' else 'raises significant concerns about'} this investment. My final recommendation is **{recommendation}** based on the complete picture."""
            
            elif agent_type == 'sentiment':
                analysis = f"""**Final Consensus - Round 3:**

Following our three-round discussion, I {'stand by' if random.random() > 0.4 else 'have refined'} my **{recommendation}** recommendation.

The integration of fundamental analysis from Wassim and valuation insights from Yugo {'reinforces' if recommendation == 'BUY' else 'challenges'} my sentiment-based assessment. Market dynamics {'support continued momentum' if recommendation == 'BUY' else 'suggest caution'}, leading to my final **{recommendation}** recommendation."""
            
            else:  # valuation
                analysis = f"""**Final Consensus - Round 3:**

After considering Wassim's fundamental analysis and Khizar's sentiment insights over three rounds, I {'confirm' if random.random() > 0.4 else 'have refined'} my **{recommendation}** recommendation.

The mathematical framework, combined with fundamental drivers and sentiment factors, {'clearly indicates' if recommendation == 'BUY' else 'raises concerns about'} the investment opportunity. My final **{recommendation}** recommendation reflects this comprehensive analysis."""
        
        return analysis
    
    async def run_demo(self, stock_symbol):
        """Run the updated agent demo"""
        
        print(f"\n📊 Analyzing: {stock_symbol}")
        print("=" * 60)
        print("🤖 Updated Agent System:")
        print("• Wassim (Fundamental Agent)")
        print("• Khizar (Sentiment Agent)")
        print("• Yugo (Valuation Agent)")
        print("• Each agent speaks a maximum of 3 times for consensus building")
        print("=" * 60)
        
        # Round 1: Initial analyses
        print("\n🔄 Round 1: Initial Analyses")
        print("-" * 40)
        
        initial_recommendations = {}
        for agent_type, agent in self.agents.items():
            analysis = self.generate_analysis(agent_type, stock_symbol, 1)
            recommendation = "BUY" if "BUY" in analysis else "SELL"
            initial_recommendations[agent_type] = recommendation
            
            print(f"\n{agent['icon']} {agent['name']} ({agent['specialty']} Agent) - Round 1, Turn 1:")
            print(analysis)
            print("-" * 60)
            await asyncio.sleep(0.5)
        
        # Round 2: Consensus building
        print("\n🔄 Round 2: Consensus Building")
        print("-" * 40)
        
        for agent_type, agent in self.agents.items():
            analysis = self.generate_analysis(agent_type, stock_symbol, 2)
            
            print(f"\n{agent['icon']} {agent['name']} ({agent['specialty']} Agent) - Round 2, Turn 2:")
            print(analysis)
            print("-" * 60)
            await asyncio.sleep(0.5)
        
        # Round 3: Final consensus building
        print("\n🔄 Round 3: Final Consensus Building")
        print("-" * 40)
        
        for agent_type, agent in self.agents.items():
            analysis = self.generate_analysis(agent_type, stock_symbol, 3)
            
            print(f"\n{agent['icon']} {agent['name']} ({agent['specialty']} Agent) - Round 3, Turn 3:")
            print(analysis)
            print("-" * 60)
            await asyncio.sleep(0.5)
        
        # Final consensus
        print("\n🎯 Final Consensus")
        print("-" * 40)
        
        recommendations = list(initial_recommendations.values())
        buy_count = recommendations.count("BUY")
        sell_count = recommendations.count("SELL")
        final_rec = "BUY" if buy_count > sell_count else "SELL"
        
        print(f"After 3 rounds of discussion (9 total turns), agents reached consensus:")
        print(f"Final Recommendation: **{final_rec}**")
        print(f"Vote: {buy_count} BUY, {sell_count} SELL")
        print(f"Consensus: {'Yes' if buy_count == sell_count else 'Majority'}")
        
        print(f"\n✅ Updated system features demonstrated:")
        print("• New agent names: Wassim, Khizar, Yugo")
        print("• Clear turn display: Round X, Turn Y")
        print("• 3-round consensus building (max 3 turns per agent)")
        print("• Professional agent interactions")


async def main():
    """Main demo function"""
    
    print("🎪 UPDATED AGENT SYSTEM DEMO")
    print("=" * 50)
    
    demo = UpdatedAgentDemo()
    await demo.run_demo("AAPL")
    
    print(f"\n🚀 To run the actual updated system:")
    print("   python interactive_cli.py")
    print("   (Make sure Ollama is running: brew services start ollama)")


if __name__ == "__main__":
    asyncio.run(main())
