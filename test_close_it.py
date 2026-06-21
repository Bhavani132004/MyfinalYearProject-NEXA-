from src.nlp.context_analyzer import ContextAnalyzer
from src.actions.command_executor import CommandExecutor

def test_close_it():
    print("Testing 'close it' logic")
    
    # Setup context
    analyzer = ContextAnalyzer()
    analyzer.update_application_context("notepad")
    print(f"Current Context: {analyzer.current_application}")
    
    # Simulate processing
    text = "close it"
    
    # 1. Resolve pronouns
    resolved = analyzer._resolve_pronouns(text)
    print(f"Original: '{text}' -> Resolved: '{resolved}'")
    
    # 2. Extract App Name
    cmd = {"text": text, "resolved_text": resolved}
    executor = CommandExecutor()
    app_name = executor._extract_app_name(cmd)
    
    print(f"Extracted App Name: {app_name}")
    
    if app_name == "notepad":
        print("SUCCESS! Pronoun correctly resolved and extracted.")
    else:
        print("FAILED!")

if __name__ == "__main__":
    test_close_it()
