"""
Test script to verify the CLI interface fix works
"""

import asyncio
from interactive_cli import InteractiveFinancialInterface


async def test_cli_fix():
    """Test that the CLI interface works without the name error"""
    
    print("🧪 TESTING CLI INTERFACE FIX")
    print("=" * 50)
    
    interface = InteractiveFinancialInterface()
    
    try:
        # Test agent initialization
        print("🔄 Testing agent initialization...")
        await interface.initialize_agents()
        print("✅ Agent initialization successful!")
        
        # Test a simple analysis
        print("\n🔄 Testing analysis with debate...")
        result = await interface.run_analysis_with_debate(
            "Provide analysis and recommendation whether a risk neutral investor should BUY or SELL AAPL stock.",
            "AAPL"
        )
        
        if result:
            print("✅ Analysis completed successfully!")
            print(f"Final Recommendation: {result['final_recommendation']}")
            print(f"Consensus Reached: {result['consensus_reached']}")
        else:
            print("❌ Analysis failed")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if "agent name must be a valid Python identifier" in str(e):
            print("🔧 The agent name error is still present - need to fix further")
        else:
            print("🔧 Different error - agent names are fixed")
    
    finally:
        await interface.close()


if __name__ == "__main__":
    asyncio.run(test_cli_fix())





