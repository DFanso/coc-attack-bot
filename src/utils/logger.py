"""
Logger - Logging utility for the COC Attack Bot
"""

import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    """Simple logging utility for the COC Attack Bot"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_dir = "logs"
        
        # Create logs directory
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Set default log file if not provided
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d")
            log_file = f"coc_bot_{timestamp}.log"
        
        self.log_file = os.path.join(self.log_dir, log_file)
        
        # Configure logging
        self._setup_logging()
        
        self.info("Logger initialized")
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create logger
        self.logger = logging.getLogger('COCBot')
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log critical message"""
        self.logger.critical(message)
    
    def log_action(self, action: str, details: str = "") -> None:
        """Log bot action"""
        message = f"BOT ACTION: {action}"
        if details:
            message += f" - {details}"
        self.info(message)
    
    def log_recording(self, session_name: str, action_count: int, duration: float) -> None:
        """Log recording completion"""
        self.info(f"RECORDING COMPLETE: {session_name} - {action_count} actions, {duration:.1f}s")
    
    def log_playback(self, session_name: str, status: str) -> None:
        """Log playback status"""
        self.info(f"PLAYBACK {status.upper()}: {session_name}")
    
    def log_coordinate_mapping(self, name: str, x: int, y: int) -> None:
        """Log coordinate mapping"""
        self.info(f"COORDINATE MAPPED: {name} at ({x}, {y})")
    
    def get_log_file_path(self) -> str:
        """Get the current log file path"""
        return self.log_file 