#!/bin/bash

# This script sets up a fresh virtual environment and installs all required dependencies

# Define colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up AI Red Teaming Toolkit...${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Path to our project
PROJECT_DIR="/Users/admin/Documents/redteam-tools"
cd "$PROJECT_DIR"

# Remove old venv if it exists and create a fresh one
echo -e "${GREEN}Creating a fresh virtual environment...${NC}"
rm -rf venv
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
echo -e "${GREEN}Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install required packages
echo -e "${GREEN}Installing required packages...${NC}"
pip install flask openai requests python-dotenv flask-wtf nltk langdetect transformers tiktoken

# Generate requirements.txt
echo -e "${GREEN}Generating requirements.txt...${NC}"
pip freeze > requirements.txt

# Display completion message
echo -e "${GREEN}Setup complete! You can now run the application with:${NC}"
echo "source venv/bin/activate"
echo "python app.py"
echo ""
echo -e "${GREEN}Or simply use:${NC}"
echo "./run.sh"

# Make run.sh executable
chmod +x run.sh

echo -e "${GREEN}Done!${NC}"