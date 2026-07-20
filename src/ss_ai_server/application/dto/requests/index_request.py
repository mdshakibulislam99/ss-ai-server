"""
IndexRequest - Request DTO for product indexing
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class IndexRequest:
    """Request DTO for indexing a product"""
    
    product_id: str
    site_id: str
    title: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    categories: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    featured_image_url: Optional[str] = None
    gallery_image_urls: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    reindex: bool = False
    
    def __post_init__(self) -> None:
        """Validate request data"""
        if not self.product_id or not self.product_id.strip():
            raise ValueError("product_id is required and cannot be empty")
        if not self.site_id or not self.site_id.strip():
            raise ValueError("site_id is required and cannot be empty")
        if not self.featured_image_url and not self.gallery_image_urls:
            raise ValueError("At least one image URL is required (featured_image_url or gallery_image_urls)")
    
    @property
    def all_image_urls(self) -> List[str]:
        """Get all image URLs combined"""
        urls = []
        if self.featured_image_url:
            urls.append(self.featured_image_url)
        urls.extend(self.gallery_image_urls)
        return urls


@dataclass
class BatchIndexRequest:
    """Request DTO for batch indexing products"""
    
    products: List[IndexRequest]
    
    def __post_init__(self) -> None:
        """Validate batch request"""
        if not self.products:
            raise ValueError("At least one product is required for batch indexing")
        if len(self.products) > 100:
            raise ValueError("Batch size cannot exceed 100 products")
</｜｜DSML｜｜parameter>
<｜｜DSML｜｜parameter name="task_progress" string="true">- [x] Read existing architecture files
- [ ] Create IndexRequest/IndexResponse DTOs
- [ ] Create IndexProductUseCase
- [ ] Create IndexingService in domain services
- [ ] Update ProductRepository
- [ ] Update API route (v1/index.py)
- [ ] Wire dependencies in container.py
- [ ] Commit and push</｜｜DSML｜｜parameter>
</｜｜DSML｜｜invoke>
</｜｜DSML｜｜tool_calls>