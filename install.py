#!/usr/bin/env python3
"""
Installation script for Market Summary Generator
This script helps set up the system and verify the installation
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def check_imports():
    """Check if all required modules can be imported"""
    required_modules = [
        "crewai",
        "litellm", 
        "tavily",
        "telegram",
        "reportlab",
        "matplotlib",
        "yfinance",
        "pandas",
        "requests",
        "python_dotenv"
    ]
    
    print("🔍 Checking module imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            if module == "python_dotenv":
                importlib.import_module("dotenv")
            else:
                importlib.import_module(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All modules imported successfully")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["outputs", "temp_images", "logs"]
    
    print("📁 Creating directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    try:
        with open("env_example.txt", "r") as f:
            content = f.read()
        
        with open(".env", "w") as f:
            f.write(content)
        
        print("✅ .env file created from template")
        print("⚠️  Please edit .env file with your API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def run_demo():
    """Run the demo to verify everything works"""
    print("🚀 Running demo...")
    try:
        subprocess.check_call([sys.executable, "demo.py"])
        print("✅ Demo completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed: {e}")
        return False

def main():
    """Main installation process"""
    print("🚀 Market Summary Generator - Installation")
    print("=" * 50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing requirements", install_requirements),
        ("Checking imports", check_imports),
        ("Creating directories", create_directories),
        ("Creating .env file", create_env_file),
        ("Running demo", run_demo)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            failed_steps.append(step_name)
    
    print("\n" + "=" * 50)
    
    if failed_steps:
        print("❌ Installation completed with errors:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\n🔧 Please fix the errors above and run the installation again")
        return 1
    else:
        print("✅ Installation completed successfully!")
        print("\n🎉 Next steps:")
        print("   1. Edit .env file with your API keys")
        print("   2. Test configuration: python run_market_summary.py --mode test")
        print("   3. Run first summary: python run_market_summary.py --mode once --force")
        print("   4. Schedule daily runs: python run_market_summary.py --mode schedule")
        return 0

if __name__ == "__main__":
    exit(main())
