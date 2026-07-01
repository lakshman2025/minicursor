import sys
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from harness import Harness  
from tools import (
    ListFilesTool,
    MkdirTool,
    ReadFileTool,
    SearchCodeTool,
    ShellTool,
    ToolRegistry,
    WriteFileTool,
)

_harness: Optional[Harness] = None


def get_harness() -> Harness:
    global _harness
    if _harness is None:
        registry = ToolRegistry()
        registry.register(MkdirTool())
        registry.register(WriteFileTool())
        registry.register(ReadFileTool())
        registry.register(ListFilesTool())
        registry.register(SearchCodeTool())
        registry.register(ShellTool())
        _harness = Harness(registry)
    return _harness
