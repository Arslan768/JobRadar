# JobRadar

A job-search web app with live filters — deliberately AI-free. Browse aggregated job postings; filter by keyword, location, salary, and remote status; save searches behind a login. An admin ingestion command pulls postings from a public source into Postgres.

This is **app 1 of an 11-app learning curriculum**: the domain is intentionally boring so the engineering fundamentals (async database access, migrations, auth, testing, CI, deployment) get full attention. Once shipped, the generic parts become a template repository that later apps are born from.

## Stack

- **API:** FastAPI, strict typing (mypy `strict`), pydantic-settings, structured logging
- **Database:** PostgreSQL, SQLAlchemy (async), Alembic migrations
- **UI:** HTMX + Jinja — server-rendered, no JS build chain
- **Auth:** JWT, rate limiting
- **Testing:** pytest against a real test database
- **Ops:** Docker Compose, GitHub Actions CI, non-root production Dockerfile
- **Tooling:** uv, ruff

## Getting started

Requires [uv](https://docs.astral.sh/uv/) (it installs the pinned Python automatically).

```powershell
uv sync                    # create venv + install deps from the lockfile
copy .env.example .env     # then edit values as needed
uv run uvicorn app.main:app --reload
```

API docs at http://127.0.0.1:8000/docs, health check at `/health`.

## Development

```powershell
uv run ruff check .    # lint
uv run ruff format .   # format
uv run mypy app        # type-check (strict)
```

## Progress

Built milestone by milestone, each documented in [docs/milestones/](docs/milestones/):

| # | Milestone | Status |
|---|-----------|--------|
| 1 | [Project skeleton — uv, FastAPI, settings, health endpoints](docs/milestones/01-skeleton.md) | ✅ |
| 2 | Postgres + async SQLAlchemy + first Alembic migration | ⏳ |
| 3 | Job ingestion from a public source | — |
| 4 | Search API + HTMX/Jinja UI with filters and pagination | — |
| 5 | Users, JWT auth, saved searches, rate limiting | — |
| 6 | pytest suite against a real test database | — |
| 7 | Dockerfile, GitHub Actions CI, deploy (Render + Neon) | — |
| 8 | Extract the golden-skeleton template repo | — |
