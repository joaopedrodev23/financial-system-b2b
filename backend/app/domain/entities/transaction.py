from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass(frozen=True)
class Transaction:
    id: UUID
    user_id: UUID
    category_id: UUID | None
    type: TransactionType
    amount: Decimal
    description: str | None
    date: date
    created_at: datetime
    updated_at: datetime
