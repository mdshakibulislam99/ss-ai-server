"""
QueueJob entity - Represents a background job
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict,  Optional


class JobStatus(str, Enum):
    """Job status enum"""
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class JobType(str, Enum):
    """Job type enum"""
    EMBEDDING_GENERATION = "embedding_generation"
    BATCH_INDEXING = "batch_indexing"
    REINDEXING = "reindexing"
    DELETE_EMBEDDINGS = "delete_embeddings"
    DUPLICATE_DETECTION = "duplicate_detection"
    MODEL_WARMUP = "model_warmup"
    BACKUP = "backup"
    CLEANUP = "cleanup"


@dataclass
class QueueJob:
    """Queue job entity"""
    
    job_id: str
    job_type: JobType
    payload: Dict[str, Any]
    status: JobStatus = JobStatus.PENDING
    priority: int = 0
    retry_count: int = 0
    max_retries: int = 3
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
    
    def start(self) -> "QueueJob":
        """Mark job as started"""
        self.status = JobStatus.PROCESSING
        self.started_at = datetime.now(timezone.utc)
        return self
    
    def complete(self, result: Dict[str, Any]) -> "QueueJob":
        """Mark job as completed"""
        self.status = JobStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now(timezone.utc)
        return self
    
    def fail(self, error: str) -> "QueueJob":
        """Mark job as failed"""
        self.status = JobStatus.FAILED
        self.error = error
        self.completed_at = datetime.now(timezone.utc)
        return self
    
    def retry(self) -> "QueueJob":
        """Retry job"""
        self.retry_count += 1
        self.status = JobStatus.RETRYING
        self.error = None
        return self
    
    def can_retry(self) -> bool:
        """Check if job can be retried"""
        return self.retry_count < self.max_retries
    
    def cancel(self) -> "QueueJob":
        """Cancel job"""
        self.status = JobStatus.CANCELLED
        self.completed_at = datetime.now(timezone.utc)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "job_id": self.job_id,
            "job_type": self.job_type.value,
            "status": self.status.value,
            "priority": self.priority,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "payload": self.payload,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QueueJob":
        """Create from dictionary"""
        # Convert string enums
        if "job_type" in data:
            data["job_type"] = JobType(data["job_type"])
        if "status" in data:
            data["status"] = JobStatus(data["status"])
        
        # Parse datetime fields
        for field in ["created_at", "started_at", "completed_at"]:
            if field in data and data[field]:
                data[field] = datetime.fromisoformat(data[field])
        
        return cls(**data)