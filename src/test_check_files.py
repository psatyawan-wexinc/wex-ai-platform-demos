import os
from pathlib import Path
import json

def check_test_files():
    test_files = {
        'test_audio.py': 'Audio transcription tests',
        'test_image.py': 'Image generation tests',
        'test_openai_image.py': 'OpenAI-compatible image tests',
        'test_transcription.py': 'Transcription service tests',
        'test_image_models.py': 'Image model tests',
        'test_verify_models.py': 'Model verification tests',
        'test_simple_image.py': 'Simple image generation tests',
        'test_minimal_image.py': 'Minimal image generation tests'
    }
    
    print("\nChecking all test files:")
    
    for filename, description in test_files.items():
        print(f"\n{'='*50}")
        print(f"File: {filename}")
        print(f"Purpose: {description}")
        print(f"{'='*50}")
        
        file_path = Path('src') / filename
        if not file_path.exists():
            print(f"File not found: {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract key information
        print("\nKey Details:")
        
        # Check imports
        imports = [line for line in content.split('\n') if line.strip().startswith('import') or line.strip().startswith('from')]
        print("\nImports:")
        for imp in imports:
            print(f"- {imp.strip()}")
            
        # Check URLs
        urls = [line for line in content.split('\n') if 'url' in line.lower() and ('http' in line or 'base_url' in line)]
        print("\nURLs:")
        for url in urls:
            print(f"- {url.strip()}")
            
        # Check model references
        models = [line for line in content.split('\n') if '"model"' in line or "'model'" in line]
        print("\nModel References:")
        for model in models:
            print(f"- {model.strip()}")
            
        # Check for successful test cases
        success_cases = [line for line in content.split('\n') if 'print' in line and ('success' in line.lower() or 'saved' in line.lower())]
        print("\nSuccess Indicators:")
        for case in success_cases:
            print(f"- {case.strip()}")

if __name__ == "__main__":
    check_test_files() 