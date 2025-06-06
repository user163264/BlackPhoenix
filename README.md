# BlackPhoenix Red Team Toolkit

A sophisticated workbench for red teaming language models. Work in progress.

## Overview

The BlackPhoenix Red Team Toolkit is a purpose-built toolkit for developing, testing, and documenting sophisticated red teaming techniques for language models. Unlike standard tools that directly test model behaviors, this laboratory focuses on generating prompts that can be tested against external models, making it ideal for red teaming assignments.

## Key Features

- **Multi-lingual Chain Obfuscation (MLCO)**: Transform prompts through language translation chains
- **Segmented Multilingual Translation**: Create prompts with word-level language mixing (now with enhanced JSON-based batch translation)
- **Token Manipulation Lab**: Advanced token-level obfuscation techniques
- **System Engineering**: Tools for crafting system prompts to exploit vulnerabilities
- **Prompt Library**: Collection of system prompts for experimentation
- **Coming Soon**: Cognitive bias exploitation, technique pipeline builder, and more

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key in `.env`
4. Run the laboratory:
   ```
   ./run_lab.sh
   ```
5. Access the laboratory at http://localhost:5001

## Usage

The laboratory is designed around the concept of prompt generation workflows:

1. Choose a laboratory module based on the obfuscation technique you want to explore
2. Configure the input and transformation parameters
3. Generate obfuscated prompts
4. Analyze the transformation process through visualizations
5. Export the results for testing against external models

## Recent Updates

- **Enhanced Segmented Translation**: The segmented multilingual translation feature now uses a batch JSON-based approach for improved reliability and translation quality ([Documentation](docs/enhanced_segmented_translation.md))
- **Improved Error Handling**: Better logging and fallback mechanisms for API calls
- **API Key Management**: More robust handling of API keys and environment variables

## Development

This project uses Flask for the backend, with a custom UI inspired by scientific software. The modular design makes it easy to add new obfuscation techniques.

## License

For research purposes only.
