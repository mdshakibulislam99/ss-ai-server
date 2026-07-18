"""
Embedding entity - Represents a vector embedding
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class Embedding:
    """Embedding entity"""
    
    embedding_id: str
    product_id: str
    vector: Any  # numpy.ndarray
    model_name: str
    model_version: str
    dimensions: int
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
    
    def get_vector_hash(self) -> str:
        """Get hash of vector for caching"""
        import hashlib
        return hashlib.md5(self.vector.tobytes()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (without vector data)"""
        return {
            "embedding_id": self.embedding_id,
            "product_id": self.product_id,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "dimensions": self.dimensions,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Embedding":
        """Create from dictionary"""
        if "created_at" in data and data["created_at"]:
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)