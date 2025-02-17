import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import urllib3
import httpx
import json
import importlib
import sys

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_all_examples():
    # Load environment variables
    load_dotenv()
    
    # Files to test
    test_files = [
        'test_audio.py',
        'test_image.py',
        'test_openai_image.py',
        'test_transcription.py',
        'test_image_models.py'
    ]
    
    print("\nTesting all example files:")
    
    for test_file in test_files:
        print(f"\n{'='*50}")
        print(f"Testing {test_file}:")
        print(f"{'='*50}")
        
        try:
            # Read the file contents
            file_path = Path('src') / test_file
            if not file_path.exists():
                print(f"File not found: {file_path}")
                continue
                
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Look for API endpoints
            endpoints = []
            for line in content.split('\n'):
                if 'url' in line.lower() and 'http' in line:
                    endpoints.append(line.strip())
            
            print("\nEndpoints found:")
            for endpoint in endpoints:
                print(f"- {endpoint}")
            
            # Look for model names
            models = []
            for line in content.split('\n'):
                if '"model"' in line or "'model'" in line:
                    models.append(line.strip())
            
            print("\nModels found:")
            for model in models:
                print(f"- {model}")
            
            # Look for request payloads
            payloads = []
            in_payload = False
            current_payload = []
            
            for line in content.split('\n'):
                if 'payload' in line and '{' in line:
                    in_payload = True
                    current_payload = [line.strip()]
                elif in_payload:
                    current_payload.append(line.strip())
                    if '}' in line and line.strip().count('}') >= line.strip().count('{'):
                        in_payload = False
                        payloads.append('\n'.join(current_payload))
                        current_payload = []
            
            print("\nPayloads found:")
            for payload in payloads:
                print(f"\n{payload}")
            
            # Look for successful response handling
            success_handlers = []
            for line in content.split('\n'):
                if 'response' in line.lower() and ('200' in line or 'ok' in line.lower()):
                    success_handlers.append(line.strip())
            
            print("\nSuccess handlers found:")
            for handler in success_handlers:
                print(f"- {handler}")
            
        except Exception as e:
            print(f"Error analyzing {test_file}: {str(e)}")
            continue

if __name__ == "__main__":
    asyncio.run(test_all_examples()) 