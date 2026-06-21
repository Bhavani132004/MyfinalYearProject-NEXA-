import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ml.intent_classifier import IntentClassifier
from src.core.logger import logger

def main():
    logger.info("Starting model training pipeline...")
    
    # 1. Train Intent Classifier
    classifier = IntentClassifier()
    dataset_path = "data/dataset.json"
    
    if os.path.exists(dataset_path):
        logger.info(f"Training Intent Classifier with {dataset_path}...")
        success = classifier.train(dataset_path)
        if success:
            logger.info("Intent Classifier trained and saved successfully.")
        else:
            logger.error("Intent Classifier training failed.")
    else:
        logger.error(f"Dataset not found at {dataset_path}. Run generate_dataset.py first.")

if __name__ == "__main__":
    main()
