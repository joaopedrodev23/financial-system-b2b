from app.domain.entities.user import User
from app.domain.entities.category import Category
from app.domain.entities.transaction import Transaction
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.models.category_model import CategoryModel
from app.infrastructure.db.models.transaction_model import TransactionModel


def user_model_to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        hashed_password=model.hashed_password,
        is_active=model.is_active,
        created_at=model.created_at,
    )


def category_model_to_entity(model: CategoryModel) -> Category:
    return Category(
        id=model.id,
        user_id=model.user_id,
        name=model.name,
        type=model.type,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def transaction_model_to_entity(model: TransactionModel) -> Transaction:
    return Transaction(
        id=model.id,
        user_id=model.user_id,
        category_id=model.category_id,
        type=model.type,
        amount=model.amount,
        description=model.description,
        date=model.date,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
