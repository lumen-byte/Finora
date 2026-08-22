from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.api.deps import get_db
from backend.app.schemas.category import CategoryResponse
from backend.app.schemas.user import UserResponse
from backend.app.services.category_service import CategoryService
from backend.app.api.deps import get_current_user

router = APIRouter(tags=["categories"])

@router.get("", response_model=List[CategoryResponse])
def get_categories(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    return service.get_categories()
