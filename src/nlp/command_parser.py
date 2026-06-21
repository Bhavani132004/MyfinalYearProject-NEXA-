"""Parse text commands to structured format"""

from .intent_detector import IntentDetector
from .entity_extractor import EntityExtractor
from src.core.logger import logger

class CommandParser:
    """Parses text to structured commands"""
    
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.entity_extractor = EntityExtractor()
    
    def parse(self, text):
        """Parse text to structured command"""
        try:
            logger.info(f"Parsing command: {text}")
            
            # Detect intent
            intent_result = self.intent_detector.detect(text)
            
            # Extract entities
            entity_result = self.entity_extractor.extract_entities(text)
            
            # Build command structure
            command = {
                "text": text,
                "intent": intent_result['intent'],
                "confidence": intent_result['confidence'],
                "entities": entity_result['entities'],
                "grouped_entities": entity_result['grouped'],
                "parameters": self._extract_parameters(text, intent_result['intent'])
            }
            
            logger.info(f"Command parsed: {command['intent']}")
            return command
            
        except Exception as e:
            logger.error(f"Command parsing error: {e}")
            return {
                "text": text,
                "intent": "unknown",
                "confidence": 0.0,
                "entities": [],
                "parameters": {}
            }
    
    def _extract_parameters(self, text, intent):
        """Extract parameters specific to intent"""
        params = {}
        
        text_lower = text.lower()
        
        # Extract file operations
        if "open" in text_lower:
            params['action'] = 'open'
        elif "close" in text_lower:
            params['action'] = 'close'
        elif "save" in text_lower:
            params['action'] = 'save'
        
        # Extract file types
        if "document" in text_lower:
            params['type'] = 'document'
        elif "image" in text_lower:
            params['type'] = 'image'
        
        return params