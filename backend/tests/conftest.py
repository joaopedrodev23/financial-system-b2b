import os

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Ensure settings come from environment (avoid .env BOM issues).
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("POSTGRES_USER", "finance_user")
os.environ.setdefault("POSTGRES_PASSWORD", "finance_pass")
os.environ.setdefault("POSTGRES_DB", "finance_db")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")

from app.core import config as app_config

app_config.Settings.model_config["env_file"] = None
app_config.get_settings.cache_clear()

from app.core.config import get_settings
from app.infrastructure.db.session import get_db
from app.main import app

settings = get_settings()
API_PREFIX = settings.api_v1_str


@pytest.fixture(scope="session")
def api_prefix():
    return API_PREFIX


@pytest.fixture(scope="session")
def db_engine():
    return create_engine(settings.database_url, pool_pre_ping=True)


@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection, autocommit=False, autoflush=False)
    session = SessionLocal()
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        if trans.nested and not trans._parent.nested:
            sess.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
