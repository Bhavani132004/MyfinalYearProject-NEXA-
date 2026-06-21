"""Multitasking support"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from src.core.logger import logger

class MultitaskingManager:
    """Manages parallel command execution"""
    
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_tasks = {}
    
    def execute_parallel(self, commands, executor_func):
        """Execute multiple commands in parallel"""
        try:
            futures = {}
            
            for cmd_id, command in enumerate(commands):
                future = self.executor.submit(executor_func, command)
                futures[future] = cmd_id
                self.active_tasks[cmd_id] = future
            
            results = {}
            for future in as_completed(futures):
                cmd_id = futures[future]
                try:
                    results[cmd_id] = future.result()
                except Exception as e:
                    logger.error(f"Task {cmd_id} failed: {e}")
                    results[cmd_id] = {"success": False, "error": str(e)}
                finally:
                    del self.active_tasks[cmd_id]
            
            return results
        
        except Exception as e:
            logger.error(f"Parallel execution error: {e}")
            raise
    
    def cancel_task(self, task_id):
        """Cancel a running task"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id].cancel()
            del self.active_tasks[task_id]
    
    def get_active_tasks(self):
        """Get list of active tasks"""
        return list(self.active_tasks.keys())