import json

from llm import LLM


class AgentLLM:

    def __init__(self, registry):
        self.llm = LLM()
        self.registry = registry

    def _format_tools(self) -> str:
        lines = []

        for tool in self.registry.describe_tools():

            signature = (
                f"{tool['name']}({tool['parameters']})"
            )

            lines.append(signature)
            lines.append(f"  {tool['description']}")

        return "\n".join(lines)

    def _parse_action(self, raw: dict) -> dict:
        if raw.get("finish"):
            return {
                "finish": True,
                "message": raw.get("message", "Task completed."),
            }

        if "tool" in raw:
            return {"tool": raw["tool"], "args": raw.get("args", {})}

        # Legacy / malformed shapes from older prompts
        if raw.get("type") == "finish":
            return {
                "finish": True,
                "message": raw.get("message", "Task completed."),
            }
        if raw.get("type") == "tool" and "tool" in raw:
            return {"tool": raw["tool"], "args": raw.get("args", {})}
        if raw.get("type") in self.registry.tools:
            return {"tool": raw["type"], "args": raw.get("args", {})}

        raise ValueError(f"Unrecognized action: {raw}")

    
   def step(self, context: str) -> dict:

        prompt = f"""
    You are an autonomous AI Software Engineering Agent.

    Your responsibility is to complete the user's request from start to finish.

    You are responsible for:
    - understanding the request
    - planning the next step
    - choosing the correct tool
    - observing tool results
    - recovering from failures
    - continuing until the application is complete and runnable

    Return ONLY the NEXT action.

    ==================================================
    AVAILABLE TOOLS

    {self._format_tools()}

    Use ONLY these tools.
    Never invent tool names.

    ==================================================
    GENERAL WORKFLOW

    For every iteration:

    1. Read the current context.
    2. Review previous tool results.
    3. Decide the next best action.
    4. Return exactly ONE tool call.
    5. Wait for the result.
    6. Continue until finished.

    ==================================================
    RULES

    Filesystem
    ----------
    - Use list_files to inspect directories.
    - Use mkdir before creating new folders.
    - Use write_file to create or modify files.
    - Use read_file only when you genuinely need file contents.
    - Use search_code only to search existing source code.

    Avoid loops
    -----------
    - Never repeat the same tool call with identical arguments.
    - Never repeatedly read the same file.
    - Never repeatedly list the same directory.
    - If enough information exists, continue implementing.

    ==================================================
    SHELL TOOL

    Use the shell tool for:

    - creating virtual environments
    - installing dependencies
    - running tests
    - starting applications
    - verifying the application works

    Never use shell to edit source code.

    ==================================================
    APPLICATION GENERATION

    When building a new application:

    1. Create the project directory.
    2. Create all required folders.
    3. Create every required source file.
    4. Create configuration files.
    5. Create requirements.txt.
    6. Create tests when appropriate.

    Then:

    7. If a virtual environment already exists, reuse it.
    Otherwise create one.

    8. Install dependencies.

    9. Run tests if tests exist.

    10. Start the application.

    If any command fails:

    - inspect the error
    - fix the problem
    - retry

    Continue until the project is runnable.

    ==================================================
    SERVER VERIFICATION

    When verifying a web application:

    - Start the server WITHOUT --reload.
    - Prefer a temporary port such as 8765.
    - Wait until the server is accepting requests.
    - Verify the application using the root endpoint or /health endpoint.
    - If verification succeeds, STOP the server immediately.
    - Never leave background processes running.
    - Return finish only after the server has been stopped.

    ==================================================
    TASK COMPLETION

    A task is complete ONLY if:

    ✓ All required files exist.
    ✓ The requested functionality is implemented.
    ✓ Dependencies are installed.
    ✓ Tests pass (if present).
    ✓ The application starts successfully.
    ✓ The verification server has been stopped.
    ✓ No background processes remain.
    ✓ No additional work is required.

    Do NOT finish immediately after writing files.

    ==================================================
    CURRENT CONTEXT

    {context}

    ==================================================
    Return ONLY ONE JSON object.

    Tool Example

    {{
        "tool": "write_file",
        "args": {{
            "path": "workspace/app/main.py",
            "content": "..."
        }}
    }}

    Shell Example

    {{
        "tool": "shell",
        "args": {{
            "command": "python -m pip install -r requirements.txt"
        }}
    }}

    Finish Example

    {{
        "finish": true,
        "message": "Task completed."
    }}

    Return raw JSON only.
    """

        response = self.llm.generate(prompt)

        return self._parse_action(json.loads(response))


    def summarize(self, state):

        prompt = f"""
    You are an AI coding assistant.

    Write a concise completion message for the user.

    User Request:
    {state.messages[-1]["content"]}

    Tool History:
    {json.dumps(state.tool_history, indent=2)}

    Include:
    - What was built.
    - Important files created or modified.
    - Dependencies installed.
    - Tests executed and results.
    - Whether the application starts successfully.
    - Exact command to run the application.
    - URL if the application starts a web server.
    - Mention any remaining issues if they exist.

    Keep it under 200 words.
    Do not mention internal reasoning.
    """

        return self.llm.generate(prompt).strip()