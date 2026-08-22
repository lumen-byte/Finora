from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from backend.app.models.account import Account
from backend.app.schemas.account import AccountCreate, AccountUpdate

class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, account_id: UUID, user_id: UUID) -> Optional[Account]:
        return self.session.query(Account).filter(Account.id == account_id, Account.user_id == user_id).first()

    def get_all(self, user_id: UUID) -> List[Account]:
        return self.session.query(Account).filter(Account.user_id == user_id).all()

    def create(self, user_id: UUID, obj_in: AccountCreate) -> Account:
        db_obj = Account(
            user_id=user_id,
            name=obj_in.name,
            account_type=obj_in.account_type,
            currency=obj_in.currency,
            current_balance=obj_in.current_balance
        )
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Account, obj_in: AccountUpdate) -> Account:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: Account) -> None:
        self.session.delete(db_obj)
        self.session.commit()
