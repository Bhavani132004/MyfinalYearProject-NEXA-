import sys
import os
import traceback

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def log(msg):
    print(msg, flush=True)

def test_module(label, module_path, class_name=None):
    try:
        mod = __import__(module_path, fromlist=[class_name or ''])
        log(f"[OK] {module_path}")
        return True
    except Exception as e:
        log(f"[FAIL] {module_path}")
        log(f"       Error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    log("=" * 60)
    log("Import Verification Script")
    log("=" * 60)

    results = []

    log("\n--- Core ---")
    results.append(test_module("logger", "src.core.logger"))
    results.append(test_module("config_manager", "src.core.config_manager"))
    results.append(test_module("error_handler", "src.core.error_handler"))
    results.append(test_module("models", "src.core.models"))
    results.append(test_module("db_handler", "src.core.db_handler"))
    results.append(test_module("authentication", "src.core.authentication"))

    log("\n--- NLP ---")
    results.append(test_module("intent_classifier", "src.nlp.intent_classifier"))
    results.append(test_module("intent_detector", "src.nlp.intent_detector"))
    results.append(test_module("entity_extractor", "src.nlp.entity_extractor"))
    results.append(test_module("context_analyzer", "src.nlp.context_analyzer"))
    results.append(test_module("command_parser", "src.nlp.command_parser"))

    log("\n--- Speech ---")
    results.append(test_module("whisper_handler", "src.speech.whisper_handler"))
    results.append(test_module("speech_to_text", "src.speech.speech_to_text"))
    results.append(test_module("text_to_speech", "src.speech.text_to_speech"))

    log("\n--- Input ---")
    results.append(test_module("audio_capture", "src.input.audio_capture"))

    log("\n--- Actions ---")
    results.append(test_module("action_mapper", "src.actions.action_mapper"))
    results.append(test_module("app_controller", "src.actions.app_controller"))
    results.append(test_module("file_operations", "src.actions.file_operations"))
    results.append(test_module("web_automation", "src.actions.web_automation"))
    results.append(test_module("system_controller", "src.actions.system_controller"))
    results.append(test_module("automation_handler", "src.actions.automation_handler"))
    results.append(test_module("command_executor", "src.actions.command_executor"))

    log("\n--- Context ---")
    results.append(test_module("session_manager", "src.context.session_manager"))
    results.append(test_module("context_manager", "src.context.context_manager"))

    log("\n--- Engine (Full Chain) ---")
    results.append(test_module("main_engine", "src.core.main_engine"))

    log("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    log(f"RESULT: {passed}/{total} modules imported successfully.")
    log("=" * 60)
    sys.exit(0 if passed == total else 1)
