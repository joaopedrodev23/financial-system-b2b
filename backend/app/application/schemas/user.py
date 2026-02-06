from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime
