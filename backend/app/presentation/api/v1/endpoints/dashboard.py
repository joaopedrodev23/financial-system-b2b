from datetime import date
from fastapi import APIRouter, Depends, Query
from app.application.schemas.dashboard import DashboardSummary
from app.application.use_cases.dashboard.summary import get_dashboard_summary
from app.infrastructure.db.session import get_db
from app.infrastructure.db.repositories.transaction_repository_impl import TransactionRepositoryImpl
from app.presentation.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = TransactionRepositoryImpl(db)
    result = get_dashboard_summary(repo, current_user.id, start_date, end_date)
    return DashboardSummary(**result)
