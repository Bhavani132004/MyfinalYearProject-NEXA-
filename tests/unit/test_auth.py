"""Authentication tests"""

import unittest
from src.auth.password_utils import hash_password, verify_password

class TestAuthentication(unittest.TestCase):
    """Test authentication"""
    
    def test_password_hashing(self):
        """Test password hashing"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        self.assertNotEqual(password, hashed)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrong", hashed))

if __name__ == '__main__':
    unittest.main()