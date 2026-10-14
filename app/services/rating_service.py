from sqlalchemy.orm import Session

from app.core.cache import delete as cache_delete
from app.repositories.movie_repo import MovieRepository
from app.repositories.rating_repo import RatingRepository
from app.schemas.rating import RatingCreate


class RatingService:
    def __init__(self, db: Session):
        self.repo = RatingRepository(db)
        self.movie_repo = MovieRepository(db)

    def rate_movie(self, user_id: int, data: RatingCreate):
        # Verify movie exists
        movie = self.movie_repo.get_by_id(data.movie_id)
        if not movie:
            raise ValueError(f"Movie {data.movie_id} not found")

        rating = self.repo.upsert(
            user_id=user_id,
            movie_id=data.movie_id,
            rating=data.rating,
        )
        cache_delete(
            "movies:trending",
            f"movies:{data.movie_id}",
            f"recommendations:{user_id}",
        )
        return rating

    def get_movie_stats(self, movie_id: int):
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")
        stats = self.repo.get_movie_stats(movie_id)
        return {"movie_id": movie_id, **stats}

    def get_my_rating(self, user_id: int, movie_id: int):
        return self.repo.get_user_rating(user_id, movie_id)
