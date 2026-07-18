"""
ModelName value object - Represents an AI model identifier
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ModelName:
    """Model name value object"""
    
    value: str
    provider: str
    version: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation"""
        if self.version:
            return f"{self.provider}:{self.value}:{self.version}"
        return f"{self.provider}:{self.value}"
    
    def __repr__(self) -> str:
        """Representation"""
        return f"ModelName({self})"
    
    @classmethod
    def from_string(cls, model_string: str) -> "ModelName":
        """Create from string format 'provider:model:version'"""
        parts = model_string.split(":")
        if len(parts) == 3:
            provider, value, version = parts
            return cls(value=value, provider=provider, version=version)
        elif len(parts) == 2:
            provider, value = parts
            return cls(value=value, provider=provider)
        else:
            raise ValueError(f"Invalid model string format: {model_string}")