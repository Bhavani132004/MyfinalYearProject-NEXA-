import os
import subprocess
import sys

def build():
    print("Starting NEXA EXE Build Process...")
    
    # Check for pyinstaller
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Define paths
    base_path = os.path.abspath(".")
    main_script = os.path.join(base_path, "main.py")
    
    # Run PyInstaller
    # --onefile: Create a single executable
    # --windowed: No console window
    # --add-data: Include styles and other assets
    # Note: syntax for add-data is 'source;destination' on Windows
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "NEXA",
        f"--add-data={os.path.join('src', 'gui', 'styles')};src/gui/styles",
        "--hidden-import=PyQt5.sip",
        "--hidden-import=speech_recognition",
        "--hidden-import=pyaudio",
        main_script
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd)
    
    print("\nBuild Complete! Check the 'dist' folder for NEXA.exe")

if __name__ == "__main__":
    build()