"""
Interactive Command-Line Interface for Financial Analysis Multi-Agent System
Shows real agent conversations and consensus building
"""

import asyncio
import random
import time
import os
from datetime import datetime
import pandas as pd
import numpy as np
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.ollama import OllamaChatCompletionClient
from indicator_forecaster import IndicatorForecaster
from macro_var_analyzer import MacroVARAnalyzer
from data_fetchers import fetch_yahoo_prices, fetch_fundamentals
from portfolio_constructor import equal_weight_weights, inverse_vol_weights
from backtester import run_backtest
from sector_comparator import SectorComparator
from arima_regime_switching import ARIMARegimeSwitching
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
        self.sector_comparator = SectorComparator()
        self.arima_regime = ARIMARegimeSwitching()
        
    async def initialize_agents(self):
        """Initialize the two financial agents (Wassim and Yugo)"""
        print("Initializing AI agents...")
        
        self.ollama_client = OllamaChatCompletionClient(model="llama3.2")
        
        # Create specialized agents with personality
        self.agents = {
            'fundamental': AssistantAgent(
                name="Wassim_Fundamental_Agent",
                model_client=self.ollama_client,
                system_message="""You are Wassim, an integrated valuation and fundamental analysis expert (male, age 48).  
Education: Bachelor's and Master's degrees in Economics, specializing in Financial Econometrics and Quantitative Finance.  
Career Background: Former equity research analyst and portfolio strategist at leading asset management firms, experienced in valuation modeling, macroeconomic analysis, and cross-asset allocation.  

You are an ENTJ analyst in asset management — analytical, visionary, and execution-driven.  

When analyzing equities, you specialize in:
- **Relative Valuation**: Compare PBR (Price-to-Book), ROE (Return on Equity), and ROA (Return on Assets) across sector peers
- **Sector Positioning**: Identify whether stocks are trading at premium/discount valuations relative to sector averages
- **Fundamental Quality**: Assess operating efficiency (ROA), shareholder returns (ROE), and valuation multiples (PBR, PE)
- **Macro Context**: Understand broader economic trends and their impact on sector fundamentals

When sector comparison data is provided:
- Analyze percentile rankings (e.g., "ROE at 85th percentile means top-tier profitability")
- Interpret z-scores (e.g., "PBR z-score of -1.2 indicates trading at a discount")
- Compare composite scores across stocks (higher score = better fundamentals + cheaper valuation)
- Identify value opportunities where high ROE/ROA stocks trade at low PBR

CRITICAL: At the end of your final analysis, you MUST provide a structured consensus statement in this exact format:
CONSENSUS: direction=X confidence=Y.Z reliability=W.V

Where:
- direction: -1 (SELL), 0 (HOLD), or +1 (BUY)
- confidence: 0.0 to 1.0 (your confidence in this recommendation)
- reliability: 0.0 to 1.0 (your reliability/credibility for this type of analysis)

Always provide comprehensive analysis with specific numbers, percentages, and detailed reasoning for your BUY/SELL recommendations.
Be conversational but professional in your responses. Address other agents by name when responding to them.
Format your analysis with clear sections and bullet points for readability."""
            ),
            
            'valuation': AssistantAgent(
                name="Yugo_Valuation_Agent",
                model_client=self.ollama_client,
                system_message="""You are Yugo, a quantitative and technical analysis expert (male, age 46).  
Education: Bachelor's in Computer Science and Master's in Computational Engineering, specializing in Machine Learning and Time-Series Forecasting.  
Career Background: Former quantitative researcher and data scientist at a global hedge fund and AI research lab, specializing in predictive modeling, algorithmic trading, and statistical forecasting systems.  

You are an INTP analyst — curious, analytical, and quietly inventive.  


You specialize in:
- **ARIMA Regime-Switching Forecasting**: Analyze forecasts from different volatility regimes (low/medium/high vol)
- **Regime Interpretation**: Explain which regime the market is in and what it means for forecast reliability
- **Technical Indicator Analysis**: Interpret RSI, MACD, Bollinger Bands, and realized volatility
- **Statistical Rigor**: Evaluate MSE/MAE metrics, confidence intervals, and forecast accuracy
- **Risk-Adjusted Returns**: Calculate Sharpe ratios and volatility-adjusted price targets
- **Multi-Horizon Forecasting**: Integrate 1D and 1W forecasts with regime-specific dynamics

When ARIMA regime-switching data is provided:
- Identify current volatility regime (low/medium/high)
- Explain how regime affects forecast confidence (low vol = more reliable, high vol = wider CI)
- Compare AIC/BIC across regime models to assess which fits best
- Interpret regime transitions as signals (e.g., low→high vol = increasing uncertainty)
- Use regime-specific forecasts for price targets

When technical indicator data is available:
- Summarize key forecasting insights (walk-forward MSE/MAE)
- Provide specific price targets with confidence intervals
- Analyze volatility patterns and risk metrics

CRITICAL: At the end of your final analysis, you MUST provide a structured consensus statement in this exact format:
CONSENSUS: direction=X confidence=Y.Z reliability=W.V

Where:
- direction: -1 (SELL), 0 (HOLD), or +1 (BUY)
- confidence: 0.0 to 1.0 (your confidence in this recommendation)
- reliability: 0.0 to 1.0 (your reliability/credibility for this type of analysis)

Always provide comprehensive quantitative analysis with specific numbers, models, price targets, and detailed reasoning.
Be analytical but accessible in your responses. Address other agents by name when responding to them.
Format your analysis with clear sections and bullet points for readability."""
            )
        }
        
        print("✅ Agents initialized successfully!")
    
    async def run_sector_portfolio_analysis(self):
        """
        Integrated sector-based portfolio analysis with agent debate.
        
        Workflow:
        1. User picks stocks in same sector (recommend 5-10)
        2. Fetch fundamentals (PBR/ROE/ROA) + historical prices from Yahoo Finance
        3. Wassim (Fundamental Agent) analyzes sector comparison & valuations
        4. Yugo (Valuation Agent) runs ARIMA regime-switching forecasts
        5. Agents debate using sophisticated consensus mechanism
        6. Consensus filter validates/warns/vetoes investment decision
        7. Construct portfolio from top-ranked stocks and backtest
        
        Outputs: Agent debate transcript, consensus filter, portfolio metrics, equity curves
        """
        try:
            print("\n🏢 Sector Portfolio Analysis & Agent Debate")
            print("=" * 80)
            
            # Get stock symbols
            symbols_str = input("Enter 10 stock tickers in the same sector (comma-separated, e.g., AAPL,MSFT,...): ").strip()
            if not symbols_str:
                print("❌ No tickers provided.")
                return
            symbols = [s.strip().upper() for s in symbols_str.split(',') if s.strip()]
            
            if len(symbols) < 2:
                print("❌ Please provide at least 2 tickers for comparison.")
                return
            
            start = input("Start date [YYYY-MM-DD, default 2020-01-01]: ").strip() or "2020-01-01"
            end = input("End date [YYYY-MM-DD, default today]: ").strip() or datetime.today().strftime('%Y-%m-%d')
            
            print(f"\n⬇️  Fetching fundamentals for {len(symbols)} stocks...")
            print("⏳ Please wait, adding delays to avoid rate limiting...")
            fundamentals_df = fetch_fundamentals(symbols)
            
            # Check if we got valid data
            valid_data_count = fundamentals_df[['pb_ratio', 'roe', 'roa']].notna().any(axis=1).sum()
            if valid_data_count == 0:
                print("\n⚠️  WARNING: No fundamental data retrieved (Yahoo Finance rate limit likely hit)")
                print("💡 Try waiting a few minutes and running again, or use fewer stocks")
                return
            elif valid_data_count < len(symbols):
                print(f"\n⚠️  WARNING: Only {valid_data_count}/{len(symbols)} stocks have valid fundamental data")
            
            print("✅ Fundamentals fetched:")
            print(fundamentals_df[['symbol', 'sector', 'pb_ratio', 'roe', 'roa']].to_string(index=False))
            
            # Verify sector consistency
            sectors = fundamentals_df['sector'].value_counts()
            if len(sectors) > 1:
                print(f"\n⚠️  Warning: Multiple sectors detected: {sectors.to_dict()}")
                print("    Analysis will use the most common sector.")
            
            # Sector comparison
            print("\n📊 Running sector comparison analysis...")
            if self.sector_comparator.load_fundamentals(fundamentals_df):
                sector_comp_df = self.sector_comparator.compute_sector_comparison()
                sector_report = self.sector_comparator.format_comparison_report()
                print(sector_report)
                
                # Get rankings
                rankings = self.sector_comparator.get_sector_rankings()
                print("\n🏆 Sector Rankings (by composite score):")
                print(rankings[['symbol', 'composite_score', 'pb_ratio', 'roe', 'roa']].head(10).to_string(index=False))
            
            # Fetch price data
            print(f"\n⬇️  Fetching price data from {start} to {end}...")
            price_dict = fetch_yahoo_prices(symbols, start=start, end=end, interval="1d")
            
            # Build price DataFrame with clean single-level column index
            frames = []
            valid_symbols = []
            for sym in symbols:
                df = price_dict.get(sym, None)
                if df is not None and not df.empty and 'adj_close' in df.columns:
                    # Extract as Series to avoid MultiIndex issues
                    price_series = df['adj_close'].copy()
                    price_series.name = sym
                    frames.append(price_series)
                    valid_symbols.append(sym)
            
            if not frames:
                print("❌ No valid price data downloaded.")
                return
            
            # Concatenate Series into DataFrame with simple column index
            price_df = pd.concat(frames, axis=1)
            price_df = price_df.dropna(how='all')
            
            # Ensure we have a simple Index (not MultiIndex) on columns
            if isinstance(price_df.columns, pd.MultiIndex):
                price_df.columns = price_df.columns.get_level_values(-1)
            
            print(f"✅ Price data fetched: {price_df.shape[0]} days, {price_df.shape[1]} stocks")
            
            # Run ARIMA regime-switching on a representative stock (first one)
            arima_report = None
            if len(valid_symbols) > 0:
                rep_symbol = valid_symbols[0]
                print(f"\n🔮 Running ARIMA regime-switching forecast for {rep_symbol}...")
                # Extract series properly and ensure it's a simple Series with datetime index
                rep_prices = price_df[rep_symbol].dropna()
                # Convert to simple Series if needed (remove any MultiIndex issues)
                if isinstance(rep_prices.index, pd.MultiIndex):
                    rep_prices = rep_prices.reset_index(drop=True)
                # Ensure it's a Series with proper name
                rep_prices.name = rep_symbol
                
                if self.arima_regime.load_data(rep_prices):
                    self.arima_regime.detect_regimes()
                    self.arima_regime.fit_regime_models(order=(2, 1, 2))
                    self.arima_regime.forecast(steps=5)
                    arima_report = self.arima_regime.format_report()
                    print(arima_report)
            
            # Initialize agents
            await self.initialize_agents()
            
            # Build analysis prompt for agents
            sector = fundamentals_df['sector'].mode()[0] if not fundamentals_df['sector'].mode().empty else 'Unknown'
            prompt = f"""
Sector Portfolio Analysis: {sector}

Task: Analyze {len(valid_symbols)} stocks in the {sector} sector and recommend which stocks to BUY/HOLD/SELL for a sector portfolio.

Wassim: Focus on relative valuation using the sector comparison data below. Identify value opportunities where high-quality companies (high ROE/ROA) trade at attractive valuations (low PBR relative to peers).

Yugo: Focus on ARIMA regime-switching forecasts and technical dynamics. Consider current volatility regime and forecast reliability.

Both: Debate and reach consensus on which stocks offer the best risk-adjusted opportunities. Consider constructing a portfolio from the top 5-7 stocks.

📊 Sector Comparison Data:
{sector_report}

🏆 Top Ranked Stocks:
{rankings[['symbol', 'composite_score', 'pb_ratio', 'roe', 'roa']].head(10).to_string(index=False) if 'rankings' in locals() else 'N/A'}
"""
            
            if arima_report:
                prompt += f"\n\n🔮 ARIMA Regime-Switching Analysis ({rep_symbol}):\n{arima_report}\n"
            
            prompt += """
CRITICAL: Provide specific stock recommendations (BUY/HOLD/SELL) and suggest portfolio weights.
At the end, provide your CONSENSUS statement.
"""
            
            # Run agent debate
            result = await self.run_analysis_with_debate(prompt, f"{sector} Sector")
            
            # Display results
            self.display_final_results(result)
            
            # Apply consensus filter
            print("\n" + "=" * 80)
            print("🎯 CONSENSUS FILTER: Agent Recommendation Impact")
            print("=" * 80)
            
            final_rec = result.get('final_recommendation', 'HOLD')
            consensus_reached = result.get('consensus_reached', False)
            
            # Extract consensus strength if available
            agent_data = result.get('agent_data', {})
            if agent_data:
                avg_confidence = np.mean([d['confidence'] for d in agent_data.values()])
                avg_reliability = np.mean([d['reliability'] for d in agent_data.values()])
                consensus_strength = avg_confidence * avg_reliability
            else:
                consensus_strength = 0.5  # Default moderate strength
            
            print(f"Agent Consensus: {final_rec}")
            print(f"Consensus Reached: {'Yes' if consensus_reached else 'No'}")
            if agent_data:
                print(f"Average Confidence: {avg_confidence:.2f}")
                print(f"Average Reliability: {avg_reliability:.2f}")
                print(f"Consensus Strength: {consensus_strength:.2f}")
            print("-" * 80)
            
            # Decision logic based on consensus
            if final_rec == 'SELL':
                print("🔴 SELL CONSENSUS DETECTED")
                print("   The agents recommend AGAINST investing in this sector.")
                print("   Reasons may include:")
                print("   - Overvalued fundamentals (high PBR relative to quality)")
                print("   - High volatility regime with poor forecast outlook")
                print("   - Sector headwinds or deteriorating metrics")
                print("")
                user_override = input("   ⚠️  Do you want to proceed with portfolio construction anyway? [y/N]: ").strip().lower()
                if user_override not in ['y', 'yes']:
                    print("\n❌ Portfolio construction cancelled based on agent recommendation.")
                    print("   Consider analyzing a different sector or waiting for better conditions.")
                    return
                else:
                    print("\n⚠️  User override: Proceeding despite SELL consensus...")
                    
            elif final_rec == 'HOLD':
                print("⚪ HOLD CONSENSUS DETECTED")
                print("   The agents are NEUTRAL on this sector.")
                print("   This may indicate:")
                print("   - Mixed signals between fundamentals and technicals")
                print("   - Fair valuation (neither cheap nor expensive)")
                print("   - Moderate uncertainty or conflicting data")
                if consensus_strength < 0.5:
                    print("   - Low consensus strength suggests high uncertainty")
                print("")
                print("   💡 Recommendation: Proceed with caution")
                print("      Consider smaller position sizes or additional analysis")
                print("")
                    
            else:  # BUY
                print("🟢 BUY CONSENSUS DETECTED")
                print("   The agents recommend investing in this sector.")
                print("   Positive factors may include:")
                print("   - Strong fundamentals at attractive valuations")
                print("   - Favorable volatility regime and forecast outlook")
                print("   - High-quality companies with growth potential")
                if consensus_strength >= 0.7:
                    print(f"   - Strong consensus (strength {consensus_strength:.2f}) adds confidence")
                elif consensus_strength < 0.5:
                    print(f"   - Moderate consensus (strength {consensus_strength:.2f}) suggests some uncertainty")
                print("")
                print("   ✅ Recommendation: Portfolio construction supported by agent analysis")
                print("")
            
            print("=" * 80)
            
            # Construct portfolio based on top-ranked stocks
            construct = input("\nConstruct and backtest a portfolio from top-ranked stocks? [y/N]: ").strip().lower()
            if construct in ['y', 'yes']:
                n_stocks = input("How many top stocks to include? (default 5): ").strip() or "5"
                try:
                    n_stocks = int(n_stocks)
                except:
                    n_stocks = 5
                
                top_symbols = rankings.head(n_stocks)['symbol'].tolist()
                top_symbols = [s for s in top_symbols if s in price_df.columns]
                
                if len(top_symbols) < 2:
                    print("❌ Not enough valid stocks for portfolio.")
                    return
                
                print(f"\n🧮 Constructing portfolio from: {', '.join(top_symbols)}")
                
                portfolio_prices = price_df[top_symbols].dropna()
                
                strategy = input("Strategy [equal|invvol] (default equal): ").strip().lower() or "equal"
                freq = input("Rebalance frequency [D/W/M/Q] (default M): ").strip().upper() or "M"
                
                if strategy == 'invvol':
                    w = inverse_vol_weights(portfolio_prices)
                else:
                    w = equal_weight_weights(top_symbols)
                
                print(f"\n📊 Portfolio weights:\n{w.to_string()}")
                
                # Backtest
                res = run_backtest(portfolio_prices, target_weights=w, rebalance_frequency=freq, trading_cost_bps=5.0)
                
                print("\n📊 Portfolio Performance Metrics")
                print("=" * 80)
                for k, v in res.metrics.items():
                    if isinstance(v, float):
                        print(f"{k}: {v:.4f}")
                
                # Save equity curve
                try:
                    import matplotlib.pyplot as plt
                    plt.figure(figsize=(12, 5))
                    res.equity_curve.plot()
                    plt.title(f"{sector} Sector Portfolio Equity Curve")
                    plt.xlabel("Date"); plt.ylabel("Equity")
                    plt.grid(alpha=0.3)
                    out = f"sector_portfolio_{sector.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    plt.tight_layout(); plt.savefig(out, dpi=200); plt.close()
                    print(f"\n🖼️  Saved: {out}")
                except Exception as e:
                    print(f"⚠️ Could not save plot: {e}")
                
                # Save cumulative return chart
                try:
                    import matplotlib.pyplot as plt
                    import numpy as np
                    
                    cumulative_return = (res.equity_curve - 1) * 100  # Convert to percentage
                    
                    plt.figure(figsize=(12, 5))
                    plt.plot(cumulative_return.index, cumulative_return.values, linewidth=2, color='#2E86AB')
                    plt.title(f"Cumulative Return of Portfolio ({sector} Sector)", fontsize=14, fontweight='bold')
                    plt.xlabel("Date", fontsize=12)
                    plt.ylabel("Cumulative Return (%)", fontsize=12)
                    plt.grid(alpha=0.3, linestyle='--')
                    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
                    
                    out_cum = f"cumulative_return_{sector.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    plt.tight_layout()
                    plt.savefig(out_cum, dpi=200, bbox_inches='tight')
                    plt.close()
                    print(f"🖼️  Saved: {out_cum}")
                except Exception as e:
                    print(f"⚠️ Could not save cumulative return plot: {e}")
                
                # Save rolling Sharpe ratio chart
                try:
                    import matplotlib.pyplot as plt
                    import numpy as np
                    
                    # Calculate daily returns
                    daily_returns = res.equity_curve.pct_change().dropna()
                    
                    # Calculate rolling Sharpe ratio (60-day window, annualized)
                    rolling_window = 60
                    rolling_mean = daily_returns.rolling(window=rolling_window).mean() * 252
                    rolling_std = daily_returns.rolling(window=rolling_window).std() * np.sqrt(252)
                    rolling_sharpe = rolling_mean / rolling_std.replace(0, np.nan)
                    rolling_sharpe = rolling_sharpe.dropna()
                    
                    if len(rolling_sharpe) > 0:
                        plt.figure(figsize=(12, 5))
                        plt.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=2, color='#A23B72')
                        plt.title(f"Rolling Sharpe Ratio of Portfolio ({sector} Sector, {rolling_window}-day window)", fontsize=14, fontweight='bold')
                        plt.xlabel("Date", fontsize=12)
                        plt.ylabel("Rolling Sharpe Ratio", fontsize=12)
                        plt.grid(alpha=0.3, linestyle='--')
                        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
                        plt.axhline(y=1, color='green', linestyle='--', linewidth=0.8, alpha=0.5, label='Sharpe=1.0')
                        plt.axhline(y=2, color='darkgreen', linestyle='--', linewidth=0.8, alpha=0.5, label='Sharpe=2.0')
                        plt.legend(loc='best')
                        
                        out_sharpe = f"rolling_sharpe_{sector.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        plt.tight_layout()
                        plt.savefig(out_sharpe, dpi=200, bbox_inches='tight')
                        plt.close()
                        print(f"🖼️  Saved: {out_sharpe}")
                    else:
                        print("⚠️ Not enough data for rolling Sharpe ratio calculation")
                except Exception as e:
                    print(f"⚠️ Could not save rolling Sharpe plot: {e}")
        
        except Exception as e:
            print(f"❌ Error in sector portfolio analysis: {e}")
            import traceback
            traceback.print_exc()

    
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




if __name__ == "__main__":
    # Launch the integrated system
    print("\n" + "=" * 80)
    print("🤖 Financial Analysis Multi-Agent System")
    print("=" * 80)
    print("\nAll data fetched from Yahoo Finance & FRED APIs")
    print("\nFeatures:")
    print("• Sector portfolio analysis with AI agent debate")
    print("• ARIMA regime-switching forecasts")
    print("• Fundamental analysis (PBR/ROE/ROA)")
    print("• Consensus filter for investment validation")
    print("• Portfolio backtesting with performance analytics")
    print("=" * 80)
    
    # Run sector portfolio analysis with agents
    async def run_analysis():
        iface = InteractiveFinancialInterface()
        try:
            await iface.run_sector_portfolio_analysis()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        finally:
            await iface.close()
    
    asyncio.run(run_analysis())
