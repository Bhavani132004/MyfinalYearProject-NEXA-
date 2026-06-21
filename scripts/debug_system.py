
import os
import subprocess
import psutil

def list_target_processes():
    print("--- Checking Running Processes ---")
    targets = ['calc', 'calculator', 'calendar', 'outlook', 'winword', 'excel']
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'].lower()
            if any(t in name for t in targets):
                print(f"Found: {proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def test_file_search_logic():
    print("\n--- Testing File Search Logic ---")
    # Simulate the logic from CommandExecutor._execute_file_search
    import re
    text = "search for requirements.txt in src"
    target = re.sub(r'^(?:is there a|find|finding|search for|searching for|search|searching|where is|locate|locating|look for|show me|look up|lookup)\s+', '', text)
    target = re.sub(r'^(?:local|my|the|a|an|some)\s+', '', target)
    parts = re.split(r'\s+(?:in|from|at|within|on|to)\b', target)
    filename = parts[0].strip()
    print(f"Original: '{text}' -> Extracted Filename: '{filename}'")
    
    # Try actual search
    root_dir = os.path.abspath(".")
    print(f"Searching in: {root_dir}")
    matches = []
    for root, dirs, files in os.walk(root_dir):
        if filename.lower() in [f.lower() for f in files]:
            matches.append(os.path.join(root, filename))
            
    print(f"Matches: {matches}")

if __name__ == "__main__":
    try:
        list_target_processes()
        test_file_search_logic()
    except Exception as e:
        print(f"Error: {e}")
