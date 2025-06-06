import sys
import os

# Add project path
sys.path.insert(0, '/Users/admin/Documents/redteam-tools')

print("=== DIAGNOSTIC RESULTS ===")

# Test 1: Check Flask directory
try:
    flask_dir = "/Users/admin/Documents/redteam-tools/venv/lib/python3.13/site-packages/flask"
    if os.path.exists(flask_dir):
        print(f"✅ Flask directory exists: {flask_dir}")
        
        # Check __init__.py
        init_file = os.path.join(flask_dir, "__init__.py")
        if os.path.exists(init_file):
            with open(init_file, 'r') as f:
                content = f.read()
                if content.strip():
                    print(f"✅ __init__.py has content ({len(content)} chars)")
                    print(f"   First 200 chars: {content[:200]}")
                else:
                    print("❌ __init__.py is empty!")
        else:
            print("❌ __init__.py missing!")
    else:
        print("❌ Flask directory missing!")
except Exception as e:
    print(f"❌ Error checking Flask directory: {e}")

# Test 2: Try basic import
try:
    import flask
    print(f"✅ Flask imported, version: {getattr(flask, '__version__', 'unknown')}")
except Exception as e:
    print(f"❌ Flask import failed: {e}")

# Test 3: Try Flask class import
try:
    from flask import Flask
    app = Flask(__name__)
    print("✅ Flask app creation successful")
except Exception as e:
    print(f"❌ Flask class import failed: {e}")

# Test 4: Check OpenAI
try:
    import openai
    print(f"✅ OpenAI imported, version: {openai.__version__}")
except Exception as e:
    print(f"❌ OpenAI import failed: {e}")

print("=== END DIAGNOSTIC ===")
