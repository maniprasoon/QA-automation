import logging
import os
from datetime import datetime
from pathlib import Path
from utilities.config import Config

class TestLogger:
    """Custom logger for test execution tracking"""
    
    def __init__(self, test_name=""):
        self.test_name = test_name
        self.logger = logging.getLogger(test_name)
        self.setup_logger()
    
    def setup_logger(self):
        """Configure logger with handlers"""
        # Create unique log file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = Config.LOGS_DIR / f"test_execution_{timestamp}.log"
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Set logging level
        self.logger.setLevel(logging.DEBUG)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_info(self, message):
        """Log informational messages"""
        self.logger.info(f"[{self.test_name}] {message}")
    
    def log_error(self, message):
        """Log error messages"""
        self.logger.error(f"[{self.test_name}] {message}")
    
    def log_debug(self, message):
        """Log debug messages"""
        self.logger.debug(f"[{self.test_name}] {message}")
    
    def log_test_start(self):
        """Log test start information"""
        self.logger.info("=" * 50)
        self.logger.info(f"Starting Test: {self.test_name}")
        self.logger.info("=" * 50)
    
    def log_test_end(self, status="PASSED"):
        """Log test end information"""
        self.logger.info("=" * 50)
        self.logger.info(f"Test {self.test_name} {status}")
        self.logger.info("=" * 50)

# Global logger instance
def get_logger(test_name=""):
    return TestLogger(test_name)