import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent
import urllib3
import json
import requests

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_bedrock_image():
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
    
    # Test case with actual Bedrock model name and simplified prompt
    test_case = {
        "prompt": "red apple", # Simplified prompt
        "output_file": "bedrock_apple.png"
    }
    
    try:
        print("\nTesting image generation with simplified prompt")
        print(f"Prompt: {test_case['prompt']}")
        
        output_path = output_dir / test_case['output_file']
        print(f"Output path: {output_path}")
        
        # Create request payload with actual Bedrock model name
        payload = {
            "model": "amazon.titan-image-generator-v1",
            "prompt": test_case['prompt'],
            "size": "1024x1024"
        }
        
        # Make request to standard image generation endpoint
        url = f"{base_url}/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        print(f"Sending request to: {url}")
        print(f"Request payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            verify=False
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"Error response: {response.text}")
            response.raise_for_status()
        
        result = response.json()
        print(f"Response data: {json.dumps(result, indent=2)}")
        
        if result.get('data') and result['data'][0].get('url'):
            image_url = result['data'][0]['url']
            print(f"Image URL received: {image_url}")
            
            # Download and save the image
            print("Downloading image...")
            image_response = requests.get(image_url, verify=False)
            image_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(image_response.content)
            
            print(f"Image saved to: {output_path}")
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"File size: {size/1024:.1f} KB")
        else:
            print("No image URL in response")
        
    except Exception as e:
        print(f"\nTest failed: {type(e).__name__}: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response content: {e.response.text}")
    finally:
        await agent.client.close()

if __name__ == "__main__":
    asyncio.run(test_bedrock_image()) 