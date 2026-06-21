"""
AI-Driven Voice Based Intelligent Desktop Control System
Main Application Entry Point

This is the primary entry point for the application. It initializes all
components and starts the GUI.

Author: AI Voice Control Team
Version: 1.0.0
License: MIT
"""

import sys
import os
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QTimer
from src.gui.login_window import LoginWindow
from src.core.logger import setup_logger
from src.core.config_manager import config
from src.core.db_handler import DatabaseHandler
import logging

# Initialize logging
logger = setup_logger(name="MainApp", level=logging.INFO)

class ApplicationInitializer:
    """Initializes all application components"""
    
    def __init__(self):
        self.logger = logger
        self.config = config
        self.db = None
        self.app = None
    
    def check_environment(self):
        """Check system environment and requirements"""
        try:
            self.logger.info("=" * 70)
            self.logger.info("AI Voice Desktop Control System - Initialization")
            self.logger.info("=" * 70)
            
            # Check Python version
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            self.logger.info(f"Python Version: {python_version}")
            
            if sys.version_info < (3, 8):
                self.logger.critical("Python 3.8 or higher required")
                return False
            
            # Check required directories
            required_dirs = [
                'data',
                'data/database',
                'data/models',
                'data/user_profiles',
                'logs',
                'src',
                'config'
            ]
            
            for directory in required_dirs:
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    self.logger.info(f"Created directory: {directory}")
                else:
                    self.logger.info(f"Found directory: {directory}")
            
            return True
        
        except Exception as e:
            self.logger.critical(f"Environment check failed: {e}")
            return False
    
    def initialize_database(self):
        """Initialize database connection"""
        try:
            self.logger.info("Initializing database...")
            self.db = DatabaseHandler()
            self.logger.info("[OK] Database initialized successfully")
            return True
        
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            return False
    
    def load_configuration(self):
        """Load application configuration"""
        try:
            self.logger.info("Loading configuration...")
            
            # Load default config
            app_name = self.config.get('app.name', 'AI Voice Desktop Control')
            app_version = self.config.get('app.version', '1.0.0')
            debug = self.config.get('app.debug', False)
            
            self.logger.info(f"App Name: {app_name}")
            self.logger.info(f"App Version: {app_version}")
            self.logger.info(f"Debug Mode: {debug}")
            
            # Log audio settings
            sample_rate = self.config.get('speech.sample_rate', 16000)
            chunk_size = self.config.get('speech.chunk_size', 1024)
            
            self.logger.info(f"Audio Sample Rate: {sample_rate} Hz")
            self.logger.info(f"Audio Chunk Size: {chunk_size}")
            
            # Log NLP settings
            nlp_model = self.config.get('nlp.model_type', 'bert')
            confidence_threshold = self.config.get('nlp.confidence_threshold', 0.7)
            
            self.logger.info(f"NLP Model: {nlp_model}")
            self.logger.info(f"Confidence Threshold: {confidence_threshold}")
            
            # Log GUI settings
            theme = self.config.get('gui.theme', 'dark')
            window_width = self.config.get('gui.window_width', 1000)
            window_height = self.config.get('gui.window_height', 700)
            
            self.logger.info(f"Theme: {theme}")
            self.logger.info(f"Window Size: {window_width}x{window_height}")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Configuration loading failed: {e}")
            return False
    
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        try:
            self.logger.info("\nChecking dependencies...")
            
            dependencies = {
                'PyQt5': 'PyQt5.QtWidgets',
                'numpy': 'numpy',
                'soundfile': 'soundfile',
                'librosa': 'librosa',
                'sqlalchemy': 'sqlalchemy',
                'pyyaml': 'yaml',
                'speech_recognition': 'speech_recognition'
            }
            
            missing = []
            
            for name, module in dependencies.items():
                try:
                    __import__(module)
                    self.logger.info(f"✓ {name} - OK")
                except ImportError:
                    missing.append(name)
                    self.logger.warning(f"✗ {name} - Missing")
            
            if missing:
                self.logger.error(f"Missing dependencies: {', '.join(missing)}")
                self.logger.error("Run: pip install -r requirements.txt")
                return False
            
            self.logger.info("✓ All dependencies installed")
            return True
        
        except Exception as e:
            self.logger.error(f"Dependency check failed: {e}")
            return False
    
    def create_application(self):
        """Create PyQt5 application"""
        try:
            self.logger.info("\nInitializing PyQt5 application...")
            
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("AI Voice Desktop Control")
            self.app.setApplicationVersion("1.0.0")
            self.app.setStyle('Fusion')
            
            self.logger.info("✓ PyQt5 application created")
            return True
        
        except Exception as e:
            self.logger.error(f"Application creation failed: {e}")
            return False
    
    def create_splash_screen(self):
        """Create splash screen"""
        try:
            self.logger.info("Creating splash screen...")
            
            # Create a simple splash screen with text
            splash_pixmap = QPixmap(400, 300)
            splash_pixmap.fill(QColor(43, 43, 43))  # Dark background
            
            splash = QSplashScreen(splash_pixmap)
            splash.setWindowTitle("Starting AI Voice Control...")
            
            # Add text
            from PyQt5.QtGui import QPainter
            painter = QPainter(splash_pixmap)
            painter.setPen(QColor(255, 255, 255))
            
            font = QFont("Arial", 16, QFont.Bold)
            painter.setFont(font)
            
            painter.drawText(
                splash_pixmap.rect(),
                Qt.AlignCenter,
                "AI Voice Desktop Control\nv1.0.0\n\nInitializing..."
            )
            painter.end()
            
            splash.setPixmap(splash_pixmap)
            splash.show()
            
            self.app.processEvents()
            
            self.logger.info("✓ Splash screen created")
            return splash
        
        except Exception as e:
            self.logger.warning(f"Splash screen creation failed: {e}")
            return None
    
    def verify_models(self):
        """Verify that model configuration files exist"""
        try:
            self.logger.info("\nVerifying model configurations...")
            
            model_paths = {
                'Whisper': 'data/models/whisper/config.json',
                'Wav2Vec2': 'data/models/wav2vec2/config.json',
                'BERT Intent': 'data/models/bert_intent/config.json',
                'Voice Auth': 'data/models/voice_auth/config.json'
            }
            
            all_ok = True
            for name, path in model_paths.items():
                if os.path.exists(path):
                    self.logger.info(f"✓ {name} configuration found")
                else:
                    self.logger.warning(f"✗ {name} configuration not found")
                    all_ok = False
            
            if not all_ok:
                self.logger.warning("Some model configurations missing")
                self.logger.warning("Models will be downloaded on first use")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Model verification failed: {e}")
            return False
    
    def initialize_all(self):
        """Initialize all components"""
        try:
            self.logger.info("\n" + "=" * 70)
            self.logger.info("INITIALIZATION SEQUENCE START")
            self.logger.info("=" * 70)
            
            # Step 1: Check environment
            if not self.check_environment():
                self.logger.critical("Environment check failed")
                return False
            
            self.logger.info("✓ Environment check passed")
            
            # Step 2: Check dependencies
            if not self.check_dependencies():
                self.logger.critical("Dependency check failed")
                return False
            
            self.logger.info("✓ Dependency check passed")
            
            # Step 3: Load configuration
            if not self.load_configuration():
                self.logger.critical("Configuration loading failed")
                return False
            
            self.logger.info("✓ Configuration loaded")
            
            # Step 4: Initialize database
            if not self.initialize_database():
                self.logger.critical("Database initialization failed")
                return False
            
            self.logger.info("✓ Database initialized")
            
            # Step 5: Verify models
            if not self.verify_models():
                self.logger.warning("Model verification completed with warnings")
            
            self.logger.info("✓ Model verification complete")
            
            # Step 6: Create PyQt5 app
            if not self.create_application():
                self.logger.critical("Application creation failed")
                return False
            
            self.logger.info("✓ PyQt5 application created")
            
            self.logger.info("\n" + "=" * 70)
            self.logger.info("INITIALIZATION SUCCESSFUL ✓")
            self.logger.info("=" * 70 + "\n")
            
            return True
        
        except Exception as e:
            self.logger.critical(f"Initialization failed: {e}")
            return False


def main():
    """
    Main application entry point
    
    Sequence:
    1. Initialize application components
    2. Create PyQt5 application
    3. Show login window
    4. Start event loop
    """
    
    try:
        # Initialize all components
        initializer = ApplicationInitializer()
        
        if not initializer.initialize_all():
            print("\n[FAIL] INITIALIZATION FAILED")
            print("Check data/logs/app.log for details")
            return 1
        
        # Create splash screen
        splash = initializer.create_splash_screen()
        
        try:
            # Create and show login window
            logger.info("Creating login window...")
            login_window = LoginWindow()
            login_window.show()
            
            logger.info("✓ Login window displayed")
            logger.info("=" * 70)
            logger.info("APPLICATION READY - WAITING FOR USER INPUT")
            logger.info("=" * 70)
            
            # Hide splash screen after a short delay
            if splash:
                QTimer.singleShot(2000, splash.close)
            
            # Start event loop
            return initializer.app.exec_()
        
        except Exception as e:
            logger.critical(f"Error showing login window: {e}")
            if splash:
                splash.close()
            return 1
    
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("Check data/logs/app.log for details")
        return 1


def show_help():
    """Show help information"""
    help_text = """
    AI Voice Desktop Control System - v1.0.0
    
    USAGE:
        python main.py              # Start application
        python main.py --help       # Show this help
        python main.py --setup      # Run setup wizard
        python main.py --models     # Download models
    
    KEYBOARD SHORTCUTS (in application):
        Ctrl+M      - Start recording
        Ctrl+N      - Stop recording
        Ctrl+L      - Clear history
        Ctrl+Q      - Quit application
    
    VOICE COMMANDS EXAMPLES:
        - "Open notepad"
        - "Search google for python"
        - "Create new file"
        - "Open chrome"
        - "Close application"
    
    TROUBLESHOOTING:
        1. Check data/logs/app.log for errors
        2. Verify internet connection (for model download)
        3. Ensure microphone is connected
        4. Check audio device settings
    
    For more information, visit documentation files.
    """
    print(help_text)


if __name__ == "__main__":
    
    # Check command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h', 'help']:
            show_help()
            sys.exit(0)
        
        elif arg in ['--setup']:
            logger.info("Running setup wizard...")
            try:
                from scripts.setup_environment import main as setup_main
                setup_main()
            except Exception as e:
                logger.error(f"Setup failed: {e}")
            sys.exit(0)
        
        elif arg in ['--models']:
            logger.info("Downloading models...")
            try:
                from scripts.download_models import main as download_main
                download_main()
            except Exception as e:
                logger.error(f"Model download failed: {e}")
            sys.exit(0)
        
        elif arg in ['--version', '-v']:
            print("AI Voice Desktop Control v1.0.0")
            sys.exit(0)
        
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information")
            sys.exit(1)
    
    # Normal startup
    exit_code = main()
    
    logger.info("=" * 70)
    logger.info("APPLICATION SHUTDOWN")
    logger.info("=" * 70)
    
    sys.exit(exit_code)