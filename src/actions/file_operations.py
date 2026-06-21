"""File operation handler"""

import os
import shutil
from src.core.logger import logger

class FileOperations:
    """Handles file operations"""
    
    def open_file(self, file_path):
        """Open file"""
        try:
            if os.path.exists(file_path):
                os.startfile(file_path)
                logger.info(f"File opened: {file_path}")
            else:
                raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error opening file: {e}")
            raise
    
    def create_file(self, file_path, content=""):
        """Create file"""
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            logger.info(f"File created: {file_path}")
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            raise
    
    def delete_file(self, file_path):
        """Delete file or directory"""
        try:
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    logger.info(f"Directory deleted: {file_path}")
                else:
                    os.remove(file_path)
                    logger.info(f"File deleted: {file_path}")
            else:
                raise FileNotFoundError(f"Path not found: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting: {e}")
            raise
    
    def copy_file(self, source, destination):
        """Copy file"""
        try:
            shutil.copy(source, destination)
            logger.info(f"File copied: {source} -> {destination}")
        except Exception as e:
            logger.error(f"Error copying file: {e}")
            raise
    
    def move_file(self, source, destination):
        """Move file"""
        try:
            shutil.move(source, destination)
            logger.info(f"File moved: {source} -> {destination}")
        except Exception as e:
            logger.error(f"Error moving file: {e}")
            raise
    
    def create_directory(self, dir_path):
        """Create a new directory"""
        try:
            expanded_path = os.path.expanduser(os.path.expandvars(dir_path))
            if not os.path.exists(expanded_path):
                os.makedirs(expanded_path)
                logger.info(f"Directory created: {expanded_path}")
                return True
            else:
                logger.warning(f"Directory already exists: {expanded_path}")
                return False
        except Exception as e:
            logger.error(f"Error creating directory: {e}")
            raise

    def list_directory(self, directory=None):
        """List directory contents"""
        try:
            if not directory:
                directory = os.path.expanduser('~')
            
            expanded_dir = os.path.expanduser(os.path.expandvars(directory))
            if os.path.exists(expanded_dir):
                items = os.listdir(expanded_dir)
                logger.info(f"Listed directory: {expanded_dir} ({len(items)} items)")
                return items
            return []
        except Exception as e:
            logger.error(f"Error listing directory: {e}")
            raise

    def search_files(self, filename, search_path=None):
        """Search for files by name with expanded scope and category awareness"""
        try:
            results = []
            filename_lower = filename.lower().strip()
            
            # Category search logic
            categories = {
                'pictures': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
                'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
                'music': ['.mp3', '.wav', '.flac', '.m4a', '.wma'],
                'audio': ['.mp3', '.wav', '.flac', '.m4a', '.wma'],
                'pdf': ['.pdf'],
                'documents': ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.txt'],
                'scripts': ['.py', '.js', '.sh', '.bat', '.ps1', '.php', '.cpp', '.h'],
                'data': ['.csv', '.json', '.xml', '.sql', '.db']
            }
            
            search_extensions = categories.get(filename_lower)
            if search_extensions:
                logger.info(f"Category search detected for '{filename_lower}'. Searching extensions: {search_extensions}")
            
            if not search_path:
                # Expanded search paths
                search_paths = [
                    self.get_well_known_path('desktop'),
                    self.get_well_known_path('documents'),
                    self.get_well_known_path('downloads'),
                    self.get_well_known_path('pictures'),
                    self.get_well_known_path('music'),
                    self.get_well_known_path('videos'),
                ]
                
                # Add D: drive if it exists
                if os.path.exists("D:\\"):
                    search_paths.append("D:\\")
            else:
                search_paths = [search_path]
            
            logger.info(f"Searching for '{filename}' in {len(search_paths)} locations...")
            
            count = 0
            limit = 15
            
            for path in search_paths:
                if not path or not os.path.exists(path):
                    continue
                    
                # Use os.walk with error handling
                for root, dirs, files in os.walk(path, topdown=True):
                    # Skip system/hidden folders to speed up
                    dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('$') and d != 'AppData' and 'node_modules' not in d]
                    
                    try:
                        # Check files
                        for file in files:
                            match_found = False
                            
                            if search_extensions:
                                # Category match: check extension
                                if any(file.lower().endswith(ext) for ext in search_extensions):
                                    match_found = True
                            else:
                                # Standard name match
                                if filename_lower in file.lower():
                                    match_found = True
                            
                            if match_found:
                                full_path = os.path.join(root, file)
                                results.append(full_path)
                                count += 1
                                if count >= limit: return results
                        
                        # Check directories (only if not a category extension search)
                        if not search_extensions:
                            for d in dirs:
                                if filename_lower in d.lower():
                                    full_path = os.path.join(root, d)
                                    results.append(full_path)
                                    count += 1
                                    if count >= limit: return results
                                
                    except OSError:
                        pass # Skip inaccessible files/folders
                            
            return results
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return []

    def get_well_known_path(self, folder_name):
        """Resolve common folder names to absolute paths (Windows)"""
        try:
            user_profile = os.environ.get('USERPROFILE', '')
            folders = {
                'desktop': os.path.join(user_profile, 'Desktop'),
                'documents': os.path.join(user_profile, 'Documents'),
                'my documents': os.path.join(user_profile, 'Documents'),
                'downloads': os.path.join(user_profile, 'Downloads'),
                'pictures': os.path.join(user_profile, 'Pictures'),
                'music': os.path.join(user_profile, 'Music'),
                'videos': os.path.join(user_profile, 'Videos'),
                'home': user_profile
            }
            return folders.get(folder_name.lower())
        except Exception as e:
            logger.error(f"Error resolving path '{folder_name}': {e}")
            return None

    def rename_file(self, old_path, new_name):
        """Rename file or directory"""
        try:
            if not os.path.exists(old_path):
                raise FileNotFoundError(f"Source path not found: {old_path}")
            
            directory = os.path.dirname(old_path)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            logger.info(f"Renamed: {old_path} -> {new_path}")
            return True
        except Exception as e:
            logger.error(f"Error renaming: {e}")
            raise
