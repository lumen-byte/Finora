from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class InsightResponse(BaseModel):
    id: str
    title: str
    message: str
    severity: str # INFO, WARNING, IMPORTANT
    related_category: Optional[str] = None
    related_transaction_id: Optional[UUID] = None
