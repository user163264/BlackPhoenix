#!/bin/bash

# Make the test executable
chmod +x /Users/admin/Documents/redteam-tools/test_enhanced_token_obfuscator.py
chmod +x /Users/admin/Documents/redteam-tools/run_token_obfuscator_tests.sh

echo "Running Enhanced Token Obfuscator Tests..."
echo "==========================================="

cd /Users/admin/Documents/redteam-tools

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Activated virtual environment"
fi

# Run the test
python3 test_enhanced_token_obfuscator.py

echo ""
echo "Test execution completed."
