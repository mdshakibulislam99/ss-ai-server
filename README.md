# SS AI Server

AI backend for WordPress image similarity search.

## Deploy to Render

1. Push this repo to GitHub
2. Go to https://dashboard.render.com/ → New Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml`
5. Click Create Web Service

The API will be available at `https://your-app.onrender.com`.

## Local Development

```bash
pip install -e ".[dev]"
uvicorn ss_ai_server.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/search/image` | Search by image |
| POST | `/api/v1/index/product` | Index a product |
| POST | `/api/v1/index/batch` | Batch index products |
| DELETE | `/api/v1/index/product/{id}` | Delete product embeddings |
| GET | `/api/v1/admin/stats` | System stats |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| ENVIRONMENT | development | production or development |
| SECRET_KEY | - | Set in production |
| VECTOR_STORE_PATH | /data/vector_store | FAISS index path |

See `.env.example` for all options.