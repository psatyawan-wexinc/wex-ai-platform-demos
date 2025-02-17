import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import urllib3
from openai import AsyncOpenAI, DefaultAsyncHttpxClient
import httpx
import base64

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_openai_image():
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
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Test case with minimal parameters
    test_case = {
        "prompt": "A simple red apple on a white background",
        "output_file": "openai_apple.png"
    }
    
    try:
        print("\nTesting image generation with OpenAI client")
        print(f"Base URL: {base_url}")
        print(f"Prompt: {test_case['prompt']}")
        
        output_path = output_dir / test_case['output_file']
        print(f"Output path: {output_path}")
        
        # Generate image using OpenAI client with minimal parameters
        response = await client.images.generate(
            model="bedrock-titan-image-generator-v1",
            prompt=test_case['prompt'],
            size="1024x1024"
        )
        
        print("Image generation successful!")
        
        # Handle the response
        if hasattr(response.data[0], 'b64_json'):
            # If we get base64 data
            image_bytes = base64.b64decode(response.data[0].b64_json)
            with open(output_path, 'wb') as f:
                f.write(image_bytes)
            print("Saved base64 image data")
        elif hasattr(response.data[0], 'url'):
            # If we get a URL
            image_url = response.data[0].url
            print(f"Image URL received: {image_url}")
            
            async with httpx.AsyncClient(verify=False) as http_client:
                image_response = await http_client.get(image_url)
                image_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(image_response.content)
            print("Saved image from URL")
        
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"Image saved to: {output_path}")
            print(f"File size: {size/1024:.1f} KB")
        else:
            print(f"Warning: Image file not found at {output_path}")
        
    except Exception as e:
        print(f"\nTest failed: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError):
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
        raise
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_openai_image()) 