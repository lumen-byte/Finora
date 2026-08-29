from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from backend.app.models.copilot import Conversation, Message, Role
from datetime import datetime, UTC

class CopilotRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: UUID, title: Optional[str] = None) -> Conversation:
        conversation = Conversation(user_id=user_id, title=title)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
        return self.session.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()

    def get_user_conversations(self, user_id: UUID, skip: int = 0, limit: int = 20) -> List[Conversation]:
        return self.session.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()

    def delete_conversation(self, conversation_id: UUID, user_id: UUID) -> bool:
        conversation = self.get_conversation(conversation_id, user_id)
        if conversation:
            self.session.delete(conversation)
            self.session.commit()
            return True
        return False

    def add_message(self, conversation_id: UUID, role: Role, content: str) -> Message:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        self.session.add(message)
        
        conversation = self.session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.updated_at = datetime.now(UTC)
            
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_recent_messages(self, conversation_id: UUID, limit: int = 10) -> List[Message]:
        messages = self.session.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit).all()
        
        return list(reversed(messages))
