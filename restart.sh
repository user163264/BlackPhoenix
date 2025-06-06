#!/bin/bash

# Check for running Flask server on the default port 5001
echo "Checking for existing Flask server..."
if pgrep -f "python app.py" > /dev/null; then
    echo "Found running Flask server, stopping it..."
    pkill -f "python app.py"
    # Wait a moment for the process to terminate
    sleep 2
fi

# Make sure the scripts are executable
chmod +x *.sh

# Restart the application
echo "Starting AI Red Teaming Toolkit..."
./run.sh
