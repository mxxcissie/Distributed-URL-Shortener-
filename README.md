# URL Shortener

A production-style distributed URL shortener demonstrating caching, rate limiting, load balancing, and horizontal scalability. Built with a FastAPI backend, React frontend, PostgreSQL, Redis, Docker, and CI/CD (GitHub Actions).

## Live Demo

- Frontend: https://url-shortener-frontend-av1x.onrender.com  
- Backend API: https://url-shortener-gfp0.onrender.com/docs

## Frontend

A lightweight React frontend provides a simple interface for:

- Creating short URLs
- Viewing generated links
- Retrieving click statistics

The frontend communicates with the deployed FastAPI backend via REST APIs, enabling end-to-end interaction with the distributed system.

## Deployment

- Deployed on Render (cloud platform)
- Uses managed PostgreSQL as the persistent source of truth
- Redis is used as a shared cache and coordination layer in distributed environments, with graceful fallback when unavailable
- Environment-based configuration enables seamless switching between local, Docker, and cloud deployments
- Frontend deployed as a static site on Render, providing a user interface for interacting with backend APIs

## Quick Test

- Frontend:
  - Open the web UI: https://url-shortener-frontend-av1x.onrender.com

- Backend API:
```bash
curl https://url-shortener-gfp0.onrender.com/health
curl -X POST "https://url-shortener-gfp0.onrender.com/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url":"https://www.google.com"}'
```

## Why This Project

This project was built to simulate a production-style distributed system incorporating real-world backend and system design principles, rather than a simple CRUD application.

Key goals:

- Design a scalable API with clear request/response contracts
- Introduce caching and rate limiting as core system-level concerns
- Support multiple runtime environments (local, Docker, cloud)
- Ensure reliability through automated testing and CI validation
- Provide end-to-end interaction through a lightweight frontend

## System Design Summary

- Stateless FastAPI services behind an Nginx load balancer
- PostgreSQL as the single source of truth for durability and consistency
- Redis used for shared caching and distributed rate limiting
- Horizontal scaling achieved via multiple stateless application replicas
- Graceful degradation when Redis is unavailable

## Features

- Create short URLs via API (`POST /shorten`) or through the frontend UI
- Redirect short URLs with `GET /{short_code}`
- Track click counts with `GET /stats/{short_code}`
- Cache redirect lookups using Redis
- Enforce request rate limits using Redis-backed distributed rate limiting
- Run the full stack locally using Docker Compose
- Validate system behavior with pytest and GitHub Actions CI
- Support horizontal scaling via stateless application instances behind a load balancer
- Benchmark cache performance (miss vs. hit latency)

## Cache Performance Benchmark

To validate the effectiveness of Redis caching, redirect latency was measured for cache misses (first request) and cache hits (subsequent requests).

Run locally:
```bash
python scripts/benchmark_cache.py
```

Example results:

- Cache miss latency: ~30–45 ms
- Average cache hit latency: ~6 ms
- Approximate speedup: ~5–7×

This demonstrates that Redis caching significantly reduces redirect latency and minimizes repeated database queries in read-heavy workloads.

## Backend Highlights

- Designed RESTful APIs using FastAPI for URL creation, redirection, and analytics
- Implemented PostgreSQL-backed persistence as the durable source of truth for URL mappings and analytics
- Integrated Redis for shared caching and distributed rate limiting with graceful fallback when unavailable
- Containerized and orchestrated multiple application instances using Docker Compose to simulate a distributed environment
- Built automated test coverage with pytest to validate core workflows
- Configured GitHub Actions CI to run tests on every push and pull request
- Introduced Nginx as a load balancer to distribute traffic across multiple FastAPI instances
- Validated Redis caching effectiveness using benchmark measurements (cache miss vs. hit latency)

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- React
- Docker / Docker Compose
- Nginx
- pytest
- GitHub Actions

## Project Structure

```text
app/                  # FastAPI backend application
  __init__.py
  main.py             # application entrypoint
  core/               # application configuration and environment setup
    __init__.py
    config.py
  services/           # external services and infrastructure logic
    __init__.py
    cache.py
    rate_limiter.py
  crud.py             # database operations
  database.py         # database connection and setup
  models.py           # SQLAlchemy models
  schemas.py          # Pydantic schemas
  utils.py            # helper utilities

frontend/             # React frontend (Vite, API integration)
nginx/                # Nginx configuration for load balancing
tests/                # automated tests

scripts/
  seed.py             # sample data loader
  benchmark_cache.py  # measures cache miss vs. hit latency

docker-compose.yml    # service orchestration
Dockerfile            # app container definition
requirements.txt      # backend dependencies
```

## Environment Variables

- `ENV` — runtime environment (development / production)
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection string (optional)
- `BASE_URL` — base URL for generated short links
- `PORT` — application port

## Health Check

The service exposes a health check endpoint:
```http
GET /health
```
```bash
curl http://127.0.0.1:8000/health
```

## How to Run Locally

### Run Full Stack with Docker

```bash
docker compose up --build
```
Open:
- Backend API docs: http://127.0.0.1:8000/docs
- Backend health: http://127.0.0.1:8000/health

### Run Backend Locally (Services in Docker)

- Start required services:
```bash
docker compose up -d db redis
```
- Activate virtual environment:
```bash
source venv/bin/activate
```
- Install dependencies:
```bash
pip install -r requirements.txt
```
- Run backend:
```bash
uvicorn app.main:app --reload
```

### Run Frontend Locally

```bash
cd frontend
npm install
npm run dev
```
Open:
Frontend: http://localhost:5173

## Run Tests

```bash
pytest -v
```

## Seed Sample Data

```bash
python -m scripts.seed
```

## Quick Demo Flow

- Start the full stack:
```bash
docker compose up --build
```
- Open the frontend UI: http://localhost:5173
- Enter a URL (e.g., https://www.google.com) and generate a short link
- Open the returned short URL in your browser to verify redirection
- Check click statistics using the UI or via: `GET /stats/{short_code}`

### Optional (API-level testing)

- Open API docs: http://127.0.0.1:8000/docs
- Create a short URL using `POST /shorten`
```json
{
  "original_url": "https://www.google.com"
}
```

## Distributed Architecture

This project demonstrates a horizontally scalable, distributed system with a React frontend and a FastAPI backend running locally using Docker Compose.

The architecture is designed for scalability, fault tolerance, and consistent behavior across multiple application instances.

### Components

- Nginx load balancer
- 3 FastAPI application replicas
- PostgreSQL as the durable, shared source of truth
- Redis for shared caching and distributed rate limiting

### System Request Flow

1. User interacts with the React frontend or sends a request directly to Nginx
2. Nginx routes the request to one FastAPI replica
3. The selected instance processes the request and interacts with shared PostgreSQL and Redis
4. Redirect requests use Redis as a cache-first lookup layer
5. Rate limiting is enforced globally across replicas through Redis

## Architecture

```text
React Frontend / Browser
      ↓
Nginx Load Balancer
      ↓
+-----------------------------+
|  FastAPI Application Layer  |
|  - app1                     |
|  - app2                     |
|  - app3                     |
+-----------------------------+
      ↓
+--------------------------------+
|  Shared Infrastructure         |
|  - Redis (cache + rate limit)  |
|  - PostgreSQL (source of truth)|
+--------------------------------+
```

## Key Design Decisions

- Introduced Nginx as a load balancer to distribute traffic across multiple FastAPI instances
- Ensured a stateless application design so any instance can handle any request
- Used Redis as a shared cache and coordination layer for distributed rate limiting
- Used PostgreSQL as the single source of truth for URL mappings and analytics
- Enforced uniqueness of short codes at the database level to ensure correctness under concurrent distributed writes

## Distributed Validation

- Confirmed load balancing by observing requests handled across multiple instances
- Verified shared Redis cache behavior across replicas
- Validated global rate limiting enforcement across instances
- Ensured consistent state via shared PostgreSQL storage

## Request Flow

### Create Short URL (`POST /shorten`)

- Request enters the FastAPI service
- Redis-backed rate limiter validates request frequency
- A short code is generated and checked for uniqueness
- Mapping is stored in PostgreSQL

### Redirect (`GET /{short_code}`)

- FastAPI checks Redis cache for the short code
- On cache hit → return redirect immediately (low latency)
- On cache miss:
  - Query PostgreSQL
  - Store result in Redis for future requests
  - Increment click count
  - Return redirect response

### Stats (`GET /stats/{short_code}`)

- Retrieve URL metadata and click count from PostgreSQL

## Design Notes

- PostgreSQL serves as the single source of truth for URL mappings and analytics, ensuring consistency across all application instances
- Redis is used as a shared cache layer to optimize read-heavy redirect traffic and reduce database load
- Cache effectiveness is validated through latency benchmarking, demonstrating faster response times for repeated requests
- Rate limiting is enforced using Redis to ensure global limits across all replicas, preventing per-instance bypass
- The application is stateless, allowing any FastAPI instance to handle any request
- Click counts are updated even on cache hits to maintain consistency between cache and persistent storage
- Short codes are generated randomly and validated with a database uniqueness constraint to avoid collisions
- Redis is treated as an optional dependency, with graceful fallback to database queries to maintain system availability
- Nginx distributes incoming requests across multiple FastAPI instances for scalability and fault tolerance
- The system supports horizontal scaling by adding more application instances without changing the client interface

## Future Improvements

- Introduce background workers for asynchronous click tracking
- Enhance rate limiting with sliding window or token bucket algorithms
- Implement custom aliases and expiration policies
- Build analytics aggregation pipeline for high-volume traffic
- Deploy multi-instance setup to the cloud using container orchestration (e.g., Kubernetes)