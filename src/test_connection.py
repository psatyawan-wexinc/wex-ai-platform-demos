import os
import asyncio
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent

async def test_connection():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set the API_KEY in your .env file")
    
    # Initialize agent
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    print(f"Initializing agent with base URL: {base_url}")
    agent = MultiModalAgent(api_key, base_url)
    
    try:
        print("Testing simple chat completion...")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ]
        
        response = await agent.client.chat.completions.create(
            model="azure-gpt-4o",
            messages=messages
        )
        
        print("\nConnection successful!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"\nConnection failed: {type(e).__name__}: {str(e)}")
        raise
    finally:
        print("\nCleaning up...")
        await agent.client.close()

if __name__ == "__main__":
    try:
        asyncio.run(test_connection())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {type(e).__name__}: {str(e)}") 