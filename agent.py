import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from tools import (
    ToolRegistry,
    MkdirTool,
    WriteFileTool,
    ReadFileTool,
    ListFilesTool,
    SearchCodeTool,
    ShellTool,
)
from harness import Harness


registry = ToolRegistry()

registry.register(MkdirTool())
registry.register(WriteFileTool())
registry.register(ReadFileTool())
registry.register(ListFilesTool())
registry.register(SearchCodeTool())
registry.register(ShellTool())

agent = Harness(registry)

app = FastAPI(title="Minicursor Agent")
STATIC_DIR = Path(__file__).parent / "static"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=5)


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        assistant_message = agent.run(request.message)
        return ChatResponse(reply=assistant_message["content"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_cli():
    while True:
        user_input = input("\nYou >> ")

        if user_input.lower() == "exit":
            break

        try:
            assistant_message = agent.run(user_input)
            print(f"\nAssistant >> {assistant_message['content']}")
        except Exception as e:
            print(f"\nAgent Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        run_cli()
    else:
        uvicorn.run("agent:app", host="127.0.0.1", port=8000, reload=True)
