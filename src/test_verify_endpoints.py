import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import urllib3
import httpx
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_verify_endpoints():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Base URLs to test
    base_urls = [
        "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com",
        "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com/v1",
        "https://aig.dev.ai-platform.ext.wexfabric.com",
        "https://aig.dev.ai-platform.ext.wexfabric.com/v1"
    ]
    
    # Endpoints to test
    endpoints = [
        "/v1/models",
        "/v1/images/generations",
        "/bedrock/invoke",
        "/bedrock/images/generations",
        "/health",
        "/docs"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print("\nVerifying API endpoints...")
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            for base_url in base_urls:
                print(f"\nTesting base URL: {base_url}")
                
                for endpoint in endpoints:
                    url = f"{base_url}{endpoint}".replace("//v1", "/v1")
                    try:
                        print(f"\nTesting endpoint: {url}")
                        
                        # Try GET request first
                        response = await client.get(
                            url,
                            headers=headers
                        )
                        
                        print(f"GET Status: {response.status_code}")
                        print(f"Headers: {dict(response.headers)}")
                        
                        if response.status_code < 500:  # Include 4xx to see error messages
                            try:
                                print(f"Response: {json.dumps(response.json(), indent=2)}")
                            except:
                                print(f"Raw response: {response.text[:200]}...")
                        
                        # If it's an image endpoint, try a POST request
                        if 'image' in endpoint:
                            test_payload = {
                                "model": "bedrock-titan-image-generator-v1",
                                "prompt": "test",
                                "size": "1024x1024"
                            }
                            
                            print(f"\nTesting POST to {url}")
                            print(f"Payload: {json.dumps(test_payload, indent=2)}")
                            
                            response = await client.post(
                                url,
                                headers=headers,
                                json=test_payload
                            )
                            
                            print(f"POST Status: {response.status_code}")
                            print(f"Headers: {dict(response.headers)}")
                            
                            if response.status_code < 500:
                                try:
                                    print(f"Response: {json.dumps(response.json(), indent=2)}")
                                except:
                                    print(f"Raw response: {response.text[:200]}...")
                    
                    except Exception as e:
                        print(f"Error testing {url}: {type(e).__name__}: {str(e)}")
                        continue
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError):
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
        raise

if __name__ == "__main__":
    asyncio.run(test_verify_endpoints()) 