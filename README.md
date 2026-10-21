# TaskFlow — Dockerized Task Manager

A portfolio-ready task management application built with **FastAPI**, **PostgreSQL**, **Docker**, and **Docker Compose**.

## Features
- Create, list, complete, and delete tasks
- Responsive web UI and documented REST API
- PostgreSQL persistence via a named Docker volume
- Database readiness and API health checks
- Non-root application container
- GitHub Actions CI: tests, Compose validation, image build

## Architecture
```
Browser → FastAPI container → PostgreSQL container
               ↑                   ↑
         port 8000           named volume
```

## Quick start
1. Install Docker Desktop and start Docker Engine.
2. Copy `.env.example` to `.env` and change `POSTGRES_PASSWORD`.
3. Run `docker compose up --build -d`.
4. Visit http://localhost:8000 and http://localhost:8000/docs.
5. Run `docker compose ps` to inspect health and `docker compose logs -f api` to inspect logs.
6. Stop with `docker compose down`. Data remains in the volume. **Warning:** `docker compose down -v` deletes database data.

> The included password fallback is for local demos only. Never use it for production.

## API
| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | DB connectivity check |
| GET | `/api/tasks` | List tasks |
| POST | `/api/tasks` | Create task (`{"title":"Learn Docker"}`) |
| PATCH | `/api/tasks/{id}` | Update status (`{"completed":true}`) |
| DELETE | `/api/tasks/{id}` | Delete task |

## Run tests without Docker
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## What to practice
1. Explain the difference between an image and a container.
2. Explain why the database uses a named volume.
3. Use `docker compose exec db psql -U taskflow -d taskflow` and run `SELECT * FROM tasks;`.
4. Explain `depends_on` and the database health check.
5. Make your own change: add task priorities, a filter, or a due date.
6. Capture a screenshot of the UI and add it to this README.

## GitHub
```bash
git init
git add .
git commit -m "Build Dockerized task manager with FastAPI and PostgreSQL"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/taskflow-docker.git
git push -u origin main
```
Create an empty repository on GitHub first and replace `YOUR_USERNAME`.

## CV description
**TaskFlow — Containerized Task Management Application**: Built a REST API with FastAPI and PostgreSQL, orchestrated services with Docker Compose, implemented persistent storage, health checks, automated tests, and GitHub Actions CI.

## Next steps
For a stronger DevOps portfolio, add Nginx as a reverse proxy, database migrations with Alembic, and deployment documentation.
