import os
import requests
from dotenv import load_dotenv

def check_available_models():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{base_url}/v1/models",
            headers=headers
        )
        response.raise_for_status()
        print("Available models:")
        print(response.json())
    except Exception as e:
        print(f"Error getting models: {e}")
        if hasattr(e, 'response'):
            print(f"Response content: {e.response.text}")

if __name__ == "__main__":
    check_available_models() 