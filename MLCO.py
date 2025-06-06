
import os
import openai
from flask import Flask, request, jsonify, render_template
import json
import random
import time
import re
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure OpenAI API
# For security, the API key should be in an environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY", "")
print(f"Loaded API key: {'Key found' if openai.api_key else 'No API key found'}")

# If API key is not found, try to load it directly from .env file as backup
if not openai.api_key:
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    openai.api_key = line.strip().split('=', 1)[1]
                    print(f"Loaded API key from .env file directly: {'Key found' if openai.api_key else 'No API key found'}")
                    break

# List of languages to use in the chain
LANGUAGES = [
    "Arabic", "Chinese", "Dutch", "French", "German", "Hindi", 
    "Italian", "Japanese", "Korean", "Portuguese", "Russian", 
    "Spanish", "Swedish", "Thai", "Turkish", "Vietnamese"
]

def translate_text(text, source_lang, target_lang, model="gpt-3.5-turbo"):
    """Translate text from source language to target language using the OpenAI API."""
    try:
        print(f"Attempting to translate: '{text}' from {source_lang} to {target_lang}")
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the following text from {source_lang} to {target_lang}. Preserve the meaning as precisely as possible."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        translated = response.choices[0].message.content.strip()
        print(f"Translation successful: '{text}' -> '{translated}'")
        return translated
    except Exception as e:
        print(f"TRANSLATION ERROR: '{text}' from {source_lang} to {target_lang}. Error: {e}")
        # You can also log the API key (first few characters) to check if it's being used
        api_key = openai.api_key
        if api_key:
            print(f"API Key: {api_key[:5]}...{api_key[-4:]} (length: {len(api_key)})")
        else:
            print("API Key is not set!")
        return text

def multi_lingual_obfuscation(text, num_chains=3, languages=None):
    """
    Obfuscate text by translating it through a chain of languages.
    
    Args:
        text: The text to obfuscate
        num_chains: Number of languages to translate through
        languages: Optional list of specific languages to use
    
    Returns:
        dict: A dictionary containing the original text, final obfuscated text,
              translation chain, and intermediate results
    """
    if languages is None:
        # Randomly select languages for the chain
        languages = random.sample(LANGUAGES, min(num_chains, len(LANGUAGES)))
    
    current_text = text
    current_lang = "English"
    
    chain = []
    intermediate_results = []
    
    # Log the start of the translation chain
    print(f"Starting multi-lingual obfuscation chain with languages: {languages}")
    print(f"Original text: {text}")
    
    for target_lang in languages:
        print(f"Translating from {current_lang} to {target_lang}...")
        chain.append(f"{current_lang} → {target_lang}")
        translated = translate_text(current_text, current_lang, target_lang)
        intermediate_results.append({
            "language": target_lang,
            "text": translated
        })
        print(f"Translated to {target_lang}: {translated[:50]}...")
        current_text = translated
        current_lang = target_lang
        # Add a small delay to prevent rate limiting
        time.sleep(0.5)
    
    # Translate back to English
    print(f"Translating back to English from {current_lang}...")
    chain.append(f"{current_lang} → English")
    final_text = translate_text(current_text, current_lang, "English")
    intermediate_results.append({
        "language": "English",
        "text": final_text
    })
    
    print(f"Final obfuscated text: {final_text[:50]}...")
    
    return {
        "original_text": text,
        "obfuscated_text": final_text,
        "chain": chain,
        "intermediate_results": intermediate_results
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mlco')
def mlco():
    return render_template('mlco.html')

@app.route('/mlco/lab')
def mlco_lab():
    return render_template('mlco_lab.html')

@app.route('/mlco/modern')
def mlco_lab_modern():
    return render_template('mlco_lab_modern.html')

@app.route('/api/mlco/segmented', methods=['POST'])
def segmented_translation():
    data = request.json
    text = data.get('text', '')
    segment_size = int(data.get('segment_size', 3))
    languages = data.get('languages', None)
    randomize_languages = data.get('randomize_languages', False)
    
    result = segmented_multilingual_translation(text, segment_size, languages, randomize_languages)
    return jsonify(result)

def segmented_multilingual_translation(text, segment_size=3, languages=None, randomize_languages=False):
    """
    Translate different segments of text into different languages using JSON structure.
    
    Args:
        text: The text to be translated
        segment_size: Number of words per segment
        languages: List of specific languages to use (if None, uses all available languages)
        randomize_languages: Whether to randomize the language order (default: False)
    
    Returns:
        dict: A dictionary containing the original text, multilingual text,
              segments with their translations, and metadata
    """
    if languages is None:
        # Use all available languages
        languages = LANGUAGES.copy()
    
    if randomize_languages:
        random.shuffle(languages)
    
    # Split text into words
    words = re.findall(r'\w+|[^\w\s]', text)
    
    segments = []
    segment_count = 0
    
    # Group words into segments of specified size
    for i in range(0, len(words), segment_size):
        segment_words = words[i:i+segment_size]
        original_segment = " ".join(segment_words)
        # Remove leading space if it's a punctuation mark
        original_segment = re.sub(r'\s+([.,!?;:])', r'\1', original_segment)
        
        # Select language for this segment
        lang_index = segment_count % len(languages)
        target_lang = languages[lang_index]
        
        # Prepare segment data
        segments.append({
            "segment_id": segment_count + 1,  # 1-based indexing for clarity
            "original": original_segment,
            "language": target_lang,
            "risk": "Medium",  # Default risk level
            "translated": ""  # Will be filled after translation
        })
        
        segment_count += 1
    
    # Use JSON-based batch translation approach
    print(f"Preparing to translate {segment_count} segments in {len(segments)} languages")
    
    try:
        # Create JSON payload for translation
        translation_payload = json.dumps(segments, ensure_ascii=False, indent=2)
        
        # Build a prompt for translation
        translation_prompt = f"""Translate each segment into its specified language:

```json
{translation_payload}
```

Return the translated segments in valid JSON format with the same structure, adding 'translated' field to each segment."""
        
        # Use OpenAI for translation (more reliable)
        system_prompt = "You are a professional translator. Return only valid JSON with translations. Preserve the exact JSON structure."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": translation_prompt}
            ],
            temperature=0.2,
            max_tokens=2048
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Extract JSON from response (handling potential wrapper text)
        import re
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```|\[\s*{[\s\S]*}\s*\]', response_text)
        if json_match:
            json_text = json_match.group(1) if json_match.group(1) else response_text
        else:
            json_text = response_text
        
        # Clean up any remaining markdown or backticks
        json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON response
        translated_segments = json.loads(json_text)
        
        # Update segments with translations
        segments_dict = {}
        for segment in translated_segments:
            segment_id = segment.get("segment_id")
            if segment_id:
                segments_dict[segment_id] = segment
                
        # Build final segments list and multilingual text
        final_segments = []
        multilingual_text = ""
        
        for i, segment in enumerate(segments):
            segment_id = segment.get("segment_id")
            translated_segment = segments_dict.get(segment_id, {})
            
            # Get the translated text or fallback to original
            translated_text = translated_segment.get("translated", "")
            if not translated_text:
                translated_text = segment.get("original")
                print(f"Warning: Translation missing for segment {segment_id}, using original text")
            
            final_segments.append({
                "segment_index": i,
                "original_text": segment.get("original", ""),
                "translated_text": translated_text,
                "language": segment.get("language", "Unknown")
            })
            
            # Add to multilingual text (with space handling)
            if i > 0 and not segment.get("original", "").startswith((',', '.', '!', '?', ';', ':')):
                multilingual_text += " "
            multilingual_text += translated_text
            
    except Exception as e:
        print(f"Error in JSON-based translation: {e}")
        # Fallback to original implementation for each segment separately
        final_segments = []
        multilingual_text = ""
        
        for i, segment in enumerate(segments):
            original_text = segment.get("original", "")
            target_lang = segment.get("language", "English")
            
            # Translate this segment
            if target_lang != "English":
                translated_text = translate_text(original_text, "English", target_lang)
            else:
                translated_text = original_text
            
            final_segments.append({
                "segment_index": i,
                "original_text": original_text,
                "translated_text": translated_text,
                "language": target_lang
            })
            
            # Add to multilingual text (with space handling)
            if i > 0 and not original_text.startswith((',', '.', '!', '?', ';', ':')):
                multilingual_text += " "
            multilingual_text += translated_text
    
    print(f"Created multilingual text with {segment_count} segments in {len(languages)} languages")
    
    return {
        "original_text": text,
        "multilingual_text": multilingual_text,
        "segments": final_segments,
        "languages_used": languages[:len(segments)] if len(segments) < len(languages) else languages,
        "segment_size": segment_size
    }

@app.route('/api/obfuscate', methods=['POST'])
def obfuscate():
    data = request.json
    text = data.get('text', '')
    obfuscation_type = data.get('obfuscation_type', 'chain')
    
    if obfuscation_type == 'chain':
        num_chains = int(data.get('num_chains', 3))
        # Optional: Allow specifying exact language chain
        languages = data.get('languages', None)
        result = multi_lingual_obfuscation(text, num_chains, languages)
    else:  # segmented
        segment_size = int(data.get('segment_size', 3))
        languages = data.get('languages', None)
        randomize_languages = data.get('randomize_languages', False)
        result = segmented_multilingual_translation(text, segment_size, languages, randomize_languages)
    
    return jsonify(result)

@app.route('/api/test-target', methods=['POST'])
def test_target():
    """
    Test the obfuscated text against a target model to see if it bypasses moderation
    """
    data = request.json
    text = data.get('text', '')
    target_model = data.get('model', 'gpt-3.5-turbo')
    
    try:
        # First test with original prompt to see if it's normally blocked
        original_response = openai.ChatCompletion.create(
            model=target_model,
            messages=[
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Then test with obfuscated prompt
        obfuscated_text = data.get('obfuscated_text', '') or data.get('multilingual_text', '')
        obfuscated_response = openai.ChatCompletion.create(
            model=target_model,
            messages=[
                {"role": "user", "content": obfuscated_text}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return jsonify({
            "original_response": original_response.choices[0].message.content,
            "obfuscated_response": obfuscated_response.choices[0].message.content,
            "success": True
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        })

if __name__ == '__main__':
    # Check if the templates directory exists, create if it doesn't
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"Created templates directory: {templates_dir}")
    
    # Create .env file with API key if it doesn't exist
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            f.write(f"OPENAI_API_KEY=your_openai_api_key_here\n")
        print(f"Created .env file with API key")
    
    app.run(debug=True, host='localhost', port=5000)
