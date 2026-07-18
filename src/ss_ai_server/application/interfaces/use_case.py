"""
UseCase interface - Base interface for all use cases
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class UseCase(ABC, Generic[T, R]):
    """Base interface for use cases"""
    
    @abstractmethod
    async def execute(self, request: T) -> R:
        """
        Execute use case
        
        Args:
            request: Use case request
            
        Returns:
            Use case response
        """
        pass