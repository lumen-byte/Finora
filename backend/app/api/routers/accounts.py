from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.app.api.deps import get_db
from backend.app.schemas.account import AccountCreate, AccountUpdate, AccountResponse
from backend.app.schemas.user import UserResponse
from backend.app.services.account_service import AccountService
from backend.app.api.deps import get_current_user

router = APIRouter(tags=["accounts"])

@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_in: AccountCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    return service.create_account(current_user.id, account_in)

@router.get("", response_model=List[AccountResponse])
def get_accounts(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    return service.get_accounts(current_user.id)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    return service.get_account(account_id, current_user.id)

@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: UUID,
    account_in: AccountUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    return service.update_account(account_id, current_user.id, account_in)

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    service.delete_account(account_id, current_user.id)
