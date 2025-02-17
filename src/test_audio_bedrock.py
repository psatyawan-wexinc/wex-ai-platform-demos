import os
import asyncio
from pathlib import Path
import httpx
import json
import base64
from typing import Optional, BinaryIO

class AudioTranscriber:
    """Bedrock Audio Transcription Client"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "multipart/form-data"
        }
    
    async def transcribe_audio(
        self,
        audio_file: BinaryIO,
        language: Optional[str] = None
    ) -> dict:
        """Transcribe audio using multipart form data"""
        
        # Prepare the multipart form data
        files = {
            'file': ('audio.wav', audio_file, 'audio/wav'),
            'model': (None, 'bedrock-claude-v2')
        }
        
        if language:
            files['language'] = (None, language)
        
        # Make the API request
        url = f"{self.base_url}/audio/transcriptions"
        
        print(f"\nSending transcription request to: {url}")
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                files=files,
                timeout=30.0
            )
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                print(f"Request files: {files}")
                response.raise_for_status()
            
            return response.json()

async def test_transcription():
    """Test the audio transcription functionality"""
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
    transcriber = AudioTranscriber(api_key, base_url)
    
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
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Duration: {duration} seconds")
        print(f"Frequency: {frequency} Hz")
        
        # Open and transcribe the audio file
        with open(output_wav, 'rb') as audio_file:
            result = await transcriber.transcribe_audio(
                audio_file,
                language="en"
            )
        
        print("\nTranscription result:")
        print(json.dumps(result, indent=2))
        
        # Save transcription to file
        output_text = output_dir / "transcription.txt"
        with open(output_text, 'w') as f:
            if 'text' in result:
                f.write(result['text'])
                print(f"\nTranscription saved to: {output_text}")
            else:
                print("No transcription text in response")
    
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        if isinstance(e, httpx.HTTPError) and hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response headers: {dict(e.response.headers)}")
            print(f"Response content: {e.response.text}")
        raise
    finally:
        # Clean up test file
        try:
            if output_wav.exists():
                output_wav.unlink()
                print(f"\nCleaned up test file: {output_wav}")
        except PermissionError:
            print(f"Note: Could not delete test file {output_wav} - it may be in use")

if __name__ == "__main__":
    asyncio.run(test_transcription()) 