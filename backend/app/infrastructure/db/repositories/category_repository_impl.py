from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.entities.category import CategoryType
from app.domain.repositories.category_repository import CategoryRepository
from app.infrastructure.db.models.category_model import CategoryModel
from app.infrastructure.db.repositories.mappers import category_model_to_entity


class CategoryRepositoryImpl(CategoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def list_by_user(self, user_id):
        stmt = select(CategoryModel).where(CategoryModel.user_id == user_id).order_by(CategoryModel.name.asc())
        models = self.db.execute(stmt).scalars().all()
        return [category_model_to_entity(model) for model in models]

    def get_by_id(self, category_id, user_id):
        stmt = select(CategoryModel).where(
            CategoryModel.id == category_id,
            CategoryModel.user_id == user_id,
        )
        model = self.db.execute(stmt).scalars().first()
        return category_model_to_entity(model) if model else None

    def create(self, user_id, name: str, type: CategoryType):
        model = CategoryModel(user_id=user_id, name=name, type=type)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return category_model_to_entity(model)

    def update(self, category_id, user_id, name: str, type: CategoryType):
        stmt = select(CategoryModel).where(
            CategoryModel.id == category_id,
            CategoryModel.user_id == user_id,
        )
        model = self.db.execute(stmt).scalars().first()
        if not model:
            return None
        model.name = name
        model.type = type
        self.db.commit()
        self.db.refresh(model)
        return category_model_to_entity(model)

    def delete(self, category_id, user_id) -> bool:
        stmt = select(CategoryModel).where(
            CategoryModel.id == category_id,
            CategoryModel.user_id == user_id,
        )
        model = self.db.execute(stmt).scalars().first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True
