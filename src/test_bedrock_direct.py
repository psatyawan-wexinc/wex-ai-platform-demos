import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import urllib3
import httpx
import json
import base64

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_bedrock_direct():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Use internal URL with /v1 path
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com/v1"
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Test case with minimal parameters
    test_case = {
        "prompt": "A simple red apple on a white background",
        "output_file": "bedrock_direct.png"
    }
    
    try:
        print("\nTesting Bedrock direct image generation")
        print(f"Base URL: {base_url}")
        print(f"Prompt: {test_case['prompt']}")
        
        output_path = output_dir / test_case['output_file']
        print(f"Output path: {output_path}")
        
        # Create request with minimal parameters
        payload = {
            "model": "titan-image-generator-v1",
            "prompt": test_case['prompt'],
            "size": "1024x1024"
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Use the images endpoint
        url = f"{base_url}/images/generations"
        print(f"Sending request to: {url}")
        print(f"Request payload: {json.dumps(payload, indent=2)}")
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=60.0
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                response.raise_for_status()
            
            result = response.json()
            print(f"Response data: {json.dumps(result, indent=2)}")
            
            # Handle URL response
            if 'data' in result and result['data']:
                image_url = result['data'][0].get('url')
                if image_url:
                    print(f"Image URL received: {image_url}")
                    
                    # Download the image
                    image_response = await client.get(image_url)
                    image_response.raise_for_status()
                    
                    with open(output_path, 'wb') as f:
                        f.write(image_response.content)
                    print(f"Image saved to: {output_path}")
                    
                    if os.path.exists(output_path):
                        size = os.path.getsize(output_path)
                        print(f"File size: {size/1024:.1f} KB")
                else:
                    print("No image URL in response")
            else:
                print("No data in response")
        
    except Exception as e:
        print(f"\nTest failed: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError):
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
            print(f"Request URL: {url}")
            print(f"Request headers: {headers}")
            print(f"Request payload: {json.dumps(payload, indent=2)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_bedrock_direct()) 