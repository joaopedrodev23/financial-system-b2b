from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
from app.domain.entities.transaction import TransactionType


class TransactionCreate(BaseModel):
    category_id: UUID | None = None
    type: TransactionType
    amount: Decimal = Field(gt=0)
    description: str | None = Field(default=None, max_length=255)
    date: date


class TransactionUpdate(BaseModel):
    category_id: UUID | None = None
    type: TransactionType
    amount: Decimal = Field(gt=0)
    description: str | None = Field(default=None, max_length=255)
    date: date


class TransactionOut(BaseModel):
    id: UUID
    category_id: UUID | None
    type: TransactionType
    amount: Decimal
    description: str | None
    date: date
    created_at: datetime
    updated_at: datetime
