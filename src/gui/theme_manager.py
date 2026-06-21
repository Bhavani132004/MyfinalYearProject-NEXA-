"""Theme manager for application styling"""

from PyQt5.QtGui import QFont, QColor, QPalette

class ThemeManager:
    """Manages application themes"""
    
    DARK_THEME = {
        "background": "#2b2b2b",
        "foreground": "#ffffff",
        "primary": "#0d47a1",
        "secondary": "#1976d2",
        "accent": "#00bcd4",
        "text": "#ffffff"
    }
    
    LIGHT_THEME = {
        "background": "#ffffff",
        "foreground": "#000000",
        "primary": "#1976d2",
        "secondary": "#0d47a1",
        "accent": "#00bcd4",
        "text": "#000000"
    }
    
    @staticmethod
    def apply_dark_theme(app):
        """Apply dark theme"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(43, 43, 43))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        app.setPalette(palette)
    
    @staticmethod
    def apply_light_theme(app):
        """Apply light theme"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        app.setPalette(palette)