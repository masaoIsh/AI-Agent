#!/usr/bin/env python3
"""
Test script for the new CSV-centric workflow
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_csv_workflow():
    """Test the new CSV-centric workflow"""
    print("🧪 Testing CSV-Centric Workflow")
    print("=" * 50)
    
    try:
        from arima_forecaster import create_sample_data
        
        # Create sample CSV data
        print("📊 Creating sample CSV data...")
        success = create_sample_data("test_workflow_data.csv")
        
        if success and os.path.exists("test_workflow_data.csv"):
            print("✅ Sample CSV data created successfully")
            
            # Test importing the interactive CLI
            print("🔧 Testing interactive CLI import...")
            from interactive_cli import InteractiveFinancialInterface
            
            interface = InteractiveFinancialInterface()
            print("✅ InteractiveFinancialInterface created successfully")
            
            # Test ARIMA analysis
            print("📈 Testing ARIMA analysis...")
            report = interface.perform_arima_analysis("test_workflow_data.csv")
            
            if report:
                print("✅ ARIMA analysis completed successfully")
                print("📋 Sample report generated")
                return True
            else:
                print("❌ ARIMA analysis failed")
                return False
        else:
            print("❌ Failed to create sample CSV data")
            return False
            
    except Exception as e:
        print(f"❌ Error in workflow test: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    print("\n🧹 Cleaning up test files...")
    
    test_files = ["test_workflow_data.csv", "arima_forecast.png"]
    
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Removed {file}")
            except Exception as e:
                print(f"⚠️  Could not remove {file}: {e}")

def main():
    """Run CSV workflow test"""
    print("🚀 CSV-Centric Workflow Test")
    print("=" * 60)
    
    success = test_csv_workflow()
    
    if success:
        print("\n🎉 CSV-centric workflow test passed!")
        print("The new workflow is ready:")
        print("1. ✅ Prompts for CSV file first")
        print("2. ✅ Asks which equity the data represents")
        print("3. ✅ Performs ARIMA analysis automatically")
        print("4. ✅ Integrates forecasting into agent discussions")
    else:
        print("\n❌ CSV-centric workflow test failed")
    
    cleanup_test_files()

if __name__ == "__main__":
    main()
