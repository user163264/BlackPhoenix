import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # App configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", "redteam-tools-secret-key-2024")
    PORT = int(os.environ.get("PORT", 5001))
    DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
    
    # API configuration
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "gpt-4o")
    TEMPERATURE = float(os.environ.get("TEMPERATURE", 0.7))
    MAX_TOKENS = int(os.environ.get("MAX_TOKENS", 1000))
    
    # Test settings
    MAX_OBFUSCATION_LAYERS = 5
    
    # Extended language list for MLCO lab
    LANGUAGES = {
        "ar": "Arabic", 
        "zh": "Chinese", 
        "nl": "Dutch", 
        "fr": "French", 
        "de": "German", 
        "hi": "Hindi", 
        "it": "Italian", 
        "ja": "Japanese", 
        "ko": "Korean", 
        "pt": "Portuguese", 
        "ru": "Russian", 
        "es": "Spanish", 
        "sv": "Swedish", 
        "th": "Thai", 
        "tr": "Turkish", 
        "vi": "Vietnamese",
        "en": "English"
    }
    
    # System module settings
    MAX_SYSTEM_SATURATION_TOKENS = 10000
    
    # Lab settings
    LAB_NAME = os.environ.get("LAB_NAME", "AI Red Teaming Laboratory")
    LAB_VERSION = os.environ.get("LAB_VERSION", "1.1.0")
    
    # Tokens and characters limits
    MAX_PROMPT_LENGTH = 4000
    MAX_SYSTEM_PROMPT_LENGTH = 1500
    
    # Default system prompt for testing
    DEFAULT_SYSTEM_PROMPT = "You are a helpful, harmless, and honest AI assistant."
