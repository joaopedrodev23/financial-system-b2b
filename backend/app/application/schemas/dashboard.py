from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    start_date: date | None
    end_date: date | None
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
