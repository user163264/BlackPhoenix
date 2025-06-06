#!/usr/bin/env python3

import sys
import subprocess
import os

def run_command(cmd, description):
    """Run a shell command and print the result."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd="/Users/admin/Documents/redteam-tools")
        print(f"   Output: {result.stdout.strip()}")
        if result.stderr:
            print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"   Exception: {e}")
        return False

def main():
    print("🚑 Emergency Flask & Dependencies Fix")
    print("=" * 50)
    
    # Activate virtual environment and fix Flask
    venv_python = "/Users/admin/Documents/redteam-tools/venv/bin/python3"
    venv_pip = "/Users/admin/Documents/redteam-tools/venv/bin/pip"
    
    # 1. Uninstall Flask completely
    run_command(f"{venv_pip} uninstall flask -y", "Uninstalling Flask")
    
    # 2. Clear pip cache
    run_command(f"{venv_pip} cache purge", "Clearing pip cache")
    
    # 3. Reinstall Flask from scratch
    run_command(f"{venv_pip} install --no-cache-dir Flask==3.0.0", "Installing Flask 3.0.0")
    
    # 4. Install other missing dependencies
    run_command(f"{venv_pip} install --no-cache-dir Flask-WTF==1.1.1", "Installing Flask-WTF")
    run_command(f"{venv_pip} install --no-cache-dir Werkzeug==3.0.1", "Installing Werkzeug")
    
    # 5. Verify Flask installation
    print("\n🧪 Testing Flask installation...")
    test_code = '''
import sys
sys.path.insert(0, "/Users/admin/Documents/redteam-tools")

try:
    import flask
    print(f"✅ Flask version: {flask.__version__}")
    
    from flask import Flask, render_template, request, jsonify
    print("✅ Flask imports successful")
    
    app = Flask(__name__)
    print("✅ Flask app creation successful")
    
except Exception as e:
    print(f"❌ Flask test failed: {e}")
    import traceback
    traceback.print_exc()

# Test OpenAI import
try:
    import openai
    print(f"✅ OpenAI version: {openai.__version__}")
    
    # Test the specific import that was failing
    client = openai.OpenAI(api_key="test-key")
    print("✅ OpenAI client creation successful")
    
except Exception as e:
    print(f"❌ OpenAI test failed: {e}")
    import traceback
    traceback.print_exc()
'''
    
    # Write test script
    with open("/Users/admin/Documents/redteam-tools/test_imports.py", "w") as f:
        f.write(test_code)
    
    # Run test
    run_command(f"{venv_python} test_imports.py", "Running import tests")
    
    print("\n🎯 Fix Summary:")
    print("- Completely reinstalled Flask")
    print("- Installed compatible versions")
    print("- Verified imports")
    print("\n🚀 Try running your app again with: python3 app.py")

if __name__ == "__main__":
    main()
