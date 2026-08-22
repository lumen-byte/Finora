from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.api.deps import get_current_user, get_db
from backend.app.schemas.user import UserResponse
from backend.app.schemas.insight import InsightResponse
from backend.app.services.insight_service import InsightService

router = APIRouter(tags=["insights"])

@router.get("", response_model=List[InsightResponse])
def get_insights(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = InsightService(db)
    return service.generate_insights(current_user.id)
