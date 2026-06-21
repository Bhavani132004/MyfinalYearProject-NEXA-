"""Audio processing utilities"""

import numpy as np
from src.core.logger import logger

class AudioUtils:
    """Audio utilities"""
    
    @staticmethod
    def get_audio_duration(audio_data, sample_rate=16000):
        """Get audio duration in seconds"""
        return len(audio_data) / sample_rate
    
    @staticmethod
    def get_audio_level(audio_data):
        """Get audio level (RMS)"""
        return np.sqrt(np.mean(audio_data**2))
    
    @staticmethod
    def normalize_audio(audio_data):
        """Normalize audio to -1 to 1 range"""
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            return audio_data / max_val
        return audio_data