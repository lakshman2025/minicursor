from tools import (
    ToolRegistry,
    MkdirTool,
    WriteFileTool,
    ReadFileTool,
    SearchCodeTool,
)

from harness import Harness


registry = ToolRegistry()

registry.register(MkdirTool())
registry.register(WriteFileTool())
registry.register(ReadFileTool())
registry.register(SearchCodeTool())

result = registry.execute(
    "search_code",
    query="FastAPI"
)


while True:

    user_input = input("\nYou >> ")

    if user_input.lower() == "exit":
        break


    try:
        agent = Harness(registry)
        agent.run(user_input)

    except Exception as e:
        print(f"\nAgent Error: {e}")

