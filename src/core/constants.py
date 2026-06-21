"""Application constants and enumerations"""

from enum import Enum

class CommandStatus(Enum):
    """Command execution status"""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

class UserRole(Enum):
    """User roles"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class IntentType(Enum):
    """Intent classification types"""
    OPEN_APP = "open_app"
    CLOSE_APP = "close_app"
    FILE_OPERATION = "file_operation"
    SEARCH = "search"
    EMAIL = "email"
    SYSTEM_CONTROL = "system_control"
    UNKNOWN = "unknown"

# Application constants
APP_NAME = "AI Voice Desktop Control System"
APP_VERSION = "1.0.0"
MIN_AUDIO_DURATION = 0.5  # seconds
MAX_AUDIO_DURATION = 60  # seconds
DEFAULT_LANGUAGE = "en"
SESSION_TIMEOUT = 3600  # 1 hour

# Model configuration
WHISPER_MODEL_SIZE = "base"
BERT_MODEL_NAME = "bert-base-uncased"
CONFIDENCE_THRESHOLD = 0.7

# Security
MAX_LOGIN_ATTEMPTS = 5
PASSWORD_MIN_LENGTH = 6
VOICE_SAMPLES_REQUIRED = 3

# Database
DB_ECHO = False
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20