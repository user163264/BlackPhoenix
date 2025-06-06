#!/bin/bash
# Run the MLCO lab with the fixed segmented translation
echo "Starting the Prompt Engineering Laboratory with fixed segmented translation..."
echo "This version addresses the issues with the segmented multilingual translation feature."
echo
echo "To use the segmented translation:"
echo "1. Navigate to http://localhost:5001/mlco"
echo "2. Enter your text"
echo "3. Select 'Segmented Multilingual' as the obfuscation type"
echo "4. Configure segment size and language options"
echo "5. Click 'Generate Obfuscated Prompt'"
echo
echo "Starting server..."
python3 app.py
