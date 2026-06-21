
"""Real-time voice visualization"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QPen, QColor
import numpy as np

class VoiceVisualizer(QWidget):
    """Visualizes voice input in real-time"""
    
    def __init__(self):
        super().__init__()
        self.audio_data = []
        self.initUI()
    
    def initUI(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        title = QLabel('Voice Visualizer')
        title.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(title)
        
        self.canvas = VoiceCanvas()
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
    
    def update_audio(self, audio_data):
        """Update audio visualization"""
        self.audio_data = audio_data
        self.canvas.update_waveform(audio_data)

class VoiceCanvas(QWidget):
    """Canvas for visualizing waveform"""
    
    def __init__(self):
        super().__init__()
        self.waveform = []
        self.setMinimumHeight(150)
        self.setStyleSheet("background-color: #1a1a1a; border: 1px solid #4CAF50;")
    
    def update_waveform(self, audio_data):
        """Update waveform data"""
        if isinstance(audio_data, np.ndarray):
            # Downsample for visualization
            step = max(1, len(audio_data) // 200)
            self.waveform = audio_data[::step].tolist()
        else:
            self.waveform = []
        self.update()
    
    def paintEvent(self, event):
        """Paint waveform"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Draw background
        painter.fillRect(self.rect(), QColor('#1a1a1a'))
        
        if self.waveform:
            # Draw waveform
            pen = QPen(QColor('#4CAF50'), 2)
            painter.setPen(pen)
            
            scale_x = width / len(self.waveform)
            center_y = height / 2
            scale_y = height / 2 * 0.8
            
            for i in range(len(self.waveform) - 1):
                x1 = i * scale_x
                y1 = center_y - self.waveform[i] * scale_y
                
                x2 = (i + 1) * scale_x
                y2 = center_y - self.waveform[i + 1] * scale_y
                
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        
        # Draw center line
        pen = QPen(QColor('#555555'), 1)
        painter.setPen(pen)
        painter.drawLine(0, height // 2, width, height // 2)