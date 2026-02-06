from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    BOTH = "both"


@dataclass(frozen=True)
class Category:
    id: UUID
    user_id: UUID
    name: str
    type: CategoryType
    created_at: datetime
    updated_at: datetime
