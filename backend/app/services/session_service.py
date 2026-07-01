from typing import List, Optional

from app.models.session import Session as SessionModel
from app.repositories.agent_state_repository import AgentStateRepository
from app.repositories.session_repository import SessionRepository


class SessionService:
    def __init__(
        self,
        session_repository: SessionRepository,
        agent_state_repository: AgentStateRepository,
    ):
        self.session_repository = session_repository
        self.agent_state_repository = agent_state_repository

    def create_session(self, title: str, workspace: str) -> SessionModel:
        session = self.session_repository.create(
            title=title,
            workspace=workspace,
        )
        self.agent_state_repository.create(session_id=session.id)
        return session

    def get_session(self, session_id: str) -> Optional[SessionModel]:
        return self.session_repository.get_by_id(session_id)

    def get_sessions(self) -> List[SessionModel]:
        return self.session_repository.get_all()

    def deactivate_session(self, session_id: str) -> Optional[SessionModel]:
        session = self.session_repository.get_by_id(session_id)
        if session:
            return self.session_repository.deactivate(session)
        return None
