from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.application.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.application.schemas.user import UserOut
from app.application.use_cases.auth.authenticate import authenticate_user
from app.application.use_cases.auth.register import register_user
from app.core.config import get_settings
from app.infrastructure.db.session import get_db
from app.infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.security.jwt import create_access_token
from app.infrastructure.security.password import get_password_hash, verify_password
from app.presentation.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db=Depends(get_db)):
    user_repo = UserRepositoryImpl(db)
    try:
        user = register_user(user_repo, data.email, data.password, get_password_hash)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado")
    return UserOut(**user.__dict__)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db=Depends(get_db)):
    user_repo = UserRepositoryImpl(db)
    if settings.demo_mode and data.email == settings.demo_email and data.password == settings.demo_password:
        user = user_repo.get_by_email(data.email)
        if user and not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário inativo")
        if not user:
            try:
                user = user_repo.create(email=data.email, hashed_password=get_password_hash(data.password))
            except IntegrityError:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado")
        token = create_access_token(subject=str(user.id), expires_minutes=settings.access_token_expire_minutes)
        return TokenResponse(access_token=token, expires_in=settings.access_token_expire_minutes * 60)
    user = authenticate_user(user_repo, data.email, data.password, verify_password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token(subject=str(user.id), expires_minutes=settings.access_token_expire_minutes)
    return TokenResponse(access_token=token, expires_in=settings.access_token_expire_minutes * 60)


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return UserOut(**current_user.__dict__)
