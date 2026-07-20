from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage
from app.schemas.chat_schema import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatMessagesListResponse,
)
from app.database.database import get_db
from app.models.user import User
from app.models.chat_session import ChatSession
from app.schemas.chat_schema import ChatSessionDetail
from app.schemas.chat_schema import (ChatSessionCreate,ChatSessionResponse,)
from app.core.security import get_current_user
from app.services.chat_service import generate_ai_response


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/session",response_model=ChatSessionResponse,status_code=201)
def create_chat_session(session: ChatSessionCreate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):

    user = (db.query(User).filter(User.email == current_user.email).first())

    if user is None:
        raise HTTPException(status_code=404,detail="User not found")

    new_session = ChatSession(title=session.title,user_id=user.id)

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session

@router.get("/sessions",response_model=list[ChatSessionResponse])
def get_my_chat_sessions(current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):

    user = (db.query(User).filter(User.email == current_user.email).first())

    if user is None:
        raise HTTPException(status_code=404,detail="User not found")

    sessions = (db.query(ChatSession).filter(ChatSession.user_id == user.id).order_by(ChatSession.created_at.desc()).all())

    return sessions

@router.delete("/session/{session_id}")
def delete_chat_session(session_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):

    user = (db.query(User).filter(User.email == current_user.email).first())

    session = (db.query(ChatSession).filter(ChatSession.id == session_id,ChatSession.user_id == user.id).first())

    if session is None:
        raise HTTPException(status_code=404,detail="Session not found")

    db.delete(session)
    db.commit()

    return {
        "message": "Session deleted successfully"
    }

@router.get("/session/{session_id}",response_model=ChatSessionDetail)
def get_chat_session(session_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):

    user = (db.query(User).filter(User.email == current_user.email).first())

    session = (db.query(ChatSession).filter(ChatSession.id == session_id,ChatSession.user_id == user.id).first())

    if session is None:
        raise HTTPException(status_code=404,detail="Session not found")

    return {
        "session_id": session.id,
        "title": session.title,
        "messages": session.messages
    }

@router.post("/{session_id}/message",response_model=ChatMessageResponse,)
def send_message(session_id: int,chat: ChatMessageCreate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):

    session = (db.query(ChatSession).filter(ChatSession.id == session_id,ChatSession.user_id == current_user.id).first())

    if session is None:
        raise HTTPException(status_code=404,detail="Chat session not found",)

    user_message = ChatMessage(session_id=session.id,sender="user",message=chat.message,)

    db.add(user_message)
    db.commit()

    ai_reply = generate_ai_response(chat.message)

    assistant_message = ChatMessage(session_id=session.id,sender="assistant",message=ai_reply,)

    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return assistant_message

@router.get("/{session_id}/messages",response_model=ChatMessagesListResponse)
def get_messages(session_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),):

    user = (db.query(User).filter(User.email == current_user.email).first())

    session = (db.query(ChatSession).filter(ChatSession.id == session_id,ChatSession.user_id == user.id).first())

    if session is None:
        raise HTTPException(status_code=404,detail="Session not found")

    messages = (db.query(ChatMessage).filter(ChatMessage.session_id == session.id).order_by(ChatMessage.created_at.asc()).all())

    return {
        "messages": messages
    }