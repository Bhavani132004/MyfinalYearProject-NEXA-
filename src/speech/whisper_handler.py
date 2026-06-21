"""Speech recognition handler using Google Speech Recognition"""

import speech_recognition as sr
import numpy as np
from src.core.logger import logger

class WhisperHandler:
    """Handles Speech Recognition (Google API replacement for Whisper)"""
    
    def __init__(self, model_size="base"):
        # model_size kept for API compatibility but not used
        self.recognizer = sr.Recognizer()
        
        try:
            logger.info(f"Initializing Google Speech Recognition...")
            # Adjust recognizer settings for better accuracy
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            logger.info("Speech Recognition initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Speech Recognition: {e}")
            raise
    
    def transcribe(self, audio_data):
        """Transcribe audio using Google Speech Recognition"""
        try:
            # Convert numpy array to AudioData if needed
            if isinstance(audio_data, np.ndarray):
                # Convert to 16-bit PCM
                audio_data = (audio_data * 32767).astype(np.int16)
                audio = sr.AudioData(audio_data.tobytes(), 16000, 2)
            else:
                audio = audio_data
            
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            return text.strip()
        except sr.UnknownValueError:
            logger.warning("Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Could not request results from Speech Recognition service; {e}")
            raise
        except Exception as e:
            logger.error(f"Speech transcription error: {e}")
            raise
    
    def transcribe_with_timestamps(self, audio_data):
        """Transcribe with timestamp information (simplified - no timestamps in Google API)"""
        try:
            text = self.transcribe(audio_data)
            return {
                'text': text,
                'chunks': [{'text': text, 'timestamp': (0.0, None)}]
            }
        except Exception as e:
            logger.error(f"Speech transcription with timestamps error: {e}")
            raise