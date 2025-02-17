import wave
import numpy as np

def create_test_audio(filename: str = "test.wav", duration: float = 1.0):
    """Create a test audio file with a simple tone."""
    # Audio parameters
    sample_rate = 44100
    frequency = 440  # Hz (A4 note)
    
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate sine wave
    tone = np.sin(2 * np.pi * frequency * t)
    
    # Normalize to 16-bit range
    audio = np.int16(tone * 32767)
    
    # Save as WAV file
    with wave.open(filename, 'wb') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav.setframerate(sample_rate)
        wav.writeframes(audio.tobytes())
    
    print(f"Created test audio file: {filename}")
    return filename

if __name__ == "__main__":
    create_test_audio("test.wav", duration=1.0) 