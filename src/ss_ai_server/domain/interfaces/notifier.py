"""
Notifier interface - Abstract base class for notifications
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Notifier(ABC):
    """Abstract base class for notifications"""
    
    @abstractmethod
    async def send(self, recipient: str, subject: str, message: str, 
                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Send notification
        
        Args:
            recipient: Recipient (email, webhook, etc.)
            subject: Notification subject
            message: Notification message
            metadata: Additional metadata
            
        Returns:
            True if sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    async def send_batch(self, notifications: list[Dict[str, Any]]) -> list[bool]:
        """
        Send batch notifications
        
        Args:
            notifications: List of notification dicts
            
        Returns:
            List of success/failure booleans
        """
        pass