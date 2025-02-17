import requests
import json
from typing import Optional, Dict, Any
from pathlib import Path
import base64
import os
import httpx
from openai import AsyncOpenAI, DefaultAsyncHttpxClient

class MultiModalAgent:
    def __init__(self, api_key: str, base_url: str):
        """Initialize the multi-modal agent."""
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "multipart/form-data"
        }
        
        # Create OpenAI client with proper SSL handling and longer timeout
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=self.base_url,
            http_client=DefaultAsyncHttpxClient(
                verify=False,  # Disable SSL verification for development
                timeout=httpx.Timeout(300.0, connect=60.0)  # Increase timeout to 5 minutes
            )
        )
        print(f"Initialized client with base URL: {self.base_url}")

    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file using OpenAI's Whisper model"""
        
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        # Prepare the multipart form data
        files = {
            'file': ('audio.wav', open(audio_file_path, 'rb'), 'audio/wav'),
            'model': (None, 'whisper-1')
        }
        
        # Make the API request
        url = f"{self.base_url}/audio/transcriptions"
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                files=files,
                timeout=30.0
            )
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                response.raise_for_status()
            
            result = response.json()
            return result['text']

    async def generate_response(self, text: str) -> Dict[str, Any]:
        """Generate chat completion response using Azure GPT-4."""
        messages = [
            {
                "role": "system",
                "content": """You are a helpful assistant that provides responses in JSON format. 
                Always include both a text response and an image prompt in your JSON output.
                Format your response as: {"response": "detailed text response", "image_prompt": "clear image generation prompt"}"""
            },
            {
                "role": "user",
                "content": f"Create a response to: '{text}'. Return your response in JSON format with 'response' and 'image_prompt' fields."
            }
        ]
        
        response = await self.client.chat.completions.create(
            model="azure-gpt-4o",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Raw response: {response.choices[0].message.content}")
            raise

    async def generate_image(self, prompt: str, output_path: str) -> str:
        """Generate image using Bedrock Titan."""
        try:
            print(f"Generating image with prompt: {prompt}")
            
            # Use the OpenAI client for image generation with minimal parameters
            response = await self.client.images.generate(
                model="bedrock-titan-image-generator-v1",
                prompt=prompt,
                size="1024x1024"
            )
            
            print("Image generation successful!")
            
            # Handle the response
            if hasattr(response.data[0], 'b64_json'):
                # If we get base64 data
                image_bytes = base64.b64decode(response.data[0].b64_json)
                with open(output_path, 'wb') as f:
                    f.write(image_bytes)
                print("Saved base64 image data")
            elif hasattr(response.data[0], 'url'):
                # If we get a URL
                image_url = response.data[0].url
                print(f"Image URL received: {image_url}")
                
                async with httpx.AsyncClient(verify=False) as client:
                    image_response = await client.get(image_url)
                    image_response.raise_for_status()
                    
                    with open(output_path, 'wb') as f:
                        f.write(image_response.content)
                print("Saved image from URL")
            
            print(f"Image saved to: {output_path}")
            return output_path

        except Exception as e:
            print(f"Error in image generation: {type(e).__name__}: {str(e)}")
            if isinstance(e, httpx.HTTPError):
                print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
            raise

    async def process_input(self, audio_file_path: str, output_dir: Path) -> Dict[str, str]:
        """Process voice input and generate multi-modal response."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Transcribe audio to text
        text = await self.transcribe_audio(audio_file_path)
        print(f"Transcribed text: {text}")
        
        # 2. Generate response and image prompt
        response = await self.generate_response(text)
        text_response = response['response']
        image_prompt = response['image_prompt']
        print(f"Generated response: {text_response}")
        print(f"Image prompt: {image_prompt}")
        
        # 3. Generate image
        image_path = await self.generate_image(
            image_prompt, 
            str(output_dir / 'response.png')
        )
        
        return {
            'transcription': text,
            'response_text': text_response,
            'image_file': image_path
        } 