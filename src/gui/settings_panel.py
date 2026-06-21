"""Settings panel"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QComboBox, QSlider, QPushButton, QCheckBox, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.core.logger import logger

class SettingsPanel(QWidget):
    """User settings panel"""
    
    def __init__(self):
        super().__init__()
        self.settings = {}
        self.initUI()
    
    def initUI(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Settings')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)
        
        # Audio Settings
        layout.addWidget(QLabel('Audio Settings:'))
        
        audio_layout = QVBoxLayout()
        
        audio_layout.addWidget(QLabel('Recording Duration (seconds):'))
        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(1)
        self.duration_spin.setMaximum(30)
        self.duration_spin.setValue(5)
        audio_layout.addWidget(self.duration_spin)
        
        audio_layout.addWidget(QLabel('Microphone Device:'))
        self.mic_combo = QComboBox()
        self.mic_combo.addItems(['Default', 'Microphone 1', 'Microphone 2'])
        audio_layout.addWidget(self.mic_combo)
        
        layout.addLayout(audio_layout)
        
        # Theme Settings
        layout.addWidget(QLabel('Theme Settings:'))
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel('Theme:'))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Dark', 'Light'])
        theme_layout.addWidget(self.theme_combo)
        
        layout.addLayout(theme_layout)
        
        # Voice Settings
        layout.addWidget(QLabel('Voice Settings:'))
        
        voice_layout = QVBoxLayout()
        
        self.voice_feedback = QCheckBox('Voice Feedback')
        self.voice_feedback.setChecked(True)
        voice_layout.addWidget(self.voice_feedback)
        
        self.auto_execute = QCheckBox('Auto Execute Commands')
        self.auto_execute.setChecked(True)
        voice_layout.addWidget(self.auto_execute)
        
        layout.addLayout(voice_layout)
        
        # Confidence Threshold
        layout.addWidget(QLabel('Confidence Threshold:'))
        
        confidence_layout = QHBoxLayout()
        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setMinimum(0)
        self.confidence_slider.setMaximum(100)
        self.confidence_slider.setValue(70)
        self.confidence_label = QLabel('70%')
        self.confidence_slider.valueChanged.connect(self.update_confidence)
        
        confidence_layout.addWidget(self.confidence_slider)
        confidence_layout.addWidget(self.confidence_label)
        
        layout.addLayout(confidence_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton('Save Settings')
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        reset_btn = QPushButton('Reset to Default')
        reset_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        reset_btn.clicked.connect(self.reset_settings)
        btn_layout.addWidget(reset_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def update_confidence(self):
        """Update confidence label"""
        value = self.confidence_slider.value()
        self.confidence_label.setText(f'{value}%')
    
    def save_settings(self):
        """Save settings"""
        try:
            self.settings = {
                'duration': self.duration_spin.value(),
                'microphone': self.mic_combo.currentText(),
                'theme': self.theme_combo.currentText(),
                'voice_feedback': self.voice_feedback.isChecked(),
                'auto_execute': self.auto_execute.isChecked(),
                'confidence': self.confidence_slider.value() / 100.0
            }
            logger.info(f"Settings saved: {self.settings}")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def reset_settings(self):
        """Reset to defaults"""
        try:
            self.duration_spin.setValue(5)
            self.mic_combo.setCurrentIndex(0)
            self.theme_combo.setCurrentIndex(0)
            self.voice_feedback.setChecked(True)
            self.auto_execute.setChecked(True)
            self.confidence_slider.setValue(70)
            logger.info("Settings reset to default")
        except Exception as e:
            logger.error(f"Error resetting settings: {e}")