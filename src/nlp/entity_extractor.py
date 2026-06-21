"""Named Entity Recognition using rule-based methods"""

import re
from src.core.logger import logger

class EntityExtractor:
    """Extracts entities from text using rule-based methods"""
    
    def __init__(self):
        try:
            logger.info("Initializing rule-based entity extractor...")
            
            # Define common patterns
            self.patterns = {
                'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                'URL': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                'NUMBER': r'\b\d+\b',
                'TIME': r'\b([01]?[0-9]|2[0-3]):[0-5][0-9]\b',
                'DATE': r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
            }
            
            # Common application names
            self.applications = [
                'notepad', 'calculator', 'calc', 'chrome', 'firefox', 'edge',
                'word', 'ms word', 'microsoft word', 'excel', 'ms excel', 'microsoft excel',
                'powerpoint', 'ppt', 'outlook', 'teams',
                'paint', 'mspaint', 'cmd', 'terminal', 'explorer', 'task manager',
                'control panel', 'settings', 'browser', 'file explorer',
                'google chrome', 'microsoft edge', 'internet explorer',
                'visual studio', 'code', 'vscode', 'photoshop', 'spotify',
                'vlc', 'media player', 'discord', 'slack', 'zoom',
                'vs code', 'command prompt', 'powershell', 'wordpad',
                'write', 'camera', 'photos', 'calendar', 'mail',
                'movies & tv', 'weather', 'news', 'store', 'microsoft store',
                'obs', 'steam', 'adobe', 'acrobat', 'reader', 'pdf',
                'skype', 'anydesk', 'teamviewer', 'postman', 'docker', 'virtualbox', 'sublime text'
            ]
            
            logger.info("Entity extractor initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing entity extractor: {e}")
            raise
    
    def extract_entities(self, text):
        """Extract named entities from text"""
        try:
            entities = []
            grouped = {}
            
            # Extract pattern-based entities
            for entity_type, pattern in self.patterns.items():
                matches = re.finditer(pattern, text)
                for match in matches:
                    entity = {
                        'entity_group': entity_type,
                        'word': match.group(),
                        'start': match.start(),
                        'end': match.end(),
                        'score': 1.0
                    }
                    entities.append(entity)
                    
                    if entity_type not in grouped:
                        grouped[entity_type] = []
                    grouped[entity_type].append(match.group())
            
            # Extract application names
            text_lower = text.lower()
            for app in self.applications:
                pattern = rf'\b{re.escape(app)}\b'
                match = re.search(pattern, text_lower)
                if match:
                    entity = {
                        'entity_group': 'APP',
                        'word': app,
                        'start': match.start(),
                        'end': match.end(),
                        'score': 1.0
                    }
                    entities.append(entity)
                    
                    if 'APP' not in grouped:
                        grouped['APP'] = []
                    # Avoid duplicates
                    if app not in grouped['APP']:
                        grouped['APP'].append(app)
            
            # Extract filenames/search queries
            filenames = self.extract_filenames(text)
            for filename in filenames:
                # Find start/end positions
                start = text_lower.find(filename)
                if start != -1:
                    entity = {
                        'entity_group': 'FILE',
                        'word': filename,
                        'start': start,
                        'end': start + len(filename),
                        'score': 1.0
                    }
                    entities.append(entity)
                    if 'FILE' not in grouped:
                        grouped['FILE'] = []
                    if filename not in grouped['FILE']:
                        grouped['FILE'].append(filename)
            
            return {
                "text": text,
                "entities": entities,
                "grouped": grouped
            }
            
        except Exception as e:
            logger.error(f"Entity extraction error: {e}")
            return {
                "text": text,
                "entities": [],
                "grouped": {}
            }
    
    def extract_filenames(self, text):
        """Extract potential filenames or search queries from text"""
        import re
        text_lower = text.lower()
        
        # 1. Look for patterns like "something.ext"
        pattern = r'\b[\w\-]+\.[a-z]{2,4}\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            return matches
            
        # 2. Extract after search keywords if no extension found
        search_keywords = ["search for ", "find ", "locate ", "where is ", "look up "]
        for kw in search_keywords:
            if kw in text_lower:
                query = text_lower.split(kw, 1)[1].strip()
                # Remove common trailing fillers
                query = re.sub(r'\b(in|on|at|within|from|my|the|a|any)\b.*$', '', query).strip()
                # Remove possessive/determiners at start
                query = re.sub(r'^(my|the|a|an|some)\b', '', query).strip()
                if query:
                    return [query]
        
        # 3. Fallback: just return the longest word that isn't a common keyword? 
        # For now, stick to the keywords match.
        return []
    
    def extract_applications(self, text):
        """Extract application names"""
        common_apps = ['chrome', 'firefox', 'notepad', 'calculator', 'word', 'excel']
        found_apps = [app for app in common_apps if app.lower() in text.lower()]
        return found_apps