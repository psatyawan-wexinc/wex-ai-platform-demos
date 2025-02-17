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

async def test_simple_image():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Initialize HTTP client
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    try:
        print("\nGenerating image...")
        
        # Create simplified Bedrock request
        payload = {
            "modelId": "amazon.titan-image-generator-v1",
            "input": {
                "mode": "text-image",
                "text": "A simple red apple on a white background",
                "width": 1024,
                "height": 1024,
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0
            }
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Use Bedrock invoke endpoint
        url = f"{base_url}/bedrock/invoke"
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
            
            # Handle base64 image data
            if 'artifacts' in result and result['artifacts']:
                image_data = result['artifacts'][0].get('base64')
                if image_data:
                    # Save the image
                    output_path = output_dir / "simple_apple.png"
                    image_bytes = base64.b64decode(image_data)
                    with open(output_path, 'wb') as f:
                        f.write(image_bytes)
                    
                    print(f"Image saved to: {output_path}")
                    if os.path.exists(output_path):
                        size = os.path.getsize(output_path)
                        print(f"File size: {size/1024:.1f} KB")
                else:
                    print("No base64 image data in response")
            else:
                print("No artifacts in response")
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError):
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
            print(f"Request URL: {url}")
            print(f"Request headers: {headers}")
            print(f"Request payload: {json.dumps(payload, indent=2)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_simple_image()) 