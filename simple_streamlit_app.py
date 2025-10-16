"""
Simple Streamlit Interface for Financial Analysis Multi-Agent System
Shows agent conversations and consensus building
"""

import streamlit as st
import asyncio
import time
import random
from datetime import datetime


class SimpleFinancialAgent:
    """Simplified financial agent for demo purposes"""
    
    def __init__(self, name, specialty, expertise):
        self.name = name
        self.specialty = specialty
        self.expertise = expertise
        self.recommendation = None
        self.reasoning = ""
    
    def analyze_stock(self, stock_symbol, user_prompt):
        """Analyze a stock and provide recommendation"""
        # Randomly choose BUY or SELL for demo
        self.recommendation = random.choice(["BUY", "SELL"])
        
        # Generate detailed reasoning based on specialty
        if self.specialty == "Fundamental":
            self.reasoning = self._generate_fundamental_reasoning(stock_symbol, self.recommendation)
        elif self.specialty == "Sentiment":
            self.reasoning = self._generate_sentiment_reasoning(stock_symbol, self.recommendation)
        else:  # Valuation
            self.reasoning = self._generate_valuation_reasoning(stock_symbol, self.recommendation)
    
    def _generate_fundamental_reasoning(self, stock_symbol, recommendation):
        """Generate detailed fundamental analysis reasoning"""
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
        
        return analysis
    
    def _generate_sentiment_reasoning(self, stock_symbol, recommendation):
        """Generate detailed sentiment analysis reasoning"""
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
        
        return analysis
    
    def _generate_valuation_reasoning(self, stock_symbol, recommendation):
        """Generate detailed valuation analysis reasoning"""
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
        
        return analysis


class SimpleFinancialInterface:
    """Simple interface for financial analysis agents"""
    
    def __init__(self):
        self.agents = {
            'fundamental': SimpleFinancialAgent(
                "Dr. Sarah Chen", 
                "Fundamental", 
                "Financial statements, ratios, and business fundamentals"
            ),
            'sentiment': SimpleFinancialAgent(
                "Dr. Marcus Rodriguez", 
                "Sentiment", 
                "Market psychology, news sentiment, and investor behavior"
            ),
            'valuation': SimpleFinancialAgent(
                "Dr. Priya Patel", 
                "Valuation", 
                "DCF models, comparable analysis, and intrinsic value"
            )
        }
        self.conversation_history = []
    
    def run_analysis_with_debate(self, user_prompt, stock_symbol):
        """Run analysis with agent debate simulation"""
        
        # Clear previous conversation
        self.conversation_history = []
        
        # Step 1: Initial analyses
        st.write("🔄 **Step 1: Initial Analysis**")
        
        initial_analyses = {}
        for agent_type, agent in self.agents.items():
            agent.analyze_stock(stock_symbol, user_prompt)
            initial_analyses[agent_type] = agent.recommendation
            
            # Display initial analysis
            if 'Fundamental' in agent.specialty:
                st.markdown(f"**🧮 {agent.name} ({agent.specialty} Analyst):**")
            elif 'Sentiment' in agent.specialty:
                st.markdown(f"**📊 {agent.name} ({agent.specialty} Analyst):**")
            else:
                st.markdown(f"**📈 {agent.name} ({agent.specialty} Analyst):**")
            
            st.write(f"Initial Recommendation: **{agent.recommendation}**")
            st.write(f"Analysis:\n{agent.reasoning}")
            st.write("---")
            
            # Add to conversation history
            self.conversation_history.append({
                'speaker': agent.name,
                'type': 'initial',
                'recommendation': agent.recommendation,
                'reasoning': agent.reasoning
            })
        
        # Step 2: Check for consensus
        recommendations = list(initial_analyses.values())
        unique_recommendations = set(recommendations)
        
        if len(unique_recommendations) == 1:
            st.write("✅ **Consensus Reached!** All agents agree on the recommendation.")
            return {
                'consensus_reached': True,
                'final_recommendation': recommendations[0],
                'debate_conducted': False,
                'conversation_history': self.conversation_history
            }
        
        # Step 3: Debate simulation
        st.write("🗣️ **Step 2: Agent Debate**")
        st.write("Agents disagree - starting debate process...")
        
        # Simulate debate rounds
        debate_rounds = random.randint(2, 4)
        
        for round_num in range(debate_rounds):
            st.write(f"\n**Round {round_num + 1}:**")
            
            # Each agent gets to respond
            for agent_type, agent in self.agents.items():
                # Simulate agent response to debate
                response = self._simulate_debate_response(agent, round_num, recommendations)
                
                if 'Fundamental' in agent.specialty:
                    st.markdown(f"**🧮 {agent.name}:**")
                elif 'Sentiment' in agent.specialty:
                    st.markdown(f"**📊 {agent.name}:**")
                else:
                    st.markdown(f"**📈 {agent.name}:**")
                
                st.write(response)
                st.write("---")
                
                # Add to conversation history
                self.conversation_history.append({
                    'speaker': agent.name,
                    'type': 'debate',
                    'round': round_num + 1,
                    'response': response
                })
            
            # Small delay for visual effect
            time.sleep(0.5)
        
        # Step 4: Final consensus
        st.write("🎯 **Step 3: Final Consensus**")
        
        # Simulate some agents changing their minds during debate
        final_recommendations = []
        for agent_type, agent in self.agents.items():
            # 20% chance of changing recommendation after debate
            if random.random() < 0.2:
                agent.recommendation = "SELL" if agent.recommendation == "BUY" else "BUY"
            final_recommendations.append(agent.recommendation)
        
        # Determine final recommendation
        buy_count = final_recommendations.count("BUY")
        sell_count = final_recommendations.count("SELL")
        final_rec = "BUY" if buy_count > sell_count else "SELL"
        
        st.write(f"After debate, agents have reached a **{final_rec}** recommendation")
        st.write(f"Final vote: {buy_count} BUY, {sell_count} SELL")
        
        return {
            'consensus_reached': buy_count == sell_count,
            'final_recommendation': final_rec,
            'debate_conducted': True,
            'final_votes': {'BUY': buy_count, 'SELL': sell_count},
            'conversation_history': self.conversation_history
        }
    
    def _simulate_debate_response(self, agent, round_num, all_recommendations):
        """Simulate agent response during debate"""
        
        responses = {
            'Fundamental': [
                """I appreciate your perspectives, but I must emphasize that fundamental analysis provides the bedrock for any investment decision. While sentiment and valuation are important, the underlying financial health of the company cannot be ignored. My analysis shows strong revenue growth, healthy margins, and a robust balance sheet that supports long-term value creation.""",
                
                """I understand the concerns about market sentiment and valuation, but let me address this from a fundamental perspective. The company's competitive position, management quality, and financial metrics suggest this is a fundamentally sound business. While short-term volatility may occur, the underlying business fundamentals support a positive long-term outlook.""",
                
                """After reviewing the financial statements and industry dynamics, I remain confident in my recommendation. The company's ability to generate consistent cash flows, maintain pricing power, and reinvest in growth initiatives creates a compelling fundamental case that outweighs near-term sentiment concerns.""",
                
                """I acknowledge the valuation concerns raised, but fundamental analysis suggests the company is well-positioned for sustained growth. The combination of strong market position, improving operational efficiency, and strategic initiatives provides a solid foundation for long-term shareholder value creation."""
            ],
            'Sentiment': [
                """I respect the fundamental analysis, but market sentiment is often a leading indicator that shouldn't be dismissed. The current sentiment landscape shows clear directional bias that can drive significant price movements. While fundamentals matter, investor psychology and market dynamics often determine short to medium-term returns.""",
                
                """From a behavioral finance perspective, the current sentiment indicators suggest investors are pricing in both opportunities and risks. The news flow, analyst revisions, and institutional positioning all point to a specific market narrative that we need to consider alongside traditional fundamental metrics.""",
                
                """Market sentiment reflects the collective wisdom and fears of market participants. While it may seem irrational at times, sentiment often anticipates fundamental changes before they're reflected in financial statements. The current sentiment landscape provides important context for investment timing and risk assessment.""",
                
                """I understand the focus on fundamentals, but sentiment analysis reveals important market dynamics that can significantly impact returns. The combination of news flow, social media buzz, and institutional activity creates momentum that can either amplify or dampen fundamental value realization."""
            ],
            'Valuation': [
                """From a quantitative valuation perspective, my models suggest the current price doesn't adequately reflect intrinsic value. While I appreciate the fundamental and sentiment arguments, valuation analysis provides an objective framework for assessing risk-adjusted returns. The math simply doesn't support the current valuation levels.""",
                
                """I acknowledge the positive fundamental and sentiment factors, but valuation discipline is crucial for risk management. My DCF models, comparable analysis, and scenario testing all suggest that current prices require optimistic assumptions that may not materialize. We need to maintain valuation discipline regardless of short-term factors.""",
                
                """While sentiment and fundamentals provide important context, valuation analysis offers a quantitative framework for assessing investment opportunity. The current valuation multiples and intrinsic value calculations suggest limited upside potential relative to the risks involved. We must consider the risk-reward profile objectively.""",
                
                """My valuation models incorporate both fundamental drivers and sentiment factors, but the mathematical reality is that current prices don't provide adequate margin of safety. Even under optimistic scenarios, the risk-adjusted returns are not compelling enough to justify the current valuation levels."""
            ]
        }
        
        # Sometimes agents change their mind
        if round_num > 0 and random.random() < 0.3:  # 30% chance in later rounds
            return f"After considering the arguments, I'm reconsidering my position. {random.choice(responses[agent.specialty])}"
        
        return random.choice(responses[agent.specialty])


def main():
    """Main Streamlit application"""
    
    st.set_page_config(
        page_title="Financial Analysis Multi-Agent System",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Financial Analysis Multi-Agent System")
    st.markdown("**Three AI experts debate and reach consensus on investment recommendations**")
    
    # Sidebar for input
    with st.sidebar:
        st.header("📊 Analysis Parameters")
        
        # Stock symbol input
        stock_symbol = st.text_input(
            "Stock Symbol", 
            value="AAPL",
            help="Enter the stock symbol to analyze (e.g., AAPL, TSLA, MSFT)"
        ).upper()
        
        # Analysis prompt
        default_prompt = "Provide analysis and recommendation whether a risk neutral investor should BUY or SELL this stock."
        user_prompt = st.text_area(
            "Analysis Prompt",
            value=default_prompt,
            height=100,
            help="Customize the analysis request"
        )
        
        # Analysis button
        analyze_button = st.button("🚀 Start Analysis", type="primary")
        
        st.markdown("---")
        st.markdown("### 👥 Meet the Experts")
        st.markdown("""
        **🧮 Dr. Sarah Chen** - Fundamental Analyst
        - 15 years experience
        - Financial statements & valuations
        
        **📊 Dr. Marcus Rodriguez** - Sentiment Analyst  
        - 12 years experience
        - Market psychology & news
        
        **📈 Dr. Priya Patel** - Valuation Analyst
        - 18 years experience
        - DCF models & quantitative analysis
        """)
    
    # Main content area
    if analyze_button:
        if not stock_symbol:
            st.error("Please enter a stock symbol")
            return
        
        # Initialize the interface
        if 'financial_interface' not in st.session_state:
            st.session_state.financial_interface = SimpleFinancialInterface()
        
        interface = st.session_state.financial_interface
        
        # Display the analysis
        st.write(f"## 📈 Analyzing: {stock_symbol}")
        st.write(f"**Prompt:** {user_prompt}")
        st.write("---")
        
        # Run the analysis
        result = interface.run_analysis_with_debate(user_prompt, stock_symbol)
        
        # Display results
        st.success("🎉 Analysis Complete!")
        
        # Results summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Final Recommendation", 
                result['final_recommendation'],
                delta="Consensus" if result['consensus_reached'] else "Majority"
            )
        
        with col2:
            st.metric(
                "Consensus Reached",
                "✅ Yes" if result['consensus_reached'] else "❌ No"
            )
        
        with col3:
            st.metric(
                "Debate Conducted",
                "✅ Yes" if result['debate_conducted'] else "❌ No"
            )
        
        # Show final votes if debate was conducted
        if result['debate_conducted']:
            st.subheader("📊 Final Vote Breakdown")
            vote_cols = st.columns(2)
            with vote_cols[0]:
                st.metric("BUY", result['final_votes']['BUY'])
            with vote_cols[1]:
                st.metric("SELL", result['final_votes']['SELL'])
        
        # Show conversation summary
        st.subheader("💬 Conversation Summary")
        st.write(f"Total messages: {len(result['conversation_history'])}")
        
        # Expandable conversation history
        with st.expander("View Full Conversation History"):
            for i, entry in enumerate(result['conversation_history']):
                if entry['type'] == 'initial':
                    st.write(f"**{entry['speaker']}** (Initial Analysis): {entry['recommendation']}")
                else:
                    st.write(f"**{entry['speaker']}** (Round {entry['round']}): {entry['response']}")
    
    # Instructions
    else:
        st.markdown("""
        ## 🎯 How to Use This System
        
        1. **Enter a stock symbol** in the sidebar (e.g., AAPL, TSLA, MSFT)
        2. **Customize the analysis prompt** if desired
        3. **Click "Start Analysis"** to begin the multi-agent debate
        4. **Watch as three AI experts** analyze the stock and debate their positions
        5. **See consensus building** as they discuss and potentially change their minds
        6. **Get the final recommendation** with detailed breakdown
        
        ### 🔍 What You'll See:
        - **Initial analyses** from each expert with detailed reasoning
        - **Real-time debate** between the three AI agents
        - **Consensus building** as agents respond to each other
        - **Final recommendation** with vote breakdown
        
        ### ⚠️ Note:
        This is a demonstration system using simulated AI agents. For real investment decisions, 
        always consult with financial professionals and verify with current market data.
        """)
        
        # Example
        st.markdown("### 💡 Example Output")
        st.code("""
🧮 Dr. Sarah Chen (Fundamental Analyst):
Initial Recommendation: BUY
Analysis:
 • Strong revenue growth of 18% YoY demonstrates market demand
 • Healthy P/E ratio of 22x vs industry average of 24x
 • Low debt-to-equity ratio of 0.3x shows strong balance sheet

📊 Dr. Marcus Rodriguez (Sentiment Analyst):
Initial Recommendation: SELL
Analysis:
 • Negative news sentiment with 70% bearish coverage
 • Recent analyst downgrades and 12% price target cuts
 • Institutional selling pressure building with 18% net outflows

[Agents debate and reach final consensus...]
        """)


if __name__ == "__main__":
    main()
