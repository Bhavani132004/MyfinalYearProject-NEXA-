import os
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from src.core.logger import logger

class IntentClassifier:
    def __init__(self, model_path="data/models/intent_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.intents = []
        
    def train(self, dataset_path):
        """Train the intent classification model"""
        try:
            logger.info(f"Loading dataset from {dataset_path}...")
            with open(dataset_path, 'r') as f:
                data = json.load(f)
            
            texts = [item['text'] for item in data]
            labels = [item['intent'] for item in data]
            
            # Create pipeline
            self.model = Pipeline([
                ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
                ('clf', SVC(kernel='linear', probability=True))
            ])
            
            # Train
            logger.info("Training model...")
            X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Evaluate
            logger.info("Evaluating model...")
            predictions = self.model.predict(X_test)
            report = classification_report(y_test, predictions)
            logger.info(f"Classification Report:\n{report}")
            
            # Save
            self.save_model()
            return True
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return False

    def predict(self, text):
        """Predict intent for a given text"""
        if not self.model:
            if not self.load_model():
                return {"intent": "unknown", "confidence": 0.0}
        
        try:
            # Predict
            probas = self.model.predict_proba([text])[0]
            max_index = np.argmax(probas)
            confidence = probas[max_index]
            intent = self.model.classes_[max_index]
            
            return {
                "intent": intent,
                "confidence": float(confidence)
            }
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"intent": "unknown", "confidence": 0.0}

    def save_model(self):
        """Save the trained model to disk"""
        try:
            directory = os.path.dirname(self.model_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            logger.info(f"Model saved to {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            return False

    def load_model(self):
        """Load the model from disk"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                return True
            else:
                logger.warning(f"Model file not found at {self.model_path}")
                return False
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
