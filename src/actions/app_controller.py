"""Application control"""

import subprocess
import platform
import shutil
import os
from src.core.logger import logger

class ApplicationController:
    """Controls application execution"""
    
    APP_PATHS = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'calc': 'calc.exe',
        'chrome': 'chrome.exe',
        'google chrome': 'chrome.exe',
        'firefox': 'firefox.exe',
        'word': 'winword.exe',
        'ms word': 'winword.exe',
        'microsoft word': 'winword.exe',
        'msword': 'winword.exe',
        'excel': 'excel.exe',
        'ms excel': 'excel.exe',
        'microsoft excel': 'excel.exe',
        'powerpoint': 'powerpnt.exe',
        'ppt': 'powerpnt.exe',
        'pptx': 'powerpnt.exe',
        'pnt': 'powerpnt.exe',
        'microsoft powerpoint': 'powerpnt.exe',
        'outlook': 'outlook.exe',
        'teams': 'teams.exe',
        'microsoft teams': 'teams.exe',
        'mspaint': 'mspaint.exe',
        'paint': 'mspaint.exe',
        'vlc': 'vlc.exe',
        'spotify': 'spotify.exe',
        'discord': 'discord.exe',
        'slack': 'slack.exe',
        'zoom': 'zoom.exe',
        'terminal': 'cmd.exe',
        'cmd': 'cmd.exe',
        'command prompt': 'cmd.exe',
        'powershell': 'powershell.exe',
        'explorer': 'explorer.exe',
        'file explorer': 'explorer.exe',
        'my computer': 'explorer.exe',
        'this pc': 'explorer.exe',
        'onedrive': 'OneDrive.exe',
        'control panel': 'control',
        'settings': 'start ms-settings:',
        'browser': 'https://www.google.com',
        'store': 'start ms-windows-store:',
        'microsoft store': 'start ms-windows-store:',
        'photos': 'start ms-photos:',
        'camera': 'start microsoft.windows.camera:',
        'calendar': 'start outlookcal:',
        'weather': 'start bingweather:',
        'news': 'start bingnews:',
        'mail': 'start outlookmail:',
        'gmail': 'https://mail.google.com',
        'whatsapp': 'start whatsapp:',
        'maps': 'start bingmaps:',
        'linkedin': 'https://www.linkedin.com',
        'youtube': 'https://www.youtube.com',
        'sublime text': 'subl.exe',
        'task manager': 'taskmgr.exe',
        'tax manager': 'taskmgr.exe',
        'taskmgr': 'taskmgr.exe'
    }
    
    def __init__(self):
        self.open_apps = {}
    
    def open_application(self, app_name, preferences=None):
        """Open application with enhanced reliability and fallbacks"""
        try:
            app_name = app_name.lower().strip()
            
            # Check for aliases in personalization
            if preferences and 'aliases' in preferences:
                original = app_name
                app_name = preferences['aliases'].get(app_name, app_name)
                if original != app_name:
                    logger.info(f"Alias resolved: '{original}' -> '{app_name}'")
            
            logger.info(f"Attempting to open application: {app_name}")
            
            # Check for URI schemes first
            exe_or_uri = self.APP_PATHS.get(app_name, app_name)
            
            # 1. Handle URI schemes and shell start commands
            if exe_or_uri.startswith('start ') or exe_or_uri.startswith('http') or exe_or_uri.startswith('ms-') or any(s in exe_or_uri for s in [':', '//']):
                cmd = exe_or_uri if exe_or_uri.startswith('start') else f'start {exe_or_uri}'
                logger.info(f"Launching via shell: {cmd}")
                os.system(cmd)
                self.open_apps[app_name] = True
                return

            # 2. Try to find the full path or start as process
            full_path = shutil.which(exe_or_uri)
            if not full_path and not exe_or_uri.lower().endswith('.exe'):
                full_path = shutil.which(exe_or_uri + '.exe')
            
            if full_path:
                logger.info(f"Found path: {full_path}")
                subprocess.Popen(f'"{full_path}"', shell=True)
                self.open_apps[app_name] = True
                return

            # 3. Fallback: Try to start as a file if it looks like one
            if '.' in app_name:
                logger.info(f"App name '{app_name}' looks like a file, trying to open directly...")
                try:
                    os.startfile(app_name)
                    self.open_apps[app_name] = True
                    return
                except:
                    pass

            # 4. Final Fallback: try shell 'start'
            target = exe_or_uri if exe_or_uri.lower().endswith('.exe') else exe_or_uri + '.exe'
            logger.info(f"Trying final shell start: {target}")
            subprocess.Popen(f'start {target}', shell=True)
            self.open_apps[app_name] = True
        
        except Exception as e:
            logger.error(f"Error opening '{app_name}': {e}")
            raise
    
    def close_application(self, app_name, preferences=None):
        """Close application with enhanced UWP support"""
        try:
            app_name = app_name.lower().strip()
            
            if preferences and 'aliases' in preferences:
                original = app_name
                app_name = preferences['aliases'].get(app_name, app_name)
                if original != app_name:
                    logger.info(f"Alias resolved: '{original}' -> '{app_name}'")
            
            logger.info(f"Attempting to close application: {app_name}")
            
            # Map friendly names to actual process names (including UWP)
            # Add UWP app mappings here
            uwp_mappings = {
                'calculator': 'CalculatorApp.exe',
                'calc': 'CalculatorApp.exe',
                'calendar': 'HxCalendarAppImm.exe',
                'outlook calendar': 'HxCalendarAppImm.exe',
                'photos': 'Microsoft.Photos.exe',
                'movies & tv': 'Video.UI.exe',
                'groove music': 'Music.UI.exe',
                'settings': 'SystemSettings.exe',
                'store': 'WinStore.App.exe',
                'weather': 'Microsoft.Msn.Weather.exe',
                'news': 'Microsoft.Msn.News.exe',
                'mail': 'HxOutlook.exe', # Often bundled with Calendar
            }
            
            # Check UWP first
            exe_name = uwp_mappings.get(app_name)
            
            # Special handling for OneDrive (it's often in a specific user path)
            if app_name == 'onedrive':
                local_app_data = os.environ.get('LOCALAPPDATA', '')
                program_files = os.environ.get('ProgramFiles', '')
                paths_to_check = [
                    os.path.join(local_app_data, r'Microsoft\OneDrive\OneDrive.exe'),
                    os.path.join(program_files, r'Microsoft OneDrive\OneDrive.exe'),
                    r'C:\Program Files\Microsoft OneDrive\OneDrive.exe'
                ]
                for p in paths_to_check:
                    if os.path.exists(p):
                        exe_name = p
                        break
            
            if not exe_name:
                exe_name = self.APP_PATHS.get(app_name, app_name)
            
            # Special case: Browser mapping is often a URL
            if exe_name.startswith('http') or app_name == 'browser':
                browsers = ['chrome.exe', 'msedge.exe', 'firefox.exe', 'browser.exe']
                for b in browsers:
                    os.system(f'taskkill /F /IM {b} /T >nul 2>&1')
                return {"success": True, "message": "Closed browser processes"}

            # Prepare process name candidates
            candidates = []
            if exe_name:
                candidates.append(exe_name)
                if not exe_name.lower().endswith('.exe'):
                    candidates.append(exe_name + '.exe')
            
            # Also try the raw name
            if app_name not in candidates:
                candidates.append(app_name)
                candidates.append(app_name + '.exe')

            if platform.system() == 'Windows':
                success_count = 0
                for proc in candidates:
                    # Clean up 'start ' commands from mappings
                    proc = proc.replace('start ', '').replace('ms-settings:', '')
                    if not proc: continue
                    
                    logger.info(f"Trying taskkill on: {proc}")
                    result = os.system(f'taskkill /F /IM {proc} /T >nul 2>&1')
                    if result == 0:
                        success_count += 1
                
                if success_count > 0:
                     if app_name in self.open_apps:
                            del self.open_apps[app_name]
                     return {"success": True, "message": f"Closed {app_name}"}
                
                return {"success": False, "message": f"Could not find or close {app_name}. Is it running?"}
            else:
                return {"success": True, "message": f"Close command sent for {app_name}"}
        
        except Exception as e:
            logger.error(f"Error closing '{app_name}': {e}")
            raise
    
    def list_open_applications(self):
        """List open applications"""
        return list(self.open_apps.keys())