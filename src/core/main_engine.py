"""Main application engine orchestrating all modules"""

import threading
from src.speech.speech_to_text import SpeechToTextProcessor
from src.speech.text_to_speech import TextToSpeech
from src.nlp.intent_detector import IntentDetector
from src.nlp.entity_extractor import EntityExtractor
from src.nlp.context_analyzer import ContextAnalyzer
from src.actions.command_executor import CommandExecutor
from src.context.context_manager import ContextManager
from src.core.logger import logger
from src.core.error_handler import handle_error

class VoiceControlEngine:
    """Main orchestration engine"""
    
    def __init__(self):
        self.speech_processor = SpeechToTextProcessor()
        self.tts = TextToSpeech()
        self.intent_detector = IntentDetector()
        self.entity_extractor = EntityExtractor()
        self.context_analyzer = ContextAnalyzer()
        self.command_executor = CommandExecutor()
        self.context_manager = ContextManager()
        self.multitasking = self.command_executor.multitasking # Shared manager
        self.user_id = None
        
        logger.info("Voice Control Engine initialized")
    
    def set_user(self, user_id):
        """Set current user"""
        self.user_id = user_id
        self.context_manager.set_user(user_id)
        
        # Welcome message
        if user_id:
            try:
                username = self.context_manager.get_context('username') or "User"
                self.speak(f"Hello {username}, I am NEXA. Ready to assist you.")
            except:
                pass
                
        logger.info(f"User set to: {user_id}")
    
    def speak(self, text):
        """Speak text (threaded to avoid blocking)"""
        if not text: return
        
        # Check preference
        prefs = self.get_user_preferences()
        if not prefs.get('voice_feedback', True):
            return
            
        try:
            threading.Thread(target=self.tts.speak, args=(text,), daemon=True).start()
        except Exception as e:
            logger.error(f"Error starting TTS thread: {e}")

    def process_voice_command(self, audio_data):
        """Process complete voice command pipeline"""
        try:
            # 1. Speech to Text
            logger.info("Processing voice command...")
            text = self.speech_processor.transcribe(audio_data)
            logger.info(f"Transcribed text: {text}")
            
            if not text:
                return {"success": False, "message": "No speech detected"}

            res = self._process_text_flow(text)
            if res.get('success'):
                logger.info(f"Command executed successfully: {res.get('message')}")
            else:
                logger.warning(f"Command execution failed: {res.get('message')}")
            return res
            
        except Exception as e:
            return handle_error(e, logger)

    def process_text_command(self, text):
        """Process command from text input"""
        return self._process_text_flow(text)

    def _process_text_flow(self, full_text):
        """Internal flow for processing text with smarter multitasking and inheritance"""
        try:
            import re
            # Expanded joining words and characters
            split_pattern = r'\b(?:then|and then|afterwards|along with|also|then also|followed by|could you also|and also|could you separately)\b|,|;'
            
            # Detect intents on the full text first
            original_intent = self.intent_detector.detect(full_text)
            
            # Split candidates. We also handle 'and' but carefully
            raw_parts = re.split(fr'{split_pattern}|\band\b', full_text, flags=re.IGNORECASE)
            parts = [p.strip() for p in raw_parts if p.strip()]
            
            # Logic to decide if we should really split or keep as one command
            should_split = True
            
            # If it looks like a simple search with "and" inside the query (e.g. "search for cats and dogs")
            # We check if the parts look like distinct commands.
            if len(parts) > 1 and original_intent['intent'] in ['web_search', 'file_search']:
                # If both parts lack a verb, it's likely a compound query
                # Heuristic: if 'open', 'close', 'play', 'run' not in the second part, keep it together
                verbs = ['open', 'close', 'launch', 'run', 'start', 'play', 'search', 'find']
                has_verb_in_parts = all(any(v in p.lower() for v in verbs) for p in parts)
                
                if not has_verb_in_parts:
                    should_split = False
            
            if len(parts) <= 1:
                should_split = False
                
            if not should_split:
                return self._execute_single_command(full_text)

            # combine results
            p_results = []
            
            # Execute in parallel using MultitaskingManager
            # Note: We convert command dicts to a list for the manager
            commands_to_run = []
            for part_text in parts:
                # Basic prep for each part
                resolved = self.context_analyzer._resolve_pronouns(part_text)
                intent_res = self.intent_detector.detect(resolved)
                ent_res = self.entity_extractor.extract_entities(resolved)
                
                command = intent_res.copy()
                command['text'] = resolved
                command['grouped_entities'] = ent_res.get('grouped', {})
                commands_to_run.append(self.context_manager.enrich_intent(command))

            # Trigger parallel execution
            parallel_results_map = self.multitasking.execute_parallel(commands_to_run, self._execute_internal_only)
            
            for i in range(len(commands_to_run)):
                p_results.append(parallel_results_map.get(i, {"success": False, "message": "Failed to execute"}))
            
            success = all(r.get('success', False) for r in p_results)
            combined_msg = " | ".join([r.get('message', '') for r in p_results])
            
            # Speak result if success
            if success:
                self.speak(f"Completed {len(p_results)} tasks.")
                
            return {
                "success": success,
                "message": f"Successfully completed {len(p_results)} tasks: {combined_msg}",
                "results": p_results,
                "text": full_text,
                "intent": "multitasking"
            }
            
        except Exception as e:
            return handle_error(e, logger)

    def _execute_internal_only(self, enriched_command):
        """Internal execution without history or speech (for multitasking)"""
        res = self.command_executor.execute(enriched_command)
        res['intent'] = enriched_command.get('intent', 'unknown')
        return res

    def _execute_single_command(self, text):
        """Helper to run a single command string through the pipeline"""
        # Resolve context (pronouns like 'it')
        resolved_text = self.context_analyzer._resolve_pronouns(text)
        
        # 2. Intent Detection
        intent_result = self.intent_detector.detect(resolved_text)
        
        # 3. Entity Extraction
        entity_result = self.entity_extractor.extract_entities(resolved_text)
        
        # 4. Update Context
        apps = entity_result.get('grouped', {}).get('APP', [])
        if apps:
            self.context_analyzer.update_application_context(apps[0])
        
        # 5. Build command
        command = intent_result.copy()
        command['text'] = resolved_text
        command['entities'] = entity_result.get('entities', [])
        command['grouped_entities'] = entity_result.get('grouped', {})
        
        # 6. Add enrichment
        enriched = self.context_manager.enrich_intent(command)
        
        # 7. Execute
        res = self.command_executor.execute(enriched)
        
        # 8. POST-EXECUTION CONTEXT SYNC (Critical for "Close it")
        # If the executor successfully opened an app, ensure it's in our context
        exec_app = res.get('app_name')
        if res.get('success') and exec_app:
            self.context_analyzer.update_application_context(exec_app)
        
        res['text'] = resolved_text
        res['intent'] = command.get('intent', 'unknown')
        
        # Speak result
        if res.get('success') and res.get('message'):
            self.speak(res['message'])
        elif not res.get('success'):
            self.speak("Sorry, I couldn't do that.")
        
        # Store in history
        self.context_manager.add_to_history(resolved_text, res)
        return res

    def get_command_history(self, limit=10):
        """Get user command history"""
        return self.context_manager.get_history(limit)
    
    def get_user_preferences(self):
        """Get user preferences"""
        return self.context_manager.get_preferences(self.user_id)
    
    def update_user_preferences(self, preferences):
        """Update user preferences"""
        self.context_manager.update_preferences(self.user_id, preferences)
        logger.info(f"Preferences updated for user: {self.user_id}")

    def get_suggestion(self):
        """Get behavioral suggestion from context analyzer"""
        return self.context_analyzer.get_behavioral_suggestion()
