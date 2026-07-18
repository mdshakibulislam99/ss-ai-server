"""
Local Storage - Local filesystem storage implementation
"""

import os
from typing import Optional

from ...domain.interfaces.storage import Storage


class LocalStorage(Storage):
    """Local filesystem storage implementation"""
    
    def __init__(self, base_path: str = "/data/storage"):
        """
        Initialize local storage
        
        Args:
            base_path: Base directory for storage
        """
        self._base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    async def save(self, path: str, data: bytes, content_type: str) -> str:
        """
        Save file
        
        Args:
            path: File path
            data: File data
            content_type: MIME type
            
        Returns:
            File path
        """
        full_path = os.path.join(self._base_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'wb') as f:
            f.write(data)
        
        return full_path
    
    async def load(self, path: str) -> bytes:
        """Load file"""
        full_path = os.path.join(self._base_path, path)
        with open(full_path, 'rb') as f:
            return f.read()
    
    async def delete(self, path: str) -> bool:
        """Delete file"""
        full_path = os.path.join(self._base_path, path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    
    async def exists(self, path: str) -> bool:
        """Check if file exists"""
        full_path = os.path.join(self._base_path, path)
        return os.path.exists(full_path)
    
    async def get_url(self, path: str) -> str:
        """Get public URL for file"""
        return f"file://{os.path.join(self._base_path, path)}"