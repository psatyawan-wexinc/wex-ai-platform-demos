import os
import asyncio
from pathlib import Path
import httpx
import json
from typing import Optional, BinaryIO

class MultiModalAgentAudio:
    """Simplified MultiModal Agent for audio processing only"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
    
    async def list_models(self) -> dict:
        """List available models"""
        url = f"{self.base_url}/v1/models"
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(
                url,
                headers=self.headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                response.raise_for_status()
            
            return response.json()
    
    async def transcribe_audio(
        self,
        audio_file: BinaryIO,
        model: Optional[str] = None,  # Will be set after checking available models
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> dict:
        """
        Transcribe audio file using the specified model.
        
        Args:
            audio_file: Audio file object
            model: Model to use for transcription
            language: Optional language code
            prompt: Optional prompt to guide transcription
        
        Returns:
            dict: Transcription result
        """
        # Check available models first
        models = await self.list_models()
        print("\nAvailable models:")
        for model_info in models.get('data', []):
            print(f"- {model_info['id']}")
        
        # Use first available model that mentions 'speech' or 'audio'
        if not model:
            for model_info in models.get('data', []):
                model_id = model_info['id'].lower()
                if 'speech' in model_id or 'audio' in model_id or 'whisper' in model_id:
                    model = model_info['id']
                    print(f"\nSelected model: {model}")
                    break
        
        if not model:
            raise ValueError("No suitable audio transcription model found")
        
        # Prepare the multipart form data
        files = {
            'file': ('audio.wav', audio_file, 'audio/wav'),
            'model': (None, model)
        }
        
        # Add optional parameters if provided
        if language:
            files['language'] = (None, language)
        if prompt:
            files['prompt'] = (None, prompt)
        
        # Make the API request
        url = f"{self.base_url}/v1/audio/transcriptions"
        
        print(f"\nSending transcription request to: {url}")
        print(f"Model: {model}")
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                url,
                headers=self.headers,
                files=files,
                timeout=30.0
            )
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
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
    
    # Initialize agent
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    agent = MultiModalAgentAudio(api_key, base_url)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Create a test WAV file
    output_wav = output_dir / "test_audio.wav"
    
    try:
        # Generate a simple WAV file
        sample_rate = 44100
        duration = 1  # seconds
        
        with wave.open(str(output_wav), 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(sample_rate)
            # Generate 1 second of silence
            wav_file.writeframes(b'\x00' * (sample_rate * 2))
        
        print(f"\nCreated test audio file: {output_wav}")
        
        # Open and transcribe the audio file
        with open(output_wav, 'rb') as audio_file:
            # Transcribe the audio without specifying model (will auto-select)
            result = await agent.transcribe_audio(
                audio_file,
                language="en",
                prompt="This is a test transcription"
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