
"""Custom chat bubbles for messaging interface"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtProperty, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

class TypeWriterLabel(QLabel):
    """A label that displays text character by character for a more natural feel"""
    finished = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.full_text = text
        self.current_text = ""
        self.char_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_text)
        self.setWordWrap(True)

    def start_typing(self, speed=30):
        self.current_text = ""
        self.char_index = 0
        self.timer.start(speed)

    def _update_text(self):
        if self.char_index < len(self.full_text):
            self.current_text += self.full_text[self.char_index]
            self.setText(self.current_text)
            self.char_index += 1
        else:
            self.timer.stop()
            self.finished.emit()

class ChatBubble(QFrame):
    """Base class for chat bubbles with rounded corners and styling"""
    
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.initUI(text)
        
        # Fade in animation
        self.setWindowOpacity(0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(400)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def initUI(self, text):
        layout = QVBoxLayout()
        
        if self.is_user:
            self.label = QLabel(text)
            self.setObjectName("userBubble")
            self.label.setStyleSheet("color: #ffffff; background: transparent; font-size: 13px;")
        else:
            self.label = TypeWriterLabel(text)
            self.setObjectName("assistantBubble")
            self.label.setStyleSheet("color: #cdd6f4; background: transparent; font-size: 13px;")
            QTimer.singleShot(200, self.label.start_typing)
            
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        layout.setContentsMargins(15, 12, 15, 12)
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.setMinimumHeight(45)
        self.setMinimumWidth(80)
        self.setMaximumWidth(700)

class MessageWidget(QWidget):
    """A container that aligns the chat bubble to left or right"""
    
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        
        self.bubble = ChatBubble(text, is_user)
        
        if is_user:
            layout.addStretch()
            layout.addWidget(self.bubble)
        else:
            layout.addWidget(self.bubble)
            layout.addStretch()
            
        self.setLayout(layout)

class TypingIndicator(QWidget):
    """A small widget to show 'Assistant is typing...' message or animation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        self.label = QLabel("Thinking...")
        self.label.setStyleSheet("color: #9399b2; font-style: italic; font-size: 12px;")
        layout.addWidget(self.label)
        layout.addStretch()
        
        self.setLayout(layout)
        self.hide() # Hidden by default
