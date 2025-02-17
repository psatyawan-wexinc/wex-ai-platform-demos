import os
import asyncio
from pathlib import Path
import httpx
import json
from typing import Optional, BinaryIO, AsyncGenerator
from openai import AsyncOpenAI

class AudioTranscriberStream:
    """Streaming Audio Transcription Client"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "multipart/form-data"
        }
    
    async def transcribe_audio_stream(
        self,
        audio_file: BinaryIO,
        language: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Transcribe audio with streaming response using the audio API
        """
        # Prepare multipart form data
        files = {
            'file': ('audio.wav', audio_file, 'audio/wav'),
            'model': (None, 'whisper-1'),
            'language': (None, language or 'en'),
            'response_format': (None, 'text')
        }
        
        # Make the API request
        url = f"{self.base_url}/audio/transcriptions"
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                files=files,
                timeout=60.0
            )
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                response.raise_for_status()
            
            # Stream the response text
            text = response.text
            chunk_size = 100  # Stream in small chunks
            for i in range(0, len(text), chunk_size):
                yield text[i:i + chunk_size]

async def test_transcription():
    """Test the streaming audio transcription"""
    from dotenv import load_dotenv
    import urllib3
    import wave
    
    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set API_KEY in your .env file")
    
    # Initialize transcriber
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    transcriber = AudioTranscriberStream(api_key, base_url)
    
    # Input and output paths
    input_wav = "input.wav"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Print audio file info
        with wave.open(input_wav, 'rb') as wav_file:
            print(f"\nAudio file info:")
            print(f"Number of channels: {wav_file.getnchannels()}")
            print(f"Sample width: {wav_file.getsampwidth()}")
            print(f"Frame rate: {wav_file.getframerate()}")
            print(f"Number of frames: {wav_file.getnframes()}")
            duration = wav_file.getnframes() / wav_file.getframerate()
            print(f"Duration: {duration:.2f} seconds")
            
            # Get file size
            size = Path(input_wav).stat().st_size
            print(f"File size: {size/1024/1024:.2f} MB")
        
        # Open and transcribe the audio file with streaming
        transcription = ""
        with open(input_wav, 'rb') as audio_file:
            print("\nStarting transcription stream:")
            async for chunk in transcriber.transcribe_audio_stream(
                audio_file,
                language="en"
            ):
                print(chunk, end="", flush=True)
                transcription += chunk
        
        print("\n\nFinal transcription:")
        print(transcription)
        
        # Save transcription to file
        output_text = output_dir / "transcription.txt"
        with open(output_text, 'w') as f:
            f.write(transcription)
            print(f"\nTranscription saved to: {output_text}")
    
    except FileNotFoundError:
        print(f"\nError: Input file '{input_wav}' not found")
        raise
    except Exception as e:
        print(f"\nError: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError) and hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response headers: {dict(e.response.headers)}")
            print(f"Response content: {e.response.text}")
        raise

if __name__ == "__main__":
    asyncio.run(test_transcription()) 