from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import select

from app.core.config import get_settings
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.security.password import get_password_hash
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.models.category_model import CategoryModel
from app.infrastructure.db.models.transaction_model import TransactionModel
from app.domain.entities.category import CategoryType
from app.domain.entities.transaction import TransactionType

settings = get_settings()
DEMO_EMAIL = settings.demo_email
DEMO_PASSWORD = settings.demo_password


def get_or_create_user(db, email: str, password: str) -> UserModel:
    user = db.execute(select(UserModel).where(UserModel.email == email)).scalars().first()
    if user:
        return user
    user = UserModel(email=email, hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_category(db, user_id, name: str, type: CategoryType) -> CategoryModel:
    category = (
        db.execute(
            select(CategoryModel).where(
                CategoryModel.user_id == user_id,
                CategoryModel.name == name,
            )
        )
        .scalars()
        .first()
    )
    if category:
        return category
    category = CategoryModel(user_id=user_id, name=name, type=type)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def seed_transactions(db, user_id, categories: dict[str, CategoryModel]) -> None:
    existing = db.execute(select(TransactionModel).where(TransactionModel.user_id == user_id)).scalars().first()
    if existing:
        print("Transações já existem. Seed ignorado para este usuário.")
        return

    today = date.today()
    data = [
        (today - timedelta(days=1), TransactionType.INCOME, Decimal("1200.00"), "Venda no cartão", categories["Vendas"]),
        (today - timedelta(days=2), TransactionType.EXPENSE, Decimal("320.50"), "Conta de luz", categories["Operação"]),
        (today - timedelta(days=3), TransactionType.EXPENSE, Decimal("150.00"), "Internet e telefone", categories["Operação"]),
        (today - timedelta(days=4), TransactionType.INCOME, Decimal("850.00"), "Serviço prestado", categories["Serviços"]),
        (today - timedelta(days=5), TransactionType.EXPENSE, Decimal("210.30"), "Materiais", categories["Fornecedores"]),
        (today - timedelta(days=6), TransactionType.EXPENSE, Decimal("99.90"), "Ferramentas", categories["Fornecedores"]),
        (today - timedelta(days=7), TransactionType.INCOME, Decimal("400.00"), "Pagamento PIX", categories["Vendas"]),
        (today - timedelta(days=8), TransactionType.EXPENSE, Decimal("180.00"), "Impostos", categories["Impostos"]),
        (today - timedelta(days=10), TransactionType.INCOME, Decimal("2300.00"), "Contrato mensal", categories["Serviços"]),
        (today - timedelta(days=12), TransactionType.EXPENSE, Decimal("560.00"), "Aluguel", categories["Operação"]),
    ]

    for item in data:
        db.add(
            TransactionModel(
                user_id=user_id,
                category_id=item[4].id,
                type=item[1],
                amount=item[2],
                description=item[3],
                date=item[0],
            )
        )
    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        demo_user = get_or_create_user(db, DEMO_EMAIL, DEMO_PASSWORD)

        categories = {
            "Vendas": get_or_create_category(db, demo_user.id, "Vendas", CategoryType.INCOME),
            "Serviços": get_or_create_category(db, demo_user.id, "Serviços", CategoryType.INCOME),
            "Operação": get_or_create_category(db, demo_user.id, "Operação", CategoryType.EXPENSE),
            "Fornecedores": get_or_create_category(db, demo_user.id, "Fornecedores", CategoryType.EXPENSE),
            "Impostos": get_or_create_category(db, demo_user.id, "Impostos", CategoryType.EXPENSE),
        }

        seed_transactions(db, demo_user.id, categories)
        print("Seed concluído com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
