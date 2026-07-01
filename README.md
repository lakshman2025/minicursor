# Minicursor

A small interactive coding agent that uses an LLM to plan and run tools (read/write files, search code, run shell commands). It runs as a **React UI + FastAPI backend** with conversations persisted in PostgreSQL. A standalone CLI / legacy web entry point (`agent.py`) is also available.

## Objectives

The project was developed to understand:

* Agent-based software architecture
* LLM reasoning and decision making
* Tool calling using an autonomous agent
* Context management across multiple iterations
* Execution loop between the agent and the runtime
* Autonomous software generation
* Persisting agent state across server restarts

## System Architecture

```
React UI (frontend/)  →  FastAPI (backend/)  →  PostgreSQL
                              ↓
                    Harness → AgentLLM → Tools
```

**Agent core** (project root):

* **Harness** – Controls the execution loop, executes tools, and updates agent state.
* **Agent LLM** – Decides the next action (tool call, casual reply, or finish).
* **Context Builder** – Builds the prompt from conversation and tool history.
* **Tool Registry** – Stores and executes available tools.

**Backend** (`backend/`):

* **Sessions** – Chat metadata (title, workspace, active flag).
* **Agent State** – Conversation and tool history stored as JSONB in PostgreSQL.
* **Repositories / Services** – Database access and business rules.

## Workflow

1. The user opens a chat session in the UI (or sends a message via API).
2. The backend loads `agent_state` for that session from the database.
3. The Harness appends the user message and runs the agent loop.
4. The Agent LLM decides: reply casually, call a tool, or finish.
5. Tool results are stored in `agent_state.tool_history`.
6. The loop continues until the task is complete.
7. The assistant reply is saved to `agent_state.messages` and returned to the UI.

## Implemented Tools

* List files
* Create directories
* Read / write files
* Search code
* Execute shell commands

## Features

* Autonomous decision-making using an LLM
* Multi-step reasoning through an iterative execution loop
* Casual chat and coding tasks in the same flow
* Session-based chats with persistent history
* React chat UI with sidebar (new / remove / select sessions)
* FastAPI REST API (`/sessions`, `/sessions/{id}/chat`)
* Soft-delete sessions (`active = false`)

## Prerequisites

- Python 3.10 or newer
- Node.js 18+ (for the React frontend)
- PostgreSQL
- An LLM API endpoint and API key

## Setup

### 1. Project root

```bash
cd minicursor
```

### 2. Python virtual environment

```bash
python -m venv env
```

Windows (PowerShell):

```powershell
.\env\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source env/bin/activate
```

### 3. Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 5. Environment file

Create a `.env` file in the **project root**:

```env
LLM_ENDPOINT=https://your-llm-provider.example/v1/responses
LLM_API_KEY=your_api_key_here
LLM_MODEL=your_model_name
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/minicursor
```

### 6. Database migrations

From the `backend/` directory:

```bash
cd backend
alembic upgrade head
cd ..
```

---

## How to run (recommended — full stack)

You need **two terminals** plus PostgreSQL running.

### Terminal 1 — Backend API

```powershell
cd backend
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs

### Terminal 2 — React UI

```powershell
cd frontend
npm run dev
```

UI: http://localhost:5173

The Vite dev server proxies `/api/*` to the backend, so the UI talks to FastAPI without CORS setup.

### Using the UI

1. Open http://localhost:5173
2. Sidebar should show **Connected**
3. Click **+ New chat** to create a session
4. Type a message and press **Send**
5. Click **×** on a session to remove it (soft-delete)

### End-to-end flow

```
Browser (5173)
  → POST /api/sessions/{id}/chat
  → Vite proxy → FastAPI (8000)
  → ChatService → Harness → LLM + tools
  → Save agent_state to PostgreSQL
  → GET /api/sessions/{id} (UI reloads conversation)
```

More detail:

* [docs/frontend-backend-connection.md](docs/frontend-backend-connection.md) — how the UI connects to the API
* [docs/request-lifecycle.md](docs/request-lifecycle.md) — full request path through DB and agent

---

## API quick reference

| Action | Method | Path |
|--------|--------|------|
| List active sessions | `GET` | `/sessions/` |
| Create session | `POST` | `/sessions/?title=...&workspace=...` |
| Get session + messages | `GET` | `/sessions/{id}` |
| Remove session | `DELETE` | `/sessions/{id}` |
| Send message | `POST` | `/sessions/{id}/chat` |

Chat request body:

```json
{ "message": "build a FastAPI todo application" }
```

Example (direct to backend, no proxy):

```powershell
curl -X POST "http://127.0.0.1:8000/sessions/{session_id}/chat" `
  -H "Content-Type: application/json" `
  -d "{\"message\": \"Hi\"}"
```

---

## Legacy: standalone agent (`agent.py`)

For quick local testing without the database or React UI:

### Simple web UI

```bash
python agent.py
```

Open http://127.0.0.1:8000/ — uses the built-in static page and `POST /chat` (no session persistence).

### CLI mode

```bash
python agent.py cli
```

Type tasks at the `You >>` prompt. Type `exit` to quit.

---

## Notes

- Generated files are typically written under the `workspace/` directory.
- Shell commands run with `workspace/` as the working directory for tool execution.
- Agent requests may take a long time — the LLM may run many tool steps.
- If the UI shows **Cannot reach backend**, ensure uvicorn is running on port 8000.
- If chat fails, check `.env` LLM settings and the uvicorn terminal for errors.
