from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional
from backend.app.models.category import TransactionType

class CategoryBase(BaseModel):
    name: str
    type: TransactionType
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
