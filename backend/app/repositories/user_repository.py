from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from backend.app.core.security import get_password_hash
from typing import Optional

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    def create(self, user_in: UserCreate) -> User:
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_active=user_in.is_active
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user
