#!/usr/bin/env python3
"""
Environment diagnostic and fix script for the red teaming toolkit
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd="/Users/admin/Documents/redteam-tools")
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed:")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def main():
    print("🚀 Fixing Red Team Toolkit Environment")
    print("=" * 50)
    
    # Check if we're in the right directory
    project_root = Path("/Users/admin/Documents/redteam-tools")
    if not project_root.exists():
        print(f"❌ Project directory {project_root} not found!")
        return
    
    # Navigate to project directory
    os.chdir(project_root)
    
    # Step 1: Activate virtual environment and reinstall dependencies
    print("\n📦 Fixing Python Environment")
    print("-" * 30)
    
    # Uninstall problematic packages
    run_command("source venv/bin/activate && pip uninstall -y flask openai", 
                "Removing corrupted packages")
    
    # Clear pip cache
    run_command("source venv/bin/activate && pip cache purge", 
                "Clearing pip cache")
    
    # Reinstall with specific versions
    run_command("source venv/bin/activate && pip install flask==3.0.0", 
                "Installing Flask 3.0.0")
    
    run_command("source venv/bin/activate && pip install openai==1.12.0", 
                "Installing OpenAI 1.12.0")
    
    # Install other dependencies
    run_command("source venv/bin/activate && pip install requests beautifulsoup4 python-dotenv", 
                "Installing additional dependencies")
    
    print("\n🧪 Testing imports...")
    print("-" * 30)
    
    # Test script
    test_script = '''
import sys
print(f"Python: {sys.version}")

try:
    from flask import Flask, render_template, request, jsonify
    print("✅ Flask imports successful")
    
    app = Flask(__name__)
    print("✅ Flask app creation successful")
except Exception as e:
    print(f"❌ Flask issue: {e}")

try:
    import openai
    print(f"✅ OpenAI version: {openai.__version__}")
except Exception as e:
    print(f"❌ OpenAI issue: {e}")

try:
    import requests
    print("✅ Requests imported")
except Exception as e:
    print(f"❌ Requests issue: {e}")
'''
    
    with open("test_imports.py", "w") as f:
        f.write(test_script)
    
    run_command("source venv/bin/activate && python test_imports.py", 
                "Testing Python imports")
    
    # Clean up
    if os.path.exists("test_imports.py"):
        os.remove("test_imports.py")
    
    print("\n🎯 Environment fix complete!")
    print("You can now run: python run.py")

if __name__ == "__main__":
    main()
