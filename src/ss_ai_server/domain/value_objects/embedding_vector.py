"""
EmbeddingVector value object - Represents a vector embedding
"""

from dataclasses import dataclass
from typing import List, Optional

import numpy as np


@dataclass(frozen=True)
class EmbeddingVector:
    """Embedding vector value object"""
    
    values: np.ndarray
    model_name: str
    dimensions: int
    version: Optional[str] = None
    
    def __post_init__(self):
        """Validate vector"""
        if not isinstance(self.values, np.ndarray):
            raise TypeError("Values must be a numpy array")
        if self.values.ndim != 1:
            raise ValueError("Values must be a 1D array")
        if len(self.values) != self.dimensions:
            raise ValueError(f"Vector length {len(self.values)} does not match dimensions {self.dimensions}")
    
    def __len__(self) -> int:
        """Get vector length"""
        return len(self.values)
    
    def __getitem__(self, index: int) -> float:
        """Get vector element"""
        return self.values[index]
    
    def normalize(self) -> "EmbeddingVector":
        """Normalize vector (L2 normalization)"""
        norm = np.linalg.norm(self.values)
        if norm == 0:
            return self
        normalized = self.values / norm
        return EmbeddingVector(
            values=normalized,
            model_name=self.model_name,
            dimensions=self.dimensions,
            version=self.version
        )
    
    def cosine_similarity(self, other: "EmbeddingVector") -> float:
        """Calculate cosine similarity with another vector"""
        if self.dimensions != other.dimensions:
            raise ValueError("Vectors must have same dimensions")
        
        dot_product = np.dot(self.values, other.values)
        norm_product = np.linalg.norm(self.values) * np.linalg.norm(other.values)
        
        if norm_product == 0:
            return 0.0
        
        return float(dot_product / norm_product)
    
    def euclidean_distance(self, other: "EmbeddingVector") -> float:
        """Calculate Euclidean distance to another vector"""
        if self.dimensions != other.dimensions:
            raise ValueError("Vectors must have same dimensions")
        
        return float(np.linalg.norm(self.values - other.values))
    
    def to_list(self) -> List[float]:
        """Convert to list of floats"""
        return self.values.tolist()
    
    @classmethod
    def from_list(cls, values: List[float], model_name: str, version: Optional[str] = None) -> "EmbeddingVector":
        """Create from list of floats"""
        return cls(
            values=np.array(values, dtype=np.float32),
            model_name=model_name,
            dimensions=len(values),
            version=version
        )