"""Long-term memory storage for user preferences"""

import json
import os
from src.core.logger import logger

class MemoryStorage:
    """Stores and retrieves long-term memory"""
    
    def __init__(self):
        self.memory_dir = "data/user_profiles"
        self.memory = {}
    
    def load_memory(self, user_id):
        """Load user memory"""
        try:
            memory_file = os.path.join(
                self.memory_dir,
                f"user_{user_id}",
                "memory.json"
            )
            
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    self.memory[user_id] = json.load(f)
            else:
                self.memory[user_id] = self._create_default_memory()
            
            logger.info(f"Memory loaded for user: {user_id}")
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            self.memory[user_id] = self._create_default_memory()
    
    def _create_default_memory(self):
        """Create default memory structure"""
        return {
            "frequent_commands": {},
            "favorite_apps": [],
            "last_accessed": {},
            "learned_shortcuts": {},
            "user_preferences": {}
        }
    
    def save_memory(self, user_id):
        """Save user memory"""
        try:
            memory_dir = os.path.join(self.memory_dir, f"user_{user_id}")
            os.makedirs(memory_dir, exist_ok=True)
            
            memory_file = os.path.join(memory_dir, "memory.json")
            with open(memory_file, 'w') as f:
                json.dump(self.memory.get(user_id, {}), f, indent=2)
            
            logger.info(f"Memory saved for user: {user_id}")
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def add_frequent_command(self, user_id, command, count=1):
        """Add to frequent commands"""
        if user_id not in self.memory:
            self.load_memory(user_id)
        
        freq = self.memory[user_id]["frequent_commands"]
        if command in freq:
            freq[command] += count
        else:
            freq[command] = count
    
    def add_favorite_app(self, user_id, app_name):
        """Add favorite application"""
        if user_id not in self.memory:
            self.load_memory(user_id)
        
        favorites = self.memory[user_id]["favorite_apps"]
        if app_name not in favorites:
            favorites.append(app_name)
    
    def get_frequent_commands(self, user_id, limit=5):
        """Get frequent commands"""
        if user_id not in self.memory:
            self.load_memory(user_id)
        
        freq = self.memory[user_id]["frequent_commands"]
        sorted_cmds = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [cmd for cmd, _ in sorted_cmds[:limit]]
    
    def get_favorite_apps(self, user_id):
        """Get favorite apps"""
        if user_id not in self.memory:
            self.load_memory(user_id)
        
        return self.memory[user_id]["favorite_apps"]