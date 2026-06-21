"""User personalization and preferences"""

import json
import os
from src.core.logger import logger

class PersonalizationManager:
    """Manages user personalization"""
    
    def __init__(self):
        self.profiles = {}
        self.profiles_dir = "data/user_profiles"
    
    def load_user_profile(self, user_id):
        """Load user profile"""
        try:
            profile_path = os.path.join(self.profiles_dir, f"user_{user_id}", "preferences.json")
            
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as f:
                    self.profiles[user_id] = json.load(f)
            else:
                self.profiles[user_id] = self._create_default_profile()
            
            logger.info(f"Profile loaded for user: {user_id}")
        except Exception as e:
            logger.error(f"Error loading profile: {e}")
            self.profiles[user_id] = self._create_default_profile()
    
    def _create_default_profile(self):
        """Create default user profile"""
        return {
            "theme": "dark",
            "language": "en",
            "recording_duration": 5,
            "confidence_threshold": 0.7,
            "auto_execute": True,
            "voice_feedback": True,
            "aliases": {
                "my browser": "chrome",
                "writing tool": "notepad",
                "math": "calculator"
            }
        }
    
    def get_user_preferences(self, user_id):
        """Get user preferences"""
        return self.profiles.get(user_id, self._create_default_profile())
    
    def update_preferences(self, user_id, preferences):
        """Update user preferences"""
        try:
            if user_id in self.profiles:
                self.profiles[user_id].update(preferences)
            else:
                profile = self._create_default_profile()
                profile.update(preferences)
                self.profiles[user_id] = profile
            
            # Save to file
            self._save_profile(user_id)
            logger.info(f"Preferences updated for user: {user_id}")
        except Exception as e:
            logger.error(f"Error updating preferences: {e}")
    
    def _save_profile(self, user_id):
        """Save profile to file"""
        try:
            profile_dir = os.path.join(self.profiles_dir, f"user_{user_id}")
            os.makedirs(profile_dir, exist_ok=True)
            
            profile_path = os.path.join(profile_dir, "preferences.json")
            with open(profile_path, 'w') as f:
                json.dump(self.profiles[user_id], f, indent=2)
        except Exception as e:
            logger.error(f"Error saving profile: {e}")