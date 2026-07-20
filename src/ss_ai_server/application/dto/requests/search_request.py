"""
SearchRequest - Request DTO for image search
"""

from dataclasses import dataclass, field
from typing import Optional


SUPPORTED_FORMATS = {"image/jpeg", "image/png", "image/webp"}
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
DEFAULT_MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB


@dataclass
class SearchRequest:
    """Search request DTO"""
    
    image_data: bytes
    original_filename: Optional[str] = None
    content_type: Optional[str] = None
    limit: int = 20
    threshold: float = 0.7
    cache_key: Optional[str] = None
    max_image_size: int = DEFAULT_MAX_IMAGE_SIZE
    
    def __post_init__(self) -> None:
        """Validate request data"""
        if not self.image_data or len(self.image_data) == 0:
            raise ValueError("Image data is required and cannot be empty")
        
        if len(self.image_data) > self.max_image_size:
            raise ValueError(
                f"Image size ({len(self.image_data)} bytes) exceeds maximum "
                f"allowed size ({self.max_image_size} bytes)"
            )
        
        if self.limit < 1:
            raise ValueError("Limit must be at least 1")
        if self.limit > 100:
            raise ValueError("Limit cannot exceed 100")
        if not 0.0 <= self.threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")
        if self.max_image_size < 1024:
            raise ValueError("Max image size must be at least 1KB")