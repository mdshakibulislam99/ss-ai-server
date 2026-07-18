"""
ConfidenceScore value object - Represents a confidence/score value
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfidenceScore:
    """Confidence score value object"""
    
    value: float
    
    def __post_init__(self) -> None:
        """Validate score"""
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(f"Confidence score must be between 0.0 and 1.0, got {self.value}")
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.value:.4f}"
    
    def __repr__(self) -> str:
        """Representation"""
        return f"ConfidenceScore({self.value})"
    
    def __lt__(self, other: "ConfidenceScore") -> bool:
        """Less than comparison"""
        return self.value < other.value
    
    def __le__(self, other: "ConfidenceScore") -> bool:
        """Less than or equal comparison"""
        return self.value <= other.value
    
    def __gt__(self, other: "ConfidenceScore") -> bool:
        """Greater than comparison"""
        return self.value > other.value
    
    def __ge__(self, other: "ConfidenceScore") -> bool:
        """Greater than or equal comparison"""
        return self.value >= other.value
    
    def is_above_threshold(self, threshold: float) -> bool:
        """Check if score is above threshold"""
        return self.value >= threshold
    
    def to_percentage(self) -> float:
        """Convert to percentage"""
        return self.value * 100