from typing import List, Optional
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from backend.app.models.transaction import Transaction
from backend.app.models.category import TransactionType
from backend.app.schemas.transaction import TransactionCreate, TransactionUpdate

class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, transaction_id: UUID, user_id: UUID) -> Optional[Transaction]:
        return self.session.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()

    def get_all(
        self,
        user_id: UUID,
        account_id: Optional[UUID] = None,
        category_id: Optional[UUID] = None,
        type: Optional[TransactionType] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Transaction]:
        query = self.session.query(Transaction).filter(Transaction.user_id == user_id)
        
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
        if type:
            query = query.filter(Transaction.type == type)
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        if search:
            query = query.filter(
                (Transaction.merchant.ilike(f"%{search}%")) |
                (Transaction.description.ilike(f"%{search}%"))
            )
            
        return query.order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit).all()

    def create(self, user_id: UUID, obj_in: TransactionCreate) -> Transaction:
        db_obj = Transaction(
            user_id=user_id,
            **obj_in.model_dump()
        )
        self.session.add(db_obj)
        self.session.flush() # Flush to get ID, don't commit yet (handled by service)
        return db_obj

    def update(self, db_obj: Transaction, obj_in: TransactionUpdate) -> Transaction:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        self.session.flush() # Handled by service
        return db_obj

    def delete(self, db_obj: Transaction) -> None:
        self.session.delete(db_obj)
        self.session.flush() # Handled by service
