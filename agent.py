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

while True:

    user_input = input("\nYou >> ")

    if user_input.lower() == "exit":
        break


    try:
        
        agent.run(user_input)

    except Exception as e:
        print(f"\nAgent Error: {e}")


