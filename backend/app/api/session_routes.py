from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.agent_state_repository import AgentStateRepository
from app.repositories.session_repository import SessionRepository
from app.services.session_service import SessionService


router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
)


def _session_service(db: Session) -> SessionService:
    return SessionService(SessionRepository(db), AgentStateRepository(db))


def _serialize_session(session, include_messages: bool = False) -> dict:
    messages = []
    if include_messages and session.agent_state:
        messages = session.agent_state.messages or []

    return {
        "id": str(session.id),
        "title": session.title,
        "workspace": session.workspace,
        "updated_at": session.updated_at,
        "messages": messages,
    }


@router.post('/')
def create_session(title: str, workspace: str, db: Session = Depends(get_db)):
    session = _session_service(db).create_session(title, workspace)
    return _serialize_session(session, include_messages=True)

@router.get('/{session_id}')
def get_session(session_id: str, db: Session = Depends(get_db)):
    session = _session_service(db).get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return _serialize_session(session, include_messages=True)

@router.get('/')
def get_sessions(db: Session = Depends(get_db)):
    sessions = _session_service(db).get_sessions()
    return [_serialize_session(session) for session in sessions]

@router.delete('/{session_id}')
def deactivate_session(session_id: str, db: Session = Depends(get_db)):
    session = _session_service(db).deactivate_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return _serialize_session(session)