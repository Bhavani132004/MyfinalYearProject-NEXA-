"""Model loader for lightweight alternatives"""

import spacy
from src.core.logger import logger

class ModelLoader:
    """Loads and manages ML models (Spacy)"""
    
    def __init__(self):
        self.models = {}
        logger.info("Initializing ModelLoader (Lightweight)")
    
    def load_spacy_model(self, model_name="en_core_web_md"):
        """Load Spacy NLP model"""
        try:
            if 'spacy' not in self.models:
                logger.info(f"Loading Spacy model {model_name}...")
                try:
                    nlp = spacy.load(model_name)
                except OSError:
                    logger.warning(f"Model {model_name} not found. Attempting to download...")
                    from spacy.cli import download
                    download(model_name)
                    nlp = spacy.load(model_name)
                
                self.models['spacy'] = nlp
                logger.info("Spacy model loaded successfully")
            return self.models['spacy']
        except Exception as e:
            logger.error(f"Error loading Spacy model: {e}")
            raise

    # Legacy wrappers for compatibility (if needed by main.py, though we should update callsites)
    def load_nlp_engine(self):
        return self.load_spacy_model()