#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fixed Segmented Multilingual Translation Module

This version of the segmented_multilingual_translation function includes all necessary
imports internally to avoid dependency issues.
"""

def fixed_segmented_translation(text, segment_size=3, languages=None, randomize_languages=False):
    """
    Translate different segments of text into different languages using JSON structure.
    
    This function includes all necessary imports internally to avoid scope issues.
    
    Args:
        text: The text to be translated
        segment_size: Number of words per segment
        languages: List of specific languages to use (if None, uses all available languages)
        randomize_languages: Whether to randomize the language order (default: False)
    
    Returns:
        dict: A dictionary containing the original text, multilingual text,
              segments with their translations, and metadata
    """
    # Import all necessary modules inside the function
    import re
    import json
    import random
    import openai
    import os
    
    # Default languages list
    DEFAULT_LANGUAGES = [
        "Arabic", "Chinese", "Dutch", "French", "German", "Hindi", 
        "Italian", "Japanese", "Korean", "Portuguese", "Russian", 
        "Spanish", "Swedish", "Thai", "Turkish", "Vietnamese"
    ]
    
    # Use shorter language codes for OpenAI API
    LANGUAGE_CODES = {
        "Arabic": "ar",
        "Chinese": "zh",
        "Dutch": "nl",
        "French": "fr",
        "German": "de",
        "Hindi": "hi",
        "Italian": "it",
        "Japanese": "ja",
        "Korean": "ko",
        "Portuguese": "pt",
        "Russian": "ru",
        "Spanish": "es",
        "Swedish": "sv",
        "Thai": "th",
        "Turkish": "tr",
        "Vietnamese": "vi",
        "English": "en"
    }
    
    # Reverse mapping for API responses
    CODE_TO_LANGUAGE = {code: lang for lang, code in LANGUAGE_CODES.items()}
    
    # Ensure API key is set
    if not openai.api_key:
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            # Try to get from .env file as backup
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY='):
                            api_key = line.strip().split('=', 1)[1]
                            break
        openai.api_key = api_key

    # Translation function
    def translate_text(text, source_lang, target_lang, model="gpt-3.5-turbo"):
        """Translate text from source language to target language using the OpenAI API."""
        try:
            # Convert language names to codes
            source_code = LANGUAGE_CODES.get(source_lang, "en")
            target_code = LANGUAGE_CODES.get(target_lang, target_lang.lower())
            
            print(f"Translating '{text}' from {source_lang} to {target_lang}")
            
            # Check if we're using the older API format or newer format
            try:
                # Try the newer API format with OpenAI client
                client = openai.OpenAI(api_key=openai.api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": f"You are a professional translator. Translate exactly this text from {source_lang} to {target_lang}. Return ONLY the translation, nothing else."},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.2,
                    max_tokens=1024
                )
                
                translated = response.choices[0].message.content.strip()
            except AttributeError:
                # Fallback to the older ChatCompletion format
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": f"You are a professional translator. Translate exactly this text from {source_lang} to {target_lang}. Return ONLY the translation, nothing else."},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.2,
                    max_tokens=1024
                )
                
                translated = response.choices[0].message.content.strip()
            
            print(f"Translation result: '{translated}'")
            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    if languages is None:
        # Use all available languages
        languages = DEFAULT_LANGUAGES.copy()
    
    # Check if languages are codes instead of names
    processed_languages = []
    for lang in languages:
        # If provided as a code, convert to language name if possible
        if len(lang) <= 3 and lang.lower() in CODE_TO_LANGUAGE:
            processed_languages.append(CODE_TO_LANGUAGE[lang.lower()])
        else:
            processed_languages.append(lang)
    
    languages = processed_languages
    
    # Apply randomization if requested
    if randomize_languages:
        print("Randomizing language order")
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
    
    print(f"Translating {segment_count} segments in {len(languages)} languages")
    
    # Process each segment individually for more reliability
    final_segments = []
    multilingual_text = ""
    
    for i, segment in enumerate(segments):
        segment_id = segment.get("segment_id")
        original_text = segment.get("original")
        target_lang = segment.get("language")
        
        print(f"\nProcessing segment {segment_id}: '{original_text}' to {target_lang}")
        
        # Translate this segment
        if target_lang != "English":
            try:
                # Actually do the translation - this was the missing part
                translated_text = translate_text(original_text, "English", target_lang)
            except Exception as e:
                print(f"Error translating segment {segment_id}: {e}")
                translated_text = original_text
        else:
            translated_text = original_text
        
        # Store the result
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
    
    print(f"\nCreated multilingual text with {segment_count} segments in {len(languages)} languages")
    print(f"Multilingual text: {multilingual_text}")
    
    return {
        "original_text": text,
        "multilingual_text": multilingual_text,
        "segments": final_segments,
        "languages_used": languages[:len(segments)] if len(segments) < len(languages) else languages,
        "segment_size": segment_size
    }
