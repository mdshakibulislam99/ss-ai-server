"""
Health Checker - Health check implementation
"""

from typing import Dict, List, Optional

from ...domain.interfaces.logger import Logger


class HealthChecker:
    """Health check implementation"""
    
    def __init__(self, logger: Logger):
        """
        Initialize health checker
        
        Args:
            logger: Logger instance
        """
        self._logger = logger
        self._checks = {}
    
    def register_check(self, name: str, check_func) -> None:
        """
        Register health check
        
        Args:
            name: Check name
            check_func: Check function (async, returns bool)
        """
        self._checks[name] = check_func
    
    async def check_health(self) -> Dict[str, any]:
        """
        Run all health checks
        
        Returns:
            Health status dictionary
        """
        results = {}
        overall_healthy = True
        
        for name, check_func in self._checks.items():
            try:
                is_healthy = await check_func()
                results[name] = {
                    "status": "healthy" if is_healthy else "unhealthy",
                    "healthy": is_healthy
                }
                if not is_healthy:
                    overall_healthy = False
            except Exception as e:
                self._logger.error(f"Health check failed: {name}", error=str(e))
                results[name] = {
                    "status": "error",
                    "healthy": False,
                    "error": str(e)
                }
                overall_healthy = False
        
        return {
            "healthy": overall_healthy,
            "checks": results
        }