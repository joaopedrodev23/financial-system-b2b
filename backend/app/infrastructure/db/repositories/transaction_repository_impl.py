from datetime import date
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.domain.entities.transaction import TransactionType
from app.domain.repositories.transaction_repository import TransactionRepository
from app.infrastructure.db.models.transaction_model import TransactionModel
from app.infrastructure.db.repositories.mappers import transaction_model_to_entity


class TransactionRepositoryImpl(TransactionRepository):
    def __init__(self, db: Session):
        self.db = db

    def list_by_user(self, user_id, start_date=None, end_date=None, type=None, category_id=None):
        stmt = select(TransactionModel).where(TransactionModel.user_id == user_id)
        if start_date:
            stmt = stmt.where(TransactionModel.date >= start_date)
        if end_date:
            stmt = stmt.where(TransactionModel.date <= end_date)
        if type:
            stmt = stmt.where(TransactionModel.type == type)
        if category_id:
            stmt = stmt.where(TransactionModel.category_id == category_id)
        stmt = stmt.order_by(TransactionModel.date.desc(), TransactionModel.created_at.desc())
        models = self.db.execute(stmt).scalars().all()
        return [transaction_model_to_entity(model) for model in models]

    def get_by_id(self, transaction_id, user_id):
        stmt = select(TransactionModel).where(
            TransactionModel.id == transaction_id,
            TransactionModel.user_id == user_id,
        )
        model = self.db.execute(stmt).scalars().first()
        return transaction_model_to_entity(model) if model else None

    def create(self, user_id, category_id, type: TransactionType, amount: Decimal, description, date: date):
        model = TransactionModel(
            user_id=user_id,
            category_id=category_id,
            type=type,
            amount=amount,
            description=description,
            date=date,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return transaction_model_to_entity(model)

    def update(self, transaction_id, user_id, category_id, type: TransactionType, amount: Decimal, description, date: date):
        stmt = select(TransactionModel).where(
            TransactionModel.id == transaction_id,
            TransactionModel.user_id == user_id,
        )
        model = self.db.execute(stmt).scalars().first()
        if not model:
            return None
        model.category_id = category_id
        model.type = type
        model.amount = amount
        model.description = description
        model.date = date
        self.db.commit()
        self.db.refresh(model)
        return transaction_model_to_entity(model)

    def delete(self, transaction_id, user_id) -> bool:
        stmt = select(TransactionModel).where(
            TransactionModel.id == transaction_id,
            TransactionModel.user_id == user_id,
        )
        model = self.db.execute(stmt).scalars().first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def summary(self, user_id, start_date=None, end_date=None) -> dict:
        def _sum_by_type(tx_type: TransactionType):
            stmt = select(func.coalesce(func.sum(TransactionModel.amount), 0)).where(
                TransactionModel.user_id == user_id,
                TransactionModel.type == tx_type,
            )
            if start_date:
                stmt = stmt.where(TransactionModel.date >= start_date)
            if end_date:
                stmt = stmt.where(TransactionModel.date <= end_date)
            return self.db.execute(stmt).scalar_one()

        total_income = _sum_by_type(TransactionType.INCOME)
        total_expense = _sum_by_type(TransactionType.EXPENSE)
        balance = Decimal(total_income) - Decimal(total_expense)

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "start_date": start_date,
            "end_date": end_date,
        }
