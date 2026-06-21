"""Text-to-Speech Engine Interface"""

import pyttsx3
import threading
import queue
import time
from src.core.logger import logger

class TextToSpeech:
    """Handles text-to-speech synthesis with a non-blocking background worker"""
    
    def __init__(self):
        self.speech_queue = queue.Queue()
        self.worker_thread = None
        self.running = False
        self.engine = None
        
        try:
            self.start_worker()
            logger.info("Text-to-Speech worker started")
        except Exception as e:
            logger.error(f"Failed to initialize TTS system: {e}")

    def start_worker(self):
        """Start the background worker thread"""
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def _worker_loop(self):
        """Worker thread to process speech queue"""
        try:
            self.engine = pyttsx3.init()
            self.setup_voice()
        except Exception as e:
            logger.error(f"TTS Engine Init Error in worker: {e}")
            return

        while self.running:
            try:
                text = self.speech_queue.get(timeout=1)
                if not text:
                    self.speech_queue.task_done()
                    continue

                logger.info(f"Speaking: '{text}'")
                self.engine.say(text)
                self.engine.runAndWait()
                self.speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"TTS Worker Loop Error: {e}")
                try:
                    self.engine = pyttsx3.init()
                    self.setup_voice()
                except: pass

    def setup_voice(self):
        """Configure voice settings"""
        if not self.engine: return
        try:
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if "Zira" in voice.name or "Eva" in voice.name:
                    self.engine.setProperty('voice', voice.id)
                    break 
            self.engine.setProperty('rate', 180)
            self.engine.setProperty('volume', 1.0)
        except Exception as e:
            logger.warning(f"Error configuring voice: {e}")

    def speak(self, text):
        """Queue text for speech (Non-blocking)"""
        if not text: return
        self.speech_queue.put(text)

    def speak_async(self, text):
        """Alias for speak"""
        self.speak(text)

    def stop(self):
        """Stop the worker"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1)
