#!/bin/bash

echo "🚑 Emergency Flask Fix"
echo "===================="

cd /Users/admin/Documents/redteam-tools

# Activate virtual environment
source venv/bin/activate

echo "📦 Uninstalling Flask..."
pip uninstall flask -y

echo "🧹 Clearing pip cache..."
pip cache purge

echo "📥 Installing Flask 3.0.0..."
pip install --no-cache-dir Flask==3.0.0

echo "📥 Installing Flask-WTF..."
pip install --no-cache-dir Flask-WTF==1.1.1

echo "📥 Installing Werkzeug..."
pip install --no-cache-dir Werkzeug==3.0.1

echo "🧪 Testing imports..."
python3 -c "
import flask
print(f'✅ Flask version: {flask.__version__}')

from flask import Flask, render_template, request, jsonify
print('✅ Flask imports successful')

app = Flask(__name__)
print('✅ Flask app creation successful')

import openai
print(f'✅ OpenAI version: {openai.__version__}')
"

echo "✅ Flask fix complete!"
