# Minicursor

A small interactive coding agent that uses an LLM to plan and run tools (read/write files, search code, run shell commands). It can be used from the terminal, a web UI, or a FastAPI `POST /chat` endpoint.

## Objectives

The project was developed to understand:

* Agent-based software architecture
* LLM reasoning and decision making
* Tool calling using an autonomous agent
* Context management across multiple iterations
* Execution loop between the agent and the runtime
* Autonomous software generation

## System Architecture

The system consists of the following components:

* **Harness** – Controls the execution loop, executes tools, and maintains the agent state.
* **Agent LLM** – Acts as the decision-making component. It analyzes the current context and decides the next action.
* **Context Builder** – Prepares the prompt by combining the user's request with previous tool results.
* **Tool Registry** – Stores and executes the available tools.
* **Agent State** – Maintains conversation history and tool execution history throughout the task.

## Workflow

1. The user submits a request.
2. The Harness builds the execution context.
3. The context is sent to the Agent LLM.
4. The Agent LLM decides the next tool to execute.
5. The Harness executes the selected tool.
6. The tool result is stored in the agent state.
7. The updated context is sent back to the Agent LLM.
8. Steps 3–7 continue until the agent determines that the task is complete.
9. Finally, the agent generates a summary of the completed work for the user.

## Implemented Tools

The current implementation includes the following tools:

* List files
* Create directories
* Read files
* Write files
* Search code
* Execute shell commands

The shell tool allows the agent to:

* Create Python virtual environments
* Install project dependencies
* Execute test cases
* Start applications for verification

## Features

* Autonomous decision-making using an LLM
* Multi-step reasoning through an iterative execution loop
* Dynamic tool selection
* Context-aware execution
* Automatic project generation
* Dependency installation
* Test execution
* Application verification
* Final task summarization
* FastAPI backend with `POST /chat`
* Simple web UI for submitting tasks from the browser

## Prerequisites

- Python 3.10 or newer
- An LLM API endpoint and API key

## Setup

1. **Clone or open this project**, then go to the project root:

```bash
cd minicursor
```

2. **Create and activate a virtual environment** (recommended):

```bash
python -m venv env
```

On Windows (PowerShell):

```powershell
.\env\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source env/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the project root with your LLM settings:

```env
LLM_ENDPOINT=https://your-llm-provider.example/v1/responses
LLM_API_KEY=your_api_key_here
LLM_MODEL=your_model_name
```

Replace the values with your provider's endpoint, API key, and model name.

## Run the agent

### Web UI (default)

From the project root (with your virtual environment activated):

```bash
python agent.py
```

Then open in your browser:

```text
http://127.0.0.1:8000/
```

Type a task in plain English, for example:

```text
build a FastAPI todo application
```

Click **Send**. The agent will run tools in the background and display a summary when the task is done.

### API server

You can also start the server with uvicorn:

```bash
uvicorn agent:app --reload --host 127.0.0.1 --port 8000
```

Send a chat request:

```bash
curl -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"build a FastAPI todo application\"}"
```

On macOS/Linux, use `\` instead of `^`.

Example response:

```json
{
  "reply": "Summary of the completed work..."
}
```

Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### CLI mode

For terminal-only usage:

```bash
python agent.py cli
```

You should see a prompt:

```text
You >>
```

Type a task in plain English. The agent will call tools, print each action, and finish with a summary when the task is done.

To stop the agent, type:

```text
exit
```

## Notes

- Generated files are typically written under the `workspace/` directory.
- Shell commands run with the current working directory as the project root.
- Agent requests may take a long time to complete because the LLM runs multiple tool steps.
- If you see connection or auth errors, check that `.env` is configured correctly and that your API key is valid.
