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
from indicator_forecaster import IndicatorForecaster
from macro_var_analyzer import MacroVARAnalyzer
from consensus_mechanism import (
    process_1_collect, process_2_unanimous_hold, process_3_min_conf,
    process_4_conflict, process_5_vibe, process_6_value, process_7_summary
)


class InteractiveFinancialInterface:
    
    def __init__(self):
        self.ollama_client = None
        self.agents = {}
        self.conversation_history = []
        self.indicator_forecaster = IndicatorForecaster()
        self.macro_analyzer = MacroVARAnalyzer()
        
    async def initialize_agents(self):
        """Initialize the two financial agents (Wassim and Yugo)"""
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
- Macro VAR/Granger causality analysis

When analyzing stocks with indicator-based forecasting and macro data, provide detailed analysis including:
- Specific financial metrics (revenue growth, margins, ratios)
- Balance sheet strength and debt analysis
- Cash flow generation and sustainability
- Industry position and competitive advantages
- Management track record and strategic direction
- How fundamental metrics align with macro economic drivers
- Fundamental validation of forecasted price movements

When indicator forecasting and macro VAR data is available:
- Correlate fundamental metrics with macro economic indicators
- Validate forecasted trends against fundamental drivers
- Assess whether forecasted movements align with business fundamentals
- Provide fundamental context for statistical forecasting results

CRITICAL: At the end of your final analysis, you MUST provide a structured consensus statement in this exact format:
CONSENSUS: direction=X confidence=Y.Z reliability=W.V

Where:
- direction: -1 (SELL), 0 (HOLD), or +1 (BUY)
- confidence: 0.0 to 1.0 (your confidence in this recommendation)
- reliability: 0.0 to 1.0 (your reliability/credibility for this type of analysis)

Always provide comprehensive analysis with specific numbers, percentages, and detailed reasoning for your BUY/SELL recommendations.
Be conversational but professional in your responses. Address other agents by name when responding to them (Wassim, Yugo).
Format your analysis with clear sections and bullet points for readability."""
            ),
            
            'valuation': AssistantAgent(
                name="Yugo_Valuation_Agent",
                model_client=self.ollama_client,
                system_message="""You are Yugo, a valuation and quantitative analysis expert with 18 years of experience, specializing in time series forecasting and data-driven investment analysis.

Your expertise includes:
- Advanced time series analysis including technical indicator-based forecasting
- Statistical modeling and quantitative risk assessment
- Discounted Cash Flow (DCF) modeling and intrinsic value calculation
- Comparable company analysis (Comps) and trading multiples
- Precedent transaction analysis and M&A valuations
- Asset-based valuation methods and sum-of-parts analysis
- Risk-adjusted valuation scenarios and Monte Carlo modeling

As the LEAD ANALYST for CSV data analysis, you should:
- Lead discussions when indicator-based forecasting data is available
- Interpret time series trends and statistical significance
- Provide quantitative insights from historical data patterns
- Calculate price targets based on forecasted trends
- Assess volatility and risk metrics from time series analysis
- Integrate forecasting results with traditional valuation methods

When CSV data and indicator-based analysis is provided, focus on:
- Interpreting the technical indicator forecasting results and their investment implications
- Explaining statistical confidence levels and forecast reliability (MSE/MAE metrics)
- Calculating risk-adjusted returns based on forecasted trends
- Providing specific price targets with confidence intervals
- Analyzing volatility patterns and risk metrics
- Correlating historical performance with forecasted outcomes

CRITICAL: At the end of your final analysis, you MUST provide a structured consensus statement in this exact format:
CONSENSUS: direction=X confidence=Y.Z reliability=W.V

Where:
- direction: -1 (SELL), 0 (HOLD), or +1 (BUY)
- confidence: 0.0 to 1.0 (your confidence in this recommendation)
- reliability: 0.0 to 1.0 (your reliability/credibility for this type of analysis)

Always provide comprehensive valuation analysis with specific numbers, models, price targets, and detailed reasoning for your BUY/SELL recommendations.
Be analytical but accessible in your responses. Address other agents by name when responding to them (Wassim, Yugo).
Format your analysis with clear sections and bullet points for readability.
When indicator-based data is available, start your analysis by summarizing the key forecasting insights."""
            )
        }
        
        print("✅ Agents initialized successfully!")
    
    def perform_indicator_analysis(self, csv_file_path):
        """Perform indicator-based forecasting analysis on CSV data"""
        try:
            print(f"\n📈 Conducting Indicator-Based Forecasting on: {csv_file_path}")
            print("=" * 60)
            
            # Load CSV data
            if not self.indicator_forecaster.load_csv_data(csv_file_path):
                print("❌ Failed to load CSV data")
                print("💡 Please check that your CSV file has:")
                print("   - Proper date column (e.g., Date, timeOpen, timestamp)")
                print("   - Numeric value column (e.g., close, price, value)")
                print("   - Valid CSV format")
                return None
            
            # Build features and run walk-forward validation
            self.indicator_forecaster._build_features()
            wf = self.indicator_forecaster.walk_forward_validate()
            print(f"1D-ahead -> MSE: {wf['mse_1d']:.4f}, MAE: {wf['mae_1d']:.4f}")
            print(f"1W-ahead -> MSE: {wf['mse_1w']:.4f}, MAE: {wf['mae_1w']:.4f}")

            # Forecast next day and week
            self.indicator_forecaster.forecast_ahead(periods_1d=1, periods_1w=7)
            plot_prefix = f"indicator_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.indicator_forecaster.save_plots(filename_prefix=plot_prefix)

            # Build a short textual report for agents
            report = (
                f"Indicator Model Walk-Forward Metrics\n"
                f"1D-ahead: MSE={wf['mse_1d']:.4f}, MAE={wf['mae_1d']:.4f}\n"
                f"1W-ahead: MSE={wf['mse_1w']:.4f}, MAE={wf['mae_1w']:.4f}\n"
                f"Forecast images saved with prefix {plot_prefix}"
            )
            print(report)
            return report
                
        except Exception as e:
            print(f"❌ Error in indicator-based analysis: {str(e)}")
            print("💡 Please check your CSV file format and data quality")
            return None
    
    async def run_interactive_analysis(self):
        """Run interactive analysis with user input"""
        
        print("\n🤖 Financial Analysis Multi-Agent System with Indicator-Based Forecasting + Macro VAR")
        print("=" * 70)
        
        # Get user inputs - macro CSV then price CSV
        macro_csv = input("Enter MACRO CSV path ['CPI','Unemployment','10Y_Treasury','FedFundsRate','IP_Index']: ").strip()
        csv_file = input("Enter PRICE CSV path with historical price data: ").strip()
        
        if not macro_csv or not csv_file:
            print("❌ No CSV file provided. Exiting.")
            return
        
        # Ask which equity this data represents
        stock_symbol = input("Which equity/stock does this CSV data represent? (e.g., AAPL, TSLA, MSFT): ").upper().strip()
        
        if not stock_symbol:
            print("❌ No stock symbol provided. Exiting.")
            return
        
        user_prompt = input("\nEnter analysis prompt (or press Enter for default): ").strip()
        if not user_prompt:
            user_prompt = (
                f"Analyze {stock_symbol} using indicator-based forecasting (walk-forward, 1D/1W) and macro VAR/Granger results to determine "
                f"whether a risk-neutral investor should BUY or SELL. Base on price forecasts and macro causality (p-values, direction, strength)."
            )
        
        print(f"\n📊 Analyzing: {stock_symbol}")
        print(f"Prompt: {user_prompt}")
        if csv_file:
            print(f"📈 CSV Data: {csv_file}")
        print("=" * 60)
        
        # Perform macro analysis
        macro_table_str = None
        if os.path.exists(macro_csv):
            if self.macro_analyzer.load_macro_csv(macro_csv):
                # Build returns from price data after it's loaded later; for now, postpone if price missing
                pass
            else:
                print("❌ Failed to load macro CSV data")
        else:
            print(f"❌ Macro CSV not found: {macro_csv}")
            return

        # Perform indicator-based analysis on the provided price CSV file
        indicator_report = None
        if os.path.exists(csv_file):
            indicator_report = self.perform_indicator_analysis(csv_file)
        else:
            print(f"❌ CSV file not found: {csv_file}")
            print("💡 Please check the file path and try again.")
            print("   Make sure the file exists and you have the correct path.")
            return
        
        # Check if analysis was successful
        if not indicator_report:
            print("❌ Indicator-based analysis failed. Cannot proceed with agent analysis.")
            print("💡 Please check your CSV file format and try again.")
            return
        
        # Build returns from the price series (close) for macro VAR alignment
        # Use the loaded forecaster data
        try:
            price_series = self.indicator_forecaster.data[self.indicator_forecaster.value_column].astype(float)
            returns = price_series.pct_change().dropna()
            table = self.macro_analyzer.analyze(returns)
            macro_table_str = MacroVARAnalyzer.format_table(table)
            print("\n📑 Macro Granger Causality Table:\n" + macro_table_str)
        except Exception as e:
            print(f"⚠️ Could not compute macro VAR/Granger: {e}")
            macro_table_str = None

        # Initialize agents (without Khizar)
        await self.initialize_agents()
        
        # Add indicator report to the prompt - this is central to the analysis
        enhanced_prompt = user_prompt
        if indicator_report:
            enhanced_prompt += (
                f"\n\n📈 CRITICAL: Indicator-Based Time Series Analysis Results for {stock_symbol}:\n{indicator_report}\n\n"
                f"IMPORTANT: Base recommendations on indicator-driven forecasts and macro causality. "
                f"Yugo should lead with quantitative insights and forecasts. "
                f"Wassim should integrate fundamentals and macro causal drivers of returns."
            )

        if macro_table_str:
            enhanced_prompt += (
                f"\n\n🏛️ Macro VAR/Granger Causality (drivers of returns):\n{macro_table_str}\n"
            )
        
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
        
        # Create the debate team - each agent speaks maximum 3 times (6 total turns for 2 agents)
        agent_list = list(self.agents.values())
        debate_team = RoundRobinGroupChat(agent_list, max_turns=6)  # 3 rounds per agent
        
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
9. CRITICAL: In your final turn, you MUST provide a structured consensus statement:
   CONSENSUS: direction=X confidence=Y.Z reliability=W.V
   Where direction is -1 (SELL), 0 (HOLD), or +1 (BUY); confidence and reliability are 0.0 to 1.0

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
        """Analyze conversation history using sophisticated consensus protocol"""
        
        print("\n🧮 Applying Sophisticated Consensus Protocol...")
        print("=" * 60)
        
        # Extract structured consensus data from agent messages
        agent_data = {}
        agent_positions = {}
        
        for entry in self.conversation_history:
            content = entry['message']
            speaker = entry['speaker']
            
            # Look for CONSENSUS statements
            if 'CONSENSUS:' in content:
                try:
                    # Extract consensus data: direction=X confidence=Y.Z reliability=W.V
                    consensus_line = content.split('CONSENSUS:')[1].strip().split('\n')[0]
                    
                    # Parse direction
                    if 'direction=-1' in consensus_line:
                        direction = -1
                    elif 'direction=0' in consensus_line:
                        direction = 0
                    elif 'direction=1' in consensus_line or 'direction=+1' in consensus_line:
                        direction = 1
                    else:
                        continue
                    
                    # Parse confidence
                    confidence_start = consensus_line.find('confidence=') + 11
                    confidence_end = consensus_line.find(' ', confidence_start)
                    if confidence_end == -1:
                        confidence_end = len(consensus_line)
                    confidence = float(consensus_line[confidence_start:confidence_end])
                    
                    # Parse reliability
                    reliability_start = consensus_line.find('reliability=') + 12
                    reliability_end = consensus_line.find(' ', reliability_start)
                    if reliability_end == -1:
                        reliability_end = len(consensus_line)
                    reliability = float(consensus_line[reliability_start:reliability_end])
                    
                    # Store agent data
                    agent_name = 'Wassim' if 'Wassim' in speaker else 'Yugo'
                    agent_data[agent_name] = {
                        'direction': direction,
                        'confidence': confidence,
                        'reliability': reliability
                    }
                    
                    # Map to string for compatibility
                    if direction == 1:
                        agent_positions[speaker] = 'BUY'
                    elif direction == -1:
                        agent_positions[speaker] = 'SELL'
                    else:
                        agent_positions[speaker] = 'HOLD'
                        
                except (ValueError, IndexError) as e:
                    print(f"⚠️ Could not parse consensus from {speaker}: {e}")
                    continue
        
        # If no structured data found, fall back to simple counting
        if not agent_data:
            print("⚠️ No structured consensus data found, falling back to simple counting...")
            return self._fallback_consensus()
        
        # Apply sophisticated consensus protocol
        try:
            process_1_collect(agent_data)
            
            if process_2_unanimous_hold(agent_data):
                decision = "HOLD"
                consensus_reached = True
                print(f"\n🏁 Final Decision: {decision} (Unanimous High-Confidence Neutrality)")
            else:
                if not process_3_min_conf(agent_data):
                    print("\n🔄 Debate continues (Low confidence).")
                    consensus_reached = False
                    decision = "HOLD"
                elif not process_4_conflict(agent_data):
                    print("\n🔄 Debate continues (Strong conflict).")
                    consensus_reached = False
                    decision = "HOLD"
                elif not process_5_vibe(agent_data):
                    print("\n🔄 Debate continues (Weak overall alignment).")
                    consensus_reached = False
                    decision = "HOLD"
                else:
                    decision, total_value, p_val = process_6_value(agent_data)
                    consensus_reached = True
                    process_7_summary(agent_data, decision, total_value, p_val)
            
            # Convert to string format for compatibility
            if decision == "BUY":
                final_recommendation = "BUY"
            elif decision == "SELL":
                final_recommendation = "SELL"
            else:
                final_recommendation = "HOLD"
            
            # Build recommendations dict for compatibility
            recommendations = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
            for agent_name, data in agent_data.items():
                if data['direction'] == 1:
                    recommendations['BUY'] += 1
                elif data['direction'] == -1:
                    recommendations['SELL'] += 1
                else:
                    recommendations['HOLD'] += 1
            
            return {
                'consensus_reached': consensus_reached,
                'final_recommendation': final_recommendation,
                'recommendations': recommendations,
                'agent_positions': agent_positions,
                'conversation_length': len(self.conversation_history),
                'sophisticated_consensus': True,
                'agent_data': agent_data
            }
            
        except Exception as e:
            print(f"⚠️ Error in sophisticated consensus: {e}")
            print("🔄 Falling back to simple consensus...")
            return self._fallback_consensus()
    
    def _fallback_consensus(self):
        """Fallback to simple consensus counting"""
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
            'conversation_length': len(self.conversation_history),
            'sophisticated_consensus': False
        }
    
    def display_final_results(self, result):
        """Display final analysis results"""
        
        print("\n🎉 ANALYSIS COMPLETE!")
        print("=" * 60)
        
        print(f"Final Recommendation: {result['final_recommendation']}")
        print(f"Consensus Reached: {'Yes' if result['consensus_reached'] else 'No'}")
        print(f"Consensus Method: {'Sophisticated Protocol' if result.get('sophisticated_consensus', False) else 'Simple Counting'}")
        print(f"Conversation Length: {result['conversation_length']} messages")
        
        print(f"\n📈 Recommendation Breakdown:")
        for rec, count in result['recommendations'].items():
            if count > 0:
                print(f"  {rec}: {count}")
        
        print(f"\n👥 Individual Agent Positions:")
        for agent, position in result['agent_positions'].items():
            if 'Wassim_Fundamental_Agent' in agent:
                agent_name = "Wassim (Fundamental Agent)"
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
