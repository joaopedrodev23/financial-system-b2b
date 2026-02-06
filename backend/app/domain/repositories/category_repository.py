from datetime import datetime
from typing import Protocol
from uuid import UUID
from app.domain.entities.category import Category, CategoryType


class CategoryRepository(Protocol):
    def list_by_user(self, user_id: UUID) -> list[Category]:
        ...

    def get_by_id(self, category_id: UUID, user_id: UUID) -> Category | None:
        ...

    def create(self, user_id: UUID, name: str, type: CategoryType) -> Category:
        ...

    def update(self, category_id: UUID, user_id: UUID, name: str, type: CategoryType) -> Category | None:
        ...

    def delete(self, category_id: UUID, user_id: UUID) -> bool:
        ...
