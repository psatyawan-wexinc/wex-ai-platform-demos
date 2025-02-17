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

async def test_minimal_image():
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
        
        # Create request based on OpenAPI spec
        payload = {
            "model": "amazon.titan-image-generator-v1",  # Changed based on OpenAPI spec
            "prompt": "A simple red apple on a white background",
            "response_format": "b64_json"  # Added based on OpenAPI spec
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Use the v1 endpoint
        url = f"{base_url}/v1/images/generations"
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
            
            # Handle response data
            if 'data' in result and result['data']:
                image_data = result['data'][0]
                if 'b64_json' in image_data:
                    # Handle base64 data
                    image_bytes = base64.b64decode(image_data['b64_json'])
                    output_path = output_dir / "minimal_apple.png"
                    with open(output_path, 'wb') as f:
                        f.write(image_bytes)
                    print(f"Saved base64 image to: {output_path}")
                elif 'url' in image_data:
                    # Handle URL response
                    image_url = image_data['url']
                    print(f"Image URL received: {image_url}")
                    
                    # Download the image
                    output_path = output_dir / "minimal_apple.png"
                    image_response = await client.get(image_url)
                    image_response.raise_for_status()
                    
                    with open(output_path, 'wb') as f:
                        f.write(image_response.content)
                    print(f"Saved URL image to: {output_path}")
                
                if os.path.exists(output_path):
                    size = os.path.getsize(output_path)
                    print(f"File size: {size/1024:.1f} KB")
            else:
                print("No image data in response")
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError):
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
            print(f"Request URL: {url}")
            print(f"Request headers: {headers}")
            print(f"Request payload: {json.dumps(payload, indent=2)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_minimal_image()) 