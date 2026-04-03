# URL Shortener

A production-style backend URL shortener built with FastAPI, PostgreSQL, Redis, Docker, pytest, and GitHub Actions CI.

## Features

- Create short URLs with `POST /shorten`
- Redirect short URLs with `GET /{short_code}`
- Track click counts with `GET /stats/{short_code}`
- Cache redirect lookups using Redis
- Protect the create endpoint with Redis-backed rate limiting
- Run the full stack locally with Docker Compose
- Validate the backend with automated pytest tests and GitHub Actions CI
- Includes simple request logging and improved error handling for backend observability

## Architecture

- Redirect requests first check Redis for cached URL resolution. On cache miss, the app reads from PostgreSQL, stores the result in Redis, increments click count, and returns a redirect response.

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