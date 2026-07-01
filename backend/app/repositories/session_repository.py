from typing import List, Optional

from sqlalchemy.orm import Session as DBSession, joinedload

from app.models.session import Session as SessionModel

class SessionRepository:
    def __init__(self, db: DBSession):
        self.db = db
    def create(self, title: str, workspace: str, active: bool = True) -> SessionModel:
        session = SessionModel(title=title, workspace=workspace, active=active)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    def get_by_id(self, session_id: str) -> Optional[SessionModel]:
        return (
            self.db.query(SessionModel)
            .options(joinedload(SessionModel.agent_state))
            .filter(SessionModel.id == session_id, SessionModel.active == True)
            .first()
        )

    def get_all(self) -> List[SessionModel]:
        return self.db.query(SessionModel).filter(SessionModel.active == True).all()
    def update(self, session:SessionModel) -> SessionModel:
        self.db.commit()
        self.db.refresh(session)
        return session 
    def deactivate(self, session:SessionModel) -> None:
        session.active = False
        self.db.commit()
        self.db.refresh(session)
        return session


