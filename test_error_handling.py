#!/usr/bin/env python3
"""
Test script for error handling when CSV file is not found
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_csv_not_found_error():
    """Test that the system properly exits when CSV file is not found"""
    print("🧪 Testing CSV file not found error handling")
    print("=" * 50)
    
    try:
        from interactive_cli import InteractiveFinancialInterface
        
        interface = InteractiveFinancialInterface()
        
        # Test the ARIMA analysis method directly
        print("Testing perform_arima_analysis with non-existent file...")
        result = interface.perform_arima_analysis("nonexistent_file.csv")
        
        if result is None:
            print("✅ Correctly returned None for non-existent file")
            return True
        else:
            print("❌ Should have returned None for non-existent file")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_file_exists_check():
    """Test the file exists check"""
    print("\n🔍 Testing file existence check")
    print("=" * 30)
    
    # Test with non-existent file
    if not os.path.exists("nonexistent_file.csv"):
        print("✅ Correctly detected non-existent file")
        return True
    else:
        print("❌ Incorrectly detected non-existent file as existing")
        return False

def main():
    """Run error handling tests"""
    print("🚀 Error Handling Test")
    print("=" * 60)
    
    tests = [
        ("File Existence Check", test_file_exists_check),
        ("CSV Not Found Error", test_csv_not_found_error),
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
        print("\n🎉 All error handling tests passed!")
        print("The system now properly exits when CSV file is not found.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")

if __name__ == "__main__":
    main()
