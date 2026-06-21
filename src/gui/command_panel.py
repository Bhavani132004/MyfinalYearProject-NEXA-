"""Command history panel"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QListWidget, QListWidgetItem, QMessageBox)
from PyQt5.QtGui import QFont, QColor
from src.core.logger import logger

class CommandPanel(QWidget):
    """Command history panel"""
    
    def __init__(self):
        super().__init__()
        self.commands = []
        self.initUI()
    
    def initUI(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        title = QLabel('Command History')
        title.setFont(QFont('Arial', 12, QFont.Bold))
        header.addWidget(title)
        
        clear_btn = QPushButton('Clear History')
        clear_btn.setMaximumWidth(120)
        clear_btn.clicked.connect(self.clear_history)
        header.addWidget(clear_btn)
        
        layout.addLayout(header)
        
        # Command list
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background-color: #3c3c3c; color: white;")
        layout.addWidget(self.list_widget)
        
        # Stats
        stats_layout = QHBoxLayout()
        self.total_label = QLabel('Total Commands: 0')
        self.success_label = QLabel('Success: 0')
        self.failed_label = QLabel('Failed: 0')
        
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.success_label)
        stats_layout.addWidget(self.failed_label)
        
        layout.addLayout(stats_layout)
        
        self.setLayout(layout)
    
    def add_command(self, command_text, status, timestamp):
        """Add command to history"""
        try:
            item = QListWidgetItem(f"[{timestamp}] {command_text} - {status}")
            
            if status == 'Success':
                item.setForeground(QColor('green'))
            else:
                item.setForeground(QColor('red'))
            
            self.list_widget.addItem(item)
            self.commands.append({'text': command_text, 'status': status, 'time': timestamp})
            self.update_stats()
            
            logger.info(f"Command added to panel: {command_text}")
        except Exception as e:
            logger.error(f"Error adding command: {e}")
    
    def update_stats(self):
        """Update statistics"""
        total = len(self.commands)
        success = sum(1 for c in self.commands if c['status'] == 'Success')
        failed = total - success
        
        self.total_label.setText(f'Total Commands: {total}')
        self.success_label.setText(f'Success: {success}')
        self.failed_label.setText(f'Failed: {failed}')
    
    def clear_history(self):
        """Clear command history"""
        try:
            reply = QMessageBox.question(self, 'Confirm', 'Clear all command history?')
            if reply == QMessageBox.Yes:
                self.list_widget.clear()
                self.commands = []
                self.update_stats()
                logger.info("Command history cleared")
        except Exception as e:
            logger.error(f"Error clearing history: {e}")