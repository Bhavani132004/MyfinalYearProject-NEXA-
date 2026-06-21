import json
import random
import os

def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

DATA_DIR = "data"
DATASET_FILE = os.path.join(DATA_DIR, "dataset.json")

def generate_dataset():
    check_dir(DATA_DIR)
    
    intents = {
        "open_app": [
            "open chrome", "launch chrome", "start chrome", "run chrome", "open up chrome",
            "open firefox", "launch firefox", "start firefox", "run firefox",
            "open notepad", "launch notepad", "start notepad", "run notepad",
            "open calculator", "launch calculator", "start calculator", "run calculator",
            "open vscode", "launch vscode", "start vscode", "run vscode",
            "open visual studio code", "launch python IDE", "start spotify", "play spotify",
            "open excel", "launch word", "start powerpoint", "run outlook",
            "open slack", "start teams", "launch zoom", "open camera",
            "open settings", "launch control panel", "start cmd", "open terminal",
            "open explorer", "launch file manager", "start paint", "open discord",
            "open steam", "launch game", "start browser", "open edge",
            "launch safari", "start adobe reader", "open photoshop", "launch premiere",
            "open illustrator", "start blender", "run unity", "open android studio"
        ],
        "close_app": [
            "close chrome", "exit chrome", "quit chrome", "kill chrome", "stop chrome",
            "close firefox", "exit firefox", "quit firefox",
            "close notepad", "exit notepad", "quit notepad",
            "close calculator", "exit calculator", "quit calculator",
            "close vscode", "exit vscode", "quit vscode",
            "close spotify", "exit word", "quit excel", "stop powerpoint",
            "close outlook", "exit teams", "quit zoom", "close camera",
            "close settings", "exit control panel", "quit cmd", "close terminal",
            "close explorer", "exit paint", "quit discord", "close steam",
            "close browser", "exit edge", "quit safari", "close reader",
            "close photoshop", "exit premiere", "quit blender", "close all windows"
        ],
        "web_search": [
            "search for python tutorials", "google climate change", "look up recipes",
            "find best laptops 2024", "search youtube for music", "search web for news",
            "browse for funny cats", "search online for tickets", "who won the game",
            "what is the capital of france", "search google for restaurants",
            "search bing for images", "look up weather in london", "find pizza near me",
            "search creating a website", "google how to cook pasta",
            "search youtube for python course", "look up movie reviews",
            "search meaning of life", "check stock market", "search wikipedia for ai",
            "find lyrics to song", "search amazon for books"
        ],
        "system_control": [
            "shutdown computer", "turn off pc", "restart system", "reboot computer",
            "log out", "lock screen", "sleep mode", "hibernate", "turn volume up",
            "increase volume", "decrease volume", "turn volume down", "mute sound",
            "unmute audio", "set brightness to 50", "increase brightness",
            "decrease brightness", "check battery status", "show system info",
            "open task manager", "start tax manager", "open process explorer",
            "check my battery life", "tell me system information", "how is my battery",
            "switch user", "sign out"
        ],
        "file_search": [
          "search for my resume", "find the project report", "locate finance spreadsheet",
          "search for meeting notes", "find python scripts", "where is my presentation",
          "look up budget file", "search for images", "find any pdf files",
          "search for document named backup", "locate the readme file",
          "find my pictures", "search for videos", "where is the desktop folder",
          "look for a file called data"
        ],
        "file_operation": [
            "create new folder", "make a directory", "create text file", "new document",
            "delete this file", "remove folder", "copy file", "move file to documents",
            "rename file to backup", "list files in download", "show my documents",
            "open downloads folder", "create backup", "delete rough draft",
            "copy image to pictures", "move video to videos", "navigate to desktop",
            "go to music folder", "list directory contents", "make new file"
        ],
        "time_date": [
            "what time is it", "tell me the time", "current time", "what follows today",
            "what is the date", "tell me today's date", "current date", "day of the week",
            "what day is it", "is it monday", "set alarm for 7am", "timer for 10 minutes",
            "what time is it in london", "show calendar", "schedule for today"
        ],
        "weather": [
            "what is the weather", "weather today", "is it raining", "temperature outside",
            "weather forecast", "will it snow tomorrow", "weather in new york",
            "current temperature", "how hot is it", "is it sunny"
        ],
        "music_control": [
            "play music", "pause song", "stop music", "next track", "skip song",
            "previous song", "volume up", "volume down", "mute music", "resume playing",
            "play some jazz", "play rock music", "shuffle playlist", "repeat song",
            "play music on youtube", "pause the song", "skip this track", "play some rock",
            "lower the volume", "mute the music", "start playing jazz"
        ],
        "help": [
            "help me", "what can you do", "show commands", "list features", "how to use",
            "assist me", "i need help", "tell me your capabilities", "what are your functions",
            "guide me"
        ],
        "greetings": [
            "hello", "hi there", "good morning", "good evening", "hey nexa", "hi nexa",
            "good afternoon", "how are you", "nice to meet you", "who are you",
            "what is your name", "introduce yourself"
        ]
    }
    
    dataset = []
    
    for intent, examples in intents.items():
        for example in examples:
            # Simple Entity Extraction Logic for Dataset Labeling
            entities = {}
            if intent in ["open_app", "close_app"]:
                parts = example.split()
                # Heuristic: verify if last word or specific words are apps
                # This is a simplification for synthetic data
                for word in parts:
                    if word in ["chrome", "firefox", "notepad", "calculator", "vscode", "spotify", "excel", "word", "powerpoint", "outlook", "slack", "teams", "zoom", "camera", "settings", "explorer", "paint", "discord", "steam", "edge", "safari", "photoshop", "premiere", "blender", "unity"]:
                        entities["app_name"] = [word]
                        break
            
            elif intent == "web_search":
                if "for " in example:
                    query = example.split("for ", 1)[1]
                    entities["search_query"] = [query]
                elif "google " in example:
                    query = example.split("google ", 1)[1]
                    entities["search_query"] = [query]
            
            elif intent == "file_search":
                # Extract filename from "search for X", "find X", "locate X"
                for prefix in ["search for ", "find ", "locate ", "where is ", "look up "]:
                    if prefix in example:
                        query = example.split(prefix, 1)[1]
                        # Remove filler words
                        for filler in ["my ", "the ", "a ", "any "]:
                            query = query.replace(filler, "")
                        entities["search_query"] = [query.strip()]
                        break
            
            dataset.append({
                "text": example,
                "intent": intent,
                "entities": entities
            })
            
    # Add variations/noise
    # TODO: Implement augmentation if needed
    
    with open(DATASET_FILE, 'w') as f:
        json.dump(dataset, f, indent=2)
        
    print(f"Dataset generated with {len(dataset)} examples at {DATASET_FILE}")

if __name__ == "__main__":
    generate_dataset()
