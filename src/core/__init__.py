"""Core module - Application core functionality"""

from src.core.logger import setup_logger, logger
from src.core.config_manager import config, ConfigManager
from src.core.constants import *
from src.core.error_handler import (
    ApplicationError,
    AuthenticationError,
    SpeechProcessingError,
    NLPProcessingError,
    CommandExecutionError,
    DatabaseError,
    handle_error
)

__all__ = [
    'setup_logger',
    'logger',
    'config',
    'ConfigManager',
    'ApplicationError',
    'AuthenticationError',
    'SpeechProcessingError',
    'NLPProcessingError',
    'CommandExecutionError',
    'DatabaseError',
    'handle_error'
]