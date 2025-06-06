#!/bin/bash

# Create a bash script to make all shell scripts executable
chmod +x *.sh

echo "Made all shell scripts executable."
echo "Running API key test..."

# Run the API key test
./test_api_key.sh

# Print instructions
echo ""
echo "🧪 To start the AI Red Teaming Toolkit, run:"
echo "   ./run.sh"
echo ""
echo "🔬 Then access the toolkit at http://localhost:5001"
echo ""
echo "🔄 If you need to restart the application, run:"
echo "   ./restart.sh"
echo ""
echo "🔑 If you encounter API issues, run:" 
echo "   ./test_api_key.sh"
