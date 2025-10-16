"""
Test script to demonstrate the enhanced detailed analysis
"""

from simple_streamlit_app import SimpleFinancialAgent


def test_enhanced_analysis():
    """Test the enhanced analysis with detailed reasoning"""
    
    print("🧪 TESTING ENHANCED DETAILED ANALYSIS")
    print("=" * 60)
    
    # Create agents
    agents = {
        'fundamental': SimpleFinancialAgent("Dr. Sarah Chen", "Fundamental", "Financial statements and ratios"),
        'sentiment': SimpleFinancialAgent("Dr. Marcus Rodriguez", "Sentiment", "Market psychology and news"),
        'valuation': SimpleFinancialAgent("Dr. Priya Patel", "Valuation", "DCF models and valuations")
    }
    
    stock = "AAPL"
    user_prompt = "Provide analysis and recommendation whether a risk neutral investor should BUY or SELL this stock."
    
    print(f"📊 Testing detailed analysis for {stock}")
    print("=" * 60)
    
    for agent_type, agent in agents.items():
        agent.analyze_stock(stock, user_prompt)
        
        # Display agent analysis
        specialty_icon = {"Fundamental": "🧮", "Sentiment": "📊", "Valuation": "📈"}
        print(f"\n{specialty_icon[agent.specialty]} {agent.name} ({agent.specialty} Analyst):")
        print(f"Recommendation: {agent.recommendation}")
        print("\nDetailed Analysis:")
        print(agent.reasoning)
        print("\n" + "-" * 60)
    
    print("\n🎉 Enhanced analysis test complete!")
    print("The agents now provide:")
    print("• Detailed financial metrics and ratios")
    print("• Specific percentages and numbers")
    print("• Professional formatting with sections")
    print("• Comprehensive reasoning for recommendations")
    print("• Risk-adjusted scenarios and target prices")


if __name__ == "__main__":
    test_enhanced_analysis()
