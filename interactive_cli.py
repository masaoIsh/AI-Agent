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
from backtester import compute_returns
from optimizer_mpt import (
    wassim_confidence,
    yugo_confidence_from_prices,
    combine_confidence,
    map_scores_to_expected_returns_from_confidence,
    sample_covariance,
    max_sharpe_long_only,
)
from rolling_portfolio_optimizer import (
    rolling_optimize_weights,
    compare_in_sample_vs_out_of_sample,
    analyze_weight_stability,
)
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

**YOUR PRIMARY TASK**: Select which specific stocks from the provided list should be included in the portfolio.
- Analyze each stock individually based on fundamentals
- Rank stocks and identify your top picks (typically 5-7 stocks from a list of 10)
- Explain WHY you're including each stock and WHY you're excluding others
- Consider both quality (ROE/ROA) and valuation (PBR) when making selections

CRITICAL: At the end of your final analysis, you MUST provide your stock selections in this exact format:
MY PICKS: [SYMBOL1, SYMBOL2, SYMBOL3, SYMBOL4, SYMBOL5, SYMBOL6, SYMBOL7]
CONFIDENCE: X.XX (0.0 to 1.0 - your confidence in this stock selection)

You MUST pick at least 7-8 stocks to ensure adequate diversification.

Example:
MY PICKS: [AAPL, MSFT, GOOGL, NVDA, META, AMD, AVGO, CRM]
CONFIDENCE: 0.85

Always provide comprehensive analysis with specific numbers, percentages, and detailed reasoning for each stock pick.
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

**YOUR PRIMARY TASK**: Select which specific stocks from the provided list should be included in the portfolio.
- Evaluate each stock based on regime analysis and forecast outlook
- Consider volatility regimes: favor low/medium vol stocks, be cautious with high vol
- Rank stocks and identify your top picks (typically 5-7 stocks from a list of 10)
- Explain WHY you're including each stock and WHY you're excluding others
- Balance upside potential with regime-based risk assessment

CRITICAL: At the end of your final analysis, you MUST provide your stock selections in this exact format:
MY PICKS: [SYMBOL1, SYMBOL2, SYMBOL3, SYMBOL4, SYMBOL5, SYMBOL6, SYMBOL7]
CONFIDENCE: X.XX (0.0 to 1.0 - your confidence in this stock selection)

You MUST pick at least 7-8 stocks to ensure adequate diversification.

Example:
MY PICKS: [AAPL, MSFT, NVDA, GOOGL, AMD, INTC, TXN, MU]
CONFIDENCE: 0.78

Always provide comprehensive quantitative analysis with specific numbers, models, price targets, and detailed reasoning for each stock pick.
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
                # Default US Technology universe (15 names)
                symbols = [
                    "AAPL","MSFT","NVDA","GOOGL","META","AMD","AVGO","CRM","ORCL","INTC",
                    "TXN","AMAT","MU","ADI","PANW",
                ]
                print(f"Using default Technology universe: {', '.join(symbols)}")
            else:
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
Sector Portfolio Selection: {sector}

**YOUR PRIMARY TASK**: Select AT LEAST 7-8 stocks from the {len(valid_symbols)} stocks below to include in a portfolio.

Available stocks: {', '.join(valid_symbols)}

Wassim: Focus on relative valuation using sector comparison data. Pick stocks with:
- High quality fundamentals (ROE/ROA in top percentiles)
- Attractive valuations (PBR at discount relative to quality)
- Strong composite scores
IMPORTANT: You MUST pick at least 7-8 stocks for adequate diversification.

Yugo: Focus on ARIMA regime-switching forecasts and technical dynamics. Pick stocks with:
- Favorable volatility regimes (low/medium vol preferred over high vol)
- Positive forecast outlook
- Good risk-adjusted return potential
IMPORTANT: You MUST pick at least 7-8 stocks for adequate diversification.

Both: Debate each stock's merits. At the end, EACH agent must provide:
1. Your specific stock picks (MINIMUM 7-8 stocks): MY PICKS: [SYMBOL1, SYMBOL2, SYMBOL3, ...]
2. Your confidence level: CONFIDENCE: 0.XX

📊 Sector Comparison Data:
{sector_report}

🏆 Top Ranked Stocks (by composite score):
{rankings[['symbol', 'composite_score', 'pb_ratio', 'roe', 'roa']].head(10).to_string(index=False) if 'rankings' in locals() else 'N/A'}
"""
            
            if arima_report:
                prompt += f"\n\n🔮 ARIMA Regime-Switching Analysis ({rep_symbol}):\n{arima_report}\n"
            
            prompt += """
CRITICAL: You must provide your final stock selections using this exact format:
MY PICKS: [SYMBOL1, SYMBOL2, SYMBOL3, SYMBOL4, SYMBOL5, SYMBOL6, SYMBOL7, SYMBOL8]
CONFIDENCE: 0.XX

REMEMBER: Pick AT LEAST 7-8 stocks (you can pick more if confident).
Explain WHY you picked each stock and WHY you excluded others.
"""
            
            # Run agent debate
            result = await self.run_analysis_with_debate(prompt, f"{sector} Sector")
            
            # Display results
            self.display_final_results(result)
            
            # Use agent-selected stocks for portfolio
            print("\n" + "=" * 80)
            print("🎯 AGENT STOCK SELECTIONS")
            print("=" * 80)
            
            selected_stocks = result.get('selected_stocks', [])
            ranked_stocks = result.get('ranked_stocks', [])
            avg_confidence = result.get('avg_confidence', 0.5)
            
            if not selected_stocks:
                print("⚠️ No stocks selected by agents. Portfolio construction cancelled.")
                return
            
            print(f"Agents selected {len(selected_stocks)} stocks:")
            for symbol, data in ranked_stocks:
                consensus_level = "🟢 STRONG" if data['count'] >= 2 else "⚪ MODERATE"
                agents_str = " & ".join(data['agents'])
                print(f"  {consensus_level} {symbol}: Picked by {agents_str} (score: {data['total_weight']:.2f})")
            
            print("")
            print(f"Average Confidence: {avg_confidence:.2f}")
            print("=" * 80)
            
            # Construct portfolio from agent-selected stocks
            construct = input("\nConstruct and backtest portfolio from agent-selected stocks? [y/N]: ").strip().lower()
            if construct in ['y', 'yes']:
                # Filter to stocks that exist in price data
                portfolio_symbols = [s for s in selected_stocks if s in price_df.columns]
                
                if len(portfolio_symbols) < 2:
                    print("❌ Not enough valid stocks for portfolio.")
                    return
                
                print(f"\n🧮 Constructing portfolio from {len(portfolio_symbols)} agent-selected stocks:")
                print(f"   {', '.join(portfolio_symbols)}")
                
                portfolio_prices = price_df[portfolio_symbols].dropna()
                
                strategy = input("\nStrategy [equal|invvol|mpt] (default mpt): ").strip().lower() or "mpt"
                freq = input("Rebalance frequency [D/W/M/Q] (default M): ").strip().upper() or "M"
                
                # Ask user if they want out-of-sample validation
                use_oos = input("\n🔬 Use OUT-OF-SAMPLE rolling optimization? [Y/n]: ").strip().lower()
                use_oos = use_oos != 'n'  # Default to yes
                
                if use_oos:
                    print("\n" + "=" * 80)
                    print("🔬 OUT-OF-SAMPLE BACKTESTING (Proper Walk-Forward Validation)")
                    print("=" * 80)
                    print("This uses rolling optimization where at each rebalancing date,")
                    print("only past data is used to optimize weights. This avoids look-ahead bias.")
                    print()
                    
                    # Rolling optimization
                    weights_schedule = rolling_optimize_weights(
                        price_df=portfolio_prices,
                        fundamentals_df=fundamentals_df,
                        rebalance_frequency=freq,
                        strategy=strategy,
                        min_train_days=252,
                        lookback_days=None,  # Use expanding window
                        max_weight=0.20,
                        verbose=True
                    )
                    
                    # Analyze weight stability
                    stability = analyze_weight_stability(weights_schedule)
                    print(f"\n📊 Weight Stability Analysis:")
                    print(f"   Mean turnover per rebalance: {stability['mean_turnover_per_rebalance']:.2%}")
                    print(f"   Number of rebalancing events: {stability['num_rebalancing_events']}")
                    print(f"   Avg days between rebalances: {stability['avg_days_between_rebalance']:.1f}")
                    
                    # Backtest with time-varying weights
                    res = run_backtest(
                        portfolio_prices, 
                        weights_schedule=weights_schedule,
                        trading_cost_bps=5.0
                    )
                    
                    # Show sample of weights over time
                    print(f"\n📊 Sample Portfolio Weights (First & Last Rebalance):")
                    rebal_history = weights_schedule.attrs.get('rebal_history', [])
                    if len(rebal_history) > 0:
                        print(f"\n   First rebalance ({rebal_history[0]['date'].strftime('%Y-%m-%d')}):")
                        print(rebal_history[0]['weights'].to_string())
                        if len(rebal_history) > 1:
                            print(f"\n   Last rebalance ({rebal_history[-1]['date'].strftime('%Y-%m-%d')}):")
                            print(rebal_history[-1]['weights'].to_string())
                    
                else:
                    print("\n" + "=" * 80)
                    print("⚠️  IN-SAMPLE BACKTESTING (Single-Point Optimization with Look-Ahead Bias)")
                    print("=" * 80)
                    print("WARNING: This uses ALL data to optimize weights once, then backtests on the same data.")
                    print("This creates look-ahead bias and will likely overestimate performance.")
                    print()
                    
                    # Original single-point optimization
                    if strategy == 'invvol':
                        w = inverse_vol_weights(portfolio_prices)
                    elif strategy == 'equal':
                        w = equal_weight_weights(portfolio_symbols)
                    else:
                        # MPT pipeline: Agents -> confidence -> μ, sample Σ -> max Sharpe
                        c_w = wassim_confidence(fundamentals_df)
                        c_y = yugo_confidence_from_prices(portfolio_prices, lookback=126, method="ema")
                        c = combine_confidence(c_w, c_y, w_wassim=0.5, w_yugo=0.5)
                        c = c.reindex(portfolio_symbols).fillna(0.5)
                        mu = map_scores_to_expected_returns_from_confidence(c, ann_low=0.02, ann_high=0.15)
                        returns = compute_returns(portfolio_prices)
                        Sigma = sample_covariance(returns, lookback=252)
                        common = mu.index.intersection(Sigma.columns)
                        mu = mu.loc[common]
                        Sigma = Sigma.loc[common, common]
                        if len(common) < 2:
                            print("❌ Not enough overlap for MPT optimization. Falling back to inverse vol.")
                            w = inverse_vol_weights(portfolio_prices)
                        else:
                            w = max_sharpe_long_only(mu, Sigma, max_weight=0.20)
                    
                    print(f"\n📊 Static Portfolio weights:\n{w.to_string()}")
                    
                    # Backtest with static weights
                    res = run_backtest(
                        portfolio_prices, 
                        target_weights=w, 
                        rebalance_frequency=freq, 
                        trading_cost_bps=5.0
                    )
                
                # Show if this is OOS validated
                oos_validated = weights_schedule.attrs.get('oos_validated', False) if use_oos else False
                validation_status = "✅ OUT-OF-SAMPLE (No Look-Ahead Bias)" if oos_validated else "⚠️  IN-SAMPLE (Contains Look-Ahead Bias)"
                
                print("\n📊 Portfolio Performance Metrics")
                print("=" * 80)
                print(f"Validation: {validation_status}")
                print("-" * 80)
                for k, v in res.metrics.items():
                    if isinstance(v, float):
                        print(f"{k}: {v:.4f}")
                
                # Optionally compare with in-sample if user chose out-of-sample
                if use_oos:
                    compare = input("\n🔍 Compare with IN-SAMPLE baseline? [y/N]: ").strip().lower()
                    if compare in ['y', 'yes']:
                        print("\n📊 Running IN-SAMPLE comparison (using all data)...")
                        try:
                            # Run in-sample for comparison
                            if strategy == 'invvol':
                                w_in = inverse_vol_weights(portfolio_prices)
                            elif strategy == 'equal':
                                w_in = equal_weight_weights(portfolio_symbols)
                            else:
                                c_w = wassim_confidence(fundamentals_df)
                                c_y = yugo_confidence_from_prices(portfolio_prices, lookback=126, method="ema")
                                c = combine_confidence(c_w, c_y, w_wassim=0.5, w_yugo=0.5)
                                c = c.reindex(portfolio_symbols).fillna(0.5)
                                mu = map_scores_to_expected_returns_from_confidence(c, ann_low=0.02, ann_high=0.15)
                                returns = compute_returns(portfolio_prices)
                                Sigma = sample_covariance(returns, lookback=252)
                                common = mu.index.intersection(Sigma.columns)
                                if len(common) >= 2:
                                    mu = mu.loc[common]
                                    Sigma = Sigma.loc[common, common]
                                    w_in = max_sharpe_long_only(mu, Sigma, max_weight=0.20)
                                    w_in = w_in.reindex(portfolio_symbols).fillna(0.0)
                                else:
                                    w_in = equal_weight_weights(portfolio_symbols)
                            
                            res_in = run_backtest(portfolio_prices, target_weights=w_in, rebalance_frequency=freq, trading_cost_bps=5.0)
                            
                            print("\n📊 COMPARISON: Out-of-Sample vs In-Sample")
                            print("=" * 80)
                            print(f"{'Metric':<15} {'Out-of-Sample':<20} {'In-Sample':<20} {'Difference':<15}")
                            print("-" * 80)
                            for k in res.metrics.keys():
                                oos_val = res.metrics[k]
                                in_val = res_in.metrics[k]
                                diff = oos_val - in_val
                                diff_pct = (diff / abs(in_val) * 100) if in_val != 0 else 0
                                print(f"{k:<15} {oos_val:>18.4f}  {in_val:>18.4f}  {diff:>+13.4f} ({diff_pct:+.1f}%)")
                            
                            # Save comparison visualization
                            self._save_comparison_charts(
                                res_oos=res,
                                res_in=res_in,
                                sector=sector,
                                strategy=strategy
                            )
                        except Exception as e:
                            print(f"⚠️ Could not run in-sample comparison: {e}")
                            import traceback
                            traceback.print_exc()
                
                # Save equity curve
                try:
                    import matplotlib.pyplot as plt
                    validation_label = "OOS" if oos_validated else "In-Sample"
                    plt.figure(figsize=(12, 5))
                    res.equity_curve.plot(linewidth=2)
                    plt.title(f"{sector} Sector Portfolio Equity Curve ({validation_label})")
                    plt.xlabel("Date"); plt.ylabel("Equity")
                    plt.grid(alpha=0.3)
                    out = f"sector_portfolio_{sector.replace(' ', '_')}_{validation_label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
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
        """Analyze conversation history and extract stock picks from agents"""
        
        print("\n🧮 Extracting Stock Picks from Agent Debate...")
        print("=" * 60)
        
        # Extract stock picks from conversation
        messages = [{'content': entry['message'], 'source': entry['speaker']} 
                   for entry in self.conversation_history]
        
        agent_picks = self._extract_stock_picks(messages)
        
        if not agent_picks:
            print("⚠️ No stock picks found in agent messages, falling back to simple consensus...")
            return self._fallback_consensus()
        
        # Combine picks from both agents
        ranked_stocks, stock_scores = self._combine_stock_picks(agent_picks)
        
        if not ranked_stocks:
            print("⚠️ Could not combine stock picks, falling back...")
            return self._fallback_consensus()
        
        # Extract just the stock symbols in ranked order
        selected_stocks = [symbol for symbol, _ in ranked_stocks]
        
        # Ensure minimum 5 stocks for portfolio construction
        MIN_STOCKS = 5
        if len(selected_stocks) < MIN_STOCKS:
            print(f"\n⚠️  Only {len(selected_stocks)} stocks selected by agents, need at least {MIN_STOCKS}")
            print(f"    Please ensure agents pick at least {MIN_STOCKS} stocks each.")
            # Return with flag that consensus failed
            return {
                'consensus_reached': False,
                'selected_stocks': selected_stocks,
                'ranked_stocks': ranked_stocks,
                'stock_scores': stock_scores,
                'agent_picks': agent_picks,
                'avg_confidence': 0.0,
                'method': 'stock_selection',
                'conversation_length': len(self.conversation_history),
                'error': f'Insufficient stocks: {len(selected_stocks)} < {MIN_STOCKS}'
            }
        
        # Calculate average confidence (reliability removed)
        avg_confidence = sum(d['confidence'] for d in agent_picks.values()) / len(agent_picks)
        
        print(f"\n✅ Stock Selection Complete!")
        print(f"   Selected {len(selected_stocks)} stocks from agent recommendations")
        print(f"   Average Confidence: {avg_confidence:.2f}")
        
        return {
            'consensus_reached': True,
            'selected_stocks': selected_stocks,
            'ranked_stocks': ranked_stocks,
            'stock_scores': stock_scores,
            'agent_picks': agent_picks,
            'avg_confidence': avg_confidence,
            'method': 'stock_selection',
            'conversation_length': len(self.conversation_history)
        }
    
    def analyze_consensus_old(self):
        """OLD METHOD: Analyze conversation history using sophisticated consensus protocol"""
        
        print("\n🧮 Applying Sophisticated Consensus Protocol...")
        print("=" * 60)
        
        # Extract structured consensus data from agent messages
        agent_data = {}
        agent_positions = {}
        
        for entry in self.conversation_history:
            content = entry['message']
            speaker = entry['speaker']
            
            # Look for CONSENSUS statements (OLD FORMAT)
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
    
    def _extract_stock_picks(self, messages):
        """Extract stock picks from agent messages"""
        import re
        
        agent_picks = {}
        
        for msg in messages:
            content = msg.content if hasattr(msg, 'content') else str(msg)
            speaker = msg.source if hasattr(msg, 'source') else 'Unknown'
            
            # Look for MY PICKS: [SYMBOL1, SYMBOL2, ...]
            if 'MY PICKS:' in content.upper():
                try:
                    # Extract the stock list - try both with and without brackets
                    picks_match = re.search(r'MY PICKS:\s*\[([^\]]+)\]', content, re.IGNORECASE)
                    if not picks_match:
                        # Try without brackets
                        picks_match = re.search(r'MY PICKS:\s*([A-Z, ]+)', content, re.IGNORECASE)
                    if picks_match:
                        picks_str = picks_match.group(1)
                        # Clean and split the symbols
                        symbols = [s.strip().upper() for s in picks_str.split(',')]
                        symbols = [s for s in symbols if s and len(s) <= 5]  # Remove empty and placeholders
                        
                        # Filter out placeholder symbols like SYMBOL1, SYMBOL2, etc.
                        symbols = [s for s in symbols if not s.startswith('SYMBOL') and s != '...']
                        
                        # Skip if no valid symbols
                        if not symbols:
                            continue
                        
                        # Extract confidence - try multiple patterns
                        confidence = 0.5  # default
                        conf_patterns = [
                            r'CONFIDENCE:\s*([\d\.]+)',
                            r'CONFIDENCE\s*([\d\.]+)',
                            r'confidence:\s*([\d\.]+)',
                            r'confidence\s*([\d\.]+)'
                        ]
                        for pattern in conf_patterns:
                            conf_match = re.search(pattern, content, re.IGNORECASE)
                            if conf_match:
                                confidence = float(conf_match.group(1))
                                break
                        
                        # Only store if confidence > 0 (skip placeholder examples)
                        if confidence > 0:
                            # Store agent picks (keep the latest valid one per agent)
                            agent_name = 'Wassim' if 'Wassim' in speaker else 'Yugo'
                            agent_picks[agent_name] = {
                                'picks': symbols,
                                'confidence': confidence
                            }
                            
                            print(f"\n📋 {agent_name}'s Picks: {symbols}")
                            print(f"   Confidence: {confidence:.2f}")
                        
                except Exception as e:
                    print(f"⚠️ Error parsing picks from {speaker}: {e}")
        
        return agent_picks
    
    def _combine_stock_picks(self, agent_picks):
        """Combine stock picks from multiple agents with weighted scoring"""
        if not agent_picks:
            return None, None
        
        # Count how many agents picked each stock and their weights
        stock_scores = {}
        
        for agent_name, data in agent_picks.items():
            # Use confidence only (reliability removed)
            weight = data.get('confidence', 0.5)
            for symbol in data['picks']:
                if symbol not in stock_scores:
                    stock_scores[symbol] = {
                        'agents': [],
                        'total_weight': 0.0,
                        'count': 0
                    }
                stock_scores[symbol]['agents'].append(agent_name)
                stock_scores[symbol]['total_weight'] += weight
                stock_scores[symbol]['count'] += 1
        
        # Sort by total weight (confidence * reliability sum)
        ranked_stocks = sorted(
            stock_scores.items(),
            key=lambda x: (x[1]['count'], x[1]['total_weight']),  # Sort by count first, then weight
            reverse=True
        )
        
        print("\n" + "=" * 80)
        print("📊 CONSENSUS STOCK RANKING")
        print("=" * 80)
        
        for symbol, data in ranked_stocks:
            consensus_level = "🟢 STRONG" if data['count'] >= 2 else "⚪ MODERATE"
            agents_str = " & ".join(data['agents'])
            print(f"{consensus_level} | {symbol:6} | Picked by: {agents_str:20} | Score: {data['total_weight']:.2f}")
        
        print("=" * 80)
        
        return ranked_stocks, stock_scores
    
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
    
    def _save_comparison_charts(self, res_oos, res_in, sector, strategy):
        """Save side-by-side comparison charts of OOS vs In-Sample"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            fig, axes = plt.subplots(2, 1, figsize=(14, 10))
            
            # Equity curves comparison
            ax1 = axes[0]
            res_oos.equity_curve.plot(ax=ax1, label='Out-of-Sample', linewidth=2, color='#2E86AB')
            res_in.equity_curve.plot(ax=ax1, label='In-Sample (Biased)', linewidth=2, color='#FF6B6B', alpha=0.7, linestyle='--')
            ax1.set_title(f'{sector} Sector: Out-of-Sample vs In-Sample Equity Curves', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Equity')
            ax1.legend()
            ax1.grid(alpha=0.3)
            
            # Cumulative returns comparison
            ax2 = axes[1]
            cum_oos = (res_oos.equity_curve - 1) * 100
            cum_in = (res_in.equity_curve - 1) * 100
            ax2.plot(cum_oos.index, cum_oos.values, label='Out-of-Sample', linewidth=2, color='#2E86AB')
            ax2.plot(cum_in.index, cum_in.values, label='In-Sample (Biased)', linewidth=2, color='#FF6B6B', alpha=0.7, linestyle='--')
            ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
            ax2.set_title('Cumulative Returns Comparison', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Cumulative Return (%)')
            ax2.legend()
            ax2.grid(alpha=0.3)
            
            plt.tight_layout()
            out = f"comparison_OOS_vs_InSample_{sector.replace(' ', '_')}_{strategy}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(out, dpi=200, bbox_inches='tight')
            plt.close()
            print(f"\n🖼️  Saved comparison chart: {out}")
            
            # Performance metrics bar chart
            fig, ax = plt.subplots(1, 1, figsize=(12, 6))
            metrics = ['CAGR', 'Sharpe', 'Vol', 'MaxDD']
            oos_vals = [res_oos.metrics.get(m, 0) for m in metrics]
            in_vals = [res_in.metrics.get(m, 0) for m in metrics]
            
            x = np.arange(len(metrics))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, oos_vals, width, label='Out-of-Sample', color='#2E86AB')
            bars2 = ax.bar(x + width/2, in_vals, width, label='In-Sample (Biased)', color='#FF6B6B', alpha=0.7)
            
            ax.set_xlabel('Metric', fontsize=12)
            ax.set_ylabel('Value', fontsize=12)
            ax.set_title(f'{sector} Sector: Performance Metrics Comparison', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(metrics)
            ax.legend()
            ax.grid(alpha=0.3, axis='y')
            ax.axhline(y=0, color='black', linewidth=0.8)
            
            plt.tight_layout()
            out_bar = f"metrics_comparison_{sector.replace(' ', '_')}_{strategy}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(out_bar, dpi=200, bbox_inches='tight')
            plt.close()
            print(f"🖼️  Saved metrics comparison: {out_bar}")
            
        except Exception as e:
            print(f"⚠️ Could not save comparison charts: {e}")
            import traceback
            traceback.print_exc()
    
    def display_final_results(self, result):
        """Display final analysis results"""
        
        print("\n🎉 ANALYSIS COMPLETE!")
        print("=" * 60)
        
        if result.get('method') == 'stock_selection':
            # New stock selection format
            selected_stocks = result.get('selected_stocks', [])
            print(f"Selected Stocks: {len(selected_stocks)}")
            print(f"Consensus Reached: {'Yes' if result['consensus_reached'] else 'No'}")
            print(f"Selection Method: Agent Stock Picks")
            print(f"Conversation Length: {result['conversation_length']} messages")
            
            print(f"\n📋 Stock Selections:")
            agent_picks = result.get('agent_picks', {})
            for agent_name, data in agent_picks.items():
                picks_str = ", ".join(data['picks'])
                print(f"  {agent_name}: {picks_str}")
                print(f"    (Confidence: {data['confidence']:.2f})")
        else:
            # Old BUY/HOLD/SELL format (fallback)
            print(f"Final Recommendation: {result.get('final_recommendation', 'N/A')}")
            print(f"Consensus Reached: {'Yes' if result['consensus_reached'] else 'No'}")
            print(f"Consensus Method: {'Sophisticated Protocol' if result.get('sophisticated_consensus', False) else 'Simple Counting'}")
            print(f"Conversation Length: {result['conversation_length']} messages")
            
            if 'recommendations' in result:
                print(f"\n📈 Recommendation Breakdown:")
                for rec, count in result['recommendations'].items():
                    if count > 0:
                        print(f"  {rec}: {count}")
            
            if 'agent_positions' in result:
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
    print("\nAll data fetched from Yahoo Finance")
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
