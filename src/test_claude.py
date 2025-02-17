import os
import asyncio
from pathlib import Path
import wave
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent

def print_audio_info(audio_path: str):
    """Print information about the audio file."""
    with wave.open(audio_path, 'rb') as wav:
        print(f"\nAudio file info:")
        print(f"Number of channels: {wav.getnchannels()}")
        print(f"Sample width: {wav.getsampwidth()}")
        print(f"Frame rate: {wav.getframerate()}")
        print(f"Number of frames: {wav.getnframes()}")
        print(f"Parameters: {wav.getparams()}")
        duration = wav.getnframes() / wav.getframerate()
        print(f"Duration: {duration:.2f} seconds")
        
        # Get file size
        size = Path(audio_path).stat().st_size
        print(f"File size: {size/1024/1024:.2f} MB")

async def test_claude():
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
    
    # Test audio file
    input_audio = "input.wav"
    
    # Check if input file exists and print info
    if not os.path.exists(input_audio):
        raise FileNotFoundError(f"Input audio file not found: {input_audio}")
    
    print_audio_info(input_audio)
    
    try:
        print("\nStarting transcription with Claude 3...")
        result = await agent.transcribe_audio(input_audio)
        print("\nTranscription successful!")
        print(f"Transcribed text: {result}")
    except Exception as e:
        print(f"\nTranscription failed: {type(e).__name__}: {str(e)}")
    finally:
        await agent.client.close()

if __name__ == "__main__":
    asyncio.run(test_claude()) 