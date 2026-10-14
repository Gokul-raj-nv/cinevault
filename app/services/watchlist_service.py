from sqlalchemy.orm import Session

from app.core.cache import delete as cache_delete
from app.repositories.movie_repo import MovieRepository
from app.repositories.watchlist_repo import WatchlistRepository


class WatchlistService:
    def __init__(self, db: Session):
        self.repo = WatchlistRepository(db)
        self.movie_repo = MovieRepository(db)

    def add_to_watchlist(self, user_id: int, movie_id: int):
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")

        if self.repo.is_in_watchlist(user_id, movie_id):
            raise ValueError("Movie is already in your watchlist")

        item = self.repo.add(user_id=user_id, movie_id=movie_id)
        cache_delete(f"recommendations:{user_id}")
        return item

    def remove_from_watchlist(self, user_id: int, movie_id: int):
        item = self.repo.get_item(user_id, movie_id)
        if not item:
            raise ValueError("Movie is not in your watchlist")
        self.repo.remove(item)
        cache_delete(f"recommendations:{user_id}")

    def get_watchlist(self, user_id: int):
        return self.repo.get_user_watchlist(user_id)

    def check_status(self, user_id: int, movie_id: int):
        return {
            "movie_id": movie_id,
            "in_watchlist": self.repo.is_in_watchlist(user_id, movie_id),
        }
