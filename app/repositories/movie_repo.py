from typing import Optional

from sqlalchemy import case, func
from sqlalchemy.orm import Session, joinedload

from app.models.movie import Movie
from app.models.rating import Rating


class MovieRepository:
    """All database access for Movie records lives in this class."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        genre_id: Optional[int] = None,
        search: Optional[str] = None,
        language: Optional[str] = None,
    ) -> tuple[int, list[Movie]]:
        query = self.db.query(Movie).options(joinedload(Movie.genre))

        if genre_id is not None:
            query = query.filter(Movie.genre_id == genre_id)
        if language:
            query = query.filter(Movie.language == language)
        if search:
            query = query.filter(Movie.title.ilike(f"%{search.strip()}%"))

        total = query.count()
        movies = (
            query.order_by(Movie.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return total, movies

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return (
            self.db.query(Movie)
            .options(joinedload(Movie.genre), joinedload(Movie.actors))
            .filter(Movie.id == movie_id)
            .first()
        )

    def create(self, **kwargs) -> Movie:
        movie = Movie(**kwargs)
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update(self, movie: Movie, **kwargs) -> Movie:
        for key, value in kwargs.items():
            setattr(movie, key, value)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie: Movie) -> None:
        self.db.delete(movie)
        self.db.commit()

    def get_average_rating(self, movie_id: int) -> Optional[float]:
        average = (
            self.db.query(func.avg(Rating.rating))
            .filter(Rating.movie_id == movie_id)
            .scalar()
        )
        return round(float(average), 2) if average is not None else None

    def get_trending(self, limit: int = 10) -> list[Movie]:
        """Most-rated movies, retaining ranking order; newest movies are a fallback."""
        ranked_ids = (
            self.db.query(Rating.movie_id)
            .group_by(Rating.movie_id)
            .order_by(func.count(Rating.id).desc(), func.avg(Rating.rating).desc())
            .limit(limit)
            .all()
        )
        ids = [row[0] for row in ranked_ids]

        if not ids:
            return (
                self.db.query(Movie)
                .options(joinedload(Movie.genre))
                .order_by(Movie.created_at.desc())
                .limit(limit)
                .all()
            )

        ranking = case({movie_id: position for position, movie_id in enumerate(ids)}, value=Movie.id)
        return (
            self.db.query(Movie)
            .options(joinedload(Movie.genre))
            .filter(Movie.id.in_(ids))
            .order_by(ranking)
            .all()
        )

    def search_by_embedding(self, embedding: list[float], limit: int) -> list[tuple[Movie, float]]:
        """Return nearest movies using pgvector cosine distance (smaller is better)."""
        distance = Movie.embedding.cosine_distance(embedding)
        rows = (
            self.db.query(Movie, distance.label("distance"))
            .options(joinedload(Movie.genre))
            .filter(Movie.embedding.is_not(None))
            .order_by(distance)
            .limit(limit)
            .all()
        )
        return [(movie, float(movie_distance)) for movie, movie_distance in rows]
