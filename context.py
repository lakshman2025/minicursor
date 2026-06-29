from state import AgentState


class ContextBuilder:

    def build(self, state: AgentState, user_request: str) -> str:
        conversation = "\n".join(
            msg["content"] for msg in state.messages[-4:]
        )

        context = f"""Conversation
{conversation}
Current Request
{user_request}
"""

        return context
