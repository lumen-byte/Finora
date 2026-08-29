from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.api.deps import get_current_user, get_db
from backend.app.schemas.user import UserResponse
from backend.app.schemas.copilot import (
    CopilotChatRequest,
    CopilotChatResponse,
    ConversationResponse,
    MessageResponse
)
from backend.app.services.copilot_service import CopilotService
from backend.app.repositories.copilot_repository import CopilotRepository

router = APIRouter(tags=["copilot"])

@router.post("/chat", response_model=CopilotChatResponse)
def copilot_chat(
    request: CopilotChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        service = CopilotService(db)
        result = service.chat(current_user.id, request.message, request.conversation_id)
        return CopilotChatResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    skip: int = 0,
    limit: int = 20,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = CopilotRepository(db)
    return repo.get_user_conversations(current_user.id, skip, limit)

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = CopilotRepository(db)
    conversation = repo.get_conversation(conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conversation

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = CopilotRepository(db)
    success = repo.delete_conversation(conversation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
