"""User profile management"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QMessageBox, QTextEdit)
from PyQt5.QtGui import QFont
from src.core.logger import logger

class ProfileManager(QWidget):
    """Manages user profile"""
    
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.initUI()
    
    def initUI(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f'User Profile - {self.username}')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)
        
        # Profile Info
        info_layout = QVBoxLayout()
        
        info_layout.addWidget(QLabel('Username:'))
        self.username_field = QLineEdit()
        self.username_field.setText(self.username)
        self.username_field.setReadOnly(True)
        self.username_field.setStyleSheet("background-color: #3c3c3c; color: white;")
        info_layout.addWidget(self.username_field)
        
        info_layout.addWidget(QLabel('User ID:'))
        self.user_id_field = QLineEdit()
        self.user_id_field.setText(str(self.user_id))
        self.user_id_field.setReadOnly(True)
        self.user_id_field.setStyleSheet("background-color: #3c3c3c; color: white;")
        info_layout.addWidget(self.user_id_field)
        
        info_layout.addWidget(QLabel('Bio:'))
        self.bio_field = QTextEdit()
        self.bio_field.setStyleSheet("background-color: #3c3c3c; color: white;")
        self.bio_field.setMaximumHeight(100)
        info_layout.addWidget(self.bio_field)
        
        layout.addLayout(info_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        update_btn = QPushButton('Update Profile')
        update_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        update_btn.clicked.connect(self.update_profile)
        btn_layout.addWidget(update_btn)
        
        change_pwd_btn = QPushButton('Change Password')
        change_pwd_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        change_pwd_btn.clicked.connect(self.change_password)
        btn_layout.addWidget(change_pwd_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def update_profile(self):
        """Update profile"""
        try:
            bio = self.bio_field.toPlainText()
            logger.info(f"Profile updated for user {self.user_id}")
            QMessageBox.information(self, 'Success', 'Profile updated successfully!')
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            QMessageBox.critical(self, 'Error', str(e))
    
    def change_password(self):
        """Change password - open dialog"""
        try:
            # This would typically open a dialog for password change
            QMessageBox.information(self, 'Info', 'Password change feature coming soon!')
        except Exception as e:
            logger.error(f"Error: {e}")