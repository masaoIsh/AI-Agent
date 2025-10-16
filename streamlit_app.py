"""
Streamlit Web Interface for Financial Analysis Multi-Agent System
Shows real agent conversations and consensus building
"""

import streamlit as st
import asyncio
import time
from datetime import datetime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.ollama import OllamaChatCompletionClient


class FinancialAgentInterface:
    """Streamlit interface for financial analysis agents"""
    
    def __init__(self):
        self.ollama_client = None
        self.agents = {}
        self.conversation_history = []
        
    async def initialize_agents(self):
        """Initialize the three financial agents"""
        if self.ollama_client is None:
            self.ollama_client = OllamaChatCompletionClient(model="llama3.2")
        
        # Create specialized agents
        self.agents = {
            'fundamental': AssistantAgent(
                name="FundamentalAnalyst",
                model_client=self.ollama_client,
                system_message="""You are Dr. Sarah Chen, a fundamental analysis expert with 15 years of experience.
                
Your expertise includes:
- Financial statement analysis (P&L, Balance Sheet, Cash Flow)
- Company valuation metrics (P/E, P/B, EV/EBITDA, ROE, ROA)
- Industry analysis and competitive positioning
- Management quality assessment and corporate governance
- Growth prospects and market opportunities

When analyzing stocks, you focus on:
- Revenue growth trends and profitability
- Balance sheet strength and debt levels
- Cash flow generation and dividend sustainability
- Industry position and competitive advantages
- Management track record and strategic direction

Always provide specific financial metrics and reasoning for your recommendations.
Be conversational but professional in your responses."""
            ),
            
            'sentiment': AssistantAgent(
                name="SentimentAnalyst", 
                model_client=self.ollama_client,
                system_message="""You are Dr. Marcus Rodriguez, a market sentiment and behavioral finance expert with 12 years of experience.
                
Your expertise includes:
- News sentiment and media coverage analysis
- Social media sentiment monitoring (Twitter, Reddit, forums)
- Analyst ratings and price target changes
- Institutional investor sentiment and positioning
- Market momentum and technical sentiment indicators
- Behavioral finance and investor psychology

When analyzing stocks, you focus on:
- Recent news flow and media coverage
- Social media buzz and retail investor sentiment
- Analyst upgrades/downgrades and consensus changes
- Institutional buying/selling patterns
- Market momentum and volatility trends
- Investor fear/greed indicators

Always provide specific sentiment indicators and market psychology insights.
Be engaging and insightful in your responses."""
            ),
            
            'valuation': AssistantAgent(
                name="ValuationAnalyst",
                model_client=self.ollama_client,
                system_message="""You are Dr. Priya Patel, a valuation and quantitative analysis expert with 18 years of experience.
                
Your expertise includes:
- Discounted Cash Flow (DCF) modeling and intrinsic value calculation
- Comparable company analysis (Comps) and trading multiples
- Precedent transaction analysis and M&A valuations
- Asset-based valuation methods and sum-of-parts analysis
- Risk-adjusted valuation scenarios and Monte Carlo modeling
- Options pricing and derivatives valuation

When analyzing stocks, you focus on:
- Intrinsic value vs. current market price
- DCF models with various growth scenarios
- Peer company comparisons and relative valuation
- Risk-adjusted returns and probability distributions
- Market efficiency and pricing anomalies
- Long-term value creation potential

Always provide specific valuation metrics, models, and price targets.
Be analytical but accessible in your responses."""
            )
        }
    
    async def run_analysis_with_debate(self, user_prompt, stock_symbol):
        """Run analysis with agent debate and consensus building"""
        
        # Initialize agents if not done
        if not self.agents:
            await self.initialize_agents()
        
        # Clear previous conversation
        self.conversation_history = []
        
        # Create the debate team
        agent_list = list(self.agents.values())
        debate_team = RoundRobinGroupChat(agent_list, max_turns=9)  # 3 rounds per agent
        
        # Create the analysis task
        analysis_task = f"""Analysis Request: {user_prompt}

Stock Symbol: {stock_symbol}

Instructions:
1. Each of you should provide your initial analysis and recommendation
2. Listen to other agents' perspectives and engage in constructive debate
3. Challenge assumptions and ask probing questions
4. Look for common ground and areas of agreement
5. Work towards building a consensus recommendation
6. If consensus cannot be reached, provide a majority recommendation with minority views

Please begin with your initial analyses and then engage in discussion."""

        # Run the debate
        st.write("🤖 **Agents are now analyzing and debating...**")
        
        # Create placeholders for streaming updates
        debate_container = st.container()
        
        try:
            # Stream the debate
            stream = debate_team.run_stream(task=analysis_task)
            
            current_speaker = None
            current_message = ""
            
            async for message in stream:
                # Extract message details
                sender = message.get('sender', 'Unknown')
                content = message.get('content', '')
                
                # Store in conversation history
                self.conversation_history.append({
                    'timestamp': datetime.now(),
                    'speaker': sender,
                    'message': content
                })
                
                # Display the message
                with debate_container:
                    if sender != current_speaker:
                        if current_speaker:
                            st.write("")  # Add spacing between speakers
                        
                        # Determine agent type and styling
                        if 'FundamentalAnalyst' in sender:
                            st.markdown(f"**🧮 Dr. Sarah Chen (Fundamental Analyst):**")
                        elif 'SentimentAnalyst' in sender:
                            st.markdown(f"**📊 Dr. Marcus Rodriguez (Sentiment Analyst):**")
                        elif 'ValuationAnalyst' in sender:
                            st.markdown(f"**📈 Dr. Priya Patel (Valuation Analyst):**")
                        else:
                            st.markdown(f"**{sender}:**")
                        
                        current_speaker = sender
                    
                    # Display message content
                    st.write(content)
                    st.write("---")
                
                # Small delay for better visual effect
                await asyncio.sleep(0.5)
        
        except Exception as e:
            st.error(f"Error during debate: {str(e)}")
            return None
        
        # Analyze the conversation for consensus
        consensus_result = self._analyze_consensus()
        
        return consensus_result
    
    def _analyze_consensus(self):
        """Analyze conversation history to determine consensus"""
        
        # Extract recommendations from the conversation
        recommendations = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
        agent_positions = {}
        
        for entry in self.conversation_history:
            content = entry['message'].upper()
            speaker = entry['speaker']
            
            # Count explicit recommendations
            if 'RECOMMEND BUY' in content or 'RECOMMENDATION: BUY' in content:
                recommendations['BUY'] += 1
                agent_positions[speaker] = 'BUY'
            elif 'RECOMMEND SELL' in content or 'RECOMMENDATION: SELL' in content:
                recommendations['SELL'] += 1
                agent_positions[speaker] = 'SELL'
            elif 'RECOMMEND HOLD' in content or 'RECOMMENDATION: HOLD' in content:
                recommendations['HOLD'] += 1
                agent_positions[speaker] = 'HOLD'
            elif 'BUY' in content and 'SELL' not in content:
                recommendations['BUY'] += 1
                agent_positions[speaker] = 'BUY'
            elif 'SELL' in content:
                recommendations['SELL'] += 1
                agent_positions[speaker] = 'SELL'
        
        # Determine consensus
        max_rec = max(recommendations, key=recommendations.get)
        total_recs = sum(recommendations.values())
        
        consensus_reached = recommendations[max_rec] > total_recs / 2
        
        return {
            'consensus_reached': consensus_reached,
            'final_recommendation': max_rec,
            'recommendations': recommendations,
            'agent_positions': agent_positions,
            'conversation_length': len(self.conversation_history)
        }
    
    async def close(self):
        """Close the Ollama client"""
        if self.ollama_client:
            await self.ollama_client.close()


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
            st.session_state.financial_interface = FinancialAgentInterface()
        
        interface = st.session_state.financial_interface
        
        # Run the analysis
        with st.spinner("Initializing agents and running analysis..."):
            try:
                # Run the async function
                consensus_result = asyncio.run(
                    interface.run_analysis_with_debate(user_prompt, stock_symbol)
                )
                
                if consensus_result:
                    # Display consensus results
                    st.success("🎉 Analysis Complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Final Recommendation", 
                            consensus_result['final_recommendation'],
                            delta="Consensus" if consensus_result['consensus_reached'] else "Majority"
                        )
                    
                    with col2:
                        st.metric(
                            "Consensus Reached",
                            "✅ Yes" if consensus_result['consensus_reached'] else "❌ No"
                        )
                    
                    with col3:
                        st.metric(
                            "Conversation Length",
                            f"{consensus_result['conversation_length']} messages"
                        )
                    
                    # Show detailed breakdown
                    st.subheader("📊 Recommendation Breakdown")
                    
                    rec_cols = st.columns(3)
                    with rec_cols[0]:
                        st.metric("BUY", consensus_result['recommendations']['BUY'])
                    with rec_cols[1]:
                        st.metric("SELL", consensus_result['recommendations']['SELL'])
                    with rec_cols[2]:
                        st.metric("HOLD", consensus_result['recommendations']['HOLD'])
                    
                    # Show agent positions
                    st.subheader("👥 Individual Agent Positions")
                    for agent, position in consensus_result['agent_positions'].items():
                        agent_name = agent.replace('Analyst', '')
                        st.write(f"**{agent_name}**: {position}")
                
                else:
                    st.error("Failed to complete analysis")
            
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.info("Make sure Ollama is running: `brew services start ollama`")
    
    # Instructions
    else:
        st.markdown("""
        ## 🎯 How to Use This System
        
        1. **Enter a stock symbol** in the sidebar (e.g., AAPL, TSLA, MSFT)
        2. **Customize the analysis prompt** if desired
        3. **Click "Start Analysis"** to begin the multi-agent debate
        4. **Watch as three AI experts** analyze the stock and debate their positions
        5. **See consensus building** in real-time as they discuss
        6. **Get the final recommendation** with detailed breakdown
        
        ### 🔍 What You'll See:
        - **Real-time conversation** between the three AI agents
        - **Specialized perspectives** from each expert
        - **Constructive debate** and consensus building
        - **Final recommendation** with detailed reasoning
        
        ### ⚠️ Note:
        This system uses AI knowledge and reasoning capabilities. For real investment decisions, 
        always consult with financial professionals and verify with current market data.
        """)
        
        # Example analysis
        st.markdown("### 💡 Example Analysis")
        st.code("""
Analysis Request: Provide analysis and recommendation whether a risk neutral investor should BUY or SELL AAPL.

🧮 Dr. Sarah Chen (Fundamental Analyst): 
Based on Apple's strong fundamentals, I recommend BUY...

📊 Dr. Marcus Rodriguez (Sentiment Analyst):
From a sentiment perspective, I see some concerns...

📈 Dr. Priya Patel (Valuation Analyst):
My DCF model suggests the stock is undervalued...

[Agents continue debating and reach consensus...]
        """)


if __name__ == "__main__":
    main()


