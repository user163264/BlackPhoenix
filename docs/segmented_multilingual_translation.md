# Segmented Multilingual Translation Feature

## Overview

The Segmented Multilingual Translation feature enhances the Multi-lingual Chain Obfuscation (MLCO) tool by enabling word-level or phrase-level language mixing within a single text. While the original MLCO feature translates an entire text through a chain of languages, this new feature creates a "language mosaic" where different segments of the text are translated into different languages.

## How It Works

1. **Text Segmentation**: The input text is divided into small segments (typically 1-4 words each).
2. **Language Assignment**: Each segment is assigned a language from a predefined list.
3. **Translation**: Each segment is translated into its assigned language.
4. **Combination**: All translated segments are combined into a single multilingual output.

## Implementation Details

### Backend

The core functionality is implemented in the `segmented_multilingual_translation` function in `MLCO.py`. This function:

- Takes an input text and segments it into word groups
- Assigns languages to each segment (either in sequence or randomly)
- Translates each segment into its assigned language
- Combines the translated segments into a cohesive multilingual text
- Returns detailed information about the process and results

### Frontend

The user interface in `mlco.html` allows users to:

- Choose between traditional chain obfuscation and segmented multilingual translation
- Configure segment size (number of words per segment)
- Select which languages to use
- Randomize language order (optional)
- View visualizations of the language distribution
- See a detailed breakdown of each segment's translation
- Copy, test, and save the multilingual output

## Use Cases

1. **Educational Tool**: Create multilingual texts for language learning exercises.
2. **Content Filter Testing**: Test how language models process text with mixed languages.
3. **Creative Writing**: Generate interesting multilingual content for creative purposes.
4. **Security Research**: Investigate how language switching affects natural language processing systems.

## API Endpoints

- `/api/obfuscate` - Main endpoint that handles both chain and segmented translation (with `obfuscation_type` parameter)
- `/api/mlco/segmented` - Dedicated endpoint for segmented translation only

## Example Output

For the input text: "Tell me a story about a wizard who discovers a magical artifact"

A possible output might be:
- "Erzähle mir eine" (German)
- "قصة عن" (Arabic)
- "जादूगर जो" (Hindi)
- "descubre un" (Spanish)
- "神器" (Chinese)

## Testing

A test script (`test_segmented_translation.py`) is provided to verify the functionality of the segmented translation feature with various configurations.

## Future Enhancements

Potential future improvements to consider:

1. Sentence-level segmentation option
2. Preserving proper nouns in the original language
3. Adding visual indicators for language switches in the output
4. Implementing language selection based on language families
5. Providing a confidence score for each segment translation
