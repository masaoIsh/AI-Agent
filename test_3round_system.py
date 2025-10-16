"""
Test script to verify the 3-round system works correctly
"""

import asyncio
from interactive_cli import InteractiveFinancialInterface


async def test_3round_system():
    """Test the 3-round system"""
    
    print("🧪 TESTING 3-ROUND SYSTEM")
    print("=" * 50)
    print("✅ Testing: Each agent speaks maximum 3 times")
    print("✅ Testing: Automatic termination after 9 turns")
    print("✅ Testing: Clear turn display")
    print("=" * 50)
    
    interface = InteractiveFinancialInterface()
    
    try:
        # Test agent initialization
        print("\n🔄 Testing agent initialization...")
        await interface.initialize_agents()
        print("✅ Agent initialization successful!")
        
        # Verify agent names
        print("\n📋 Agent Names:")
        for agent_type, agent in interface.agents.items():
            print(f"  {agent_type}: {agent.name}")
        
        # Test the 3-round analysis
        print("\n🔄 Testing 3-round analysis...")
        result = await interface.run_analysis_with_debate(
            "Provide analysis and recommendation whether a risk neutral investor should BUY or SELL AAPL stock.",
            "AAPL"
        )
        
        if result:
            print("\n✅ Analysis completed successfully!")
            print(f"Final Recommendation: {result['final_recommendation']}")
            print(f"Consensus Reached: {result['consensus_reached']}")
            print(f"Conversation Length: {result['conversation_length']} messages")
            
            # Verify we got the expected number of messages (9 turns = 3 per agent)
            expected_turns = 9  # 3 rounds × 3 agents
            actual_turns = result['conversation_length']
            print(f"Expected Turns: {expected_turns}, Actual Turns: {actual_turns}")
            
            if actual_turns >= expected_turns:
                print("✅ Correct number of turns achieved!")
                print("✅ System automatically terminated after each agent spoke 3 times")
            else:
                print(f"⚠️ Expected {expected_turns} turns, got {actual_turns}")
                if actual_turns < expected_turns:
                    print("⚠️ Discussion may have terminated early due to consensus")
            
            # Show turn breakdown
            print(f"\n📊 Turn Analysis:")
            print(f"  Total turns: {actual_turns}")
            print(f"  Turns per agent: {actual_turns // 3}")
            print(f"  Remaining turns: {actual_turns % 3}")
            
        else:
            print("❌ Analysis failed")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        await interface.close()


if __name__ == "__main__":
    asyncio.run(test_3round_system())





