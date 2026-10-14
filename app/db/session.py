from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
import app.models  # Register every ORM model before SQLAlchemy configures relationships.

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # test connection before using it
    pool_size=10,             # max 10 connections in pool
    max_overflow=20,          # allow 20 extra connections during spikes
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """FastAPI dependency — yields a DB session, always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
