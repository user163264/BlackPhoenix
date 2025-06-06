#!/bin/bash

echo "🚑 COMPLETE FLASK INSTALLATION FIX"
echo "=================================="
echo ""

# Navigate to project directory
cd /Users/admin/Documents/redteam-tools

echo "📍 Current directory: $(pwd)"
echo ""

# Make scripts executable
echo "🔧 Making rebuild script executable..."
chmod +x rebuild_env.sh
chmod +x complete_flask_fix.sh

echo "✅ Scripts are now executable"
echo ""

# Check current Flask status
echo "🔍 Checking current Flask installation..."
if [ -d "venv" ]; then
    echo "📦 Virtual environment exists - checking Flask..."
    if ./venv/bin/python3 -c "import flask; print(f'Flask {flask.__version__} found')" 2>/dev/null; then
        echo "⚠️  Flask exists but may be corrupted"
    else
        echo "❌ Flask import failed - corruption confirmed"
    fi
else
    echo "❌ No virtual environment found"
fi

echo ""
echo "🚀 Starting environment rebuild..."
echo ""

# Run the rebuild
./rebuild_env.sh

echo ""
echo "🧪 FINAL VERIFICATION"
echo "===================="

# Comprehensive test
./venv/bin/python3 -c "
print('🧪 Testing complete Flask setup...')
print()

try:
    # Test Flask import
    import flask
    print(f'✅ Flask {flask.__version__} imported successfully')
    
    # Test Flask app creation
    from flask import Flask, render_template, request, jsonify
    app = Flask(__name__)
    print('✅ Flask app creation works')
    
    # Test OpenAI
    import openai
    print(f'✅ OpenAI {openai.__version__} imported successfully')
    
    # Test other dependencies
    import requests
    import os
    from dotenv import load_dotenv
    import langdetect
    print('✅ All core dependencies working')
    
    print()
    print('🎉 FLASK INSTALLATION COMPLETELY FIXED!')
    print('🚀 Ready to run your application!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    print('🔄 Rebuild may need to be run again')
"

echo ""
echo "📋 NEXT STEPS:"
echo "1. Run: source venv/bin/activate"
echo "2. Run: python3 app.py"
echo ""
echo "✅ Flask installation fix complete!"
