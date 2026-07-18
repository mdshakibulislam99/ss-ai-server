# SS AI Server - Complete System Architecture

**Version:** 1.0.0  
**Status:** Production Design  
**Architecture Type:** Enterprise Microservices-Ready Monolith  
**Design Philosophy:** Modular, Scalable, Cloud-Native, Future-Proof

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Folder Structure](#2-folder-structure)
3. [Module Architecture](#3-module-architecture)
4. [Layer Architecture](#4-layer-architecture)
5. [Domain Architecture](#5-domain-architecture)
6. [Service Architecture](#6-service-architecture)
7. [AI Provider Architecture](#7-ai-provider-architecture)
8. [Vector Database Architecture](#8-vector-database-architecture)
9. [API Architecture](#9-api-architecture)
10. [Authentication Architecture](#10-authentication-architecture)
11. [Queue Architecture](#11-queue-architecture)
12. [Worker Architecture](#12-worker-architecture)
13. [Embedding Pipeline](#13-embedding-pipeline)
14. [Search Pipeline](#14-search-pipeline)
15. [Index Pipeline](#15-index-pipeline)
16. [Storage Architecture](#16-storage-architecture)
17. [Cache Architecture](#17-cache-architecture)
18. [Logging Architecture](#18-logging-architecture)
19. [Monitoring Architecture](#19-monitoring-architecture)
20. [Analytics Architecture](#20-analytics-architecture)
21. [Security Architecture](#21-security-architecture)
22. [Configuration Architecture](#22-configuration-architecture)
23. [Deployment Architecture](#23-deployment-architecture)
24. [Docker Architecture](#24-docker-architecture)
25. [Dependency Injection Architecture](#25-dependency-injection-architecture)
26. [Interface Design](#26-interface-design)
27. [Future Module Strategy](#27-future-module-strategy)
28. [Scalability Strategy](#28-scalability-strategy)
29. [Error Handling Strategy](#29-error-handling-strategy)
30. [Complete Development Roadmap](#30-complete-development-roadmap)

---

## 1. System Overview

### 1.1 Vision

SS AI Server is a production-grade, enterprise-level AI backend designed to power multiple commercial WordPress plugins. It provides a unified, scalable, and modular platform for AI-powered features including image search, OCR, product recommendations, background removal, and more.

### 1.2 Core Principles

- **Modularity First:** Every component is independently replaceable
- **Interface-Driven:** All dependencies are abstracted behind interfaces
- **Provider Agnostic:** Support multiple AI models, vector databases, and storage backends
- **Cloud Native:** Designed for containerized deployment from day one
- **Performance Optimized:** Async processing, caching, and batch operations built-in
- **Security by Design:** Enterprise-grade security at every layer
- **Observable:** Comprehensive logging, monitoring, and analytics

### 1.3 System Characteristics

- **Language:** Python 3.11+
- **Architecture:** Clean Architecture with Domain-Driven Design
- **API Style:** RESTful with versioning
- **Processing:** Asynchronous with background workers
- **Database:** Multi-database strategy (relational + vector + cache)
- **Deployment:** Container-first, platform-agnostic

### 1.4 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Load Balancer / CDN                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    API Gateway / Reverse Proxy               │
│                  (Rate Limiting, Auth, SSL)                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│  API Server    │  │  API Server │  │   API Server    │
│  (Instance 1)  │  │ (Instance 2)│  │  (Instance N)   │
└───────┬────────┘  └──────┬──────┘  └────────┬────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
        ┌───────────────────▼───────────────────┐
        │      Message Queue (Redis/Bull)        │
        └───────────────────┬───────────────────┘
                            │
        ┌───────────────────▼───────────────────┐
        │         Worker Cluster                │
        │  ┌─────────┐  ┌─────────┐  ┌────────┐ │
        │  │ Worker 1│  │ Worker 2│  │Worker N│ │
        │  └─────────┘  └─────────┘  └────────┘ │
        └───────────────────┬───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│  Vector DB     │  │  Relational │  │   Cache         │
│  (FAISS/etc)   │  │  Database   │  │   (Redis)       │
└────────────────┘  └─────────────┘  └─────────────────┘
```

---

## 2. Folder Structure

### 2.1 Root Structure

```
ss-ai-server/
├── src/
│   ├── ss_ai_server/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── app.py
│   │   │
│   │   ├── domain/                    # Domain Layer (Business Logic)
│   │   │   ├── __init__.py
│   │   │   ├── entities/              # Domain Entities
│   │   │   │   ├── __init__.py
│   │   │   │   ├── product.py
│   │   │   │   ├── embedding.py
│   │   │   │   ├── image.py
│   │   │   │   ├── search_result.py
│   │   │   │   ├── queue_job.py
│   │   │   │   └── api_key.py
│   │   │   │
│   │   │   ├── value_objects/         # Value Objects
│   │   │   │   ├── __init__.py
│   │   │   │   ├── model_name.py
│   │   │   │   ├── embedding_vector.py
│   │   │   │   ├── api_key_hash.py
│   │   │   │   └── confidence_score.py
│   │   │   │
│   │   │   ├── interfaces/            # Domain Interfaces (Abstract Base Classes)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── ai_provider.py
│   │   │   │   ├── vector_store.py
│   │   │   │   ├── embedding_cache.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── queue.py
│   │   │   │   ├── storage.py
│   │   │   │   ├── logger.py
│   │   │   │   └── notifier.py
│   │   │   │
│   │   │   └── services/              # Domain Services
│   │   │       ├── __init__.py
│   │   │       ├── embedding_service.py
│   │   │       ├── search_service.py
│   │   │       └── validation_service.py
│   │   │
│   │   ├── application/               # Application Layer (Use Cases)
│   │   │   ├── __init__.py
│   │   │   ├── use_cases/             # Use Case Implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── search_image.py
│   │   │   │   ├── index_product.py
│   │   │   │   ├── batch_index.py
│   │   │   │   ├── delete_embedding.py
│   │   │   │   ├── detect_duplicates.py
│   │   │   │   └── health_check.py
│   │   │   │
│   │   │   ├── dto/                   # Data Transfer Objects
│   │   │   │   ├── __init__.py
│   │   │   │   ├── requests/
│   │   │   │   │   ├── search_request.py
│   │   │   │   │   ├── index_request.py
│   │   │   │   │   └── batch_index_request.py
│   │   │   │   └── responses/
│   │   │   │       ├── search_response.py
│   │   │   │       ├── index_response.py
│   │   │   │       └── health_response.py
│   │   │   │
│   │   │   └── interfaces/            # Application Interfaces
│   │   │       ├── __init__.py
│   │   │       └── use_case.py
│   │   │
│   │   ├── infrastructure/            # Infrastructure Layer
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── ai/                    # AI Provider Implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_provider.py
│   │   │   │   ├── openclip_provider.py
│   │   │   │   ├── siglip_provider.py
│   │   │   │   ├── mobilenet_provider.py
│   │   │   │   └── provider_factory.py
│   │   │   │
│   │   │   ├── vector_stores/         # Vector Database Implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_vector_store.py
│   │   │   │   ├── faiss_store.py
│   │   │   │   ├── hnswlib_store.py
│   │   │   │   ├── chromadb_store.py
│   │   │   │   └── vector_store_factory.py
│   │   │   │
│   │   │   ├── repositories/          # Repository Implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── product_repository.py
│   │   │   │   ├── embedding_repository.py
│   │   │   │   ├── api_key_repository.py
│   │   │   │   └── queue_repository.py
│   │   │   │
│   │   │   ├── cache/                 # Cache Implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── redis_cache.py
│   │   │   │   ├── memory_cache.py
│   │   │   │   └── embedding_cache.py
│   │   │   │
│   │   │   ├── queue/                 # Queue Implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── redis_queue.py
│   │   │   │   ├── celery_queue.py
│   │   │   │   └── job_processor.py
│   │   │   │
│   │   │   ├── storage/               # Storage Implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── local_storage.py
│   │   │   │   ├── s3_storage.py
│   │   │   │   └── image_handler.py
│   │   │   │
│   │   │   ├── logging/               # Logging Implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── logger.py
│   │   │   │   ├── audit_logger.py
│   │   │   │   └── log_formatter.py
│   │   │   │
│   │   │   ├── monitoring/            # Monitoring Implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── metrics.py
│   │   │   │   ├── health_checker.py
│   │   │   │   └── prometheus_exporter.py
│   │   │   │
│   │   │   └── persistence/           # Database Implementations
│   │   │       ├── __init__.py
│   │   │       ├── postgres.py
│   │   │       ├── sqlite.py
│   │   │       └── database_manager.py
│   │   │
│   │   ├── presentation/              # Presentation Layer (API)
│   │   │   ├── __init__.py
│   │   │   ├── api/                   # API Routes
│   │   │   │   ├── __init__.py
│   │   │   │   ├── v1/                # API Version 1
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── router.py
│   │   │   │   │   ├── search.py
│   │   │   │   │   ├── index.py
│   │   │   │   │   ├── batch.py
│   │   │   │   │   ├── admin.py
│   │   │   │   │   ├── health.py
│   │   │   │   │   └── analytics.py
│   │   │   │   └── v2/                # API Version 2 (Future)
│   │   │   │       └── __init__.py
│   │   │   │
│   │   │   ├── middleware/            # Middleware
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── rate_limit.py
│   │   │   │   ├── cors.py
│   │   │   │   ├── validation.py
│   │   │   │   └── error_handler.py
│   │   │   │
│   │   │   └── schemas/               # Pydantic Schemas
│   │   │       ├── __init__.py
│   │   │       ├── product.py
│   │   │       ├── search.py
│   │   │       └── common.py
│   │   │
│   │   ├── workers/                   # Background Workers
│   │   │   ├── __init__.py
│   │   │   ├── base_worker.py
│   │   │   ├── embedding_worker.py
│   │   │   ├── batch_worker.py
│   │   │   ├── cleanup_worker.py
│   │   │   └── worker_manager.py
│   │   │
│   │   ├── config/                    # Configuration
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── database.py
│   │   │   ├── ai_models.py
│   │   │   └── logging.py
│   │   │
│   │   ├── utils/                     # Utilities
│   │   │   ├── __init__.py
│   │   │   ├── image_processor.py
│   │   │   ├── validators.py
│   │   │   ├── helpers.py
│   │   │   └── decorators.py
│   │   │
│   │   └── exceptions/                # Custom Exceptions
│   │       ├── __init__.py
│   │       ├── domain_exceptions.py
│   │       ├── application_exceptions.py
│   │       └── infrastructure_exceptions.py
│   │
│   └── tests/                         # Test Suite
│       ├── __init__.py
│       ├── unit/
│       ├── integration/
│       ├── e2e/
│       └── fixtures/
│
├── deployments/                       # Deployment Configurations
│   ├── docker/
│   │   ├── Dockerfile
│   │   ├── Dockerfile.worker
│   │   └── .dockerignore
│   ├── docker-compose/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   └── docker-compose.prod.yml
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   └── scripts/
│       ├── deploy.sh
│       ├── migrate.sh
│       └── backup.sh
│
├── docs/                              # Documentation
│   ├── api/
│   ├── architecture/
│   ├── deployment/
│   └── development/
│
├── scripts/                           # Development Scripts
│   ├── setup.sh
│   ├── test.sh
│   ├── lint.sh
│   └── migrate.sh
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── ARCHITECTURE.md
```

### 2.2 Directory Organization Principles

- **Domain Layer:** Pure business logic, no external dependencies
- **Application Layer:** Use cases and orchestration, depends only on domain
- **Infrastructure Layer:** External implementations, depends on domain interfaces
- **Presentation Layer:** API endpoints, depends on application layer
- **Workers:** Background processing, can access all layers

---

## 3. Module Architecture

### 3.1 Core Modules

```
┌─────────────────────────────────────────────────────────────┐
│                      SS AI Server Core                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   AI Module  │  │ Search Module│  │ Index Module │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │              │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐     │
│  │ Queue Module │  │ Auth Module  │  │Cache Module  │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │              │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐     │
│  │Logger Module │  │Analytics Mod │  │Monitor Module│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Module Descriptions

#### 3.2.1 AI Module
**Purpose:** Manage AI model providers and generate embeddings

**Responsibilities:**
- Model provider abstraction
- Embedding generation
- Model switching and configuration
- Batch embedding processing
- Model versioning support

**Key Components:**
- AI Provider Factory
- Model Registry
- Embedding Generator
- Batch Processor

#### 3.2.2 Search Module
**Purpose:** Handle similarity search operations

**Responsibilities:**
- Vector similarity search
- Result ranking and filtering
- Search history tracking
- Search analytics
- Multi-modal search support

**Key Components:**
- Search Engine
- Result Ranker
- Search History Manager
- Similarity Calculator

#### 3.2.3 Index Module
**Purpose:** Manage product indexing and embedding storage

**Responsibilities:**
- Product registration
- Embedding storage
- Index management
- Re-indexing operations
- Batch indexing

**Key Components:**
- Index Manager
- Product Registry
- Embedding Store
- Batch Indexer

#### 3.2.4 Queue Module
**Purpose:** Background job processing

**Responsibilities:**
- Job queuing
- Job prioritization
- Job retry logic
- Job status tracking
- Queue monitoring

**Key Components:**
- Queue Manager
- Job Scheduler
- Priority Queue
- Retry Handler

#### 3.2.5 Auth Module
**Purpose:** Authentication and authorization

**Responsibilities:**
- API key validation
- JWT token management
- IP whitelisting
- Rate limiting
- Permission management

**Key Components:**
- Auth Manager
- API Key Validator
- JWT Handler
- Rate Limiter
- IP Filter

#### 3.2.6 Cache Module
**Purpose:** Performance optimization through caching

**Responsibilities:**
- Embedding cache
- Result cache
- Model cache
- Session cache
- Cache invalidation

**Key Components:**
- Cache Manager
- Embedding Cache
- Result Cache
- Cache Invalidation

#### 3.2.7 Logger Module
**Purpose:** Comprehensive logging

**Responsibilities:**
- Request logging
- Error logging
- Audit logging
- Performance logging
- Log aggregation

**Key Components:**
- Logger Factory
- Audit Logger
- Request Logger
- Error Logger

#### 3.2.8 Analytics Module
**Purpose:** Usage analytics and reporting

**Responsibilities:**
- Usage tracking
- Performance metrics
- User analytics
- Search analytics
- Report generation

**Key Components:**
- Analytics Collector
- Metrics Aggregator
- Report Generator
- Dashboard Provider

#### 3.2.9 Monitor Module
**Purpose:** System health and performance monitoring

**Responsibilities:**
- Health checks
- Performance monitoring
- Resource monitoring
- Alert management
- Status reporting

**Key Components:**
- Health Checker
- Metrics Collector
- Alert Manager
- Status Reporter

---

## 4. Layer Architecture

### 4.1 Clean Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  (API Routes, Middleware, Schemas, Controllers)              │
└───────────────────────────┬─────────────────────────────────┘
                            │ Depends On
┌───────────────────────────▼─────────────────────────────────┐
│                   Application Layer                          │
│  (Use Cases, DTOs, Orchestration)                            │
└───────────────────────────┬─────────────────────────────────┘
                            │ Depends On
┌───────────────────────────▼─────────────────────────────────┐
│                     Domain Layer                             │
│  (Entities, Value Objects, Interfaces, Services)             │
└───────────────────────────┬─────────────────────────────────┘
                            │ Implemented By
┌───────────────────────────▼─────────────────────────────────┐
│                 Infrastructure Layer                         │
│  (AI Providers, Vector DB, Repositories, External APIs)      │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Layer Responsibilities

#### 4.2.1 Domain Layer (Innermost)
**Dependencies:** None (Pure Python)

**Contains:**
- Business entities (Product, Embedding, SearchResult)
- Value objects (ModelName, EmbeddingVector, ConfidenceScore)
- Domain interfaces (abstract base classes)
- Domain services (business logic)

**Rules:**
- No external framework dependencies
- No database dependencies
- No I/O operations
- Pure business logic only

#### 4.2.2 Application Layer
**Dependencies:** Domain Layer

**Contains:**
- Use case implementations
- DTOs (Data Transfer Objects)
- Application interfaces
- Orchestration logic

**Rules:**
- Depends only on domain interfaces
- No infrastructure details
- No database queries
- Coordinates domain objects

#### 4.2.3 Infrastructure Layer
**Dependencies:** Domain Layer

**Contains:**
- AI provider implementations
- Vector database implementations
- Repository implementations
- External service integrations
- Database connections

**Rules:**
- Implements domain interfaces
- Handles all I/O operations
- Manages external dependencies
- Platform-specific code

#### 4.2.4 Presentation Layer (Outermost)
**Dependencies:** Application Layer

**Contains:**
- API routes and endpoints
- Middleware
- Request/Response schemas
- Controllers
- Authentication handlers

**Rules:**
- Depends on application use cases
- Handles HTTP concerns
- Input validation
- Response formatting

### 4.3 Dependency Rule

**Critical Rule:** Dependencies point inward only. Outer layers can depend on inner layers, but inner layers never depend on outer layers.

```
Presentation → Application → Domain ← Infrastructure
```

---

## 5. Domain Architecture

### 5.1 Domain Entities

#### 5.1.1 Product Entity
```python
class Product:
    - product_id: str
    - site_id: str
    - title: str
    - description: str
    - image_urls: List[str]
    - embedding: EmbeddingVector
    - metadata: Dict
    - created_at: datetime
    - updated_at: datetime
    - indexed_at: datetime
```

**Responsibilities:**
- Represent a product in the system
- Manage product metadata
- Track indexing status

#### 5.1.2 Embedding Entity
```python
class Embedding:
    - embedding_id: str
    - product_id: str
    - vector: EmbeddingVector
    - model_name: ModelName
    - dimensions: int
    - created_at: datetime
```

**Responsibilities:**
- Store vector representation
- Track model used
- Manage embedding lifecycle

#### 5.1.3 SearchResult Entity
```python
class SearchResult:
    - product_id: str
    - similarity_score: ConfidenceScore
    - product_data: Dict
    - rank: int
```

**Responsibilities:**
- Represent search results
- Store similarity metrics
- Track ranking

#### 5.1.4 QueueJob Entity
```python
class QueueJob:
    - job_id: str
    - job_type: JobType
    - payload: Dict
    - status: JobStatus
    - priority: int
    - retry_count: int
    - max_retries: int
    - created_at: datetime
    - started_at: datetime
    - completed_at: datetime
    - error: str
```

**Responsibilities:**
- Track background jobs
- Manage job lifecycle
- Handle retry logic

#### 5.1.5 ApiKey Entity
```python
class ApiKey:
    - key_id: str
    - key_hash: ApiKeyHash
    - site_id: str
    - name: str
    - permissions: List[str]
    - rate_limit: int
    - ip_whitelist: List[str]
    - is_active: bool
    - created_at: datetime
    - expires_at: datetime
```

**Responsibilities:**
- Manage API authentication
- Track permissions
- Enforce rate limits

### 5.2 Value Objects

#### 5.2.1 ModelName
```python
class ModelName:
    - value: str
    - version: str
    - provider: str
```

**Properties:**
- Immutable
- Self-validating
- Comparable

#### 5.2.2 EmbeddingVector
```python
class EmbeddingVector:
    - values: np.ndarray
    - dimensions: int
    - model: ModelName
```

**Properties:**
- Immutable
- Type-safe
- Serialization support

#### 5.2.3 ConfidenceScore
```python
class ConfidenceScore:
    - value: float
    - threshold: float
```

**Properties:**
- Range: 0.0 to 1.0
- Comparable
- Threshold validation

#### 5.2.4 ApiKeyHash
```python
class ApiKeyHash:
    - hash: str
    - algorithm: str
```

**Properties:**
- Secure hashing
- One-way only
- Algorithm agnostic

### 5.3 Domain Interfaces

#### 5.3.1 AI Provider Interface
```python
class AIProvider(ABC):
    @abstractmethod
    def generate_embedding(self, image: Image) -> EmbeddingVector:
        pass
    
    @abstractmethod
    def generate_embeddings_batch(self, images: List[Image]) -> List[EmbeddingVector]:
        pass
    
    @abstractmethod
    def get_model_info(self) -> ModelInfo:
        pass
    
    @abstractmethod
    def load_model(self):
        pass
    
    @abstractmethod
    def unload_model(self):
        pass
```

#### 5.3.2 Vector Store Interface
```python
class VectorStore(ABC):
    @abstractmethod
    def add_vectors(self, vectors: List[Tuple[str, EmbeddingVector]]) -> None:
        pass
    
    @abstractmethod
    def search(self, query_vector: EmbeddingVector, limit: int, 
               filter_dict: Dict) -> List[SearchResult]:
        pass
    
    @abstractmethod
    def delete_vectors(self, product_ids: List[str]) -> None:
        pass
    
    @abstractmethod
    def get_stats(self) -> VectorStoreStats:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass
```

#### 5.3.3 Repository Interface
```python
class Repository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
    
    @abstractmethod
    def exists(self, id: str) -> bool:
        pass
```

#### 5.3.4 Queue Interface
```python
class Queue(ABC, Generic[T]):
    @abstractmethod
    def enqueue(self, job: T, priority: int = 0) -> str:
        pass
    
    @abstractmethod
    def dequeue(self) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_job(self, job_id: str) -> Optional[T]:
        pass
    
    @abstractmethod
    def update_job_status(self, job_id: str, status: JobStatus) -> None:
        pass
    
    @abstractmethod
    def get_queue_stats(self) -> QueueStats:
        pass
```

#### 5.3.5 Cache Interface
```python
class Cache(ABC, Generic[K, V]):
    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        pass
    
    @abstractmethod
    def set(self, key: K, value: V, ttl: int = None) -> None:
        pass
    
    @abstractmethod
    def delete(self, key: K) -> bool:
        pass
    
    @abstractmethod
    def exists(self, key: K) -> bool:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass
```

### 5.4 Domain Services

#### 5.4.1 Embedding Service
```python
class EmbeddingService:
    - ai_provider: AIProvider
    - cache: EmbeddingCache
    - validator: ValidationService
    
    def generate_embedding(self, image: Image) -> EmbeddingVector:
        # Check cache
        # Validate image
        # Generate embedding
        # Cache result
        # Return embedding
```

#### 5.4.2 Search Service
```python
class SearchService:
    - vector_store: VectorStore
    - embedding_service: EmbeddingService
    - cache: Cache
    
    def search_similar(self, query: SearchQuery) -> SearchResults:
        # Generate query embedding
        # Check cache
        # Search vector store
        # Rank results
        # Cache results
        # Return results
```

#### 5.4.3 Validation Service
```python
class ValidationService:
    def validate_image(self, image: Image) -> ValidationResult:
        # Check format
        # Check size
        # Check dimensions
        # Check for corruption
```

---

## 6. Service Architecture

### 6.1 Service Types

#### 6.1.1 Domain Services
- **Purpose:** Contain business logic that doesn't naturally belong to an entity
- **Location:** Domain Layer
- **Dependencies:** Only domain entities and interfaces
- **Examples:** EmbeddingService, SearchService, ValidationService

#### 6.1.2 Application Services
- **Purpose:** Orchestrate use cases and coordinate domain services
- **Location:** Application Layer
- **Dependencies:** Domain services and interfaces
- **Examples:** SearchImageUseCase, IndexProductUseCase

#### 6.1.3 Infrastructure Services
- **Purpose:** Implement technical concerns
- **Location:** Infrastructure Layer
- **Dependencies:** External libraries and frameworks
- **Examples:** EmailService, NotificationService, MetricsService

### 6.2 Service Communication

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Services                      │
│  (Use Case Orchestration)                                    │
└───────────────┬─────────────────────────┬───────────────────┘
                │                         │
    ┌───────────▼──────────┐   ┌─────────▼──────────┐
    │   Domain Services    │   │ Domain Interfaces  │
    │  (Business Logic)    │   │   (Contracts)       │
    └───────────┬──────────┘   └─────────┬──────────┘
                │                         │
                │    ┌────────────────────┘
                │    │
    ┌───────────▼──────────────────▼──────────┐
    │      Infrastructure Services            │
    │  (Technical Implementations)            │
    └─────────────────────────────────────────┘
```

### 6.3 Service Registry

All services are registered in a central service container for dependency injection.

```python
class ServiceContainer:
    - ai_providers: Dict[str, AIProvider]
    - vector_stores: Dict[str, VectorStore]
    - repositories: Dict[str, Repository]
    - caches: Dict[str, Cache]
    - queues: Dict[str, Queue]
    
    def register(self, interface, implementation)
    def resolve(self, interface)
    def configure(self)
```

---

## 7. AI Provider Architecture

### 7.1 Provider Abstraction

The AI module uses a provider pattern to support multiple AI models without code changes.

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Provider Interface                     │
│  (Abstract Base Class)                                       │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│ OpenCLIP       │  │ SigLIP      │  │ MobileNet       │
│ Provider       │  │ Provider    │  │ Provider        │
└────────────────┘  └─────────────┘  └─────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────▼────────┐
                    │ Provider       │
                    │ Factory        │
                    └────────────────┘
```

### 7.2 Provider Interface

```python
class AIProvider(ABC):
    """Base interface for all AI providers"""
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider name (e.g., 'openclip', 'siglip')"""
        pass
    
    @abstractmethod
    def get_supported_models(self) -> List[ModelInfo]:
        """Return list of supported models"""
        pass
    
    @abstractmethod
    def load_model(self, model_name: str) -> None:
        """Load specific model into memory"""
        pass
    
    @abstractmethod
    def unload_model(self) -> None:
        """Unload model from memory"""
        pass
    
    @abstractmethod
    def generate_embedding(self, image: Image) -> EmbeddingVector:
        """Generate embedding for single image"""
        pass
    
    @abstractmethod
    def generate_embeddings_batch(self, images: List[Image]) -> List[EmbeddingVector]:
        """Generate embeddings for multiple images"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> ModelInfo:
        """Get current model information"""
        pass
    
    @abstractmethod
    def warmup(self) -> None:
        """Warm up model for faster inference"""
        pass
```

### 7.3 Provider Implementations

#### 7.3.1 OpenCLIP Provider
```python
class OpenCLIPProvider(AIProvider):
    - model: OpenCLIPModel
    - preprocess: Callable
    - tokenizer: Callable
    
    def load_model(self, model_name: str):
        # Load OpenCLIP model
        # Load preprocessing
        # Warm up model
    
    def generate_embedding(self, image: Image) -> EmbeddingVector:
        # Preprocess image
        # Run inference
        # Normalize embedding
        # Return vector
```

**Supported Models:**
- ViT-B-32
- ViT-B-16
- ViT-L-14
- ViT-L-14-336
- RN50
- RN101

#### 7.3.2 SigLIP Provider
```python
class SigLIPProvider(AIProvider):
    - model: SigLIPModel
    - preprocess: Callable
    
    def load_model(self, model_name: str):
        # Load SigLIP model
        # Load preprocessing
    
    def generate_embedding(self, image: Image) -> EmbeddingVector:
        # Preprocess image
        # Run inference
        # Return normalized vector
```

**Supported Models:**
- SigLIP-B/16-384
- SigLIP-B/16-256
- SigLIP-L/16-256

#### 7.3.3 MobileNet Provider
```python
class MobileNetProvider(AIProvider):
    - model: MobileNetModel
    - preprocess: Callable
    
    def load_model(self, model_name: str):
        # Load MobileNet model
        # Load preprocessing
    
    def generate_embedding(self, image: Image) -> EmbeddingVector:
        # Preprocess image
        # Run inference
        # Return vector
```

**Supported Models:**
- MobileNetV2
- MobileNetV3-Small
- MobileNetV3-Large

### 7.4 Provider Factory

```python
class AIProviderFactory:
    _providers: Dict[str, Type[AIProvider]] = {
        'openclip': OpenCLIPProvider,
        'siglip': SigLIPProvider,
        'mobilenet': MobileNetProvider
    }
    
    def create_provider(self, provider_type: str, config: Dict) -> AIProvider:
        provider_class = self._providers.get(provider_type)
        if not provider_class:
            raise UnsupportedProviderError(provider_type)
        return provider_class(config)
    
    def register_provider(self, name: str, provider_class: Type[AIProvider]):
        self._providers[name] = provider_class
```

### 7.5 Model Management

```python
class ModelManager:
    - loaded_models: Dict[str, AIProvider]
    - model_configs: Dict[str, ModelConfig]
    - cache: Cache
    
    def get_provider(self, model_name: str) -> AIProvider:
        # Check if model loaded
        # Load if necessary
        # Return provider
    
    def unload_provider(self, model_name: str):
        # Unload from memory
        # Clear cache
    
    def switch_model(self, model_name: str):
        # Unload current
        # Load new
        # Update config
```

### 7.6 Provider Configuration

```yaml
ai_providers:
  default: openclip
  
  providers:
    openclip:
      enabled: true
      models:
        - name: ViT-B-32
          dimensions: 512
          preprocessing:
            resize: 224
            normalize: true
          batch_size: 32
          warmup: true
      
      settings:
        device: auto  # auto, cpu, cuda
        precision: fp32  # fp32, fp16, int8
        cache_dir: /models/openclip
    
    siglip:
      enabled: true
      models:
        - name: SigLIP-B/16-384
          dimensions: 768
          preprocessing:
            resize: 384
            normalize: true
          batch_size: 16
      
      settings:
        device: auto
        precision: fp32
    
    mobilenet:
      enabled: true
      models:
        - name: MobileNetV3-Large
          dimensions: 960
          preprocessing:
            resize: 224
            normalize: true
          batch_size: 64
      
      settings:
        device: auto
        precision: fp32
```

---

## 8. Vector Database Architecture

### 8.1 Vector Store Abstraction

The system uses an abstraction layer to support multiple vector databases.

```
┌─────────────────────────────────────────────────────────────┐
│                  Vector Store Interface                      │
│  (Abstract Base Class)                                       │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│   FAISS        │  │ hnswlib     │  │ ChromaDB        │
│   Store        │  │ Store       │  │ Store           │
└────────────────┘  └─────────────┘  └─────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────▼────────┐
                    │ Vector Store   │
                    │ Factory        │
                    └────────────────┘
```

### 8.2 Vector Store Interface

```python
class VectorStore(ABC):
    """Base interface for all vector stores"""
    
    @abstractmethod
    def initialize(self, dimensions: int, metric: str = 'cosine') -> None:
        """Initialize vector store with dimensions and metric"""
        pass
    
    @abstractmethod
    def add_vectors(self, vectors: List[Tuple[str, EmbeddingVector, Dict]]) -> None:
        """
        Add vectors to store
        Args:
            vectors: List of (product_id, embedding, metadata) tuples
        """
        pass
    
    @abstractmethod
    def search(self, query_vector: EmbeddingVector, limit: int = 10,
               filter_dict: Dict = None) -> List[SearchResult]:
        """
        Search for similar vectors
        Args:
            query_vector: Query embedding
            limit: Maximum results
            filter_dict: Metadata filters
        Returns:
            List of search results sorted by similarity
        """
        pass
    
    @abstractmethod
    def delete_vectors(self, product_ids: List[str]) -> int:
        """Delete vectors by product IDs, return count deleted"""
        pass
    
    @abstractmethod
    def get_vector(self, product_id: str) -> Optional[Tuple[EmbeddingVector, Dict]]:
        """Get single vector by product ID"""
        pass
    
    @abstractmethod
    def get_stats(self) -> VectorStoreStats:
        """Get vector store statistics"""
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """Persist vector store to disk"""
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        """Load vector store from disk"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all vectors"""
        pass
    
    @abstractmethod
    def get_all_vectors(self) -> List[Tuple[str, EmbeddingVector]]:
        """Get all vectors (for backup/migration)"""
        pass
```

### 8.3 Vector Store Implementations

#### 8.3.1 FAISS Store
```python
class FAISSStore(VectorStore):
    - index: faiss.Index
    - id_map: Dict[int, str]  # FAISS index to product_id
    - metadata: Dict[str, Dict]  # product_id to metadata
    - dimensions: int
    - metric: str
    
    def initialize(self, dimensions: int, metric: str = 'cosine'):
        # Create FAISS index
        # Set metric (cosine, l2, inner_product)
        # Initialize id_map
    
    def add_vectors(self, vectors: List[Tuple[str, EmbeddingVector, Dict]]):
        # Convert to numpy arrays
        # Add to FAISS index
        # Update id_map and metadata
    
    def search(self, query_vector: EmbeddingVector, limit: int, filter_dict: Dict):
        # Convert query to numpy
        # Search FAISS index
        # Apply filters
        # Convert to SearchResults
```

**Characteristics:**
- Fastest for large datasets (>1M vectors)
- Excellent for batch operations
- Limited filtering capabilities
- Memory efficient

#### 8.3.2 hnswlib Store
```python
class HnswlibStore(VectorStore):
    - index: hnswlib.Index
    - id_map: Dict[int, str]
    - metadata: Dict[str, Dict]
    - dimensions: int
    
    def initialize(self, dimensions: int, metric: str = 'cosine'):
        # Create HNSW index
        # Set parameters (M, ef_construction)
    
    def add_vectors(self, vectors: List[Tuple[str, EmbeddingVector, Dict]]):
        # Add to HNSW index
        # Update mappings
    
    def search(self, query_vector: EmbeddingVector, limit: int, filter_dict: Dict):
        # Set ef_search parameter
        # Search index
        # Apply filters
```

**Characteristics:**
- Good balance of speed and accuracy
- Supports incremental updates
- Memory efficient
- Good for medium datasets (10K-1M)

#### 8.3.3 ChromaDB Store
```python
class ChromaDBStore(VectorStore):
    - client: chromadb.Client
    - collection: chromadb.Collection
    - dimensions: int
    
    def initialize(self, dimensions: int, metric: str = 'cosine'):
        # Create ChromaDB client
        # Create collection
    
    def add_vectors(self, vectors: List[Tuple[str, EmbeddingVector, Dict]]):
        # Add to ChromaDB collection
        # Store embeddings and metadata
    
    def search(self, query_vector: EmbeddingVector, limit: int, filter_dict: Dict):
        # Query ChromaDB
        # Apply metadata filters
        # Return results
```

**Characteristics:**
- Built-in metadata filtering
- Persistent storage
- Easy to use
- Good for small to medium datasets

### 8.4 Vector Store Factory

```python
class VectorStoreFactory:
    _stores: Dict[str, Type[VectorStore]] = {
        'faiss': FAISSStore,
        'hnswlib': HnswlibStore,
        'chromadb': ChromaDBStore
    }
    
    def create_store(self, store_type: str, config: Dict) -> VectorStore:
        store_class = self._stores.get(store_type)
        if not store_class:
            raise UnsupportedVectorStoreError(store_type)
        return store_class(config)
    
    def register_store(self, name: str, store_class: Type[VectorStore]):
        self._stores[name] = store_class
```

### 8.5 Vector Store Configuration

```yaml
vector_store:
  type: faiss  # faiss, hnswlib, chromadb
  
  settings:
    dimensions: 512  # Must match model output
    metric: cosine  # cosine, l2, inner_product
    
    faiss:
      index_type: IndexFlatIP  # IndexFlatIP, IndexIVFFlat, IndexHNSW
      normalize: true  # Normalize vectors for cosine similarity
    
    hnswlib:
      M: 16  # Number of connections
      ef_construction: 200
      ef_search: 50
    
    chromadb:
      persist_directory: /data/vector_db
      collection_name: product_embeddings
  
  backup:
    enabled: true
    path: /backups/vector_store
    schedule: "0 2 * * *"  # Daily at 2 AM
```

### 8.6 Vector Store Manager

```python
class VectorStoreManager:
    - store: VectorStore
    - backup_manager: BackupManager
    - stats_collector: StatsCollector
    
    def __init__(self, config: Dict):
        # Create store via factory
        # Initialize with config
        # Load existing data
    
    def add_product_embedding(self, product_id: str, embedding: EmbeddingVector, metadata: Dict):
        # Add to vector store
        # Update statistics
    
    def search_similar(self, query: EmbeddingVector, limit: int, filters: Dict) -> List[SearchResult]:
        # Search vector store
        # Apply filters
        # Return ranked results
    
    def delete_product_embeddings(self, product_ids: List[str]) -> int:
        # Delete from vector store
        # Return count
    
    def backup(self) -> str:
        # Backup vector store
        # Return backup path
    
    def restore(self, backup_path: str):
        # Restore from backup
```

---

## 9. API Architecture

### 9.1 API Design Principles

- **RESTful:** Follow REST principles
- **Versioned:** All endpoints under `/api/v1/`
- **Consistent:** Uniform response format
- **Documented:** OpenAPI/Swagger documentation
- **Secure:** Authentication and authorization on all endpoints
- **Validated:** Input validation on all requests
- **Rate Limited:** Protect against abuse

### 9.2 API Versioning Strategy

```
/api/v1/          # Current stable version
/api/v2/          # Future version (backward incompatible changes)
```

**Versioning Rules:**
- Major version changes for breaking changes
- Minor versions not used (use v1, v2, etc.)
- Deprecation period of 6 months minimum
- Backward compatibility maintained within version

### 9.3 API Endpoints

#### 9.3.1 Health Endpoints

```
GET  /api/v1/health              # Overall health check
GET  /api/v1/health/detailed     # Detailed health with component status
GET  /api/v1/health/ready        # Readiness probe (Kubernetes)
GET  /api/v1/health/live         # Liveness probe (Kubernetes)
```

#### 9.3.2 Search Endpoints

```
POST /api/v1/search/image                    # Search by image upload
POST /api/v1/search/url                      # Search by image URL
POST /api/v1/search/batch                    # Batch search
GET  /api/v1/search/history                  # Search history
GET  /api/v1/search/similar/{product_id}     # Find similar products
```

#### 9.3.3 Index Endpoints

```
POST /api/v1/index/product                   # Index single product
POST /api/v1/index/batch                     # Batch index products
POST /api/v1/index/reindex                   # Reindex all products
DELETE /api/v1/index/product/{product_id}    # Delete product embedding
POST /api/v1/index/refresh                   # Refresh index
```

#### 9.3.4 Admin Endpoints

```
GET    /api/v1/admin/stats                   # System statistics
GET    /api/v1/admin/queue                   # Queue status
POST   /api/v1/admin/queue/clear             # Clear queue
GET    /api/v1/admin/models                  # Available AI models
POST   /api/v1/admin/models/switch           # Switch AI model
GET    /api/v1/admin/logs                    # View logs
POST   /api/v1/admin/cache/clear             # Clear cache
GET    /api/v1/admin/vector-store/stats      # Vector store statistics
POST   /api/v1/admin/vector-store/backup     # Backup vector store
POST   /api/v1/admin/vector-store/restore    # Restore vector store
```

#### 9.3.5 Analytics Endpoints

```
GET /api/v1/analytics/usage                  # Usage statistics
GET /api/v1/analytics/performance            # Performance metrics
GET /api/v1/analytics/search                 # Search analytics
GET /api/v1/analytics/errors                 # Error statistics
GET /api/v1/analytics/reports                # Generate reports
```

### 9.4 API Request/Response Format

#### 9.4.1 Standard Response Format

```json
{
  "success": true,
  "data": {},
  "message": "Operation successful",
  "timestamp": "2026-07-18T15:30:00Z",
  "request_id": "uuid-v4"
}
```

#### 9.4.2 Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "image_url",
        "message": "Invalid URL format"
      }
    ]
  },
  "timestamp": "2026-07-18T15:30:00Z",
  "request_id": "uuid-v4"
}
```

#### 9.4.3 Pagination Format

```json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

### 9.5 API Middleware Stack

```
Request
  │
  ├─→ CORS Middleware
  ├─→ Security Headers Middleware
  ├─→ Rate Limiting Middleware
  ├─→ Authentication Middleware
  ├─→ IP Whitelist Middleware
  ├─→ Request Validation Middleware
  ├─→ Logging Middleware
  ├─→ Error Handling Middleware
  │
  └─→ Route Handler
```

### 9.6 API Rate Limiting

```python
class RateLimiter:
    - limits: Dict[str, RateLimit]
    - storage: Cache
    
    def check_limit(self, api_key: str, endpoint: str) -> RateLimitResult:
        # Get limit for API key
        # Check current usage
        # Return result
    
    def get_remaining(self, api_key: str, endpoint: str) -> int:
        # Get remaining requests
```

**Rate Limit Tiers:**

| Tier | Requests/Minute | Requests/Day | Features |
|------|----------------|--------------|----------|
| Free | 60 | 1,000 | Basic search, indexing |
| Pro | 300 | 10,000 | Batch operations, priority queue |
| Enterprise | 1,000 | 100,000 | Dedicated resources, SLA |

### 9.7 API Documentation

- **Format:** OpenAPI 3.0
- **Tool:** Swagger UI / ReDoc
- **Endpoint:** `/docs`, `/redoc`
- **Auto-generated:** From code annotations
- **Interactive:** Try-it-out functionality

---

## 10. Authentication Architecture

### 10.1 Authentication Methods

#### 10.1.1 API Key Authentication
```python
class APIKeyAuth:
    - repository: ApiKeyRepository
    - cache: Cache
    - rate_limiter: RateLimiter
    
    def authenticate(self, api_key: str) -> ApiKey:
        # Hash API key
        # Check cache
        # Validate against database
        # Check expiration
        # Check IP whitelist
        # Return API key details
```

**API Key Format:**
```
ss_ai_sk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Parts:**
- `ss_ai_sk`: Prefix identifying SS AI Server
- `live`: Environment (live/test)
- `xxxxxxxx...`: Random 32-character key

#### 10.1.2 JWT Authentication
```python
class JWTAuth:
    - secret_key: str
    - algorithm: str
    - expiration: int
    
    def create_token(self, user_id: str, permissions: List[str]) -> str:
        # Create JWT payload
        # Sign token
        # Return token
    
    def validate_token(self, token: str) -> TokenPayload:
        # Decode token
        # Verify signature
        # Check expiration
        # Return payload
```

**JWT Payload:**
```json
{
  "sub": "user_id",
  "permissions": ["search", "index", "admin"],
  "iat": 1234567890,
  "exp": 1234567890,
  "site_id": "site_123"
}
```

### 10.2 Authentication Flow

```
Client Request
  │
  ├─→ Extract API Key / JWT from headers
  │
  ├─→ Validate credentials
  │   ├─→ Check cache
  │   ├─→ Check database
  │   └─→ Verify permissions
  │
  ├─→ Check rate limits
  │
  ├─→ Check IP whitelist
  │
  └─→ Attach user context to request
```

### 10.3 Permission System

```python
class Permission:
    SEARCH = "search"
    INDEX = "index"
    BATCH_INDEX = "batch_index"
    ADMIN = "admin"
    ANALYTICS = "analytics"
    DELETE = "delete"

class PermissionChecker:
    def has_permission(self, api_key: ApiKey, permission: str) -> bool:
        return permission in api_key.permissions
```

### 10.4 IP Whitelist

```python
class IPWhitelist:
    - whitelist: List[str]
    - cache: Cache
    
    def is_allowed(self, api_key: ApiKey, ip_address: str) -> bool:
        # If whitelist empty, allow all
        # Check if IP in whitelist
        # Return result
```

### 10.5 Security Headers

```python
class SecurityHeaders:
    def get_headers(self) -> Dict[str, str]:
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
```

---

## 11. Queue Architecture

### 11.1 Queue System Design

The queue system handles background processing for CPU-intensive operations like embedding generation and batch indexing.

```
┌─────────────────────────────────────────────────────────────┐
│                      Queue System                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ High Priority│  │ Normal Queue │  │ Low Priority │     │
│  │   Queue      │  │              │  │   Queue      │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │              │
│         └─────────────────┼─────────────────┘              │
│                           │                                │
│                  ┌────────▼────────┐                       │
│                  │  Job Scheduler  │                       │
│                  └────────┬────────┘                       │
│                           │                                │
│                  ┌────────▼────────┐                       │
│                  │  Worker Pool    │                       │
│                  │  ┌──────────┐   │                       │
│                  │  │ Worker 1 │   │                       │
│                  │  │ Worker 2 │   │                       │
│                  │  │ Worker N │   │                       │
│                  │  └──────────┘   │                       │
│                  └─────────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 11.2 Queue Interface

```python
class Queue(ABC, Generic[T]):
    @abstractmethod
    def enqueue(self, job: T, priority: int = 0) -> str:
        """Add job to queue, return job ID"""
        pass
    
    @abstractmethod
    def dequeue(self) -> Optional[T]:
        """Get next job from queue"""
        pass
    
    @abstractmethod
    def get_job(self, job_id: str) -> Optional[T]:
        """Get job by ID"""
        pass
    
    @abstractmethod
    def update_job_status(self, job_id: str, status: JobStatus, 
                         result: Dict = None, error: str = None) -> None:
        """Update job status"""
        pass
    
    @abstractmethod
    def retry_job(self, job_id: str) -> bool:
        """Retry failed job"""
        pass
    
    @abstractmethod
    def get_queue_stats(self) -> QueueStats:
        """Get queue statistics"""
        pass
    
    @abstractmethod
    def clear_queue(self, job_type: str = None) -> int:
        """Clear queue, optionally by job type"""
        pass
```

### 11.3 Job Types

```python
class JobType(Enum):
    EMBEDDING_GENERATION = "embedding_generation"
    BATCH_INDEXING = "batch_indexing"
    REINDEXING = "reindexing"
    DELETE_EMBEDDINGS = "delete_embeddings"
    DUPLICATE_DETECTION = "duplicate_detection"
    MODEL_WARMUP = "model_warmup"
    BACKUP = "backup"
    CLEANUP = "cleanup"
```

### 11.4 Job States

```python
class JobStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"
```

### 11.5 Queue Implementations

#### 11.5.1 Redis Queue
```python
class RedisQueue(Queue):
    - redis: Redis
    - queue_prefix: str
    
    def enqueue(self, job: QueueJob, priority: int = 0) -> str:
        # Serialize job
        # Add to priority queue
        # Return job ID
    
    def dequeue(self) -> Optional[QueueJob]:
        # Pop from queue
        # Deserialize job
        # Return job
```

**Characteristics:**
- Fast in-memory queue
- Supports priority queues
- Persistent with Redis AOF/RDB
- Good for single-server deployments

#### 11.5.2 Celery Queue
```python
class CeleryQueue(Queue):
    - celery_app: Celery
    - broker_url: str
    
    def enqueue(self, job: QueueJob, priority: int = 0) -> str:
        # Create Celery task
        # Send to broker
        # Return task ID
```

**Characteristics:**
- Distributed task queue
- Supports multiple brokers (Redis, RabbitMQ)
- Built-in retry and scheduling
- Good for multi-worker deployments

### 11.6 Job Priority System

```python
class PriorityQueue:
    - queues: Dict[int, Queue]  # priority -> queue
    
    def enqueue(self, job: QueueJob, priority: int = 0) -> str:
        # Clamp priority to valid range
        # Add to appropriate queue
        # Return job ID
    
    def dequeue(self) -> Optional[QueueJob]:
        # Check high priority first
        # Then normal
        # Then low priority
        # Return first available job
```

**Priority Levels:**
- 3: Critical (system health checks)
- 2: High (user-initiated operations)
- 1: Normal (background tasks)
- 0: Low (cleanup, analytics)

### 11.7 Retry Strategy

```python
class RetryStrategy:
    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_delay: int = 1  # seconds
    
    def get_next_retry(self, retry_count: int) -> int:
        delay = self.initial_delay * (self.backoff_factor ** retry_count)
        return min(delay, 300)  # Max 5 minutes
```

**Retry Rules:**
- Exponential backoff
- Maximum 3 retries
- Retry on transient errors only
- No retry on validation errors

### 11.8 Queue Configuration

```yaml
queue:
  type: redis  # redis, celery
  
  redis:
    host: localhost
    port: 6379
    db: 0
    password: null
    prefix: ss_ai_queue
  
  celery:
    broker_url: redis://localhost:6379/0
    result_backend: redis://localhost:6379/1
    task_serializer: json
    result_serializer: json
  
  settings:
    max_retries: 3
    retry_backoff: 2.0
    job_timeout: 3600  # 1 hour
    result_expiry: 86400  # 24 hours
    worker_concurrency: 4
```

---

## 12. Worker Architecture

### 12.1 Worker System Design

Workers process background jobs from the queue system.

```
┌─────────────────────────────────────────────────────────────┐
│                    Worker Manager                            │
│  (Orchestrates all workers)                                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│ Embedding      │  │ Batch       │  │ Cleanup         │
│ Worker         │  │ Worker      │  │ Worker          │
└────────────────┘  └─────────────┘  └─────────────────┘
```

### 12.2 Worker Base Class

```python
class BaseWorker(ABC):
    - queue: Queue
    - logger: Logger
    - running: bool
    - worker_id: str
    
    @abstractmethod
    def process_job(self, job: QueueJob) -> JobResult:
        """Process a single job"""
        pass
    
    @abstractmethod
    def get_job_type(self) -> JobType:
        """Return job type this worker handles"""
        pass
    
    def start(self):
        """Start worker loop"""
        self.running = True
        while self.running:
            job = self.queue.dequeue()
            if job:
                self.process_job(job)
            else:
                time.sleep(1)
    
    def stop(self):
        """Stop worker gracefully"""
        self.running = False
    
    def handle_error(self, job: QueueJob, error: Exception) -> None:
        """Handle job processing error"""
        # Log error
        # Update job status
        # Retry if applicable
```

### 12.3 Worker Implementations

#### 12.3.1 Embedding Worker
```python
class EmbeddingWorker(BaseWorker):
    - ai_provider: AIProvider
    - product_repository: ProductRepository
    - vector_store: VectorStore
    - cache: EmbeddingCache
    
    def get_job_type(self) -> JobType:
        return JobType.EMBEDDING_GENERATION
    
    def process_job(self, job: QueueJob) -> JobResult:
        # Extract product_id from job
        # Load product from repository
        # Download/load image
        # Generate embedding
        # Store in vector store
        # Update product status
        # Return result
```

**Responsibilities:**
- Generate embeddings for single products
- Handle image loading and preprocessing
- Store embeddings in vector database
- Update product status

#### 12.3.2 Batch Worker
```python
class BatchWorker(BaseWorker):
    - ai_provider: AIProvider
    - product_repository: ProductRepository
    - vector_store: VectorStore
    - batch_size: int
    
    def get_job_type(self) -> JobType:
        return JobType.BATCH_INDEXING
    
    def process_job(self, job: QueueJob) -> JobResult:
        # Extract batch parameters
        # Load products in batches
        # Generate embeddings in batch
        # Store in vector store
        # Update progress
        # Return result
```

**Responsibilities:**
- Process batch indexing jobs
- Optimize for throughput
- Handle large datasets
- Report progress

#### 12.3.3 Cleanup Worker
```python
class CleanupWorker(BaseWorker):
    - product_repository: ProductRepository
    - vector_store: VectorStore
    - log_retention_days: int
    
    def get_job_type(self) -> JobType:
        return JobType.CLEANUP
    
    def process_job(self, job: QueueJob) -> JobResult:
        # Clean old logs
        # Clean expired cache entries
        # Clean failed jobs
        # Clean orphaned embeddings
        # Return result
```

**Responsibilities:**
- Clean old logs
- Remove expired cache entries
- Clean failed jobs
- Remove orphaned data

### 12.4 Worker Manager

```python
class WorkerManager:
    - workers: Dict[JobType, BaseWorker]
    - queue: Queue
    - logger: Logger
    
    def register_worker(self, job_type: JobType, worker: BaseWorker):
        self.workers[job_type] = worker
    
    def start_all_workers(self):
        for worker in self.workers.values():
            worker.start()
    
    def stop_all_workers(self):
        for worker in self.workers.values():
            worker.stop()
    
    def get_worker_stats(self) -> Dict[JobType, WorkerStats]:
        return {
            job_type: worker.get_stats()
            for job_type, worker in self.workers.items()
        }
```

### 12.5 Worker Configuration

```yaml
workers:
  embedding:
    enabled: true
    concurrency: 2
    batch_size: 32
    timeout: 300  # 5 minutes per job
  
  batch:
    enabled: true
    concurrency: 1
    batch_size: 100
    timeout: 3600  # 1 hour per job
  
  cleanup:
    enabled: true
    schedule: "0 3 * * *"  # Daily at 3 AM
    log_retention_days: 30
    cache_retention_days: 7
```

---

## 13. Embedding Pipeline

### 13.1 Pipeline Overview

The embedding pipeline transforms images into vector representations.

```
┌─────────────────────────────────────────────────────────────┐
│                    Embedding Pipeline                        │
└─────────────────────────────────────────────────────────────┘

Input Image
    │
    ▼
┌─────────────────┐
│ Image Validator │ ──→ Validate format, size, dimensions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Image Loader    │ ──→ Load from URL, upload, or path
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Preprocessor    │ ──→ Resize, normalize, augment
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Provider    │ ──→ Generate embedding vector
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Postprocessor  │ ──→ Normalize, validate dimensions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cache Layer    │ ──→ Cache embedding for reuse
└────────┬────────┘
         │
         ▼
Embedding Vector
```

### 13.2 Pipeline Stages

#### 13.2.1 Image Validation
```python
class ImageValidator:
    def validate(self, image: Image) -> ValidationResult:
        # Check format (JPEG, PNG, WebP)
        # Check file size (max 10MB)
        # Check dimensions (min 32x32, max 10000x10000)
        # Check for corruption
        # Check for malicious content
        return ValidationResult(valid=True/False, errors=[])
```

**Validation Rules:**
- Supported formats: JPEG, PNG, WebP, GIF
- Max file size: 10MB
- Min dimensions: 32x32
- Max dimensions: 10000x10000
- Must be valid image file
- No executable content

#### 13.2.2 Image Loading
```python
class ImageLoader:
    def load_from_url(self, url: str) -> Image:
        # Download image
        # Validate content type
        # Load into memory
        # Return Image object
    
    def load_from_upload(self, file: UploadFile) -> Image:
        # Read uploaded file
        # Validate format
        # Load into memory
        # Return Image object
    
    def load_from_path(self, path: str) -> Image:
        # Load from filesystem
        # Validate file
        # Return Image object
```

#### 13.2.3 Image Preprocessing
```python
class ImagePreprocessor:
    - target_size: Tuple[int, int]
    - normalize: bool
    - mean: List[float]
    - std: List[float]
    
    def preprocess(self, image: Image) -> torch.Tensor:
        # Resize to target size
        # Convert to tensor
        # Normalize if required
        # Add batch dimension
        # Return tensor
```

**Preprocessing Steps:**
1. Resize to model input size
2. Convert to RGB (if needed)
3. Convert to tensor
4. Normalize (if required)
5. Add batch dimension

#### 13.2.4 Embedding Generation
```python
class EmbeddingGenerator:
    - ai_provider: AIProvider
    - cache: EmbeddingCache
    
    def generate(self, image: Image) -> EmbeddingVector:
        # Check cache
        # Generate embedding
        # Cache result
        # Return embedding
```

#### 13.2.5 Postprocessing
```python
class EmbeddingPostprocessor:
    def postprocess(self, embedding: EmbeddingVector) -> EmbeddingVector:
        # Normalize vector (L2 norm)
        # Validate dimensions
        # Check for NaN/Inf
        # Return processed embedding
```

### 13.3 Pipeline Orchestration

```python
class EmbeddingPipeline:
    - validator: ImageValidator
    - loader: ImageLoader
    - preprocessor: ImagePreprocessor
    - generator: EmbeddingGenerator
    - postprocessor: EmbeddingPostprocessor
    - cache: EmbeddingCache
    
    def process(self, image_source: ImageSource) -> EmbeddingVector:
        # Validate image
        # Load image
        # Preprocess
        # Generate embedding
        # Postprocess
        # Cache result
        # Return embedding
```

### 13.4 Batch Processing

```python
class BatchEmbeddingPipeline:
    - pipeline: EmbeddingPipeline
    - batch_size: int
    
    def process_batch(self, images: List[Image]) -> List[EmbeddingVector]:
        # Split into batches
        # Process each batch
        # Combine results
        # Return embeddings
```

**Batch Optimization:**
- Process multiple images in single inference
- Reduce overhead
- Maximize GPU utilization
- Handle memory efficiently

### 13.5 Pipeline Configuration

```yaml
embedding_pipeline:
  validation:
    max_file_size: 10485760  # 10MB
    min_dimensions: [32, 32]
    max_dimensions: [10000, 10000]
    allowed_formats: [jpeg, png, webp, gif]
  
  preprocessing:
    target_size: [224, 224]
    normalize: true
    mean: [0.485, 0.456, 0.406]
    std: [0.229, 0.224, 0.225]
  
  generation:
    batch_size: 32
    use_cache: true
    cache_ttl: 86400  # 24 hours
  
  postprocessing:
    normalize: true
    validate_dimensions: true
```

---

## 14. Search Pipeline

### 14.1 Pipeline Overview

The search pipeline processes search queries and returns similar products.

```
┌─────────────────────────────────────────────────────────────┐
│                     Search Pipeline                          │
└─────────────────────────────────────────────────────────────┘

Search Query (Image/URL)
    │
    ▼
┌─────────────────┐
│ Query Validator │ ──→ Validate input
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Query Embedding │ ──→ Generate embedding for query
│   Generator     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cache Check    │ ──→ Check if result cached
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vector Search   │ ──→ Search vector database
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Filter & Rank  │ ──→ Apply filters, rank results
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cache Result   │ ──→ Cache search results
└────────┬────────┘
         │
         ▼
Search Results
```

### 14.2 Pipeline Stages

#### 14.2.1 Query Validation
```python
class SearchQueryValidator:
    def validate(self, query: SearchQuery) -> ValidationResult:
        # Check image/URL provided
        # Check limit (max 100)
        # Check threshold (0.0 to 1.0)
        # Validate filters
        return ValidationResult(valid=True/False, errors=[])
```

#### 14.2.2 Query Embedding Generation
```python
class QueryEmbeddingGenerator:
    - embedding_pipeline: EmbeddingPipeline
    - cache: Cache
    
    def generate(self, query: SearchQuery) -> EmbeddingVector:
        # Check cache
        # Generate embedding
        # Cache result
        # Return embedding
```

#### 14.2.3 Vector Search
```python
class VectorSearcher:
    - vector_store: VectorStore
    
    def search(self, embedding: EmbeddingVector, limit: int, 
               threshold: float, filters: Dict) -> List[SearchResult]:
        # Search vector store
        # Apply threshold filter
        # Apply metadata filters
        # Return results
```

#### 14.2.4 Result Ranking
```python
class ResultRanker:
    def rank(self, results: List[SearchResult], 
             strategy: RankingStrategy) -> List[SearchResult]:
        # Apply ranking algorithm
        # Sort by score
        # Apply diversity filter
        # Return ranked results
```

**Ranking Strategies:**
- Similarity (by score)
- Recency (by date)
- Popularity (by views)
- Combined (weighted score)

#### 14.2.5 Result Filtering
```python
class ResultFilter:
    def filter(self, results: List[SearchResult], 
               filters: SearchFilters) -> List[SearchResult]:
        # Filter by category
        # Filter by price range
        # Filter by date range
        # Filter by site
        # Return filtered results
```

### 14.3 Search Pipeline Orchestration

```python
class SearchPipeline:
    - validator: SearchQueryValidator
    - embedding_generator: QueryEmbeddingGenerator
    - vector_searcher: VectorSearcher
    - ranker: ResultRanker
    - filter: ResultFilter
    - cache: Cache
    
    def search(self, query: SearchQuery) -> SearchResponse:
        # Validate query
        # Generate embedding
        # Check cache
        # Search vectors
        # Filter results
        # Rank results
        # Cache results
        # Return response
```

### 14.4 Search Configuration

```yaml
search:
  default_limit: 20
  max_limit: 100
  default_threshold: 0.7
  min_threshold: 0.0
  max_threshold: 1.0
  
  ranking:
    strategy: similarity  # similarity, recency, popularity, combined
    weights:
      similarity: 0.7
      recency: 0.2
      popularity: 0.1
  
  filters:
    enabled: true
    allowed_filters: [category, price_range, date_range, site_id]
  
  cache:
    enabled: true
    ttl: 300  # 5 minutes
    key_prefix: "search:"
```

---

## 15. Index Pipeline

### 15.1 Pipeline Overview

The index pipeline processes and stores product embeddings.

```
┌─────────────────────────────────────────────────────────────┐
│                     Index Pipeline                           │
└─────────────────────────────────────────────────────────────┘

Product Data
    │
    ▼
┌─────────────────┐
│  Validation     │ ──→ Validate product data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Image Processing│ ──→ Process product images
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Embedding Gen   │ ──→ Generate embeddings
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vector Store    │ ──→ Store in vector database
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Metadata Store  │ ──→ Store in relational database
└────────┬────────┘
         │
         ▼
Indexed Product
```

### 15.2 Pipeline Stages

#### 15.2.1 Product Validation
```python
class ProductValidator:
    def validate(self, product: Product) -> ValidationResult:
        # Check required fields
        # Validate product_id
        # Validate site_id
        # Check image URLs
        # Validate metadata
        return ValidationResult(valid=True/False, errors=[])
```

#### 15.2.2 Image Processing
```python
class ProductImageProcessor:
    - image_loader: ImageLoader
    - embedding_pipeline: EmbeddingPipeline
    
    def process_images(self, product: Product) -> List[EmbeddingVector]:
        # Load all images
        # Generate embeddings
        # Aggregate embeddings (average, max, etc.)
        # Return embedding
```

**Image Aggregation Strategies:**
- Average: Mean of all image embeddings
- Max: Maximum pooling
- First: Use first image only
- Weighted: Weight by image quality

#### 15.2.3 Vector Storage
```python
class VectorStorage:
    - vector_store: VectorStore
    - product_repository: ProductRepository
    
    def store(self, product: Product, embedding: EmbeddingVector):
        # Store in vector database
        # Update product record
        # Update index timestamp
```

#### 15.2.4 Metadata Storage
```python
class MetadataStorage:
    - repository: ProductRepository
    
    def store(self, product: Product):
        # Store product metadata
        # Update indexing status
        # Store timestamps
```

### 15.3 Index Pipeline Orchestration

```python
class IndexPipeline:
    - validator: ProductValidator
    - image_processor: ProductImageProcessor
    - vector_storage: VectorStorage
    - metadata_storage: MetadataStorage
    
    def index_product(self, product: Product) -> IndexResult:
        # Validate product
        # Process images
        # Generate embedding
        # Store vector
        # Store metadata
        # Return result
```

### 15.4 Batch Indexing

```python
class BatchIndexPipeline:
    - index_pipeline: IndexPipeline
    - batch_size: int
    - progress_tracker: ProgressTracker
    
    def index_batch(self, products: List[Product], 
                    callback: Callable = None) -> BatchIndexResult:
        # Split into batches
        # Process each batch
        # Track progress
        # Handle errors
        # Return results
```

### 15.5 Index Configuration

```yaml
index_pipeline:
  validation:
    required_fields: [product_id, site_id, image_urls]
    optional_fields: [title, description, price, category]
  
  image_processing:
    max_images_per_product: 10
    aggregation_strategy: average  # average, max, first, weighted
    skip_duplicates: true
  
  storage:
    store_metadata: true
    update_existing: true
    batch_size: 100
  
  error_handling:
    skip_invalid: true
    retry_failed: true
    max_retries: 3
```

---

## 16. Storage Architecture

### 16.1 Storage Strategy

The system uses multiple storage backends for different data types.

```
┌─────────────────────────────────────────────────────────────┐
│                    Storage Layer                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Relational  │  │   Vector     │  │    Cache     │     │
│  │   Database   │  │   Database   │  │   (Redis)    │     │
│  │  (PostgreSQL)│  │  (FAISS/etc) │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Object     │  │   Queue      │  │   File       │     │
│  │   Storage    │  │   (Redis)    │  │   Storage    │     │
│  │   (S3/etc)   │  │              │  │  (Local/S3)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 16.2 Storage Types

#### 16.2.1 Relational Database
**Purpose:** Store metadata, API keys, logs, configurations

**Schema:**
```sql
-- Products table
CREATE TABLE products (
    product_id VARCHAR(255) PRIMARY KEY,
    site_id VARCHAR(255) NOT NULL,
    title TEXT,
    description TEXT,
    image_urls JSONB,
    metadata JSONB,
    indexed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_site_id (site_id),
    INDEX idx_indexed_at (indexed_at)
);

-- API Keys table
CREATE TABLE api_keys (
    key_id VARCHAR(255) PRIMARY KEY,
    key_hash VARCHAR(255) NOT NULL,
    site_id VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    permissions JSONB,
    rate_limit INT,
    ip_whitelist JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    INDEX idx_site_id (site_id),
    INDEX idx_key_hash (key_hash)
);

-- Queue Jobs table
CREATE TABLE queue_jobs (
    job_id VARCHAR(255) PRIMARY KEY,
    job_type VARCHAR(100) NOT NULL,
    payload JSONB,
    status VARCHAR(50) NOT NULL,
    priority INT DEFAULT 0,
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error TEXT,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Search History table
CREATE TABLE search_history (
    search_id VARCHAR(255) PRIMARY KEY,
    api_key_id VARCHAR(255),
    query_type VARCHAR(50),
    results_count INT,
    processing_time_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_api_key_id (api_key_id),
    INDEX idx_created_at (created_at)
);

-- Analytics table
CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_type (event_type),
    INDEX idx_created_at (created_at)
);

-- Logs table
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    context JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_level (level),
    INDEX idx_created_at (created_at)
);
```

**Supported Databases:**
- PostgreSQL (production)
- SQLite (development)
- MySQL (optional)

#### 16.2.2 Vector Database
**Purpose:** Store and search embeddings

**Storage:**
- FAISS index files
- hnswlib index files
- ChromaDB files

**Backup:**
- Daily automated backups
- Backup before updates
- Point-in-time recovery

#### 16.2.3 Cache (Redis)
**Purpose:** Fast access to frequently used data

**Cache Keys:**
```
embedding:{hash}                    # Embedding cache
search:{query_hash}:{limit}         # Search results
api_key:{hash}                      # API key validation
model_info:{model_name}             # Model information
stats:{type}:{period}               # Statistics
```

**TTL Policies:**
- Embeddings: 24 hours
- Search results: 5 minutes
- API keys: 1 hour
- Model info: 6 hours
- Stats: 1 hour

#### 16.2.4 Object Storage
**Purpose:** Store images and backups

**Structure:**
```
bucket/
├── images/
│   ├── {site_id}/
│   │   ├── {product_id}_1.jpg
│   │   ├── {product_id}_2.jpg
│   │   └── ...
├── backups/
│   ├── vector_store/
│   │   ├── backup_2026-07-18.index
│   │   └── ...
│   └── database/
│       ├── backup_2026-07-18.sql
│       └── ...
└── temp/
    └── ...
```

**Supported Storage:**
- Local filesystem
- Amazon S3
- Google Cloud Storage
- Azure Blob Storage
- MinIO (self-hosted)

#### 16.2.5 Queue Storage
**Purpose:** Store background jobs

**Implementation:**
- Redis lists (for simple queues)
- Redis sorted sets (for priority queues)
- Celery with Redis/RabbitMQ broker

### 16.3 Storage Configuration

```yaml
storage:
  database:
    type: postgresql  # postgresql, sqlite, mysql
    host: localhost
    port: 5432
    database: ss_ai_server
    username: postgres
    password: ${DB_PASSWORD}
    pool_size: 20
    max_overflow: 10
  
  vector_store:
    type: faiss  # faiss, hnswlib, chromadb
    path: /data/vector_store
    backup:
      enabled: true
      path: /backups/vector_store
      schedule: "0 2 * * *"
  
  cache:
    type: redis
    host: localhost
    port: 6379
    db: 0
    password: ${REDIS_PASSWORD}
    prefix: ss_ai_cache
    ttl:
      embedding: 86400
      search: 300
      api_key: 3600
  
  object_storage:
    type: local  # local, s3, gcs, azure
    path: /data/storage
    s3:
      bucket: ss-ai-server
      region: us-east-1
      access_key: ${AWS_ACCESS_KEY}
      secret_key: ${AWS_SECRET_KEY}
  
  queue:
    type: redis
    host: localhost
    port: 6379
    db: 1
    password: ${REDIS_PASSWORD}
```

---

## 17. Cache Architecture

### 17.1 Cache Strategy

Multi-level caching for optimal performance.

```
┌─────────────────────────────────────────────────────────────┐
│                    Cache Hierarchy                           │
└─────────────────────────────────────────────────────────────┘

Request
    │
    ▼
┌─────────────────┐
│  L1: Memory     │ ──→ In-memory LRU cache (fastest)
│  Cache          │
└────────┬────────┘
         │ Miss
         ▼
┌─────────────────┐
│  L2: Redis      │ ──→ Distributed cache (fast)
│  Cache          │
└────────┬────────┘
         │ Miss
         ▼
┌─────────────────┐
│  L3: Database   │ ──→ Source of truth (slowest)
└─────────────────┘
```

### 17.2 Cache Layers

#### 17.2.1 L1: Memory Cache
```python
class MemoryCache:
    - cache: Dict[str, Tuple[Any, datetime]]
    - max_size: int
    - ttl: int
    
    def get(self, key: str) -> Optional[Any]:
        # Check if key exists
        # Check if expired
        # Return value or None
    
    def set(self, key: str, value: Any, ttl: int = None):
        # Add to cache
        # Evict if full (LRU)
```

**Characteristics:**
- Fastest access
- Limited size
- Per-process
- No persistence

#### 17.2.2 L2: Redis Cache
```python
class RedisCache:
    - redis: Redis
    - prefix: str
    
    def get(self, key: str) -> Optional[Any]:
        # Get from Redis
        # Deserialize
        # Return value
    
    def set(self, key: str, value: Any, ttl: int = None):
        # Serialize value
        # Set in Redis with TTL
```

**Characteristics:**
- Fast access
- Distributed
- Persistent
- Shared across processes

#### 17.2.3 L3: Database
```python
class DatabaseCache:
    - repository: Repository
    
    def get(self, key: str) -> Optional[Any]:
        # Query database
        # Return value
```

**Characteristics:**
- Slowest access
- Persistent
- Source of truth

### 17.3 Cache Policies

#### 17.3.1 Cache-Aside
```python
def get_with_cache(self, key: str, fetch_func: Callable) -> Any:
    # Check cache
    value = cache.get(key)
    if value:
        return value
    
    # Fetch from source
    value = fetch_func()
    
    # Update cache
    cache.set(key, value)
    
    return value
```

#### 17.3.2 Write-Through
```python
def set_with_cache(self, key: str, value: Any):
    # Update database
    database.save(key, value)
    
    # Update cache
    cache.set(key, value)
```

#### 17.3.3 Write-Behind
```python
def set_with_cache(self, key: str, value: Any):
    # Update cache immediately
    cache.set(key, value)
    
    # Queue database update
    queue.enqueue(DatabaseUpdateJob(key, value))
```

### 17.4 Cache Invalidation

```python
class CacheInvalidator:
    - cache: Cache
    
    def invalidate_embedding(self, product_id: str):
        # Invalidate embedding cache
        # Invalidate search caches
    
    def invalidate_search(self, query_hash: str):
        # Invalidate search result cache
    
    def invalidate_all(self):
        # Clear all cache
```

**Invalidation Rules:**
- Invalidate on product update
- Invalidate on reindex
- Invalidate on model switch
- TTL-based expiration

### 17.5 Cache Configuration

```yaml
cache:
  enabled: true
  
  memory:
    enabled: true
    max_size: 1000  # items
    ttl: 300  # 5 minutes
  
  redis:
    enabled: true
    host: localhost
    port: 6379
    db: 0
    prefix: ss_ai_cache
    
    ttl:
      embedding: 86400  # 24 hours
      search: 300  # 5 minutes
      api_key: 3600  # 1 hour
      model_info: 21600  # 6 hours
  
  policies:
    embedding:
      strategy: cache-aside
      ttl: 86400
      max_size: 10000
    
    search:
      strategy: cache-aside
      ttl: 300
      max_size: 1000
```

---

## 18. Logging Architecture

### 18.1 Logging Strategy

Structured logging with multiple outputs and log levels.

```
┌─────────────────────────────────────────────────────────────┐
│                    Logging System                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Application Logs                                           │
│       │                                                     │
│       ├─→ Console (Development)                             │
│       ├─→ File (Local)                                      │
│       ├─→ ELK Stack (Production)                            │
│       ├─→ CloudWatch (AWS)                                  │
│       └─→ Datadog (Monitoring)                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 18.2 Log Levels

```python
class LogLevel(Enum):
    DEBUG = 10    # Detailed diagnostic information
    INFO = 20     # General informational messages
    WARNING = 30  # Warning messages
    ERROR = 40    # Error messages
    CRITICAL = 50 # Critical errors
```

**Usage Guidelines:**
- **DEBUG:** Development only, detailed diagnostics
- **INFO:** General operations, request tracking
- **WARNING:** Recoverable issues, deprecated usage
- **ERROR:** Failures, exceptions
- **CRITICAL:** System failures, data loss

### 18.3 Log Structure

```json
{
  "timestamp": "2026-07-18T15:30:00.123Z",
  "level": "INFO",
  "logger": "ss_ai_server.search",
  "message": "Search completed",
  "context": {
    "request_id": "uuid-v4",
    "api_key_id": "key_123",
    "site_id": "site_456",
    "processing_time_ms": 150,
    "results_count": 20,
    "model": "openclip-ViT-B-32"
  },
  "trace_id": "trace-uuid",
  "span_id": "span-uuid"
}
```

### 18.4 Log Types

#### 18.4.1 Request Logs
```python
class RequestLogger:
    def log_request(self, request: Request, response: Response, 
                    processing_time: float):
        # Log HTTP request
        # Include method, path, status
        # Include user context
        # Include processing time
```

**Logged Data:**
- HTTP method
- Endpoint
- Status code
- Processing time
- User ID / API key
- IP address
- User agent

#### 18.4.2 Error Logs
```python
class ErrorLogger:
    def log_error(self, error: Exception, context: Dict):
        # Log exception details
        # Include stack trace
        # Include context
        # Include request info
```

**Logged Data:**
- Exception type
- Error message
- Stack trace
- Request context
- User context
- Timestamp

#### 18.4.3 Audit Logs
```python
class AuditLogger:
    def log_action(self, action: str, user_id: str, 
                   resource: str, details: Dict):
        # Log security-relevant actions
        # Include user context
        # Include resource details
```

**Logged Actions:**
- Authentication attempts
- Authorization failures
- Data modifications
- Configuration changes
- Admin actions

#### 18.4.4 Performance Logs
```python
class PerformanceLogger:
    def log_metric(self, metric: str, value: float, 
                   tags: Dict[str, str]):
        # Log performance metrics
        # Include tags for filtering
```

**Logged Metrics:**
- Embedding generation time
- Search latency
- Queue processing time
- Database query time
- Cache hit rate

### 18.5 Log Aggregation

```python
class LogAggregator:
    - log_stores: List[LogStore]
    
    def log(self, level: LogLevel, message: str, context: Dict):
        # Create log entry
        # Send to all log stores
        # Handle failures gracefully
```

**Log Stores:**
- Console (development)
- File (local)
- Elasticsearch (ELK stack)
- CloudWatch (AWS)
- Datadog (monitoring)

### 18.6 Log Configuration

```yaml
logging:
  level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: json  # json, text
  
  outputs:
    console:
      enabled: true
      level: DEBUG
      format: text
    
    file:
      enabled: true
      level: INFO
      path: /logs/ss_ai_server.log
      rotation:
        max_size: 100MB
        backup_count: 10
    
    elasticsearch:
      enabled: false
      hosts: ["localhost:9200"]
      index: ss_ai_server_logs
      level: INFO
    
    cloudwatch:
      enabled: false
      log_group: /ss-ai-server/logs
      region: us-east-1
      level: INFO
  
  loggers:
    ss_ai_server:
      level: INFO
    ss_ai_server.ai:
      level: DEBUG
    ss_ai_server.search:
      level: INFO
    ss_ai_server.queue:
      level: INFO
```

---

## 19. Monitoring Architecture

### 19.1 Monitoring Strategy

Comprehensive monitoring for system health and performance.

```
┌─────────────────────────────────────────────────────────────┐
│                    Monitoring System                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Metrics Collection                                         │
│       │                                                     │
│       ├─→ System Metrics (CPU, Memory, Disk)                │
│       ├─→ Application Metrics (Requests, Errors)            │
│       ├─→ Business Metrics (Searches, Indexes)              │
│       └─→ AI Metrics (Model latency, Throughput)            │
│                                                             │
│       │                                                     │
│       ▼                                                     │
│  Metrics Storage (Prometheus / InfluxDB)                    │
│       │                                                     │
│       ▼                                                     │
│  Visualization (Grafana)                                    │
│       │                                                     │
│       ▼                                                     │
│  Alerting (Alertmanager / PagerDuty)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 19.2 Metrics Types

#### 19.2.1 System Metrics
```python
class SystemMetrics:
    - cpu_usage: float
    - memory_usage: float
    - disk_usage: float
    - network_io: float
    - process_count: int
```

**Metrics:**
- CPU usage percentage
- Memory usage (RSS, VMS)
- Disk usage and I/O
- Network I/O
- Process count
- Thread count

#### 19.2.2 Application Metrics
```python
class ApplicationMetrics:
    - request_count: Counter
    - request_latency: Histogram
    - error_count: Counter
    - active_connections: Gauge
```

**Metrics:**
- Request count (by endpoint, method, status)
- Request latency (p50, p95, p99)
- Error count (by type, endpoint)
- Active connections
- Queue length
- Worker utilization

#### 19.2.3 Business Metrics
```python
class BusinessMetrics:
    - searches_performed: Counter
    - products_indexed: Counter
    - embeddings_generated: Counter
    - batch_jobs_completed: Counter
```

**Metrics:**
- Searches performed (per hour/day)
- Products indexed (per hour/day)
- Embeddings generated (per hour/day)
- Batch jobs completed
- API key usage
- Search latency

#### 19.2.4 AI Metrics
```python
class AIMetrics:
    - model_load_time: Histogram
    - embedding_generation_time: Histogram
    - batch_processing_time: Histogram
    - model_memory_usage: Gauge
    - gpu_utilization: Gauge
```

**Metrics:**
- Model load time
- Embedding generation time (single/batch)
- Model memory usage
- GPU utilization (if available)
- Model inference throughput
- Cache hit rate

### 19.3 Health Checks

```python
class HealthChecker:
    - checks: Dict[str, HealthCheck]
    
    def register_check(self, name: str, check: HealthCheck):
        self.checks[name] = check
    
    def check_health(self) -> HealthStatus:
        results = {}
        for name, check in self.checks.items():
            results[name] = check.check()
        
        overall_status = self._determine_status(results)
        return HealthStatus(status=overall_status, checks=results)
```

**Health Checks:**
- Database connectivity
- Redis connectivity
- Vector store accessibility
- AI model loaded
- Disk space
- Memory availability
- Queue connectivity

### 19.4 Monitoring Configuration

```yaml
monitoring:
  enabled: true
  
  metrics:
    provider: prometheus  # prometheus, influxdb, datadog
    port: 9090
    path: /metrics
  
  health:
    enabled: true
    endpoint: /health
    detailed_endpoint: /health/detailed
  
  checks:
    database:
      enabled: true
      timeout: 5
    redis:
      enabled: true
      timeout: 5
    vector_store:
      enabled: true
      timeout: 5
    ai_model:
      enabled: true
      timeout: 10
    disk_space:
      enabled: true
      min_free_gb: 10
    memory:
      enabled: true
      max_usage_percent: 90
  
  alerts:
    enabled: true
    channels:
      - email
      - slack
      - pagerduty
    
    rules:
      - name: HighErrorRate
        condition: error_rate > 0.05
        duration: 5m
        severity: critical
      
      - name: HighLatency
        condition: p95_latency > 1000ms
        duration: 5m
        severity: warning
      
      - name: LowDiskSpace
        condition: disk_free < 10GB
        duration: 1m
        severity: critical
```

---

## 20. Analytics Architecture

### 20.1 Analytics Strategy

Collect and analyze usage data for insights and optimization.

```
┌─────────────────────────────────────────────────────────────┐
│                    Analytics System                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Event Collection                                           │
│       │                                                     │
│       ├─→ Search Events                                     │
│       ├─→ Index Events                                      │
│       ├─→ API Usage Events                                  │
│       └─→ Error Events                                      │
│                                                             │
│       │                                                     │
│       ▼                                                     │
│  Event Processing (Aggregation, Enrichment)                 │
│       │                                                     │
│       ▼                                                     │
│  Storage (Time-Series Database)                             │
│       │                                                     │
│       ▼                                                     │
│  Analytics Engine (Queries, Reports)                        │
│       │                                                     │
│       ▼                                                     │
│  Visualization (Dashboards, Reports)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 20.2 Event Types

#### 20.2.1 Search Events
```python
class SearchEvent:
    - event_id: str
    - event_type: str = "search"
    - api_key_id: str
    - site_id: str
    - query_type: str  # image, url
    - results_count: int
    - processing_time_ms: int
    - model_used: str
    - timestamp: datetime
```

**Tracked Data:**
- Search query type
- Number of results
- Processing time
- Model used
- User/site ID
- Timestamp

#### 20.2.2 Index Events
```python
class IndexEvent:
    - event_id: str
    - event_type: str = "index"
    - api_key_id: str
    - site_id: str
    - product_id: str
    - action: str  # create, update, delete
    - processing_time_ms: int
    - success: bool
    - timestamp: datetime
```

**Tracked Data:**
- Product ID
- Action (create/update/delete)
- Processing time
- Success/failure
- User/site ID

#### 20.2.3 API Usage Events
```python
class APIUsageEvent:
    - event_id: str
    - event_type: str = "api_usage"
    - api_key_id: str
    - endpoint: str
    - method: str
    - status_code: int
    - processing_time_ms: int
    - timestamp: datetime
```

**Tracked Data:**
- Endpoint
- HTTP method
- Status code
- Processing time
- User/site ID

#### 20.2.4 Error Events
```python
class ErrorEvent:
    - event_id: str
    - event_type: str = "error"
    - api_key_id: str
    - error_type: str
    - error_message: str
    - stack_trace: str
    - context: Dict
    - timestamp: datetime
```

**Tracked Data:**
- Error type
- Error message
- Stack trace
- Context
- User/site ID

### 20.3 Analytics Storage

```python
class AnalyticsStorage:
    - time_series_db: TimeSeriesDB
    
    def store_event(self, event: AnalyticsEvent):
        # Store event in time-series database
        # Tag with metadata
        # Set TTL
    
    def query_events(self, query: AnalyticsQuery) -> List[AnalyticsEvent]:
        # Query events
        # Apply filters
        # Aggregate if needed
        # Return results
```

**Storage Options:**
- InfluxDB (time-series)
- TimescaleDB (PostgreSQL extension)
- Prometheus (metrics)
- Elasticsearch (logs)

### 20.4 Analytics Queries

```python
class AnalyticsQueries:
    # Usage over time
    def get_usage_over_time(self, start: datetime, end: datetime,
                           group_by: str = "hour") -> TimeSeriesData:
        # Query search events
        # Group by time period
        # Return time series
    
    # Top users
    def get_top_users(self, limit: int = 10) -> List[UserStats]:
        # Query API usage events
        # Group by user
        # Sort by usage
        # Return top users
    
    # Search performance
    def get_search_performance(self, start: datetime, end: datetime) -> Metrics:
        # Query search events
        # Calculate p50, p95, p99 latency
        # Return metrics
    
    # Error rate
    def get_error_rate(self, start: datetime, end: datetime) -> float:
        # Query error events
        # Calculate error rate
        # Return percentage
```

### 20.5 Analytics Configuration

```yaml
analytics:
  enabled: true
  
  collection:
    events:
      - search
      - index
      - api_usage
      - error
    
    sampling:
      enabled: false
      rate: 1.0  # 100% sampling
  
  storage:
    type: influxdb  # influxdb, timescaledb, elasticsearch
    host: localhost
    port: 8086
    database: ss_ai_analytics
    retention: 90d  # 90 days
  
  queries:
    cache_ttl: 300  # 5 minutes
    
  reports:
    enabled: true
    schedule: "0 0 * * *"  # Daily
    email:
      enabled: false
      recipients: []
```

---

## 21. Security Architecture

### 21.1 Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Network    │  │   Transport  │  │ Application  │     │
│  │   Security   │→│   Security   │→│   Security   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Data       │  │   Access     │  │   Audit      │     │
│  │   Security   │  │   Control    │  │   Logging    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 21.2 Network Security

#### 21.2.1 Firewall Rules
```yaml
firewall:
  allowed_ports:
    - 22  # SSH
    - 80  # HTTP (redirect to HTTPS)
    - 443  # HTTPS
  
  blocked_ports:
    - 3306  # MySQL (internal only)
    - 5432  # PostgreSQL (internal only)
    - 6379  # Redis (internal only)
```

#### 21.2.2 DDoS Protection
```python
class DDoSProtection:
    - rate_limiter: RateLimiter
    - ip_tracker: IPTracker
    
    def check_request(self, ip: str) -> bool:
        # Track requests per IP
        # Block if threshold exceeded
        # Return allowed/blocked
```

### 21.3 Transport Security

#### 21.3.1 HTTPS Only
```python
class HTTPSEnforcer:
    def enforce_https(self, request: Request) -> Response:
        if not request.is_secure:
            return redirect(request.url.replace("http://", "https://"))
```

#### 21.3.2 TLS Configuration
```yaml
tls:
  enabled: true
  version: TLSv1.3
  cipher_suites:
    - TLS_AES_256_GCM_SHA384
    - TLS_CHACHA20_POLY1305_SHA256
    - TLS_AES_128_GCM_SHA256
  
  certificate:
    path: /etc/ssl/certs/server.crt
    key_path: /etc/ssl/private/server.key
  
  hsts:
    enabled: true
    max_age: 31536000  # 1 year
    include_subdomains: true
```

### 21.4 Application Security

#### 21.4.1 Input Validation
```python
class InputValidator:
    def validate_search_request(self, request: SearchRequest) -> ValidationResult:
        # Validate image format
        # Validate URL format
        # Validate limit range
        # Validate threshold range
        # Sanitize inputs
        return ValidationResult(valid=True/False, errors=[])
```

#### 21.4.2 Image Validation
```python
class ImageValidator:
    def validate_image(self, image_data: bytes) -> ValidationResult:
        # Check file signature
        # Check file size
        # Check dimensions
        # Check for malicious content
        # Scan for vulnerabilities
        return ValidationResult(valid=True/False, errors=[])
```

**Security Checks:**
- File signature validation
- Size limits
- Dimension limits
- Malware scanning
- Path traversal prevention

#### 21.4.3 SQL Injection Prevention
```python
class SafeQueryBuilder:
    def build_query(self, table: str, filters: Dict) -> str:
        # Use parameterized queries
        # Never concatenate user input
        # Use ORM
```

#### 21.4.4 XSS Prevention
```python
class XSSProtector:
    def sanitize(self, input: str) -> str:
        # Escape HTML characters
        # Remove scripts
        # Sanitize output
```

### 21.5 Authentication & Authorization

#### 21.5.1 API Key Security
```python
class APIKeySecurity:
    def hash_key(self, api_key: str) -> str:
        # Use SHA-256
        # Add salt
        # Return hash
    
    def verify_key(self, api_key: str, hash: str) -> bool:
        # Hash input
        # Compare with stored hash
        # Constant-time comparison
```

**Security Measures:**
- SHA-256 hashing
- Salted hashes
- Constant-time comparison
- Never store plaintext keys

#### 21.5.2 JWT Security
```python
class JWTSecurity:
    def create_token(self, payload: Dict) -> str:
        # Use strong secret key
        # Set expiration
        # Sign with HS256/RS256
        # Return token
    
    def validate_token(self, token: str) -> Dict:
        # Verify signature
        # Check expiration
        # Validate claims
        # Return payload
```

**Security Measures:**
- Strong secret keys (256-bit)
- Short expiration (1 hour)
- Refresh tokens
- Signature validation

### 21.6 Rate Limiting

```python
class RateLimiter:
    - limits: Dict[str, RateLimit]
    - storage: Cache
    
    def check_rate_limit(self, api_key: str, endpoint: str) -> RateLimitResult:
        # Get limit for API key
        # Get current usage
        # Check if exceeded
        # Return result
```

**Rate Limit Rules:**
- Per API key
- Per endpoint
- Per IP address
- Sliding window algorithm
- Burst allowance

### 21.7 Data Security

#### 21.7.1 Encryption at Rest
```yaml
encryption:
  database:
    enabled: true
    algorithm: AES-256-GCM
  
  storage:
    enabled: true
    algorithm: AES-256-GCM
  
  backups:
    enabled: true
    algorithm: AES-256-GCM
```

#### 21.7.2 Encryption in Transit
```yaml
encryption:
  tls:
    enabled: true
    version: TLSv1.3
    certificate_rotation: true
```

### 21.8 Audit Logging

```python
class AuditLogger:
    def log_security_event(self, event: SecurityEvent):
        # Log authentication attempts
        # Log authorization failures
        # Log data access
        # Log configuration changes
        # Log admin actions
```

**Audited Events:**
- Authentication success/failure
- Authorization failures
- Data modifications
- Configuration changes
- Admin actions
- API key creation/deletion

### 21.9 Security Configuration

```yaml
security:
  authentication:
    api_key:
      enabled: true
      header_name: "X-API-Key"
      hash_algorithm: SHA256
    
    jwt:
      enabled: true
      header_name: "Authorization"
      algorithm: HS256
      expiration: 3600  # 1 hour
  
  authorization:
    ip_whitelist:
      enabled: true
      header_name: "X-Forwarded-For"
    
    rate_limiting:
      enabled: true
      default_limit: 60  # requests per minute
  
  input_validation:
    enabled: true
    max_request_size: 10MB
    max_url_length: 2048
  
  image_validation:
    enabled: true
    max_file_size: 10MB
    allowed_formats: [jpeg, png, webp]
    scan_malware: true
  
  headers:
    enabled: true
    hsts: true
    csp: true
    x_frame_options: DENY
  
  encryption:
    at_rest: true
    in_transit: true
    algorithm: AES-256-GCM
```

---

## 22. Configuration Architecture

### 22.1 Configuration Strategy

Environment-based configuration with secrets management.

```
┌─────────────────────────────────────────────────────────────┐
│                    Configuration System                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Configuration Sources (Priority Order)                     │
│       │                                                     │
│       ├─→ Environment Variables                             │
│       ├─→ .env Files                                        │
│       ├─→ Configuration Files (YAML/JSON)                   │
│       └─→ Default Values                                    │
│                                                             │
│       │                                                     │
│       ▼                                                     │
│  Configuration Validation                                   │
│       │                                                     │
│       ▼                                                     │
│  Configuration Distribution                                 │
│       │                                                     │
│       ├─→ Application Config                                │
│       ├─→ Database Config                                    │
│       ├─→ AI Model Config                                    │
│       └─→ Security Config                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 22.2 Configuration Layers

#### 22.2.1 Environment Configuration
```python
class EnvironmentConfig:
    - environment: str  # development, staging, production
    - debug: bool
    - log_level: str
```

**Environments:**
- `development`: Local development
- `staging`: Pre-production testing
- `production`: Live environment

#### 22.2.2 Application Configuration
```python
class ApplicationConfig:
    - app_name: str
    - version: str
    - api_prefix: str
    - api_version: str
    - workers: int
    - timeout: int
```

#### 22.2.3 Database Configuration
```python
class DatabaseConfig:
    - type: str
    - host: str
    - port: int
    - database: str
    - username: str
    - password: str
    - pool_size: int
```

#### 22.2.4 AI Model Configuration
```python
class AIConfig:
    - default_provider: str
    - default_model: str
    - device: str
    - precision: str
    - cache_enabled: bool
```

#### 22.2.5 Security Configuration
```python
class SecurityConfig:
    - secret_key: str
    - algorithm: str
    - token_expiration: int
    - rate_limit_enabled: bool
    - ip_whitelist_enabled: bool
```

### 22.3 Configuration Management

```python
class ConfigurationManager:
    - configs: Dict[str, BaseConfig]
    - validators: Dict[str, ConfigValidator]
    
    def load_config(self, config_type: str) -> BaseConfig:
        # Load from environment
        # Load from file
        # Apply defaults
        # Validate
        # Return config
    
    def validate_config(self, config: BaseConfig) -> ValidationResult:
        # Validate required fields
        # Validate types
        # Validate ranges
        # Return result
```

### 22.4 Secrets Management

```python
class SecretsManager:
    - vault_client: VaultClient
    
    def get_secret(self, secret_name: str) -> str:
        # Check environment variables
        # Check secrets manager
        # Return secret value
    
    def rotate_secret(self, secret_name: str) -> str:
        # Generate new secret
        # Store in secrets manager
        # Return new secret
```

**Secrets:**
- Database passwords
- API keys
- JWT secret keys
- Encryption keys
- Third-party API keys

**Secrets Managers:**
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager
- Environment variables (fallback)

### 22.5 Configuration Files

#### 22.5.1 Main Configuration
```yaml
# config/default.yaml
app:
  name: SS AI Server
  version: 1.0.0
  environment: development
  debug: false
  
api:
  prefix: /api
  version: v1
  cors:
    enabled: true
    origins: ["*"]
  
server:
  host: 0.0.0.0
  port: 8000
  workers: 4
  timeout: 30
  
database:
  type: postgresql
  host: localhost
  port: 5432
  database: ss_ai_server
  pool_size: 20
  
redis:
  host: localhost
  port: 6379
  db: 0
  
vector_store:
  type: faiss
  dimensions: 512
  
ai:
  default_provider: openclip
  default_model: ViT-B-32
  device: auto
  precision: fp32
  
logging:
  level: INFO
  format: json
  
monitoring:
  enabled: true
  metrics_port: 9090
```

#### 22.5.2 Environment-Specific Configuration
```yaml
# config/development.yaml
app:
  environment: development
  debug: true
  
logging:
  level: DEBUG
  
database:
  type: sqlite
  path: /data/ss_ai_server.db

# config/production.yaml
app:
  environment: production
  debug: false
  
logging:
  level: INFO
  
database:
  type: postgresql
  host: ${DB_HOST}
  password: ${DB_PASSWORD}
```

### 22.6 Configuration Validation

```python
class ConfigValidator:
    def validate_app_config(self, config: AppConfig) -> ValidationResult:
        # Validate required fields
        # Validate environment
        # Validate version format
        return ValidationResult(valid=True/False, errors=[])
    
    def validate_database_config(self, config: DatabaseConfig) -> ValidationResult:
        # Validate connection parameters
        # Test connection
        # Validate pool size
        return ValidationResult(valid=True/False, errors=[])
```

---

## 23. Deployment Architecture

### 23.1 Deployment Strategy

Platform-agnostic deployment with containerization.

```
┌─────────────────────────────────────────────────────────────┐
│                  Deployment Options                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Docker     │  │   Docker     │  │   Cloud      │     │
│  │  Compose     │  │   Swarm      │  │  Platforms   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   VPS        │  │   Coolify    │  │  Kubernetes  │     │
│  │              │  │   Dokploy    │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 23.2 Deployment Platforms

#### 23.2.1 Docker Compose (Development/Small Production)
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/ss_ai
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/data
  
  worker:
    build: .
    command: celery -A app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/ss_ai
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=ss_ai
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

#### 23.2.2 Render (Cloud Platform)
```yaml
# render.yaml
services:
  - type: web
    name: ss-ai-server-api
    runtime: docker
    plan: starter
    branch: main
    dockerfilePath: ./deployments/docker/Dockerfile
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: ss-ai-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          name: ss-ai-redis
          type: redis
          property: connectionString
  
  - type: worker
    name: ss-ai-server-worker
    runtime: docker
    plan: starter
    branch: main
    dockerfilePath: ./deployments/docker/Dockerfile.worker
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: ss-ai-db
          property: connectionString
  
  - type: redis
    name: ss-ai-redis
    plan: starter
  
  - type: postgres
    name: ss-ai-db
    plan: starter
```

#### 23.2.3 Railway (Cloud Platform)
```yaml
# railway.json
{
  "deploy": {
    "startCommand": "uvicorn app:app --host 0.0.0.0 --port $PORT",
    "multiRegionConfig": {
      "europe": {
        "region": "eu-west-1"
      }
    }
  },
  "environments": {
    "production": {
      "variables": {
        "DATABASE_URL": "${{Postgres.DATABASE_URL}}",
        "REDIS_URL": "${{Redis.REDIS_URL}}"
      }
    }
  }
}
```

#### 23.2.4 Fly.io (Edge Deployment)
```yaml
# fly.toml
app = "ss-ai-server"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1

[[services]]
  http_checks = []
  internal_port = 8000
  processes = ["app"]
  protocol = "tcp"
  script_checks = []
  
  [services.concurrency]
    hard_limit = 25
    soft_limit = 20
    type = "connections"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

#### 23.2.5 Kubernetes (Enterprise)
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ss-ai-server
  labels:
    app: ss-ai-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ss-ai-server
  template:
    metadata:
      labels:
        app: ss-ai-server
    spec:
      containers:
      - name: api
        image: ss-ai-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ss-ai-secrets
              key: database-url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ss-ai-server
spec:
  selector:
    app: ss-ai-server
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 23.3 Deployment Configuration

```yaml
deployment:
  platform: docker-compose  # docker-compose, render, railway, fly, kubernetes
  
  scaling:
    api:
      min_instances: 1
      max_instances: 10
      target_cpu: 70
    
    worker:
      min_instances: 1
      max_instances: 5
      target_cpu: 80
  
  resources:
    api:
      cpu: "1000m"
      memory: "2Gi"
      limits:
        cpu: "2000m"
        memory: "4Gi"
    
    worker:
      cpu: "2000m"
      memory: "4Gi"
      limits:
        cpu: "4000m"
        memory: "8Gi"
  
  health_checks:
    enabled: true
    liveness_path: /health/live
    readiness_path: /health/ready
    startup_delay: 30
```

---

## 24. Docker Architecture

### 24.1 Docker Strategy

Multi-stage builds for optimized images.

### 24.2 API Dockerfile

```dockerfile
# Stage 1: Base
FROM python:3.11-slim as base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies
FROM base as dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Development
FROM dependencies as development
COPY . .
RUN pip install --no-cache-dir -r requirements-dev.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Stage 4: Production
FROM dependencies as production
COPY src/ ./src/
COPY migrations/ ./migrations/
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health/live')"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 24.3 Worker Dockerfile

```dockerfile
FROM python:3.11-slim as base
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run worker
CMD ["celery", "-A", "app", "worker", "--loglevel=info"]
```

### 24.4 Docker Compose

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: deployments/docker/Dockerfile
      target: production
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/ss_ai
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./data:/data
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health/live')"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 1G
  
  worker:
    build:
      context: .
      dockerfile: deployments/docker/Dockerfile.worker
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/ss_ai
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./data:/data
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '1'
          memory: 2G
  
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=ss_ai
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d ss_ai"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

### 24.5 Docker Configuration

```yaml
docker:
  api:
    base_image: python:3.11-slim
    target: production
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL
      - REDIS_URL
      - SECRET_KEY
    volumes:
      - ./data:/data
    healthcheck:
      path: /health/live
      interval: 30s
  
  worker:
    base_image: python:3.11-slim
    command: celery -A app worker --loglevel=info
    environment:
      - DATABASE_URL
      - REDIS_URL
    volumes:
      - ./data:/data
  
  database:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
```

---

## 25. Dependency Injection Architecture

### 25.1 DI Strategy

Use dependency injection for loose coupling and testability.

```
┌─────────────────────────────────────────────────────────────┐
│                 Dependency Injection Container                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Registrations:                                             │
│    - AIProvider → OpenCLIPProvider                          │
│    - VectorStore → FAISSStore                               │
│    - ProductRepository → PostgresProductRepository          │
│    - Queue → RedisQueue                                     │
│    - Cache → RedisCache                                     │
│                                                             │
│  Resolution:                                                │
│    - Use Case → Domain Services → Infrastructure            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 25.2 Service Container

```python
class ServiceContainer:
    _instance = None
    _services: Dict[Type, Any] = {}
    _singletons: Dict[Type, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register(self, interface: Type, implementation: Type, singleton: bool = False):
        """Register a service"""
        self._services[interface] = (implementation, singleton)
    
    def resolve(self, interface: Type) -> Any:
        """Resolve a service"""
        if interface not in self._services:
            raise ServiceNotFoundError(interface)
        
        implementation, singleton = self._services[interface]
        
        if singleton and interface in self._singletons:
            return self._singletons[interface]
        
        # Create instance
        instance = self._create_instance(implementation)
        
        if singleton:
            self._singletons[interface] = instance
        
        return instance
    
    def _create_instance(self, cls: Type) -> Any:
        """Create instance with dependency injection"""
        # Inspect constructor
        sig = inspect.signature(cls.__init__)
        kwargs = {}
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            # Resolve dependency
            param_type = param.annotation
            if param_type != inspect.Parameter.empty:
                kwargs[param_name] = self.resolve(param_type)
        
        return cls(**kwargs)
```

### 25.3 Service Registration

```python
class ServiceRegistry:
    def register_services(self, container: ServiceContainer):
        # Register AI providers
        container.register(AIProvider, OpenCLIPProvider, singleton=True)
        container.register(AIProvider, SigLIPProvider, singleton=True)
        
        # Register vector stores
        container.register(VectorStore, FAISSStore, singleton=True)
        
        # Register repositories
        container.register(ProductRepository, PostgresProductRepository, singleton=True)
        container.register(EmbeddingRepository, PostgresEmbeddingRepository, singleton=True)
        
        # Register cache
        container.register(Cache, RedisCache, singleton=True)
        
        # Register queue
        container.register(Queue, RedisQueue, singleton=True)
        
        # Register use cases
        container.register(SearchImageUseCase, SearchImageUseCase)
        container.register(IndexProductUseCase, IndexProductUseCase)
```

### 25.4 Configuration-Based DI

```python
class ConfigurationBasedDI:
    def configure_services(self, config: Dict, container: ServiceContainer):
        # AI Providers
        for provider_name, provider_config in config['ai_providers'].items():
            provider_class = self._get_provider_class(provider_name)
            container.register(AIProvider, provider_class, singleton=True)
        
        # Vector Store
        vector_store_type = config['vector_store']['type']
        vector_store_class = self._get_vector_store_class(vector_store_type)
        container.register(VectorStore, vector_store_class, singleton=True)
        
        # Repositories
        db_type = config['database']['type']
        repo_class = self._get_repository_class(db_type)
        container.register(ProductRepository, repo_class, singleton=True)
```

### 25.5 Benefits of DI

- **Testability:** Easy to mock dependencies
- **Flexibility:** Swap implementations without changing code
- **Configuration:** Configure services via config files
- **Loose Coupling:** Components don't create their dependencies
- **Single Responsibility:** Each class has one job

---

## 26. Interface Design

### 26.1 Interface Principles

- **Single Responsibility:** Each interface has one purpose
- **Interface Segregation:** Small, focused interfaces
- **Dependency Inversion:** Depend on abstractions, not concretions
- **Explicit Contracts:** Clear method signatures and documentation

### 26.2 Core Interfaces

#### 26.2.1 AI Provider Interface
```python
class AIProvider(ABC):
    """Interface for AI model providers"""
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider name"""
        pass
    
    @abstractmethod
    def get_supported_models(self) -> List[ModelInfo]:
        """Return list of supported models"""
        pass
    
    @abstractmethod
    def load_model(self, model_name: str) -> None:
        """Load model into memory"""
        pass
    
    @abstractmethod
    def unload_model(self) -> None:
        """Unload model from memory"""
        pass
    
    @abstractmethod
    def generate_embedding(self, image: Image) -> EmbeddingVector:
        """Generate embedding for single image"""
        pass
    
    @abstractmethod
    def generate_embeddings_batch(self, images: List[Image]) -> List[EmbeddingVector]:
        """Generate embeddings for batch of images"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> ModelInfo:
        """Get current model information"""
        pass
    
    @abstractmethod
    def warmup(self) -> None:
        """Warm up model for faster inference"""
        pass
```

#### 26.2.2 Vector Store Interface
```python
class VectorStore(ABC):
    """Interface for vector databases"""
    
    @abstractmethod
    def initialize(self, dimensions: int, metric: str = 'cosine') -> None:
        """Initialize vector store"""
        pass
    
    @abstractmethod
    def add_vectors(self, vectors: List[Tuple[str, EmbeddingVector, Dict]]) -> None:
        """Add vectors to store"""
        pass
    
    @abstractmethod
    def search(self, query_vector: EmbeddingVector, limit: int = 10,
               filter_dict: Dict = None) -> List[SearchResult]:
        """Search for similar vectors"""
        pass
    
    @abstractmethod
    def delete_vectors(self, product_ids: List[str]) -> int:
        """Delete vectors by product IDs"""
        pass
    
    @abstractmethod
    def get_vector(self, product_id: str) -> Optional[Tuple[EmbeddingVector, Dict]]:
        """Get single vector"""
        pass
    
    @abstractmethod
    def get_stats(self) -> VectorStoreStats:
        """Get vector store statistics"""
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """Persist to disk"""
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        """Load from disk"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all vectors"""
        pass
```

#### 26.2.3 Repository Interface
```python
class Repository(ABC, Generic[T]):
    """Generic repository interface"""
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add new entity"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update existing entity"""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete entity by ID"""
        pass
    
    @abstractmethod
    def exists(self, id: str) -> bool:
        """Check if entity exists"""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count entities"""
        pass
```

#### 26.2.4 Queue Interface
```python
class Queue(ABC, Generic[T]):
    """Interface for job queues"""
    
    @abstractmethod
    def enqueue(self, job: T, priority: int = 0) -> str:
        """Add job to queue"""
        pass
    
    @abstractmethod
    def dequeue(self) -> Optional[T]:
        """Get next job"""
        pass
    
    @abstractmethod
    def get_job(self, job_id: str) -> Optional[T]:
        """Get job by ID"""
        pass
    
    @abstractmethod
    def update_job_status(self, job_id: str, status: JobStatus,
                         result: Dict = None, error: str = None) -> None:
        """Update job status"""
        pass
    
    @abstractmethod
    def retry_job(self, job_id: str) -> bool:
        """Retry failed job"""
        pass
    
    @abstractmethod
    def get_queue_stats(self) -> QueueStats:
        """Get queue statistics"""
        pass
    
    @abstractmethod
    def clear_queue(self, job_type: str = None) -> int:
        """Clear queue"""
        pass
```

#### 26.2.5 Cache Interface
```python
class Cache(ABC, Generic[K, V]):
    """Interface for caching"""
    
    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        """Get value by key"""
        pass
    
    @abstractmethod
    def set(self, key: K, value: V, ttl: int = None) -> None:
        """Set value with optional TTL"""
        pass
    
    @abstractmethod
    def delete(self, key: K) -> bool:
        """Delete value by key"""
        pass
    
    @abstractmethod
    def exists(self, key: K) -> bool:
        """Check if key exists"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all values"""
        pass
    
    @abstractmethod
    def get_many(self, keys: List[K]) -> Dict[K, V]:
        """Get multiple values"""
        pass
    
    @abstractmethod
    def set_many(self, mapping: Dict[K, V], ttl: int = None) -> None:
        """Set multiple values"""
        pass
```

#### 26.2.6 Storage Interface
```python
class Storage(ABC):
    """Interface for file storage"""
    
    @abstractmethod
    def save(self, path: str, data: bytes, content_type: str) -> str:
        """Save file, return URL"""
        pass
    
    @abstractmethod
    def load(self, path: str) -> bytes:
        """Load file"""
        pass
    
    @abstractmethod
    def delete(self, path: str) -> bool:
        """Delete file"""
        pass
    
    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if file exists"""
        pass
    
    @abstractmethod
    def get_url(self, path: str) -> str:
        """Get public URL"""
        pass
```

### 26.3 Interface Documentation

All interfaces must include:
- **Docstrings:** Clear description of purpose
- **Type Hints:** Complete type annotations
- **Parameter Documentation:** Purpose and constraints
- **Return Documentation:** Return type and meaning
- **Exception Documentation:** Possible exceptions
- **Examples:** Usage examples

---

## 27. Future Module Strategy

### 27.1 Modularity by Design

The architecture supports adding new modules without modifying core code.

```
┌─────────────────────────────────────────────────────────────┐
│                    Core System                               │
│  (Unchanging Foundation)                                     │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│ Image Search   │  │    OCR      │  │ Product Recs    │
│   Module       │  │   Module    │  │    Module       │
└────────────────┘  └─────────────┘  └─────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────▼────────┐
                    │  Plugin        │
                    │  Interface     │
                    └────────────────┘
```

### 27.2 Module Interface

```python
class Module(ABC):
    """Base interface for all modules"""
    
    @abstractmethod
    def get_module_name(self) -> str:
        """Return module name"""
        pass
    
    @abstractmethod
    def get_module_version(self) -> str:
        """Return module version"""
        pass
    
    @abstractmethod
    def initialize(self, container: ServiceContainer) -> None:
        """Initialize module with DI container"""
        pass
    
    @abstractmethod
    def register_routes(self, router: APIRouter) -> None:
        """Register API routes"""
        pass
    
    @abstractmethod
    def register_workers(self, worker_manager: WorkerManager) -> None:
        """Register background workers"""
        pass
    
    @abstractmethod
    def get_health_status(self) -> HealthStatus:
        """Return module health status"""
        pass
```

### 27.3 Future Modules

#### 27.3.1 OCR Module
```python
class OCRModule(Module):
    - ocr_provider: OCRProvider
    - text_repository: TextRepository
    
    def get_module_name(self) -> str:
        return "ocr"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/ocr/extract", self.extract_text)
        router.add_route("/ocr/batch", self.batch_extract)
    
    def extract_text(self, image: Image) -> TextResult:
        # Extract text from image
        # Return text and confidence
```

**Capabilities:**
- Extract text from images
- Support multiple languages
- Batch processing
- Confidence scoring

#### 27.3.2 Product Recommendation Module
```python
class ProductRecommendationModule(Module):
    - recommendation_engine: RecommendationEngine
    - user_repository: UserRepository
    
    def get_module_name(self) -> str:
        return "product_recommendation"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/recommendations/user/{user_id}", self.get_recommendations)
        router.add_route("/recommendations/similar/{product_id}", self.get_similar)
    
    def get_recommendations(self, user_id: str) -> List[Product]:
        # Get user preferences
        # Generate recommendations
        # Return products
```

**Capabilities:**
- Collaborative filtering
- Content-based recommendations
- Hybrid recommendations
- Personalization

#### 27.3.3 Auto Product Tags Module
```python
class AutoProductTagsModule(Module):
    - tag_generator: TagGenerator
    - tag_repository: TagRepository
    
    def get_module_name(self) -> str:
        return "auto_product_tags"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/tags/generate", self.generate_tags)
        router.add_route("/tags/batch", self.batch_generate)
    
    def generate_tags(self, product: Product) -> List[Tag]:
        # Analyze product
        # Generate tags
        # Return tags
```

**Capabilities:**
- Automatic tag generation
- Multi-language support
- Tag categorization
- Tag confidence scoring

#### 27.3.4 Duplicate Detection Module
```python
class DuplicateDetectionModule(Module):
    - duplicate_detector: DuplicateDetector
    - product_repository: ProductRepository
    
    def get_module_name(self) -> str:
        return "duplicate_detection"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/duplicates/detect", self.detect_duplicates)
        router.add_route("/duplicates/batch", self.batch_detect)
    
    def detect_duplicates(self, product_id: str) -> List[Duplicate]:
        # Find similar products
        # Calculate similarity
        # Return duplicates
```

**Capabilities:**
- Near-duplicate detection
- Similarity thresholding
- Batch detection
- Duplicate clustering

#### 27.3.5 Image Captioning Module
```python
class ImageCaptioningModule(Module):
    - caption_generator: CaptionGenerator
    
    def get_module_name(self) -> str:
        return "image_captioning"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/caption/generate", self.generate_caption)
    
    def generate_caption(self, image: Image) -> Caption:
        # Generate caption
        # Return caption and confidence
```

**Capabilities:**
- Automatic caption generation
- Multi-language support
- Caption length control
- Confidence scoring

#### 27.3.6 Background Removal Module
```python
class BackgroundRemovalModule(Module):
    - background_remover: BackgroundRemover
    
    def get_module_name(self) -> str:
        return "background_removal"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/background/remove", self.remove_background)
    
    def remove_background(self, image: Image) -> Image:
        # Remove background
        # Return transparent image
```

**Capabilities:**
- Automatic background removal
- Multiple algorithms
- Quality preservation
- Batch processing

#### 27.3.7 Vision Analysis Module
```python
class VisionAnalysisModule(Module):
    - vision_analyzer: VisionAnalyzer
    
    def get_module_name(self) -> str:
        return "vision_analysis"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/vision/analyze", self.analyze)
    
    def analyze(self, image: Image) -> AnalysisResult:
        # Analyze image
        # Return objects, scenes, attributes
```

**Capabilities:**
- Object detection
- Scene classification
- Attribute extraction
- Content moderation

#### 27.3.8 Object Detection Module
```python
class ObjectDetectionModule(Module):
    - object_detector: ObjectDetector
    
    def get_module_name(self) -> str:
        return "object_detection"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/objects/detect", self.detect_objects)
    
    def detect_objects(self, image: Image) -> List[Object]:
        # Detect objects
        # Return bounding boxes and labels
```

**Capabilities:**
- Object detection
- Bounding box generation
- Class labeling
- Confidence scoring

#### 27.3.9 SEO AI Module
```python
class SEOAIModule(Module):
    - seo_analyzer: SEOAnalyzer
    
    def get_module_name(self) -> str:
        return "seo_ai"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/seo/analyze", self.analyze_seo)
        router.add_route("/seo/suggest", self.suggest_improvements)
    
    def analyze_seo(self, product: Product) -> SEOAnalysis:
        # Analyze SEO
        # Return suggestions
```

**Capabilities:**
- SEO analysis
- Meta tag generation
- Keyword suggestions
- Content optimization

#### 27.3.10 Document AI Module
```python
class DocumentAIModule(Module):
    - document_processor: DocumentProcessor
    
    def get_module_name(self) -> str:
        return "document_ai"
    
    def register_routes(self, router: APIRouter):
        router.add_route("/document/extract", self.extract_text)
        router.add_route("/document/analyze", self.analyze)
    
    def extract_text(self, document: Document) -> TextResult:
        # Extract text from document
        # Return structured data
```

**Capabilities:**
- Document parsing
- Text extraction
- Table extraction
- Form recognition

### 27.4 Module Registration

```python
class ModuleManager:
    - modules: Dict[str, Module]
    - container: ServiceContainer
    
    def register_module(self, module: Module):
        # Initialize module
        module.initialize(self.container)
        
        # Register routes
        module.register_routes(self.router)
        
        # Register workers
        module.register_workers(self.worker_manager)
        
        # Store module
        self.modules[module.get_module_name()] = module
    
    def get_module(self, name: str) -> Module:
        return self.modules.get(name)
    
    def get_all_modules(self) -> List[Module]:
        return list(self.modules.values())
```

### 27.5 Module Configuration

```yaml
modules:
  image_search:
    enabled: true
  
  ocr:
    enabled: false
    provider: tesseract
    languages: [eng, spa, fra]
  
  product_recommendation:
    enabled: false
    algorithm: collaborative_filtering
  
  auto_product_tags:
    enabled: false
    max_tags: 10
    confidence_threshold: 0.7
  
  duplicate_detection:
    enabled: false
    threshold: 0.95
  
  image_captioning:
    enabled: false
    model: blip
  
  background_removal:
    enabled: false
    algorithm: u2net
  
  vision_analysis:
    enabled: false
    models: [object_detection, scene_classification]
  
  object_detection:
    enabled: false
    model: yolov8
  
  seo_ai:
    enabled: false
  
  document_ai:
    enabled: false
    supported_formats: [pdf, docx, txt]
```

---

## 28. Scalability Strategy

### 28.1 Scalability Dimensions

```
┌─────────────────────────────────────────────────────────────┐
│                  Scalability Strategy                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Horizontal  │  │  Vertical    │  │   Data       │     │
│  │  Scaling     │  │  Scaling     │  │  Partitioning│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Caching    │  │  Async       │  │   CDN        │     │
│  │              │  │  Processing  │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 28.2 Horizontal Scaling

#### 28.2.1 API Server Scaling
```yaml
api:
  replicas: 3  # Start with 3, scale to 10
  autoscaling:
    enabled: true
    min_replicas: 2
    max_replicas: 10
    target_cpu: 70
    target_memory: 80
```

**Scaling Strategy:**
- Load balancer distributes traffic
- Stateless API servers
- Scale based on CPU/memory
- Scale based on request rate

#### 28.2.2 Worker Scaling
```yaml
workers:
  embedding:
    replicas: 2
    autoscaling:
      enabled: true
      min_replicas: 1
      max_replicas: 5
      target_queue_length: 10
  
  batch:
    replicas: 1
    autoscaling:
      enabled: true
      min_replicas: 1
      max_replicas: 3
      target_queue_length: 5
```

**Scaling Strategy:**
- Scale based on queue length
- Scale based on processing time
- Priority-based scaling

### 28.3 Vertical Scaling

#### 28.3.1 Resource Allocation
```yaml
api:
  resources:
    requests:
      cpu: "500m"
      memory: "1Gi"
    limits:
      cpu: "2000m"
      memory: "4Gi"

worker:
  resources:
    requests:
      cpu: "1000m"
      memory: "2Gi"
    limits:
      cpu: "4000m"
      memory: "8Gi"
```

**Optimization:**
- Right-size resources
- Monitor utilization
- Adjust based on metrics

### 28.4 Data Partitioning

#### 28.4.1 Database Partitioning
```sql
-- Partition products by site_id
CREATE TABLE products (
    product_id VARCHAR(255),
    site_id VARCHAR(255),
    ...
) PARTITION BY HASH (site_id);

-- Create partitions
CREATE TABLE products_0 PARTITION OF products
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE products_1 PARTITION OF products
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

#### 28.4.2 Vector Store Partitioning
```python
class PartitionedVectorStore:
    - stores: Dict[str, VectorStore]  # site_id -> store
    
    def add_vectors(self, vectors: List[Tuple[str, EmbeddingVector, Dict]]):
        # Group by site_id
        # Add to appropriate store
    
    def search(self, query: EmbeddingVector, site_ids: List[str]) -> List[SearchResult]:
        # Search in relevant stores
        # Combine results
        # Return ranked results
```

### 28.5 Caching Strategy

#### 28.5.1 Multi-Level Caching
```python
class MultiLevelCache:
    - l1_cache: MemoryCache
    - l2_cache: RedisCache
    
    def get(self, key: str) -> Optional[Any]:
        # Check L1
        value = self.l1_cache.get(key)
        if value:
            return value
        
        # Check L2
        value = self.l2_cache.get(key)
        if value:
            # Populate L1
            self.l1_cache.set(key, value)
            return value
        
        return None
```

#### 28.5.2 Cache Warming
```python
class CacheWarmer:
    def warm_popular_searches(self):
        # Get popular search queries
        # Pre-compute results
        # Store in cache
```

### 28.6 Async Processing

#### 28.6.1 Async Architecture
```python
class AsyncProcessor:
    - queue: Queue
    - workers: List[Worker]
    
    async def process_async(self, job: Job) -> JobResult:
        # Add to queue
        job_id = self.queue.enqueue(job)
        
        # Wait for result
        result = await self.wait_for_result(job_id)
        
        return result
```

**Benefits:**
- Non-blocking operations
- Better resource utilization
- Improved throughput
- Better user experience

### 28.7 Performance Optimization

#### 28.7.1 Batch Processing
```python
class BatchProcessor:
    def process_batch(self, items: List[Item], batch_size: int = 32):
        # Split into batches
        batches = [items[i:i+batch_size] for i in range(0, len(items), batch_size)]
        
        # Process batches
        results = []
        for batch in batches:
            result = self.process_single_batch(batch)
            results.extend(result)
        
        return results
```

#### 28.7.2 Connection Pooling
```python
class ConnectionPool:
    - pool: Pool
    
    def get_connection(self) -> Connection:
        # Get from pool
        # Return connection
    
    def release_connection(self, conn: Connection):
        # Return to pool
```

#### 28.7.3 Lazy Loading
```python
class LazyLoader:
    def __init__(self, load_func: Callable):
        self.load_func = load_func
        self._value = None
        self._loaded = False
    
    def get_value(self) -> Any:
        if not self._loaded:
            self._value = self.load_func()
            self._loaded = True
        return self._value
```

### 28.8 Scalability Metrics

```python
class ScalabilityMetrics:
    - requests_per_second: float
    - average_latency: float
    - p95_latency: float
    - p99_latency: float
    - error_rate: float
    - cpu_utilization: float
    - memory_utilization: float
    - queue_length: int
    - worker_utilization: float
```

**Target Metrics:**
- Requests per second: 1000+
- Average latency: <200ms
- P95 latency: <500ms
- P99 latency: <1000ms
- Error rate: <0.1%
- CPU utilization: <70%
- Memory utilization: <80%

---

## 29. Error Handling Strategy

### 29.1 Error Handling Principles

- **Fail Fast:** Detect errors early
- **Graceful Degradation:** Continue operating with reduced functionality
- **Retry with Backoff:** Retry transient errors
- **Circuit Breaker:** Prevent cascading failures
- **Comprehensive Logging:** Log all errors with context
- **User-Friendly Messages:** Clear error messages

### 29.2 Error Types

#### 29.2.1 Domain Errors
```python
class DomainError(Exception):
    """Base domain error"""
    pass

class ValidationError(DomainError):
    """Validation failed"""
    pass

class NotFoundError(DomainError):
    """Entity not found"""
    pass

class BusinessRuleError(DomainError):
    """Business rule violation"""
    pass
```

#### 29.2.2 Application Errors
```python
class ApplicationError(Exception):
    """Base application error"""
    pass

class UseCaseError(ApplicationError):
    """Use case execution failed"""
    pass

class ValidationError(ApplicationError):
    """Input validation failed"""
    pass
```

#### 29.2.3 Infrastructure Errors
```python
class InfrastructureError(Exception):
    """Base infrastructure error"""
    pass

class DatabaseError(InfrastructureError):
    """Database operation failed"""
    pass

class AIProviderError(InfrastructureError):
    """AI provider error"""
    pass

class VectorStoreError(InfrastructureError):
    """Vector store error"""
    pass

class QueueError(InfrastructureError):
    """Queue operation failed"""
    pass
```

### 29.3 Error Handling Middleware

```python
class ErrorHandlingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        try:
            await self.app(scope, receive, send)
        except DomainError as e:
            # Log error
            # Return 400 Bad Request
            await self.send_error_response(send, 400, str(e))
        except ApplicationError as e:
            # Log error
            # Return 500 Internal Server Error
            await self.send_error_response(send, 500, str(e))
        except InfrastructureError as e:
            # Log error
            # Return 503 Service Unavailable
            await self.send_error_response(send, 503, str(e))
        except Exception as e:
            # Log error
            # Return 500 Internal Server Error
            await self.send_error_response(send, 500, "Internal server error")
```

### 29.4 Retry Strategy

```python
class RetryStrategy:
    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_delay: float = 1.0
    max_delay: float = 60.0
    
    def get_next_delay(self, retry_count: int) -> float:
        delay = self.initial_delay * (self.backoff_factor ** retry_count)
        return min(delay, self.max_delay)
    
    def should_retry(self, error: Exception, retry_count: int) -> bool:
        if retry_count >= self.max_retries:
            return False
        
        # Retry on transient errors
        return isinstance(error, (TransientError, TimeoutError, ConnectionError))
```

**Retry Rules:**
- Exponential backoff
- Maximum 3 retries
- Retry only on transient errors
- No retry on validation errors

### 29.5 Circuit Breaker

```python
class CircuitBreaker:
    - failure_threshold: int = 5
    - recovery_timeout: int = 60
    - failure_count: int = 0
    - last_failure_time: datetime
    - state: CircuitState = CLOSED
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == OPEN:
            if self._should_attempt_reset():
                self.state = HALF_OPEN
            else:
                raise CircuitBreakerOpenError()
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = OPEN
```

**Circuit Breaker States:**
- **CLOSED:** Normal operation
- **OPEN:** Failing, reject requests
- **HALF_OPEN:** Testing if recovered

### 29.6 Fallback Strategy

```python
class FallbackStrategy:
    def execute_with_fallback(self, primary: Callable, 
                             fallback: Callable, *args, **kwargs) -> Any:
        try:
            return primary(*args, **kwargs)
        except Exception as e:
            # Log error
            # Execute fallback
            return fallback(*args, **kwargs)
```

**Fallback Examples:**
- Use cached results if AI provider fails
- Return empty results if vector store fails
- Use default model if preferred model fails

### 29.7 Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "EMBEDDING_GENERATION_FAILED",
    "message": "Failed to generate embedding",
    "details": {
      "reason": "Model not loaded",
      "model": "openclip-ViT-B-32"
    },
    "request_id": "uuid-v4",
    "timestamp": "2026-07-18T15:30:00Z",
    "documentation_url": "https://docs.ss-ai-server.com/errors/EMBEDDING_GENERATION_FAILED"
  }
}
```

### 29.8 Error Codes

```python
class ErrorCode(Enum):
    # Validation Errors (400)
    INVALID_INPUT = "INVALID_INPUT"
    INVALID_IMAGE = "INVALID_IMAGE"
    INVALID_URL = "INVALID_URL"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    
    # Authentication Errors (401)
    INVALID_API_KEY = "INVALID_API_KEY"
    EXPIRED_API_KEY = "EXPIRED_API_KEY"
    INVALID_JWT = "INVALID_JWT"
    EXPIRED_JWT = "EXPIRED_JWT"
    
    # Authorization Errors (403)
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    IP_NOT_WHITELISTED = "IP_NOT_WHITELISTED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    
    # Not Found Errors (404)
    PRODUCT_NOT_FOUND = "PRODUCT_NOT_FOUND"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    
    # Server Errors (500)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    AI_PROVIDER_ERROR = "AI_PROVIDER_ERROR"
    VECTOR_STORE_ERROR = "VECTOR_STORE_ERROR"
    QUEUE_ERROR = "QUEUE_ERROR"
    
    # Service Unavailable (503)
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    MODEL_NOT_LOADED = "MODEL_NOT_LOADED"
    CIRCUIT_BREAKER_OPEN = "CIRCUIT_BREAKER_OPEN"
```

---

## 30. Complete Development Roadmap

### 30.1 Development Phases

```
┌─────────────────────────────────────────────────────────────┐
│                  Development Roadmap                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1: Foundation (Weeks 1-4)                            │
│  Phase 2: Core Features (Weeks 5-8)                         │
│  Phase 3: AI Integration (Weeks 9-12)                       │
│  Phase 4: Production Ready (Weeks 13-16)                    │
│  Phase 5: Advanced Features (Weeks 17-20)                   │
│  Phase 6: Scale & Optimize (Weeks 21-24)                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 30.2 Phase 1: Foundation (Weeks 1-4)

**Goal:** Establish core architecture and infrastructure

**Week 1: Project Setup**
- [ ] Initialize project structure
- [ ] Set up development environment
- [ ] Configure version control
- [ ] Set up CI/CD pipeline
- [ ] Create Docker configuration
- [ ] Set up database schema
- [ ] Configure logging

**Week 2: Core Architecture**
- [ ] Implement domain layer (entities, value objects)
- [ ] Implement repository interfaces
- [ ] Implement service interfaces
- [ ] Set up dependency injection
- [ ] Implement configuration management
- [ ] Set up error handling framework

**Week 3: Infrastructure Layer**
- [ ] Implement database repositories
- [ ] Implement cache (Redis)
- [ ] Implement queue (Redis)
- [ ] Implement storage (local/S3)
- [ ] Implement logging infrastructure
- [ ] Implement monitoring

**Week 4: API Foundation**
- [ ] Set up FastAPI application
- [ ] Implement middleware stack
- [ ] Implement authentication
- [ ] Implement rate limiting
- [ ] Create health check endpoints
- [ ] Create API documentation

**Deliverables:**
- Working project structure
- Database schema
- Basic API with authentication
- Docker setup
- CI/CD pipeline

### 30.3 Phase 2: Core Features (Weeks 5-8)

**Goal:** Implement core image search functionality

**Week 5: Image Processing**
- [ ] Implement image validation
- [ ] Implement image loading
- [ ] Implement image preprocessing
- [ ] Implement image storage
- [ ] Create image processing pipeline

**Week 6: Embedding Generation**
- [ ] Implement AI provider interface
- [ ] Implement OpenCLIP provider
- [ ] Implement embedding generation
- [ ] Implement batch processing
- [ ] Implement embedding cache
- [ ] Create embedding pipeline

**Week 7: Vector Store**
- [ ] Implement vector store interface
- [ ] Implement FAISS store
- [ ] Implement hnswlib store
- [ ] Implement vector store manager
- [ ] Implement vector backup/restore
- [ ] Create vector store configuration

**Week 8: Search & Index**
- [ ] Implement search service
- [ ] Implement index service
- [ ] Implement search pipeline
- [ ] Implement index pipeline
- [ ] Create search API endpoints
- [ ] Create index API endpoints

**Deliverables:**
- Working image search
- Product indexing
- Vector storage
- Basic API endpoints

### 30.4 Phase 3: AI Integration (Weeks 9-12)

**Goal:** Integrate multiple AI models and providers

**Week 9: Additional AI Providers**
- [ ] Implement SigLIP provider
- [ ] Implement MobileNet provider
- [ ] Implement provider factory
- [ ] Implement model manager
- [ ] Create model switching logic
- [ ] Add model configuration

**Week 10: Advanced Search**
- [ ] Implement batch search
- [ ] Implement duplicate detection
- [ ] Implement search ranking
- [ ] Implement search filtering
- [ ] Implement search history
- [ ] Add search analytics

**Week 11: Background Processing**
- [ ] Implement queue system
- [ ] Implement embedding worker
- [ ] Implement batch worker
- [ ] Implement worker manager
- [ ] Implement job retry logic
- [ ] Add queue monitoring

**Week 12: Testing & Optimization**
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Write E2E tests
- [ ] Optimize performance
- [ ] Optimize memory usage
- [ ] Optimize batch processing

**Deliverables:**
- Multiple AI providers
- Background processing
- Comprehensive testing
- Performance optimization

### 30.5 Phase 4: Production Ready (Weeks 13-16)

**Goal:** Make system production-ready

**Week 13: Security**
- [ ] Implement comprehensive authentication
- [ ] Implement authorization
- [ ] Implement IP whitelisting
- [ ] Implement rate limiting
- [ ] Implement input validation
- [ ] Implement security headers
- [ ] Add audit logging

**Week 14: Monitoring & Logging**
- [ ] Implement structured logging
- [ ] Implement metrics collection
- [ ] Implement health checks
- [ ] Implement monitoring dashboard
- [ ] Set up alerting
- [ ] Add performance monitoring

**Week 15: Analytics**
- [ ] Implement analytics collection
- [ ] Implement analytics storage
- [ ] Implement analytics queries
- [ ] Create analytics API
- [ ] Build analytics dashboard
- [ ] Add reporting

**Week 16: Documentation & Deployment**
- [ ] Write API documentation
- [ ] Write deployment guides
- [ ] Write user documentation
- [ ] Create deployment scripts
- [ ] Set up production deployment
- [ ] Perform load testing

**Deliverables:**
- Production-ready system
- Comprehensive security
- Monitoring and logging
- Analytics and reporting
- Complete documentation

### 30.6 Phase 5: Advanced Features (Weeks 17-20)

**Goal:** Add advanced features and modules

**Week 17: Module System**
- [ ] Implement module interface
- [ ] Implement module manager
- [ ] Create module loader
- [ ] Add module configuration
- [ ] Test module system

**Week 18: Additional Modules**
- [ ] Implement OCR module
- [ ] Implement product recommendation module
- [ ] Implement auto product tags module
- [ ] Implement duplicate detection module
- [ ] Test all modules

**Week 19: More Modules**
- [ ] Implement image captioning module
- [ ] Implement background removal module
- [ ] Implement vision analysis module
- [ ] Implement object detection module
- [ ] Test all modules

**Week 20: Final Modules**
- [ ] Implement SEO AI module
- [ ] Implement document AI module
- [ ] Integrate all modules
- [ ] Test module interactions
- [ ] Optimize module loading

**Deliverables:**
- Modular system
- 10+ functional modules
- Module documentation
- Module testing

### 30.7 Phase 6: Scale & Optimize (Weeks 21-24)

**Goal:** Optimize for scale and performance

**Week 21: Performance Optimization**
- [ ] Profile application
- [ ] Optimize database queries
- [ ] Optimize vector store operations
- [ ] Optimize caching strategy
- [ ] Optimize batch processing
- [ ] Reduce memory usage

**Week 22: Scalability**
- [ ] Implement horizontal scaling
- [ ] Implement load balancing
- [ ] Implement database partitioning
- [ ] Implement vector store partitioning
- [ ] Test scalability
- [ ] Optimize resource usage

**Week 23: High Availability**
- [ ] Implement failover
- [ ] Implement backup/restore
- [ ] Implement disaster recovery
- [ ] Test failover scenarios
- [ ] Implement health checks
- [ ] Add redundancy

**Week 24: Final Testing & Launch**
- [ ] Perform load testing
- [ ] Perform stress testing
- [ ] Perform security testing
- [ ] Fix bugs
- [ ] Optimize based on testing
- [ ] Prepare for launch

**Deliverables:**
- Optimized performance
- Scalable architecture
- High availability
- Production-ready system

### 30.8 Post-Launch (Ongoing)

**Maintenance:**
- Bug fixes
- Security patches
- Performance monitoring
- User support

**Enhancements:**
- New AI models
- New modules
- Performance improvements
- Feature requests

**Monitoring:**
- System health
- Performance metrics
- Error rates
- User feedback

---

## Conclusion

This architecture document provides a comprehensive blueprint for building SS AI Server, a production-grade AI backend for WordPress plugins. The design follows enterprise best practices including:

- **Clean Architecture** for maintainability
- **Domain-Driven Design** for business logic
- **Dependency Injection** for testability
- **Interface-First Design** for flexibility
- **Modular Architecture** for extensibility
- **Cloud-Native Design** for scalability

The system is designed to:
- Support multiple AI providers and models
- Support multiple vector databases
- Scale horizontally and vertically
- Deploy on any platform
- Add new modules without core changes
- Maintain high performance and availability
- Ensure security and compliance

This architecture will serve as the foundation for building one of the best self-hosted AI servers for WordPress plugins.

---

**Document Version:** 1.0.0  
**Last Updated:** 2026-07-18  
**Status:** Final Design  
**Next Steps:** Implementation Planning