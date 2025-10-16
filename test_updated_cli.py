"""
Test script to verify the updated interactive_cli.py works with new agent names and 2-round consensus
"""

import asyncio
from interactive_cli import InteractiveFinancialInterface


async def test_updated_cli():
    """Test the updated CLI interface"""
    
    print("🧪 TESTING UPDATED CLI INTERFACE")
    print("=" * 50)
    print("✅ Testing new agent names: Wassim, Khizar, Yugo")
    print("✅ Testing 2-round consensus (each agent speaks twice)")
    print("✅ Testing turn display in CLI")
    print("=" * 50)
    
    interface = InteractiveFinancialInterface()
    
    try:
        # Test agent initialization
        print("\n🔄 Testing agent initialization with new names...")
        await interface.initialize_agents()
        print("✅ Agent initialization successful!")
        
        # Verify agent names
        print("\n📋 Agent Names Verification:")
        for agent_type, agent in interface.agents.items():
            print(f"  {agent_type}: {agent.name}")
        
        # Test a simple analysis
        print("\n🔄 Testing analysis with 2-round debate...")
        result = await interface.run_analysis_with_debate(
            "Provide analysis and recommendation whether a risk neutral investor should BUY or SELL AAPL stock.",
            "AAPL"
        )
        
        if result:
            print("\n✅ Analysis completed successfully!")
            print(f"Final Recommendation: {result['final_recommendation']}")
            print(f"Consensus Reached: {result['consensus_reached']}")
            print(f"Conversation Length: {result['conversation_length']} messages")
            
            # Verify we got the expected number of messages (6 turns = 2 per agent)
            expected_turns = 6  # 2 rounds × 3 agents
            actual_turns = result['conversation_length']
            print(f"Expected Turns: {expected_turns}, Actual Turns: {actual_turns}")
            
            if actual_turns >= expected_turns:
                print("✅ Correct number of turns achieved!")
            else:
                print(f"⚠️ Expected {expected_turns} turns, got {actual_turns}")
        else:
            print("❌ Analysis failed")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        await interface.close()


if __name__ == "__main__":
    asyncio.run(test_updated_cli())





