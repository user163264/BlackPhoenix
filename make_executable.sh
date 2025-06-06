#!/bin/bash

# Makes all shell scripts executable in the project

cd "$(dirname "$0")"

# Make all shell scripts executable
chmod +x *.sh

echo "✅ Made all shell scripts executable."
echo ""
echo "🧪 To start the AI Red Teaming Toolkit, run:"
echo "   ./run.sh"
echo ""
echo "🔬 Then access the toolkit at http://localhost:5001"