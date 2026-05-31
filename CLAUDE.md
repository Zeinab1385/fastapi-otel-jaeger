# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a small FastAPI service for a "Telemetry and Architecture Hub" user registration API. The application is split into three layers:

- `api.py` defines the FastAPI app, creates a singleton `UserServices`, and exposes `POST /register`.
- `service.py` contains business logic in `UserServices`, currently checking for duplicate email addresses before saving a user.
- `repository.py` contains `UserRepository`, which owns PostgreSQL connection settings and all SQL access through `psycopg2` with `RealDictCursor`.

The request flow is:

`POST /register` in `api.py` → `UserServices.register_new_user()` in `service.py` → `UserRepository.get_user_by_email()` / `save_user()` in `repository.py` → PostgreSQL `users` table.

## Development commands

The repository includes a local virtual environment at `.venv/`, but `requirements.txt` is currently empty even though the code imports FastAPI, Uvicorn, and psycopg2. If dependencies are missing, install them explicitly:

```bash
python -m pip install fastapi uvicorn psycopg2-binary
```

Run the API locally:

```bash
python -m uvicorn api:app --reload
```

Exercise the registration endpoint once the app and local PostgreSQL database are running:

```bash
curl -X POST http://127.0.0.1:8000/register \
  -H 'Content-Type: application/json' \
  -d '{"name":"Ada Lovelace","email":"ada@example.com"}'
```

Check syntax/import-time compilation without starting the server:

```bash
python -m py_compile api.py service.py repository.py
```

There is no test suite or configured lint command in this repository yet. If tests are added with pytest, conventional commands would be:

```bash
python -m pytest
python -m pytest path/to/test_file.py::test_name
```

## Database assumptions

`UserRepository` connects to PostgreSQL using hard-coded local settings:

- database: `telemetry_db`
- user: `postgres`
- host: `localhost`
- port: `5432`

The code expects a `users` table with at least `id`, `name`, and `email` columns. There are no migrations or schema files in the repository, so database setup must currently be inferred from the SQL in `repository.py`.

## Notes for future changes

- Keep the API/service/repository separation intact: HTTP concerns in `api.py`, business rules in `service.py`, SQL and connection handling in `repository.py`.
- `save_user()` should pass SQL parameters as a sequence compatible with `psycopg2` when modifying database code.
