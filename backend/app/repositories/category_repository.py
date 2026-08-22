from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from backend.app.models.category import Category

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, category_id: UUID) -> Optional[Category]:
        return self.session.query(Category).filter(Category.id == category_id).first()

    def get_all(self) -> List[Category]:
        return self.session.query(Category).all()
