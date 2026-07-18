"""
Base Repository - Base implementation for repositories
"""

from typing import Generic, List, Optional, TypeVar

from ...domain.interfaces.repository import Repository

T = TypeVar("T")


class BaseRepository(Repository[T], Generic[T]):
    """Base implementation for repositories"""
    
    def __init__(self):
        """Initialize base repository"""
        self._entities = {}
    
    async def get_by_id(self, id: str) -> Optional[T]:
        """Get entity by ID"""
        return self._entities.get(id)
    
    async def get_all(self) -> List[T]:
        """Get all entities"""
        return list(self._entities.values())
    
    async def add(self, entity: T) -> T:
        """Add new entity"""
        entity_id = getattr(entity, 'product_id', None) or getattr(entity, 'key_id', None)
        if entity_id:
            self._entities[entity_id] = entity
        return entity
    
    async def update(self, entity: T) -> T:
        """Update existing entity"""
        entity_id = getattr(entity, 'product_id', None) or getattr(entity, 'key_id', None)
        if entity_id and entity_id in self._entities:
            self._entities[entity_id] = entity
        return entity
    
    async def delete(self, id: str) -> bool:
        """Delete entity by ID"""
        if id in self._entities:
            del self._entities[id]
            return True
        return False
    
    async def exists(self, id: str) -> bool:
        """Check if entity exists"""
        return id in self._entities
    
    async def count(self) -> int:
        """Count entities"""
        return len(self._entities)