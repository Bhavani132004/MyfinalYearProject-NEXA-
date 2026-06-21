
"""Modern personalization dialog for user settings"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QCheckBox, QScrollArea, 
                             QWidget, QFrame, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt
import json

class PersonalizationDialog(QDialog):
    """
    A modern, premium dialog for user personalization.
    Allows editing Preferences and Application Aliases.
    """
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.initUI()
        self.load_settings()

    def initUI(self):
        self.setWindowTitle("NEXA - Personalization")
        self.setMinimumSize(500, 600)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("Personalization & Settings")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #89b4fa;")
        layout.addWidget(header)
        
        # Scroll Area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        
        # General Preferences Section
        scroll_layout.addWidget(self._create_section_label("General Preferences"))
        self.prefs_edit = QTextEdit()
        self.prefs_edit.setPlaceholderText('{"recording_duration": 5, "voice_feedback": true}')
        self.prefs_edit.setMinimumHeight(150)
        scroll_layout.addWidget(self.prefs_edit)
        
        # Aliases Section
        scroll_layout.addWidget(self._create_section_label("Application Aliases"))
        self.aliases_edit = QTextEdit()
        self.aliases_edit.setPlaceholderText('{"my browser": "chrome", "math": "calculator"}')
        self.aliases_edit.setMinimumHeight(150)
        scroll_layout.addWidget(self.aliases_edit)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Buttons
        btns = QHBoxLayout()
        btns.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedWidth(100)
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save & Apply")
        save_btn.setObjectName("recordBtn") # Reuse the green primary button style
        save_btn.setFixedWidth(150)
        save_btn.clicked.connect(self.save_settings)
        btns.addWidget(save_btn)
        
        layout.addLayout(btns)

    def _create_section_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #cdd6f4; margin-top: 10px;")
        return lbl

    def load_settings(self):
        try:
            prefs = self.engine.get_user_preferences()
            aliases = prefs.pop('aliases', {})
            
            self.prefs_edit.setText(json.dumps(prefs, indent=4))
            self.aliases_edit.setText(json.dumps(aliases, indent=4))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load settings: {e}")

    def save_settings(self):
        try:
            prefs = json.loads(self.prefs_edit.toPlainText())
            aliases = json.loads(self.aliases_edit.toPlainText())
            
            # Combine
            prefs['aliases'] = aliases
            
            self.engine.update_user_preferences(prefs)
            QMessageBox.information(self, "Success", "Settings applied successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Invalid Format", f"Please ensure settings are in valid JSON format.\n\nError: {e}")
