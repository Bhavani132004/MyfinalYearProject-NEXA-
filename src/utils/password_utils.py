"""Password hashing and verification"""

import hashlib
import secrets
from src.core.logger import logger

class PasswordUtils:
    """Password utilities"""
    
    @staticmethod
    def hash_password(password, salt=None):
        """Hash password using PBKDF2"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        
        return f"{salt}${pwd_hash.hex()}"
    
    @staticmethod
    def verify_password(password, password_hash):
        """Verify password against hash"""
        try:
            salt, hash_hex = password_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return new_hash.hex() == hash_hex
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

def hash_password(password):
    """Convenience function"""
    return PasswordUtils.hash_password(password)

def verify_password(password, password_hash):
    """Convenience function"""
    return PasswordUtils.verify_password(password, password_hash)