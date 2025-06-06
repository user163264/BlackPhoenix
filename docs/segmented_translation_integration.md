# Integration Guide: Segmented Multilingual Translation

This guide is for developers who need to integrate with or extend the Segmented Multilingual Translation feature.

## API Integration

### 1. Using the Python API directly

You can import and use the `segmented_multilingual_translation` function from MLCO.py:

```python
from MLCO import segmented_multilingual_translation

result = segmented_multilingual_translation(
    text="Your text here",
    segment_size=3,  # words per segment
    languages=["German", "French", "Spanish"],  # optional, uses all available languages if None
    randomize_languages=False  # optional, set to True to randomize language order
)

# Access the results
multilingual_text = result["multilingual_text"]
segments = result["segments"]
languages_used = result["languages_used"]
```

### 2. Using the HTTP API

Make a POST request to `/api/obfuscate` with the following parameters:

```json
{
  "text": "Your text here",
  "obfuscation_type": "segmented",
  "segment_size": 3,
  "languages": ["German", "French", "Spanish"],
  "randomize_languages": false
}
```

Or use the dedicated endpoint `/api/mlco/segmented`:

```json
{
  "text": "Your text here",
  "segment_size": 3,
  "languages": ["German", "French", "Spanish"],
  "randomize_languages": false
}
```

## Enhanced Translation System

The translation system now uses a JSON-based batch approach that offers improved reliability and quality:

1. All segments are translated in a single API call
2. Structured JSON ensures consistent handling of translations
3. Fallback mechanisms automatically handle errors

### JSON Structure (Internal)

```json
[
  {
    "segment_id": 1,
    "original": "segment words here",
    "language": "German",
    "risk": "Medium"
  },
  {
    "segment_id": 2,
    "original": "more words here",
    "language": "French",
    "risk": "Medium"
  }
]
```

## Response Format

Both API methods return a JSON object with the following structure (unchanged from previous version):

```json
{
  "original_text": "Your original text",
  "multilingual_text": "The combined multilingual text",
  "segments": [
    {
      "segment_index": 0,
      "original_text": "segment words here",
      "translated_text": "translated segment here",
      "language": "Language Name"
    },
    // More segments...
  ],
  "languages_used": ["Language1", "Language2", "..."],
  "segment_size": 3
}
```

## Extending the Feature

### Adding new languages

To add new languages to the system, modify the `LANGUAGES` list in `MLCO.py`:

```python
LANGUAGES = [
    "Arabic", "Chinese", "Dutch", "French", "German", "Hindi", 
    "Italian", "Japanese", "Korean", "Portuguese", "Russian", 
    "Spanish", "Swedish", "Thai", "Turkish", "Vietnamese",
    "YourNewLanguage"  # Add new languages here
]
```

### Modifying segmentation logic

The current implementation segments by word count. If you want to change the segmentation logic (e.g., to segment by sentences), modify the loop in the `segmented_multilingual_translation` function:

```python
# Current word-based segmentation:
words = re.findall(r'\w+|[^\w\s]', text)
for i in range(0, len(words), segment_size):
    segment_words = words[i:i+segment_size]
    # ...

# Example of sentence-based segmentation (would need to be implemented):
sentences = re.split(r'(?<=[.!?])\s+', text)
for i, sentence in enumerate(sentences):
    # ...
```

## Common Issues and Solutions

1. **Translation API rate limiting**
   - The function includes a small delay between translations
   - For heavy usage, consider implementing a queue system

2. **Word boundary issues in combined text**
   - The current implementation handles basic punctuation
   - For more complex cases, you might need to enhance the joining logic

3. **JSON Parsing Errors**
   - If you encounter JSON parsing errors, check the API response format
   - The system will automatically fall back to individual translations if batch processing fails

4. **API Key Configuration**
   - Ensure your OpenAI API key is correctly set in the .env file
   - For production use, consider using a more secure key management system

## UI Customization

The UI components for the segmented translation feature are in `templates/mlco.html`. Key sections:

- Radio buttons for switching between obfuscation types
- Segment size configuration input
- Language selection interface
- Results display with language color coding

To modify the appearance of language segments in the results, look for the CSS classes:
- `.segment-badge`
- `.segment-item`
- `.language-color-indicator`
