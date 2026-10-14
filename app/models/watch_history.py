from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class WatchHistory(Base):
    __tablename__ = "watch_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    watched_at = Column(DateTime, default=datetime.utcnow)
    last_position_seconds = Column(Integer, default=0)  # "continue watching" position

    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="uq_user_movie_history"),
    )

    user = relationship("User", back_populates="watch_history")
    movie = relationship("Movie", back_populates="watch_history")
