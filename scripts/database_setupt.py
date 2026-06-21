"""Database setup script"""

from src.database.db_handler import DatabaseHandler
from src.core.logger import logger

def setup_database():
    """Initialize database"""
    try:
        print("Setting up database...")
        db = DatabaseHandler()
        print("✓ Database initialized")
        return True
    except Exception as e:
        logger.error(f"Database setup error: {e}")
        print(f"✗ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    setup_database()