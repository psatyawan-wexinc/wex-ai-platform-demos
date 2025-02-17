import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI, DefaultAsyncHttpxClient
import httpx

async def list_models():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set the API_KEY in your .env file")
    
    # Initialize client
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
        http_client=DefaultAsyncHttpxClient(
            verify=False,
            timeout=httpx.Timeout(30.0),
            http2=True
        )
    )
    
    try:
        print("Fetching available models...")
        models = await client.models.list()
        
        print("\nAvailable models:")
        for model in models.data:
            print(f"- {model.id}")
            
        # Look specifically for audio/transcription models
        print("\nPotential audio transcription models:")
        audio_models = [m for m in models.data if any(x in m.id.lower() for x in ['whisper', 'audio', 'speech', 'transcribe'])]
        for model in audio_models:
            print(f"- {model.id}")
            
    except Exception as e:
        print(f"Error listing models: {type(e).__name__}: {str(e)}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(list_models()) 