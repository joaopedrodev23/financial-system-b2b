from datetime import date
from decimal import Decimal
from typing import Protocol
from uuid import UUID
from app.domain.entities.transaction import Transaction, TransactionType


class TransactionRepository(Protocol):
    def list_by_user(
        self,
        user_id: UUID,
        start_date: date | None = None,
        end_date: date | None = None,
        type: TransactionType | None = None,
        category_id: UUID | None = None,
    ) -> list[Transaction]:
        ...

    def get_by_id(self, transaction_id: UUID, user_id: UUID) -> Transaction | None:
        ...

    def create(
        self,
        user_id: UUID,
        category_id: UUID | None,
        type: TransactionType,
        amount: Decimal,
        description: str | None,
        date: date,
    ) -> Transaction:
        ...

    def update(
        self,
        transaction_id: UUID,
        user_id: UUID,
        category_id: UUID | None,
        type: TransactionType,
        amount: Decimal,
        description: str | None,
        date: date,
    ) -> Transaction | None:
        ...

    def delete(self, transaction_id: UUID, user_id: UUID) -> bool:
        ...

    def summary(
        self,
        user_id: UUID,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> dict:
        ...
