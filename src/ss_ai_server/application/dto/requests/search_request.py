"""
SearchRequest - Request DTO for image search
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchRequest:
    """Search request DTO"""
    
    image_data: bytes
    limit: int = 20
    threshold: float = 0.7
    cache_key: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate request"""
        if self.limit < 1:
            raise ValueError("Limit must be at least 1")
        if self.limit > 100:
            raise ValueError("Limit cannot exceed 100")
        if not 0.0 <= self.threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")