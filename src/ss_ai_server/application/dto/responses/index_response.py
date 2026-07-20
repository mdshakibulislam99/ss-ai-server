"""
IndexResponse - Response DTO for product indexing
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class IndexResponse:
    """Response DTO for product indexing"""
    
    success: bool
    product_id: str
    images_indexed: int = 0
    processing_time_ms: float = 0.0
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "product_id": self.product_id,
            "images_indexed": self.images_indexed,
            "processing_time_ms": self.processing_time_ms,
            "message": self.message,
            "errors": self.errors,
            "metadata": self.metadata,
        }


@dataclass
class BatchIndexResponse:
    """Response DTO for batch product indexing"""
    
    success: bool
    total_products: int = 0
    indexed_count: int = 0
    failed_count: int = 0
    results: List[IndexResponse] = field(default_factory=list)
    processing_time_ms: float = 0.0
    message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "total_products": self.total_products,
            "indexed_count": self.indexed_count,
            "failed_count": self.failed_count,
            "results": [r.to_dict() for r in self.results],
            "processing_time_ms": self.processing_time_ms,
            "message": self.message,
        }