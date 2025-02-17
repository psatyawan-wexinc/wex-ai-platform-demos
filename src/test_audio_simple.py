import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import urllib3
import httpx
import json
import wave

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_audio_transcription():
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
        print("\nTesting audio transcription...")
        
        # Create a simple test WAV file
        sample_rate = 44100
        duration = 1  # seconds
        output_wav = output_dir / "test_audio.wav"
        
        with wave.open(str(output_wav), 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(sample_rate)
            # Generate 1 second of silence
            wav_file.writeframes(b'\x00' * (sample_rate * 2))
        
        print(f"Created test audio file: {output_wav}")
        
        # Prepare transcription request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        # Create form data with the audio file
        files = {
            'file': ('test_audio.wav', open(output_wav, 'rb'), 'audio/wav'),
            'model': (None, 'whisper-1')
        }
        
        url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com/v1/audio/transcriptions"
        
        print(f"\nSending request to: {url}")
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                url,
                headers=headers,
                files=files,
                timeout=30.0
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                response.raise_for_status()
            
            result = response.json()
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
        if isinstance(e, httpx.HTTPError):
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
            print(f"Request URL: {url}")
            print(f"Request headers: {headers}")
        raise
    finally:
        # Clean up test audio file
        if output_wav.exists():
            output_wav.unlink()
            print(f"\nCleaned up test file: {output_wav}")

if __name__ == "__main__":
    asyncio.run(test_audio_transcription()) 