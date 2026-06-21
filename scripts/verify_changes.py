import sys
import os
import re

# Add src to path
sys.path.append(os.getcwd())

from src.nlp_processing.command_parser import CommandParser
from src.desktop_control.command_executor import CommandExecutor

def test_all_categories():
    parser = CommandParser()
    executor = CommandExecutor()
    
    # Representative samples from each category in the dataset
    test_suite = {
        "open_app": ["open chrome", "start spotify", "launch python IDE", "open visual studio code"],
        "close_app": ["close chrome", "exit word", "close all windows"],
        "web_search": ["google climate change", "search youtube for music", "who won the game"],
        "system_control": ["shutdown computer", "hibernate", "set brightness to 50", "check my battery life", "sign out"],
        "file_search": ["search for my resume", "find any pdf files", "where is the desktop folder"],
        "file_operation": ["create new folder test_dir", "create text file test_file.txt", "list files in data", "delete file test_file.txt", "delete folder test_dir"],
        "time_date": ["what time is it", "what is the date", "what follows today"],
        "weather": ["what is the weather", "temperature outside", "is it raining"],
        "music_control": ["play some jazz", "pause song", "skip song"],
        "help": ["help me", "what can you do", "tell me your capabilities"],
        "greetings": ["hello", "how are you", "what is your name"]
    }
    
    print("=" * 80)
    print(f"{'CATEGORY':<15} | {'COMMAND':<30} | {'INTENT':<15} | {'SUCCESS'}")
    print("=" * 80)
    
    total = 0
    passed = 0
    
    for category, commands in test_suite.items():
        for cmd in commands:
            total += 1
            try:
                parsed = parser.parse(cmd)
                # For file operations that create/delete, we expect success if implemented
                result = executor.execute(parsed)
                success = result.get('success', False)
                
                # Check if intent matches category (some mappings might differ slightly like greetings->hello)
                intent = parsed.get('intent', 'unknown')
                
                print(f"{category:<15} | {cmd:<30} | {intent:<15} | {success}")
                
                if success:
                    passed += 1
                else:
                    print(f"  > Error: {result.get('message', 'No details')}")
                    
            except Exception as e:
                print(f"{category:<15} | {cmd:<30} | ERROR           | False")
                print(f"  > Exception: {e}")
        print("-" * 80)

    print(f"FINAL RESULT: {passed}/{total} commands executed successfully.")
    print("=" * 80)

if __name__ == "__main__":
    test_all_categories()
