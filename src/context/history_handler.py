"""Command history management"""

from datetime import datetime
from src.core.logger import logger

class HistoryHandler:
    """Manages command history"""
    
    def __init__(self):
        self.history = []
    
    def add_command(self, user_id, text, intent, result):
        """Add command to history (Legacy)"""
        self.add_entry(user_id, text, result)

    def add_entry(self, user_id, command, result):
        """Add command to history"""
        try:
            command_record = {
                "user_id": user_id,
                "command": command,
                "result": result,
                "timestamp": datetime.now(),
                "success": result.get("success", False) if isinstance(result, dict) else False
            }
            self.history.append(command_record)
            logger.info(f"Command added to history")
        except Exception as e:
            logger.error(f"Error adding to history: {e}")
    
    def get_recent(self, user_id, limit=10):
        """Get recent commands for user"""
        user_commands = [h for h in self.history if h['user_id'] == user_id]
        sorted_cmds = sorted(user_commands, key=lambda x: x['timestamp'], reverse=True)
        return [c['command'] for c in sorted_cmds[:limit]]

    def get_commands(self, user_id, limit=10):
        """Get user commands (Legacy)"""
        user_commands = [h for h in self.history if h['user_id'] == user_id]
        return sorted(user_commands, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_recent_commands(self, limit=5):
        """Get recent commands"""
        return sorted(self.history, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def clear_history(self, user_id):
        """Clear user history"""
        self.history = [h for h in self.history if h['user_id'] != user_id]
        logger.info(f"History cleared for user: {user_id}")