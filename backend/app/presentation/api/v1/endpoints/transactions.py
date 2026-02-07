import csv
import io
from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from app.application.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from app.application.use_cases.transactions.crud import (
    create_transaction,
    delete_transaction,
    list_transactions,
    update_transaction,
)
from app.core.config import get_settings
from app.domain.entities.transaction import TransactionType
from app.infrastructure.db.session import get_db
from app.infrastructure.db.repositories.category_repository_impl import CategoryRepositoryImpl
from app.infrastructure.db.repositories.transaction_repository_impl import TransactionRepositoryImpl
from app.presentation.deps import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])
settings = get_settings()


def _validate_category(db, user_id, category_id: UUID | None):
    if not category_id:
        return
    category_repo = CategoryRepositoryImpl(db)
    category = category_repo.get_by_id(category_id, user_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria inválida")


@router.get("", response_model=list[TransactionOut])
def get_transactions(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    type: TransactionType | None = Query(default=None),
    category_id: UUID | None = Query(default=None),
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = TransactionRepositoryImpl(db)
    transactions = list_transactions(repo, current_user.id, start_date, end_date, type, category_id)
    return [TransactionOut(**t.__dict__) for t in transactions]


@router.post("", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create(data: TransactionCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    _validate_category(db, current_user.id, data.category_id)
    repo = TransactionRepositoryImpl(db)
    transaction = create_transaction(
        repo,
        current_user.id,
        data.category_id,
        data.type,
        data.amount,
        data.description,
        data.date,
    )
    return TransactionOut(**transaction.__dict__)


@router.put("/{transaction_id}", response_model=TransactionOut)
def update(transaction_id: UUID, data: TransactionUpdate, db=Depends(get_db), current_user=Depends(get_current_user)):
    _validate_category(db, current_user.id, data.category_id)
    repo = TransactionRepositoryImpl(db)
    transaction = update_transaction(
        repo,
        current_user.id,
        transaction_id,
        data.category_id,
        data.type,
        data.amount,
        data.description,
        data.date,
    )
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lançamento não encontrado")
    return TransactionOut(**transaction.__dict__)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(transaction_id: UUID, db=Depends(get_db), current_user=Depends(get_current_user)):
    repo = TransactionRepositoryImpl(db)
    success = delete_transaction(repo, current_user.id, transaction_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lançamento não encontrado")
    return None


@router.get("/export")
def export_csv(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    type: TransactionType | None = Query(default=None),
    category_id: UUID | None = Query(default=None),
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not settings.enable_csv_export:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Exportação CSV desativada")
    repo = TransactionRepositoryImpl(db)
    transactions = list_transactions(repo, current_user.id, start_date, end_date, type, category_id)

    def generate():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "categoria_id", "tipo", "valor", "descricao", "data"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for t in transactions:
            writer.writerow(
                [
                    str(t.id),
                    str(t.category_id) if t.category_id else "",
                    t.type.value,
                    f"{t.amount:.2f}",
                    t.description or "",
                    t.date.isoformat(),
                ]
            )
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    headers = {"Content-Disposition": "attachment; filename=transacoes.csv"}
    return StreamingResponse(generate(), media_type="text/csv", headers=headers)
