import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import urllib3
import httpx
import json
import base64
from openai import AsyncOpenAI

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_combined_image():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    try:
        print("\nTrying direct API call...")
        
        # Try direct API call with exact model name from /v1/models
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model": "bedrock-titan-image-generator-v1",  # Exact name from models list
            "prompt": "A simple red apple on a white background"
        }
        
        url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com/v1/images/generations"
        
        async with httpx.AsyncClient(verify=False) as client:
            print(f"Sending request to: {url}")
            print(f"Request payload: {json.dumps(payload, indent=2)}")
            
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
                output_path = output_dir / "combined_apple.png"
                
                if 'b64_json' in image_data:
                    # Handle base64 response
                    image_bytes = base64.b64decode(image_data['b64_json'])
                    with open(output_path, 'wb') as f:
                        f.write(image_bytes)
                    print(f"Saved base64 image to: {output_path}")
                elif 'url' in image_data:
                    # Handle URL response
                    image_url = image_data['url']
                    print(f"Image URL received: {image_url}")
                    
                    async with httpx.AsyncClient(verify=False) as http_client:
                        image_response = await http_client.get(image_url)
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
    asyncio.run(test_combined_image()) 