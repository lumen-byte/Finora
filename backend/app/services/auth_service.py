from sqlalchemy.orm import Session
from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas.user import UserCreate
from backend.app.core.security import verify_password
from backend.app.models.user import User
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    def register_user(self, user_in: UserCreate) -> User:
        user = self.repository.get_by_email(user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )
        return self.repository.create(user_in)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email)
        if not user:
            return None
        if not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def authenticate_google_user(self, email: str, google_id: str) -> User:
        user = self.repository.get_by_email(email)
        if not user:
            return self.repository.create_google_user(email=email, google_id=google_id)
        if not user.google_id:
            return self.repository.update_google_id(user=user, google_id=google_id)
        if user.google_id != google_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google ID mismatch for this email."
            )
        return user
