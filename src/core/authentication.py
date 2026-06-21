"""User authentication logic"""

from src.utils.password_utils import hash_password, verify_password
from .db_handler import DatabaseHandler
from src.core.logger import logger
from src.core.error_handler import AuthenticationError

class Authenticator:
    """Handles user authentication"""
    
    def __init__(self):
        self.db = DatabaseHandler()
        self.failed_attempts = {}
    
    def register_user(self, username, password, email):
        """Register new user"""
        try:
            # Check if user exists
            user = self.db.get_user_by_username(username)
            if user:
                raise AuthenticationError("Username already exists")
            
            # Hash password
            password_hash = hash_password(password)
            
            # Create user
            user = self.db.create_user(
                username=username,
                password_hash=password_hash,
                email=email
            )
            
            logger.info(f"User registered: {username}")
            return {"success": True, "user_id": user.id}
            
        except Exception as e:
            logger.error(f"Registration error: {e}")
            raise
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        try:
            # Reset attempts on successful verification
            if username in self.failed_attempts:
                del self.failed_attempts[username]
            
            user = self.db.get_user_by_username(username)
            
            if not user:
                raise AuthenticationError("Invalid username or password")
            
            if not verify_password(password, user.password_hash):
                self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
                if self.failed_attempts[username] >= 5:
                    raise AuthenticationError("Too many failed attempts")
                raise AuthenticationError("Invalid username or password")
            
            logger.info(f"User authenticated: {username}")
            return {"success": True, "user_id": user.id, "username": username}
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        try:
            user = self.db.get_user_by_id(user_id)
            
            if not verify_password(old_password, user.password_hash):
                raise AuthenticationError("Incorrect old password")
            
            new_hash = hash_password(new_password)
            self.db.update_user_password(user_id, new_hash)
            
            logger.info(f"Password changed for user: {user_id}")
            return {"success": True}
            
        except Exception as e:
            logger.error(f"Password change error: {e}")
            raise

def authenticate_user(username, password):
    """Convenience function for authentication"""
    auth = Authenticator()
    return auth.authenticate(username, password)