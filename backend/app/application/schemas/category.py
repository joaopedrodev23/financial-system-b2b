from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.domain.entities.category import CategoryType


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    type: CategoryType


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    type: CategoryType


class CategoryOut(BaseModel):
    id: UUID
    name: str
    type: CategoryType
    created_at: datetime
    updated_at: datetime
