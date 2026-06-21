"""Intent detection using ML model with rule-based fallback"""

import re
import os
from src.core.logger import logger
from .intent_classifier import IntentClassifier

class IntentDetector:
    """Detects user intent using ML model and pattern matching fallback"""
    
    def __init__(self):
        # Initialize ML Classifier
        self.classifier = IntentClassifier()
        self.use_ml = self.classifier.load_model()
        
        if not self.use_ml:
            logger.warning("ML Model not found/loaded. Falling back to rule-based detection.")
        
        # Define fallback patterns (Legacy/High-Precision)
        self.intent_patterns = {
            "open_app": [
                r'\b(open|launch|start|run)\b',
            ],
            "close_app": [
                r'\b(close|exit|quit|kill|stop|terminate)\b',
            ],
            "file_operation": [
                r'\b(create|make|new)\b.*(folder|directory|file|document|backup|draft|note)',
                r'\b(delete|remove|trash)\b.*(file|folder|document|draft|backup|item)',
                r'\b(copy|move|rename)\b.*(file|image|video|to|backup|item)',
                r'\b(list|show|contents)\b.*(files|directory|folder|documents|download|contents)',
                r'\b(open|navigate|go to)\b.*(folder|desktop|download|documents|music|videos|pictures)',
                r'\b(make a directory|create text file|new document|create backup|make new file|delete this file)\b',
            ],
            "file_search": [
                r'\b(search for|find|locate|where is|look up|look for)\b.*\b(resume|report|spreadsheet|notes|scripts|presentation|file|images|pdf|document|readme|pictures|videos|folder|data)\b',
                r'\b(any pdf files|my pictures|videos|desktop folder)\b',
            ],
            "weather": [
                r'\b(weather|temperature|temparature|raining|snow|sunny|forecast|how hot)\b',
            ],
            "time_date": [
                r'\b(time|date|clock|today|now|monday|alarm|timer|calendar|schedule)\b',
                r'\b(what follows today|day of the week|what day is it|is it monday)\b',
                r'\b(time in london|show calendar|schedule for today)\b',
            ],
            "music_control": [
                r'\b(play|pause|stop|resume|next|skip|previous|shuffle|repeat)\b.*\b(music|song|track|playing|jazz|rock|playlist)\b',
                r'\b(volume up|volume down|mute music)\b',
                r'\b(play music|pause song|stop music|next track|skip song|previous song|resume playing|play some jazz|play rock music|shuffle playlist|repeat song)\b',
            ],
            "help": [
                r'\b(help|assist|commands|capabilities|functions|guide|what can you do|show commands|list features|how to use)\b',
            ],
            "greetings": [
                r'\b(hello|hi|hey|morning|evening|afternoon|how are you|nice to meet you|who are you|name|introduce yourself)\b',
                r'\b(hey nexa|hi nexa)\b',
            ],
            "web_search": [
                r'\b(search for|google|google for|look up|search on google|on youtube|search youtube for|browse for|search online for|who won|what is the capital|search google for|search bing for|find pizza near me|search creating a website|search meaning of life|check stock market|search wikipedia for|find lyrics to|search amazon for|search web for)\b',
                r'\b(tutorials|climate|recipes|laptops|news|cats|tickets|game|capital|france|restaurants|images|pizza|website|pasta|reviews|life|stock|market|wikipedia|lyrics|amazon)\b',
            ],
            "system_control": [
                r'\b(shutdown|restart|volume|brightness|mute|battery|system info|system information|task manager|tax manager)\b',
            ],
            "dictation": [
                r'\b(type|write|dictate|insert|say)\b.*\b(text|sentence|word|paragraph|this)\b',
                r'\b(type the following)\b',
                r'^type\s+',
            ],
            "save_file": [
                r'\b(save|store)\b.*\b(file|document|note|this|changes)\b',
                r'\b(save it|save this)\b',
            ],
            "search_internal": [
                r'\b(search for|find|look up)\b.*\b(on|in|inside)\b.*\b(youtube|spotify|browser|app|notepad)\b',
            ],
        }
        
        logger.info("Intent detector initialized")
    
    def detect(self, text, confidence_threshold=0.6):
        """Detect intent from text"""
        try:
            text_lower = text.lower()
            intent = "unknown"
            confidence = 0.0
            all_scores = {}
            
            # 1. Try ML Prediction first
            if self.use_ml:
                prediction = self.classifier.predict(text)
                intent = prediction["intent"]
                confidence = prediction["confidence"]
                
                # HEURISTIC OVERRIDE:
                # If ML predicts 'web_search' or 'open_app' but text contains clear file keywords,
                # force 'file_search'. BUT do not override if it looks like a file_operation.
                file_keywords = [
                    'file', 'folder', 'document', 'pdf', 'txt', 'docx', 'xlsx', 'disk', 
                    'directory', 'ppt', 'pptx', 'spreadsheet', 'presentation', 'resume', 
                    'notes', 'report', 'readme', 'data', 'script'
                ]
                operation_keywords = ['create', 'make', 'new', 'delete', 'remove', 'copy', 'move', 'rename', 'list', 'show', 'navigate', 'go to', 'open folder']
                
                # Check for extensions
                has_extension = re.search(r'\.[a-z]{2,4}\b', text_lower)
                is_operation = any(k in text_lower for k in operation_keywords)
                
                # Check if it's NOT a specific app open command like "Open OneDrive"
                if not is_operation and (intent in ['web_search', 'open_app'] or confidence < confidence_threshold) and \
                   (any(k in text_lower for k in file_keywords) or has_extension):
                    
                    if 'onedrive' in text_lower and 'search' not in text_lower and 'find' not in text_lower:
                        pass # Don't override app open for OneDrive
                    else:
                        logger.info(f"Overriding ML intent '{intent}' -> 'file_search' based on file keywords/extension.")
                        return {
                            "text": text,
                            "intent": "file_search",
                            "confidence": 1.0,
                            "source": "heuristic_override"
                        }

                # If confidence is high enough, return it
                if confidence >= confidence_threshold:
                    logger.info(f"ML Intent Detection: {intent} ({confidence:.2f})")
                    return {
                        "text": text,
                        "intent": intent,
                        "confidence": confidence,
                        "source": "ml"
                    }
            
            # 2. Fallback to Rule-based if ML failed or low confidence
            logger.info(f"ML confidence low ({confidence:.2f}). Checking rules...")
            
            for pat_intent, patterns in self.intent_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, text_lower):
                        # Simple rule match gives a fixed moderate confidence
                        return {
                            "text": text,
                            "intent": pat_intent,
                            "confidence": 0.7,
                            "source": "rule_based"
                        }
            
            return {
                "text": text,
                "intent": "unknown",
                "confidence": 0.0,
                "source": "none"
            }
            
        except Exception as e:
            logger.error(f"Intent detection error: {e}")
            return {
                "text": text,
                "intent": "unknown",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def batch_detect(self, texts):
        """Detect intent for multiple texts"""
        return [self.detect(text) for text in texts]
