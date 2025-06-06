#!/bin/bash

# Use port 5001 instead of 5000 to avoid conflicts with AirPlay on macOS
PORT=5001

echo "The OpenAI API may require authentication. Please check the API key in config.py"

# Function to check if a port is available
check_port_availability() {
    local port=$1
    echo "Checking if port $port is available..."
    
    # Check if the port is in use
    if lsof -i :$port >/dev/null 2>&1; then
        echo "⚠️ Port $port is already in use!"
        
        # Check if it's AirPlay
        if lsof -i :$port | grep -q "AirPlay"; then
            echo "⚠️ Port $port is being used by AirPlay Receiver."
            echo "To fix this, you can either:"
            echo "1. Disable AirPlay Receiver in System Preferences -> General -> AirDrop & Handoff"
            echo "2. Or continue using a different port (current script will use $PORT)"
        else
            # Try to get the process name
            local process_name=$(lsof -i :$port | tail -n 1 | awk '{print $1}')
            echo "⚠️ Port $port is being used by: $process_name"
        fi
        
        # Kill the process if requested
        read -p "Do you want to try to kill the process using port $port? (y/n): " answer
        if [[ "$answer" == "y" ]]; then
            kill_port_process $port
        fi
    else
        echo "✅ Port $port is available."
    fi
}

# Function to kill any process running on the specified port
kill_port_process() {
    local port=$1
    echo "Checking for processes already using port $port..."
    
    # Find the process ID using the port (works on macOS)
    local pid=$(lsof -i :$port -t 2>/dev/null)
    
    if [ -n "$pid" ]; then
        echo "Found process $pid using port $port. Terminating..."
        kill -9 $pid 2>/dev/null
        sleep 1
        echo "Process terminated."
    else
        echo "No processes found using port $port."
    fi
}

# Check port availability instead of automatically killing
check_port_availability $PORT

echo "Starting AI Red Teaming Toolkit..."

# Activate the virtual environment
source venv/bin/activate

# Run the Flask application
python app.py &
APP_PID=$!

# Wait for the server to start
sleep 2

# Open the browser (works on macOS)
echo "Opening browser to http://localhost:$PORT/"
open http://localhost:$PORT/

# Display instructions
echo ""
echo "AI Red Teaming Toolkit is running at http://localhost:$PORT/"
echo "Press Ctrl+C to stop the server when you're done."

# Make sure the app stops when the script is interrupted
trap "kill $APP_PID 2>/dev/null" EXIT

# Keep the script running until user interrupts
wait $APP_PID