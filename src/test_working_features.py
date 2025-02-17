import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import urllib3
import httpx
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_working_features():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        print("\nTesting Working Features:")
        
        async with httpx.AsyncClient(verify=False) as client:
            # 1. Test /v1/models endpoint
            print("\n1. Testing Models List:")
            url = f"{base_url}/v1/models"
            response = await client.get(url, headers=headers)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                models = response.json()
                print("\nAvailable Models:")
                for model in models.get('data', []):
                    print(f"- {model.get('id')}")
                    print(f"  Created: {model.get('created')}")
                    print(f"  Owner: {model.get('owned_by')}")
            
            # 2. Test model categories
            print("\n2. Model Categories:")
            models_data = response.json().get('data', [])
            
            # Group models by type
            image_models = [m for m in models_data if any(x in m['id'].lower() for x in ['image', 'dall'])]
            text_models = [m for m in models_data if any(x in m['id'].lower() for x in ['gpt', 'text', 'claude'])]
            embedding_models = [m for m in models_data if 'embed' in m['id'].lower()]
            
            print("\nImage Models:")
            for m in image_models:
                print(f"- {m['id']}")
            
            print("\nText/Chat Models:")
            for m in text_models:
                print(f"- {m['id']}")
            
            print("\nEmbedding Models:")
            for m in embedding_models:
                print(f"- {m['id']}")
            
            # 3. Test health endpoint if available
            print("\n3. Testing Health Endpoint:")
            try:
                health_url = f"{base_url}/health"
                health_response = await client.get(health_url, headers=headers)
                print(f"Health Status: {health_response.status_code}")
                if health_response.status_code < 500:
                    print(json.dumps(health_response.json(), indent=2))
            except Exception as e:
                print(f"Health endpoint not available: {str(e)}")
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError):
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
        raise

if __name__ == "__main__":
    asyncio.run(test_working_features()) 