# logger/filters.py
import logging
import os
import yaml
from pathlib import Path

class SensitiveDataFilter(logging.Filter):
    """
    Filter to remove sensitive data from logs
    """
    
    def __init__(self):
        super().__init__()
        self.sensitive_keywords = [
            'password', 'pwd', 'secret', 'token', 'key', 'auth',
            'credential', 'session', 'cookie', 'authorization'
        ]
    
    def filter(self, record):
        # Convert log message to string
        message = str(record.getMessage())
        
        # Check if message contains sensitive data
        for keyword in self.sensitive_keywords:
            if keyword.lower() in message.lower():
                # Replace sensitive data with asterisks
                record.msg = message.replace(
                    message[message.lower().find(keyword.lower()):],
                    '***REDACTED***'
                )
                break
        
        return True

class DatabaseFilter(logging.Filter):
    """
    Filter for database-related logs
    """
    
    def filter(self, record):
        # Only allow database-related logs
        return any(keyword in record.name.lower() for keyword in ['db', 'database', 'sqlalchemy', 'crud'])

def setup_logging():
    """
    Setup logging configuration
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # Load logging configuration
    config_path = Path(__file__).parent / 'logging_config.yaml'
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        logging.config.dictConfig(config)
        
        # Add custom filters
        logger = logging.getLogger('m2dsia')
        logger.addFilter(SensitiveDataFilter())
        
        return logger
    
    except Exception as e:
        # Fallback to basic logging if configuration fails
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger('m2dsia')
        logger.warning(f"Failed to load logging configuration: {e}")
        return logger

def get_logger(name: str):
    """
    Get logger instance
    """
    return logging.getLogger(f'm2dsia.{name}')