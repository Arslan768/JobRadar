# Milestone 1 — Project Skeleton

**Status:** ✅ Complete · **Date:** 2026-07-14

## Goal

Stand up a modern, strictly-typed Python project before writing any real features: dependency management with uv, configuration via pydantic-settings, a minimal FastAPI app with health endpoints, and linting/type-checking that stays honest from day one. Everything later (database, auth, CI) builds on this foundation.

## What was built

- **uv-managed project** — `pyproject.toml` as the single source of truth, `uv.lock` committed for reproducible installs, Python pinned via `.python-version`.
- **`app/config.py`** — a `Settings` class (pydantic-settings) that loads from `.env`, exposed through a `get_settings()` function cached with `functools.lru_cache`.
- **`app/main.py`** — FastAPI app with four routes: `/` (welcome), `/health` (app name + version), `/health/live` (liveness), `/health/ready` (readiness). Routes receive settings via `Depends(get_settings)` rather than importing a module-level object.
- **Tooling** — ruff (lint + format) and mypy in `strict` mode, both configured in `pyproject.toml`.
- **Hygiene** — `.env` gitignored with a committed `.env.example` template; `__pycache__/`, `.venv/`, and tool caches ignored.

## Key concepts

- **pydantic-settings over `os.environ`**: settings are declared once with types and defaults, validated at startup (a typo'd `DEBUG=fales` fails loudly instead of silently being truthy), and documented by the class itself.
- **`lru_cache` on `get_settings()`**: the `.env` file is read once per process, and tests can clear the cache or override the dependency to inject test config.
- **`Depends(get_settings)` over module-level import**: FastAPI's `dependency_overrides` can swap the settings provider in tests — but only for code that receives settings as a dependency. Module-level imports are frozen at import time. The module-level `settings` object exists only for `FastAPI(title=...)`, which runs at import.
- **`uv run`**: executes a command inside the project venv (creating/syncing it from the lockfile first), so the venv never needs manual activation.
- **Liveness vs readiness**: `/health/live` answers "is the process up?"; `/health/ready` will later answer "can it serve traffic?" (e.g., is the database reachable?). Orchestrators and platforms like Render treat these differently.

## Decisions

- **Python 3.13, strict mypy from day 1** — started on 3.14, downgraded to 3.13 for wheel availability of C-extension packages (asyncpg comes in Milestone 2). Strict typing is cheap to adopt while the codebase is tiny and miserable to retrofit.
- **Ruff with a widened rule set** (`E`, `W`, `F`, `I`, `B`, `UP`, `SIM`) instead of the narrow defaults — import sorting, bug-prone-pattern detection, and modern-syntax enforcement for free.

## Problems hit

- **`uv sync` failed with "Access is denied" when switching 3.14 → 3.13.** Windows locks an `.exe` while any process runs from it, and a `python.exe` from `.venv` was still alive. Killing it once wasn't enough — the VS Code Python extension kept respawning the interpreter within a second. Fix: kill the process and delete `.venv` in a tight retry loop, then `uv sync` recreated it cleanly. Lesson: on Windows, stop the dev server (and expect VS Code to fight back) before rebuilding a venv.

## How to verify

```powershell
uv run ruff check .        # no issues
uv run mypy app            # strict mode, no errors
uv run uvicorn app.main:app --reload
# then:
curl http://127.0.0.1:8000/health        # {"status":"healthy","app":...,"version":...}
curl http://127.0.0.1:8000/health/ready  # {"status":"ready"}
# http://127.0.0.1:8000/docs shows the interactive API docs
```
