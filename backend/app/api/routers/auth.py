from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Any

from backend.app.schemas.user import UserCreate, UserResponse
from backend.app.schemas.auth import Token
from backend.app.api.deps import SessionDep, CurrentUser
from backend.app.services.auth_service import AuthService
from backend.app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, session: SessionDep) -> Any:
    """
    Register a new user.
    """
    auth_service = AuthService(session)
    user = auth_service.register_user(user_in)
    return user

@router.post("/login", response_model=Token)
def login(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    auth_service = AuthService(session)
    user = auth_service.authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user

@router.post("/demo", response_model=Token)
def demo_login(session: SessionDep) -> Any:
    """
    Login as the demo user automatically without password.
    """
    auth_service = AuthService(session)
    user = auth_service.repository.get_by_email("demo@finora.ai")
    if not user:
        raise HTTPException(status_code=404, detail="Demo user not found in database. Seed the database first.")
    
    access_token = create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
