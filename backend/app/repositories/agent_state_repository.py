import uuid
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from app.models.agent_state import AgentState as AgentStateModel


class AgentStateRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, session_id: uuid.UUID) -> AgentStateModel:
        state = AgentStateModel(session_id=session_id)
        self.db.add(state)
        self.db.commit()
        self.db.refresh(state)
        return state

    def get_by_session_id(self, session_id: uuid.UUID) -> Optional[AgentStateModel]:
        return (
            self.db.query(AgentStateModel)
            .filter(AgentStateModel.session_id == session_id)
            .first()
        )

    def update(self, state: AgentStateModel) -> AgentStateModel:
        flag_modified(state, "messages")
        flag_modified(state, "tool_history")
        flag_modified(state, "last_tool_result")
        self.db.commit()
        self.db.refresh(state)
        return state
