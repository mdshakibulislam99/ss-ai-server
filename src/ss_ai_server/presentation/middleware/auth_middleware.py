"""
Authentication Middleware

Handles API key validation and authentication
"""

from typing import Callable, Optional
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from ...config.settings import Settings, settings
from ...domain.interfaces.cache import Cache
from ...exceptions.base_exceptions import AuthorizationError


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """
    API Key authentication middleware
    
    Validates API keys from request headers
    """
    
    def __init__(
        self,
        app,
        settings: Optional[Settings] = None,
        cache: Optional[Cache] = None,
        exclude_paths: Optional[list] = None
    ):
        """
        Initialize API key auth middleware
        
        Args:
            app: ASGI application
            settings: Application settings
            cache: Cache service for API key validation
            exclude_paths: Paths to exclude from authentication
        """
        super().__init__(app)
        self.settings = settings or Settings()
        self.cache = cache
        self.exclude_paths = exclude_paths or [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/health",
            "/api/v1/health/",
            "/api/v1/health/ready",
            "/api/v1/health/live",
        ]
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ):
        """
        Process request and validate API key
        
        Args:
            request: HTTP request
            call_next: Next middleware/handler
            
        Returns:
            HTTP response
            
        Raises:
            HTTPException: If authentication fails
        """
        # Skip authentication for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)
        
        # Get API key from header
        api_key = request.headers.get(self.settings.api_key_header)
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Missing API key. Provide key in '{self.settings.api_key_header}' header",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        # Validate API key (simplified - in production, validate against database)
        if not self._validate_api_key(api_key):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        # Add API key info to request state
        request.state.api_key = api_key
        
        return await call_next(request)
    
    def _validate_api_key(self, api_key: str) -> bool:
        """
        Validate API key
        
        Args:
            api_key: API key to validate
            
        Returns:
            True if valid, False otherwise
        """
        # In production, validate against database or external service
        # For now, check against environment variable or accept all in development
        if self.settings.is_development:
            return True
        
        # Check cache first
        if self.cache:
            cached_result = self.cache.get(f"api_key:{api_key}")
            if cached_result is not None:
                return cached_result
        
        # Validate against configured API keys
        # In production, this would query a database
        valid_keys = getattr(self.settings, 'valid_api_keys', [])
        is_valid = api_key in valid_keys if valid_keys else False
        
        # Cache result
        if self.cache and is_valid:
            self.cache.set(f"api_key:{api_key}", True, ttl=3600)
        
        return is_valid


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Generic authentication middleware
    
    Supports multiple authentication methods
    """
    
    def __init__(
        self,
        app,
        settings: Optional[Settings] = None,
        cache: Optional[Cache] = None
    ):
        """
        Initialize auth middleware
        
        Args:
            app: ASGI application
            settings: Application settings
            cache: Cache service
        """
        super().__init__(app)
        self.settings = settings or Settings()
        self.cache = cache
        self.api_key_middleware = APIKeyAuthMiddleware(
            app,
            settings=settings,
            cache=cache
        )
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ):
        """
        Process request with authentication
        
        Args:
            request: HTTP request
            call_next: Next middleware/handler
            
        Returns:
            HTTP response
        """
        # Use API key authentication
        return await self.api_key_middleware.dispatch(request, call_next)