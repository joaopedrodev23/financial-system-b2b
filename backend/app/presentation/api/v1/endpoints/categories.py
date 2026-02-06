from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from app.application.use_cases.categories.crud import create_category, delete_category, list_categories, update_category
from app.infrastructure.db.session import get_db
from app.infrastructure.db.repositories.category_repository_impl import CategoryRepositoryImpl
from app.presentation.deps import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def get_categories(db=Depends(get_db), current_user=Depends(get_current_user)):
    repo = CategoryRepositoryImpl(db)
    categories = list_categories(repo, current_user.id)
    return [CategoryOut(**c.__dict__) for c in categories]


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create(data: CategoryCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    repo = CategoryRepositoryImpl(db)
    category = create_category(repo, current_user.id, data.name, data.type)
    return CategoryOut(**category.__dict__)


@router.put("/{category_id}", response_model=CategoryOut)
def update(category_id: UUID, data: CategoryUpdate, db=Depends(get_db), current_user=Depends(get_current_user)):
    repo = CategoryRepositoryImpl(db)
    category = update_category(repo, current_user.id, category_id, data.name, data.type)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    return CategoryOut(**category.__dict__)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(category_id: UUID, db=Depends(get_db), current_user=Depends(get_current_user)):
    repo = CategoryRepositoryImpl(db)
    success = delete_category(repo, current_user.id, category_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    return None
