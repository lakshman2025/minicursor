import json
import os

from state import AgentState


class ContextBuilder:

    def build(self, state: AgentState, user_request: str) -> str:

        conversation = "\n".join(
            msg["content"]
            for msg in state.messages[-20:]
        )

        tool_history = json.dumps(
            state.tool_history[-20:],
            indent=2
        )

        

        return f"""
Working Directory
{os.getcwd()}

Conversation
{conversation}

Current Request
{user_request}

Previous Tool Results
{tool_history if state.tool_history else "(none yet)"}

Remember:
- Do not repeat the same tool call unless new information is needed.
- Continue implementing until the requested application is complete.
- Finish only when no more work is required.
"""