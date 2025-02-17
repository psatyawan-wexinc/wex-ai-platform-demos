import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent
import urllib3
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_image():
    # Load environment variables
    load_dotenv()
    
    # Get API keys
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Initialize agent with WEX API for image generation
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    print(f"Initializing agent with base URL: {base_url}")
    agent = MultiModalAgent(api_key, base_url)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory created/verified: {output_dir}")
    
    # Test cases with different types of images
    test_cases = [
        {
            "name": "sunset",
            "prompt": "A beautiful sunset over snow-capped mountains, with vibrant orange and purple clouds",
            "filename": "sunset.png"
        },
        {
            "name": "garden",
            "prompt": "A peaceful garden with blooming roses, tulips, and a small fountain",
            "filename": "garden.png"
        }
    ]
    
    try:
        for test_case in test_cases:
            print(f"\nTesting image generation: {test_case['name']}")
            print(f"Prompt: {test_case['prompt']}")
            
            output_path = output_dir / test_case['filename']
            print(f"Output path: {output_path}")
            
            try:
                image_path = await agent.generate_image(
                    test_case['prompt'],
                    str(output_path)
                )
                print(f"Image generation successful!")
                print(f"Image saved to: {image_path}")
                print("-" * 80)
                
            except Exception as e:
                print(f"Failed to generate {test_case['name']}: {type(e).__name__}: {str(e)}")
                continue
            
    except Exception as e:
        print(f"\nTest execution failed: {type(e).__name__}: {str(e)}")
    finally:
        await agent.client.close()

if __name__ == "__main__":
    asyncio.run(test_image()) 