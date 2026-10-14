from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.db.base import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=True)
    release_year = Column(Integer, nullable=True)
    runtime_minutes = Column(Integer, nullable=True)   # e.g. 152
    language = Column(String(50), default="English")
    poster_url = Column(String(500), nullable=True)
    embedding = Column(Vector(384), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Foreign key to Genre
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    genre = relationship("Genre", back_populates="movies")
    actors = relationship("Actor", secondary="movie_actors", back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", passive_deletes=True)
    watchlist_entries = relationship("Watchlist", back_populates="movie", passive_deletes=True)
    watch_history = relationship("WatchHistory", back_populates="movie", passive_deletes=True)
