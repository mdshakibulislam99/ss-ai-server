"""
Cache interface - Abstract base class for caching
"""

from abc import ABC, abstractmethod
from typing import Dict,  Generic, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Cache(ABC, Generic[K, V]):
    """Abstract base class for caching"""
    
    @abstractmethod
    async def get(self, key: K) -> Optional[V]:
        """Get value by key"""
        pass
    
    @abstractmethod
    async def set(self, key: K, value: V, ttl: Optional[int] = None) -> None:
        """Set value with optional TTL (seconds)"""
        pass
    
    @abstractmethod
    async def delete(self, key: K) -> bool:
        """Delete value by key"""
        pass
    
    @abstractmethod
    async def exists(self, key: K) -> bool:
        """Check if key exists"""
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """Clear all values"""
        pass
    
    @abstractmethod
    async def get_many(self, keys: List[K]) -> Dict[K, V]:
        """Get multiple values"""
        pass
    
    @abstractmethod
    async def set_many(self, mapping: Dict[K, V], ttl: Optional[int] = None) -> None:
        """Set multiple values"""
        pass