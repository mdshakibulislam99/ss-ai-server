"""
Memory Cache - In-memory cache implementation
"""

from typing import Any,  Dict,  Optional

from ...domain.interfaces.cache import Cache  # noqa: F401


class MemoryCache(Cache):
    """In-memory cache implementation"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300) -> None:
        """
        Initialize memory cache
        
        Args:
            max_size: Maximum number of items in cache
            default_ttl: Default TTL in seconds
        """
        self._cache = {}
        self._max_size = max_size
        self._default_ttl = default_ttl
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value by key"""
        if key not in self._cache:
            return None
        
        value, expiry = self._cache[key]
        
        # Check if expired
        import time
        if expiry and time.time() > expiry:
            del self._cache[key]
            return None
        
        return value
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value with optional TTL"""
        import time
        
        # Evict oldest if at capacity
        if len(self._cache) >= self._max_size and key not in self._cache:
            # Remove oldest entry
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        # Set expiry
        if ttl is not None:
            expiry = time.time() + ttl
        elif self._default_ttl > 0:
            expiry = time.time() + self._default_ttl
        else:
            expiry = None
        
        self._cache[key] = (value, expiry)
    
    async def delete(self, key: str) -> bool:
        """Delete value by key"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return key in self._cache
    
    async def clear(self) -> None:
        """Clear all values"""
        self._cache.clear()
    
    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values"""
        result = {}
        for key in keys:
            value = await self.get(key)
            if value is not None:
                result[key] = value
        return result
    
    async def set_many(self, mapping: Dict[str, Any], ttl: Optional[int] = None) -> None:
        """Set multiple values"""
        for key, value in mapping.items():
            await self.set(key, value, ttl)