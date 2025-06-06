#!/bin/bash

# Set the working directory to the script's directory
cd "$(dirname "$0")"

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup_fresh.sh to create a fresh environment..."
    ./setup_fresh.sh
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# Check if Flask is installed
if ! python -c "import flask" &> /dev/null; then
    echo "Flask is not installed in the virtual environment. Running setup_fresh.sh..."
    ./setup_fresh.sh
    exit 1
fi

# Make sure the API key is set
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    echo "# OpenAI API Configuration" > .env
    echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
    echo "DEFAULT_MODEL=gpt-4o" >> .env
    echo "TEMPERATURE=0.7" >> .env
    echo "MAX_TOKENS=1000" >> .env
    echo "" >> .env
    echo "# App Configuration" >> .env
    echo "SECRET_KEY=redteam-tools-secret-key-2024" >> .env
    echo "PORT=5001" >> .env
    echo "DEBUG=True" >> .env
    echo "" >> .env
    echo "# Lab Configuration" >> .env
    echo "LAB_NAME=\"AI Red Teaming Laboratory\"" >> .env
    echo "LAB_VERSION=\"1.1.0\"" >> .env
fi

# Run the Flask application
echo "Starting AI Red Teaming Toolkit..."
echo "Access the toolkit at http://localhost:5001"
python app.py