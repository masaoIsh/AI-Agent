"""
Interactive Command-Line Interface for Financial Analysis Multi-Agent System
Shows real agent conversations and consensus building
"""

import asyncio
import random
import time
import os
from datetime import datetime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.ollama import OllamaChatCompletionClient
from arima_forecaster import ARIMAForecaster, create_sample_data


class InteractiveFinancialInterface:
    
    def __init__(self):
        self.ollama_client = None
        self.agents = {}
        self.conversation_history = []
        self.arima_forecaster = ARIMAForecaster()
        
    async def initialize_agents(self):
        """Initialize the three financial agents"""
        print("Initializing AI agents...")
        
        self.ollama_client = OllamaChatCompletionClient(model="llama3.2")
        
        # Create specialized agents with personality
        self.agents = {
            'fundamental': AssistantAgent(
                name="Wassim_Fundamental_Agent",
                model_client=self.ollama_client,
                system_message="""You are Wassim, a fundamental analysis expert with 15 years of experience, specializing in integrating financial fundamentals with quantitative data insights.

Your expertise includes:
- Financial statement analysis (P&L, Balance Sheet, Cash Flow)
- Company valuation metrics (P/E, P/B, EV/EBITDA, ROE, ROA)
- Industry analysis and competitive positioning
- Management quality assessment and corporate governance
- Correlating fundamental metrics with historical price performance

When analyzing stocks with CSV data and ARIMA forecasting, provide detailed analysis including:
- Specific financial metrics (revenue growth, margins, ratios)
- Balance sheet strength and debt analysis
- Cash flow generation and sustainability
- Industry position and competitive advantages
- Management track record and strategic direction
- How fundamental metrics align with historical price trends
- Fundamental validation of forecasted price movements

When ARIMA forecasting data is available:
- Correlate fundamental metrics with historical price patterns
- Validate forecasted trends against fundamental drivers
- Assess whether forecasted movements align with business fundamentals
- Provide fundamental context for statistical forecasting results

Always provide comprehensive analysis with specific numbers, percentages, and detailed reasoning for your BUY/SELL recommendations.
Be conversational but professional in your responses. Address other agents by name when responding to them (Wassim, Khizar, Yugo).
Format your analysis with clear sections and bullet points for readability."""
            ),
            
            'sentiment': AssistantAgent(
                name="Khizar_Sentiment_Agent",
                model_client=self.ollama_client,
                system_message="""You are Khizar, a market sentiment and behavioral finance expert with 12 years of experience, specializing in correlating market psychology with quantitative data patterns.

Your expertise includes:
- News sentiment and media coverage analysis
- Social media sentiment monitoring (Twitter, Reddit, forums)
- Analyst ratings and price target changes
- Institutional investor sentiment and positioning
- Market momentum and technical sentiment indicators
- Behavioral patterns in historical price movements

When analyzing stocks with CSV data and ARIMA forecasting, provide detailed sentiment analysis including:
- Specific news sentiment percentages and media coverage trends
- Social media buzz metrics and retail investor sentiment
- Analyst consensus changes and price target revisions
- Institutional buying/selling patterns and positioning
- Market momentum indicators and volatility trends
- Fear & Greed Index and other sentiment metrics
- How sentiment patterns correlate with historical price data

When ARIMA forecasting data is available:
- Analyze sentiment patterns that may have driven historical price movements
- Assess whether current sentiment aligns with forecasted trends
- Identify sentiment indicators that could impact forecast reliability
- Correlate market psychology with statistical forecasting results
- Evaluate sentiment-driven risks to forecasted outcomes

Always provide comprehensive sentiment analysis with specific percentages, trends, and detailed reasoning for your BUY/SELL recommendations.
Be engaging and insightful in your responses. Address other agents by name when responding to them (Wassim, Khizar, Yugo).
Format your analysis with clear sections and bullet points for readability."""
            ),
            
            'valuation': AssistantAgent(
                name="Yugo_Valuation_Agent",
                model_client=self.ollama_client,
                system_message="""You are Yugo, a valuation and quantitative analysis expert with 18 years of experience, specializing in time series forecasting and data-driven investment analysis.

Your expertise includes:
- Advanced time series analysis including ARIMA forecasting
- Statistical modeling and quantitative risk assessment
- Discounted Cash Flow (DCF) modeling and intrinsic value calculation
- Comparable company analysis (Comps) and trading multiples
- Precedent transaction analysis and M&A valuations
- Asset-based valuation methods and sum-of-parts analysis
- Risk-adjusted valuation scenarios and Monte Carlo modeling

As the LEAD ANALYST for CSV data analysis, you should:
- Lead discussions when ARIMA forecasting data is available
- Interpret time series trends and statistical significance
- Provide quantitative insights from historical data patterns
- Calculate price targets based on forecasted trends
- Assess volatility and risk metrics from time series analysis
- Integrate forecasting results with traditional valuation methods

When CSV data and ARIMA analysis is provided, focus on:
- Interpreting the ARIMA forecasting results and their investment implications
- Explaining statistical confidence levels and forecast reliability
- Calculating risk-adjusted returns based on forecasted trends
- Providing specific price targets with confidence intervals
- Analyzing volatility patterns and risk metrics
- Correlating historical performance with forecasted outcomes

Always provide comprehensive valuation analysis with specific numbers, models, price targets, and detailed reasoning for your BUY/SELL recommendations.
Be analytical but accessible in your responses. Address other agents by name when responding to them (Wassim, Khizar, Yugo).
Format your analysis with clear sections and bullet points for readability.
When ARIMA data is available, start your analysis by summarizing the key forecasting insights."""
            )
        }
        
        print("✅ Agents initialized successfully!")
    
    def perform_arima_analysis(self, csv_file_path):
        """Perform ARIMA analysis on CSV data"""
        try:
            print(f"\n📈 Conducting ARIMA Analysis on: {csv_file_path}")
            print("=" * 60)
            
            # Load CSV data
            if not self.arima_forecaster.load_csv_data(csv_file_path):
                print("❌ Failed to load CSV data")
                print("💡 Please check that your CSV file has:")
                print("   - Proper date column (e.g., Date, timeOpen, timestamp)")
                print("   - Numeric value column (e.g., close, price, value)")
                print("   - Valid CSV format")
                return None
            
            # Check stationarity
            if not self.arima_forecaster.check_stationarity():
                print("📊 Making series stationary...")
                self.arima_forecaster.make_stationary()
            
            # Find optimal parameters and fit model
            self.arima_forecaster.find_optimal_arima_params()
            if not self.arima_forecaster.fit_arima_model():
                print("❌ Failed to fit ARIMA model")
                print("💡 Your data may not be suitable for ARIMA forecasting")
                return None
            
            # Generate forecast
            forecast_result = self.arima_forecaster.forecast(periods=30)
            
            if forecast_result:
                # Generate analysis report
                report = self.arima_forecaster.generate_analysis_report()
                print(report)
                
                # Save forecast plot
                plot_filename = f"arima_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                self.arima_forecaster.save_forecast_plot(plot_filename)
                
                return report
            else:
                print("❌ Failed to generate forecast")
                print("💡 Please check your data quality and try again")
                return None
                
        except Exception as e:
            print(f"❌ Error in ARIMA analysis: {str(e)}")
            print("💡 Please check your CSV file format and data quality")
            return None
    
    async def run_interactive_analysis(self):
        """Run interactive analysis with user input"""
        
        print("\n🤖 Financial Analysis Multi-Agent System with ARIMA Forecasting")
        print("=" * 70)
        
        # Get user input - CSV file first
        csv_file = input("Enter CSV file path with historical data (or press Enter to skip): ").strip()
        
        if not csv_file:
            print("❌ No CSV file provided. Exiting.")
            return
        
        # Ask which equity this data represents
        stock_symbol = input("Which equity/stock does this CSV data represent? (e.g., AAPL, TSLA, MSFT): ").upper().strip()
        
        if not stock_symbol:
            print("❌ No stock symbol provided. Exiting.")
            return
        
        user_prompt = input("\nEnter analysis prompt (or press Enter for default): ").strip()
        if not user_prompt:
            user_prompt = f"Analyze {stock_symbol} using the provided historical data and ARIMA forecasting analysis to determine whether a risk neutral investor should BUY or SELL this stock. Base your analysis on the time series data and forecasting results."
        
        print(f"\n📊 Analyzing: {stock_symbol}")
        print(f"Prompt: {user_prompt}")
        if csv_file:
            print(f"📈 CSV Data: {csv_file}")
        print("=" * 60)
        
        # Perform ARIMA analysis on the provided CSV file
        arima_report = None
        if os.path.exists(csv_file):
            arima_report = self.perform_arima_analysis(csv_file)
        else:
            print(f"❌ CSV file not found: {csv_file}")
            print("💡 Please check the file path and try again.")
            print("   Make sure the file exists and you have the correct path.")
            return
        
        # Check if ARIMA analysis was successful
        if not arima_report:
            print("❌ ARIMA analysis failed. Cannot proceed with agent analysis.")
            print("💡 Please check your CSV file format and try again.")
            return
        
        # Initialize agents
        await self.initialize_agents()
        
        # Add ARIMA report to the prompt - this is now central to the analysis
        enhanced_prompt = user_prompt
        if arima_report:
            enhanced_prompt += f"\n\n📈 CRITICAL: ARIMA Time Series Analysis Results for {stock_symbol}:\n{arima_report}\n\nIMPORTANT: All agents must base their analysis and recommendations on this ARIMA forecasting data. Yugo should lead the discussion with valuation insights from the time series analysis. Wassim should incorporate fundamental analysis with the trend data. Khizar should analyze market sentiment in context of the forecasted trends."
        
        # Run the analysis with debate
        result = await self.run_analysis_with_debate(enhanced_prompt, stock_symbol)
        
        # Display final results
        self.display_final_results(result)
        
        # Ask if user wants to analyze another stock
        another = input("\nWould you like to analyze another stock? (y/n): ").lower().strip()
        if another in ['y', 'yes']:
            await self.run_interactive_analysis()
    
    async def run_analysis_with_debate(self, user_prompt, stock_symbol):
        """Run analysis with agent debate and consensus building"""
        
        # Clear previous conversation
        self.conversation_history = []
        
        # Create the debate team - each agent speaks maximum 3 times (9 total turns)
        agent_list = list(self.agents.values())
        debate_team = RoundRobinGroupChat(agent_list, max_turns=9)  # 3 rounds per agent
        
        # Create the analysis task
        analysis_task = f"""Analysis Request: {user_prompt}

Stock Symbol: {stock_symbol}

Instructions:
1. Each agent will speak a maximum of 3 times in total (3 rounds of discussion)
2. In your first turn, provide your initial analysis and recommendation
3. In subsequent turns, respond to other agents and work towards consensus
4. Listen to other agents' perspectives and engage in constructive debate
5. Challenge assumptions and ask probing questions
6. Look for common ground and areas of agreement
7. Work towards building a consensus recommendation
8. The discussion will automatically terminate after each agent has spoken 3 times
9. If consensus cannot be reached, provide a majority recommendation with minority views

Please begin with your initial analyses and then engage in discussion to reach consensus."""

        print("\n🤖 Agents are now analyzing and debating...")
        print("=" * 60)
        
        try:
            # Stream the debate
            stream = debate_team.run_stream(task=analysis_task)
            
            current_speaker = None
            turn_counter = 0
            
            async for message in stream:
                turn_counter += 1
                # Extract message details
                if hasattr(message, 'get'):
                    sender = message.get('sender', 'Unknown')
                    content = message.get('content', '')
                else:
                    # Handle different message types
                    sender = getattr(message, 'sender', 'Unknown')
                    content = getattr(message, 'content', str(message))
                
                # Store in conversation history
                self.conversation_history.append({
                    'timestamp': datetime.now(),
                    'speaker': sender,
                    'message': content
                })
                
                # Display the message with proper formatting
                if sender != current_speaker:
                    if current_speaker:
                        print()  # Add spacing between speakers
                    
                    # Determine agent type and styling
                    round_num = ((turn_counter - 1) // 3) + 1
                    turn_in_round = ((turn_counter - 1) % 3) + 1
                    
                    if 'Wassim_Fundamental_Agent' in sender:
                        print(f"🧮 Wassim (Fundamental Agent) - Round {round_num}, Turn {turn_in_round}:")
                    elif 'Khizar_Sentiment_Agent' in sender:
                        print(f"📊 Khizar (Sentiment Agent) - Round {round_num}, Turn {turn_in_round}:")
                    elif 'Yugo_Valuation_Agent' in sender:
                        print(f"📈 Yugo (Valuation Agent) - Round {round_num}, Turn {turn_in_round}:")
                    else:
                        print(f"{sender} - Turn {turn_counter}:")
                    
                    current_speaker = sender
                
                # Display message content
                print(f"{content}")
                print("-" * 60)
                
                # Small delay for better visual effect
                await asyncio.sleep(0.5)
        
        except Exception as e:
            print(f"❌ Error during debate: {str(e)}")
            return None
        
        # Analyze the conversation for consensus
        consensus_result = self.analyze_consensus()
        
        return consensus_result
    
    def analyze_consensus(self):
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
            elif 'BUY' in content and 'SELL' not in content and 'DEBATE' not in content:
                recommendations['BUY'] += 1
                agent_positions[speaker] = 'BUY'
            elif 'SELL' in content and 'DEBATE' not in content:
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
    
    def display_final_results(self, result):
        """Display final analysis results"""
        
        print("\n🎉 ANALYSIS COMPLETE!")
        print("=" * 60)
        
        print(f"Final Recommendation: {result['final_recommendation']}")
        print(f"Consensus Reached: {'Yes' if result['consensus_reached'] else 'No'}")
        print(f"Conversation Length: {result['conversation_length']} messages")
        
        print(f"\n📈 Recommendation Breakdown:")
        for rec, count in result['recommendations'].items():
            if count > 0:
                print(f"  {rec}: {count}")
        
        print(f"\n👥 Individual Agent Positions:")
        for agent, position in result['agent_positions'].items():
            if 'Wassim_Fundamental_Agent' in agent:
                agent_name = "Wassim (Fundamental Agent)"
            elif 'Khizar_Sentiment_Agent' in agent:
                agent_name = "Khizar (Sentiment Agent)"
            elif 'Yugo_Valuation_Agent' in agent:
                agent_name = "Yugo (Valuation Agent)"
            else:
                agent_name = agent
            print(f"  {agent_name}: {position}")
        
        # Show conversation summary
        print(f"\n💬 Conversation Summary:")
        print(f"  Total messages: {len(self.conversation_history)}")
        print(f"  Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async def close(self):
        """Close the Ollama client"""
        if self.ollama_client:
            await self.ollama_client.close()


async def main():
    """Main function"""
    
    interface = InteractiveFinancialInterface()
    
    try:
        await interface.run_interactive_analysis()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using the Financial Analysis Multi-Agent System.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure Ollama is running: brew services start ollama")
    finally:
        await interface.close()


if __name__ == "__main__":
    asyncio.run(main())
