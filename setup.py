#!/usr/bin/env python3
"""
Setup script for AI Financial Analysis Multi-Agent System
Automates the installation and setup process
"""

import subprocess
import sys
import platform
import os
from pathlib import Path

def run_command(command, description, check=True):
    """Run a shell command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} completed")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False
    return True

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python 3.10+ required, but found {version.major}.{version.minor}")
        print("Please install Python 3.10 or higher")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_ollama():
    """Check if Ollama is installed and running"""
    print("🤖 Checking Ollama installation...")
    
    # Check if ollama command exists
    if not run_command("which ollama", "Checking if Ollama is installed", check=False):
        print("❌ Ollama not found. Please install Ollama first:")
        print("  macOS: brew install ollama")
        print("  Linux: curl -fsSL https://ollama.ai/install.sh | sh")
        print("  Windows: Download from https://ollama.ai/download")
        return False
    
    # Check if Ollama service is running
    if not run_command("ollama list", "Checking if Ollama service is running", check=False):
        print("❌ Ollama service not running. Starting Ollama...")
        system = platform.system().lower()
        if system == "darwin":  # macOS
            run_command("brew services start ollama", "Starting Ollama service", check=False)
        else:
            print("Please start Ollama manually: ollama serve")
            return False
    
    print("✅ Ollama is installed and running")
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        return False
    print("✅ Python dependencies installed")
    return True

def download_llama_model():
    """Download the required Llama model"""
    print("📥 Downloading Llama3.2 model (this may take a while)...")
    if not run_command("ollama pull llama3.2", "Downloading Llama3.2 model"):
        print("❌ Failed to download Llama3.2 model")
        print("You can try downloading it manually: ollama pull llama3.2")
        return False
    print("✅ Llama3.2 model downloaded")
    return True

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    
    # Test if we can import the required modules
    try:
        import autogen_agentchat
        import autogen_ext
        import ollama
        print("✅ All required modules can be imported")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test if we can list Ollama models
    if not run_command("ollama list | grep llama3.2", "Checking if llama3.2 model is available", check=False):
        print("❌ Llama3.2 model not found in Ollama")
        return False
    
    print("✅ Installation test passed")
    return True

def main():
    """Main setup function"""
    print("🚀 AI Financial Analysis Multi-Agent System Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check Ollama
    if not check_ollama():
        sys.exit(1)
    
    # Install Python dependencies
    if not install_python_dependencies():
        sys.exit(1)
    
    # Download Llama model
    if not download_llama_model():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 60)
    print("You can now run the system with:")
    print("  python interactive_cli.py")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
