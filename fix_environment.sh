#!/bin/bash

echo "🔧 Fixing Flask Installation and Python Environment..."

cd /Users/admin/Documents/redteam-tools

# Deactivate any active virtual environment
deactivate 2>/dev/null || true

# Remove the corrupted virtual environment
echo "📁 Removing corrupted virtual environment..."
rm -rf venv

# Create a fresh virtual environment
echo "🆕 Creating fresh virtual environment..."
python3 -m venv venv

# Activate the new virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip first
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Verify Flask installation
echo "✅ Verifying Flask installation..."
python -c "from flask import Flask; print('Flask imported successfully')"

# Test our app imports
echo "🧪 Testing app imports..."
python -c "
import sys
sys.path.insert(0, '.')
try:
    from config import Config
    print('✅ Config imported successfully')
    from modules.token_obfuscator import TokenObfuscator
    print('✅ TokenObfuscator imported successfully')
    from flask import Flask, render_template, request, jsonify
    print('✅ Flask imports successful')
    print('🎉 All imports working correctly!')
except Exception as e:
    print(f'❌ Import error: {e}')
    import traceback
    traceback.print_exc()
"

echo "🚀 Environment setup complete! Try running the app again:"
echo "   ./start_app.sh"
