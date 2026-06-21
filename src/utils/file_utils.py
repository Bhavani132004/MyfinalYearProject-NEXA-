"""File utilities"""

import os
import json
from src.core.logger import logger

class FileUtils:
    """File utility functions"""
    
    @staticmethod
    def read_json(file_path):
        """Read JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON: {e}")
            return {}
    
    @staticmethod
    def write_json(file_path, data):
        """Write JSON file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing JSON: {e}")
    
    @staticmethod
    def file_exists(file_path):
        """Check if file exists"""
        return os.path.exists(file_path)
    
    @staticmethod
    def get_file_size(file_path):
        """Get file size in bytes"""
        return os.path.getsize(file_path)