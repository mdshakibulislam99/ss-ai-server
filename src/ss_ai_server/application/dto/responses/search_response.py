"""
SearchResponse - Response DTO for image search
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SearchResultItem:
    """Individual search result item"""
    
    product_id: str
    similarity_score: float
    confidence_percentage: float
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "product_id": self.product_id,
            "similarity_score": self.similarity_score,
            "confidence_percentage": self.confidence_percentage,
            "metadata": self.metadata or {},
        }


@dataclass
class SearchResponse:
    """Search response DTO"""
    
    success: bool
    results: List[SearchResultItem]
    query_embedding: Optional[Any] = None
    total_count: int = 0
    processing_time_ms: float = 0.0
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "results": [r.to_dict() for r in self.results],
            "total_count": self.total_count,
            "processing_time_ms": self.processing_time_ms,
            "message": self.message,
            "metadata": self.metadata,
        }
