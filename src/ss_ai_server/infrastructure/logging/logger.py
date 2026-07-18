"""
Logger - Logging implementation
"""

import logging

from ...domain.interfaces.logger import Logger


class LoggerImpl(Logger):
    """Logging implementation"""
    
    def __init__(self, name: str = "ss_ai_server", level: str = "INFO"):
        """
        Initialize logger
        
        Args:
            name: Logger name
            level: Log level
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, level.upper()))
        
        # Add console handler if not already added
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message"""
        self._logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message"""
        self._logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message"""
        self._logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message"""
        self._logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message"""
        self._logger.critical(message, extra=kwargs)