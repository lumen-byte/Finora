import enum
import uuid
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from backend.app.db.base import Base

class TransactionType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(Enum(TransactionType), nullable=False)
    icon = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
