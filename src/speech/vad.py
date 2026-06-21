"""Voice Activity Detection"""

import numpy as np
from scipy import signal
from src.core.logger import logger

class VoiceActivityDetector:
    """Detects voice activity in audio"""
    
    def __init__(self, threshold=0.02):
        self.threshold = threshold
        self.frame_length = 512
    
    def detect_voice_activity(self, audio_data, sample_rate=16000):
        """Detect voice activity in audio"""
        try:
            # Calculate energy frames
            frames = self._frame_audio(audio_data)
            energies = [np.sqrt(np.sum(f**2) / len(f)) for f in frames]
            
            # Detect voice activity
            voice_activity = [e > self.threshold for e in energies]
            
            return voice_activity, energies
            
        except Exception as e:
            logger.error(f"VAD error: {e}")
            return None, None
    
    def _frame_audio(self, audio_data):
        """Frame audio data"""
        frames = []
        for i in range(0, len(audio_data) - self.frame_length, self.frame_length):
            frames.append(audio_data[i:i + self.frame_length])
        return frames
    
    def trim_silence(self, audio_data, sample_rate=16000):
        """Trim silence from audio"""
        voice_activity, _ = self.detect_voice_activity(audio_data, sample_rate)
        
        if voice_activity is None:
            return audio_data
        
        # Find first and last voice activity
        voice_frames = [i for i, v in enumerate(voice_activity) if v]
        
        if not voice_frames:
            return audio_data
        
        start_frame = voice_frames[0]
        end_frame = voice_frames[-1] + 1
        
        start_sample = start_frame * self.frame_length
        end_sample = min(end_frame * self.frame_length, len(audio_data))
        
        return audio_data[start_sample:end_sample]