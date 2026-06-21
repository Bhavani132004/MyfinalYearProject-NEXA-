"""Database query helpers"""

from sqlalchemy import func
from src.database.models import Command, User, Session
from src.core.logger import logger

class Queries:
    """Database queries"""
    
    @staticmethod
    def get_user_command_history(session, user_id, limit=10):
        """Get user command history"""
        return session.query(Command).filter(
            Command.user_id == user_id
        ).order_by(Command.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_command_statistics(session, user_id):
        """Get command statistics"""
        return session.query(
            Command.intent,
            func.count(Command.id).label('count')
        ).filter(
            Command.user_id == user_id
        ).group_by(Command.intent).all()
    
    @staticmethod
    def get_most_used_commands(session, user_id, limit=5):
        """Get most used commands"""
        return session.query(
            Command.command_text,
            func.count(Command.id).label('count')
        ).filter(
            Command.user_id == user_id
        ).group_by(Command.command_text).order_by(
            func.count(Command.id).desc()
        ).limit(limit).all()
    
    @staticmethod
    def add_command_record(session, user_id, command_text, intent, confidence, status):
        """Add command record"""
        try:
            cmd = Command(
                user_id=user_id,
                command_text=command_text,
                intent=intent,
                confidence=confidence,
                execution_status=status
            )
            session.add(cmd)
            session.commit()
            logger.info(f"Command recorded for user {user_id}")
            return cmd
        except Exception as e:
            session.rollback()
            logger.error(f"Error recording command: {e}")
            raise