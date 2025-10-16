#!/usr/bin/env python3
"""
Test script for ARIMA forecasting functionality
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_arima_imports():
    """Test if ARIMA dependencies can be imported"""
    print("🧪 Testing ARIMA dependencies...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ matplotlib import failed: {e}")
        return False
    
    try:
        from statsmodels.tsa.arima.model import ARIMA
        print("✅ statsmodels imported successfully")
    except ImportError as e:
        print(f"❌ statsmodels import failed: {e}")
        return False
    
    try:
        from arima_forecaster import ARIMAForecaster, create_sample_data
        print("✅ arima_forecaster imported successfully")
    except ImportError as e:
        print(f"❌ arima_forecaster import failed: {e}")
        return False
    
    return True

def test_sample_data_creation():
    """Test sample data creation"""
    print("\n📊 Testing sample data creation...")
    
    try:
        from arima_forecaster import create_sample_data
        
        success = create_sample_data("test_sample_data.csv")
        if success and os.path.exists("test_sample_data.csv"):
            print("✅ Sample data created successfully")
            return True
        else:
            print("❌ Sample data creation failed")
            return False
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def test_arima_forecasting():
    """Test ARIMA forecasting functionality"""
    print("\n🔮 Testing ARIMA forecasting...")
    
    try:
        from arima_forecaster import ARIMAForecaster
        
        # Create forecaster instance
        forecaster = ARIMAForecaster()
        
        # Load sample data
        if not forecaster.load_csv_data("test_sample_data.csv"):
            print("❌ Failed to load sample data")
            return False
        
        # Check stationarity
        forecaster.check_stationarity()
        
        # Make stationary if needed
        if not forecaster.diagnostics.get('is_stationary', False):
            forecaster.make_stationary()
        
        # Find optimal parameters
        forecaster.find_optimal_arima_params()
        
        # Fit model
        if not forecaster.fit_arima_model():
            print("❌ Failed to fit ARIMA model")
            return False
        
        # Generate forecast
        forecast_result = forecaster.forecast(periods=10)
        if not forecast_result:
            print("❌ Failed to generate forecast")
            return False
        
        # Generate report
        report = forecaster.generate_analysis_report()
        if report:
            print("✅ ARIMA forecasting test completed successfully")
            print("📊 Sample report generated")
            return True
        else:
            print("❌ Failed to generate analysis report")
            return False
            
    except Exception as e:
        print(f"❌ Error in ARIMA forecasting test: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    print("\n🧹 Cleaning up test files...")
    
    test_files = ["test_sample_data.csv", "arima_forecast.png"]
    
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Removed {file}")
            except Exception as e:
                print(f"⚠️  Could not remove {file}: {e}")

def main():
    """Run all ARIMA tests"""
    print("🚀 ARIMA Forecasting Functionality Test")
    print("=" * 60)
    
    tests = [
        ("Dependencies", test_arima_imports),
        ("Sample Data Creation", test_sample_data_creation),
        ("ARIMA Forecasting", test_arima_forecasting),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All ARIMA tests passed! The functionality is ready to use.")
        print("You can now use CSV files with the interactive CLI for ARIMA forecasting.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please install missing dependencies:")
        print("pip install pandas numpy matplotlib statsmodels seaborn")
    
    # Cleanup
    cleanup_test_files()

if __name__ == "__main__":
    main()



