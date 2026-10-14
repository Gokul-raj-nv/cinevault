from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db.base import Base

# Association table — no class needed, just a Table object
movie_actors = Table(
    "movie_actors",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True),
)
