# Backend README

This backend is part of the `fastAPI-TS-TodoApp` project and is built with FastAPI and SQLAlchemy.

## Required tools

- Docker
- Docker Compose
- Python 3.12+ if you want to run tests locally

## Environment files

Two environment files are required for the backend to run in Docker:

- `backend/.env.backend`
- `backend/.env.db`

These files should be created from the provided examples:

```bash
cd backend
cp .env.backend.example .env.backend
cp .env.db.example .env.db
```

### What these files do

- `.env.backend` contains the application database URL and other backend secrets.
- `.env.db` contains PostgreSQL credentials and database name for the `db` container.

> Do not commit `.env.backend` or `.env.db` to version control. Only `.env.backend.example` and `.env.db.example` should be tracked.

## Docker Compose

The root `docker-compose.yml` file defines two services:

- `db` — PostgreSQL database
- `backend` — FastAPI app built from `backend/Dockerfile`

The backend service reads environment variables from `backend/.env.backend`.

### Start the backend with Docker

From the project root:

```bash
docker-compose up --build backend
```

Or rebuild both services and start everything:

```bash
docker-compose up --build
```

### Stop the containers

```bash
docker-compose down
```

## Backend container details

The backend Dockerfile uses:

- `WORKDIR /app`
- copies `requirements.txt`
- installs dependencies
- copies the backend source code
- starts the app with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Accessing the API

Once the backend is running, the API should be available at:

- `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`

## Local testing

If you want to run tests locally inside the backend directory:

```bash
cd backend
source .venv/bin/activate
python -m pytest
```

## Notes

- Ensure your `.env.backend` file references the `db` hostname, not `localhost`, when running in Docker.
- Example `DATABASE_URL` value from `.env.backend.example`:

```text
DATABASE_URL = "postgresql+asyncpg://postgres:password@db:5432/tododb"
```

- The `db` service must be healthy before the backend starts. Docker Compose uses `depends_on` with `condition: service_healthy` for this.
