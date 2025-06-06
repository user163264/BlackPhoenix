#!/bin/bash

echo "🚨 COMPLETE ENVIRONMENT REBUILD"
echo "================================"

cd /Users/admin/Documents/redteam-tools

# Remove old venv
echo "🗑️  Removing old virtual environment..."
rm -rf venv

# Create new venv
echo "🏗️  Creating new virtual environment..."
python3 -m venv venv

# Activate and upgrade pip
echo "📦 Upgrading pip..."
./venv/bin/pip install --upgrade pip

# Install core packages
echo "📦 Installing Flask..."
./venv/bin/pip install --no-cache-dir Flask==3.0.0

echo "📦 Installing Flask-WTF..."
./venv/bin/pip install --no-cache-dir Flask-WTF==1.1.1

echo "📦 Installing Werkzeug..."
./venv/bin/pip install --no-cache-dir Werkzeug==3.0.1

echo "📦 Installing OpenAI..."
./venv/bin/pip install --no-cache-dir openai==1.79.0

echo "📦 Installing other dependencies..."
./venv/bin/pip install --no-cache-dir requests==2.32.3
./venv/bin/pip install --no-cache-dir python-dotenv==1.1.0
./venv/bin/pip install --no-cache-dir langdetect==1.0.9
./venv/bin/pip install --no-cache-dir transformers==4.52.1
./venv/bin/pip install --no-cache-dir tiktoken==0.9.0
./venv/bin/pip install --no-cache-dir nltk==3.9.1
./venv/bin/pip install --no-cache-dir pydantic==2.11.4

# Test the installation
echo "🧪 Testing installation..."
./venv/bin/python3 -c "
import flask
print(f'✅ Flask {flask.__version__}')

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
print('✅ Flask app creation works')

import openai
print(f'✅ OpenAI {openai.__version__}')

print('🎉 Core imports successful!')
"

echo ""
echo "✅ Environment rebuild complete!"
echo "🚀 Try running: ./venv/bin/python3 app.py"
