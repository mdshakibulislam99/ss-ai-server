"""
SearchResponse - Response DTO for image search
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SearchResultItem(BaseModel):
    """Individual search result item"""
    
    product_id: str
    similarity_score: float
    confidence_percentage: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """Search response DTO"""
    
    success: bool
    results: List[SearchResultItem] = Field(default_factory=list)
    query_embedding: Optional[Any] = None
    total_count: int = 0
    processing_time_ms: float = 0.0
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None