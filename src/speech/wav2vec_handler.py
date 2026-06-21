"""Speech recognition handler using Google Speech Recognition"""

import speech_recognition as sr
import numpy as np
from src.core.logger import logger

class Wav2Vec2Handler:
    """Handles Speech Recognition (Google API replacement for Wav2Vec2)"""
    
    def __init__(self, model_name="facebook/wav2vec2-base-960h"):
        # model_name kept for API compatibility but not used
        self.recognizer = sr.Recognizer()
        
        try:
            logger.info("Initializing Google Speech Recognition...")
            # Adjust recognizer settings
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            logger.info("Speech Recognition initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Speech Recognition: {e}")
            raise
    
    def transcribe(self, audio_data, sample_rate=16000):
        """Transcribe audio using Google Speech Recognition"""
        try:
            # Convert numpy array to AudioData if needed
            if isinstance(audio_data, np.ndarray):
                # Convert to 16-bit PCM
                audio_data = (audio_data * 32767).astype(np.int16)
                audio = sr.AudioData(audio_data.tobytes(), sample_rate, 2)
            else:
                audio = audio_data
            
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.UnknownValueError:
            logger.warning("Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Could not request results from Speech Recognition service; {e}")
            raise
        except Exception as e:
            logger.error(f"Speech transcription error: {e}")
            raise