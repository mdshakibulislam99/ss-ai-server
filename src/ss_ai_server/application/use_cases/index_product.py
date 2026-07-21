"""
IndexProductUseCase - Use case for indexing a product
"""

import time
from typing import List, Optional

from ..interfaces.use_case import UseCase
from ..dto.requests.index_request import IndexRequest, BatchIndexRequest
from ..dto.responses.index_response import IndexResponse, BatchIndexResponse
from ss_ai_server.domain.services.indexing_service import IndexingService
from ss_ai_server.domain.interfaces.logger import Logger


class IndexProductUseCase(UseCase[IndexRequest, IndexResponse]):
    """
    Use case for indexing a single product.
    
    Orchestrates the full indexing pipeline through IndexingService.
    """
    
    def __init__(
        self,
        indexing_service: IndexingService,
        logger: Optional[Logger] = None,
    ) -> None:
        """
        Initialize index product use case.
        
        Args:
            indexing_service: Domain service for indexing
            logger: Optional logger instance
        """
        self._indexing_service = indexing_service
        self._logger = logger
    
    async def execute(self, request: IndexRequest) -> IndexResponse:
        """
        Execute the indexing use case.
        
        Args:
            request: Index request with product data
            
        Returns:
            Index response with results
        """
        start_time = time.time()
        errors: List[str] = []
        
        self._log_info(f"Starting indexing for product {request.product_id}")
        
        try:
            images_indexed, pipeline_errors = await self._indexing_service.index_product(
                product_id=request.product_id,
                site_id=request.site_id,
                image_urls=request.all_image_urls,
                title=request.title,
                sku=request.sku,
                description=request.description,
                categories=request.categories,
                attributes=request.attributes,
                metadata=request.metadata,
                reindex=request.reindex,
            )
            errors.extend(pipeline_errors)
        except ValueError as e:
            return IndexResponse(
                success=False,
                product_id=request.product_id,
                message="Validation failed",
                errors=[str(e)],
                processing_time_ms=(time.time() - start_time) * 1000,
            )
        except Exception as e:
            self._log_error(f"Unexpected error indexing product {request.product_id}: {e}")
            return IndexResponse(
                success=False,
                product_id=request.product_id,
                message="Internal indexing error",
                errors=[str(e)],
                processing_time_ms=(time.time() - start_time) * 1000,
            )
        
        elapsed_ms = (time.time() - start_time) * 1000
        success = images_indexed > 0 and not errors
        
        self._log_info(
            f"Product {request.product_id} indexed: "
            f"{images_indexed} images in {elapsed_ms:.0f}ms"
        )
        
        return IndexResponse(
            success=success,
            product_id=request.product_id,
            images_indexed=images_indexed,
            processing_time_ms=elapsed_ms,
            message=f"Successfully indexed {images_indexed} images" if success else "Indexing completed with errors",
            errors=errors,
            metadata={
                "title": request.title,
                "sku": request.sku,
                "reindex": request.reindex,
            },
        )
    
    def _log_info(self, message: str) -> None:
        """Log info message."""
        if self._logger:
            self._logger.info(message)
    
    def _log_error(self, message: str) -> None:
        """Log error message."""
        if self._logger:
            self._logger.error(message)


class BatchIndexUseCase(UseCase[BatchIndexRequest, BatchIndexResponse]):
    """
    Use case for batch indexing multiple products.
    """
    
    def __init__(
        self,
        index_product_use_case: IndexProductUseCase,
        logger: Optional[Logger] = None,
    ) -> None:
        """
        Initialize batch index use case.
        
        Args:
            index_product_use_case: Single product indexing use case
            logger: Optional logger instance
        """
        self._index_product_use_case = index_product_use_case
        self._logger = logger
    
    async def execute(self, request: BatchIndexRequest) -> BatchIndexResponse:
        """
        Execute batch indexing.
        
        Args:
            request: Batch index request
            
        Returns:
            Batch index response
        """
        start_time = time.time()
        results: List[IndexResponse] = []
        
        self._log_info(f"Starting batch indexing for {len(request.products)} products")
        
        for product_request in request.products:
            try:
                result = await self._index_product_use_case.execute(product_request)
                results.append(result)
            except Exception as e:
                results.append(IndexResponse(
                    success=False,
                    product_id=product_request.product_id,
                    message="Batch indexing error",
                    errors=[str(e)],
                ))
        
        elapsed_ms = (time.time() - start_time) * 1000
        indexed_count = sum(1 for r in results if r.success)
        failed_count = sum(1 for r in results if not r.success)
        
        self._log_info(
            f"Batch indexing completed: {indexed_count} indexed, "
            f"{failed_count} failed in {elapsed_ms:.0f}ms"
        )
        
        return BatchIndexResponse(
            success=failed_count == 0,
            total_products=len(request.products),
            indexed_count=indexed_count,
            failed_count=failed_count,
            results=results,
            processing_time_ms=elapsed_ms,
            message=f"Indexed {indexed_count}/{len(request.products)} products",
        )
    
    def _log_info(self, message: str) -> None:
        """Log info message."""
        if self._logger:
            self._logger.info(message)