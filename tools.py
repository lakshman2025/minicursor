import os

IGNORED_DIRS = {"__pycache__", ".git", ".venv", "venv"}


class BaseTool:
    name = ""
    description = ""
    parameters = ""

    def execute(self, **kwargs):
        raise NotImplementedError

    def metadata(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def execute(self, tool_name, **kwargs):
        if tool_name not in self.tools:
            raise Exception(f"Tool {tool_name} not found")
        return self.tools[tool_name].execute(**kwargs)

    def describe_tools(self):
        return [tool.metadata() for tool in self.tools.values()]


class MkdirTool(BaseTool):
    name = "mkdir"
    description = "Create a directory."
    parameters = "path"

    def execute(self, path):
        os.makedirs(path, exist_ok=True)
        return f"Directory created: {path}"


class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Write content to a text file."
    parameters = "path, content"

    def execute(self, path: str, content: str):
        directory = os.path.dirname(path)

        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {
            "status": "success",
            "path": path,
            "message": f"File written successfully: {path}",
        }


class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Read the content of a text file."
    parameters = "path"

    def execute(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return {
                "status": "success",
                "path": path,
                "content": content,
                "message": f"File read successfully: {path}",
            }
        except Exception as e:
            return {
                "status": "error",
                "path": path,
                "message": f"Failed to read file: {e}",
            }


class ListFilesTool(BaseTool):
    name = "list_files"
    description = "List files and directories at a path. Use to explore the project structure."
    parameters = "path='.'"

    def execute(self, path=".", **kwargs):
        if not os.path.isdir(path):
            return {
                "status": "error",
                "path": path,
                "message": f"Path not found: {path}",
                "entries": [],
            }

        entries = []
        for name in sorted(os.listdir(path)):
            full_path = os.path.join(path, name)
            entries.append({
                "name": name,
                "type": "dir" if os.path.isdir(full_path) else "file",
            })

        return {
            "status": "success",
            "path": path,
            "entries": entries,
        }


class SearchCodeTool(BaseTool):
    name = "search_code"
    description = "Search an existing codebase for text. Use only when you need information from files that already exist."
    parameters = "query, root='workspace'"

    def execute(self, query="", root="workspace", **kwargs):
        query = query or kwargs.get("keyword", "")
        if not query:
            return {"status": "success", "query": "", "matches": []}

        if not os.path.isdir(root):
            return {
                "status": "error",
                "message": f"Search root not found: {root}",
                "query": query,
                "matches": [],
            }

        matches = []
        query_lower = query.lower()

        for current_dir, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for filename in files:
                full_path = os.path.join(current_dir, filename)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception:
                    continue

                if query_lower in content.lower():
                    matches.append({
                        "path": full_path,
                        "file": filename,
                    })

        return {
            "status": "success",
            "query": query,
            "matches": matches,
        }
import subprocess

class ShellTool(BaseTool):
    name = "shell"
    description = "Execute a shell command in the workspace."
    parameters = "command"

    def execute(self, command: str):
        try:
            result = subprocess.run(
                command,
                cwd="workspace",
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )

            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }