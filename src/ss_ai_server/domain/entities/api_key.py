"""
ApiKey entity - Represents an API key for authentication
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class ApiKey:
    """API key entity"""
    
    key_id: str
    key_hash: str
    site_id: str
    name: str
    permissions: List[str]
    rate_limit: int = 60
    ip_whitelist: Optional[List[str]] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.ip_whitelist is None:
            self.ip_whitelist = []
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
    
    def is_expired(self) -> bool:
        """Check if API key is expired"""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if API key is valid"""
        return self.is_active and not self.is_expired()
    
    def has_permission(self, permission: str) -> bool:
        """Check if API key has permission"""
        return permission in self.permissions
    
    def is_ip_allowed(self, ip_address: str) -> bool:
        """Check if IP address is allowed"""
        if not self.ip_whitelist:
            return True
        return ip_address in self.ip_whitelist
    
    def update_last_used(self) -> "ApiKey":
        """Update last used timestamp"""
        self.last_used_at = datetime.now(timezone.utc)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (without sensitive data)"""
        return {
            "key_id": self.key_id,
            "site_id": self.site_id,
            "name": self.name,
            "permissions": self.permissions,
            "rate_limit": self.rate_limit,
            "ip_whitelist": self.ip_whitelist,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiKey":
        """Create from dictionary"""
        # Parse datetime fields
        for field in ["created_at", "expires_at", "last_used_at"]:
            if field in data and data[field]:
                data[field] = datetime.fromisoformat(data[field])
        
        return cls(**data)