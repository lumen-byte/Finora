from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal
from backend.app.models.account import AccountType

class AccountBase(BaseModel):
    name: str
    account_type: AccountType
    currency: str = "USD"

class AccountCreate(AccountBase):
    current_balance: Optional[Decimal] = Decimal('0.00')

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    account_type: Optional[AccountType] = None
    current_balance: Optional[Decimal] = None
    currency: Optional[str] = None

class AccountResponse(AccountBase):
    id: UUID
    user_id: UUID
    current_balance: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
