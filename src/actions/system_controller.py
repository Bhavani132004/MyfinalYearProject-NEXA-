"""System control operations"""

import subprocess
import os
from src.core.logger import logger

class SystemController:
    """Controls system operations"""
    
    def shutdown(self, delay=0):
        """Shutdown system"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['shutdown', '/s', '/t', str(delay)])
            else:  # Linux/Mac
                subprocess.run(['shutdown', '-h', str(delay)])
            logger.info("System shutdown initiated")
        except Exception as e:
            logger.error(f"Error shutting down: {e}")
            raise
    
    def restart(self, delay=0):
        """Restart system"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['shutdown', '/r', '/t', str(delay)])
            else:  # Linux/Mac
                subprocess.run(['shutdown', '-r', str(delay)])
            logger.info("System restart initiated")
        except Exception as e:
            logger.error(f"Error restarting: {e}")
            raise
    
    def sleep(self):
        """Put system to sleep"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0', '1', '0'])
            logger.info("System sleep initiated")
        except Exception as e:
            logger.error(f"Error sleeping: {e}")
            raise

    def hibernate(self):
        """Put system to hibernate"""
        try:
            if os.name == 'nt':
                subprocess.run(['shutdown', '/h'])
            logger.info("System hibernation initiated")
        except Exception as e:
            logger.error(f"Error hibernating: {e}")
            raise
    
    def logout(self):
        """Log out current user"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['shutdown', '/l'])
            logger.info("System logout initiated")
        except Exception as e:
            logger.error(f"Error logging out: {e}")
            raise
    
    def lock_screen(self):
        """Lock screen"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
            logger.info("Screen locked")
        except Exception as e:
            logger.error(f"Error locking screen: {e}")
            raise

    def volume_up(self):
        """Increase system volume"""
        try:
            import pyautogui
            pyautogui.press('volumeup')
            logger.info("Volume increased")
        except Exception as e:
            logger.error(f"Error increasing volume: {e}")

    def volume_down(self):
        """Decrease system volume"""
        try:
            import pyautogui
            pyautogui.press('volumedown')
            logger.info("Volume decreased")
        except Exception as e:
            logger.error(f"Error decreasing volume: {e}")

    def mute(self):
        """Mute/Unmute system volume"""
        try:
            import pyautogui
            pyautogui.press('volumemute')
            logger.info("Volume muted/unmuted")
        except Exception as e:
            logger.error(f"Error muting volume: {e}")

    def play_pause_media(self):
        """Play or pause media"""
        try:
            import pyautogui
            pyautogui.press('playpause')
            logger.info("Media play/pause toggled")
        except Exception as e:
            logger.error(f"Error toggling media: {e}")

    def next_track(self):
        """Skip to next track"""
        try:
            import pyautogui
            pyautogui.press('nexttrack')
            logger.info("Skipped to next track")
        except Exception as e:
            logger.error(f"Error skipping track: {e}")

    def prev_track(self):
        """Go to previous track"""
        try:
            import pyautogui
            pyautogui.press('prevtrack')
            logger.info("Went to previous track")
        except Exception as e:
            logger.error(f"Error going to previous track: {e}")
            
    def get_battery_status(self):
        """Get battery percentage and status (Windows)"""
        try:
            if os.name == 'nt':
                # Use WMIC to get battery info
                output = subprocess.check_output('wmic path Win32_Battery get EstimatedChargeRemaining,BatteryStatus /value', shell=True).decode()
                info = {}
                for line in output.splitlines():
                    if '=' in line:
                        k, v = line.split('=', 1)
                        info[k.strip()] = v.strip()
                
                percentage = info.get('EstimatedChargeRemaining', 'Unknown')
                status_code = info.get('BatteryStatus', '2') # 2 means Discharging/OK
                status = "Charging" if status_code == '1' else "Discharging"
                
                return f"Battery is at {percentage}% and currently {status}."
            return "Battery status is only supported on Windows currently."
        except Exception as e:
            logger.error(f"Error getting battery status: {e}")
            return "Could not retrieve battery status."

    def set_brightness(self, level):
        """Set screen brightness (Windows)"""
        try:
            if os.name == 'nt':
                # Use PowerShell to set brightness
                cmd = f"powershell -Command \"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {level})\""
                subprocess.run(cmd, shell=True)
                logger.info(f"Brightness set to {level}%")
                return True
            return False
        except Exception as e:
            logger.error(f"Error setting brightness: {e}")
            return False
    
    def get_system_info(self):
        """Get system information"""
        try:
            import platform
            return {
                'system': platform.system(),
                'release': platform.release(),
                'processor': platform.processor(),
                'python_version': platform.python_version()
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            raise

    def get_time_date(self):
        """Get current time and date"""
        try:
            from datetime import datetime
            now = datetime.now()
            return {
                'time': now.strftime("%I:%M %p"),
                'date': now.strftime("%A, %B %d, %Y")
            }
        except Exception as e:
            logger.error(f"Error getting time/date: {e}")
            return None