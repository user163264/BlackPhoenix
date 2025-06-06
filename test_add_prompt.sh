#!/bin/bash

# Make the script executable
chmod +x "$0"

echo "🔍 Testing Add Prompt Functionality"
echo "=================================="

# Test if the server is running
echo "1. Testing server connection..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/system-prompts
if [ $? -eq 0 ]; then
    echo "✅ Server is running"
else
    echo "❌ Server is not running - start with ./run.sh"
    exit 1
fi

echo ""
echo "2. Testing API endpoint directly..."

# Test the API endpoint
curl -X POST http://localhost:5001/api/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Prompt CLI",
    "content": "This is a test prompt created via CLI to debug the functionality.",
    "category": "debug",
    "description": "CLI test prompt",
    "tags": "debug,cli,test"
  }' \
  -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "3. Getting all prompts to verify..."
curl -s http://localhost:5001/api/prompts | python3 -m json.tool | head -20

echo ""
echo "🔍 Test complete!"
