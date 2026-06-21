"""Backup user data script"""

import shutil
import os
from datetime import datetime

def backup_data():
    """Backup user data"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"backups/backup_{timestamp}"
        
        os.makedirs(backup_dir, exist_ok=True)
        
        shutil.copytree('data/user_profiles', f"{backup_dir}/user_profiles")
        shutil.copy('data/database/voice_control.db', f"{backup_dir}/voice_control.db")
        
        print(f"✓ Backup created: {backup_dir}")
        return True
    
    except Exception as e:
        print(f"✗ Backup failed: {e}")
        return False

if __name__ == "__main__":
    backup_data()