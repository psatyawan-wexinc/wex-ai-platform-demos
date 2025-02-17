import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def test_workflow():
    # Load environment variables
    load_dotenv()
    
    # Get API keys
    api_key = os.getenv("API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not openai_api_key:
        raise ValueError("Please set both API_KEY and OPENAI_API_KEY in your .env file")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize agents
    wex_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    openai_url = "https://api.openai.com/v1"
    
    # Create agents for different services
    transcription_agent = MultiModalAgent(openai_api_key, openai_url)
    generation_agent = MultiModalAgent(api_key, wex_url)
    
    # Test audio file
    input_audio = "test_speech.wav"
    
    try:
        # 1. Transcribe audio
        print("\nStep 1: Transcribing audio...")
        text = await transcription_agent.transcribe_audio(input_audio)
        print(f"Transcribed text: {text}")
        
        # 2. Generate response and image prompt
        print("\nStep 2: Generating response...")
        response = await generation_agent.generate_response(text)
        text_response = response['response']
        image_prompt = response['image_prompt']
        print(f"Generated response: {text_response}")
        print(f"Image prompt: {image_prompt}")
        
        # 3. Generate image
        print("\nStep 3: Generating image...")
        image_path = await generation_agent.generate_image(
            image_prompt, 
            str(output_dir / 'response.png')
        )
        print(f"Image saved to: {image_path}")
        
        print("\nWorkflow completed successfully!")
        
    except Exception as e:
        print(f"\nWorkflow failed: {type(e).__name__}: {str(e)}")
    finally:
        await transcription_agent.client.close()
        await generation_agent.client.close()

if __name__ == "__main__":
    asyncio.run(test_workflow()) 