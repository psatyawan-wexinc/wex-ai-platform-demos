import os
import asyncio
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent
import urllib3
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_response():
    # Load environment variables
    load_dotenv()
    
    # Get API keys
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Initialize agent with WEX API for chat completion
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    print(f"Initializing agent with base URL: {base_url}")
    agent = MultiModalAgent(api_key, base_url)
    
    # Test cases
    test_cases = [
        "Create a description of a beautiful sunset over mountains",
        "Describe a futuristic city with flying cars",
        "Tell me about a peaceful garden with blooming flowers"
    ]
    
    try:
        for test_text in test_cases:
            print(f"\nTesting with input: {test_text}")
            print("Generating response...")
            
            result = await agent.generate_response(test_text)
            
            print("\nResponse generation successful!")
            print("Text response:", json.dumps(result.get('response', ''), indent=2))
            print("Image prompt:", json.dumps(result.get('image_prompt', ''), indent=2))
            print("-" * 80)
            
    except Exception as e:
        print(f"\nResponse generation failed: {type(e).__name__}: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response content: {e.response.text}")
    finally:
        await agent.client.close()

if __name__ == "__main__":
    asyncio.run(test_response()) 