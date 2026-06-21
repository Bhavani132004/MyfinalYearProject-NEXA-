"""Error handling utilities"""
from src.core.logger import logger as default_logger

class ApplicationError(Exception):
    """Base application error"""
    pass

class AuthenticationError(ApplicationError):
    """Authentication related errors"""
    pass

class SpeechProcessingError(ApplicationError):
    """Speech processing errors"""
    pass

class NLPProcessingError(ApplicationError):
    """NLP processing errors"""
    pass

class CommandExecutionError(ApplicationError):
    """Command execution errors"""
    pass

class DatabaseError(ApplicationError):
    """Database related errors"""
    pass

def handle_error(error, logger=None):
    """Centralized error handling"""
    error_msg = str(error)
    error_type = type(error).__name__
    
    if logger:
        logger.error(f"{error_type}: {error_msg}")
    
    return {
        "success": False,
        "error_type": error_type,
        "message": error_msg
    }