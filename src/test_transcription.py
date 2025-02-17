import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent

async def test_transcription():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set the API_KEY in your .env file")
    
    # Initialize agent with the correct base URL from example
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    print(f"Initializing agent with base URL: {base_url}")
    agent = MultiModalAgent(api_key, base_url)
    
    # Test audio file
    input_audio = "input.wav"
    
    # Check if input file exists
    if not os.path.exists(input_audio):
        raise FileNotFoundError(f"Input audio file not found: {input_audio}")
    
    try:
        print("Starting transcription...")
        # Test transcription
        result = await agent.transcribe_audio(input_audio)
        print("\nTranscription successful!")
        print(f"Transcribed text: {result}")
    except Exception as e:
        print(f"\nTranscription failed: {type(e).__name__}: {str(e)}")
        raise
    finally:
        print("\nCleaning up...")
        await agent.client.close()

if __name__ == "__main__":
    try:
        asyncio.run(test_transcription())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {type(e).__name__}: {str(e)}") 