"""
Main script for Financial Analysis Multi-Agent Debate System
Run this to start the financial analysis and debate process
"""

import asyncio
import argparse
from autogen_ext.models.ollama import OllamaChatCompletionClient
from debate_orchestrator import DebateOrchestrator


async def main():
    """Main function to run the financial analysis debate system"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Financial Analysis Multi-Agent Debate System')
    parser.add_argument('--stock', '-s', default='AAPL', help='Stock symbol to analyze (default: AAPL)')
    parser.add_argument('--rounds', '-r', type=int, default=3, help='Maximum debate rounds (default: 3)')
    parser.add_argument('--model', '-m', default='llama3.2', help='Ollama model to use (default: llama3.2)')
    
    args = parser.parse_args()
    
    print("🤖 Financial Analysis Multi-Agent Debate System")
    print("=" * 50)
    print(f"Stock Symbol: {args.stock}")
    print(f"Max Debate Rounds: {args.rounds}")
    print(f"Model: {args.model}")
    print("=" * 50)
    
    try:
        # Initialize Ollama model client
        print(f"\n🔄 Initializing {args.model} model...")
        model_client = OllamaChatCompletionClient(model=args.model)
        
        # Initialize debate orchestrator
        print("🔄 Setting up debate orchestrator...")
        orchestrator = DebateOrchestrator(model_client)
        
        # Run the analysis and debate
        print(f"\n🚀 Starting analysis and debate for {args.stock}...")
        result = await orchestrator.analyze_stock_with_debate(args.stock, args.rounds)
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        
        print(f"\nStock Symbol: {result['stock_symbol']}")
        print(f"Consensus Reached: {'Yes' if result['consensus'] else 'No'}")
        print(f"Final Recommendation: {result['final_recommendation']}")
        
        if not result['consensus']:
            print(f"Debate Rounds: {result['debate_rounds']}")
            
            print(f"\n📝 Debate Summary:")
            print(result.get('debate_summary', 'No summary available'))
        
        print(f"\n📈 Initial Analyses:")
        for agent_name, analysis in result['initial_analyses'].items():
            print(f"\n{agent_name.upper()}:")
            print(f"Recommendation: {analysis['recommendation']}")
            print(f"Analysis: {analysis['analysis'][:200]}...")
        
        # Close the model client
        await model_client.close()
        
        print(f"\n✅ Analysis complete! Final recommendation: {result['final_recommendation']}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure Ollama is running and the model is available.")
        print("Try: ollama list")


def print_usage_examples():
    """Print usage examples"""
    print("\n📖 Usage Examples:")
    print("python main.py                           # Analyze AAPL with default settings")
    print("python main.py --stock TSLA              # Analyze Tesla")
    print("python main.py --stock MSFT --rounds 5   # Analyze Microsoft with 5 debate rounds")
    print("python main.py --stock GOOGL --model llama3.2  # Use specific model")


if __name__ == "__main__":
    # Check if help is requested
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print_usage_examples()
    
    # Run the main function
    asyncio.run(main())


