
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nlp_processing.intent_detector import IntentDetector

def test_intents():
    output_file = 'intent_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        def log(msg):
            print(msg)
            f.write(msg + "\n")
            
        try:
            log("--- Testing Intent Detection ---")
            detector = IntentDetector()
            
            test_phrases = [
                "search for ai test file",
                "find invoice.pdf",
                "search for files in my disk",
                "open onedrive",
                "search google for python",
                "check for file operations"
            ]
            
            for text in test_phrases:
                result = detector.detect(text) # Note: method name is detect, not detect_intent
                log(f"Text: '{text}'")
                log(f"  -> Predicted Intent: {result['intent']}")
                log(f"  -> Confidence: {result['confidence']}")
                log(f"  -> Source: {result.get('source', 'unknown')}")
                log("-" * 30)
                
        except Exception as e:
            log(f"Error during test: {e}")
            import traceback
            log(traceback.format_exc())

if __name__ == "__main__":
    test_intents()
