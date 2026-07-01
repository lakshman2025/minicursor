# Simple Todo API

A simple FastAPI todo application with in-memory storage.

## Features

- Health check endpoint
- Create todos
- List todos
- Get a todo by ID
- Partially update todos
- Delete todos
- Interactive API docs at `/docs`

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Then open:

- API root: http://127.0.0.1:8765/
- Health check: http://127.0.0.1:8765/health
- Docs: http://127.0.0.1:8765/docs

## Test

```bash
pytest tests
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/todos` | List all todos |
| POST | `/todos` | Create a todo |
| GET | `/todos/{todo_id}` | Get one todo |
| PATCH | `/todos/{todo_id}` | Update one todo |
| DELETE | `/todos/{todo_id}` | Delete one todo |
