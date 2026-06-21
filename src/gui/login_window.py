"""Login window UI"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QTabWidget, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from src.core.authentication import Authenticator
from .main_dashboard import MainDashboard
from src.context.session_manager import session_manager
from src.core.logger import logger

class LoginWindow(QMainWindow):
    """Main login window"""
    
    def __init__(self):
        super().__init__()
        self.auth = Authenticator()
        self.initUI()
    
    def initUI(self):
        """Initialize UI"""
        self.setWindowTitle('AI Voice Desktop Control - Login')
        self.setGeometry(100, 100, 600, 500)
        
        # Load stylesheet
        try:
            with open("src/gui/styles/modern_dark.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.warning(f"Could not load stylesheet: {e}")
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Login tab
        login_tab = self._create_login_tab()
        tabs.addTab(login_tab, "Login")
        
        # Register tab
        register_tab = self._create_register_tab()
        tabs.addTab(register_tab, "Register")
        
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        central.setLayout(layout)
    
    def _create_login_tab(self):
        """Create login tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Login to Your Account')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)
        
        # Username
        layout.addWidget(QLabel('Username:'))
        self.login_username = QLineEdit()
        layout.addWidget(self.login_username)
        
        # Password
        layout.addWidget(QLabel('Password:'))
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password)
        
        # Login button
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_register_tab(self):
        """Create register tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Create New Account')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)
        
        # Username
        layout.addWidget(QLabel('Username:'))
        self.reg_username = QLineEdit()
        layout.addWidget(self.reg_username)
        
        # Email
        layout.addWidget(QLabel('Email:'))
        self.reg_email = QLineEdit()
        layout.addWidget(self.reg_email)
        
        # Password
        layout.addWidget(QLabel('Password:'))
        self.reg_password = QLineEdit()
        self.reg_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_password)
        
        # Confirm Password
        layout.addWidget(QLabel('Confirm Password:'))
        self.reg_confirm = QLineEdit()
        self.reg_confirm.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_confirm)
        
        # Register button
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.handle_register)
        layout.addWidget(register_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def handle_login(self):
        """Handle login"""
        try:
            username = self.login_username.text()
            password = self.login_password.text()
            
            if not username or not password:
                QMessageBox.warning(self, 'Error', 'Please enter username and password')
                return
            
            result = self.auth.authenticate(username, password)
            
            if result['success']:
                # Create session
                session_id = session_manager.create_session(result['user_id'])
                
                # Open main window
                self.dashboard = MainDashboard(result['user_id'], username)
                self.dashboard.show()
                self.close()
            else:
                QMessageBox.critical(self, 'Login Failed', 'Invalid credentials')
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            QMessageBox.critical(self, 'Error', str(e))
    
    def handle_register(self):
        """Handle registration"""
        try:
            username = self.reg_username.text()
            email = self.reg_email.text()
            password = self.reg_password.text()
            confirm = self.reg_confirm.text()
            
            if not all([username, email, password, confirm]):
                QMessageBox.warning(self, 'Error', 'Please fill all fields')
                return
            
            if password != confirm:
                QMessageBox.warning(self, 'Error', 'Passwords do not match')
                return
            
            result = self.auth.register_user(username, password, email)
            
            if result['success']:
                QMessageBox.information(self, 'Success', 'Registration successful! Please login.')
                self.reg_username.clear()
                self.reg_email.clear()
                self.reg_password.clear()
                self.reg_confirm.clear()
            
        except Exception as e:
            logger.error(f"Registration error: {e}")
            QMessageBox.critical(self, 'Error', str(e))