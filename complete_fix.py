#!/usr/bin/env python3
"""
Complete environment fix - reinstall everything from scratch
"""

import subprocess
import sys
import os
import shutil

def run_cmd(cmd, description, cwd=None):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        if result.returncode == 0:
            print(f"   ✅ Success")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"   ❌ Failed (code {result.returncode})")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    project_root = "/Users/admin/Documents/redteam-tools"
    venv_path = os.path.join(project_root, "venv")
    
    print("🚨 COMPLETE ENVIRONMENT REBUILD")
    print("=" * 50)
    
    # Step 1: Remove existing venv
    if os.path.exists(venv_path):
        print(f"🗑️  Removing existing virtual environment...")
        try:
            shutil.rmtree(venv_path)
            print("   ✅ Removed successfully")
        except Exception as e:
            print(f"   ❌ Error removing venv: {e}")
            return False
    
    # Step 2: Create new venv
    if not run_cmd("python3 -m venv venv", "Creating new virtual environment", project_root):
        return False
    
    # Step 3: Upgrade pip
    pip_path = os.path.join(venv_path, "bin", "pip")
    if not run_cmd(f"{pip_path} install --upgrade pip", "Upgrading pip", project_root):
        return False
    
    # Step 4: Install requirements
    requirements = [
        "Flask==3.0.0",
        "Flask-WTF==1.1.1", 
        "Werkzeug==3.0.1",
        "openai==1.79.0",
        "requests==2.32.3",
        "python-dotenv==1.1.0",
        "langdetect==1.0.9",
        "transformers==4.52.1",
        "tiktoken==0.9.0",
        "nltk==3.9.1",
        "pydantic==2.11.4"
    ]
    
    print("📦 Installing packages...")
    for package in requirements:
        if not run_cmd(f"{pip_path} install --no-cache-dir {package}", f"Installing {package}", project_root):
            print(f"   ⚠️  Warning: Failed to install {package}")
    
    # Step 5: Test installation
    python_path = os.path.join(venv_path, "bin", "python3")
    
    test_script = '''
import sys
sys.path.insert(0, "/Users/admin/Documents/redteam-tools")

try:
    import flask
    print(f"✅ Flask {flask.__version__}")
    
    from flask import Flask, render_template, request, jsonify
    app = Flask(__name__)
    print("✅ Flask app creation works")
    
    import openai
    print(f"✅ OpenAI {openai.__version__}")
    
    from config import Config
    print(f"✅ Config imported (port: {Config.PORT})")
    
    from modules.token_obfuscator import TokenObfuscator
    print("✅ TokenObfuscator imported")
    
    print("\\n🎉 ALL IMPORTS SUCCESSFUL!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
'''
    
    # Write and run test
    test_file = os.path.join(project_root, "test_final.py")
    with open(test_file, 'w') as f:
        f.write(test_script)
    
    print("🧪 Testing final installation...")
    run_cmd(f"{python_path} test_final.py", "Running final test", project_root)
    
    print("\n" + "=" * 50)
    print("🚀 Environment rebuild complete!")
    print("Run your app with: ./venv/bin/python3 app.py")

if __name__ == "__main__":
    main()
