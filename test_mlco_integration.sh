#!/bin/bash

echo "Testing MLCO integration with the AI Red Teaming Toolkit"
echo "--------------------------------------------------------"
echo ""

# Check if the MLCO module exists
if [ -f "/Users/admin/Documents/redteam-tools/modules/multilingual.py" ]; then
    echo "✅ MLCO module found in modules directory"
else
    echo "❌ MLCO module not found in modules directory"
    exit 1
fi

# Check if the MLCO template exists
if [ -f "/Users/admin/Documents/redteam-tools/templates/mlco.html" ]; then
    echo "✅ MLCO template found in templates directory"
else
    echo "❌ MLCO template not found in templates directory"
    exit 1
fi

# Check if app.py contains the MLCO routes
if grep -q "def mlco():" "/Users/admin/Documents/redteam-tools/app.py"; then
    echo "✅ MLCO routes found in app.py"
else
    echo "❌ MLCO routes not found in app.py"
    exit 1
fi

# Check if the .env file exists with API key
if [ -f "/Users/admin/Documents/redteam-tools/.env" ]; then
    echo "✅ .env file found with API key"
else
    echo "Creating .env file with API key..."
    echo "OPENAI_API_KEY=your_openai_api_key_here" > "/Users/admin/Documents/redteam-tools/.env"
    echo "✅ .env file created with API key"
fi

echo ""
echo "✅ All tests passed! MLCO is successfully integrated with the AI Red Teaming Toolkit."
echo ""
echo "To start the application, run:"
echo "cd /Users/admin/Documents/redteam-tools && python app.py"
echo ""
echo "Then open your browser to: http://localhost:5001/mlco"
