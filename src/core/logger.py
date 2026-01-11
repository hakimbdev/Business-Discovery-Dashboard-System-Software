"""
Logging Configuration
Centralized logging setup for the entire system
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


class SystemLogger:
    """Centralized logging system"""
    
    def __init__(self, log_file: str = "logs/system.log", 
                 level: str = "INFO",
                 max_size_mb: int = 10,
                 backup_count: int = 5,
                 console_output: bool = True):
        
        self.log_file = log_file
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.backup_count = backup_count
        self.console_output = console_output
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging handlers and formatters"""
        # Ensure log directory exists
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.level)
        
        # Remove existing handlers
        root_logger.handlers = []
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=self.max_size_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(self.level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # Console handler
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a logger instance for a specific module"""
        return logging.getLogger(name)


def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a logger"""
    return logging.getLogger(name)

