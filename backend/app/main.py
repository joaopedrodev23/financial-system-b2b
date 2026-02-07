import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
