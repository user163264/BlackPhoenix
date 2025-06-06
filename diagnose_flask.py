#!/usr/bin/env python3
"""
Minimal diagnostic script to identify the Flask import issue
"""

import sys
import os

print("🔍 Flask Import Diagnostic")
print("=" * 40)

# Add current directory to path
sys.path.insert(0, '.')

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")

# Test basic imports
print("\n📦 Testing basic imports...")

try:
    import flask
    print(f"✅ flask module found at: {flask.__file__}")
    print(f"   Flask version: {flask.__version__}")
except Exception as e:
    print(f"❌ Cannot import flask: {e}")

try:
    from flask import Flask
    print("✅ Flask class imported successfully")
except Exception as e:
    print(f"❌ Cannot import Flask class: {e}")

try:
    from flask import render_template, request, jsonify
    print("✅ Flask components imported successfully")
except Exception as e:
    print(f"❌ Cannot import Flask components: {e}")

# Test Flask app creation
print("\n🏗️  Testing Flask app creation...")
try:
    from flask import Flask
    app = Flask(__name__)
    print("✅ Flask app created successfully")
except Exception as e:
    print(f"❌ Cannot create Flask app: {e}")

# Test our project imports
print("\n🧪 Testing project imports...")

try:
    from config import Config
    print("✅ Config imported")
    print(f"   Default model: {Config.DEFAULT_MODEL}")
    print(f"   Port: {Config.PORT}")
except Exception as e:
    print(f"❌ Cannot import Config: {e}")

try:
    from modules.token_obfuscator import TokenObfuscator
    print("✅ TokenObfuscator imported")
except Exception as e:
    print(f"❌ Cannot import TokenObfuscator: {e}")

print("\n" + "=" * 40)
print("Diagnostic complete!")
