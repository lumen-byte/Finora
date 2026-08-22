from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.repositories.account_repository import AccountRepository
from backend.app.schemas.account import AccountCreate, AccountUpdate
from backend.app.models.account import Account

class AccountService:
    def __init__(self, session: Session):
        self.repository = AccountRepository(session)

    def get_account(self, account_id: UUID, user_id: UUID) -> Account:
        account = self.repository.get(account_id, user_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        return account

    def get_accounts(self, user_id: UUID) -> List[Account]:
        return self.repository.get_all(user_id)

    def create_account(self, user_id: UUID, account_in: AccountCreate) -> Account:
        return self.repository.create(user_id, account_in)

    def update_account(self, account_id: UUID, user_id: UUID, account_in: AccountUpdate) -> Account:
        account = self.get_account(account_id, user_id)
        return self.repository.update(account, account_in)

    def delete_account(self, account_id: UUID, user_id: UUID) -> None:
        account = self.get_account(account_id, user_id)
        self.repository.delete(account)
