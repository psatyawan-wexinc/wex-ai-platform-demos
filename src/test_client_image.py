import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_client_image():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Initialize agent
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    print(f"Initializing agent with base URL: {base_url}")
    agent = MultiModalAgent(api_key, base_url)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Test case
    test_case = {
        "prompt": "red apple",
        "output_file": "client_apple.png"
    }
    
    try:
        print("\nTesting image generation using OpenAI client")
        print(f"Prompt: {test_case['prompt']}")
        
        output_path = output_dir / test_case['output_file']
        print(f"Output path: {output_path}")
        
        # Generate image using the agent
        image_path = await agent.generate_image(
            test_case['prompt'],
            str(output_path)
        )
        
        if os.path.exists(image_path):
            size = os.path.getsize(image_path)
            print(f"Image generation successful!")
            print(f"Image saved to: {image_path}")
            print(f"File size: {size/1024:.1f} KB")
        else:
            print(f"Warning: Image file not found at {image_path}")
        
    except Exception as e:
        print(f"\nTest failed: {type(e).__name__}: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response content: {e.response.text}")
    finally:
        await agent.client.close()

if __name__ == "__main__":
    asyncio.run(test_client_image())