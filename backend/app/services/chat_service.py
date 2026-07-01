from typing import Any, Dict

from app.agent.harness_factory import get_harness
from app.repositories.agent_state_repository import AgentStateRepository
from app.repositories.session_repository import SessionRepository


class ChatService:
    def __init__(
        self,
        session_repository: SessionRepository,
        agent_state_repository: AgentStateRepository,
    ):
        self.session_repository = session_repository
        self.agent_state_repository = agent_state_repository
        self.harness = get_harness()

    def chat(self, session_id: str, message: str) -> Dict[str, Any]:
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")

        state = self.agent_state_repository.get_by_session_id(session.id)
        if not state:
            raise ValueError("Agent state not found")

        assistant_message = self.harness.run(
            state=state,
            user_message={"role": "user", "content": message},
        )
        self.agent_state_repository.update(state)
        return assistant_message
