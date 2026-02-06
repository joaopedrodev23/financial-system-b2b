from datetime import date
from uuid import UUID
from app.domain.repositories.transaction_repository import TransactionRepository


def get_dashboard_summary(
    transaction_repo: TransactionRepository,
    user_id: UUID,
    start_date: date | None = None,
    end_date: date | None = None,
) -> dict:
    return transaction_repo.summary(user_id=user_id, start_date=start_date, end_date=end_date)
