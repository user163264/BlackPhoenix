#!/bin/bash

# Set the working directory to the script's directory
cd "$(dirname "$0")"

# Make script executable
chmod +x "$(basename "$0")"

# Activate the virtual environment
source venv/bin/activate

# Run the API key test
python -c "
import openai;
from config import Config;
client = openai.OpenAI(api_key=Config.OPENAI_API_KEY);
try:
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': 'Hello'}],
        max_tokens=5
    );
    print(f'\n✅ API Key is working properly! Response: {response.choices[0].message.content}\n');
except Exception as e:
    print(f'\n❌ API Key error: {str(e)}\n');
"

echo "If the test failed, check your API key in the .env file and make sure it's valid."
echo "You may need to check your OpenAI account for billing issues or rate limit restrictions."
