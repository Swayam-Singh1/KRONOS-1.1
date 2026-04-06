#!/usr/bin/env python3
"""
Run Enhanced Training - Simple script to run comprehensive training
"""

import sys
import os
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if API server is running
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print("❌ API server not responding")
            return False
    except Exception as e:
        print(f"❌ API server not available: {e}")
        return False

def start_api_server():
    """Start API server if not running"""
    print("🚀 Starting API server...")
    try:
        # Start API server in background
        subprocess.Popen([
            sys.executable, 
            "backend/api_server.py"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for server to start
        print("⏳ Waiting for API server to start...")
        time.sleep(10)
        
        # Check if server is now running
        if check_requirements():
            print("✅ API server started successfully")
            return True
        else:
            print("❌ Failed to start API server")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return False

def run_enhanced_training():
    """Run enhanced training"""
    print("🛡️ Starting Enhanced Training")
    print("=" * 50)
    
    try:
        # Run enhanced training
        result = subprocess.run([
            sys.executable, 
            "backend/train_from_scratch.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Enhanced training completed successfully!")
            print(result.stdout)
            return True
        else:
            print("❌ Enhanced training failed!")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Enhanced training failed: {e}")
        return False

def main():
    """Main function"""
    print("🛡️ Enhanced Training Runner")
    print("Self-Morphing AI Cybersecurity Engine")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("backend").exists():
        print("❌ Please run this script from the project root directory")
        return
    
    # Check requirements
    if not check_requirements():
        print("\n🚀 Starting API server...")
        if not start_api_server():
            print("❌ Cannot start API server. Please start manually:")
            print("   python backend/api_server.py")
            return
    
    # Run enhanced training
    print("\n🚀 Starting comprehensive training...")
    if run_enhanced_training():
        print("\n✅ Training completed successfully!")
        print("🎯 The system is now ready for cybersecurity operations.")
        print("🛡️ All engines have been trained with comprehensive synthetic data.")
    else:
        print("\n❌ Training failed. Please check the logs for details.")

if __name__ == "__main__":
    main()





