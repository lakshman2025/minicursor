from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.agent_state_repository import AgentStateRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/sessions", tags=["chat"])


def _chat_service(db: Session) -> ChatService:
    return ChatService(SessionRepository(db), AgentStateRepository(db))


@router.post("/{session_id}/chat", response_model=ChatResponse)
def chat(
    session_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    try:
        assistant_message = _chat_service(db).chat(session_id, request.message)
        return ChatResponse(
            role=assistant_message["role"],
            content=assistant_message["content"],
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
