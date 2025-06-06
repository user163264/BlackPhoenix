#!/bin/bash

echo "🔧 Quick Fix - AI Red Team Toolkit (No tiktoken)"
echo "================================================"

# Set the working directory
cd "$(dirname "$0")"

# Remove the problematic virtual environment
echo "📦 Removing old virtual environment..."
rm -rf venv

# Create a new virtual environment
echo "🐍 Creating new virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip first
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies without tiktoken
echo "📚 Installing dependencies (without tiktoken)..."
pip install -r requirements_no_tiktoken.txt

# Verify core imports work
echo "✅ Testing core imports..."
python -c "import flask; print('✅ Flask works')"
python -c "import openai; print('✅ OpenAI works')"
python -c "import requests; print('✅ Requests works')"

echo ""
echo "🎉 Quick fix complete! Starting the application..."
echo ""

# Start the application directly
echo "🚀 Starting AI Red Team Toolkit..."
python app.py
