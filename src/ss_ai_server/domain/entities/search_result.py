"""
SearchResult entity - Represents a search result
"""

from dataclasses import dataclass
from typing import Any,  Dict,  Optional


@dataclass
class SearchResult:
    """Search result entity"""
    
    product_id: str
    similarity_score: float
    product_data: Optional[Dict[str, Any]] = None
    rank: int = 0
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self) -> None:
        """Initialize default values"""
        if self.product_data is None:
            self.product_data = {}
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "product_id": self.product_id,
            "similarity_score": self.similarity_score,
            "product_data": self.product_data,
            "rank": self.rank,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        """Create from dictionary"""
        return cls(**data)