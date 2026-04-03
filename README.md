# URL Shortener

A production-style backend URL shortener built with FastAPI, PostgreSQL, Redis, Docker, pytest, and GitHub Actions CI.

This project focuses on backend engineering beyond basic CRUD, including persistent storage, redirect caching, Redis-backed rate limiting, automated testing, and CI validation.

## Features

- Create short URLs with `POST /shorten`
- Redirect short URLs with `GET /{short_code}`
- Track click counts with `GET /stats/{short_code}`
- Cache redirect lookups using Redis
- Protect the create endpoint with Redis-backed rate limiting
- Run the full stack locally with Docker Compose
- Validate backend behavior with pytest and GitHub Actions CI

## Backend Highlights

- FastAPI-based REST API for URL creation, redirect handling, and analytics
- PostgreSQL as the durable source of truth for URL mappings and click counts
- Redis used for both redirect caching and rate-limit counters
- Docker Compose setup for reproducible multi-service local development
- Automated pytest coverage for core backend flows
- GitHub Actions CI to validate changes on push and pull request

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

app/       # backend application code
tests/     # automated tests
scripts/   # helper scripts such as seed data

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
- Run the application:
```bash
source venv/bin/activate
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

Client / Browser
      ↓
FastAPI API Service
      ↓
Redis (cache + rate limiting)
      ↓
PostgreSQL (persistent storage)

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

## Future Improvements

- Custom short URL aliases
- Expiration time for links
- Analytics dashboard
- Background processing for high-scale click tracking
- Deployment to cloud platform (e.g., Render, Fly.io)

## Why This Project

This project was designed to demonstrate backend engineering fundamentals beyond simple CRUD applications, including:

- API design and validation
- database persistence and schema design
- caching strategies
- rate limiting
- containerized development
- automated testing
- CI workflow integration