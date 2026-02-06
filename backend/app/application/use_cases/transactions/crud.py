from datetime import date
from decimal import Decimal
from uuid import UUID
from app.domain.entities.transaction import TransactionType
from app.domain.repositories.transaction_repository import TransactionRepository


def list_transactions(
    transaction_repo: TransactionRepository,
    user_id: UUID,
    start_date: date | None,
    end_date: date | None,
    type: TransactionType | None,
    category_id: UUID | None,
):
    return transaction_repo.list_by_user(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        type=type,
        category_id=category_id,
    )


def create_transaction(
    transaction_repo: TransactionRepository,
    user_id: UUID,
    category_id: UUID | None,
    type: TransactionType,
    amount: Decimal,
    description: str | None,
    date: date,
):
    return transaction_repo.create(
        user_id=user_id,
        category_id=category_id,
        type=type,
        amount=amount,
        description=description,
        date=date,
    )


def update_transaction(
    transaction_repo: TransactionRepository,
    user_id: UUID,
    transaction_id: UUID,
    category_id: UUID | None,
    type: TransactionType,
    amount: Decimal,
    description: str | None,
    date: date,
):
    return transaction_repo.update(
        transaction_id=transaction_id,
        user_id=user_id,
        category_id=category_id,
        type=type,
        amount=amount,
        description=description,
        date=date,
    )


def delete_transaction(transaction_repo: TransactionRepository, user_id: UUID, transaction_id: UUID) -> bool:
    return transaction_repo.delete(transaction_id=transaction_id, user_id=user_id)
