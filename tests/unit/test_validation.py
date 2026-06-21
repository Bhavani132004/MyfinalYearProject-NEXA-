"""Validation tests"""

import unittest
from src.utils.validation import InputValidator

class TestValidation(unittest.TestCase):
    """Test validation"""
    
    def test_email_validation(self):
        """Test email validation"""
        validator = InputValidator()
        self.assertTrue(validator.validate_email("test@example.com"))
        self.assertFalse(validator.validate_email("invalid@"))
    
    def test_username_validation(self):
        """Test username validation"""
        validator = InputValidator()
        self.assertTrue(validator.validate_username("testuser123"))
        self.assertFalse(validator.validate_username("ab"))
    
    def test_password_validation(self):
        """Test password validation"""
        validator = InputValidator()
        self.assertTrue(validator.validate_password("password123"))
        self.assertFalse(validator.validate_password("12345"))

if __name__ == '__main__':
    unittest.main()