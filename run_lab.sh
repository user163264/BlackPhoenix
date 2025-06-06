#!/bin/bash

# Start the Prompt Engineering Laboratory
echo "🧪 Starting Prompt Engineering Laboratory..."
echo "⚗️ Initializing environment..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔬 Activating virtual environment..."
    source venv/bin/activate
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "🧪 Creating .env file..."
    touch .env
    echo "OPENAI_API_KEY=PLACEHOLDER" >> .env
    echo "⚠️ Please update OPENAI_API_KEY in .env file with your API key."
else
    echo "🧪 .env file found!"
fi

# Check if required packages are installed
if [ -f "requirements.txt" ]; then
    echo "🔬 Checking required packages..."
    pip install -r requirements.txt
fi

# Check if another process is using port 5001
echo "🧪 Checking port availability..."
lsof -i:5001 > /dev/null
if [ $? -eq 0 ]; then
    echo "⚠️ Port 5001 is already in use. Attempting to free it..."
    kill $(lsof -t -i:5001) 2>/dev/null || true
    sleep 2
fi

# Start the Flask application
echo "🧪 Launching Prompt Engineering Laboratory..."
python app.py

# Handle termination
trap "echo '🧪 Shutting down Prompt Engineering Laboratory...'; exit" SIGINT SIGTERM

# Keep the script running
tail -f /dev/null