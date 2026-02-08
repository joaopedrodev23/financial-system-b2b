from uuid import UUID
from fastapi import Depends, HTTPException, status
from jose import JWTError
from jose.exceptions import ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from app.core.config import get_settings
from app.infrastructure.db.session import get_db
from app.infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.security.jwt import decode_access_token

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_str}/auth/login")
UNAUTHORIZED_HEADERS = {"WWW-Authenticate": "Bearer"}


def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Valida o JWT e retorna o usuário associado ao token.
    try:
        payload = decode_access_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers=UNAUTHORIZED_HEADERS,
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers=UNAUTHORIZED_HEADERS,
        )
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers=UNAUTHORIZED_HEADERS,
        )
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers=UNAUTHORIZED_HEADERS,
        )
    try:
        user_id = UUID(subject)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers=UNAUTHORIZED_HEADERS,
        )
    user_repo = UserRepositoryImpl(db)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers=UNAUTHORIZED_HEADERS,
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo",
            headers=UNAUTHORIZED_HEADERS,
        )
    return user
