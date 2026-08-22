# Finora Backend Foundation

Finora is an AI-powered Financial Intelligence Platform. This repository contains the FastAPI backend foundation.

## Tech Stack
- **Python 3.11**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2.0**
- **Alembic** (Migrations)
- **Pydantic**
- **Docker & Docker Compose**

## Project Architecture
The project follows a clean architecture pattern:
- `api/routers/`: FastAPI routes organized by feature.
- `core/`: Global settings and security configurations.
- `db/`: Database session and base configuration.
- `models/`: SQLAlchemy declarative models.
- `schemas/`: Pydantic models for request/response validation.
- `repositories/`: Database query abstraction.
- `services/`: Business logic.

Request Flow: `Router -> Service -> Repository -> Database`

## Running with Docker (Recommended)

1. Rename `.env.example` to `.env` or just use the defaults:
```bash
cp .env.example .env
```
2. Build and start the containers:
```bash
docker-compose up -d --build
```
3. Run Alembic migrations to set up the database schema:
```bash
docker-compose exec api alembic upgrade head
```

## Available API Endpoints

- `GET /health` - Health check endpoint
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login to get an access token
- `GET /api/v1/auth/me` - Get current authenticated user details

Swagger UI documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).
