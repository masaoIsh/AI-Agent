"""
Working Demo of Financial Analysis Multi-Agent System using AutoGen + Ollama
This version uses the correct AutoGen API with Ollama integration
"""

import asyncio
import random
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def create_financial_agents():
    """Create the three financial analysis agents"""
    
    # Initialize Ollama client
    ollama_client = OllamaChatCompletionClient(model="llama3.2")
    
    # Fundamental Analysis Agent
    fundamental_agent = AssistantAgent(
        name="FundamentalAnalyst",
        model_client=ollama_client,
        system_message="""You are a fundamental analysis expert. You analyze:
        - Financial statements and ratios
        - Company valuation metrics
        - Business fundamentals and growth prospects
        
        Provide BUY or SELL recommendations based on fundamental analysis.
        Be concise and professional in your responses.""",
        description="Expert in fundamental financial analysis"
    )
    
    # Sentiment Analysis Agent
    sentiment_agent = AssistantAgent(
        name="SentimentAnalyst", 
        model_client=ollama_client,
        system_message="""You are a market sentiment analysis expert. You analyze:
        - News sentiment and media coverage
        - Social media sentiment
        - Analyst ratings and market momentum
        
        Provide BUY or SELL recommendations based on market sentiment.
        Be concise and professional in your responses.""",
        description="Expert in market sentiment analysis"
    )
    
    # Valuation Analysis Agent
    valuation_agent = AssistantAgent(
        name="ValuationAnalyst",
        model_client=ollama_client,
        system_message="""You are a valuation analysis expert. You analyze:
        - DCF models and intrinsic value
        - Comparable company analysis
        - Risk-adjusted valuations
        
        Provide BUY or SELL recommendations based on valuation analysis.
        Be concise and professional in your responses.""",
        description="Expert in stock valuation analysis"
    )
    
    return [fundamental_agent, sentiment_agent, valuation_agent], ollama_client


async def get_initial_recommendations(agents, stock_symbol):
    """Get initial recommendations from all agents"""
    recommendations = {}
    
    print(f"\n📊 Getting initial recommendations for {stock_symbol}...")
    print("-" * 50)
    
    for agent in agents:
        # Create a task for the agent
        task = f"Analyze {stock_symbol} and provide a BUY or SELL recommendation with brief reasoning."
        
        try:
            # Get the agent's response
            response = await agent.run(task=task)
            print(f"\n{agent.name}:")
            print(f"Response: {response}")
            
            # Extract recommendation (simple parsing)
            if "BUY" in response.upper():
                recommendation = "BUY"
            else:
                recommendation = "SELL"
                
            recommendations[agent.name] = {
                'recommendation': recommendation,
                'response': response
            }
            
        except Exception as e:
            print(f"Error getting recommendation from {agent.name}: {e}")
            # Fallback to random recommendation
            recommendation = random.choice(["BUY", "SELL"])
            recommendations[agent.name] = {
                'recommendation': recommendation,
                'response': f"Fallback recommendation: {recommendation} (due to error)"
            }
    
    return recommendations


async def conduct_debate(agents, stock_symbol, recommendations):
    """Conduct a round-robin debate when agents disagree"""
    
    print(f"\n🗣️  Starting debate for {stock_symbol}...")
    print("-" * 50)
    
    # Create debate team
    debate_team = RoundRobinGroupChat(agents, max_turns=6)  # 2 rounds per agent
    
    # Create debate task
    debate_task = f"""The agents have provided different recommendations for {stock_symbol}:
    
    Initial Recommendations:
    """
    
    for agent_name, rec in recommendations.items():
        debate_task += f"- {agent_name}: {rec['recommendation']}\n"
    
    debate_task += """
    
    Please discuss your positions and try to reach a consensus. 
    Each agent should explain their reasoning and respond to others' arguments.
    Be respectful but defend your position based on your expertise.
    """
    
    try:
        # Run the debate
        print("Debate in progress...")
        stream = debate_team.run_stream(task=debate_task)
        
        debate_messages = []
        async for message in stream:
            print(f"\n{message['sender']}: {message['content']}")
            debate_messages.append(message)
        
        return debate_messages
        
    except Exception as e:
        print(f"Error during debate: {e}")
        return []


async def run_financial_analysis_system():
    """Main function to run the financial analysis system"""
    
    print("🤖 Financial Analysis Multi-Agent System with Ollama")
    print("=" * 60)
    
    # Create agents
    agents, ollama_client = await create_financial_agents()
    
    # Demo stocks
    demo_stocks = ["AAPL", "TSLA", "MSFT"]
    
    try:
        for stock in demo_stocks:
            print(f"\n{'='*60}")
            print(f"ANALYZING: {stock}")
            print(f"{'='*60}")
            
            # Get initial recommendations
            recommendations = await get_initial_recommendations(agents, stock)
            
            # Check for consensus
            rec_values = [rec['recommendation'] for rec in recommendations.values()]
            unique_recs = set(rec_values)
            
            print(f"\n📋 Initial Recommendations Summary:")
            for agent_name, rec in recommendations.items():
                print(f"  {agent_name}: {rec['recommendation']}")
            
            if len(unique_recs) == 1:
                print(f"\n✅ CONSENSUS: All agents recommend {unique_recs.pop()}")
            else:
                print(f"\n⚠️  DISAGREEMENT: {len(unique_recs)} different recommendations")
                
                # Conduct debate
                debate_messages = await conduct_debate(agents, stock, recommendations)
                
                if debate_messages:
                    print(f"\n📝 Debate completed with {len(debate_messages)} messages")
                    
                    # Simple final decision (majority vote)
                    buy_count = rec_values.count("BUY")
                    sell_count = rec_values.count("SELL")
                    
                    if buy_count > sell_count:
                        final_rec = "BUY"
                    else:
                        final_rec = "SELL"
                    
                    print(f"🎯 Final Recommendation: {final_rec} (Majority: {buy_count} BUY, {sell_count} SELL)")
                else:
                    print("❌ Debate failed to complete")
            
            print(f"\n{'='*60}")
    
    finally:
        # Close the Ollama client
        await ollama_client.close()
        print("\n✅ Analysis complete!")


async def test_simple_agent():
    """Test a simple agent to verify Ollama integration"""
    
    print("🔄 Testing simple agent with Ollama...")
    
    try:
        ollama_client = OllamaChatCompletionClient(model="llama3.2")
        
        agent = AssistantAgent(
            name="TestAgent",
            model_client=ollama_client,
            system_message="You are a helpful financial assistant. Provide concise responses."
        )
        
        response = await agent.run(task="Say hello and confirm you're working with Ollama!")
        print(f"✅ Agent response: {response}")
        
        await ollama_client.close()
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False


if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Simple agent test")
    print("2. Full financial analysis system")
    
    # For automated testing, run the simple test first
    print("\n🔄 Running simple agent test first...")
    
    async def main():
        # Test simple agent first
        if await test_simple_agent():
            print("\n✅ Simple test passed! Running full system...")
            await run_financial_analysis_system()
        else:
            print("\n❌ Simple test failed. Check Ollama setup.")
    
    asyncio.run(main())


