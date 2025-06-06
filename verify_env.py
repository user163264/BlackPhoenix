#!/usr/bin/env python3
"""
Simple test to verify environment after rebuild
"""
import sys
import os

# Add project to path
sys.path.insert(0, '/Users/admin/Documents/redteam-tools')

print("🧪 POST-REBUILD VERIFICATION")
print("=" * 40)

# Test 1: Flask
try:
    import flask
    print(f"✅ Flask {flask.__version__}")
    
    from flask import Flask, render_template, request, jsonify
    app = Flask(__name__)
    print("✅ Flask app creation successful")
except Exception as e:
    print(f"❌ Flask failed: {e}")

# Test 2: OpenAI
try:
    import openai
    print(f"✅ OpenAI {openai.__version__}")
    
    # Test client creation
    client = openai.OpenAI(api_key="test-key")
    print("✅ OpenAI client creation successful")
except Exception as e:
    print(f"❌ OpenAI failed: {e}")

# Test 3: Config
try:
    from config import Config
    print(f"✅ Config imported (model: {Config.DEFAULT_MODEL}, port: {Config.PORT})")
except Exception as e:
    print(f"❌ Config failed: {e}")

# Test 4: Token Obfuscator
try:
    from modules.token_obfuscator import TokenObfuscator
    obfuscator = TokenObfuscator()
    print("✅ TokenObfuscator imported and created")
except Exception as e:
    print(f"❌ TokenObfuscator failed: {e}")

# Test 5: App creation
try:
    from app import app
    print("✅ Main app imported successfully")
except Exception as e:
    print(f"❌ Main app failed: {e}")

print("\n" + "=" * 40)
print("Verification complete!")
