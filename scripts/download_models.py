"""Download models script"""

from src.core.logger import logger

def download_models():
    """Download required models"""
    try:
        print("Downloading models (first run may take time)...")
        
        from src.core.model_loader import ModelLoader
        
        loader = ModelLoader()
        
        print("Loading Whisper model...")
        loader.load_whisper_model(model_size="base")
        
        print("Loading intent classifier...")
        loader.load_intent_classifier()
        
        print("Loading NER model...")
        loader.load_ner_model()
        
        print("✓ All models downloaded successfully")
        return True
    
    except Exception as e:
        logger.error(f"Model download error: {e}")
        print(f"✗ Model download failed: {e}")
        return False

if __name__ == "__main__":
    download_models()