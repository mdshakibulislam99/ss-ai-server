# SS AI Server

Production-grade AI backend for WordPress image similarity search.

## Features

- **Image Similarity Search**: Find visually similar products using AI-powered embeddings
- **OpenCLIP Integration**: State-of-the-art vision AI models for embedding generation
- **FAISS Vector Store**: High-performance similarity search with Facebook AI Similarity Search
- **Batch Processing**: Index multiple products simultaneously
- **RESTful API**: Clean, versioned API with comprehensive endpoints
- **Clean Architecture**: Domain-driven design with dependency injection
- **Production Ready**: Logging, monitoring, health checks, and error handling

## Quick Start

### Prerequisites

- Python 3.11+
- pip or poetry
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/mdshakibulislam99/ss-ai-image-search-ai-side.git
cd ss-ai-image-search-ai-side

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Copy environment configuration
cp .env.example .env

# Edit .env with your settings
nano .env
```

### Running Locally

```bash
# Development mode with auto-reload
uvicorn ss_ai_server.main:app --reload --host 0.0.0.0 --port 8000

# Or using the CLI
ss-ai-server
```

### Access the API

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Root Endpoint**: http://localhost:8000/

## API Endpoints

### Search
- `POST /api/v1/search/image` - Search by image upload
- `GET /api/v1/search/health` - Search service health

### Index
- `POST /api/v1/index/product` - Index a single product
- `POST /api/v1/index/batch` - Batch index products
- `DELETE /api/v1/index/product/{product_id}` - Delete product embeddings

### Admin
- `GET /api/v1/admin/stats` - System statistics
- `GET /api/v1/admin/models` - Available AI models
- `POST /api/v1/admin/cache/clear` - Clear cache
- `GET /api/v1/admin/vector-store/stats` - Vector store statistics
- `POST /api/v1/admin/vector-store/backup` - Backup vector store
- `POST /api/v1/admin/vector-store/restore` - Restore vector store
- `GET /api/v1/admin/queue` - Queue status
- `POST /api/v1/admin/queue/clear` - Clear queue

### Health
- `GET /api/v1/health` - Overall health check
- `GET /api/v1/health/ready` - Readiness probe
- `GET /api/v1/health/live` - Liveness probe

## Deployment

### Deploy to Render

1. **Push to GitHub** (already done)
   ```bash
   git push origin main
   ```

2. **Create Render Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the repository: `ss-ai-image-search-ai-side`
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables**
   - Render will auto-configure variables from `render.yaml`
   - The `SECRET_KEY` will be auto-generated
   - Ensure the `PORT` environment variable is set (Render does this automatically)

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Your service will be available at `https://ss-ai-server.onrender.com`

### Manual Deployment

If you prefer manual deployment or need to deploy elsewhere:

```bash
# Install production dependencies
pip install -e .

# Run with uvicorn
uvicorn ss_ai_server.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment

```bash
# Build image
docker build -t ss-ai-server .

# Run container
docker run -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e DATABASE_TYPE=sqlite \
  -e VECTOR_STORE_PATH=/data/vector_store \
  -v $(pwd)/data:/data \
  ss-ai-server
```

## Configuration

### Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `ENVIRONMENT`: `development` or `production`
- `DATABASE_TYPE`: `sqlite` or `postgresql`
- `VECTOR_STORE_TYPE`: `faiss`, `hnswlib`, or `chromadb`
- `AI_DEFAULT_PROVIDER`: `openclip` (default)
- `AI_DEFAULT_MODEL`: `ViT-B-32` (default)
- `SECRET_KEY`: Change in production!
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### Production Settings

For production deployment:
1. Set `ENVIRONMENT=production`
2. Set `DEBUG=false`
3. Change `SECRET_KEY` to a secure random value
4. Configure `CORS_ORIGINS` to your domain
5. Use PostgreSQL for database
6. Enable Redis for queue and cache
7. Set appropriate `WORKERS` count (2-4 recommended for Render starter plan)

## Architecture

The project follows Clean Architecture principles:

```
src/ss_ai_server/
├── domain/           # Business logic (entities, interfaces, services)
├── application/      # Use cases and DTOs
├── infrastructure/   # External implementations (AI, DB, cache)
└── presentation/     # API endpoints and middleware
```

### Key Components

- **AI Provider**: OpenCLIP for image embeddings
- **Vector Store**: FAISS for similarity search
- **Repository**: Product metadata storage
- **Cache**: In-memory caching (Redis in production)
- **Queue**: Background job processing

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_search_service.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## API Usage Examples

### Search by Image

```bash
curl -X POST "https://your-api.onrender.com/api/v1/search/image" \
  -H "X-API-Key: your-api-key" \
  -F "file=@image.jpg"
```

### Index Product

```bash
curl -X POST "https://your-api.onrender.com/api/v1/index/product" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "123",
    "site_id": "site-1",
    "title": "Product Name",
    "featured_image_url": "https://example.com/image.jpg",
    "gallery_image_urls": ["https://example.com/image2.jpg"]
  }'
```

### Get Statistics

```bash
curl "https://your-api.onrender.com/api/v1/admin/stats"
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'pydantic_settings'**
   - Solution: Install dependencies with `pip install -e ".[dev]"`

2. **Out of memory on Render**
   - Reduce `WORKERS` to 1 or 2
   - Use smaller AI model (e.g., `ViT-B-32` instead of `ViT-L-14`)
   - Upgrade Render plan for more RAM

3. **Slow first request**
   - Normal: Model loading takes time on first request
   - Consider using a warmup script or keep-alive pings

4. **Vector store not persisting**
   - Ensure disk is mounted at `/data` on Render
   - Check `VECTOR_STORE_PATH` environment variable

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/mdshakibulislam99/ss-ai-image-search-ai-side/issues
- Documentation: https://docs.ss-ai-server.com

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.