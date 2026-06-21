"""NLP utility functions"""

import re
from src.core.logger import logger

class NLPUtils:
    """NLP helper functions"""
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters except for punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        return text
    
    @staticmethod
    def tokenize(text):
        """Tokenize text into words"""
        return text.split()
    
    @staticmethod
    def remove_stopwords(tokens):
        """Remove common stopwords"""
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been'
        }
        return [t for t in tokens if t.lower() not in stopwords]
    
    @staticmethod
    def calculate_similarity(text1, text2):
        """Calculate text similarity"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1, text2).ratio()