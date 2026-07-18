"""
Repository interface - Abstract base class for repositories
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Generic repository interface"""
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[T]:
        """Get all entities"""
        pass
    
    @abstractmethod
    async def add(self, entity: T) -> T:
        """Add new entity"""
        pass
    
    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update existing entity"""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete entity by ID"""
        pass
    
    @abstractmethod
    async def exists(self, id: str) -> bool:
        """Check if entity exists"""
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """Count entities"""
        pass