import os
import asyncio
from pathlib import Path
import wave
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent
import httpx
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

async def test_audio():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    print("OpenAI API key loaded successfully")
    
    # Initialize agent
    base_url = "https://api.openai.com/v1"  # Use OpenAI API directly
    print(f"Initializing agent with base URL: {base_url}")
    agent = MultiModalAgent(api_key, base_url)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Create a test WAV file
    output_wav = output_dir / "test_audio.wav"
    
    try:
        # Generate a simple WAV file with a sine wave
        sample_rate = 44100
        duration = 1  # seconds
        frequency = 440  # Hz (A4 note)
        
        import numpy as np
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        samples = (32767 * np.sin(2 * np.pi * frequency * t)).astype(np.int16)
        
        with wave.open(str(output_wav), 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(samples.tobytes())
        
        print(f"\nCreated test audio file: {output_wav}")
        
        # Transcribe the audio
        result = await agent.transcribe_audio(str(output_wav))
        
        print("\nTranscription result:")
        print(result)
        
        # Save transcription to file
        output_text = output_dir / "transcription.txt"
        with open(output_text, 'w') as f:
            f.write(result)
            print(f"\nTranscription saved to: {output_text}")
    
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise
    finally:
        # Clean up test file
        if output_wav.exists():
            output_wav.unlink()
            print(f"\nCleaned up test file: {output_wav}")

if __name__ == "__main__":
    asyncio.run(test_audio()) 