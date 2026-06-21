import numpy as np
import soundfile as sf
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.speech_processing.audio_capture import AudioCapture
from src.speech_processing.noise_reduction import NoiseReducer
from src.speech_processing.vad import VoiceActivityDetector
from src.speech_processing.speech_to_text import SpeechToTextProcessor

def verify_pipeline():
    print("--- Audio Pipeline Verification ---")
    
    capture = AudioCapture()
    reducer = NoiseReducer()
    vad = VoiceActivityDetector()
    processor = SpeechToTextProcessor()
    
    print("\n1. Testing Recording (3 seconds)...")
    audio_data = capture.record(duration=3)
    
    if audio_data is None or len(audio_data) == 0:
        print("Error: No audio captured!")
        return
    
    print(f"Captured {len(audio_data)} samples.")
    
    print("\n2. Testing Noise Reduction...")
    clean_audio = reducer.reduce_noise(audio_data)
    
    print("\n3. Testing Normalization...")
    norm_audio = reducer.normalize_audio(clean_audio)
    rms_before = np.sqrt(np.mean(clean_audio**2))
    rms_after = np.sqrt(np.mean(norm_audio**2))
    print(f"RMS Level before: {rms_before:.4f}, after: {rms_after:.4f}")
    
    print("\n4. Testing Silence Trimming (VAD)...")
    trimmed_audio = vad.trim_silence(norm_audio)
    print(f"Samples before trimming: {len(norm_audio)}, after: {len(trimmed_audio)}")
    
    print("\n5. Testing Transcription...")
    text = processor.transcribe(audio_data)
    print(f"Final Transcribed Text: '{text}'")
    
    if text:
        print("\n[SUCCESS] Pipeline is working and transcribing text.")
    else:
        print("\n[WARNING] Pipeline works but no text was recognized. Try speaking louder or check mic settings.")

if __name__ == "__main__":
    verify_pipeline()
