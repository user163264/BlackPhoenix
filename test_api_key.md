
# OpenAI API Key Debug Tool

This simple script checks if your OpenAI API key is working properly by making a basic API call.

Run this when you're experiencing API request failures to determine if the issue is with your key.

```bash
# Activate the virtual environment if not already activated
source venv/bin/activate

# Run the test
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
    print(f'API Key is working properly! Response: {response.choices[0].message.content}');
except Exception as e:
    print(f'API Key error: {str(e)}');
"
```

If this test fails, check your API key in the `.env` file and make sure it's valid.
