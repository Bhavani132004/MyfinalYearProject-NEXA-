"""Theme manager"""

from PyQt5.QtGui import QFont, QColor, QPalette

class ThemeManager:
    """Manages application themes"""
    
    DARK_THEME = {
        "background": "#2b2b2b",
        "foreground": "#ffffff",
        "primary": "#4CAF50",
        "secondary": "#2196F3",
        "accent": "#FF9800",
        "text": "#ffffff",
        "button": "#3c3c3c"
    }
    
    LIGHT_THEME = {
        "background": "#ffffff",
        "foreground": "#000000",
        "primary": "#4CAF50",
        "secondary": "#2196F3",
        "accent": "#FF9800",
        "text": "#000000",
        "button": "#f0f0f0"
    }
    
    @staticmethod
    def apply_dark_theme(app):
        """Apply dark theme"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#2b2b2b'))
        palette.setColor(QPalette.WindowText, QColor('#ffffff'))
        palette.setColor(QPalette.Button, QColor('#3c3c3c'))
        palette.setColor(QPalette.ButtonText, QColor('#ffffff'))
        app.setPalette(palette)
    
    @staticmethod
    def apply_light_theme(app):
        """Apply light theme"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#ffffff'))
        palette.setColor(QPalette.WindowText, QColor('#000000'))
        palette.setColor(QPalette.Button, QColor('#f0f0f0'))
        palette.setColor(QPalette.ButtonText, QColor('#000000'))
        app.setPalette(palette)
    
    @staticmethod
    def get_stylesheet(theme='dark'):
        """Get stylesheet for theme"""
        if theme == 'dark':
            return ThemeManager.get_dark_stylesheet()
        else:
            return ThemeManager.get_light_stylesheet()
    
    @staticmethod
    def get_dark_stylesheet():
        """Get dark theme stylesheet"""
        return """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLineEdit {
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #555555;
            padding: 5px;
        }
        QTextEdit {
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #555555;
        }
        """
    
    @staticmethod
    def get_light_stylesheet():
        """Get light theme stylesheet"""
        return """
        QMainWindow {
            background-color: #ffffff;
            color: #000000;
        }
        QWidget {
            background-color: #ffffff;
            color: #000000;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
        }
        QLineEdit {
            background-color: #f0f0f0;
            color: #000000;
            border: 1px solid #cccccc;
            padding: 5px;
        }
        """