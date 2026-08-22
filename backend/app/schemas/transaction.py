from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from backend.app.models.category import TransactionType

class TransactionBase(BaseModel):
    account_id: UUID
    category_id: Optional[UUID] = None
    type: TransactionType
    amount: Decimal
    description: str
    merchant: Optional[str] = None
    transaction_date: date
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    account_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    type: Optional[TransactionType] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    merchant: Optional[str] = None
    transaction_date: Optional[date] = None
    notes: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
