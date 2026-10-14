from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    bio = Column(String(1000), nullable=True)

    # Many actors ↔ many movies
    movies = relationship("Movie", secondary="movie_actors", back_populates="actors")