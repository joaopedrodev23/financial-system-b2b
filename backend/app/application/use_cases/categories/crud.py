from uuid import UUID
from app.domain.entities.category import CategoryType
from app.domain.repositories.category_repository import CategoryRepository


def list_categories(category_repo: CategoryRepository, user_id: UUID):
    return category_repo.list_by_user(user_id)


def create_category(category_repo: CategoryRepository, user_id: UUID, name: str, type: CategoryType):
    return category_repo.create(user_id=user_id, name=name, type=type)


def update_category(
    category_repo: CategoryRepository,
    user_id: UUID,
    category_id: UUID,
    name: str,
    type: CategoryType,
):
    return category_repo.update(category_id=category_id, user_id=user_id, name=name, type=type)


def delete_category(category_repo: CategoryRepository, user_id: UUID, category_id: UUID) -> bool:
    return category_repo.delete(category_id=category_id, user_id=user_id)
