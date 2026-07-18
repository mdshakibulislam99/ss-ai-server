"""
Storage interface - Abstract base class for file storage
"""

from abc import ABC, abstractmethod


class Storage(ABC):
    """Abstract base class for file storage"""
    
    @abstractmethod
    async def save(self, path: str, data: bytes, content_type: str) -> str:
        """
        Save file
        
        Args:
            path: File path
            data: File data
            content_type: MIME type
            
        Returns:
            Public URL or path
        """
        pass
    
    @abstractmethod
    async def load(self, path: str) -> bytes:
        """Load file"""
        pass
    
    @abstractmethod
    async def delete(self, path: str) -> bool:
        """Delete file"""
        pass
    
    @abstractmethod
    async def exists(self, path: str) -> bool:
        """Check if file exists"""
        pass
    
    @abstractmethod
    async def get_url(self, path: str) -> str:
        """Get public URL for file"""
        pass