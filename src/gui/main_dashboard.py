"""Main application dashboard"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,
                              QCheckBox, QFrame, QMenuBar, QAction, QDockWidget,
                              QListWidget, QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QSize
from PyQt5.QtGui import QFont, QColor, QIcon
from src.core.main_engine import VoiceControlEngine

from src.core.logger import logger
from src.input.audio_capture import AudioCapture
from .assistant_visualizer import AssistantVisualizer
from .chat_widgets import MessageWidget, TypingIndicator
from .personalization_dialog import PersonalizationDialog
import numpy as np
import threading
import speech_recognition as sr
import pyaudio
from queue import Queue
import time

class ContinuousVoiceThread(QThread):
    """Dedicated thread for continuous background listening - NO BLOCKING"""
    audio_captured = pyqtSignal(object) # Emit sr.AudioData
    error_occurred = pyqtSignal(str)
    
    def __init__(self, speech_processor):
        super().__init__()
        self.processor = speech_processor
        self.running = False
        self._stop_event = threading.Event()

    def run(self):
        self.running = True
        self._stop_event.clear()
        
        try:
            mic = sr.Microphone()
            with mic as source:
                logger.info("Calibrating mic in background...")
                self.processor.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                while not self._stop_event.is_set():
                    try:
                        # listen() is blocking but with short timeout/limit it's okay.
                        # The key is we DON'T transcribe here.
                        audio = self.processor.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        self.audio_captured.emit(audio)
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        if not self._stop_event.is_set():
                            logger.error(f"Listening error: {e}")
                            self.error_occurred.emit(str(e))
                            self.msleep(100)
        except Exception as e:
            logger.error(f"Critical Mic Error: {e}")
            self.error_occurred.emit(str(e))
        
        self.running = False

    def stop(self):
        self._stop_event.set()
        self.wait()

class TranscriptionWorker(QThread):
    """Worker for offloading transcription to keep listener free"""
    text_transcribed = pyqtSignal(str)
    
    def __init__(self, processor):
        super().__init__()
        self.processor = processor
        self.queue = Queue()
        self.running = True

    def run(self):
        while self.running:
            if not self.queue.empty():
                audio_data = self.queue.get()
                try:
                    text = self.processor.transcribe(audio_data)
                    if text:
                        self.text_transcribed.emit(text)
                except Exception as e:
                    logger.error(f"Worker transcription error: {e}")
            else:
                time.sleep(0.1)

    def stop(self):
        self.running = False
        self.wait()

class ProcessingWorker(QThread):
    """Worker for executing commands in order without blocking UI"""
    finished = pyqtSignal(dict)
    
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.queue = Queue()
        self.running = True

    def run(self):
        while self.running:
            if not self.queue.empty():
                text = self.queue.get()
                try:
                    res = self.engine.process_text_command(text)
                    self.finished.emit(res)
                except Exception as e:
                    logger.error(f"Worker processing error: {e}")
            else:
                time.sleep(0.1)

class StatusBadge(QFrame):
    """A floating status badge at the top of the interface"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusBadge")
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 5, 12, 5)
        
        self.icon_label = QLabel("⏸")
        self.status_label = QLabel("Idle")
        
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.status_label)
        
        self.setStyleSheet("""
            #statusBadge {
                background: rgba(69, 71, 90, 0.6);
                border-radius: 15px;
                border: 1px solid rgba(137, 180, 250, 0.3);
            }
            QLabel { color: #89b4fa; font-weight: bold; font-size: 12px; }
        """)

    def update_status(self, text, icon, color="#89b4fa"):
        self.status_label.setText(text)
        self.icon_label.setText(icon)
        self.icon_label.setStyleSheet(f"color: {color};")
        self.status_label.setStyleSheet(f"color: {color};")

class AudioEnergyWorker(QThread):
    """Lightweight worker to sample mic volume for visualization"""
    energy_detected = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.p = pyaudio.PyAudio()
        self.stream = None

    def run(self):
        self.running = True
        try:
            self.stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=512
            )
            
            while self.running:
                data = self.stream.read(512, exception_on_overflow=False)
                # Calculate RMS (energy)
                audio_data = np.frombuffer(data, dtype=np.int16)
                if len(audio_data) > 0:
                    energy = np.sqrt(np.mean(audio_data**2))
                    # Normalize energy to 0.0 - 1.0 range (heuristic)
                    normalized = min(1.0, energy / 1000.0)
                    self.energy_detected.emit(normalized)
                time.sleep(0.01)
                
        except Exception as e:
            logger.debug(f"Energy worker inactive: {e}")
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            self.running = False

    def stop(self):
        self.running = False
        self.wait()

class MainDashboard(QMainWindow):
    """Main application dashboard with advanced features"""
    
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.engine = VoiceControlEngine()
        self.engine.set_user(user_id)
        self.processing_thread = None
        self.assistant_active = False
        self.voice_thread = None
        self.transcription_worker = TranscriptionWorker(self.engine.speech_processor)
        self.processing_worker = ProcessingWorker(self.engine)
        self.energy_worker = AudioEnergyWorker()
        self._last_app_context = None
        
        # Connect workers
        self.transcription_worker.text_transcribed.connect(self.on_voice_text_detected)
        self.processing_worker.finished.connect(self.on_processing_finished)
        self.energy_worker.energy_detected.connect(self._on_energy_detected)
        
        self.transcription_worker.start()
        self.processing_worker.start()
        
        # Proactive context monitoring
        self.context_timer = QTimer(self)
        self.context_timer.timeout.connect(self._check_proactive_context)
        self.context_timer.start(10000)
        
        # Follow-up listening logic
        self.follow_up_timer = QTimer(self)
        self.follow_up_timer.setSingleShot(True)
        self.follow_up_timer.timeout.connect(self._on_follow_up_timeout)
        
        self.initUI()
        self.initMenuBar()
        self.initHistoryDock()
        
        logger.info(f"Dashboard opened for user: {username}")
        
        # Auto-start Assistant
        QTimer.singleShot(1000, lambda: self.assistant_toggle.setChecked(True))
    
    def initMenuBar(self):
        """Initialize the modern menu bar"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu('&File')
        
        clear_history_act = QAction('Clear Chat', self)
        clear_history_act.triggered.connect(self.clear_chat)
        file_menu.addAction(clear_history_act)
        
        file_menu.addSeparator()
        
        logout_act = QAction('Logout', self)
        logout_act.triggered.connect(self.logout)
        file_menu.addAction(logout_act)
        
        exit_act = QAction('Exit', self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)
        
        # View Menu
        view_menu = menubar.addMenu('&View')
        
        toggle_history_act = QAction('Toggle History Panel', self)
        toggle_history_act.setCheckable(True)
        toggle_history_act.setChecked(True)
        toggle_history_act.triggered.connect(self.toggle_history_dock)
        view_menu.addAction(toggle_history_act)
        self.toggle_history_act = toggle_history_act
        
        # Settings Menu
        settings_menu = menubar.addMenu('&Settings')
        
        personalize_act = QAction('Personalization...', self)
        personalize_act.triggered.connect(self.open_personalization)
        settings_menu.addAction(personalize_act)
        
        # Help Menu
        help_menu = menubar.addMenu('&Help')
        about_act = QAction('About NEXA', self)
        about_act.triggered.connect(lambda: QMessageBox.about(self, "About NEXA", "NEXA AI Assistant v2.0\nRedesigned for human-like interaction."))
        help_menu.addAction(about_act)

    def initHistoryDock(self):
        """Initialize the command history side panel"""
        self.history_dock = QDockWidget("Command History", self)
        self.history_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.history_list = QListWidget()
        self.history_list.setObjectName("historyList")
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        
        self.history_dock.setWidget(self.history_list)
        self.addDockWidget(Qt.RightDockWidgetArea, self.history_dock)
        self.refresh_history()

    def initUI(self):
        """Initialize UI with modern redesigned layout"""
        self.setWindowTitle(f'NEXA - {self.username}')
        self.setMinimumSize(1100, 800)
        
        # Load stylesheet
        try:
            with open("src/gui/styles/modern_dark.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.warning(f"Could not load stylesheet: {e}")
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # LEFT PANEL
        left_panel = QFrame()
        left_panel.setObjectName("assistantArea")
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(25, 25, 25, 25)
        
        # Status Badge at top
        status_layout = QHBoxLayout()
        self.status_badge = StatusBadge()
        status_layout.addStretch()
        status_layout.addWidget(self.status_badge)
        status_layout.addStretch()
        left_layout.addLayout(status_layout)
        
        left_layout.addSpacing(20)
        
        # Greetings
        user_info = QLabel(f"Welcome back, {self.username}")
        user_info.setObjectName("welcomeLabel")
        user_info.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(user_info)
        
        # Assistant Visualizer
        self.visualizer = AssistantVisualizer()
        left_layout.addStretch()
        left_layout.addWidget(self.visualizer, alignment=Qt.AlignCenter)
        left_layout.addStretch()
        
        # Toggle Switch
        toggle_container = QFrame()
        toggle_container.setObjectName("toggleContainer")
        toggle_layout = QHBoxLayout(toggle_container)
        self.assistant_toggle = QCheckBox("Voice Assistant Active")
        self.assistant_toggle.setObjectName("toggleSwitch")
        self.assistant_toggle.setCursor(Qt.PointingHandCursor)
        self.assistant_toggle.stateChanged.connect(self.toggle_assistant)
        toggle_layout.addWidget(self.assistant_toggle)
        left_layout.addWidget(toggle_container)
        
        main_layout.addWidget(left_panel)

        # RIGHT PANEL
        right_panel = QFrame()
        right_panel.setObjectName("chatArea")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("chatScrollArea")
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.addStretch()
        self.scroll_area.setWidget(self.chat_container)
        right_layout.addWidget(self.scroll_area)
        
        self.typing_indicator = TypingIndicator()
        right_layout.addWidget(self.typing_indicator)
        
        input_container = QFrame()
        input_container.setObjectName("inputContainer")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(10, 5, 10, 5)
        
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Type a command or use voice...")
        self.cmd_input.setObjectName("commandLine")
        self.cmd_input.returnPressed.connect(self.run_text_command)
        input_layout.addWidget(self.cmd_input)
        
        self.run_btn = QPushButton("Send")
        self.run_btn.setObjectName("sendButton")
        self.run_btn.clicked.connect(self.run_text_command)
        input_layout.addWidget(self.run_btn)
        
        right_layout.addWidget(input_container)
        main_layout.addWidget(right_panel)

    def add_message(self, text, is_user=True):
        """Add a message bubble to the chat feed"""
        message = MessageWidget(text, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, message)
        QTimer.singleShot(100, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def _on_energy_detected(self, energy):
        if self.assistant_active:
            self.visualizer.set_energy(energy)

    def toggle_assistant(self, state):
        """Handle Assistant ON/OFF toggle with robust QThread listening"""
        if state == Qt.Checked:
            self.assistant_active = True
            self.visualizer.set_state(AssistantVisualizer.LISTENING)
            self.status_badge.update_status("Listening", "🎤", "#89b4fa")
            
            # Start background thread
            if not self.voice_thread or not self.voice_thread.isRunning():
                self.voice_thread = ContinuousVoiceThread(self.engine.speech_processor)
                self.voice_thread.audio_captured.connect(self._on_audio_captured)
                self.voice_thread.error_occurred.connect(self.on_processing_error)
                self.voice_thread.start()
            
            if not self.energy_worker.isRunning():
                self.energy_worker.start()
                
            logger.info("Continuous assistant activated")
        else:
            self.assistant_active = False
            self.visualizer.set_state(AssistantVisualizer.IDLE)
            self.status_badge.update_status("Idle", "⏸", "#45475a")
            if self.voice_thread: self.voice_thread.stop()
            if self.energy_worker.isRunning(): self.energy_worker.stop()
            logger.info("Continuous assistant deactivated")

    def _on_audio_captured(self, audio):
        """Put audio into transcription queue immediately"""
        if self.assistant_active:
            self.transcription_worker.queue.put(audio)

    def on_voice_text_detected(self, text):
        """Handle text detected by the continuous thread - DIRECT EXECUTION (No Wake Word)"""
        if not self.assistant_active or not text:
            return
        
        logger.info(f"Direct voice command detected: '{text}'")
        self.add_message(text, is_user=True)
        
        self.visualizer.set_state(AssistantVisualizer.THINKING)
        self.status_badge.update_status("Thinking", "🤖", "#fab387")
        self.typing_indicator.show()
        
        # Queue the command instead of spawning a new thread
        self.processing_worker.queue.put(text.lower())

    def _on_follow_up_timeout(self):
        """Reset visualizer state when no follow-up is detected"""
        if self.assistant_active:
            self.visualizer.set_state(AssistantVisualizer.IDLE)
            self.status_badge.update_status("Listening", "🎤", "#89b4fa")


    def run_text_command(self):
        """Run command from text input immediately"""
        text = self.cmd_input.text().strip()
        if not text:
            return
            
        self.add_message(text, is_user=True)
        self.cmd_input.clear()
        
        self.visualizer.set_state(AssistantVisualizer.THINKING)
        self.status_badge.update_status("Thinking", "🤖", "#fab387")
        self.typing_indicator.show()
        
        # Queue the command
        self.processing_worker.queue.put(text.lower())


    def on_processing_finished(self, result):
        """Handle processing finished immediately"""
        try:
            self.typing_indicator.hide()
            
            # Show assistant response
            if result.get('success'):
                self.visualizer.set_state(AssistantVisualizer.SPEAKING)
                self.status_badge.update_status("Speaking", "🔊", "#a6e3a1")
                msg = result.get('message', 'Done!')
                
                # Add human-like follow-up
                from src.actions.command_executor import ResponseGenerator
                follow_up = ResponseGenerator.get_follow_up()
                msg = f"{msg}\n\n{follow_up}"
                
                self.add_message(msg, is_user=False)
                
                # Immediate history refresh
                self.refresh_history()
                
                # Quick reset/continue
                QTimer.singleShot(1500, self._post_process_status)
            else:
                self.on_processing_error(result.get('message', 'I encountered an issue.'))

        except Exception as e:
            logger.error(f"Processing error: {e}")

    def _post_process_status(self):
        # After execution, we ALWAYS return to IDLE unless a new wake word is heard
        # This prevents the "disturbing" continuous execution the user complained about
        if self.assistant_active:
            self.visualizer.set_state(AssistantVisualizer.LISTENING)
            self.status_badge.update_status("Listening", "🎤", "#89b4fa")
        else:
            self.visualizer.set_state(AssistantVisualizer.IDLE)
            self.status_badge.update_status("Idle", "⏸", "#45475a")

    def on_processing_error(self, error_msg):
        self.typing_indicator.hide()
        # Don't show "No speech detected" as an error in continuous mode
        if "No speech detected" not in error_msg:
            self.add_message(f"Trouble: {error_msg}", is_user=False)
        self._post_process_status()

    def refresh_history(self):
        """Refresh command history dock list"""
        try:
            history = self.engine.get_command_history(limit=15)
            self.history_list.clear()
            for cmd in history:
                self.history_list.addItem(QListWidgetItem(cmd))
        except Exception as e: logger.error(f"History error: {e}")

    def on_history_item_clicked(self, item):
        """Run command from history immediately"""
        self.cmd_input.setText(item.text())
        self.run_text_command()

    def toggle_history_dock(self, visible):
        self.history_dock.setVisible(visible)

    def open_personalization(self):
        """Open the modern personalization dialog"""
        PersonalizationDialog(self.engine, self).exec_()
        # Reload any immediate UI changes if necessary
        try:
            with open("src/gui/styles/modern_dark.qss", "r") as f:
                self.setStyleSheet(f.read())
        except: pass

    def clear_chat(self):
        """Clear message feed"""
        while self.chat_layout.count() > 1: # Keep the bottom stretch
            item = self.chat_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self.add_message("Chat cleared.", is_user=False)

    def logout(self):
        from src.gui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def _check_proactive_context(self):
        """Periodic check for proactive suggestions (restored/enhanced)"""
        if not self.assistant_active: return
            
        suggestion = self.engine.get_suggestion()
        if suggestion and suggestion != self._last_app_context:
            self.add_message(f"💡 {suggestion}", is_user=False)
            self._last_app_context = suggestion
            # Small voice audio for suggestion
            self.engine.speak(f"Suggestion: {suggestion}")
