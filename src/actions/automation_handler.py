"""Handles desktop automation, keyboard simulation, and dictation"""

import pyautogui
import keyboard
import time
from src.core.logger import logger

class AutomationHandler:
    """Simulates keyboard and mouse interactions"""
    
    def __init__(self):
        # Safety setting for pyautogui
        pyautogui.FAILSAFE = True
        
    def type_text(self, text):
        """Type text into the currently focused window"""
        try:
            logger.info(f"Dictating text: {text}")
            # Small delay to ensure focus
            time.sleep(0.5)
            pyautogui.write(text, interval=0.01)
            return {"success": True, "message": f"Typed: {text}"}
        except Exception as e:
            logger.error(f"Typing error: {e}")
            return {"success": False, "message": str(e)}

    def press_shortcut(self, shortcut):
        """Execute a keyboard shortcut"""
        try:
            logger.info(f"Executing shortcut: {shortcut}")
            # Map friendly names to shortcuts
            mapping = {
                'save': ('ctrl', 's'),
                'select all': ('ctrl', 'a'),
                'copy': ('ctrl', 'c'),
                'paste': ('ctrl', 'v'),
                'undo': ('ctrl', 'z'),
                'enter': ('enter',),
                'new tab': ('ctrl', 't')
            }
            
            keys = mapping.get(shortcut.lower())
            if keys:
                pyautogui.hotkey(*keys)
                return {"success": True, "message": f"Executed shortcut: {shortcut}"}
            return {"success": False, "message": f"Unknown shortcut: {shortcut}"}
        except Exception as e:
            logger.error(f"Shortcut error: {e}")
            return {"success": False, "message": str(e)}

    def save_file(self):
        """Shortcut for saving"""
        return self.press_shortcut('save')

    def search_internal(self, app_name, query):
        """Specialized internal search (e.g., YouTube search bar)"""
        try:
            logger.info(f"Internal search in {app_name} for: {query}")
            # YouTube specific handling (focus search bar with '/')
            if 'youtube' in app_name.lower():
                pyautogui.press('/')
                time.sleep(0.3)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                pyautogui.write(query)
                pyautogui.press('enter')
                return {"success": True, "message": f"Searching YouTube for {query}"}
            
            # Generic: just type and enter
            pyautogui.write(query)
            pyautogui.press('enter')
            return {"success": True, "message": f"Searched for {query}"}
        except Exception as e:
            logger.error(f"Internal search error: {e}")
            return {"success": False, "message": str(e)}
