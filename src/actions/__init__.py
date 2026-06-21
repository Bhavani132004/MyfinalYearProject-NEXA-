"""Actions module - Desktop control and automation"""

from src.actions.command_executor import CommandExecutor
from src.actions.app_controller import ApplicationController
from src.actions.file_operations import FileOperations
from src.actions.system_controller import SystemController
from src.actions.action_mapper import ActionMapper
from src.actions.multitasking import MultitaskingManager
from src.actions.web_automation import WebAutomation

__all__ = [
    'CommandExecutor',
    'ApplicationController',
    'FileOperations',
    'SystemController',
    'ActionMapper',
    'MultitaskingManager',
    'WebAutomation'
]
