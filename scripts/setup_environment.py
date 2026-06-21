"""Setup environment script"""

import os
import sys
import subprocess

def create_directories():
    """Create required directories"""
    directories = [
        'data/database',
        'data/models/whisper',
        'data/models/wav2vec2',
        'data/models/bert_intent',
        'data/models/voice_auth',
        'data/user_profiles/user_template',
        'data/logs',
        'resources/icons',
        'resources/sounds',
        'resources/configs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created: {directory}")

def setup_environment_variables():
    """Setup .env file"""
    if not os.path.exists('.env'):
        with open('.env.example', 'r') as f:
            content = f.read()
        with open('.env', 'w') as f:
            f.write(content)
        print("✓ Created .env file")

def install_dependencies():
    """Install dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    print("✓ Dependencies installed")

def main():
    """Main setup"""
    print("=" * 50)
    print("AI Voice Desktop Control - Setup")
    print("=" * 50)
    
    try:
        print("\n[1/3] Creating directories...")
        create_directories()
        
        print("\n[2/3] Setting up environment...")
        setup_environment_variables()
        
        print("\n[3/3] Installing dependencies...")
        install_dependencies()
        
        print("\n" + "=" * 50)
        print("✓ Setup completed!")
        print("Run: python main.py")
        print("=" * 50)
    
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()