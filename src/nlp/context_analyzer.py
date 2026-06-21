"""Contextual analysis of commands"""

from src.core.logger import logger

class ContextAnalyzer:
    """Analyzes context for command interpretation"""
    
    def __init__(self):
        self.conversation_history = []
        self.current_application = None
        self.recent_apps = []
        self.recent_files = []
        self.app_usage_frequency = {} # Track app usage for suggestions
    
    def analyze(self, command, history=None):
        """Analyze command with context"""
        try:
            enriched = command.copy()
            
            # Add application context
            enriched['current_application'] = self.current_application
            enriched['recent_apps'] = self.recent_apps
            
            # Add history context
            enriched['history'] = history or self.conversation_history[-5:]
            
            # Resolve pronouns based on context
            enriched['resolved_text'] = self._resolve_pronouns(command['text'])
            
            return enriched
            
        except Exception as e:
            logger.error(f"Context analysis error: {e}")
            return command
    
    def _resolve_pronouns(self, text):
        """Resolve pronouns in text based on context"""
        import re
        
        # Mapping simple pronouns
        # If no context, don't replace with generic 'application' as it causes "close application" failure
        singular_app = self.current_application
        plural_apps = " and ".join(self.recent_apps[:2]) if self.recent_apps else None
        
        # Only perform replacements if we actually have context
        pronouns = {}
        if singular_app:
            pronouns.update({
                r'\bi\b\s+it\b': singular_app,
                r'\bit\b': singular_app,
                r'\bthat\b': singular_app,
                r'\bthis\b': singular_app,
                r'\bthe\b\s+application\b': singular_app,
                r'\bthe\b\s+app\b': singular_app,
            })
        
        if plural_apps:
            pronouns.update({
                r'\bthem\b': plural_apps,
                r'\bboth\b': plural_apps if len(self.recent_apps) >= 2 else (singular_app or ""),
                r'\ball\b': plural_apps
            })
        
        resolved = text
        for pattern, replacement in pronouns.items():
            if replacement:
                regex = re.compile(pattern, re.IGNORECASE)
                resolved = regex.sub(replacement, resolved)
        
        return resolved
    
    def update_application_context(self, app_name):
        """Update current application context"""
        self.current_application = app_name
        if app_name not in self.recent_apps:
            self.recent_apps.insert(0, app_name)
        else:
            # Move to front
            self.recent_apps.remove(app_name)
            self.recent_apps.insert(0, app_name)
            
        # Keep only last 5
        self.recent_apps = self.recent_apps[:5]
        
        # Track frequency for behavior suggestions
        self.app_usage_frequency[app_name] = self.app_usage_frequency.get(app_name, 0) + 1
        
        logger.info(f"Application context updated: {app_name}. Recent: {self.recent_apps}")
    
    def add_to_history(self, command):
        """Add command to history"""
        self.conversation_history.append(command)

    def get_behavioral_suggestion(self):
        """Generate a suggestion based on time/behavior"""
        from datetime import datetime
        hour = datetime.now().hour
        
        # Time-based suggestions
        if 6 <= hour < 11:
            return "Ready for your morning report?"
        elif 17 <= hour < 20:
            return "Want to check your evening schedule?"
        
        # Frequency-based suggestions
        if self.app_usage_frequency:
            # Get top app excluding currently open if exists
            eligible = {k: v for k, v in self.app_usage_frequency.items() if k != self.current_application}
            if eligible:
                top_app = max(eligible, key=eligible.get)
                if eligible[top_app] >= 2:
                    return f"I see you use {top_app} a lot. Should I open it?"
        
        return None
