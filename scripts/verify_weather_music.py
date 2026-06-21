
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath("."))

from src.nlp_processing.intent_detector import IntentDetector
from src.desktop_control.command_executor import CommandExecutor

def test():
    detector = IntentDetector()
    detector.use_ml = False # Force rule-based for verification
    executor = CommandExecutor()
    
    test_phrases = [
        "what is the weather today",
        "is weather raining",
        "is weather raining today",
        "what is the temparature outside",
        "current temparature",
        "how hot is weather",
        "play some jazz",
        "play rock music",
        "pause song",
        "next track",
        "shuffle playlist"
    ]
    
    with open("verification_results.log", "w") as f:
        f.write(f"{'Phrase':<35} | {'Detected Intent':<15} | {'Source':<15}\n")
        f.write("-" * 75 + "\n")
        
        for phrase in test_phrases:
            result = detector.detect(phrase)
            f.write(f"{phrase:<35} | {result['intent']:<15} | {result['source']:<15}\n")
            
            # Test command execution mapping (mocking real execution)
            intent = result['intent']
            action = executor.action_mapper.map_intent(intent)
            f.write(f"  -> Maps to Action: {action}\n")

if __name__ == "__main__":
    test()
