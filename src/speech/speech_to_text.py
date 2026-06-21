"""Main Speech-to-Text interface with multiple backends"""

import numpy as np
import speech_recognition as sr
import pyaudio
import os
from .whisper_handler import WhisperHandler
from src.input.audio_capture import AudioCapture
from .noise_reduction import NoiseReducer
from .vad import VoiceActivityDetector
from src.core.logger import logger

class SpeechToTextProcessor:
    """Main STT processor with Google API and Whisper fallback"""
    
    def __init__(self, model_type="google"):
        self.model_type = model_type
        self.audio_capture = AudioCapture()
        self.noise_reducer = NoiseReducer()
        self.vad = VoiceActivityDetector()
        self.recognizer = sr.Recognizer()
        
        # Optimization: Faster detection
        self.recognizer.pause_threshold = 0.5
        self.recognizer.energy_threshold = 300 # Dynamic adjustment
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize Whisper as fallback or primary if requested
        self.whisper = WhisperHandler()
        self.stop_listening = None
        
        logger.info(f"Speech processor initialized with {model_type} (Optimized for speed)")
    
    def capture_and_transcribe(self, duration=5):
        """Deprecated: Use ContinuousVoiceThread instead"""
        pass



    def transcribe(self, audio_data, sample_rate=16000):
        """Transcribe audio to text (supports both numpy and sr.AudioData)"""
        try:
            text = ""
            success = False
            
            # 1. Handle sr.AudioData (from background listener)
            if isinstance(audio_data, sr.AudioData):
                if self.model_type == "google" or self.model_type == "mixed":
                    try:
                        text = self.recognizer.recognize_google(audio_data)
                        success = True
                    except sr.UnknownValueError:
                        return "" # Silence
                    except Exception as e:
                        logger.warning(f"Google STT failed: {e}")
                
                if not success:
                    # Convert to numpy for Whisper
                    audio_bytes = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
                    audio_data = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32767.0
            
            # 2. Handle numpy array (from record/manual)
            if not success:
                # Pre-processing: Noise Reduction -> Normalization -> Trimming
                processed_audio = self.noise_reducer.reduce_noise(audio_data)
                processed_audio = self.noise_reducer.normalize_audio(processed_audio)
                processed_audio = self.vad.trim_silence(processed_audio)
                
                if len(processed_audio) < 1600: # Less than 0.1s is likely noise
                    return ""

                if self.model_type == "google" or self.model_type == "mixed":
                    try:
                        audio_int16 = (processed_audio * 32767).astype(np.int16)
                        audio_bytes = audio_int16.tobytes()
                        audio_source = sr.AudioData(audio_bytes, sample_rate, 2)
                        
                        text = self.recognizer.recognize_google(audio_source)
                        success = True
                    except sr.UnknownValueError:
                        success = True # Just means no speech detected
                        text = ""
                    except Exception as e:
                        logger.warning(f"Google STT fallback failed: {e}")
                
                if not success:
                    logger.info("Using Whisper for transcription...")
                    text = self.whisper.transcribe(processed_audio)
            
            final_text = text.strip().lower() if text else ""
            if final_text:
                logger.info(f"Transcribed Result: '{final_text}'")
            return final_text
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""
    
    def transcribe_file(self, file_path):
        """Transcribe audio file"""
        try:
            # Setup recognizer for file
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
                
            try:
                logger.info(f"Transcribing file {file_path} with Google...")
                return self.recognizer.recognize_google(audio)
            except:
                logger.info("Google failed, trying Whisper...")
                audio_data = self.audio_capture.load_audio_file(file_path)
                return self.whisper.transcribe(audio_data)
                
        except Exception as e:
            logger.error(f"File transcription error: {e}")
            raise
