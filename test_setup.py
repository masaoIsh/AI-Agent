#!/usr/bin/env python3
"""
Test script to verify the AI Financial Analysis Multi-Agent System setup
"""

import sys
import subprocess
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import autogen_agentchat
        print("✅ autogen_agentchat imported successfully")
    except ImportError as e:
        print(f"❌ autogen_agentchat import failed: {e}")
        return False
    
    try:
        import autogen_ext
        print("✅ autogen_ext imported successfully")
    except ImportError as e:
        print(f"❌ autogen_ext import failed: {e}")
        return False
    
    try:
        import ollama
        print("✅ ollama imported successfully")
    except ImportError as e:
        print(f"❌ ollama import failed: {e}")
        return False
    
    return True

def test_ollama_connection():
    """Test if Ollama is accessible"""
    print("🤖 Testing Ollama connection...")
    
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ollama is accessible")
            return True
        else:
            print(f"❌ Ollama command failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Ollama command timed out")
        return False
    except FileNotFoundError:
        print("❌ Ollama command not found. Please install Ollama first.")
        return False

def test_llama_model():
    """Test if llama3.2 model is available"""
    print("📥 Testing if llama3.2 model is available...")
    
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and "llama3.2" in result.stdout:
            print("✅ llama3.2 model is available")
            return True
        else:
            print("❌ llama3.2 model not found. Run: ollama pull llama3.2")
            return False
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

def test_main_script():
    """Test if the main script can be imported"""
    print("📄 Testing main script import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, str(Path(__file__).parent))
        import interactive_cli
        print("✅ interactive_cli.py imported successfully")
        return True
    except ImportError as e:
        print(f"❌ interactive_cli.py import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Financial Analysis Multi-Agent System - Setup Test")
    print("=" * 60)
    
    tests = [
        ("Python Imports", test_imports),
        ("Ollama Connection", test_ollama_connection),
        ("Llama Model", test_llama_model),
        ("Main Script", test_main_script),
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
        print("\n🎉 All tests passed! The system is ready to use.")
        print("Run: python interactive_cli.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the setup.")
        print("See README.md for troubleshooting steps.")

if __name__ == "__main__":
    main()



