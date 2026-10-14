import os

# These must be configured before importing any application module.
os.environ.setdefault("DATABASE_URL", "postgresql://cinevault:secret@localhost:5432/cinevault_test")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("CACHE_ENABLED", "false")
os.environ.setdefault("SEMANTIC_SEARCH_ENABLED", "false")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

import app.models  # noqa: F401 - registers every model with SQLAlchemy metadata
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine, get_db
from app.main import app
from app.models.user import User


@pytest.fixture(autouse=True)
def reset_database():
    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_headers(client):
    db = SessionLocal()
    admin = User(
        name="Admin",
        email="admin@example.com",
        password_hash=hash_password("strong-password"),
        is_admin=True,
    )
    db.add(admin)
    db.commit()
    db.close()

    response = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "strong-password"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_headers(client):
    response = client.post(
        "/auth/register",
        json={"name": "Viewer", "email": "viewer@example.com", "password": "strong-password"},
    )
    assert response.status_code == 201
    response = client.post(
        "/auth/login",
        json={"email": "viewer@example.com", "password": "strong-password"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
