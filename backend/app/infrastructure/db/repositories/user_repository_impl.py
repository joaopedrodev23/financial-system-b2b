from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.repositories.mappers import user_model_to_entity


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        stmt = select(UserModel).where(UserModel.email == email)
        model = self.db.execute(stmt).scalars().first()
        return user_model_to_entity(model) if model else None

    def get_by_id(self, user_id):
        stmt = select(UserModel).where(UserModel.id == user_id)
        model = self.db.execute(stmt).scalars().first()
        return user_model_to_entity(model) if model else None

    def create(self, email: str, hashed_password: str):
        model = UserModel(email=email, hashed_password=hashed_password)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return user_model_to_entity(model)
