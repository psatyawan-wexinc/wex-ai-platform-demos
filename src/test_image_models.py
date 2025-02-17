import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import urllib3
from openai import AsyncOpenAI, DefaultAsyncHttpxClient
import httpx
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_image_models():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Initialize OpenAI client with the correct base URL format
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com/v1"
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
        http_client=DefaultAsyncHttpxClient(
            verify=False,
            timeout=httpx.Timeout(60.0)
        )
    )
    
    try:
        print("\nFetching available models...")
        models = await client.models.list()
        
        print("\nImage-related models:")
        image_models = [
            model for model in models.data 
            if any(term in model.id.lower() for term in ['image', 'dall', 'titan'])
        ]
        
        for model in image_models:
            print(f"\nModel ID: {model.id}")
            print(f"Created: {model.created}")
            print(f"Owned by: {model.owned_by}")
            print("Full model data:", json.dumps(model.model_dump(), indent=2))
            
        print("\nTesting each image model...")
        for model in image_models:
            print(f"\nTesting model: {model.id}")
            try:
                response = await client.images.generate(
                    model=model.id,
                    prompt="A simple red apple",
                    size="1024x1024"
                )
                print(f"✓ Model {model.id} works!")
                print("Response:", json.dumps(response.model_dump(), indent=2))
            except Exception as e:
                print(f"✗ Model {model.id} failed: {str(e)}")
        
    except Exception as e:
        print(f"\nTest failed: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError):
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
        raise
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_image_models()) 