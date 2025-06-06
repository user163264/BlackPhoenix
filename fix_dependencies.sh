#!/bin/bash

echo "🔧 Fixing AI Red Team Toolkit Dependencies..."
echo "============================================="

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

# Install compatible dependencies
echo "📚 Installing compatible dependencies..."
pip install -r requirements_fixed.txt

# Verify the installation
echo "✅ Testing OpenAI import..."
python -c "import openai; print('✅ OpenAI imported successfully')" || {
    echo "❌ OpenAI import failed, trying alternative approach..."
    pip install openai==1.40.0 httpx==0.24.1
    python -c "import openai; print('✅ OpenAI imported successfully')"
}

echo ""
echo "🎉 Dependencies fixed! You can now start the application:"
echo "   ./run.sh"
echo ""
echo "🌐 Access the toolkit at: http://localhost:5001"
