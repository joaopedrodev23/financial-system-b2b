import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from app.core.config import get_settings
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine
from app.infrastructure.db import models  # noqa: F401
from app.presentation.api.v1.router import api_router

settings = get_settings()
logger = logging.getLogger("app.startup")

app = FastAPI(title=settings.project_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _translate_validation_error(err: dict) -> str:
    err_type = err.get("type", "")
    if err_type == "missing":
        return "Campo obrigatório"
    if err_type == "value_error.email":
        return "E-mail inválido"
    if err_type == "string_too_short":
        return "Texto muito curto"
    if err_type == "string_too_long":
        return "Texto muito longo"
    if err_type in ("greater_than", "greater_than_equal"):
        return "Valor abaixo do mínimo permitido"
    if err_type in ("less_than", "less_than_equal"):
        return "Valor acima do máximo permitido"
    return "Valor inválido"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append({"loc": err.get("loc"), "msg": _translate_validation_error(err), "type": err.get("type")})
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": errors})


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED and exc.detail == "Not authenticated":
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "Não autenticado"},
            headers=exc.headers,
        )
    return await http_exception_handler(request, exc)


@app.on_event("startup")
def on_startup():
    logger.info("Starting %s (%s)", settings.project_name, settings.environment)
    logger.info(
        "Database: %s:%s/%s | auto_create_db=%s",
        settings.postgres_host,
        settings.postgres_port,
        settings.postgres_db,
        settings.auto_create_db,
    )
    # Para MVP: cria as tabelas automaticamente se não existirem.
    if settings.auto_create_db:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema ensured (auto_create_db=true)")


app.include_router(api_router, prefix=settings.api_v1_str)
