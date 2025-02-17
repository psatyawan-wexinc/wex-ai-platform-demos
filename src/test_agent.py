import os
from pathlib import Path
from dotenv import load_dotenv
from multi_modal_agent import MultiModalAgent

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variable
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Please set the API_KEY in your .env file")
    
    # Initialize agent
    base_url = "https://aips-ai-gateway.ue1.dev.ai-platform.int.wexfabric.com"
    agent = MultiModalAgent(api_key, base_url)
    
    # Set up paths
    input_audio = "input.wav"  # Your input audio file
    output_dir = Path("output")
    
    # Check if input file exists
    if not os.path.exists(input_audio):
        raise FileNotFoundError(f"Input audio file not found: {input_audio}")
    
    # Process input
    try:
        result = agent.process_input(input_audio, output_dir)
        print("Processing complete!")
        print(f"Transcription: {result['transcription']}")
        print(f"Response text: {result['response_text']}")
        print(f"Speech file: {result['speech_file']}")
        print(f"Image file: {result['image_file']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 