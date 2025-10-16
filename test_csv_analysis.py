"""
Test script for CSV analysis functionality
"""

import asyncio
import pandas as pd
from interactive_cli import InteractiveFinancialInterface

async def test_csv_analysis():
    """Test the CSV analysis functionality"""
    
    print("🧪 Testing CSV Analysis Functionality")
    print("=" * 50)
    
    # Create interface
    interface = InteractiveFinancialInterface()
    
    # Test data summary creation
    print("📊 Testing data summary creation...")
    
    # Load sample CSV
    df = pd.read_csv('sample_stock_data.csv')
    print(f"✅ Loaded sample CSV: {len(df)} rows, {len(df.columns)} columns")
    
    # Test data summary
    summary = interface.create_data_summary(df)
    print("✅ Data summary created successfully")
    print("\n📋 Sample Data Summary:")
    print(summary[:500] + "..." if len(summary) > 500 else summary)
    
    print("\n🎉 CSV analysis functionality test completed!")
    print("\nTo use CSV analysis:")
    print("1. Run: python interactive_cli.py")
    print("2. Choose option 2 for CSV File Analysis")
    print("3. Enter path to your CSV file")
    print("4. Watch the agents analyze your data!")

if __name__ == "__main__":
    asyncio.run(test_csv_analysis())



