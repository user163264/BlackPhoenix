#!/bin/bash

# This script checks if a specific port is in use and offers to free it up
# Usage: ./check_port.sh [port_number]

# Default port to check
DEFAULT_PORT=5001

# Get port from command line argument or use default
PORT=${1:-$DEFAULT_PORT}

# Function to check if a port is available
check_port_availability() {
    local port=$1
    echo "Checking if port $port is available..."
    
    # Check if the port is in use
    if lsof -i :$port >/dev/null 2>&1; then
        echo "⚠️ Port $port is already in use!"
        
        # Show the processes using the port
        echo "Process details:"
        lsof -i :$port | grep LISTEN
        
        # Check if it's AirPlay
        if lsof -i :$port | grep -q "AirPlay"; then
            echo "⚠️ Port $port is being used by AirPlay Receiver."
            echo "To fix this, you can either:"
            echo "1. Disable AirPlay Receiver in System Preferences -> General -> AirDrop & Handoff"
            echo "2. Or use a different port for your application"
        fi
        
        # Kill the process if requested
        read -p "Do you want to try to kill the process using port $port? (y/n): " answer
        if [[ "$answer" == "y" ]]; then
            kill_port_process $port
            
            # Verify port is now available
            if ! lsof -i :$port >/dev/null 2>&1; then
                echo "✅ Port $port is now available."
            else
                echo "⚠️ Could not free up port $port. You may need administrator privileges or to use a different port."
            fi
        fi
    else
        echo "✅ Port $port is available."
    fi
}

# Function to kill any process running on the specified port
kill_port_process() {
    local port=$1
    echo "Attempting to terminate processes using port $port..."
    
    # Find the process ID using the port (works on macOS)
    local pid=$(lsof -i :$port -t 2>/dev/null)
    
    if [ -n "$pid" ]; then
        echo "Found process(es) $pid using port $port. Terminating..."
        kill -9 $pid 2>/dev/null
        sleep 1
        echo "Process(es) terminated."
    else
        echo "No processes found using port $port."
    fi
}

# Check the specified port
check_port_availability $PORT

echo ""
echo "Port check complete for port $PORT."