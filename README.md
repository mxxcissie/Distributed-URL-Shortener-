# URL Shortener

A production-style backend URL shortener built with FastAPI, PostgreSQL, Redis, Docker, pytest, and GitHub Actions CI.

This project focuses on backend engineering beyond basic CRUD, including persistent storage, redirect caching, Redis-backed rate limiting, automated testing, and CI validation.

## Live Demo

Base URL: `https://url-shortener-gfp0.onrender.com`

## Deployment

- Deployed on Render (cloud platform)
- Uses managed PostgreSQL for persistent storage
- Redis is optional in cloud deployment and used locally for caching/rate limiting when available
- Environment-based configuration enables seamless switching between local, Docker, and cloud environments

## Quick Test

```bash
curl https://url-shortener-gfp0.onrender.com/health
curl -X POST "https://url-shortener-gfp0.onrender.com/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url":"https://www.google.com"}'
```

## Why This Project

This project was built to simulate a production-style backend system rather than a simple CRUD app. It focuses on real-world backend concerns such as performance optimization, fault tolerance, and environment portability.

Key goals:
- Design a scalable API with clear request/response contracts
- Introduce caching and rate limiting as system-level concerns
- Support multiple runtime environments (local, Docker, cloud)
- Ensure reliability through automated testing and CI validation

## Features

- Create short URLs with `POST /shorten`
- Redirect short URLs with `GET /{short_code}`
- Track click counts with `GET /stats/{short_code}`
- Cache redirect lookups using Redis
- Protect the create endpoint with Redis-backed rate limiting
- Run the full stack locally with Docker Compose
- Validate backend behavior with pytest and GitHub Actions CI

## Backend Highlights

- Designed RESTful APIs using FastAPI for URL creation, redirection, and analytics
- Implemented PostgreSQL-backed persistence for durable storage of URL mappings
- Integrated Redis for caching and rate limiting with graceful fallback when unavailable
- Containerized the application using Docker Compose for consistent local development
- Built automated test coverage with pytest to validate core workflows
- Configured GitHub Actions CI to run tests on every push and pull request

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
app/       # backend application code
tests/     # automated tests
scripts/   # helper scripts such as seed data
```

## Environment Variables

- `ENV`
- `DATABASE_URL`
- `REDIS_URL`
- `BASE_URL`
- `PORT`

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
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

### Run App Locally (Services in Docker)
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

### Run Tests
```bash
pytest -v
```

### Seed Sample Data
```bash
python -m scripts.seed
```

### Quick Demo Flow
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

## Architecture

```text
Client / Browser
      ↓
FastAPI API Service
      ↓
Redis (cache + rate limiting)
      ↓
PostgreSQL (persistent storage)
```

### Request Flow

#### Create Short URL (`POST /shorten`)
- Request enters FastAPI
- Redis-backed rate limiter validates request frequency
- Short code is generated and checked for uniqueness
- Mapping is stored in PostgreSQL

#### Redirect (`GET /{short_code}`)
- FastAPI checks Redis cache for the short code
- On cache hit → return redirect immediately (low latency)
- On cache miss:
  - Query PostgreSQL
  - Store result in Redis for future requests
  - Increment click count
  - Return redirect response

#### Stats (`GET /stats/{short_code}`)
- Retrieve URL metadata and click count from PostgreSQL

## Design Notes

- PostgreSQL is used for durable storage of URL mappings and analytics
- Redis improves performance for read-heavy redirect traffic
- Rate limiting is applied only to POST /shorten to prevent abuse
- Click counts are updated even on cache hits to maintain consistency
- Short codes are generated randomly and checked for uniqueness
- Designed Redis as an optional dependency, enabling the service to remain fully functional in environments without cache infrastructure

## Future Improvements

- Introduce background workers for asynchronous click tracking
- Add distributed rate limiting using centralized cache
- Implement custom aliases and expiration policies
- Build analytics aggregation pipeline for high-volume traffic
- Deploy multi-instance setup with load balancing