"""
Simple CLI demo that works without complex streaming issues
"""

import asyncio
import random
from datetime import datetime


class SimpleCLIDemo:
    """Simple CLI demo with enhanced analysis"""
    
    def __init__(self):
        self.agents = {
            'fundamental': {
                'name': 'Dr. Sarah Chen',
                'specialty': 'Fundamental',
                'icon': '🧮'
            },
            'sentiment': {
                'name': 'Dr. Marcus Rodriguez', 
                'specialty': 'Sentiment',
                'icon': '📊'
            },
            'valuation': {
                'name': 'Dr. Priya Patel',
                'specialty': 'Valuation', 
                'icon': '📈'
            }
        }
    
    def generate_detailed_analysis(self, agent_type, stock_symbol):
        """Generate detailed analysis like the enhanced system"""
        
        recommendation = random.choice(["BUY", "SELL"])
        agent = self.agents[agent_type]
        
        if agent_type == 'fundamental':
            if recommendation == "BUY":
                analysis = f"""**Fundamental Analysis Summary for {stock_symbol}:**

**Positive Factors:**
• **Revenue Growth:** Strong {random.randint(8, 25)}% YoY growth demonstrates sustained market demand and execution capability
• **Profitability Metrics:** Healthy P/E ratio of {random.randint(15, 25)}x vs industry average of {random.randint(18, 28)}x, indicating reasonable valuation
• **Balance Sheet Strength:** Low debt-to-equity ratio of {random.uniform(0.1, 0.5):.1f}x shows conservative capital structure
• **Cash Flow Generation:** Consistent operating cash flow with {random.randint(10, 30)}% operating margin
• **Market Position:** Strong competitive moats and market-leading position in key segments

**Financial Health Indicators:**
• Gross margin: {random.randint(45, 75)}%
• Operating margin: {random.randint(8, 25)}%
• ROE: {random.randint(12, 25)}%
• Current ratio: {random.uniform(1.2, 3.5):.1f}x

**Recommendation:** BUY - The combination of strong fundamentals, reasonable valuation, and market position supports a positive outlook for risk-neutral investors."""
            else:
                analysis = f"""**Fundamental Analysis Summary for {stock_symbol}:**

**Concerning Factors:**
• **Revenue Growth:** Declining growth to {random.randint(2, 8)}% YoY raises questions about market saturation
• **Valuation Concerns:** High P/E ratio of {random.randint(25, 45)}x vs industry average of {random.randint(18, 28)}x suggests overvaluation
• **Financial Stress:** Increasing debt-to-equity ratio to {random.uniform(0.6, 1.2):.1f}x shows deteriorating capital structure
• **Profitability Issues:** Negative free cash flow trends and contracting margins
• **Competitive Pressure:** Intense competition eroding market share and pricing power

**Financial Health Indicators:**
• Gross margin: {random.randint(25, 45)}%
• Operating margin: {random.randint(-5, 8)}%
• ROE: {random.randint(2, 12)}%
• Current ratio: {random.uniform(0.8, 1.5):.1f}x

**Recommendation:** SELL - Financial concerns and deteriorating fundamentals outweigh growth prospects for risk-neutral investors."""
        
        elif agent_type == 'sentiment':
            if recommendation == "BUY":
                analysis = f"""**Market Sentiment Analysis for {stock_symbol}:**

**Positive Sentiment Indicators:**
• **News Coverage:** {random.randint(65, 85)}% bullish coverage from financial media with positive earnings expectations
• **Analyst Consensus:** Recent upgrades from {random.randint(2, 5)} major firms with average price target increase of {random.randint(8, 25)}%
• **Social Media Buzz:** Strong positive sentiment trending with {random.randint(70, 90)}% favorable mentions on Twitter/Reddit
• **Institutional Activity:** Net buying pressure with {random.randint(15, 35)}% increase in institutional holdings
• **Market Momentum:** Bullish price action with {random.randint(12, 35)}% gain over past 3 months

**Key Sentiment Metrics:**
• Fear & Greed Index: {random.randint(60, 85)} (Greed territory)
• Put/Call ratio: {random.uniform(0.4, 0.8):.2f} (Bullish)
• Short interest: {random.randint(8, 25)}% (Low short pressure)
• Insider sentiment: {random.choice(['Neutral', 'Positive'])} (Limited selling activity)

**Recommendation:** BUY - Strong positive sentiment across multiple channels suggests continued upward momentum for risk-neutral investors."""
            else:
                analysis = f"""**Market Sentiment Analysis for {stock_symbol}:**

**Negative Sentiment Indicators:**
• **News Coverage:** {random.randint(60, 80)}% bearish coverage with concerns about competitive pressures
• **Analyst Downgrades:** Recent downgrades from {random.randint(2, 4)} firms with {random.randint(5, 15)}% average price target cuts
• **Social Media Sentiment:** Deteriorating sentiment with increased criticism and negative buzz
• **Institutional Activity:** Selling pressure building with {random.randint(10, 25)}% net outflows from institutions
• **Market Momentum:** Bearish price action with {random.randint(8, 25)}% decline over past 3 months

**Key Sentiment Metrics:**
• Fear & Greed Index: {random.randint(15, 40)} (Fear territory)
• Put/Call ratio: {random.uniform(1.2, 2.5):.2f} (Bearish)
• Short interest: {random.randint(25, 45)}% (High short pressure)
• Insider sentiment: Negative (Recent insider selling activity)

**Recommendation:** SELL - Deteriorating sentiment and negative momentum suggest continued downside risk for risk-neutral investors."""
        
        else:  # valuation
            if recommendation == "BUY":
                analysis = f"""**Valuation Analysis for {stock_symbol}:**

**Intrinsic Value Assessment:**
• **DCF Model:** Intrinsic value of ${random.randint(180, 350)} per share, representing {random.randint(15, 35)}% upside to current price
• **Comparable Analysis:** Trading at {random.randint(10, 25)}% discount to peer group median multiples (EV/Revenue, P/E, P/B)
• **Sum-of-Parts:** Asset-based valuation suggests {random.randint(20, 40)}% undervaluation across business segments
• **Risk-Adjusted Returns:** Conservative scenarios still project {random.randint(8, 18)}% annual returns

**Valuation Metrics:**
• Current P/E: {random.randint(15, 25)}x vs peers {random.randint(18, 30)}x
• EV/EBITDA: {random.randint(12, 20)}x vs industry {random.randint(15, 25)}x
• Price-to-Book: {random.randint(2, 5)}x vs sector {random.randint(3, 6)}x
• PEG Ratio: {random.uniform(0.8, 1.5):.2f} (Attractive growth-adjusted valuation)

**Target Price Scenarios:**
• Bull Case: ${random.randint(200, 400)} ({random.randint(25, 50)}% upside)
• Base Case: ${random.randint(160, 300)} ({random.randint(10, 30)}% upside)
• Bear Case: ${random.randint(120, 200)} ({random.randint(-10, 10)}% downside)

**Recommendation:** BUY - Current valuation presents attractive risk-adjusted opportunity for risk-neutral investors with {random.randint(15, 35)}% upside potential."""
            else:
                analysis = f"""**Valuation Analysis for {stock_symbol}:**

**Intrinsic Value Concerns:**
• **DCF Model:** Intrinsic value of ${random.randint(80, 150)} per share, indicating {random.randint(10, 25)}% downside risk
• **Comparable Analysis:** Trading at {random.randint(15, 30)}% premium to peer group median multiples
• **Sum-of-Parts:** Asset-based valuation shows overvaluation across most business segments
• **Risk-Adjusted Returns:** Even optimistic scenarios project limited upside potential

**Valuation Metrics:**
• Current P/E: {random.randint(25, 45)}x vs peers {random.randint(18, 30)}x
• EV/EBITDA: {random.randint(20, 35)}x vs industry {random.randint(15, 25)}x
• Price-to-Book: {random.randint(4, 8)}x vs sector {random.randint(3, 6)}x
• PEG Ratio: {random.uniform(1.8, 3.5):.2f} (Expensive growth-adjusted valuation)

**Target Price Scenarios:**
• Bull Case: ${random.randint(120, 200)} ({random.randint(-5, 15)}% upside)
• Base Case: ${random.randint(100, 160)} ({random.randint(-15, 5)}% downside)
• Bear Case: ${random.randint(70, 120)} ({random.randint(-30, -10)}% downside)

**Recommendation:** SELL - Current valuation levels are stretched and do not provide adequate margin of safety for risk-neutral investors given {random.randint(10, 25)}% downside risk."""
        
        return recommendation, analysis
    
    def simulate_debate_response(self, agent_type, round_num):
        """Simulate detailed debate responses"""
        
        responses = {
            'fundamental': [
                """I appreciate your perspectives, but I must emphasize that fundamental analysis provides the bedrock for any investment decision. While sentiment and valuation are important, the underlying financial health of the company cannot be ignored. My analysis shows strong revenue growth, healthy margins, and a robust balance sheet that supports long-term value creation.""",
                
                """I understand the concerns about market sentiment and valuation, but let me address this from a fundamental perspective. The company's competitive position, management quality, and financial metrics suggest this is a fundamentally sound business. While short-term volatility may occur, the underlying business fundamentals support a positive long-term outlook."""
            ],
            'sentiment': [
                """I respect the fundamental analysis, but market sentiment is often a leading indicator that shouldn't be dismissed. The current sentiment landscape shows clear directional bias that can drive significant price movements. While fundamentals matter, investor psychology and market dynamics often determine short to medium-term returns.""",
                
                """From a behavioral finance perspective, the current sentiment indicators suggest investors are pricing in both opportunities and risks. The news flow, analyst revisions, and institutional positioning all point to a specific market narrative that we need to consider alongside traditional fundamental metrics."""
            ],
            'valuation': [
                """From a quantitative valuation perspective, my models suggest the current price doesn't adequately reflect intrinsic value. While I appreciate the fundamental and sentiment arguments, valuation analysis provides an objective framework for assessing risk-adjusted returns. The math simply doesn't support the current valuation levels.""",
                
                """I acknowledge the positive fundamental and sentiment factors, but valuation discipline is crucial for risk management. My DCF models, comparable analysis, and scenario testing all suggest that current prices require optimistic assumptions that may not materialize."""
            ]
        }
        
        return random.choice(responses[agent_type])
    
    async def run_demo(self, stock_symbol, user_prompt):
        """Run the enhanced CLI demo"""
        
        print(f"\n📊 Analyzing: {stock_symbol}")
        print(f"Prompt: {user_prompt}")
        print("=" * 60)
        
        # Step 1: Initial analyses
        print("\n🔄 Step 1: Initial Analysis")
        print("-" * 30)
        
        initial_analyses = {}
        for agent_type, agent in self.agents.items():
            recommendation, analysis = self.generate_detailed_analysis(agent_type, stock_symbol)
            initial_analyses[agent_type] = recommendation
            
            print(f"\n{agent['icon']} {agent['name']} ({agent['specialty']} Analyst):")
            print(f"Initial Recommendation: {recommendation}")
            print(f"\nAnalysis:")
            print(analysis)
            print("\n" + "-" * 60)
            
            # Small delay for visual effect
            await asyncio.sleep(0.5)
        
        # Step 2: Check for consensus
        recommendations = list(initial_analyses.values())
        unique_recommendations = set(recommendations)
        
        if len(unique_recommendations) == 1:
            print(f"\n✅ CONSENSUS REACHED! All agents recommend {unique_recommendations.pop()}")
            return {
                'consensus_reached': True,
                'final_recommendation': recommendations[0],
                'debate_conducted': False,
                'analyses': initial_analyses
            }
        
        # Step 3: Debate simulation
        print(f"\n⚠️ DISAGREEMENT DETECTED - Starting debate...")
        print("\n🗣️ Step 2: Agent Debate")
        print("-" * 30)
        
        debate_rounds = random.randint(2, 3)
        
        for round_num in range(debate_rounds):
            print(f"\n**Round {round_num + 1}:**")
            
            for agent_type, agent in self.agents.items():
                response = self.simulate_debate_response(agent_type, round_num)
                print(f"\n{agent['icon']} {agent['name']}:")
                print(response)
                print("-" * 60)
                
                await asyncio.sleep(0.5)
        
        # Step 4: Final consensus
        print(f"\n🎯 Step 3: Final Consensus")
        print("-" * 30)
        
        # Simulate some agents changing their minds
        final_recommendations = []
        for agent_type in self.agents.keys():
            current_rec = initial_analyses[agent_type]
            # 20% chance of changing recommendation after debate
            if random.random() < 0.2:
                current_rec = "SELL" if current_rec == "BUY" else "BUY"
            final_recommendations.append(current_rec)
        
        buy_count = final_recommendations.count("BUY")
        sell_count = final_recommendations.count("SELL")
        final_rec = "BUY" if buy_count > sell_count else "SELL"
        
        print(f"After debate, agents have reached a **{final_rec}** recommendation")
        print(f"Final vote: {buy_count} BUY, {sell_count} SELL")
        print(f"Consensus: {'Yes' if buy_count == sell_count else 'No'}")
        
        return {
            'consensus_reached': buy_count == sell_count,
            'final_recommendation': final_rec,
            'debate_conducted': True,
            'final_votes': {'BUY': buy_count, 'SELL': sell_count},
            'analyses': initial_analyses
        }


async def main():
    """Main function"""
    
    print("🤖 Enhanced Financial Analysis Multi-Agent System")
    print("=" * 60)
    
    demo = SimpleCLIDemo()
    
    # Get user input
    stock_symbol = input("Enter stock symbol (e.g., AAPL, TSLA, MSFT): ").upper().strip()
    
    if not stock_symbol:
        print("❌ No stock symbol provided. Exiting.")
        return
    
    user_prompt = input("\nEnter analysis prompt (or press Enter for default): ").strip()
    if not user_prompt:
        user_prompt = "Provide analysis and recommendation whether a risk neutral investor should BUY or SELL this stock."
    
    # Run the demo
    result = await demo.run_demo(stock_symbol, user_prompt)
    
    # Display final results
    print("\n🎉 ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"📊 Final Recommendation: {result['final_recommendation']}")
    print(f"✅ Consensus Reached: {'Yes' if result['consensus_reached'] else 'No'}")
    print(f"🗣️ Debate Conducted: {'Yes' if result['debate_conducted'] else 'No'}")
    
    if result['debate_conducted']:
        print(f"📈 Final Vote: {result['final_votes']['BUY']} BUY, {result['final_votes']['SELL']} SELL")
    
    print(f"\n✅ Enhanced analysis complete! The system now provides:")
    print("  • Detailed financial metrics and ratios")
    print("  • Specific percentages and numbers")
    print("  • Professional formatting with sections")
    print("  • Comprehensive reasoning for recommendations")
    print("  • Risk-adjusted scenarios and target prices")


if __name__ == "__main__":
    asyncio.run(main())





