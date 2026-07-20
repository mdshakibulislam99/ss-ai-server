"""
SearchImageUseCase - Use case for searching similar images
"""

import time
from typing import List, Optional

from ..interfaces.use_case import UseCase
from ..dto.requests.search_request import SearchRequest
from ..dto.responses.search_response import SearchResponse, SearchResultItem
from ...domain.services.search_service import SearchService
from ...domain.interfaces.logger import Logger


class SearchImageUseCase(UseCase[SearchRequest, SearchResponse]):
    """Use case for searching similar images"""
    
    def __init__(
        self,
        search_service: SearchService,
        logger: Optional[Logger] = None,
    ) -> None:
        """
        Initialize search image use case
        
        Args:
            search_service: Domain service for search pipeline
            logger: Optional logger instance
        """
        self._search_service = search_service
        self._logger = logger
    
    async def execute(self, request: SearchRequest) -> SearchResponse:
        """
        Execute search use case
        
        Args:
            request: Search request with image data
            
        Returns:
            Search response with results
        """
        start_time = time.time()
        
        self._log_info("Starting image search")
        
        try:
            # Execute full search pipeline
            results, query_embedding, elapsed_ms = await self._search_service.search_similar(
                image_data=request.image_data,
                limit=request.limit,
                threshold=request.threshold,
                cache_key=request.cache_key,
            )
            
            # Convert to response DTOs
            result_items = [
                SearchResultItem(
                    product_id=r.product_id,
                    similarity_score=r.similarity_score,
                    confidence_percentage=r.similarity_score * 100,
                    metadata=r.metadata or {},
                )
                for r in results
            ]
            
            self._log_info(
                f"Search completed: {len(results)} results in {elapsed_ms:.0f}ms"
            )
            
            return SearchResponse(
                success=True,
                results=result_items,
                query_embedding=query_embedding,
                total_count=len(results),
                processing_time_ms=elapsed_ms,
                message=f"Found {len(results)} similar products",
            )
            
        except ValueError as e:
            self._log_error(f"Validation error: {e}")
            return SearchResponse(
                success=False,
                results=[],
                total_count=0,
                message="Invalid image",
                processing_time_ms=(time.time() - start_time) * 1000,
            )
        except RuntimeError as e:
            self._log_error(f"Search error: {e}")
            return SearchResponse(
                success=False,
                results=[],
                total_count=0,
                message=str(e),
                processing_time_ms=(time.time() - start_time) * 1000,
            )
        except Exception as e:
            self._log_error(f"Unexpected error: {e}")
            return SearchResponse(
                success=False,
                results=[],
                total_count=0,
                message="Internal search error",
                processing_time_ms=(time.time() - start_time) * 1000,
            )
    
    def _log_info(self, message: str) -> None:
        """Log info message."""
        if self._logger:
            self._logger.info(message)
    
    def _log_error(self, message: str) -> None:
        """Log error message."""
        if self._logger:
            self._logger.error(message)