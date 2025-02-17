import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import urllib3
import httpx
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_list_models():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Use internal URL with /v1 path
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com/v1"
    
    try:
        print("\nFetching available models...")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{base_url}/models"
        print(f"Sending request to: {url}")
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(
                url,
                headers=headers,
                timeout=60.0
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                response.raise_for_status()
            
            result = response.json()
            
            print("\nAvailable models:")
            for model in result.get('data', []):
                print(f"\nModel ID: {model.get('id')}")
                print(f"Created: {model.get('created')}")
                print(f"Owned by: {model.get('owned_by')}")
                print("Full model data:", json.dumps(model, indent=2))
            
            # Filter for image-related models
            image_models = [
                model for model in result.get('data', [])
                if any(term in model.get('id', '').lower() for term in ['image', 'dall', 'titan'])
            ]
            
            print("\nImage-related models:")
            for model in image_models:
                print(f"- {model.get('id')}")
        
    except Exception as e:
        print(f"\nTest failed: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError):
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
            print(f"Request URL: {url}")
            print(f"Request headers: {headers}")
        raise

if __name__ == "__main__":
    asyncio.run(test_list_models()) 