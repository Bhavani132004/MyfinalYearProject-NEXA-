"""Web automation and browser control"""

import webbrowser
import subprocess
import os
from src.core.logger import logger

class WebAutomation:
    """Handles web browsing automation"""
    
    BROWSER_PATHS = {
        'chrome': 'chrome.exe',
        'firefox': 'firefox.exe',
        'edge': 'msedge.exe',
        'safari': 'Safari'
    }
    
    def __init__(self):
        self.current_browser = None
        self.open_tabs = {}
    
    def open_browser(self, browser_name='chrome', url='https://www.google.com'):
        """Open browser with URL"""
        try:
            browser_name = browser_name.lower()
            logger.info(f"Opening {browser_name} with {url}")
            
            if browser_name == 'chrome':
                webbrowser.get('windows-default').open(url)
            elif browser_name == 'firefox':
                webbrowser.get('firefox').open(url)
            else:
                webbrowser.open(url)
            
            self.current_browser = browser_name
            logger.info(f"Browser opened: {browser_name}")
            return {"success": True, "message": f"Opened {browser_name}"}
        
        except Exception as e:
            logger.error(f"Error opening browser: {e}")
            return {"success": False, "message": str(e)}
    
    def search_google(self, query):
        """Search on Google"""
        try:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            logger.info(f"Google search: {query}")
            return {"success": True, "message": f"Searching for {query}"}
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {"success": False, "message": str(e)}
    
    def search_youtube(self, query):
        """Search on YouTube"""
        try:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            logger.info(f"YouTube search: {query}")
            return {"success": True, "message": f"Searching YouTube for {query}"}
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return {"success": False, "message": str(e)}

    def search_bing(self, query):
        """Search on Bing"""
        try:
            url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            logger.info(f"Bing search: {query}")
            return {"success": True, "message": f"Searching Bing for {query}"}
        except Exception as e:
            logger.error(f"Bing search error: {e}")
            return {"success": False, "message": str(e)}

    def search_wikipedia(self, query):
        """Search on Wikipedia"""
        try:
            url = f"https://en.wikipedia.org/wiki/Special:Search?search={query.replace(' ', '+')}"
            webbrowser.open(url)
            logger.info(f"Wikipedia search: {query}")
            return {"success": True, "message": f"Searching Wikipedia for {query}"}
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return {"success": False, "message": str(e)}

    def search_amazon(self, query):
        """Search on Amazon"""
        try:
            url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
            webbrowser.open(url)
            logger.info(f"Amazon search: {query}")
            return {"success": True, "message": f"Searching Amazon for {query}"}
        except Exception as e:
            logger.error(f"Amazon search error: {e}")
            return {"success": False, "message": str(e)}
    
    def open_website(self, website):
        """Open specific website"""
        try:
            if not website.startswith('http'):
                website = f"https://{website}"
            
            webbrowser.open(website)
            logger.info(f"Website opened: {website}")
            return {"success": True, "message": f"Opened {website}"}
        except Exception as e:
            logger.error(f"Website open error: {e}")
            return {"success": False, "message": str(e)}
    
    def close_browser(self):
        """Close current browser"""
        try:
            if self.current_browser:
                os.system(f"taskkill /IM {self.BROWSER_PATHS.get(self.current_browser, 'chrome.exe')} /F")
                self.current_browser = None
                logger.info("Browser closed")
                return {"success": True, "message": "Browser closed"}
            return {"success": False, "message": "No browser open"}
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
            return {"success": False, "message": str(e)}
    
    def new_tab(self, url='https://www.google.com'):
        """Open new tab"""
        try:
            webbrowser.open_new_tab(url)
            logger.info(f"New tab opened: {url}")
            return {"success": True, "message": "New tab opened"}
        except Exception as e:
            logger.error(f"Error opening new tab: {e}")
            return {"success": False, "message": str(e)}