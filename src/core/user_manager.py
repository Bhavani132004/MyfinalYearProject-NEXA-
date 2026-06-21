"""User management operations"""

from src.database.db_handler import DatabaseHandler
from src.core.logger import logger

class UserManager:
    """Manages user profiles and data"""
    
    def __init__(self):
        self.db = DatabaseHandler()
    
    def get_user_profile(self, user_id):
        """Get user profile"""
        try:
            user = self.db.get_user_by_id(user_id)
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at
            }
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            raise
    
    def update_user_profile(self, user_id, **kwargs):
        """Update user profile"""
        try:
            self.db.update_user(user_id, **kwargs)
            logger.info(f"User profile updated: {user_id}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            raise
    
    def get_all_users(self):
        """Get all users (admin only)"""
        try:
            return self.db.get_all_users()
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            raise
    
    def delete_user(self, user_id):
        """Delete user account"""
        try:
            self.db.delete_user(user_id)
            logger.info(f"User deleted: {user_id}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            raise