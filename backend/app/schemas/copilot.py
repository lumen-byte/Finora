from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class CopilotChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

class CopilotChatResponse(BaseModel):
    conversation_id: UUID
    answer: str
    tools_used: List[str]

class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: Optional[List[MessageResponse]] = None

    class Config:
        from_attributes = True
