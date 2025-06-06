#!/bin/bash

echo "🔧 Quick Flask Fix for AI Red Teaming Toolkit"
echo "============================================="

cd /Users/admin/Documents/redteam-tools

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Make sure you're in the right directory."
    exit 1
fi

# Check Python version
echo "🐍 Python version:"
python3 --version

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Check current Flask installation
echo "🔍 Checking current Flask installation..."
pip show flask

# Reinstall Flask and core dependencies
echo "🔄 Reinstalling Flask..."
pip uninstall flask -y
pip install flask==3.1.1

# Reinstall other critical dependencies
echo "📦 Reinstalling core dependencies..."
pip install werkzeug==3.1.3
pip install jinja2==3.1.6
pip install openai==1.79.0
pip install python-dotenv==1.1.0

# Test Flask import
echo "✅ Testing Flask import..."
python3 -c "
try:
    from flask import Flask, render_template, request, jsonify
    print('✅ Flask imports successful!')
    app = Flask(__name__)
    print('✅ Flask app creation successful!')
except Exception as e:
    print(f'❌ Flask import failed: {e}')
    exit(1)
"

# Test our modules
echo "🧪 Testing project modules..."
python3 -c "
import os
import sys
sys.path.insert(0, '.')

try:
    from config import Config
    print('✅ Config module imported')
    
    from modules.token_obfuscator import TokenObfuscator
    print('✅ TokenObfuscator module imported')
    
    print('🎉 All modules working correctly!')
except Exception as e:
    print(f'❌ Module import error: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "🚀 Fix complete! Try starting the app:"
echo "   ./start_app.sh"
echo ""
echo "If you still get errors, try:"
echo "   python3 app.py"
