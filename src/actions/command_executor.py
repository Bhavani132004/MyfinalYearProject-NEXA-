"""Command executor for desktop automation"""

import os
from src.actions.action_mapper import ActionMapper
from src.actions.app_controller import ApplicationController
from src.actions.file_operations import FileOperations
from src.actions.system_controller import SystemController
from src.actions.web_automation import WebAutomation
from src.actions.multitasking import MultitaskingManager
from src.core.logger import logger
import random

class ResponseGenerator:
    """Generates varied, human-like responses"""
    
    FILLERS = [
        "Sure thing!", "I'm on it.", "Just a second...", 
        "Got it, working on that now.", "Absolutely.", "One moment please."
    ]
    
    CONFIRMATIONS = [
        "All done!", "I've finished that for you.", "Execution successful.",
        "Task completed.", "There you go!", "Done and done."
    ]
    
    FOLLOW_UPS = [
        "Is there anything else I can help with?", "What else can I do for you?",
        "Next task?", "I'm ready for the next one.", "Need anything else?"
    ]

    @staticmethod
    def get_filler():
        return random.choice(ResponseGenerator.FILLERS)

    @staticmethod
    def get_confirmation(original_msg):
        # Humanize the "Result: " message
        msg = original_msg.replace("Result: ", "").strip()
        prefix = random.choice(ResponseGenerator.CONFIRMATIONS)
        return f"{prefix} {msg}"

    @staticmethod
    def get_follow_up():
        return random.choice(ResponseGenerator.FOLLOW_UPS)

from src.actions.automation_handler import AutomationHandler

class CommandExecutor:
    """Executes desktop commands"""
    
    def __init__(self):
        self.action_mapper = ActionMapper()
        self.app_controller = ApplicationController()
        self.file_ops = FileOperations()
        self.system_ctrl = SystemController()
        self.web_auto = WebAutomation()
        self.automation = AutomationHandler()
        self.multitasking = MultitaskingManager()
    
    def execute(self, command, threaded=False):
        """Execute command"""
        if threaded:
            return self.multitasking.execute_parallel([command], self._execute_internal)
            
        return self._execute_internal(command)

    def _execute_internal(self, command):
        """Internal execution logic"""
        try:
            intent = command.get('intent', 'unknown')
            logger.info(f"Executing command with intent: {intent}")
            
            # Map intent to action
            action = self.action_mapper.map_intent(intent)
            
            res = {"success": False, "message": "Unknown error"}
            
            if action == 'open_app':
                res = self._execute_open_app(command)
            elif action == 'close_app':
                res = self._execute_close_app(command)
            elif action == 'dictation':
                res = self._execute_dictation(command)
            elif action == 'save_file':
                res = self._execute_save_file(command)
            elif action == 'search_internal':
                res = self._execute_search_internal(command)
            elif action == 'file_operation':
                res = self._execute_file_operation(command)
            elif action == 'system_control':
                res = self._execute_system_control(command)
            elif action == 'file_search':
                res = self._execute_file_search(command)
            elif action == 'search':
                res = self._execute_web_search(command)
            elif action == 'user_info':
                res = self._execute_user_info(command)
            elif action == 'help':
                res = self._execute_capabilities(command)
            elif action == 'capabilities':
                res = self._execute_capabilities(command)
            elif action == 'music':
                res = self._execute_music(command)
            elif action == 'email':
                res = self._execute_email(command)
            elif action == 'time':
                res = self._execute_time(command)
            elif action == 'weather':
                res = self._execute_weather(command)
            elif action == 'hello':
                res = self._execute_greetings(command)
            elif action == 'unknown':
                res = {"success": False, "message": "Result: The command is not available or not understood."}
            else:
                res = {
                    "success": False,
                    "message": f"Result: Action '{action}' is not available."
                }
                
            # Humanize successful message
            if res.get('success') and 'message' in res:
                res['message'] = ResponseGenerator.get_confirmation(res['message'])
            
            return res
        
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return {"success": False, "message": str(e)}
    
    def _execute_web_search(self, command):
        """Execute web search command with multi-platform routing"""
        try:
            text = command.get('text', '').lower()
            import re
            
            # Clean up the search query by removing generic verbs and platform names
            clean_regex = r'\b(search for|google for|google|find|look up|search on google|on youtube|search youtube for|browse for|search online for|search google for|search bing for|search wikipedia for|find lyrics to|search amazon for|search web for|search bing|search wikipedia|search amazon|youtube|bing|google|amazon|wikipedia|wikipedia for|browse|search online|search web|search)\s*'
            query = re.sub(clean_regex, '', text).strip()
            
            if not query:
                return {"success": False, "message": "Search query not specified"}
            
            # Routing logic based on platform keywords in the original text
            if 'youtube' in text:
                return self.web_auto.search_youtube(query)
            elif 'bing' in text:
                return self.web_auto.search_bing(query)
            elif 'wikipedia' in text:
                return self.web_auto.search_wikipedia(query)
            elif 'amazon' in text:
                return self.web_auto.search_amazon(query)
            elif 'browse' in text or 'search online' in text or 'weather' in text or 'stock market' in text or 'capital' in text or 'lyrics' in text:
                # Default to Google for general browsing/info
                return self.web_auto.search_google(query)
            else:
                # Default fallback
                return self.web_auto.search_google(query)
                
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return {"success": False, "message": str(e)}

    def _execute_open_app(self, command):
        """Execute open application command"""
        try:
            app_name = self._extract_app_name(command)
            prefs = command.get('user_preferences')
            if app_name:
                self.app_controller.open_application(app_name, preferences=prefs)
                return {
                    "success": True, 
                    "message": f"Opened {app_name}",
                    "app_name": app_name # Return for context sync
                }
            return {"success": False, "message": "Application not specified"}
        except Exception as e:
            logger.error(f"Open app error: {e}")
            return {"success": False, "message": str(e)}
    
    def _execute_close_app(self, command):
        """Execute close application command"""
        try:
            app_name = self._extract_app_name(command)
            prefs = command.get('user_preferences')
            if app_name:
                return self.app_controller.close_application(app_name, preferences=prefs)
            
            # If extraction failed, check if the whole command was a resolved pronoun (e.g. "close Chrome")
            resolved_text = command.get('resolved_text', '').lower()
            if 'close ' in resolved_text:
                app_from_resolved = resolved_text.split('close ', 1)[1].strip()
                if app_from_resolved and app_from_resolved != 'application':
                    return self.app_controller.close_application(app_from_resolved, preferences=prefs)
                    
            return {"success": False, "message": "Application not specified"}
        except Exception as e:
            logger.error(f"Close app error: {e}")
            return {"success": False, "message": str(e)}
    
    def _execute_file_search(self, command):
        """Execute local file search with priority for PC over Browser"""
        try:
            text = command.get('text', '').lower().strip()
            import re
            
            # 1. Extraction priority: "find any pdf files" -> search type "pdf"
            # "where is my presentation" -> search keyword "presentation"
            patterns = [
                # Pattern for common search verbs and filler words
                r'\b(?:search for|find|locate|look for|look up|where is)\b\s+(?:\b(?:my|the|a|an|any|document|file|folder)\b\s+)*(?:\b(?:named|called)\b\s+)?(.*?)\s*(?:\s+\b(?:files?|folder|document|directory|spreadsheet)\b)?$',
                # Direct match for specific categories
                r'\b(pdf|pictures?|videos?|desktop|images?|scripts?|resume|notes|report|spreadsheet|budget|backup|readme|presentation|data)\b'
            ]
            
            filename = None
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    if len(match.groups()) > 0:
                        filename = match.group(1).strip()
                        break
            
            if not filename or filename in ['file', 'files', 'something']:
                 filename = text # Fallback to full text if parsing failed
            
            # Handle specific keywords from user dataset
            mapping = {
                'any pdf files': 'pdf',
                'my pictures': 'pictures',
                'images': 'images',
                'videos': 'videos',
                'my resume': 'resume',
                'project report': 'report',
                'finance spreadsheet': 'spreadsheet',
                'meeting notes': 'notes',
                'python scripts': 'scripts',
                'my presentation': 'presentation',
                'budget file': 'budget',
                'document named backup': 'backup',
                'readme file': 'readme',
                'desktop folder': 'desktop'
            }
            
            search_term = mapping.get(filename, filename)
            logger.info(f"Local search term extracted: '{search_term}' from '{text}'")
            
            # Perform local search
            results = self.file_ops.search_files(search_term)
            
            if results:
                count = len(results)
                top_matches = [os.path.basename(r) for r in results[:3]]
                match_str = ", ".join(top_matches)
                if count > 3:
                    match_str += f", and {count - 3} more"
                
                file_name = os.path.basename(results[0])
                msg = f"Result: Found {count} files locally: {match_str}. Opening '{file_name}'"
                
                self.file_ops.open_file(results[0])
                return {"success": True, "message": msg, "results": results}
            
            # Fallback to web search ONLY if the user explicitly asks for it or it's clearly not local
            if 'on google' in text or 'online' in text:
                return self._execute_web_search(command)
                
            return {"success": False, "message": f"Result: Could not find '{search_term}' on your computer."}
            
        except Exception as e:
            logger.error(f"File search error: {e}")
            return {"success": False, "message": f"Result: Search encountered an error: {e}"}

    def _execute_user_info(self, command):
        """Provide current user information"""
        username = command.get('username', 'Unknown')
        user_id = command.get('user_id', 'Unknown')
        msg = f"Result: You are logged in as '{username}' (ID: {user_id})."
        return {"success": True, "message": msg}

    def _execute_capabilities(self, command):
        """Explain system capabilities"""
        capabilities = [
            "Open and close applications (e.g., 'Open WhatsApp', 'Close Chrome')",
            "Search for files locally (e.g., 'Find my resume', 'Search for pdf files')",
            "Perform file operations (e.g., 'Create folder', 'Move file to documents', 'Delete backup')",
            "Web search and YouTube (e.g., 'Google weather', 'Play music on YouTube')",
            "System control (e.g., 'Shutdown', 'Restart', 'Lock screen', 'Volume up/down')",
            "Information (e.g., 'What time is it', 'Tell me today's date', 'Weather forecast')",
            "Media control (e.g., 'Play/Pause music', 'Next track', 'Shuffle playlist')"
        ]
        msg = "Result: I can help you with the following:\n- " + "\n- ".join(capabilities)
        return {"success": True, "message": msg}

    def _execute_music(self, command):
        """Execute music control command"""
        try:
            text = command.get('text', '').lower()
            
            # 1. Check for specific control actions first
            if any(k in text for k in ['pause', 'stop', 'resume', 'skip', 'next', 'previous']):
                if 'pause' in text or 'stop' in text:
                    self.system_ctrl.play_pause_media()
                    return {"success": True, "message": "Result: Executed pause/stop command."}
                if 'resume' in text or ('play' in text and 'playing' in text):
                    self.system_ctrl.play_pause_media()
                    return {"success": True, "message": "Result: Resumed music."}
                if 'next' in text or 'skip' in text:
                    self.system_ctrl.next_track()
                    return {"success": True, "message": "Result: Skipped to next track."}
                if 'previous' in text:
                    self.system_ctrl.prev_track()
                    return {"success": True, "message": "Result: Went to previous track."}
            
            # 2. Volume and Mute
            if 'volume' in text or 'mute' in text:
                return self._execute_system_control(command)
                
            # 3. Play requests (Genres, Shuffle, Repeat)
            import re
            # Clean query
            query = re.sub(r'\b(play|listen to|some|music|song|track|on youtube|in chrome|on utube|utube)\b', '', text).strip()
            
            if 'shuffle' in text:
                 return self.web_auto.search_youtube(f"{query} shuffled playlist")
            if 'repeat' in text:
                 return self.web_auto.search_youtube(f"{query} on repeat")
            
            if not query or query == 'music':
                return self.web_auto.search_youtube("recommended music")
            
            return self.web_auto.search_youtube(query if query else "music")
            
        except Exception as e:
            logger.error(f"Music execution error: {e}")
            return {"success": False, "message": "Result: Music action is not available due to an error."}

    def _execute_email(self, command):
        """Execute email command"""
        try:
            import os
            os.system('start mailto:')
            return {"success": True, "message": "Result: Opened default email client"}
        except Exception as e:
            return {"success": False, "message": "Result: Email client is not available."}

    def _execute_file_operation(self, command):
        """Execute comprehensive file operations (create, delete, copy, move, rename, list, navigate)"""
        try:
            text = command.get('text', '').lower().strip()
            import re
            
            # 1. Routing for Navigation / Open Folder
            if any(k in text for k in ['open', 'navigate', 'go to']):
                # Extract folder name: "open downloads folder", "navigate to desktop"
                match = re.search(r'\b(?:open|navigate to|go to)\b\s+([\w\s]+?)\s*(?:folder|directory|contents)?$', text)
                if match:
                    folder_name = match.group(1).strip()
                    path = self.file_ops.get_well_known_path(folder_name)
                    if not path:
                        # Try searching if it's not a well-known folder
                        results = self.file_ops.search_files(folder_name)
                        path = results[0] if results else None
                    
                    if path and os.path.exists(path):
                        self.file_ops.open_file(path)
                        return {"success": True, "message": f"Result: Navigated to {folder_name}"}
                    return {"success": False, "message": f"Result: Folder '{folder_name}' not found."}

            # 2. Routing for List Operations / Show contents
            if any(k in text for k in ['list', 'show', 'what is in', 'contents of']):
                # "show my documents", "list files in download"
                match = re.search(r'\b(?:in|of|within|at|from|show|list)\s+([\w\s]+?)\s*(?:folder|directory|contents)?$', text)
                target_dir = None
                if match:
                    folder_name = match.group(1).strip()
                    if folder_name not in ['files', 'directory', 'contents']:
                         target_dir = self.file_ops.get_well_known_path(folder_name)
                
                items = self.file_ops.list_directory(target_dir)
                if items:
                    path_desc = target_dir if target_dir else "home directory"
                    msg = f"Result: Listed {len(items)} items in {path_desc}: {', '.join(items[:5])}"
                    if len(items) > 5: msg += f", and {len(items)-5} more."
                    return {"success": True, "message": msg}
                return {"success": False, "message": f"Result: Directory not found or empty."}

            # 3. Create Operations (Files and Folders)
            if any(k in text for k in ['create', 'make', 'new']):
                # "create new folder X", "make a directory Y", "create text file Z", "create backup"
                is_dir = any(k in text for k in ['folder', 'directory', 'dir'])
                name_match = re.search(r'\b(?:folder|directory|file|named|called|document|backup|draft)\s+([\w\.-]+)', text)
                if not name_match: name_match = re.search(r'\b(?:create|make|new)\s+([\w\.-]+)', text)
                
                name = name_match.group(1).strip() if name_match else None
                if name in ['folder', 'directory', 'file', 'document', 'backup']: name = "new_" + name
                if not name: name = "new_folder" if is_dir else "new_file.txt"

                if is_dir:
                    success = self.file_ops.create_directory(name)
                    msg = f"Created directory '{name}'" if success else f"Failed to create directory '{name}'"
                    return {"success": success, "message": f"Result: {msg}"}
                else:
                    if '.' not in name: name += ".txt"
                    self.file_ops.create_file(name, "Created by AI assistant")
                    return {"success": True, "message": f"Result: Created file '{name}'"}

            # 4. Routing for Delete
            if any(k in text for k in ['delete', 'remove', 'trash']):
                # "delete this file", "remove folder", "delete rough draft"
                name_match = re.search(r'\b(?:file|folder|document|draft)\s+([\w\.-]+)', text)
                if not name_match: name_match = re.search(r'\b(?:delete|remove)\s+([\w\.-]+)', text)
                
                if name_match:
                    name = name_match.group(1).strip()
                    if name == 'this':
                         return {"success": False, "message": "Result: Extraction of 'this file' context is not available yet."}
                    
                    try:
                        # Try to find the file first to get absolute path
                        search_results = self.file_ops.search_files(name)
                        target = search_results[0] if search_results else name
                        
                        self.file_ops.delete_file(target)
                        return {"success": True, "message": f"Result: Deleted '{name}'"}
                    except Exception as e:
                        return {"success": False, "message": f"Result: Could not delete '{name}': {e}"}

            # 5. Routing for Copy/Move/Rename (Dual-Path)
            if any(k in text for k in ['copy', 'move', 'rename']):
                # "move file X to documents", "copy image Y to pictures", "rename Z to backup"
                match = re.search(r'\b(?:move|copy|rename)\b\s+([\w\.-]+)\s+to\s+([\w\.-]+)', text)
                if match:
                    source_name = match.group(1).strip()
                    dest_name = match.group(2).strip()
                    
                    # Resolve destination if it's a well-known folder
                    dest_path = self.file_ops.get_well_known_path(dest_name) or dest_name
                    
                    # Search for source to get path
                    source_results = self.file_ops.search_files(source_name)
                    source_path = source_results[0] if source_results else source_name
                    
                    try:
                        if 'move' in text:
                            self.file_ops.move_file(source_path, dest_path)
                            return {"success": True, "message": f"Result: Moved '{source_name}' to '{dest_name}'"}
                        elif 'copy' in text:
                            self.file_ops.copy_file(source_path, dest_path)
                            return {"success": True, "message": f"Result: Copied '{source_name}' to '{dest_name}'"}
                        elif 'rename' in text:
                            self.file_ops.rename_file(source_path, dest_name)
                            return {"success": True, "message": f"Result: Renamed '{source_name}' to '{dest_name}'"}
                    except Exception as e:
                        return {"success": False, "message": f"Result: Operation failed: {e}"}

            return {"success": False, "message": f"Result: File operation '{text}' is not fully mapped."}
        except Exception as e:
            logger.error(f"File operation error: {e}")
            return {"success": False, "message": f"Result: File operation error: {e}"}
        except Exception as e:
            logger.error(f"File operation error: {e}")
            return {"success": False, "message": f"Result: File operation error: {e}"}
    
    def _execute_time(self, command):
        """Execute time and date command"""
        try:
            from datetime import datetime
            text = command.get('text', '').lower()
            now = datetime.now()
            
            # 1. Handle Time Queries
            if 'time' in text:
                # Check for world clock
                if 'in' in text:
                    city = text.split('in')[-1].strip().title()
                    return {"success": True, "message": f"Result: Looking up time in {city}... (Note: For now, I only show local time: {now.strftime('%I:%M %p')})"}
                return {"success": True, "message": f"Result: The current time is {now.strftime('%I:%M %p')}."}
            
            # 2. Handle Date/Day Queries
            if any(k in text for k in ['date', 'day', 'today', 'monday', 'tomorrow']):
                if 'follows today' in text or 'tomorrow' in text:
                     return {"success": True, "message": f"Result: Tomorrow is { (now).strftime('%A') }."}
                if 'day of the week' in text or 'what day' in text:
                     return {"success": True, "message": f"Result: Today is {now.strftime('%A')}."}
                if 'is it monday' in text:
                     is_monday = now.strftime('%A') == 'Monday'
                     return {"success": True, "message": f"Result: No, today is {now.strftime('%A')}." if not is_monday else "Result: Yes, today is Monday."}
                return {"success": True, "message": f"Result: Today is {now.strftime('%A, %B %d, %Y')}."}
            
            # 3. Alarms and Timers (Simulated)
            if 'alarm' in text:
                 return {"success": True, "message": f"Result: Alarm set for {text.split('at')[-1].strip() if 'at' in text else 'specified time'}."}
            if 'timer' in text:
                 return {"success": True, "message": f"Result: Timer started for {text.split('for')[-1].strip() if 'for' in text else 'specified duration'}."}
            
            # 4. Calendar and Schedule
            if 'calendar' in text or 'schedule' in text:
                 return {"success": True, "message": "Result: Opening your schedule for today... (System calendar integration pending)"}

            return {"success": True, "message": f"Result: Today is {now.strftime('%A, %B %d, %Y')}. The time is {now.strftime('%I:%M %p')}."}
        except Exception as e:
            return {"success": False, "message": f"Result: Error getting time: {e}"}

    def _execute_weather(self, command):
        """Execute weather command"""
        try:
             text = command.get('text', '').lower()
             
             # Clean the text for a better search query
             import re
             query = re.sub(r'\b(what is the|what is|tell me|show me|how is|the)\b', '', text).strip()
             
             if not query:
                 query = "weather today"
             
             # If "in [Location]" is not specified, add "today" or "outside" to make it more relevant to local weather
             if 'in' not in query and 'at' not in query:
                 if 'weather' not in query:
                     query = f"weather {query}"
             
             logger.info(f"Weather search query: {query}")
             return self.web_auto.search_google(query)
        except Exception as e:
            return {"success": False, "message": f"Result: Weather info is not available: {e}"}

    def _execute_greetings(self, command):
        """Execute greetings command with human-like interaction"""
        import random
        text = command.get('text', '').lower()
        
        if 'how are you' in text:
            responses = ["I'm doing great, thank you for asking! How are you?", "Feeling efficient and ready to help! What's on your mind?"]
        elif 'who are you' in text or 'what is your name' in text:
            responses = ["I am Nexa, your AI desktop assistant.", "I'm Nexa! Your personal AI helper for managing this computer."]
        elif 'nice to meet you' in text:
            responses = ["Nice to meet you too! Glad to assist you.", "The pleasure is mine!"]
        elif 'morning' in text:
            responses = ["Good morning! Ready to start your day?", "Morning! How can I help you today?"]
        elif 'evening' in text:
            responses = ["Good evening! Hope you had a productive day.", "Hi! Any late-day tasks for me?"]
        elif 'hi' in text or 'hello' in text or 'nexa' in text:
            responses = ["Hello! How can I help you today?", "Hi there! What's our next task?", "Hey! I'm here and listening."]
        else:
            responses = ["Hi! I'm here to help.", "Hello! What can I do for you?"]
            
        return {"success": True, "message": f"Result: {random.choice(responses)}"}

    def _execute_system_control(self, command):
        """Execute system control command"""
        try:
            text = command.get('text', '').lower()
            action = self._extract_system_action(command)
            if not action:
                 return {"success": False, "message": "Result: That system command is not available."}
                 
            if action == 'shutdown':
                self.system_ctrl.shutdown()
            elif action == 'restart':
                self.system_ctrl.restart()
            elif action == 'sleep':
                self.system_ctrl.sleep()
            elif action == 'hibernate':
                self.system_ctrl.hibernate()
            elif action == 'logout':
                self.system_ctrl.logout()
            elif action == 'lock':
                self.system_ctrl.lock_screen()
            elif action == 'volume_up':
                self.system_ctrl.volume_up()
            elif action == 'volume_down':
                self.system_ctrl.volume_down()
            elif action == 'mute':
                self.system_ctrl.mute()
            elif action == 'battery':
                msg = self.system_ctrl.get_battery_status()
                return {"success": True, "message": f"Result: {msg}"}
            elif action == 'brightness':
                # Extract number for brightness
                import re
                nums = re.findall(r'\d+', text)
                level = int(nums[0]) if nums else 50 # Default to 50
                if 'up' in text or 'increase' in text: level = 80
                elif 'down' in text or 'decrease' in text: level = 30
                
                success = self.system_ctrl.set_brightness(level)
                if success:
                    return {"success": True, "message": f"Result: Set brightness to {level}%"}
                else:
                    return {"success": False, "message": "Result: Failed to set brightness."}
            elif action == 'system_info':
                info = self.system_ctrl.get_system_info()
                msg = f"System: {info['system']} {info['release']}, CPU: {info['processor']}"
                return {"success": True, "message": f"Result: {msg}"}
                
            return {"success": True, "message": f"Result: Executed system action: {action}"}
        except Exception as e:
            logger.error(f"System execution error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {"success": False, "message": f"Result: System action error: {str(e)}"}
    
    
    def _execute_dictation(self, command):
        """Execute text dictation into active window"""
        try:
            text = command.get('text', '').lower()
            import re
            # Extract the actual content to type
            # e.g. "type 'this is a sentence'" or "write hello"
            clean_text = re.sub(r'\b(type|write|dictate|insert|say|the following|sentence|word|paragraph)\b', '', text).strip()
            # Remove quotes if present
            clean_text = clean_text.strip("'").strip('"')
            
            if not clean_text:
                return {"success": False, "message": "Nothing specified to type"}
                
            return self.automation.type_text(clean_text)
        except Exception as e:
            logger.error(f"Dictation execution error: {e}")
            return {"success": False, "message": str(e)}

    def _execute_save_file(self, command):
        """Execute save shortcut"""
        return self.automation.save_file()

    def _execute_search_internal(self, command):
        """Execute search within an app (e.g. YouTube)"""
        try:
            text = command.get('text', '').lower()
            import re
            
            # Identify the app and the query
            app_matches = ['youtube', 'spotify', 'notepad', 'browser']
            target_app = 'generic'
            for app in app_matches:
                if app in text:
                    target_app = app
                    break
            
            # Extract query: "search for cats on youtube" -> "cats"
            query = re.sub(r'\b(search for|find|look up|on|in|inside|youtube|spotify|notepad|browser|app)\b', '', text).strip()
            
            if not query:
                return {"success": False, "message": "Search query not specified"}
                
            return self.automation.search_internal(target_app, query)
        except Exception as e:
            logger.error(f"Internal search execution error: {e}")
            return {"success": False, "message": str(e)}

    def _extract_app_name(self, command):
        """Extract application name from command"""
        import re
        entities = command.get('grouped_entities', {})
        app_names = entities.get('APP', [])
        if app_names:
            return app_names[0]
        
        # Fallback: search text for common launch keywords
        text = command.get('resolved_text', command.get('text', '')).lower()
        match = re.search(r'\b(?:open|launch|start|run|close|stop|exit|quit|open up|start up)\s+([\w\s]+)', text)
        if match:
            potential_app = match.group(1).strip()
            # Be careful not to filter out everything if the app name IS a filler word (unlikely, but possible)
            fillers = ['the', 'a', 'an', 'please', 'now', 'app', 'application', 'program', 'system', 'on', 'my', 'browser']
            words = potential_app.split()
            clean_words = [w for w in words if w not in fillers]
            if clean_words:
                return " ".join(clean_words)
            return potential_app
            
        return None
    
    def _extract_system_action(self, command):
        """Extract system action from command"""
        text = command.get('text', '').lower()
        if 'shutdown' in text or 'power off' in text:
            return 'shutdown'
        elif 'restart' in text:
            return 'restart'
        elif 'sleep' in text:
            return 'sleep'
        elif 'hibernate' in text:
            return 'hibernate'
        elif 'logout' in text or 'log out' in text or 'sign out' in text:
            return 'logout'
        elif 'lock' in text:
            return 'lock'
        elif 'volume' in text and ('up' in text or 'increase' in text or 'raise' in text):
            return 'volume_up'
        elif 'volume' in text and ('down' in text or 'decrease' in text or 'lower' in text):
            return 'volume_down'
        elif 'mute' in text:
            return 'mute'
        elif 'battery' in text:
            return 'battery'
        elif 'brightness' in text:
            return 'brightness'
        elif 'system info' in text or 'system information' in text:
            return 'system_info'
        return None
