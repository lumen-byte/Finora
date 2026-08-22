import enum
import uuid
from sqlalchemy import Column, String, Enum, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.db.base import Base

class AccountType(str, enum.Enum):
    BANK = "BANK"
    CASH = "CASH"
    CREDIT_CARD = "CREDIT_CARD"
    WALLET = "WALLET"
    INVESTMENT = "INVESTMENT"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    current_balance = Column(Numeric(12, 2), default=0.00, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="accounts")
