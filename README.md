# Your Cook

Your Cook is a full-stack recipe manager with authentication, categories, tags, and recipe statistics.

The project consists of:
- `app/`: FastAPI backend
- `frontend/`: Vue 3 + Vite frontend
- `tests/`: backend tests with `pytest`
- `app/alembic/`: database migrations

## Stack

- Backend: FastAPI, SQLAlchemy 2, Pydantic 2, Alembic
- Auth: JWT + bcrypt
- Frontend: Vue 3, Pinia, Vue Router, Vite, Tailwind CSS
- Database: SQLite by default, PostgreSQL-ready via `DATABASE_URL`

## Features

- user registration and login
- personal recipes per user
- recipe categories
- tags and recipe statistics
- paginated recipe list
- protected API endpoints

## Requirements

- Python 3.11+
- Node.js 18+

## Quick Start

### 1. Backend setup

Create `.env` in the project root:

```env
SECRET_KEY=replace-with-a-random-string-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=sqlite:///./recipes.db
CORS_ORIGINS=["http://localhost:5173","http://localhost:5174","http://localhost:5175","http://localhost:3000","http://127.0.0.1:5173"]
```

Install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Start backend:

```bash
uvicorn app.main:app --reload
```

Backend URLs:
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Frontend setup

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Install dependencies and start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:
- app: `http://localhost:5173`

## Docker

If you prefer Docker:

```bash
docker-compose up --build
```

## Tests

Backend tests:

```bash
python -m pytest -q
```

## Useful Commands

Backend linting:

```bash
ruff check app tests
ruff format app tests
```

Frontend production build:

```bash
cd frontend
npm run build
```

## API Overview

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Recipes

- `GET /recipes/`
- `POST /recipes/`
- `GET /recipes/{id}`
- `PUT /recipes/{id}`
- `DELETE /recipes/{id}`
- `GET /recipes/stats`
- `GET /recipes/tags`
- `GET /recipes/tag/{tag_name}`

### Categories

- `GET /categories`
- `POST /categories`
- `GET /categories/{id}`
- `PUT /categories/{id}`
- `DELETE /categories/{id}`

## Notes

- `SECRET_KEY` is required and must be at least 32 characters long.
- The backend no longer auto-creates tables on import; use Alembic migrations.
- CORS is configured through `CORS_ORIGINS`.
- Frontend API URL is configured through `VITE_API_BASE_URL`.

## License

MIT
