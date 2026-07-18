"""
ApiKeyHash value object - Represents a hashed API key
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ApiKeyHash:
    """API key hash value object"""
    
    hash_value: str
    algorithm: str = "SHA256"
    
    def __str__(self) -> str:
        """String representation"""
        return self.hash_value
    
    def __repr__(self) -> str:
        """Representation"""
        return f"ApiKeyHash({self.algorithm}:{self.hash_value[:8]}...)"
    
    @classmethod
    def from_string(cls, hash_string: str, algorithm: str = "SHA256") -> "ApiKeyHash":
        """Create from hash string"""
        return cls(hash_value=hash_string, algorithm=algorithm)
    
    def verify(self, api_key: str, hashed: str) -> bool:
        """Verify API key against hash"""
        import hashlib
        hashed_input = hashlib.sha256(api_key.encode()).hexdigest()
        return hashed_input == self.hash_value