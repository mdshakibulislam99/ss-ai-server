"""
Logger interface - Abstract base class for logging
"""

from abc import ABC, abstractmethod


class Logger(ABC):
    """Abstract base class for logging"""
    
    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message"""
        pass
    
    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message"""
        pass
    
    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message"""
        pass
    
    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message"""
        pass
    
    @abstractmethod
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message"""
        pass