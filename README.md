# WEX AI Platform Demos

This repository contains demo applications showcasing the capabilities of the WEX AI Platform, including audio transcription, image generation, and model interaction examples.

## Features

- **Audio Processing**
  - Audio transcription with streaming support
  - Multiple model support (Claude, Whisper)
  - WAV file handling and processing

- **Image Generation**
  - Support for multiple image generation models
  - Titan Image Generator integration
  - Bedrock model support
  - Various image generation approaches (direct, streaming)

- **Model Verification**
  - Model availability checking
  - Endpoint verification
  - API compatibility testing

## Project Structure 

## Setup and Usage



## Contact

**Author:** Nick Sudh  
**Email:** nick.sudh@wexinc.com

## License

This project is proprietary and confidential. All rights reserved.

## Support

For support, please contact the WEX AI Platform team.

## Working Status

### Verified Working ✅
- `test_connection.py` - Successfully connects to API and gets response from GPT model
- `test_verify_models.py` - Successfully lists available models

### Needs Configuration ⚙️
- `test_bedrock_invoke.py` - Needs correct endpoint configuration for image generation
- `test_audio.py` - Needs correct OpenAI API configuration

### Not Working ❌
- `check_models.py` - Models endpoint returning 404 error
- `test_agent.py` - MultiModalAgent implementation needs updating
- `test_audio_stream.py` - Audio transcription endpoint not found
- `test_audio_bedrock.py` - Audio transcription endpoint not found
- `test_audio_simple.py` - Audio transcription endpoint not found
- `test_image_models.py` - Image generation endpoint not found
- `test_titan_image.py` - Image generation endpoint not found
- `test_minimal_image.py` - Image generation endpoint not found
- `test_openai_image.py` - Image generation endpoint not found

### Not Yet Tested 🔄
- `test_image.py`
- `test_bedrock_direct.py` - Testing in progress...
- `test_combined_image.py`

## Contact

**Author:** Nick Sudh  
**Email:** nick.sudh@wexinc.com

## License

This project is proprietary and confidential. All rights reserved.

## Support

For support, please contact the WEX AI Platform team. 