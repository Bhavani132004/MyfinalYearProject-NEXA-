"""Maps intents to executable actions"""

from src.core.logger import logger

class ActionMapper:
    """Maps intents to actions"""
    
    INTENT_ACTION_MAP = {
        # Legacy mappings
        'open_application': 'open_app',
        'close_application': 'close_app',
        'file_operation': 'file_operation',
        'file_search': 'file_search',
        'web_search': 'search',
        'email': 'email',
        'system_control': 'system_control',
        'music_control': 'music',
        'help': 'help',
        'capabilities': 'capabilities',
        'who_am_i': 'user_info',
        
        # New ML mappings (shortened names from dataset)
        'open_app': 'open_app',
        'close_app': 'close_app',
        'greetings': 'hello', # or map to capabilities/help
        'time_date': 'time',
        'weather': 'weather',
        
        # Automation & Dictation
        'dictation': 'dictation',
        'save_file': 'save_file',
        'search_internal': 'search_internal',
        
        'unknown': 'unknown'
    }
    
    def map_intent(self, intent):
        """Map intent to action"""
        action = self.INTENT_ACTION_MAP.get(intent, 'unknown')
        logger.info(f"Intent '{intent}' mapped to action '{action}'")
        return action
    
    def get_all_mappings(self):
        """Get all intent-action mappings"""
        return self.INTENT_ACTION_MAP