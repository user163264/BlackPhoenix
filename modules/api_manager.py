import openai
import time
import tiktoken
import logging
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_requests.log"),
        logging.StreamHandler()
    ]
)

class APIManager:
    def __init__(self):
        # Configure OpenAI client
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.request_history = []
        self.logger = logging.getLogger('api_manager')
        
        # Initialize token counter
        try:
            self.encoding = tiktoken.encoding_for_model(Config.DEFAULT_MODEL)
        except:
            self.logger.warning(f"Could not get encoding for {Config.DEFAULT_MODEL}. Using cl100k_base instead.")
            self.encoding = tiktoken.get_encoding("cl100k_base")  # Fallback encoding
        
        self.logger.info(f"APIManager initialized with model: {Config.DEFAULT_MODEL}")
    
    def count_tokens(self, text):
        """Count the number of tokens in a text string."""
        if not text:
            return 0
        return len(self.encoding.encode(text))
    
    def make_request(self, messages, model=None, temperature=None, max_tokens=None):
        """Make a request to the OpenAI API with rate limiting and error handling."""
        model = model or Config.DEFAULT_MODEL
        temperature = temperature or Config.TEMPERATURE
        max_tokens = max_tokens or Config.MAX_TOKENS
        
        # Rate limiting - simple implementation
        if len(self.request_history) > 0:
            last_request_time = self.request_history[-1]
            elapsed = time.time() - last_request_time
            if elapsed < 1.0:  # Limit to ~60 requests per minute
                time.sleep(1.0 - elapsed)
        
        # Log the request
        self.logger.info(f"Making request to model: {model}")
        
        try:
            # Use the new client-based API
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            self.request_history.append(time.time())
            if len(self.request_history) > 100:
                self.request_history.pop(0)
            
            # Log successful request
            self.logger.info(f"Request successful. Used {response.usage.total_tokens} tokens.")
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "tokens": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                }
            }
            
        except openai.RateLimitError as e:
            self.logger.error(f"Rate limit exceeded: {e}")
            return {
                "success": False,
                "error": f"Rate limit exceeded: {str(e)}. Please try again later."
            }
        except openai.APIError as e:
            self.logger.error(f"API error: {e}")
            return {
                "success": False,
                "error": f"API error: {str(e)}"
            }
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
