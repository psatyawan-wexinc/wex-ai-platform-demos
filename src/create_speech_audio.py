import numpy as np
import wave
import math

def create_speech_audio(filename: str = "test_speech.wav", duration: float = 2.0):
    """Create a test audio file that simulates speech frequencies."""
    # Audio parameters
    sample_rate = 16000  # Common for speech
    
    # Time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a signal that mimics speech frequencies (300-3400 Hz)
    frequencies = [300, 1000, 2000, 3000]  # Common speech frequencies
    audio = np.zeros_like(t)
    
    for freq in frequencies:
        # Add frequency with varying amplitude
        amplitude = np.exp(-t) * np.sin(2 * np.pi * 5 * t)  # Envelope
        audio += amplitude * np.sin(2 * np.pi * freq * t)
    
    # Normalize and convert to 16-bit PCM
    audio = audio / np.max(np.abs(audio))
    audio = np.int16(audio * 32767)
    
    # Save as WAV file
    with wave.open(filename, 'wb') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav.setframerate(sample_rate)
        wav.writeframes(audio.tobytes())
    
    print(f"Created test speech audio file: {filename}")
    return filename

if __name__ == "__main__":
    create_speech_audio("test_speech.wav", duration=2.0) 