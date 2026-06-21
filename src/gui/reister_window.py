"""User registration window"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox)
from PyQt5.QtGui import QFont
from src.auth.authentication import Authenticator
from src.core.logger import logger

class RegisterWindow(QMainWindow):
    """User registration window"""
    
    def __init__(self):
        super().__init__()
        self.auth = Authenticator()
        self.initUI()
    
    def initUI(self):
        """Initialize UI"""
        self.setWindowTitle('AI Voice Desktop Control - Register')
        self.setGeometry(150, 150, 500, 500)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Create New Account')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)
        
        # Username
        layout.addWidget(QLabel('Username:'))
        self.username = QLineEdit()
        self.username.setStyleSheet("background-color: #3c3c3c; color: white; padding: 8px;")
        self.username.setPlaceholderText("Enter username (3-20 chars)")
        layout.addWidget(self.username)
        
        # Email
        layout.addWidget(QLabel('Email:'))
        self.email = QLineEdit()
        self.email.setStyleSheet("background-color: #3c3c3c; color: white; padding: 8px;")
        self.email.setPlaceholderText("Enter valid email")
        layout.addWidget(self.email)
        
        # Password
        layout.addWidget(QLabel('Password:'))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("background-color: #3c3c3c; color: white; padding: 8px;")
        self.password.setPlaceholderText("Min 6 characters")
        layout.addWidget(self.password)
        
        # Confirm Password
        layout.addWidget(QLabel('Confirm Password:'))
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setStyleSheet("background-color: #3c3c3c; color: white; padding: 8px;")
        layout.addWidget(self.confirm_password)
        
        # Terms checkbox
        self.terms_check = QCheckBox('I agree to Terms and Conditions')
        layout.addWidget(self.terms_check)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        register_btn = QPushButton('Register')
        register_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        register_btn.clicked.connect(self.register)
        btn_layout.addWidget(register_btn)
        
        back_btn = QPushButton('Back')
        back_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
        back_btn.clicked.connect(self.go_back)
        btn_layout.addWidget(back_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        central.setLayout(layout)
    
    def register(self):
        """Handle registration"""
        try:
            username = self.username.text().strip()
            email = self.email.text().strip()
            password = self.password.text()
            confirm = self.confirm_password.text()
            
            if not all([username, email, password, confirm]):
                QMessageBox.warning(self, 'Error', 'Please fill all fields')
                return
            
            if len(username) < 3:
                QMessageBox.warning(self, 'Error', 'Username must be at least 3 characters')
                return
            
            if password != confirm:
                QMessageBox.warning(self, 'Error', 'Passwords do not match')
                return
            
            if len(password) < 6:
                QMessageBox.warning(self, 'Error', 'Password must be at least 6 characters')
                return
            
            if not self.terms_check.isChecked():
                QMessageBox.warning(self, 'Error', 'Please accept Terms and Conditions')
                return
            
            result = self.auth.register_user(username, password, email)
            
            if result['success']:
                QMessageBox.information(self, 'Success', 'Registration successful! Please login.')
                self.close()
            else:
                QMessageBox.critical(self, 'Error', 'Registration failed')
        
        except Exception as e:
            logger.error(f"Registration error: {e}")
            QMessageBox.critical(self, 'Error', str(e))
    
    def go_back(self):
        """Go back to login"""
        self.close()