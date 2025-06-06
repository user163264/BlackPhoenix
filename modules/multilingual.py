import openai
import time
import random
from config import Config

class MultilingualObfuscator:
    def __init__(self):
        # Configure OpenAI client directly in this class
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Extended language list with full names
        self.languages = {
            "ar": "Arabic",
            "zh": "Chinese", 
            "nl": "Dutch",
            "en": "English",
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
            "vi": "Vietnamese"
        }
    
    def translate_text(self, text, source_lang, target_lang):
        """Translate text from source language to target language using the LLM."""
        if source_lang not in self.languages:
            source_lang_name = source_lang
        else:
            source_lang_name = self.languages[source_lang]
            
        if target_lang not in self.languages:
            target_lang_name = target_lang
        else:
            target_lang_name = self.languages[target_lang]
        
        try:    
            messages = [
                {"role": "system", "content": "You are a professional translator."},
                {"role": "user", "content": f"Translate the following text from {source_lang_name} to {target_lang_name}. Preserve the meaning as precisely as possible. Only return the translated text, with no explanations:\n\n{text}"}
            ]
            
            response = self.client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return f"Translation error: {str(e)}"
    
    def detect_language(self, text):
        """Detect the language of a text using the LLM."""
        if not text.strip():
            return "en"  # Default to English for empty text
        
        try:
            messages = [
                {"role": "system", "content": "You are a language detection expert."},
                {"role": "user", "content": f"Detect the language of the following text. Respond with just the language code (en, fr, es, de, ru, zh, ja, ar):\n\n{text}"}
            ]
            
            response = self.client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=10
            )
            
            detected = response.choices[0].message.content.strip().lower()
            # Extract just the language code if necessary
            for code in self.languages.keys():
                if code in detected:
                    return code
            return "en"  # Default to English if detection fails
        except Exception as e:
            print(f"Language detection error: {str(e)}")
            return "en"  # Default to English if API fails
    
    def multi_lingual_obfuscation(self, text, num_chains=3, languages=None, endbookend=True, prevent_repeat=True):
        """
        Process text through a chain of language translations
        
        Args:
            text: The text to obfuscate
            num_chains: Number of languages to translate through
            languages: Optional list of specific languages to use
            endbookend: Whether to translate back to English at the end
            prevent_repeat: Whether to prevent repeated languages in the chain
            
        Returns:
            dict: A dictionary containing the original text, final obfuscated text,
                  translation chain, and intermediate results
        """
        # Default chain of languages if none provided
        if languages is None:
            # List of language codes that can be used
            available_languages = list(self.languages.keys())
            # Select random languages for the chain
            languages = random.sample(available_languages, min(num_chains, len(available_languages)))
            
            # Ensure we end with English if endbookend is True
            if endbookend and "en" not in languages:
                languages.append("en")
        
        # Prevent repeated languages in the chain if requested
        if prevent_repeat and len(languages) > len(set(languages)):
            # Remove duplicates while preserving order
            seen = set()
            languages = [x for x in languages if not (x in seen or seen.add(x))]
        
        # Start with original text
        current_text = text
        original_text = text
        intermediate_results = []
        chain = []
        
        # Add the original text to the results
        source_lang_code = self.detect_language(text)
        current_lang_code = source_lang_code
        
        intermediate_results.append({
            "language": self.languages.get(current_lang_code, current_lang_code),
            "text": current_text
        })
        
        # Translate through each language in sequence
        for target_lang_code in languages:
            source_lang_name = self.languages.get(current_lang_code, current_lang_code)
            target_lang_name = self.languages.get(target_lang_code, target_lang_code)
            
            # Add to the chain visualization
            chain.append(f"{source_lang_name} → {target_lang_name}")
            
            # Translate the text
            translated = self.translate_text(current_text, current_lang_code, target_lang_code)
            
            # Store intermediate result
            intermediate_results.append({
                "language": target_lang_name,
                "text": translated
            })
            
            # Update current text and language for next iteration
            current_text = translated
            current_lang_code = target_lang_code
            
            # Add a small delay to prevent rate limiting
            time.sleep(0.5)
        
        # Final translation back to English if the last language wasn't English and endbookend is True
        if endbookend and current_lang_code != "en":
            source_lang_name = self.languages.get(current_lang_code, current_lang_code)
            
            # Add to the chain visualization
            chain.append(f"{source_lang_name} → English")
            
            # Translate back to English
            final_text = self.translate_text(current_text, current_lang_code, "en")
            
            # Store final result
            intermediate_results.append({
                "language": "English",
                "text": final_text
            })
            
            current_text = final_text
        else:
            final_text = current_text
        
        # Return results
        return {
            "original_text": original_text,
            "obfuscated_text": final_text,
            "chain": chain,
            "intermediate_results": intermediate_results
        }