"""Manages application context"""

from .history_handler import HistoryHandler
from .personalisation import PersonalizationManager
from src.core.logger import logger

class ContextManager:
    """Manages user and application context"""
    
    def __init__(self):
        self.user_id = None
        self.history_handler = HistoryHandler()
        self.personalization = PersonalizationManager()
        self.current_context = {}
    
    def set_user(self, user_id):
        """Set current user"""
        self.user_id = user_id
        self.personalization.load_user_profile(user_id)
        # Store user info in context for context_analyzer
        self.update_context('user_id', user_id)
        logger.info(f"Context set for user: {user_id}")
    
    def set_user_info(self, username, email=None):
        """Set detailed user info"""
        self.update_context('username', username)
        if email: self.update_context('email', email)

    def enrich_intent(self, intent):
        """Enrich intent with context information"""
        try:
            # Add user preferences and context
            enriched = intent.copy()
            enriched['user_id'] = self.user_id
            enriched['username'] = self.get_context('username')
            enriched['context'] = self.current_context.copy()
            
            # Add user preferences
            enriched['user_preferences'] = self.get_preferences()
            
            logger.info(f"Intent enriched for {enriched.get('username', 'user ' + str(self.user_id))}")
            return enriched
        except Exception as e:
            logger.error(f"Error enriching intent: {e}")
            return intent

    def update_context(self, key, value):
        """Update context information"""
        try:
            self.current_context[key] = value
            logger.debug(f"Context updated: {key} = {value}")
        except Exception as e:
            logger.error(f"Error updating context: {e}")
    
    def get_context(self, key=None):
        """Get context information"""
        if key:
            return self.current_context.get(key)
        return self.current_context.copy()
    
    def clear_context(self):
        """Clear current context"""
        self.current_context = {}
        logger.info("Context cleared")
    
    def add_to_history(self, command, result):
        """Add command to history"""
        try:
            self.history_handler.add_entry(
                user_id=self.user_id,
                command=command,
                result=result
            )
        except Exception as e:
            logger.error(f"Error adding to history: {e}")
    
    def get_history(self, limit=10):
        """Get command history"""
        try:
            return self.history_handler.get_recent(user_id=self.user_id, limit=limit)
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return []
    
    def get_preferences(self, user_id=None):
        """Get user preferences"""
        try:
            target_user = user_id or self.user_id
            if target_user:
                return self.personalization.get_user_preferences(target_user)
            return {}
        except Exception as e:
            logger.error(f"Error getting preferences: {e}")
            return {}
    
    def update_preferences(self, user_id, preferences):
        """Update user preferences"""
        try:
            self.personalization.update_preferences(user_id, preferences)
            logger.info(f"Preferences updated for user {user_id}")
        except Exception as e:
            logger.error(f"Error updating preferences: {e}")