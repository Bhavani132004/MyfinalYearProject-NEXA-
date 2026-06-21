"""Database connection and operations"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.models import Base, User, Command, Session
from src.core.logger import logger
from src.core.config_manager import config

class DatabaseHandler:
    """Manages database operations"""
    
    def __init__(self):
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._init_db()
    
    def _create_engine(self):
        """Create database engine"""
        import os
        
        # Get database path (without sqlite:// prefix)
        db_path = config.get('database.path', 'data/database/voice_control.db')
        
        # Ensure database directory exists
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"Created database directory: {db_dir}")
        
        # Create engine with correct URL format
        db_url = f'sqlite:///{db_path}'
        engine = create_engine(db_url)
        logger.info(f"Database engine created: {db_url}")
        return engine
    
    def _init_db(self):
        """Initialize database tables"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def create_user(self, username, password_hash, email):
        """Create new user"""
        session = self.get_session()
        try:
            user = User(username=username, password_hash=password_hash, email=email)
            session.add(user)
            session.commit()
            session.refresh(user)  # Refresh to load all attributes
            # Store user data before closing session
            user_id = user.id
            logger.info(f"User created: {username}")
            session.expunge(user)  # Detach from session
            return user
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating user: {e}")
            raise
        finally:
            session.close()
    
    def get_user_by_username(self, username):
        """Get user by username"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.username == username).first()
            if user:
                session.refresh(user)  # Ensure all attributes are loaded
                session.expunge(user)  # Detach from session
            return user
        finally:
            session.close()
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.refresh(user)  # Ensure all attributes are loaded
                session.expunge(user)  # Detach from session
            return user
        finally:
            session.close()
    
    def update_user(self, user_id, **kwargs):
        """Update user"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.commit()
            logger.info(f"User updated: {user_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating user: {e}")
            raise
        finally:
            session.close()
    
    def update_user_password(self, user_id, password_hash):
        """Update user password"""
        self.update_user(user_id, password_hash=password_hash)
    
    def delete_user(self, user_id):
        """Delete user"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            session.delete(user)
            session.commit()
            logger.info(f"User deleted: {user_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting user: {e}")
            raise
        finally:
            session.close()
    
    def get_all_users(self):
        """Get all users"""
        session = self.get_session()
        try:
            users = session.query(User).all()
            # Detach all users from session
            for user in users:
                session.refresh(user)
                session.expunge(user)
            return users
        finally:
            session.close()