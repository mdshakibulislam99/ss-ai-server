"""
IndexingService - Domain service for product indexing pipeline
"""

import asyncio
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from ..interfaces.ai_provider import AIProvider
from ..interfaces.vector_store import VectorStore
from ..interfaces.repository import Repository
from ..interfaces.logger import Logger
from ..entities.product import Product
from ..value_objects.embedding_vector import EmbeddingVector


class IndexingService:
    """
    Domain service for the product indexing pipeline.
    
    Orchestrates the full indexing workflow:
    1. Validate image URLs
    2. Download images
    3. Generate embeddings via AIProvider
    4. Store embeddings via VectorStore
    5. Persist product metadata via Repository
    
    Depends only on interfaces - not on any concrete implementation.
    """
    
    def __init__(
        self,
        ai_provider: AIProvider,
        vector_store: VectorStore,
        product_repository: Repository[Product],
        logger: Optional[Logger] = None,
        max_image_size: int = 10 * 1024 * 1024,  # 10MB
        download_timeout: int = 30,
    ) -> None:
        """
        Initialize indexing service.
        
        Args:
            ai_provider: Provider for generating image embeddings
            vector_store: Store for persisting embeddings
            product_repository: Repository for product metadata
            logger: Optional logger instance
            max_image_size: Maximum allowed image size in bytes
            download_timeout: Timeout for image downloads in seconds
        """
        self._ai_provider = ai_provider
        self._vector_store = vector_store
        self._product_repository = product_repository
        self._logger = logger
        self._max_image_size = max_image_size
        self._download_timeout = download_timeout
    
    async def index_product(
        self,
        product_id: str,
        site_id: str,
        image_urls: List[str],
        title: Optional[str] = None,
        sku: Optional[str] = None,
        description: Optional[str] = None,
        categories: Optional[List[str]] = None,
        attributes: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        reindex: bool = False,
    ) -> Tuple[int, List[str]]:
        """
        Index a single product with its images.
        
        Args:
            product_id: Unique product identifier
            site_id: Site/tenant identifier
            image_urls: List of image URLs to index
            title: Product title
            sku: Product SKU
            description: Product description
            categories: Product categories
            attributes: Product attributes
            metadata: Additional product metadata
            reindex: If True, delete existing embeddings before re-indexing
            
        Returns:
            Tuple of (images_indexed_count, list_of_errors)
            
        Raises:
            ValueError: If validation fails
        """
        errors: List[str] = []
        images_indexed = 0
        
        # Step 1: Handle reindex - delete existing embeddings
        if reindex:
            try:
                deleted = self._vector_store.delete_vectors([product_id])
                if deleted > 0:
                    self._log_info(f"Deleted {deleted} existing embeddings for product {product_id}")
            except Exception as e:
                self._log_warning(f"Failed to delete existing embeddings for {product_id}: {e}")
        
        # Step 2: Validate image URLs
        valid_urls = self._validate_image_urls(image_urls, errors)
        if not valid_urls:
            return 0, errors
        
        # Step 3: Download images
        downloaded = await self._download_images(valid_urls, errors)
        if not downloaded:
            return 0, errors
        
        # Step 4: Generate embeddings
        try:
            embeddings = self._ai_provider.generate_embeddings_batch(downloaded)
        except Exception as e:
            error_msg = f"Failed to generate embeddings: {str(e)}"
            errors.append(error_msg)
            self._log_error(error_msg)
            return 0, errors
        
        # Step 5: Store embeddings in vector store
        try:
            vector_tuples = []
            for i, (embedding, url) in enumerate(zip(embeddings, valid_urls)):
                enriched_metadata = {
                    "product_id": product_id,
                    "site_id": site_id,
                    "image_url": url,
                    "image_index": i,
                    "title": title or "",
                    "sku": sku or "",
                    "categories": categories or [],
                    "attributes": attributes or {},
                    **(metadata or {}),
                }
                vector_tuples.append((product_id, embedding, enriched_metadata))
            
            self._vector_store.add_vectors(vector_tuples)
            images_indexed = len(vector_tuples)
            self._log_info(f"Stored {images_indexed} embeddings for product {product_id}")
        except Exception as e:
            error_msg = f"Failed to store embeddings in vector store: {str(e)}"
            errors.append(error_msg)
            self._log_error(error_msg)
            return 0, errors
        
        # Step 6: Persist product metadata
        try:
            product_metadata = {
                "title": title,
                "sku": sku,
                "description": description,
                "categories": categories or [],
                "attributes": attributes or {},
                "image_urls": image_urls,
                **(metadata or {}),
            }
            
            product = Product(
                product_id=product_id,
                site_id=site_id,
                title=title,
                description=description,
                image_urls=image_urls,
                metadata=product_metadata,
                indexed_at=datetime.now(timezone.utc),
            )
            
            exists = await self._product_repository.exists(product_id)
            if exists:
                await self._product_repository.update(product)
            else:
                await self._product_repository.add(product)
            
            self._log_info(f"Product {product_id} metadata persisted")
        except Exception as e:
            error_msg = f"Failed to persist product metadata: {str(e)}"
            errors.append(error_msg)
            self._log_error(error_msg)
        
        return images_indexed, errors
    
    def _validate_image_urls(self, urls: List[str], errors: List[str]) -> List[str]:
        """
        Validate image URLs.
        
        Args:
            urls: List of image URLs
            errors: Error list to append to
            
        Returns:
            List of valid URLs
        """
        valid = []
        for url in urls:
            if not url or not isinstance(url, str):
                errors.append(f"Invalid image URL: {url}")
                continue
            url = url.strip()
            if not url.startswith(("http://", "https://")):
                errors.append(f"Image URL must start with http:// or https://: {url}")
                continue
            valid.append(url)
        return valid
    
    async def _download_images(self, urls: List[str], errors: List[str]) -> List[bytes]:
        """
        Download images from URLs.
        
        Args:
            urls: List of image URLs
            errors: Error list to append to
            
        Returns:
            List of downloaded image bytes
        """
        import httpx
        
        downloaded = []
        
        async with httpx.AsyncClient(timeout=self._download_timeout) as client:
            for url in urls:
                try:
                    response = await client.get(url)
                    response.raise_for_status()
                    
                    content = response.content
                    if len(content) > self._max_image_size:
                        errors.append(f"Image too large ({len(content)} bytes): {url}")
                        continue
                    if len(content) == 0:
                        errors.append(f"Empty image downloaded: {url}")
                        continue
                    
                    downloaded.append(content)
                    self._log_debug(f"Downloaded image ({len(content)} bytes): {url}")
                except httpx.TimeoutException:
                    errors.append(f"Timeout downloading image: {url}")
                except httpx.HTTPStatusError as e:
                    errors.append(f"HTTP error {e.response.status_code} downloading image: {url}")
                except Exception as e:
                    errors.append(f"Failed to download image {url}: {str(e)}")
        
        return downloaded
    
    def _log_debug(self, message: str) -> None:
        """Log debug message."""
        if self._logger:
            self._logger.debug(message)
    
    def _log_info(self, message: str) -> None:
        """Log info message."""
        if self._logger:
            self._logger.info(message)
    
    def _log_warning(self, message: str) -> None:
        """Log warning message."""
        if self._logger:
            self._logger.warning(message)
    
    def _log_error(self, message: str) -> None:
        """Log error message."""
        if self._logger:
            self._logger.error(message)