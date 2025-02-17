import os
import asyncio
from pathlib import Path
import httpx
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

async def list_available_models():
    """List all available models"""
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Initialize client
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
        http_client=httpx.AsyncClient(
            verify=False,
            timeout=30.0
        )
    )
    
    try:
        # List models
        models = await client.models.list()
        
        print("\nAvailable Models:")
        for model in models.data:
            print(f"- {model.id}")
            print(f"  Created: {model.created}")
            print(f"  Owned by: {model.owned_by}")
            if hasattr(model, 'permission'):
                print(f"  Permissions: {model.permission}")
            print()
        
        return models.data
        
    except Exception as e:
        print(f"Error listing models: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError) and hasattr(e, 'response'):
            print(f"Response content: {e.response.text}")
        raise
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(list_available_models()) 