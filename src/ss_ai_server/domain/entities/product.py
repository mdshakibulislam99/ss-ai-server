"""
Product entity - Represents a product in the system
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class Product:
    """Product entity"""
    
    product_id: str
    site_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    image_urls: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    embedding_id: Optional[str] = None
    indexed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.image_urls is None:
            self.image_urls = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.updated_at is None:
            self.updated_at = datetime.now(timezone.utc)
    
    def update(self, **kwargs: Any) -> "Product":
        """Update product fields"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        return self
    
    def is_indexed(self) -> bool:
        """Check if product is indexed"""
        return self.indexed_at is not None
    
    def has_images(self) -> bool:
        """Check if product has images"""
        return self.image_urls is not None and len(self.image_urls) > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "product_id": self.product_id,
            "site_id": self.site_id,
            "title": self.title,
            "description": self.description,
            "image_urls": self.image_urls,
            "metadata": self.metadata,
            "embedding_id": self.embedding_id,
            "indexed_at": self.indexed_at.isoformat() if self.indexed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """Create from dictionary"""
        # Parse datetime fields
        for field in ["indexed_at", "created_at", "updated_at"]:
            if field in data and data[field]:
                data[field] = datetime.fromisoformat(data[field])
        
        return cls(**data)