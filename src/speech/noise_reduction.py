"""Audio noise reduction"""

import numpy as np
from scipy import signal
from src.core.logger import logger

class NoiseReducer:
    """Reduces background noise from audio"""
    
    def __init__(self):
        self.noise_profile = None
    
    def reduce_noise(self, audio_data, noise_factor=0.5):
        """Reduce noise using spectral subtraction"""
        try:
            # Ensure audio is numpy array
            if not isinstance(audio_data, np.ndarray):
                audio_data = np.array(audio_data)
            
            # Apply high-pass filter
            filtered = self._apply_highpass_filter(audio_data)
            
            # Apply noise gate
            gated = self._apply_noise_gate(filtered)
            
            return gated
            
        except Exception as e:
            logger.error(f"Noise reduction error: {e}")
            return audio_data
    
    def _apply_highpass_filter(self, audio_data):
        """Apply high-pass filter"""
        sos = signal.butter(2, 80, 'hp', fs=16000, output='sos')
        filtered = signal.sosfilt(sos, audio_data)
        return filtered
    
    def _apply_noise_gate(self, audio_data):
        """Apply noise gate"""
        # Threshold based on RMS
        threshold = np.std(audio_data) * 0.5
        gated = np.where(np.abs(audio_data) < threshold, 0, audio_data)
        return gated
    
    def normalize_audio(self, audio_data):
        """Normalize audio level"""
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            return audio_data / max_val
        return audio_data