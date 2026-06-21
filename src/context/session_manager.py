"""Session management"""

import uuid
from datetime import datetime, timedelta
from src.core.logger import logger

class SessionManager:
    """Manages user sessions"""
    
    def __init__(self, timeout_minutes=60):
        self.sessions = {}
        self.timeout = timedelta(minutes=timeout_minutes)
    
    def create_session(self, user_id):
        """Create new session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        logger.info(f"Session created for user: {user_id}")
        return session_id
    
    def validate_session(self, session_id):
        """Validate if session is active"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        if datetime.now() - session["last_activity"] > self.timeout:
            del self.sessions[session_id]
            return False
        
        session["last_activity"] = datetime.now()
        return True
    
    def get_user_id(self, session_id):
        """Get user ID from session"""
        if self.validate_session(session_id):
            return self.sessions[session_id]["user_id"]
        return None
    
    def close_session(self, session_id):
        """Close session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Session closed: {session_id}")
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        expired = []
        for session_id, session in self.sessions.items():
            if datetime.now() - session["last_activity"] > self.timeout:
                expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")

# Global session manager
session_manager = SessionManager()