"""Voice-based authentication"""

import numpy as np
from src.core.logger import logger

class VoiceAuthenticator:
    """Voice-based user authentication"""
    
    def __init__(self):
        self.voice_profiles = {}
        self.threshold = 0.7
    
    def register_voice(self, user_id, audio_samples):
        """Register voice profile for user"""
        try:
            logger.info(f"Registering voice for user: {user_id}")
            
            # Extract voice features
            features = [self._extract_features(audio) for audio in audio_samples]
            
            # Create voice profile
            profile = {
                "user_id": user_id,
                "samples": len(audio_samples),
                "features": np.mean(features, axis=0)
            }
            
            self.voice_profiles[user_id] = profile
            logger.info(f"Voice registered for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Voice registration error: {e}")
            return False
    
    def authenticate_voice(self, user_id, audio_sample):
        """Authenticate user by voice"""
        try:
            if user_id not in self.voice_profiles:
                return False
            
            # Extract features
            features = self._extract_features(audio_sample)
            profile = self.voice_profiles[user_id]
            
            # Compare with stored profile
            similarity = self._calculate_similarity(features, profile["features"])
            
            return similarity >= self.threshold
            
        except Exception as e:
            logger.error(f"Voice authentication error: {e}")
            return False
    
    def _extract_features(self, audio_data):
        """Extract voice features from audio"""
        # Placeholder for actual feature extraction
        # In production, use MFCCs or other acoustic features
        return np.mean(audio_data) if isinstance(audio_data, np.ndarray) else np.array([0.5])
    
    def _calculate_similarity(self, features1, features2):
        """Calculate similarity between voice features"""
        # Euclidean distance normalized
        distance = np.linalg.norm(features1 - features2)
        similarity = 1 / (1 + distance)
        return similarity