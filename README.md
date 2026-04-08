# URL Shortener

A production-style backend URL shortener built with a distributed architecture using FastAPI, PostgreSQL, Redis, Docker, pytest, and GitHub Actions CI.

This project emphasizes backend engineering beyond basic CRUD, focusing on performance optimization, fault tolerance, and production-ready system design.

## Live Demo

Base URL: `https://url-shortener-gfp0.onrender.com`

## Deployment

- Deployed on Render (cloud platform)
- Uses managed PostgreSQL as the persistent source of truth
- Redis is used as a shared cache and coordination layer in distributed environments, with graceful fallback when unavailable
- Environment-based configuration enables seamless switching between local, Docker, and cloud deployments

## Quick Test

```bash
curl https://url-shortener-gfp0.onrender.com/health
curl -X POST "https://url-shortener-gfp0.onrender.com/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url":"https://www.google.com"}'
```

## Why This Project

This project was built to simulate a production-style backend system incorporating distributed system principles, rather than a simple CRUD application.

Key goals:
- Design a scalable API with clear request/response contracts
- Introduce caching and rate limiting as core system-level concerns
- Support multiple runtime environments (local, Docker, cloud)
- Ensure reliability through automated testing and CI validation

## System Design Summary

- Stateless FastAPI services behind an Nginx load balancer
- PostgreSQL as the single source of truth for durability and consistency
- Redis used for shared caching and distributed rate limiting
- Horizontal scaling achieved via multiple application replicas
- Graceful degradation when Redis is unavailable

## Features

- Create short URLs with `POST /shorten`
- Redirect short URLs with `GET /{short_code}`
- Track click counts with `GET /stats/{short_code}`
- Cache redirect lookups using Redis
- Protect the create endpoint with Redis-backed rate limiting
- Run the full stack locally with Docker Compose
- Validate backend behavior with pytest and GitHub Actions CI
- Supports horizontal scaling through stateless application instances behind a load balancer

## Backend Highlights

- Designed RESTful APIs using FastAPI for URL creation, redirection, and analytics
- Implemented PostgreSQL-backed persistence as the durable source of truth for URL mappings and analytics
- Integrated Redis for shared caching and distributed rate limiting with graceful fallback when unavailable
- Containerized and orchestrated multiple application instances using Docker Compose to simulate a distributed environment
- Built automated test coverage with pytest to validate core workflows
- Configured GitHub Actions CI to run tests on every push and pull request
- Introduced Nginx as a load balancer to distribute traffic across multiple FastAPI instances

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Docker / Docker Compose
- pytest
- GitHub Actions

## Project Structure

```text
app/                  # FastAPI application code
nginx/                # Nginx configuration for load balancing
tests/                # automated tests
scripts/              # helper scripts (e.g., seed data)
docker-compose.yml    # service orchestration
Dockerfile            # app container definition
requirements.txt      # dependencies
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

### Option 1 — Run Full Stack with Docker
```bash
docker compose up --build
```
Open:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

### Option 2 — Run App Locally (Services in Docker)
- Start required services:
```bash
docker compose up -d db redis
```
- Activate virtual environment:
```bash
source venv/bin/activate
```
- Run the application:
```bash
uvicorn app.main:app --reload
```

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
- Open API docs:
http://127.0.0.1:8000/docs
- Create a short URL using `POST /shorten`
{
  "original_url": "https://www.google.com"
}
- Open the returned short URL in your browser
- Check click statistics: `GET /stats/{short_code}`

## Distributed Architecture

This project demonstrates a horizontally scalable, distributed backend architecture running locally using Docker Compose.

This architecture enables horizontal scaling, fault tolerance, and consistent behavior across multiple application instances.

### Components
- Nginx load balancer
- 3 FastAPI application replicas
- PostgreSQL as the durable, shared source of truth
- Redis for shared caching and distributed rate limiting

### System Request Flow
1. Client sends request to Nginx
2. Nginx routes request to one FastAPI replica
3. The selected instance processes the request and interacts with shared PostgreSQL and Redis
4. Redirect requests use Redis as a cache-first lookup layer
5. Rate limiting is enforced globally across replicas through Redis

## Architecture

```text
Client / Browser
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
- Ensured stateless application design so any instance can handle any request
- Used Redis as a shared cache and coordination layer for distributed rate limiting
- Used PostgreSQL as the single source of truth for URL mappings and analytics
- Enforced uniqueness of short codes at the database level to ensure correctness under concurrent distributed writes

## Distributed Validation

- confirmed load balancing by observing requests handled across multiple instances
- verified shared Redis cache behavior across replicas
- validated global rate limiting enforcement across instances
- ensured consistent state via shared PostgreSQL storage

## Request Flow

### Create Short URL (`POST /shorten`)
- Request enters FastAPI
- Redis-backed rate limiter validates request frequency
- Short code is generated and checked for uniqueness
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

- PostgreSQL is used as the single source of truth for URL mappings and analytics, ensuring consistency across all application instances
- Redis is used as a shared cache layer to optimize read-heavy redirect traffic and reduce database load
- Rate limiting is enforced using Redis to ensure global limits across all replicas, preventing per-instance bypass
- The application is designed to be stateless, allowing any FastAPI instance to handle any request
- Click counts are updated even on cache hits to maintain consistency between cache and persistent storage
- Short codes are generated randomly and validated with a database uniqueness constraint to avoid collisions
- Redis is treated as an optional dependency, with graceful fallback to database queries to maintain system availability
- Nginx is used as a load balancer to distribute incoming requests across multiple FastAPI instances for scalability and fault tolerance
- The system is designed to support horizontal scaling by adding more application instances without changing the client interface

## Future Improvements

- Introduce background workers for asynchronous click tracking
- Enhance rate limiting with sliding window or token bucket algorithms
- Implement custom aliases and expiration policies
- Build analytics aggregation pipeline for high-volume traffic
- Deploy multi-instance setup to cloud using container orchestration (e.g., Kubernetes)