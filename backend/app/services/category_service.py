from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.repositories.category_repository import CategoryRepository
from backend.app.models.category import Category

class CategoryService:
    def __init__(self, session: Session):
        self.repository = CategoryRepository(session)

    def get_category(self, category_id: UUID) -> Category:
        category = self.repository.get(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category

    def get_categories(self) -> List[Category]:
        return self.repository.get_all()
